"""Measure and check the builder's flat SVG subset in an isolated font process."""

import argparse
from collections import Counter
import ctypes as C
import ctypes.util
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


NS = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", NS[1:-1])


class Rectangle(C.Structure):
    _fields_ = [(key, C.c_double) for key in ("x", "y", "width", "height")]


class Measurement:
    def __init__(self, source, width, height):
        self.lib = C.CDLL(ctypes.util.find_library("rsvg-2") or "librsvg-2.so.2")
        self.gobject = C.CDLL(ctypes.util.find_library("gobject-2.0") or "libgobject-2.0.so.0")
        self.lib.rsvg_handle_new_from_file.argtypes = [C.c_char_p, C.POINTER(C.c_void_p)]
        self.lib.rsvg_handle_new_from_file.restype = C.c_void_p
        self.lib.rsvg_handle_set_dpi.argtypes = [C.c_void_p, C.c_double]
        self.lib.rsvg_handle_get_geometry_for_layer.argtypes = [C.c_void_p, C.c_char_p,
            C.POINTER(Rectangle), C.POINTER(Rectangle), C.POINTER(Rectangle), C.POINTER(C.c_void_p)]
        self.lib.rsvg_handle_get_geometry_for_layer.restype = C.c_int
        self.gobject.g_object_unref.argtypes = [C.c_void_p]
        error = C.c_void_p()
        self.handle = self.lib.rsvg_handle_new_from_file(str(source).encode(), C.byref(error))
        if not self.handle or error.value:
            raise ValueError("librsvg could not load the candidate SVG")
        self.lib.rsvg_handle_set_dpi(self.handle, 96)
        self.viewport = Rectangle(0, 0, width, height)
        self.version = ".".join(str(C.c_uint.in_dll(self.lib, f"rsvg_{part}_version").value)
                                for part in ("major", "minor", "micro"))

    def box(self, identifier):
        ink, logical, error = Rectangle(), Rectangle(), C.c_void_p()
        ok = self.lib.rsvg_handle_get_geometry_for_layer(self.handle, ("#"+identifier).encode(),
             C.byref(self.viewport), C.byref(ink), C.byref(logical), C.byref(error))
        if not ok or error.value:
            raise ValueError(f"Cannot measure SVG object: {identifier}")
        return [getattr(ink, key) for key in ("x", "y", "width", "height")]

    def close(self):
        self.gobject.g_object_unref(self.handle)


def overlaps(a, b, margin=0):
    return (max(a[0], b[0])-margin < min(a[0]+a[2], b[0]+b[2])-0.01 and
            max(a[1], b[1])-margin < min(a[1]+a[3], b[1]+b[3])-0.01)


def contains(outer, inner, padding=0):
    return (inner[0] >= outer[0]+padding-0.05 and inner[1] >= outer[1]+padding-0.05 and
            inner[0]+inner[2] <= outer[0]+outer[2]-padding+0.05 and
            inner[1]+inner[3] <= outer[1]+outer[3]-padding+0.05)


def points(data):
    tokens = re.findall(r"[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", data)
    result, index, x, y = [], 0, 0., 0.
    while index < len(tokens):
        command = tokens[index]
        index += 1
        if command not in {"M", "L", "H", "V"}:
            raise ValueError("Only explicit M/L/H/V routes are checked")
        if (not result and command != "M") or (result and command == "M"):
            raise ValueError("A route must have one initial M and one continuous subpath")
        count = 2 if command in {"M", "L"} else 1
        values = list(map(float, tokens[index:index+count]))
        if len(values) != count:
            raise ValueError("Incomplete route")
        index += count
        if count == 2:
            x, y = values
        elif command == "H":
            x = values[0]
        else:
            y = values[0]
        if not result or result[-1] != (x, y):
            result.append((x, y))
    if len(result) < 2 or any(a[0] != b[0] and a[1] != b[1] for a, b in zip(result, result[1:])):
        raise ValueError("Use nonempty straight or orthogonal routes")
    return result


def strips(route, stroke):
    half = stroke/2
    return [[min(a[0], b[0])-half, min(a[1], b[1])-half,
             abs(a[0]-b[0])+stroke, abs(a[1]-b[1])+stroke]
            for a, b in zip(route, route[1:])]


def triangle_hits(triangle, box):
    rectangle = [(box[0], box[1]), (box[0]+box[2], box[1]),
                 (box[0]+box[2], box[1]+box[3]), (box[0], box[1]+box[3])]
    axes = [(1, 0), (0, 1)] + [(b[1]-a[1], a[0]-b[0]) for a, b in zip(triangle, triangle[1:]+triangle[:1])]
    for x, y in axes:
        first = [a*x+b*y for a, b in triangle]
        second = [a*x+b*y for a, b in rectangle]
        if max(min(first), min(second)) >= min(max(first), max(second))-0.01:
            return False
    return True


def rect(element):
    return [float(element.attrib[key]) for key in ("x", "y", "width", "height")]


def analyze(source, display_width, debug):
    tree = ET.parse(source)
    root = tree.getroot()
    vx, vy, width, height = map(float, root.attrib["viewBox"].split())
    if vx or vy or width <= 0 or height <= 0:
        raise ValueError("Geometry checks require a positive viewBox starting at 0 0")
    metadata = root.find(f"{NS}metadata[@id='research-geometry']")
    model = json.loads(metadata.text) if metadata is not None else None
    errors, warnings = [], []

    def issue(kind, identifiers, message, bounds=None, severity="error", **details):
        (errors if severity == "error" else warnings).append(
            {"kind": kind, "objects": identifiers, "message": message, "bounds": bounds, **details})

    counts = Counter(e.attrib["id"] for e in root.iter() if "id" in e.attrib)
    for identifier, count in counts.items():
        if count > 1:
            issue("duplicate_id", [identifier], "IDs must identify one visible object")
    elements = {e.attrib["id"]: e for e in root.iter() if "id" in e.attrib}
    unsupported = [e.tag.rsplit("}", 1)[-1] for e in root.iter()
                   if any(k in e.attrib for k in ("transform", "clip-path", "mask", "filter", "style", "marker-start", "marker-mid")) or
                   e.tag.rsplit("}", 1)[-1] in {"style", "use", "foreignObject", "clipPath", "mask", "filter", "tspan", "textPath"}]
    if unsupported:
        issue("unsupported_geometry", [], "Transforms, CSS, clipping and custom masks are outside this check", elements=unsupported)
    if model and model.get("version") != 1:
        raise ValueError("Unsupported figure model version")
    if model:
        try:
            intrinsic_width, intrinsic_height = float(root.attrib["width"]), float(root.attrib["height"])
            same_aspect = intrinsic_width > 0 and intrinsic_height > 0 and abs(intrinsic_width/intrinsic_height-width/height) < 1e-6
        except (ValueError, KeyError):
            same_aspect = False
        if not same_aspect:
            issue("unsupported_viewport", [], "Managed width/height must be numeric and match the viewBox aspect ratio; font scaling would otherwise be ambiguous")
    measurement = Measurement(source, width, height)
    try:
        labels = {e.attrib["id"]: measurement.box(e.attrib["id"]) for e in root.iter(NS+"text") if "id" in e.attrib}
        if any("id" not in e.attrib for e in root.iter(NS+"text")):
            issue("unregistered_text", [], "Every text object needs a stable ID")
        objects = {o["id"]: o for o in model["objects"]} if model else {}
        owned = {t["id"]: t.get("owner") for t in model["labels"]} if model else {}
        object_ink = {key: measurement.box(key) for key in objects}
        surfaces = {key: rect(elements[obj["surface"]]) for key, obj in objects.items()}
        if model:
            for identifier in labels.keys() ^ owned.keys():
                issue("unregistered_text", [identifier], "Visible text and model labels must agree")
            parents = {child: parent for parent in root.iter() for child in parent}
            for node in root.iter():
                if node.tag.rsplit("}", 1)[-1] not in {"rect", "path", "circle", "ellipse", "line", "polyline", "polygon", "image"}:
                    continue
                chain, parent = set(), node
                while parent in parents:
                    parent = parents[parent]
                    chain.add(parent.get("id"))
                    if parent.tag == NS+"defs":
                        break
                if parent.tag == NS+"defs" or chain & objects.keys():
                    continue
                if node.get("id") != "background" and node.get("id") not in {e["id"] for e in model["edges"]}:
                    issue("unregistered_object", [node.get("id", "(missing id)")], "Visible geometry must belong to a registered object or route")

        def ancestors(identifier):
            result = set()
            while identifier in objects and objects[identifier].get("parent"):
                identifier = objects[identifier]["parent"]
                if identifier in result:
                    raise ValueError("Cyclic containment")
                result.add(identifier)
            return result

        minimum = model.get("min_font_px", 14) if model else 14
        for identifier, bounds in labels.items():
            font = elements[identifier].get("font-size", "")
            if not re.fullmatch(r"\d+(?:\.\d+)?(?:px)?", font):
                issue("unsupported_font_size", [identifier], "Use an explicit numeric font size", bounds)
            else:
                effective = float(font.removesuffix("px"))*display_width/width
                if effective < minimum-0.01:
                    issue("small_font", [identifier], "Font is too small at the target display width", bounds,
                          effective_px=effective, minimum_px=minimum)
            if not contains([0, 0, width, height], bounds):
                issue("canvas_overflow", [identifier], "Text exceeds the canvas", bounds)
            owner = owned.get(identifier)
            if owner:
                if owner not in objects:
                    issue("missing_owner", [identifier, owner], "Text owner does not exist", bounds)
                elif not contains(surfaces[owner], bounds, objects[owner]["padding"]):
                    issue("label_overflow", [identifier, owner], "Measured text does not fit with the declared padding", bounds,
                          container=surfaces[owner])

        for identifier, bounds in object_ink.items():
            if not contains([0, 0, width, height], bounds):
                issue("canvas_overflow", [identifier], "Object exceeds the canvas", bounds)
            parent = objects[identifier].get("parent")
            if parent and (parent not in surfaces or not contains(surfaces[parent], bounds, objects[parent]["padding"])):
                issue("object_overflow", [identifier, parent], "Object exceeds its declared parent or padding", bounds)
        ids = list(objects)
        for index, first in enumerate(ids):
            for second in ids[index+1:]:
                if first not in ancestors(second) and second not in ancestors(first) and overlaps(object_ink[first], object_ink[second]):
                    issue("object_overlap", [first, second], "Unrelated object bounds overlap", object_ink[second])
        ids = list(labels)
        for index, first in enumerate(ids):
            for second in ids[index+1:]:
                if overlaps(labels[first], labels[second]):
                    issue("label_overlap", [first, second], "Measured label bounds overlap", labels[second])
            for other in objects:
                owner = owned.get(first)
                if other != owner and other not in ancestors(owner) and overlaps(labels[first], object_ink[other]):
                    issue("label_object_overlap", [first, other], "Label overlaps an unrelated object", labels[first])

        for constraint in model["constraints"] if model else []:
            attribute, ids = constraint["attribute"], constraint["objects"]
            values = []
            for identifier in ids:
                if attribute == "baseline":
                    values.append(float(elements[identifier].attrib["y"]))
                else:
                    x, y, w, h = surfaces[identifier]
                    values.append({"left": x, "right": x+w, "cx": x+w/2, "top": y,
                                   "bottom": y+h, "cy": y+h/2, "width": w, "height": h}[attribute])
            if max(values)-min(values) > 0.05:
                issue("alignment", ids, f"Declared {attribute} equality is broken", actual=values, attribute=attribute)

        edges = {e["id"]: e for e in model["edges"]} if model else {}
        routes = [elements[key] for key in edges] if model else [e for e in root.iter(NS+"path") if "id" in e.attrib]
        checked_routes = 0
        for path in routes:
            identifier = path.attrib["id"]
            try:
                route = points(path.attrib["d"])
            except ValueError as error:
                issue("unsupported_route", [identifier], str(error))
                continue
            checked_routes += 1
            parts = strips(route, float(path.get("stroke-width", 1.7)))
            triangle = None
            if model and path.get("marker-end"):
                reference = re.fullmatch(r"url\(#([A-Za-z][A-Za-z0-9_.-]*)\)", path.get("marker-end"))
                marker = elements.get(reference[1]) if reference else None
                expected_marker = {"viewBox": "0 0 8 8", "refX": "8", "refY": "4", "markerWidth": "8",
                                   "markerHeight": "8", "markerUnits": "userSpaceOnUse", "orient": "auto"}
                if (marker is None or marker.tag != NS+"marker" or
                        any(marker.get(key) != setting for key, setting in expected_marker.items()) or
                        len(marker) != 1 or marker[0].get("d") != "M 0 0 L 8 4 L 0 8 Z"):
                    issue("unsupported_marker", [identifier], "Use the builder's arrow marker")
                else:
                    a, tip = route[-2:]
                    dx, dy = tip[0]-a[0], tip[1]-a[1]
                    scale = abs(dx)+abs(dy)
                    dx, dy = dx/scale, dy/scale
                    triangle = [tip, (tip[0]-8*dx+4*dy, tip[1]-8*dy-4*dx),
                                (tip[0]-8*dx-4*dy, tip[1]-8*dy+4*dx)]
            if model:
                for name, index, neighbor in (("source", 0, 1), ("target", -1, -2)):
                    port = edges[identifier][name]
                    x, y, w, h = surfaces[port["object"]]
                    f, side = port["fraction"], port["side"]
                    expected = {"north": (x+w*f, y), "south": (x+w*f, y+h),
                                "west": (x, y+h*f), "east": (x+w, y+h*f)}[side]
                    normal = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}[side]
                    point, near = route[index], route[neighbor]
                    if max(abs(point[i]-expected[i]) for i in (0, 1)) > 0.05:
                        issue("port_endpoint", [identifier, port["object"]], "Route misses its declared port", expected=expected, actual=point)
                    if sum((near[i]-point[i])*normal[i] for i in (0, 1)) <= 0:
                        issue("port_direction", [identifier, port["object"]], "Route must meet the port from outside its object")
            for label, bounds in labels.items():
                if any(overlaps(part, bounds) for part in parts) or (triangle and triangle_hits(triangle, bounds)):
                    issue("route_label_overlap", [identifier, label], "Route/arrow occupancy intersects measured text bounds", bounds)
            for other, bounds in object_ink.items():
                if objects[other]["role"] == "region":
                    continue
                relevant = list(parts)
                edge = edges[identifier]
                if edge["source"]["object"] == other:
                    relevant = relevant[1:]
                if edge["target"]["object"] == other:
                    relevant = relevant[:-1]
                if any(overlaps(part, bounds) for part in relevant) or (triangle and edge["target"]["object"] != other and triangle_hits(triangle, bounds)):
                    issue("route_object_overlap", [identifier, other], "Route crosses an unrelated node", bounds)
            bounds = measurement.box(identifier)
            if not contains([0, 0, width, height], bounds):
                issue("canvas_overflow", [identifier], "Route exceeds the canvas", bounds)

        coverage = {"model": "managed" if model else "absent: text/routes only", "text_labels": len(labels),
                    "objects": len(objects), "orthogonal_routes": checked_routes, "unsupported_features": unsupported,
                    "coordinate_units": "SVG viewBox units", "display_width_css_px": display_width,
                    "librsvg_geometry_version": measurement.version,
                    "not_checked": ["research semantics", "composition quality", "edge-edge crossings", "arbitrary SVG"]}
        result = {"status": "fail" if errors else "pass" if model else "partial", "errors": errors,
                  "warnings": warnings, "coverage": coverage, "label_ink_bounds": labels}
        if errors and debug:
            group = ET.SubElement(root, NS+"g", id="geometry-debug")
            for problem in errors:
                boxes = [problem["bounds"]] if problem["bounds"] else [
                    labels.get(key, object_ink.get(key)) for key in problem["objects"]
                    if key in labels or key in object_ink]
                for x, y, w, h in boxes:
                    node = ET.SubElement(group, NS+"rect", x=str(x-2), y=str(y-2), width=str(w+4), height=str(h+4),
                                         fill="#ef4444", stroke="#ef4444", **{"fill-opacity": "0.18", "stroke-width": "1"})
                    ET.SubElement(node, NS+"title").text = ": ".join([problem["kind"], ", ".join(problem["objects"])])
            tree.write(debug, encoding="utf-8", xml_declaration=True)
        return result
    finally:
        measurement.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--width", type=float, default=720)
    parser.add_argument("--debug", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(args.source.resolve(), args.width, args.debug)))
