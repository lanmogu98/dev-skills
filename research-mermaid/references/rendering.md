# Rendering and review

## Select the renderer

Use the repository's renderer and configuration when provided. Otherwise use an available Mermaid CLI or the destination's preview. Locate existing tools before adding dependencies; a syntax explanation alone does not justify installing a toolchain. Use the [official CLI documentation](https://github.com/mermaid-js/mermaid-cli) and [syntax reference](https://mermaid.js.org/intro/syntax-reference.html) for version-sensitive behavior.

Keep unpublished research local unless the user authorizes sending it to an external editor. Prefer a local preview for manuscripts and private source material.

GitHub can run a different Mermaid version from a local CLI or Mermaid Live. Its [diagram documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#checking-your-version-of-mermaid) describes checking the active version with an `info` diagram. A preview in one renderer does not validate another.

## Render and inspect

For an available `mmdc` command, a standalone source can be rendered with:

```sh
mmdc -i diagram.mmd -o diagram.svg
mmdc -i diagram.mmd -o diagram.png
```

Use a temporary output location for validation. Mermaid CLI can also transform Mermaid fences in Markdown into rendered-image references; direct that output to a separate temporary file so validation does not rewrite the authored document. Keep source diagrams as the maintained artifact unless the task requests rendered outputs.

Apply the delivery-size acceptance checks in [Visual baseline](visual-baseline.md#acceptance-at-the-delivery-size). Inspect the rendered image, not just the process exit status. Check labels, clipping, font/glyph support, arrowheads, crossings, boundary membership, and reading order at the intended display size. Review semantic fidelity against the source: every depicted condition, direction, status, and equality still has to be correct. Rerender after a syntax, layout, or configuration change; unchanged diagrams can reuse current evidence for the same renderer and configuration.

Check communication against the agreed reader takeaway, applying only the relevant questions:

| Content | Check in the actual preview |
| --- | --- |
| Architecture contribution | Can the reader locate the common task, changed mechanism, and its path to the claimed capability? |
| Iteration | What changes, what persists, and where does the next round enter? Does stopping mean success or merely termination? |
| Multiple loops | Are cross-loop effects attached to concrete artifacts or interfaces without invented nesting or timing? |
| Context and constraints | Are auxiliary roles distinguishable from execution stages, with their important targets preserved? |
| Visual encoding | Do grouping, alignment, shapes, line styles, color, and text emphasis retain consistent meanings? |

Temporarily ignore supporting explanations to see whether the main structure is recognizable, then remove color to check whether essential distinctions remain. These are diagnostic checks, not reasons to remove necessary qualifiers. Resolve any disagreement among caption, accessible description, and visible relationships.

For documentation, inspect supported light and dark themes, especially when custom styling is used. For publication, follow the venue's dimensions and export requirements: prefer a vector artifact when accepted, check legibility at final column width, and test grayscale when needed. A large preview is not evidence that small printed labels are readable. For dense equations, preserve the requested notation in surrounding math or use the user's chosen mathematical typesetting tool rather than silently switching formats.

When publication is authorized, inspect the published diagram or final document. Do not create a public upload or PR just to test rendering.

## Report validation accurately

Distinguish these outcomes in the delivery note:

| Check | Evidence |
| --- | --- |
| Source correspondence | Inspected definition, theorem, protocol, data record, or supplied source supporting the relationships and premises. |
| Rendering | Renderer/version and successful rendering of the delivered source. |
| Visual review | Inspection of the actual output at its intended size and relevant theme. |
| Destination compatibility | Inspection in the target host or final exported document, when available. |

Report only the checks performed. If a tool is unavailable or a browser cannot launch, deliver the source and identify rendering as unverified. A browser-environment failure is not a Mermaid syntax failure; a successful parser run alone is not visual review. Keep this note concise and outside the manuscript figure caption.
