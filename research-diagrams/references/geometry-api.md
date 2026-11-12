# Geometry authoring and feedback

Use this for new fixed SVG figures after selecting the composition. A project Python generator expresses layout through shared objects; `scripts/figure.py` builds the SVG, and `render_svg.py` measures and checks it before export. This is a small construction library, not a graph-layout engine or a collection of required figure templates.

## Start with the spatial requirements

Keep the agreed takeaway and a few essential spatial relationships in a brief working note or generator comments. For example: complete systems share title/environment bands; a one-time entry remains outside the repeating body; or contextual support sits beside the dominant operational path. The user need not specify coordinates or approve every constraint.

Then allocate regions and route lanes and instantiate their objects. Use `align` and `same_size` only where the composition requires them. Parent-relative coordinates preserve containment when a region moves; callable coordinates preserve relationships when a referenced size or position changes. These local relationships do not select a good global arrangement for you.

## Minimal use

Copy the [thin example](../assets/templates/build_figure.py) to the destination project and adapt its composition. Run it with the installed skill's absolute path:

```sh
python3 figures/build_figure.py --skill /path/to/research-diagrams \
  --output figures/method
```

A generator imports the shared code:

```python
sys.path.insert(0, str(skill_path / "scripts"))
from figure import Figure

fig = Figure(720, 300, title="Subject", description="Relationship shown")
work = fig.region("work", x=16, y=16, w=688, h=268, title="Work")
first = fig.node("first", "Revise", x=24, y=80, w=180, h=64, parent=work)
second = fig.node("second", "Validate", x=420, y=80, w=180, h=64, parent=work)
fig.align("cy", first, second)
fig.connect("progress", first.port("east"), second.port("west"))
fig.export(output_prefix)
```

`skill_path` and `output_prefix` are project-supplied `Path` values. The complete example includes argument parsing. The generated resources are `.source.svg`, `.check.json`, `.svg`, `.png`, and `.render.json`; retain the project generator as the authoring source as well. Embed the final image in Markdown using a relative path.

## Objects and placement

| Operation | Inputs and behavior |
| --- | --- |
| `Figure(width, height, title=..., description=..., min_font_px=14)` | Canvas units and adjustable working font floor at the requested export width. Defaults to the bundled Source Sans 3 family. |
| `fig.region(id, x=..., y=..., w=..., h=..., parent=None, title=None)` | Quiet container with optional title. Children and labels use its local coordinates. Optional `fill`, `stroke`, `radius`, `padding`. |
| `fig.node(id, primary, x=..., y=..., w=..., h=..., secondary="", parent=None)` | Main label at 16/600 and secondary at 14/400. A string with newlines or a list supplies explicit lines. Optional `fill`, `stroke`, `glyph`, `padding`. |
| `fig.label(id, text, x=..., y=..., parent=None, owner=None, size=16, weight=400)` | One line of text at a baseline. Defaults to centered anchor; `anchor="start"`/`"end"` and `color` are available. A parent also supplies the default owner for fitting checks. |
| `fig.align(attribute, reference, *others)` | Derives positions and records equality. Boxes support `left`, `right`, `cx`, `top`, `bottom`, `cy`; labels support `baseline`. |
| `fig.same_size(reference, *others, width=False, height=False)` | Derives selected dimensions and records equality. Unequal panel widths remain valid when not constrained. |
| `box.port(side, fraction=0.5)` | Dynamic attachment on `north`, `south`, `east` or `west`; fraction is 0–1 along that side. |
| `fig.connect(id, source_port, target_port, ...)` | Direct straight route or explicit orthogonal routing; optional `color`, `dashed`, `width`, `arrow`. |

Use `box`, `collection` or `pill` glyphs according to the selected role. Collection stacking is one intentional composite object; containment uses explicit parents. Different colors and glyphs need task-specific meanings. Keep glyphs consistent for recurring roles without making every research object the same box.

All object IDs are stable and unique. The builder registers every node label, region title, note and edge label; use `fig.label` for additional text rather than injecting unregistered SVG. Put route labels beside clear segments. The initial API does not implement text backing masks: give the text clear space, so the visible route and checks agree.

Positions and dimensions accept numbers or zero-argument callables. `box.left/top/right/bottom/cx/cy/width/height` return absolute canvas coordinates. For a parent-relative x value derived from another object, subtract the parent's left coordinate:

```python
second.x = lambda: first.right - work.left + 48
fig.connect("return", second.port("south"), first.port("south"),
            via_y=lambda: work.bottom - 28)
```

Routing options are mutually exclusive: `via_x` gives a vertical corridor, `via_y` a horizontal corridor, and `via=[(x, y), ...]` gives intermediate points. `via` can also be a callable returning points. Point coordinates can be callables. With no option, endpoints must align horizontally or vertically. A route is one continuous subpath and meets its ports from outside the object. Ports and parents must belong to this figure. Moving a node recalculates endpoints; it can still create a collision elsewhere, which requires rerouting.

## Measured checks and repair

`fig.export(prefix, width=720, font_dir=None, profile=None)` writes the candidate and invokes the checked exporter. It uses a fresh process and the exporter's Fontconfig environment for librsvg text measurement. Optional project fonts/profile follow the same workflow as [Fixed vector figures](fixed-vector.md).

The embedded model stores identity, ownership, endpoint choices and equality constraints; visible coordinates come from the SVG itself. Checks use measured glyph ink bounds for fit/collision and font size × display scaling for the font floor. Glyph ink height is not font size. The root's numeric dimensions must match the viewBox aspect ratio; changing only its height can invalidate that scaling. Checks resolve the actual marker reference and accept the standard arrow geometry. Diagnostics include object IDs, measured bounds, target display width and the source hash.

The supported checks cover:

- Label fitting with declared padding, label/label and label/unrelated-object occupancy, parent containment, and canvas bounds.
- Straight/orthogonal route strokes and the standard arrowhead against every registered label and unrelated node. Region membership and intentional collection stacking are treated separately; connecting to a region does not exempt its title.
- Declared alignment/shared-size equality, actual endpoint positions and port directions, and effective font size.

On failure, read `.check.json` and inspect `.debug.png`, which highlights reported bounds. Revise the project generator, rebuild, and rerun until the intended constraints are satisfied. Increase space, adjust a lane, or revise label wording while preserving source meaning; do not silently reduce the working font floor, omit a required relationship, or remove ownership/constraints to obtain a pass. Keep meaningful attempts when evaluating a skill change.

Occupancy boxes conservatively reserve space around glyphs and shapes; a bounds intersection does not claim a pixel-level diagnosis of every visual overlap. Review close or special cases in the actual image. The initial supported subset is flat SVG using presentation attributes, rectangular/composite bodies, explicit text and orthogonal routes. Curved routes, CSS, arbitrary transforms, external resources, clipping and masks are outside this model. Edge-edge crossings and the semantic correctness of selected targets remain visual/source review tasks.

For existing unmanaged SVG, explicit `render_svg.py check` supplies partial identified-text/orthogonal-route diagnostics, with coverage in the report. Ordinary export preserves that source's existing workflow and records geometry as unchecked. Do not describe either partial or skipped checking as a managed pass.

Finally inspect the actual exported image at its intended width against the agreed takeaway and reference mechanisms. Geometrically clear objects can still make a poor comparison or hide an iteration. When communication fails, revise the composition and its layout model together.
