# Visual composition

Read this before selecting a template for a new figure or a substantial redesign. The aim is to make the reader's main inference visible with little searching. Correct relationships and legible labels are necessary, but neither establishes a good composition.

## Decide what the visual structure must do

Start with the agreed reader takeaway and the verified relationships. Identify the unit the reader must understand: a whole system, a transformation, a repeating process, a correspondence, or interacting responsibilities. Establish its abstraction level and which distinctions carry the contribution. This keeps local details from displacing the question the figure was meant to answer.

Choose the global arrangement before the source notation or asset. When materially different compositions are plausible, consider a small number and choose the one that makes the intended inference easiest at the destination size. Judge them by how directly they expose the main relationship, preserve necessary context, distinguish information roles, and limit mental matching or edge tracing. A brief working rationale is enough; do not turn this into a user questionnaire or a mandatory report.

Specify what should be visible at three levels:

- **First glance:** the overall comparison, progression, cycle, or division of responsibilities.
- **Closer reading:** the mechanism, interfaces, and changes that explain the claim.
- **Detail:** necessary conditions and qualifications, with longer definitions in surrounding text.

Assign visual variables to these tasks deliberately. Alignment can establish correspondence, enclosure can express responsibility, and a return path can delimit an iteration. Text names and qualifies these relationships; it should not have to explain away a layout that suggests something else.

## Learn from a visual reference

Inspect the actual reference image when the user supplies or names one. Separate the source of technical facts from the reference for visual expression. An unrelated domain can supply a useful composition without supplying facts about the user's system.

Extract **relationship → visual device → reader inference**, rather than just its colors or a list of nodes. For example: corresponding systems → coordinated panel headers, repeated role symbols, and a stable environment region → the reader can locate what changed within the same task. Decide which of these devices carry the reference's effect and which are incidental styling.

Adapt those mechanisms to the task, preserving their purpose. Do not replace a requested whole-system comparison with a merged A/B mechanism diagram simply because it fits more easily. Conversely, do not copy the reference's exact number of stages, colors, or domain names when they do not serve the new material. When repairing a weak layout, retain the agreed figure question and unit of comparison; explain a necessary change of view rather than silently changing its job.

Templates are implementation examples after this decision. A runnable example is not a preferred composition or evidence of visual quality. Use only an example whose semantics and global arrangement fit; build a different structure when they do not. An old example's successful render must not override a reference or the user's visual feedback.

## Architecture comparisons

When the contribution is a reusable architecture or paradigm, first consider complete views of the existing and proposed systems. Preserve enough of each system to explain both the limitation and the mechanism enabling the new capability. Identify recurring roles and their common task so the reader can make the correspondence without reconstructing two unrelated graphs.

Coordinate the panels' hierarchy: titles, main body, recurring role symbols, environment or input/output regions, reading direction, and text scale. Corresponding roles need recognizable visual anchors; they need not occupy identical coordinates if their relationships have changed. Similar frame heights and aligned boundaries can establish a common comparison area. Unequal widths or additional space can be useful when they visibly accommodate the innovation. Accidental size differences and arbitrary offsets communicate no such reason. Equal frames alone do not establish a comparison.

Allocate space and emphasis to the structural delta: a new interface, a changed responsibility, or an additional feedback path. Keep unchanged roles visually recognizable, and distinguish the new mechanism through more than color alone. A capability label should be visibly tied to the structure that enables it.

A shared skeleton is appropriate when the reader's question concerns a local substitution within an otherwise identical mechanism. An overview with a detail is appropriate when one subsystem needs expansion. Choose these because they answer that question better, not as a general remedy for difficult panel layout. Reusing one execution path for two complete architectures can conceal the very change the reader needs to compare.

## Iteration and supporting information

For iteration, use spatial scope to distinguish initial entry from the repeated body. Make the return target, changing object, and cross-round continuity recognizable. Put a feedback path where it exposes the update, rather than letting it compete with the forward progression. The [iteration semantics](research-patterns.md#iteration-and-feedback) determine whether the next round means a new input, a repaired candidate, or a revised mechanism; they do not prescribe one loop shape for all cases.

For multiple loops, group their own work and show the interfaces through which they affect one another. Position and repeated role styling should help the reader follow each loop without inventing a nested schedule.

For context, constraints, and outputs, give supporting information a different spatial role from the processed object. Context may support a work region; a specific constraint should remain near its governed operation; feedback should reach the revision it informs. Preserve important links even when summarizing broad support with a region-level relation. See [information roles](visual-baseline.md#main-path-and-supporting-information).

Allocate space by explanatory importance. Attaching support near its target can help, but forcing every support block into a separate band can stretch the main path into long empty corridors. When this happens, reconsider the region arrangement and route lanes together while preserving the specific support targets; increased height is not itself a clearer hierarchy.

## CAKE: worked visual reasoning

Source: Ye et al., [CAKE: Compiler–Agent Co-Design for Frontier Kernel Evolution](https://arxiv.org/abs/2608.12629v1), Figures 1, 2, and 4 on pp. 2, 3, and 6. The following are observations of those figures and the transferable design reasoning, not a required house style.

| Reference | What its visual structure does | Transferable decision |
| --- | --- | --- |
| Figure 1: existing approach and CAKE | Coordinated panel tops/bottoms and title bands establish a system comparison. Recurring agent, stacked candidate, harness, and environment roles make the two views recognizable. The wider proposed-system panel accommodates two colored evolution paths around a central shared harness. | Compare complete modes when the contribution changes the system paradigm. Coordinate the comparison frame and recurring roles; use the extra space to expose the architectural innovation. Do not infer that all panels must be equally wide or that all internal nodes must align exactly. |
| Figure 2: bottom-up IR evolution | A one-time entry sits before a compact forward chain; the lower return path rejoins the first operation of the repeated body. Bold main labels and subordinate explanations separate action from purpose. The return label says what starts another round. | Make the initial/repeated distinction visible in loop placement; let the primary path convey progression. Preserve the true reentry and trigger instead of adding a generic end condition. The particular three stages and palette are task-specific. |
| Figure 4: evidence-driven compiler evolution | Context and dynamic feedback occupy the left region; two named work regions organize the right. A broad support relation differs from the internal operational arrows. A design-principle constraint sits above its check, and the final artifact has a distinct role. | Separate information roles through regions, containment, and local attachment. Use region-level support only when it preserves the claim's required detail. The two IR/compiler work regions are not a new universal diagram category. |

For Figure 1, blue follows kernel evolution while orange follows compiler-harness evolution; it does not classify every operation versus every output. Candidate stacking indicates a collection, harness containment indicates composition, and the environment boundary separates evaluation context. These devices share the explanation with the words. A transfer that preserves only the terms while flattening those relationships has lost the point of the reference.

## Carry the composition into rendering

Turn the selected composition into a few explicit spatial requirements before coding: for example, coordinated comparison panels and environment bands; an uninterrupted forward chain with its return in a separate margin; or supporting information beside a dominant work region with a local constraint attached to its target. These requirements explain what the implementation must preserve, rather than fixing coordinates for every future figure. For new fixed SVGs, carry the selected relationships into the [shared geometry model](geometry-api.md): regions, parent membership, alignments, shared dimensions, ports and route corridors. Keep the reasoning brief; do not require a second coordinate inventory or a user-supplied layout specification.

Check whether the chosen renderer actually realizes them. Mermaid directions and subgraphs express layout intent, not fixed placement: cross-region connections and feedback labels can reshape the whole graph. A semantically correct source may render as a ribbon, reorder comparison panels, or scatter the main progression. Shrinking the export or shortening labels is not a sufficient remedy when the global relationships remain wrong.

For exported composition-sensitive figures, use [explicit SVG geometry and the checked exporter](fixed-vector.md). Shared construction derives related coordinates; measured diagnostics locate fit, clearance and declared-constraint errors. Revise the project generator and rerun those checks after changes. Preserve the editable source and any generator. Other project renderers can be appropriate if they implement the required spatial relationships and keep reproducible build inputs. An automatic layout engine's name or an explicit direction is not such a guarantee.

Use a native Mermaid view when requested or when it preserves the intended structure. If a destination requires a single native Mermaid block, respect that constraint and report the specific unresolved layout limitation rather than silently switching formats. Otherwise, the authoring source need not be Mermaid. Inspect the actual exported artifact for correspondence, feedback routing, hierarchy, clipping, and legibility; preserve every important connection and label through implementation.

## Review the composition before polishing

Ask what the figure makes apparent before reading its detailed caption: which systems correspond, what changed, what repeats, or what supports the main work. The caption should supply conditions and precision, not create the comparison or loop that the drawing failed to organize. Ordinary node names and short local explanations remain part of the figure; this is not a demand for a text-free diagram.

Inspect the arrangement against the reference's selected mechanisms and the agreed takeaway. A layout can pass syntax, font-size, and overlap checks while failing this test. If it fails, revise the hierarchy, grouping, correspondence, or route structure first. Then perform the separate source-fidelity and rendering checks in [Rendering and review](rendering.md).
