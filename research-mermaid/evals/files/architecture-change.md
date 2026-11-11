# Selective recomputation source packet

Synthetic research-system design, not a measured implementation.

Both systems maintain derived results after a source dataset changes. In the fixed pipeline, the update event reruns every stage in the configured order and replaces all results. The baseline described here has no recorded relationship from changed data to the results that depend on it.

In the proposed system, a dependency index explicitly records source-to-result dependencies, including transitive ones. On a change event, an impact resolver consults that index to select affected results. A scheduler recomputes those results in dependency order. Unaffected cached results are retained; recomputed and retained results together form the current result collection. During recomputation, dependency discovery updates the index for later change events. The design assumes dependencies are recorded completely and changes are detected.

The reusable idea is to make dependencies available to change-impact resolution, separating selection of affected work from execution. This enables selective recomputation under the stated assumptions. No latency, storage cost, speedup, or claim about all pipeline systems is supplied.
