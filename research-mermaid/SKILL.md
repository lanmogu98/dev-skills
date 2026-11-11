---
name: research-mermaid
description: Use when planning, creating, revising, or reviewing Mermaid diagrams for research papers, technical notes, methods, experiment pipelines, mathematical mappings, proof dependencies, architectural contributions, system-mechanism comparisons, iterative feedback, or scientific systems. Also use when a repository's writing guidelines require it. Not for quantitative plots, anatomical illustrations, or an explicitly requested non-Mermaid format.
---

# Research Mermaid

Make the research claim, its conditions, and its evidence readable in the requested diagram. Preserve the user's chosen output format and scope.

## Establish the claim and destination

Read the destination repository's applicable instructions and follow its writing-guideline links. Use its authoritative definitions, design decisions, implementation, or experiment records for the relationships being shown. Project conventions specialize this workflow; do not import another project's paths, status vocabulary, or approval process. Merely reading a document containing a diagram does not call for redrawing it.

Before composing a new figure or changing its main relationship, establish the intended reader takeaway. Reuse an explicit intent from the conversation and briefly state it; do not ask for confirmation again. If the material permits different central claims and the focus is unclear, ask one high-level question: “What should the reader understand first from this figure?” The user supplies the purpose; infer nodes and layout from the sources. Wait for a necessary answer while continuing independent source inspection. A timeout is not confirmation. If the user asks you to use your judgment, state a working assumption and continue. Local syntax or cosmetic repairs retain the existing intent. Revisit intent only when its central relationship changes.

Identify the intended reader and destination renderer. For a paper, identify the requested export format and final figure size. If a missing fact determines a relationship, ask about that fact or mark it unresolved; a plausible narrative is not evidence. Preserve supplied citations and verify new ones before using them.

Choose the smallest view that answers the question. A caption should state the relationship and any essential conditions or omitted paths. Link evidence in the surrounding text; a separate evidence inventory is useful only when the task calls for one.

## Design the composition

For a new figure or a substantial redesign, read [Visual composition](references/visual-composition.md) and the matching section of [Diagram frameworks](references/diagram-frameworks.md) before selecting a template or Mermaid type. Establish the unit the reader must understand, the first-glance relationship, and the visual hierarchy that explains it. When different arrangements would tell different stories, choose the one that best exposes the agreed claim at the destination size; a brief working rationale is enough.

If a visual reference is supplied, inspect the image and identify which spatial, symbolic, textual, and color relationships make it work. Preserve those mechanisms when adapting it. For a whole-system comparison, keep the systems identifiable as complete views; merging them into one A/B path changes the question unless the intended comparison is a local substitution. Layout difficulty alone is not a reason to change the figure's job.

Let visual structure carry relationships: assign position, alignment, containment, connections, symbols, text, and color distinct jobs. Text names objects and essential conditions; layout organizes their relationships. Choose implementation resources after this decision, then check the rendered result against both the intended takeaway and the selected reference mechanisms.

## Choose a representation

| Question | Diagram | Guidance to read |
| --- | --- | --- |
| How do data or specimens move through an algorithm or experiment? | `flowchart` | [Research patterns: methods and experiments](references/research-patterns.md#methods-and-experiments) |
| Which mathematical paths agree, or which result depends on which? | Labeled `flowchart` | [Research patterns: mathematics and proofs](references/research-patterns.md#mathematics-and-proofs) |
| Who interacts with whom, and in what order? | `sequenceDiagram` | [Research patterns: scientific systems](references/research-patterns.md#scientific-systems) |
| Which states and transitions are allowed? | `stateDiagram-v2` | [Research patterns: scientific systems](references/research-patterns.md#scientific-systems) |
| How do components, types, or entities relate? | Grouped `flowchart`, `classDiagram`, or `erDiagram` | [Research patterns: scientific systems](references/research-patterns.md#scientific-systems) |

Use other Mermaid types when they fit the question and destination. For a quantitative result plot, use a plotting workflow that preserves numerical values, uncertainty, and axes. A request for a research figure alone does not select Mermaid.

## Use implementation resources

Read [Visual baseline](references/visual-baseline.md) for styling and delivery-size checks. Copy a `.mmd` example and theme only when they fit the chosen composition; examples do not select the composition or establish visual quality. They cover methods, experiments, mathematical mappings, proof dependencies, architecture, sequence interactions, and state lifecycles. For a local syntax repair, preserve the established intent and style; load composition guidance only if the main layout is affected.

<details>
<summary>Load additional guidance for the relationships present</summary>

- To explain a system contribution, read [Architectural change](references/diagram-frameworks.md#explain-contributions-through-architectural-change).
- For repetition, repair, optimization, or evolution in any framework, read [Iteration and feedback](references/research-patterns.md#iteration-and-feedback).
- For background material, constraints, or auxiliary inputs, read [Information roles](references/visual-baseline.md#main-path-and-supporting-information).

</details>

## Build the diagram

- Use one diagram declaration per fenced `mermaid` block or `.mmd` file. Give nodes stable IDs distinct from display labels and group IDs. Quote flowchart labels with punctuation, avoid reserved identifiers such as `end`, and place `%%` comments on separate lines. Alias sequence participants with complex names; put ER attributes on separate lines.
- Give arrows consistent meanings and directions. Distinguish data movement, temporal order, dependency, function application, association, and implication with labels or separate views. State dependency direction. Explain meaningful line-style, shape, and color differences in a caption or legend.
- Preserve conditions that change the claim, including domains, quantifiers, units, sample scope, and observation boundaries when applicable. Distinguish proposed relationships, established results, and empirical observations in words as well as styling. A grouping box or arrow must not imply an unestablished proof, causal effect, or execution order.
- Keep labels short and use the source's names. Prefer a single reading direction; use named groups for responsibilities, phases, or boundaries. Split when crossings or density obscure the relationship, rather than at an arbitrary node count. Preserve relevant loops and identify partial views.
- Prefer the destination's theme; use additional styling to encode a defined distinction. Check light/dark legibility for documentation and grayscale readability when the publication needs it. Do not rely on color alone.
- Update a diagram when its source relationships change. Keep accurate structure during local repairs; do not invent extra nodes or claims to make the layout look complete.

## Validate and deliver

Read [Rendering and review](references/rendering.md) when rendering, repairing syntax, reviewing an artifact, or exporting for publication. Check source fidelity, visual communication of the intended relationship, and rendering separately. Readable labels and a successful render do not establish that the composition works. A parser accepts diagram syntax, not the research claim.

When producing a rendered artifact, show its actual preview in the delivery, at the intended display size; link the source alongside it. Deliver the requested Mermaid source or rendered artifact, a concise caption with relevant source references and premises, and the actual validation result. Name a skipped check specifically. Keep validation notes out of manuscript prose unless they are part of the requested methods. Publishing is a separate action requiring task authorization.

## Common mistakes

| Symptom | Correction |
| --- | --- |
| A successful replay points to a universal correctness claim. | Show the tested configuration as evidence and cite a theorem separately for any universal claim. |
| Two arrows meet, but the caption never says what is equal. | State the composed-path equality, its domain, and its premises. |
| A methods pipeline contains an assumed randomization or analysis step. | Return to the protocol; identify missing information rather than filling in a conventional procedure. |
| Two architectures sit side by side, but their corresponding roles are hard to find. | Retain the intended comparison unit; coordinate panel hierarchy and recurring roles, then expose the structural change. Equal outer boxes alone do not solve the comparison. |
| A grouped architecture reads like a serial execution trace. | Label membership and show ordering only where it is established. |
| A local preview is reported as verified on GitHub or in a paper. | Report the renderer actually used and inspect the destination when available. |

## Source and license

Adapted from [ccheney/robust-skills, mermaid-diagrams](https://github.com/ccheney/robust-skills/blob/0eea7b060d12e3520556a73b15fbfa79480987d1/skills/mermaid-diagrams/SKILL.md), revision `0eea7b060d12e3520556a73b15fbfa79480987d1`. The upstream MIT notice is retained in [LICENSE](LICENSE). This adaptation adds research-claim fidelity, repository-context loading, mathematical and experimental patterns, and publication checks. The upstream reference catalog is replaced by the focused references above and official syntax links.
