# Research patterns

Read the section matching the relationship being drawn. The examples illustrate notation; actual research claims need their own sources.

## Mathematics and proofs

Start from the exact statement. Identify the objects and their domains, the maps or relations, their direction, the quantifiers, and the premises needed for the conclusion. Retain distinctions such as equality of representations, equality after decoding, observational equivalence, approximation, and implication. Put lengthy formulas in adjacent mathematical text rather than oversized node labels.

For a commuting diagram, state the equality of the composed paths. Drawing a square is insufficient: the two routes must terminate in the objects that the theorem actually compares. If equality is known only after an observation map, terminate both routes at the observed value; equality before observation would require additional evidence. Treat an inverse, injectivity, or equivalence as a claim requiring its own justification.

For a proof-dependency graph, label the direction, such as premise to dependent result, and distinguish established lemmas from proposed steps or open obligations. A dependency arrow explains proof structure; it is not by itself a logical implication or a proof of the target.

For equality after observation, use the [mathematical mapping framework](diagram-frameworks.md#mathematical-mapping). For `D(G(E(t))) = F(t)`, one route is `F`, and the other is `E` followed by the composed edge `D ∘ G`. Define that composition in the caption. This statement alone does not establish `E(F(t)) = G(E(t))`; layout convenience does not justify changing the claim.

An executable check or simulator replay contributes evidence for its exercised input, configuration, and schedule. Show it separately or label the evidence relationship; do not attach it as a proof of a universal statement. For formal verification, distinguish a theorem about the formal model from correspondence with an implementation or physical system.

## Methods and experiments

Trace the protocol's actual inputs, transformations, comparisons, and outputs. Preserve the unit of analysis and branching unit: a patient, specimen, run, seed, visit, and measurement are not interchangeable. Include sample counts, exclusions, repetitions, and allocation ratios only when supplied or derived transparently from supplied facts; do not invent stages from a conventional workflow.

Distinguish planned protocol from executed procedure and measured results. Preserve controls, intervention or allocation method, and paired versus independent comparisons when they affect interpretation. In a data-analysis pipeline, distinguish fitting from applying a transform and identify which partition informs fitting or tuning. Repeated observations from one subject must not be drawn as independent allocation units when the protocol assigns subjects.

Use the caption to state the population or dataset, relevant configuration, and what the depicted evidence supports. Preserve units and the meaning of any displayed uncertainty. A methods diagram does not substitute for a quantitative results plot.

If drawing a causal model, say whether arrows are assumptions, intervention structure, or identified effects. An observational association does not alone establish a causal arrow. Do not invent confounders, randomization, statistical significance, or a causal identification strategy to complete the picture; obtain the missing scientific input when it determines the requested graph.

For computer-systems experiments, record the workload and input matrix, baseline and candidate, hardware/software controls, correctness oracle, timing boundary, warm-up policy, trial repetitions, and failure/timeout handling when the protocol supplies them. Match configurations before comparing results. A benchmark observation supports only the exercised conditions; it is not a correctness theorem or a universal performance claim. Use the [systems experiment framework](diagram-frameworks.md#systems-experiment) for this comparison design; keep training/validation/test splits for experiments that actually use them.

## Iteration and feedback

Identify what changes, the operation in a round, the feedback source, what persists across rounds, the reentry point, and the condition for another round or completion. These are semantic questions, not six required node types. Distinguish one-time initialization from the repeated body; a return arrow alone does not explain how one round affects the next.

| Process | Relationship to preserve |
| --- | --- |
| Repeated processing | New inputs enter the same operation; do not imply that the operation learns or changes. |
| Repair and retry | A failure or counterexample changes a candidate before reevaluation; identify retained failures when supplied. |
| Feedback optimization | An evaluation changes a parameter, candidate, or selection; distinguish the current trial from retained history or best-so-far state. |
| Mechanism evolution | The generator, evaluator, or execution environment itself changes; show how that revision affects subsequent candidate work. |

Make fixed inputs and mutable objects distinguishable through naming, grouping, or labeled dependencies. Place feedback at the operation it informs, not automatically at the original input. Preserve the source's exit condition for an executable algorithm. A continuing evolution overview may instead specify the next-round trigger and repeated scope; do not invent convergence, a fixed budget, or a terminal node.

For multiple loops, name each updated object and the payload that connects one loop to the other. Two loops are coupled only when their outputs affect each other's operation; label one-way influence as such. Shared evaluation alone does not establish mutual updates, strict nesting, synchronization, or different timescales. Show concrete interfaces rather than an unexplained double-headed arrow.

Choose the spatial scope and information hierarchy using [Visual composition](visual-composition.md#iteration-and-supporting-information); semantic completeness alone does not make the loop easy to follow. Use the [feedback revision example](diagram-frameworks.md#feedback-revision-example) for state carried across rounds, and the branching methods template for control-flow guards. Neither layout is mandatory for other iteration semantics.

## Scientific systems

For pipelines and dependency views, identify whether a box is a component, artifact, stage, or boundary. Groups express membership unless ordering is explicit. Keep data flow, control flow, and dependency direction legible. Preserve input order, output identity, selector/control paths, and observation boundaries when they affect the described result.

For interactions, use sequence participants for actors and messages for their actions. Represent concurrency, alternatives, and repetition when relevant; a vertical sequence should not imply an ordering between independent actions. State a successful-path-only scope when failure paths are deliberately omitted.

For lifecycle diagrams, use states as nodes and label transitions with the governing events or conditions. Preserve who can authorize a transition when the source assigns that responsibility. Separate lifecycle status from implementation maturity and research-evidence status.

For entity or type diagrams, ground cardinalities and relationships in the schema or inspected source. Distinguish composition, inheritance, and mere association. Use the destination-compatible [Mermaid syntax reference](https://mermaid.js.org/intro/syntax-reference.html) for the selected diagram type.
