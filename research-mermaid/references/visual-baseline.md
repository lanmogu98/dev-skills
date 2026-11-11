# Visual baseline

Use this baseline when the destination has no established diagram style. It is a starting point for visual consistency, not evidence that a layout is readable. Destination and venue requirements take precedence. Load only the chosen template and theme, not the entire catalog.

## Apply the base

The [light theme](../assets/themes/light.json) and [dark theme](../assets/themes/dark.json) share typography, spacing, and role conventions. Templates contain diagram structure and may include small layout overrides; themes supply the shared typography and palette. Apply the theme as a companion config when rendering local artifacts:

```sh
mmdc -i diagram.mmd -c light.json -b white -o diagram.svg
mmdc -i diagram.mmd -c dark.json -b '#0F172A' -o diagram-dark.svg
```

Resolve these filenames from this skill's `assets/` directory or copy the selected files into the output project. A standalone `.mmd` intended for another renderer needs the chosen settings embedded, or its companion config delivered. For a Markdown fence, start with this compact frontmatter and follow it with the selected template's diagram declaration. If the template already has a config header, merge its layout overrides into this one header rather than stacking two headers:

```yaml
---
config:
  theme: base
  look: classic
  htmlLabels: false
  themeCSS: ".edgeLabel rect { opacity: 1 !important; }"
  themeVariables:
    fontFamily: "Arial, sans-serif"
    fontSize: "17px"
    primaryColor: "#F8FAFC"
    primaryTextColor: "#0F172A"
    primaryBorderColor: "#64748B"
    lineColor: "#475569"
    edgeLabelBackground: "#FFFFFF"
    clusterBkg: "#F8FAFC"
    clusterBorder: "#CBD5E1"
  flowchart:
    curve: linear
    nodeSpacing: 36
    rankSpacing: 48
    padding: 16
    wrappingWidth: 280
    minNodeWidth: 0
    look: classic
    theme: base
    htmlLabels: false
---
```

Edge-label backgrounds are opaque so paths do not show through text; verify this in the destination, where custom CSS may be restricted. The complete theme JSON includes sequence-specific colors as well. For exact parity, put the entire selected JSON object under `config` in frontmatter; JSON objects are valid YAML values. Some hosts ignore configuration or supply their own styles. Use the host theme and validate the result there instead of assuming local parity. See [official theming](https://mermaid.js.org/config/theming.html) and [flowchart syntax](https://mermaid.js.org/syntax/flowchart.html) for supported settings.

## Visual roles

| Element | Default treatment | Meaning and limits |
| --- | --- | --- |
| Data or mathematical object | Neutral rectangular node, explicit noun | An object, not an action or proof status. |
| Decision | Diamond with a short guard and labeled alternatives | Alternatives reflect actual control flow; a diamond is not a parallel fork. |
| Operation | Rounded node, blue border | A named transformation. Keep blue optional if the host owns the palette. |
| Highlighted output | Double-border node, teal border | The answer the figure emphasizes. Teal does not mean proved or correct. |
| Group | Quiet neutral boundary with a title | Membership or responsibility; a box does not establish isolation or ordering. |
| Main edge | Solid line with arrowhead | Declare its meaning for the chosen diagram family. |
| Secondary relation | Dotted arrow and a label | A separately named relation, such as fitted-parameter transfer. Dotted does not universally mean uncertainty. |

Assign each visual variable a job before choosing decoration:

| Variable | Useful relationship |
| --- | --- |
| Position and alignment | Correspondence, progression, and primary versus supporting roles. |
| Containment, regions, whitespace | Membership, responsibility boundaries, and separation of context. |
| Connections and line patterns | Explicit transformations, dependencies, feedback, or constraints. |
| Shapes | Object, operation, decision, or other named semantic role. |
| Weight and text hierarchy | Primary name versus a short explanation or necessary qualifier. |
| Color | Tracking a consistent role, path, or mechanism across the view. |

Select visual encoding to support the composition and reference mechanisms first. The operation/result palette above is a fallback when no task-specific role encoding is needed. When color instead tracks responsibilities or paths, switch the encoding consistently across the figure and explain it; the same blue should not mean both “operation” and “baseline.” Use words, shape, or position to preserve important distinctions without color. For two-level labels, emphasize the short primary name and keep the supporting line subordinate; use destination-supported text syntax and verify the render. Simple figures need no additional styling.

Use words and shapes alongside color. State theorem status in text; do not infer it from the result style. Sequence and state diagrams retain their native conventions instead of reusing flowchart role classes. For a monochrome destination, remove the flowchart border colors while retaining labels, shapes, and line patterns; switching themes alone does not override explicit `classDef` colors.

## Main path and supporting information

Place processed objects on the actual transformation path. Keep background knowledge or reference material in a supporting region; attach specifications, principles, or constraints to the steps they govern with named relations. Runtime feedback enters the operation that revises the affected object. Outputs belong to the operations that produce them.

Containment or a single relation to a work region may summarize broad support when the source warrants it. Retain specific evidence links, constraint targets, and dependencies essential to the claim; fewer arrows are not inherently clearer. In particular, avoid making context → principles → operation look like a serial execution path. See the [architecture example](diagram-frameworks.md#system-architecture) for a constraint input alongside the artifact path.

## Compose before styling

1. Follow the [composition decision](visual-composition.md): first-glance relationship, comparison unit, hierarchy, and any selected reference mechanisms. Use [Diagram frameworks](diagram-frameworks.md) and example assets to implement that decision; remove example content unsupported by the task.
2. Separate short identifiers/actions from conditions and full definitions. Usually a node needs one or two short lines; use the caption for the domain, assumptions, and full formula when those do not distinguish paths. Keep path-changing conditions beside their node or edge. Use a short main label for the object or action and a subordinate line only for an essential distinction.
3. Arrange the main relationship to fit the destination. A short serial method can run left to right. Experimental partitions need explicit labels under a shared allocation. A single phase node can carry a partition label; use a group for several related operations. Fitting and selection dependencies can stagger phases, so do not promise exact alignment from automatic layout. Mathematical paths should make their common endpoints easy to find. Do not rotate a long chain and call the layout solved.
4. Try changing direction, grouping, or decomposing the view before reducing text size, while preserving the figure's intended comparison unit and main relationship. Use subgraphs for meaningful boundaries, not as empty positioning containers. External links can cause Mermaid to ignore a subgraph's direction. ELK is an optional alternative when supported by the host; rerender and compare rather than assuming it improves the graph.

## Acceptance at the delivery size

Record the display width or publication column size. If unspecified, use a 720 CSS-pixel documentation preview and label that assumption. Check the delivered artifact at that width, without zooming. This baseline uses a working floor of 14 CSS pixels for documentation labels after scaling; it is a project-adjustable target, not a universal accessibility or publication standard. Follow the venue for print sizes.

Reject and revise a candidate when any of these holds:

- The main relation, start, or outcome requires tracing several competing paths to identify.
- Nodes, edge labels, arrowheads, or group titles overlap or are clipped; an edge crosses text or an unrelated node.
- Labels become hard to read at the delivery size. Exporting a larger PNG or increasing pixel density does not repair CSS-size text.
- Equal visual treatments encode different meanings without explanation, or the caption's line styles disagree with the actual image.
- Long labels and repeated qualifiers dominate the drawing; condense them or move non-discriminating details to the caption.

Render, inspect, repair, and rerender. Compare light and dark outputs if both are supported; inspect grayscale for monochrome publication. Deliver a visible preview with source and caption, so the user can judge communication quality rather than only seeing a successful render log. Keep limitations outside the figure caption.
