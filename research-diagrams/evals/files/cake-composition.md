# CAKE composition source packet

Read-only summary of Ye et al., *CAKE: Compiler–Agent Co-Design for Frontier Kernel Evolution*, arXiv:2608.12629v1, Figures 1, 2, and 4 on pp. 2, 3, and 6. The original figure images should accompany a visual-reference evaluation; the summary alone is not image inspection.

## Figure 1: system comparison

The existing approach evolves kernel candidates through an optimization agent, an agent harness, and an environment benchmark. The environment is treated as fixed; benchmark feedback informs subsequent kernel work.

CAKE makes compiler-harness evolution an additional part of the architecture. Kernel optimization and compiler-harness evolution interact with a shared evaluation harness. Kernel candidates enter that harness, which returns structured diagnostics to optimization. Capability gaps motivate compiler evolution; resulting IR, analysis, or lowering changes update the harness. Its constituent static validation, performance model, and code generation/GPU runtime are shown as components, not as a claimed serial execution trace. A benchmark environment provides the correctness reference and target GPU.

The original figure has separately titled existing/proposed system panels with aligned outer tops/bottoms and title bands. The proposed panel is wider. Repeated agent, candidate-stack, harness, and environment symbols provide role correspondence. Within the proposed panel, kernel evolution is on the left, a shared harness in the middle, and compiler-harness evolution on the right; two colors track the two evolution responsibilities. An environment region is placed at the bottom.

The evaluation task's claim concerns the complete system paradigm changing from kernel-only evolution to co-evolution. A local map-extraction or request-dispatch example does not describe that claim. No performance figure is needed for this composition task.

## Figure 2: initial entry and repeated work

The production-kernel corpus is the starting material, without a predefined IR. Work identifies a recurring abstraction or gap, revises the IR/compiler support, then ports and validates against the corpus. The next kernel family or a gap exposed by validation starts the repeated work again. The corpus is an initial entry; the loop does not reset to an absence of IR each round. There is no supplied global termination condition.

Visually, the entry precedes a horizontal body of equally prominent operations; a lower return route targets the beginning of that body. Main labels name the actions; subordinate lines explain purpose. The return annotation identifies the next-round trigger.

## Figure 4: information roles

Knowledge context includes production kernels and documentation. Dynamic feedback includes debugging information, sanitizer reports, and program failure cases. These provide support to IR/compiler evolution. Proposals are checked against IR design principles before implementation; compiler analysis/pass work leads to an updated harness.

The reference places context and feedback in left-side regions, two named work regions on the right, a broad support arrow between them, a local principles constraint above its check, and an output distinguished by its role. These arrangements do not mean context is specimen material or that every supporting input is a serial processing step.
