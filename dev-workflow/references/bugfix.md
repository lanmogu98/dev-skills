# Bug Fix Workflow

> **STOP. Do not touch code until you can reproduce the bug.**

## When Fix Attempt Fails (Read This First)

If you're on your **second or third attempt** at fixing this bug, STOP and ask yourself:

| Signal | What It Means | Action |
|--------|---------------|--------|
| Test passes but bug persists | You're testing the wrong thing | Go back to Phase 1, get real user data |
| Fix works but breaks something else | You're patching symptoms | Go back to Phase 3, find actual root cause |
| You're adding more and more edge cases | Original approach is flawed | Consider architectural change |
| User says "still broken" | Your mental model is wrong | Ask user for exact DOM/state/logs |

**The Rule:** When a fix fails, don't patch it. Return to Phase 1 and re-examine your assumptions.

> "When a bug takes multiple attempts, the problem is usually your understanding, not the code."

## Phase 1: Reproduce

Before any code changes:

- [ ] **Note the GitHub issue** — If bug came from roadmap's `GH` column, note the issue number (e.g., `#123`)
- [ ] **Confirm the bug exists** — Run the failing scenario manually or via test
- [ ] **Identify exact failure** — What happens vs what should happen?
- [ ] **Check if already fixed** — Search recent commits, PRs, issues

If you cannot reproduce the bug, **do not proceed**. Ask for more information.

### When to Ask User for More Data

Don't guess. Request concrete artifacts:

| Situation | What to Ask For |
|-----------|-----------------|
| UI bug | Screenshot, DOM structure (DevTools Elements tab) |
| Data issue | Actual input/output vs expected |
| Intermittent bug | Steps to reproduce, console logs |
| State issue | Component state dump, Redux/store snapshot |
| API bug | Request/response payloads, network tab |

**Pro tip:** User-provided data often reveals the real bug faster than code analysis. The DOM structure screenshot in a recent bug fix exposed the actual issue (wrong insertion position) that code reading missed.

## Phase 2: Write Failing Test

> **The test IS your bug report.**

```
1. Write a test that fails due to the bug
2. Confirm it fails for the right reason
3. This test becomes your regression guard
```

**Do not skip this step.** A bug without a test will come back.

### Signs You're Skipping TDD

If any of these are true, STOP and write the test first:

- [ ] You're already thinking about the fix implementation
- [ ] You opened the source file before writing a test
- [ ] Your test was written after the fix "just to verify"
- [ ] The test passes on the first run (did it ever fail?)

**Why this matters:** In a recent multi-round bug fix, the first two attempts failed because tests were written to match the (wrong) implementation, not the actual user expectation. Writing the test first forces you to define "what should happen" before "how to make it happen."

## Phase 3: Understand Root Cause

Ask yourself:

| Question | Why It Matters |
|----------|----------------|
| **Why** does it fail, not just where? | Fixes symptoms vs root cause |
| Is this a single bug or pattern? | May need broader fix |
| When was it introduced? | `git bisect` can help |
| Is it a regression? | Higher urgency, may need hotfix |

### Check Architectural Assumptions

Sometimes the bug exists because the architecture doesn't support the use case:

| Assumption to Check | Example |
|---------------------|---------|
| Data structure fits the problem | "One element → one translation" fails for mixed content |
| Flow direction is correct | "Append to end" fails when position matters |
| Abstraction level is right | Processing at wrong granularity (element vs text node) |

**Key question:** Can this bug be fixed within the current architecture, or does the architecture need to change?

| Approach | When to Use |
|----------|-------------|
| Fix within architecture | Bug is an edge case the code didn't handle |
| Change architecture | The design assumption itself is wrong |

> If you're adding increasingly complex workarounds, the architecture probably needs to change.

## Phase 4: Fix Minimally

**Smallest change that makes the test pass.**

- Touch only what's necessary
- Don't refactor surrounding code (separate PR if needed)
- Don't add unrelated improvements

## Phase 5: Verify

- [ ] **Failing test now passes**
- [ ] **Full test suite passes** — No regressions introduced
- [ ] **Manual verification** — Confirm fix in real environment if applicable

## Phase 6: Documentation

| Situation | Action |
|-----------|--------|
| Bug exposed incorrect documentation | **Fix the docs** |
| Fix changes user-visible behavior | **Update CHANGELOG** |
| Bug was caused by misleading docs | **Fix the docs** |
| Internal bug, no user impact | No doc changes needed |
| Found unrelated doc drift | Fix it (but separate commit) |

## Quick Checklist

Before committing a bug fix:

```
[ ] Bug is reproduced
[ ] Failing test exists
[ ] Root cause is understood (not just symptom)
[ ] Fix is minimal
[ ] All tests pass
[ ] Docs updated (if applicable)
[ ] CHANGELOG updated (if user-visible)
[ ] GitHub issue noted for PR (if applicable)
```

> **Tip:** If this bug has a GitHub issue (from roadmap's `GH` column), include `Closes #123` in your PR description to auto-close it on merge.

---

**→ Next:** Load `references/precommit.md` to prepare commit.
