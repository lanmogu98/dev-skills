# Illustrative systems benchmark protocol

This synthetic protocol is a test input, not an executed experiment or a claim about STeP.

Compare baseline and candidate implementations of an elementwise CPU kernel over a fixed list of input shapes and element types. Both receive identical input values on the same host, compiler version, and thread count. For each (implementation, workload) pair, check output against a reference with the protocol's prescribed tolerance before timing. Report correctness failures and do not time those failing pairs.

For a correct pair, perform five untimed warm-up invocations and then twenty timed invocations. Time the kernel invocation only, excluding allocation and input generation. Record individual latency samples and the status of every trial. Report failed or timed-out trials rather than silently dropping them. Summarize successful samples with median and spread for each matched workload; if one implementation has no valid samples, report the missing comparison rather than a speedup.

The run order is unspecified. Separate branches mean experimental conditions, not concurrent execution. No measurements, speedups, confidence intervals, or universal correctness claims are supplied.
