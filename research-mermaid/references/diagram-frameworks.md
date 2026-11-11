# Diagram frameworks

Choose by the reader's question, not by a preferred Mermaid keyword. These are illustrative structural templates, not facts about a project. Use the [visual baseline](visual-baseline.md) and the destination's constraints. The examples below specify captions and failure patterns for each runnable `.mmd` template.

| Question | Framework | Source |
| --- | --- | --- |
| How is an input transformed into an output? | Methods pipeline | [methods.mmd](../assets/templates/methods.mmd), [branching variant](../assets/templates/methods-branching.mmd) |
| How are implementations compared under controlled workloads? | Systems experiment | [experiment.mmd](../assets/templates/experiment.mmd) |
| Which mathematical paths give the same value? | Mathematical mapping | [mapping.mmd](../assets/templates/mapping.mmd) |
| Which premises and results support a theorem? | Proof dependencies | [proof.mmd](../assets/templates/proof.mmd) |
| Which responsibilities exchange which artifacts? | System architecture | [architecture.mmd](../assets/templates/architecture.mmd) |
| Who sends what, and in which order? | Sequence interaction | [sequence.mmd](../assets/templates/sequence.mmd) |
| Which transitions are permitted? | State lifecycle | [state.mmd](../assets/templates/state.mmd) |

## Methods pipeline

**Structure:** short input → operations → output, with one principal reading direction. Use a vertical or staged view when the destination cannot fit the serial path; introduce branches and feedback only when the method contains them.

**Example caption:** Observations pass through preparation and analysis to produce an estimate. Arrows denote data flow; the statistical method is specified in the accompanying text.

**Check:** an action is named as an action; the primary output is obvious; an executable loop has its source-defined exit condition; a continuing evolution overview shows the trigger and scope of the next round. **Failure pattern:** nine serial boxes shrink into a ribbon, with paragraphs inside each box. Move repeated qualifiers to the caption and split at a meaningful stage, preserving the connecting artifact.

### Branching and iterative computation

Use [methods-branching.mmd](../assets/templates/methods-branching.mmd) when the algorithm includes a guarded fast path, fallback, or loop. Its example is a tiled elementwise kernel, not a claim about a particular implementation.

**Example caption:** For `n ≥ 0` and tile capacity `B > 0`, an empty input returns immediately. A full, aligned tile uses the vector path; every other tile loads only valid elements using a safe fallback. The mutually exclusive paths rejoin at the elementwise transform. Stores touch only valid indices, and the loop processes all tiles before returning. Solid arrows are control flow, not data dependencies; the merge is not a synchronization barrier between parallel operations.

**Check:** each decision has complete, named alternatives; paths rejoin at the operation they actually share; the loop goes back to the next-tile selection and has an exit; the empty-input path bypasses all memory operations. Do not remove guards, fallback paths, or synchronization needed by the algorithm to achieve a cleaner layout. A successful straight-line example does not establish readability for a branch-heavy kernel: render the actual branches and loops at the target width. If edges become tangled, split an overview from a named body-detail view while preserving entry, exit, and loop semantics.

### Feedback revision example

Use [iteration-feedback.mmd](../assets/templates/iteration-feedback.mmd) when feedback changes an object carried into the next round. Read [iteration semantics](research-patterns.md#iteration-and-feedback) before adapting it; the branching example above instead emphasizes guarded execution paths.

**Example facts and caption:** A synthetic sensor-calibration procedure starts with a calibration setting and an empty trial log. Each trial measures the same fixed reference using the current setting. The measured residual and setting are appended to the retained log. Stop when the residual meets the prescribed tolerance or the trial budget is exhausted; otherwise use that history to revise the setting and measure again. Stopping at the budget does not establish accuracy. Solid arrows show trial progression and feedback; the dotted reference arrow supplies fixed measurement input.

**Adapt:** replace the setting, feedback payload, retained history, and stopping rule from the task's sources. Preserve the distinction between initialization, retained information, and the next-round entry. **Misreading to avoid:** returning to initialization would erase history; ending a trial does not always mean success.

## Systems experiment

**Structure:** fixed workload matrix and environment → baseline/candidate branches → repeated measurements → matched-workload report. These branches denote comparison conditions, not simultaneous execution. The example is a systems benchmark; use a different design when the actual question is training, ablation, scalability, or a distributed fault experiment.

**Example caption:** Baseline and candidate use the same workloads, inputs, hardware, and software environment. Outputs are checked against a reference before untimed warm-up and repeated timing. Only correct configurations enter timing; correctness failures and failed/timed-out measurements remain visible in the report. Compare latency distributions on matched workloads. Solid arrows show protocol progression; dotted arrows send correctness failures directly to the report. Repetition measures run variability and does not prove universal correctness or speedup.

**Check:** identify the controlled factors, varied implementation/configuration, measurement unit and scope, warm-up treatment, repeated-trial count, and failure accounting from the supplied protocol. Do not invent a clock, synchronization scheme, concurrency, or random run order. Keep correctness checking distinct from performance measurement. **Failure pattern:** a “run benchmark → speedup” chain hides unmatched configurations, omitted failures, or a different timing boundary in each branch. Preserve the comparison design and place detailed host versions and trial counts in the caption.

## Mathematical mapping

**Structure:** a common source and target, with two labeled routes. The template is a compact triangle: direct `F` and composed `H ∘ E`. Use a four-object square for a genuine four-object commuting claim when the renderer supports a clear arrangement; do not invent identities or equalities just to fill its corners. A composed edge is useful when the intermediates are not the subject of the figure.

**Example caption:** For every `x` satisfying `P(x)`, `H(E(x)) = F(x)`. Nodes denote mathematical objects; arrows denote function application. This is an illustrative premise, not a proved result.

**Check:** both routes end in exactly the values compared by the statement; list the domain and necessary premises; do not promote equality after decoding to equality of encoded values. **Failure pattern:** a long encode–compute–decode chain plus a remote bypass makes comparison hard. Compose secondary operations into a labeled edge and give its full definition in the caption.

## Proof dependencies

**Structure:** assumptions at the top, intermediate results in layers, target below. Arrows point from an assumption or result to a result whose proof uses it. Parallel branches need no invented order.

**Example caption:** The proof of T uses Lemmas A and B under assumption P. These arrows summarize proof dependencies, not individual implication steps. The example marks the displayed results established; real status must come from the sources.

**Check:** hypotheses and theorem status are explicit; a conjunction of prerequisites is not mistaken for alternatives; experimental observations are not presented as proof. Mark proposed or open steps in words if included. **Failure pattern:** all nodes look like proved theorems, or arrows silently reverse direction halfway through the graph.

## System architecture

**Structure:** responsibility groups containing components and artifacts; labeled connections between responsibilities. Use a vertical arrangement in a narrow document column or a horizontal arrangement on a wide canvas, without imposing a total execution order.

**Example caption:** Production emits an artifact; validation checks it against a specification and produces a validation report. Solid arrows carry artifacts; the dotted “constrains” arrow attaches the specification to the checker, not to the processing sequence. Boundaries indicate responsibility. A report is not itself evidence of universal correctness.

**Check:** node kinds and interface payloads are identifiable; group membership agrees with sources; input/output identities are preserved. **Failure pattern:** every component is placed in a serial chain, implying an execution order absent from the design. Use separate sequence views when ordering is the question.

**Adapt:** replace the producer, artifact, checker, and specification with sourced roles. Keep the constraint attached to the component it governs. A side input is not automatically an earlier execution stage; the report alone does not prove the specification holds.

### Explain contributions through architectural change

Explain a common task, the existing mechanism's limitation, the structural change, and how that change enables the claimed capability. Locate the limitation in an interface, missing information, or responsibility boundary. Show the mechanism's objects and interface payloads, not just “baseline” and “ours” labels. A capability annotation explains a consequence; do not make it a fictitious execution step.

Choose a composition that exposes the change:

- **Corresponding views:** establish a common comparison axis, such as the same task and corresponding responsibilities. Align matching inputs, operations, and outputs on shared rows or columns; keep their scale, reading direction, and encoding consistent. Label the alternatives and make the changed interface or boundary visible. Proximity alone does not establish correspondence.
- **Shared structure with an emphasized change:** use when most roles stay the same and a small interface or responsibility changes.
- **Overview with local detail:** use when the contribution is concentrated in one subsystem; identify the expanded interface in both views.

Treat equal outer frames as a supporting cue, not the comparison itself. Their dimensions should be comparable when area carries no meaning, but equal boxes with unrelated internal arrangements still make the reader reconstruct the mapping. Deliberate asymmetry can emphasize a changed subsystem when the common anchors remain clear. Do not add fictional components or execution edges to force symmetry.

If automatic layout destroys the correspondence, revise the composition instead of accepting it because it renders. A shared skeleton with explicitly labeled alternatives often suits a localized change better than two independently laid-out systems. In that view, distinguish design-change arrows from runtime paths and say whether the alternatives replace one another; do not imply that both mechanisms operate together.

Allow enough space for the differentiating mechanism. For a reusable paradigm, distinguish stable roles and relations from the current implementation's names. State the scope of limitations: omitting baseline components cannot establish impossibility, and a mechanism comparison does not demonstrate a measured speedup.

Use [architecture-change.mmd](../assets/templates/architecture-change.mmd) as an example of a shared skeleton with an explicit architectural transformation, not a new diagram family.

**Example facts and caption:** Both synthetic designs route a request to a handler; the shared path shows this invariant task. In alternative A, the handler map is inside the dispatcher-code boundary, so extension edits that code. In alternative B, a separate registry supplies the map, so extension changes registrations while dispatch code remains fixed. The thick “Design change: extract mapping” arrow denotes an architectural transformation, not a runtime transfer. Thin solid arrows carry requests; dotted A/B arrows supply the mapping in the respective alternative, not simultaneously. The enclosure expresses code membership, and the labeled A/B map nodes preserve the distinction without color. This explains an extension point, not measured performance or a limitation of every fixed dispatcher.

**Adapt:** change both sides' common task, corresponding roles, interface payloads, and sourced limitation together. Retain the mechanism-to-capability explanation in the caption or a subordinate annotation. **Misreading to avoid:** the registry is a mapping consulted during dispatch, not a stage that processes the request before the dispatcher.

## Sequence interaction

**Structure:** one lifeline per participant; messages ordered top to bottom. Solid messages are calls/requests; dashed messages are returns in this example. Add `alt`, `loop`, or `par` only for branches, repetition, or concurrency in the source.

**Example caption:** Successful request path: the researcher submits a request, the coordinator delegates execution, and the worker's result returns to the researcher. Failure paths are omitted.

**Check:** every arrow names an action or payload; activation matches actual activity; independent work is not inadvertently serialized. **Failure pattern:** components drawn as flowchart nodes hide who sends or receives each message.

## State lifecycle

**Structure:** state nodes with event/guard labels on transitions; explicit start and termination only when meaningful. Keep retries close to the state they revisit.

**Example caption:** Jobs start queued, run, and either succeed or fail. Failure permits retry; success terminates this lifecycle. Labels denote transition events.

**Check:** every depicted transition is allowed by the source; actor authorization appears when relevant; termination does not hide an allowed restart. **Failure pattern:** actions such as “run checker” are mixed with states such as “validated”, making arrow semantics ambiguous. Rename nodes as states and put actions/events on edges.
