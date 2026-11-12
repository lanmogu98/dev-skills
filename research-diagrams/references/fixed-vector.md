# Fixed vector figures

Use this path when the deliverable permits image resources and the composition depends on explicit alignment, regions, symbols, or feedback routing. The shared Python model builds an editable SVG and exposes its spatial requirements to measured checks; `rsvg-convert` renders it without a graph-layout step. A checked tool/font profile produces an outlined SVG and a PNG. Neither the authoring format nor the renderer selects a good composition for you.

## Implement the spatial argument

Start from the reader takeaway and [Visual composition](visual-composition.md). Translate the selected composition into a few spatial requirements: common panel top/title/body/environment bands, a dominant forward path with a separate return lane, or support regions beside the operations they inform. These requirements belong to this figure; they are not three new universal templates.

Allocate a canvas, regions, and routing lanes before placing individual nodes. Use the destination width as the coordinate width when practical: a `viewBox="0 0 720 H"` shown at 720 CSS pixels makes a 16-unit label approximately 16 pixels. Increase height or restructure content before shrinking the whole drawing. Keep ordinary labels around 16–18 units and subordinate labels at least 14 at that display size, subject to the destination's requirements.

- Derive related panel boundaries and title/environment bands from shared dimensions. Use deliberate width differences to accommodate the changed mechanism. Do not calculate each corresponding frame independently or substitute equal frames for recognizable role correspondence.
- Reuse glyphs for recurring roles: for example, a candidate collection can use a stack, while a harness can enclose constituent components. An agent, an operation, and an artifact need not all become identical text boxes. Keep symbols simple, relevant, and consistent; do not invent domain facts to fill them.
- Use stable IDs for meaningful regions and objects. Draw quiet backgrounds first, then routes, node bodies, and labels so a later region does not cover earlier content. Enclosure means actual membership, not merely a layout convenience.
- Assign ports and route corridors deliberately. A feedback edge should reach its actual revision target; a support relation should reach the governed region or operation. Put labels beside clear route segments with opaque backgrounds where needed. Do not let a route pass through another node, imply an unintended junction, or obscure another label.
- Emphasize short primary labels with weight 600 and use weight 400 for subordinate explanations. Use explicit line breaks and positioning; check every label after rendering. Keep each color's role consistent with the selected reference mechanism.

For new fixed figures, follow [Geometry authoring](geometry-api.md). Keep a small project generator that describes this figure's objects and spatial relationships; reuse the skill's construction, font measurement and diagnostics. The [generator example](../assets/templates/build_figure.py) demonstrates the API, not a preferred arrangement. A parent supplies local coordinates, shared alignments/sizes are derived, and ports update when their objects move. The agent still chooses the overall arrangement and route corridors. A frame moving correctly does not imply its new route is clear: rebuild and check after changes.

The [blank SVG canvas](../assets/templates/fixed-layout.svg) remains useful for an existing or explicitly hand-authored SVG. It does not carry the model's constraints. Preserve an established project pipeline or requested format; describe partial geometry coverage honestly rather than claiming every SVG has the same guarantees.

## Use one export profile

Locate [`rsvg-convert`](https://github.com/GNOME/librsvg/blob/main/rsvg-convert.rst) before adding tools. The bundled [profile](../assets/rendering/svg-profile.json) records the tested librsvg/dependency versions and exact [font files](../assets/fonts/README.md). The exporter forces Pango’s Fontconfig backend and isolates font lookup to that directory, so installed system fonts cannot silently change text metrics. This backend selection matters on macOS, where Pango can otherwise use CoreText. Keep the authoring SVG self-contained: ordinary SVG shapes/text, internal references, no HTML `foreignObject`, imported CSS, or external image/font URLs. Use the bundled `Source Sans 3` at weights 400 and 600 when its glyph coverage fits.

Run from the destination project, resolving the script from this skill's installed path:

```sh
python3 /path/to/research-diagrams/scripts/render_svg.py render \
  figures/architecture.source.svg --output figures/architecture --width 720
```

This writes `architecture.svg`, `architecture.png`, and `architecture.render.json`. The editable `.source.svg` remains text-editable; the exported SVG outlines text so display does not depend on host fonts. Title/description metadata is retained. Keep useful alternative text in the Markdown image reference as well. The PNG is rendered from the exported SVG, giving both resources the same geometry.

For a managed source, `render` first runs geometry checks in a fresh process with the same font environment and matching librsvg version. It writes `architecture.check.json`; an error returns nonzero and emits a diagnostic `.debug.svg`/`.debug.png` instead of a new final export. Read the object IDs, measured bounds and violated relationships, inspect the debug image, and revise the generator. Previous exports can still exist after a failed rebuild; their source hashes do not verify the new candidate.

To diagnose an older unmanaged source explicitly:

```sh
python3 /path/to/research-diagrams/scripts/render_svg.py check \
  figures/architecture.source.svg --output figures/architecture-check --width 720
```

This measures identified text and supported routes, but lacks ownership, alignment and port declarations. A clean partial check is not a managed geometry pass. See [Geometry authoring](geometry-api.md) for the supported subset and remaining visual review.

If the environment differs, the command reports profile drift instead of quietly changing output. Establish a project profile explicitly, retain the previous profile with its outputs, rerender, and inspect before adopting it:

```sh
python3 /path/to/research-diagrams/scripts/render_svg.py lock \
  --profile figures/render-profile.json
python3 /path/to/research-diagrams/scripts/render_svg.py render \
  figures/architecture.source.svg --output figures/architecture \
  --profile figures/render-profile.json --width 720
```

For other language coverage, use a project directory of licensed fonts and pass the same `--font-dir` to both commands. Preserve those fonts/licenses and the profile with the build. A checked version/font profile detects drift; it is not proof of identical builds across operating systems. A tested container may provide stronger build reproducibility when a project requires it. Display consistency comes from distributing the same exported resource.

## Embed and inspect the delivered resource

Use an opaque background for a fixed paper figure unless transparency is requested. It remains the same figure in light/dark document surroundings; do not allow host CSS to recolor it. Separate themed exports are optional deliverables, not evidence of cross-host consistency.

```markdown
![Existing and proposed systems, showing the changed feedback mechanism](figures/architecture.png)
```

Paths are relative to the containing Markdown file. PNG has the broadest preview compatibility; SVG is the vector companion where supported. The host displays this resource instead of executing a layout engine. Keep the editable source, generator if used, font/tool profile, rebuild command, and caption alongside the deliverable. A second semantic `.mmd` is not required.

Inspect the actual exported PNG at the intended width and review source correspondence separately. Open the Markdown in the destination when available; otherwise report that destination check as unperformed. Repeating a local export and comparing hashes checks local stability, not composition quality or every preview application. Follow [Rendering and review](rendering.md) for communication, clipping, glyph, crossing, and membership checks.
