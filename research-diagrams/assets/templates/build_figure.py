"""API example, not a preferred composition. Copy to a figure's project."""

import argparse
from pathlib import Path
import sys


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--skill", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True, help="Output prefix")
args = parser.parse_args()
sys.path.insert(0, str(args.skill.resolve() / "scripts"))
from figure import Figure


fig = Figure(720, 288, title="Retained information across rounds",
             description="An archive enters once; revision and checking repeat while information persists.")
work = fig.region("work", x=160, y=16, w=544, h=256, title="Repeated work")
archive = fig.node("archive", "Error\narchive", x=16, y=96, w=108, h=64, glyph="collection")
revise = fig.node("revise", "Revise", secondary="retain library", x=24, y=80, w=164, h=64, parent=work)
check = fig.node("check", "Check", secondary="against archive", x=332, y=80, w=180, h=64, parent=work)
fig.align("cy", revise, check)
fig.label("entry", "One-time entry", x=70, y=77, size=14)
fig.connect("initialize", archive.port("east"), revise.port("west"))
fig.connect("forward", revise.port("east"), check.port("west"))
fig.connect("repeat", check.port("south"), revise.port("south"), via_y=lambda: work.bottom-52)
fig.label("trigger", "New case or exposed gap", x=280, y=234, parent=work, size=14)
fig.export(args.output)
