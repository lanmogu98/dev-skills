#!/usr/bin/env python3
"""Export a self-contained SVG through a checked librsvg/font profile."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def profile(font_dir: Path) -> dict:
    version = subprocess.run(
        ["rsvg-convert", "--version"], check=True, capture_output=True, text=True
    ).stdout.strip()
    fonts = {
        p.name: digest(p)
        for p in sorted(font_dir.iterdir())
        if p.suffix.lower() in {".otf", ".ttf"}
    }
    if not fonts:
        raise ValueError(f"No OTF/TTF fonts in {font_dir}")
    return {"toolchain": version, "font_backend": "fontconfig", "fonts_sha256": fonts}


def render(args: argparse.Namespace, current: dict) -> None:
    expected = json.loads(args.profile.read_text())
    if current != expected:
        raise ValueError(
            "Renderer or fonts differ from the profile. Preserve the old profile; "
            "record a new one with the lock command and visually review new exports."
        )
    source = args.source.resolve()
    root = ET.parse(source).getroot()
    if root.tag != f"{{{SVG}}}svg":
        raise ValueError("Input must be an SVG document")
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] in {"foreignObject", "script"}:
            raise ValueError("Use SVG shapes and text, without HTML or scripts")
        for attr, value in element.attrib.items():
            if attr.rsplit("}", 1)[-1] == "href" and not value.startswith("#"):
                raise ValueError("Keep the SVG self-contained; external resources are unsupported")
    if "@import" in source.read_text() or "@font-face" in source.read_text():
        raise ValueError("Use the profile's font directory, without imported CSS/fonts")
    outputs = {ext: Path(f"{args.output}.{ext}").resolve() for ext in ("svg", "png")}
    if source in outputs.values():
        raise ValueError("Output must not replace the editable source SVG")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="research-figure-") as temp:
        config = Path(temp) / "fonts.conf"
        config.write_text(
            "<?xml version='1.0'?><!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>"
            f"<fontconfig><dir>{escape(str(args.font_dir.resolve()))}</dir>"
            f"<cachedir>{escape(temp)}/cache</cachedir></fontconfig>"
        )
        env = dict(os.environ, FONTCONFIG_FILE=str(config), FONTCONFIG_PATH=temp,
                   PANGOCAIRO_BACKEND="fontconfig")
        commands = [
            ["rsvg-convert", "--format=svg", f"--width={args.width}",
             "--dpi-x=96", "--dpi-y=96", "--accept-language=en",
             "--keep-aspect-ratio", "--output", str(outputs["svg"]), str(source)],
            ["rsvg-convert", "--format=png", f"--width={args.width}",
             "--dpi-x=96", "--dpi-y=96", "--accept-language=en",
             "--keep-aspect-ratio", "--output", str(outputs["png"]), str(outputs["svg"])],
        ]
        subprocess.run(commands[0], check=True, env=env)
        outlined = ET.parse(outputs["svg"])
        out_root = outlined.getroot()
        if any(el.tag == f"{{{SVG}}}text" for el in out_root.iter()):
            raise ValueError("SVG export still contains font-dependent text")
        for tag in ("title", "desc"):
            original = root.find(f"{{{SVG}}}{tag}")
            if original is not None:
                item = ET.SubElement(out_root, f"{{{SVG}}}{tag}")
                item.text = "".join(original.itertext())
        outlined.write(outputs["svg"], encoding="utf-8", xml_declaration=True)
        subprocess.run(commands[1], check=True, env=env)
    png_width, png_height = struct.unpack(">II", outputs["png"].read_bytes()[16:24])
    record = {
        "profile": current,
        "source": {"path": str(source), "sha256": digest(source)},
        "display_width_css_px": args.width,
        "png_dimensions": [png_width, png_height],
        "svg_text_outlined": True,
        "commands": commands,
        "outputs_sha256": {ext: digest(path) for ext, path in outputs.items()},
    }
    Path(f"{args.output}.render.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"svg": str(outputs["svg"]), "png": str(outputs["png"]),
                      "dimensions": record["png_dimensions"]}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("lock", "render"):
        command = commands.add_parser(name)
        command.add_argument("--font-dir", type=Path, default=ROOT / "assets/fonts")
        command.add_argument("--profile", type=Path, default=ROOT / "assets/rendering/svg-profile.json")
        if name == "render":
            command.add_argument("source", type=Path)
            command.add_argument("--output", type=Path, required=True, help="Output path without extension")
            command.add_argument("--width", type=int, default=720)
    args = parser.parse_args()
    if args.command == "render" and args.width <= 0:
        parser.error("--width must be positive")
    current = profile(args.font_dir)
    if args.command == "lock":
        args.profile.parent.mkdir(parents=True, exist_ok=True)
        args.profile.write_text(json.dumps(current, indent=2) + "\n")
        print(args.profile)
    else:
        render(args, current)


if __name__ == "__main__":
    main()
