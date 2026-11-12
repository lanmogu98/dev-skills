"""Small, explicit figure model; shared geometry, not automatic graph layout."""

from dataclasses import dataclass
from pathlib import Path
import json
import math
import re
import subprocess
import sys
from typing import Callable
import xml.etree.ElementTree as ET


Number = float | Callable[[], float]
SVG = "http://www.w3.org/2000/svg"
MODEL_ID = "research-geometry"
ET.register_namespace("", SVG)


def value(number: Number) -> float:
    result = float(number() if callable(number) else number)
    if not math.isfinite(result):
        raise ValueError("Figure coordinates must be finite")
    return result


def element(parent, tag, **attributes):
    return ET.SubElement(parent, f"{{{SVG}}}{tag}", {
        key.replace("_", "-"): f"{val:g}" if isinstance(val, (int, float)) else str(val)
        for key, val in attributes.items() if val is not None
    })


@dataclass
class Box:
    id: str
    x: Number
    y: Number
    w: Number
    h: Number
    parent: "Box | None" = None
    role: str = "node"
    fill: str = "#ffffff"
    stroke: str = "#64748b"
    radius: float = 6
    glyph: str = "box"
    padding: float = 7

    @property
    def left(self):
        return (self.parent.left if self.parent else 0) + value(self.x)

    @property
    def top(self):
        return (self.parent.top if self.parent else 0) + value(self.y)

    @property
    def width(self):
        return value(self.w)

    @property
    def height(self):
        return value(self.h)

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def cx(self):
        return (self.left + self.right) / 2

    @property
    def cy(self):
        return (self.top + self.bottom) / 2

    def port(self, side, fraction=0.5):
        if side not in {"north", "south", "east", "west"} or not 0 <= fraction <= 1:
            raise ValueError("Use north/south/east/west and a fraction from 0 to 1")
        return Port(self, side, fraction)


@dataclass
class Port:
    box: Box
    side: str
    fraction: float

    def point(self):
        b, f = self.box, self.fraction
        return {
            "north": (b.left + b.width*f, b.top),
            "south": (b.left + b.width*f, b.bottom),
            "west": (b.left, b.top + b.height*f),
            "east": (b.right, b.top + b.height*f),
        }[self.side]

    def record(self):
        return {"object": self.box.id, "side": self.side, "fraction": self.fraction}


@dataclass
class Label:
    id: str
    text: str
    x: Number
    y: Number
    parent: Box | None
    owner: Box | None
    size: float
    weight: int
    anchor: str
    color: str

    @property
    def left(self):
        return (self.parent.left if self.parent else 0) + value(self.x)

    @property
    def baseline(self):
        return (self.parent.top if self.parent else 0) + value(self.y)


@dataclass
class Edge:
    id: str
    source: Port
    target: Port
    via: list | Callable | None
    via_x: Number | None
    via_y: Number | None
    color: str
    dashed: bool
    width: float
    arrow: bool

    def points(self):
        start, end = self.source.point(), self.target.point()
        if self.via_x is not None:
            x = value(self.via_x)
            middle = [(x, start[1]), (x, end[1])]
        elif self.via_y is not None:
            y = value(self.via_y)
            middle = [(start[0], y), (end[0], y)]
        else:
            middle = self.via() if callable(self.via) else self.via or []
        points = []
        for x, y in [start, *middle, end]:
            point = (value(x), value(y))
            if not points or point != points[-1]:
                points.append(point)
        return points


class Figure:
    def __init__(self, width, height, *, title, description, min_font_px=14,
                 font_family="Source Sans 3"):
        self.width, self.height = float(width), float(height)
        self.title, self.description = title, description
        self.min_font_px, self.font_family = min_font_px, font_family
        self.boxes, self.labels, self.edges, self.constraints = [], [], [], []
        self._ids = {MODEL_ID, "regions", "routes", "objects", "labels", "background"}

    def _reserve(self, identifier):
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", identifier) or identifier in self._ids:
            raise ValueError(f"Invalid or duplicate figure ID: {identifier}")
        self._ids.add(identifier)

    def _require_box(self, box):
        if box is not None and not any(box is existing for existing in self.boxes):
            raise ValueError(f"Object {box.id!r} is not registered in this Figure")

    def region(self, identifier, *, x, y, w, h, parent=None, title=None,
               fill="#f8fafc", stroke="#cbd5e1", radius=8, padding=7):
        box = self._box(identifier, x, y, w, h, parent, "region", fill, stroke, radius, "box", padding)
        if title:
            self.label(f"{identifier}-title", title, x=12, y=27, parent=box,
                       size=18, weight=600, anchor="start")
        return box

    def _box(self, identifier, x, y, w, h, parent, role, fill, stroke, radius, glyph, padding):
        self._require_box(parent)
        self._reserve(identifier)
        self._reserve(f"{identifier}-surface")
        if glyph not in {"box", "collection", "pill"}:
            raise ValueError("Supported glyphs: box, collection, pill")
        box = Box(identifier, x, y, w, h, parent, role, fill, stroke, radius, glyph, padding)
        self.boxes.append(box)
        return box

    def node(self, identifier, primary, *, x, y, w, h, secondary="", parent=None,
             fill="#ffffff", stroke="#64748b", glyph="box", padding=7):
        box = self._box(identifier, x, y, w, h, parent, "node", fill, stroke, 6, glyph, padding)
        primary = primary.splitlines() if isinstance(primary, str) else primary
        secondary = secondary.splitlines() if isinstance(secondary, str) else secondary
        lines = [(line, 16, 600, "primary") for line in primary]
        lines += [(line, 14, 400, "secondary") for line in secondary]
        for index, (text, size, weight, role) in enumerate(lines):
            self.label(f"{identifier}-{role}-{index}", text, x=lambda b=box: b.width/2,
                       y=lambda i=index, n=len(lines), b=box: b.height/2 - (n-1)*19/2 + 5 + i*19,
                       parent=box, size=size, weight=weight)
        return box

    def label(self, identifier, text, *, x, y, parent=None, owner=None, size=16,
              weight=400, anchor="middle", color="#0f172a"):
        self._require_box(parent)
        self._require_box(owner)
        self._reserve(identifier)
        if "\n" in text or anchor not in {"start", "middle", "end"}:
            raise ValueError("Use one label per line and start/middle/end anchors")
        label = Label(identifier, text, x, y, parent, owner or parent, size, weight, anchor, color)
        self.labels.append(label)
        return label

    def align(self, attribute, reference, *others):
        axes = {"left": "x", "right": "x", "cx": "x", "top": "y", "bottom": "y", "cy": "y", "baseline": "y"}
        if attribute not in axes:
            raise ValueError(f"Unsupported alignment: {attribute}")
        axis = axes[attribute]
        for other in others:
            offset = {"right": lambda o=other: o.width, "cx": lambda o=other: o.width/2,
                      "bottom": lambda o=other: o.height, "cy": lambda o=other: o.height/2}.get(attribute, lambda: 0)
            setattr(other, axis, lambda o=other, d=offset: getattr(reference, attribute) -
                    (getattr(o.parent, "left" if axis == "x" else "top") if o.parent else 0) - d())
        self.constraints.append({"attribute": attribute, "objects": [reference.id, *(o.id for o in others)]})

    def same_size(self, reference, *others, width=False, height=False):
        for attribute, field, enabled in (("width", "w", width), ("height", "h", height)):
            if enabled:
                for other in others:
                    setattr(other, field, lambda a=attribute: getattr(reference, a))
                self.constraints.append({"attribute": attribute, "objects": [reference.id, *(o.id for o in others)]})

    def connect(self, identifier, source, target, *, via=None, via_x=None, via_y=None,
                color="#475569", dashed=False, width=1.7, arrow=True):
        if not isinstance(source, Port) or not isinstance(target, Port):
            raise ValueError("Connections require box.port(...) endpoints")
        self._require_box(source.box)
        self._require_box(target.box)
        self._reserve(identifier)
        self._reserve(f"{identifier}-arrow")
        if sum(v is not None for v in (via, via_x, via_y)) > 1:
            raise ValueError("Choose via, via_x or via_y")
        edge = Edge(identifier, source, target, via, via_x, via_y, color, dashed, width, arrow)
        self.edges.append(edge)
        return edge

    def write(self, path):
        root = ET.Element(f"{{{SVG}}}svg", width=str(self.width), height=str(self.height),
                          viewBox=f"0 0 {self.width:g} {self.height:g}")
        element(root, "title").text = self.title
        element(root, "desc").text = self.description
        model = {"version": 1, "min_font_px": self.min_font_px,
                 "objects": [{"id": b.id, "surface": f"{b.id}-surface", "role": b.role,
                              "parent": b.parent.id if b.parent else None, "padding": b.padding}
                             for b in self.boxes],
                 "labels": [{"id": t.id, "owner": t.owner.id if t.owner else None} for t in self.labels],
                 "edges": [{"id": e.id, "source": e.source.record(), "target": e.target.record()}
                           for e in self.edges], "constraints": self.constraints}
        element(root, "metadata", id=MODEL_ID).text = json.dumps(model)
        defs = element(root, "defs")
        for edge in self.edges:
            if edge.arrow:
                marker = element(defs, "marker", id=f"{edge.id}-arrow", viewBox="0 0 8 8",
                                 refX=8, refY=4, markerWidth=8, markerHeight=8,
                                 markerUnits="userSpaceOnUse", orient="auto")
                element(marker, "path", d="M 0 0 L 8 4 L 0 8 Z", fill=edge.color)
        element(root, "rect", id="background", x=0, y=0, width=self.width, height=self.height, fill="#ffffff")
        groups = {name: element(root, "g", id=name) for name in ("regions", "routes", "objects", "labels")}
        for box in self.boxes:
            if box.width <= 0 or box.height <= 0:
                raise ValueError(f"Nonpositive size: {box.id}")
            group = element(groups["regions" if box.role == "region" else "objects"], "g", id=box.id)
            if box.glyph == "collection":
                for offset in (8, 4):
                    element(group, "rect", x=box.left-offset, y=box.top-offset,
                            width=box.width, height=box.height, rx=box.radius,
                            fill=box.fill, stroke=box.stroke, stroke_width=1.2)
            element(group, "rect", id=f"{box.id}-surface", x=box.left, y=box.top,
                    width=box.width, height=box.height,
                    rx=box.height/2 if box.glyph == "pill" else box.radius,
                    fill=box.fill, stroke=box.stroke, stroke_width=1.2)
        for edge in self.edges:
            points = edge.points()
            data = " ".join(f"{'M' if i == 0 else 'L'} {x:g} {y:g}" for i, (x, y) in enumerate(points))
            element(groups["routes"], "path", id=edge.id, d=data, fill="none", stroke=edge.color,
                    stroke_width=edge.width, stroke_dasharray="6 4" if edge.dashed else None,
                    marker_end=f"url(#{edge.id}-arrow)" if edge.arrow else None)
        for label in self.labels:
            element(groups["labels"], "text", id=label.id, x=label.left, y=label.baseline,
                    font_family=self.font_family, font_size=label.size, font_weight=label.weight,
                    text_anchor=label.anchor, fill=label.color).text = label.text
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
        return path

    def export(self, output, *, width=720, font_dir=None, profile=None):
        output = Path(output).resolve()
        source = self.write(f"{output}.source.svg")
        command = [sys.executable, str(Path(__file__).with_name("render_svg.py")), "render",
                   str(source), "--output", str(output), "--width", str(width)]
        for option, setting in (("--font-dir", font_dir), ("--profile", profile)):
            if setting is not None:
                command += [option, str(setting)]
        subprocess.run(command, check=True)
        return Path(f"{output}.png")
