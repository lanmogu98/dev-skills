# Counterexample-guided repair source packet

Synthetic algorithm for repairing a candidate transformation against a fixed specification. The input specification and allowed input domain remain fixed throughout a run. Initialize the candidate from the supplied initial transformation and the counterexample set to empty, once.

Each round checks the current candidate against the fixed specification over the allowed domain. The checker returns exactly one of: verified for that domain, a concrete counterexample, or unknown. Verified terminates with the candidate and the checker's domain-scoped certificate. Unknown terminates as inconclusive, not verified.

For a counterexample, add it to the retained counterexample set without removing earlier examples. A repair procedure uses the current candidate, fixed specification, and the entire accumulated set. If it finds a revised candidate, check that candidate in the next round. If it finds none within its per-round search budget, terminate with repair exhausted, not a proof of impossibility. A revised candidate satisfying the known examples is not yet verified for the full domain. No overall termination guarantee is supplied.
