# Refactoring Guidelines

> **Load this in addition to `design.md` and `implementation.md` when refactoring.**
> Use when changing code structure without changing behavior.

## 0. Verify Test Coverage First

Before any refactoring, answer this question:

> **"If I break something, will the existing tests catch it?"**

| Answer | Action |
|--------|--------|
| Yes, confident | Proceed to refactor |
| No / Unsure | **Add tests first** (see `design.md`) — without them you're flying blind |

### Must Add Tests If:

- Existing test coverage is insufficient for the code being changed
- Refactoring involves concurrency, shared state, or resource management
- Refactoring touches error handling or edge case logic

Without confidence in test coverage, refactoring is risky — you could break behavior without knowing. Add tests first, then refactor safely.

## 1. Test-Driven Refactoring

- Spend more time designing tests (boundary, stress, concurrency) than writing code
- Commit implementation only after corresponding tests pass
- Existing tests must continue to pass — this is your safety net

## 2. State Isolation

- Long-lived objects (clients, processors) must not accumulate request-specific state
- Return values should reflect only the specific operation, not object lifetime history

## 3. Configuration Explicitness

- Never override user config with hidden defaults
- Test "negative" cases (flags set to `False`) to ensure they aren't forced `True`

## 4. Graceful Termination

- Handle SIGINT/Ctrl+C without leaving data inconsistent
- Async tasks must handle `CancelledError` to clean up resources

## 5. UX/IO Separation

- Separate structured UI (TUI/progress bars) from unstructured logging
- When using rich terminal UIs, suppress INFO logs to prevent visual interference

---

**→ Phase complete.** Return to SKILL.md for the next step.
