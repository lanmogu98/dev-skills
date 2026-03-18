---
name: dev-workflow
description: |
  Comprehensive engineering workflow for making code changes in existing codebases. Use this skill whenever the user wants to implement a feature, fix a bug, write or run tests, refactor code, create a pull request, do a code review, or make a commit. Also trigger when the user mentions branch strategy, TDD, test-driven development, pre-commit checks, merge conflicts, or debugging workflow. Covers the full cycle: exploration → design (tests first) → implementation → pre-commit → PR. Includes bug fix workflow, code review checklists, refactoring safety, multi-agent collaboration via worktrees, and optional domain review for projects with real-world consequences. If the user is working on an existing codebase and making changes of any kind, this skill applies.
---

# Dev Workflow

Engineering standards for code changes. Follow these phases in order.

## Core Principles

1. **Code is truth** — Read code first. Docs drift over time; the running code is what actually ships.
2. **Design before code** — Write tests before implementation. Tests force you to define "done" before you start, preventing scope creep and rework.
3. **Tests are design** — Tests define behavior, not just verify it. A well-written test suite IS the specification.
4. **Minimal blast radius** — Touch only necessary files. Every changed file is a potential regression; keep the change surface small.

## Priority Stack

Security → Correctness → Data Integrity → Availability → Performance → Docs → Speed

---

## Phase 1: Exploration

> **Do this FIRST before any planning or coding.**

### Required Steps

0. **Update task status**: If the project uses GitHub Issues, update the issue status/labels. If it uses `ISSUES.md`, mark the task as In Progress
1. **Create branch**: `git checkout -b feature/<name>` or `fix/<name>`
2. **Read relevant code** — Understand patterns, find insertion points
3. **Check if already exists** — Search for similar implementations
4. **Verify docs ↔ code sync** — If drift found, fix docs first

### Exploration Order

| Step | What to Find |
|------|--------------|
| 1 | Entry points: `main.py`, `index.ts`, `main.go` |
| 2 | Routes/API handlers |
| 3 | Config files |
| 4 | Related modules (follow imports) |
| 5 | Existing tests |

<details>
<summary>→ Deep dive: references/exploration.md — read when exploring an unfamiliar codebase or verifying doc-code sync</summary>
Full exploration checklist with examples, doc sync verification table, branch strategy.
</details>

---

> **Choose your path**: Adding new functionality or changing behavior → Phase 2 (Design). Fixing a reported bug → Phase 2-B (Bug Fix).

## Phase 2: Design

> Write tests before implementation. Tests define what "correct" means — without them, you're guessing whether your code works. Skipping this step is the #1 cause of rework.

### Required Steps

1. **Define behavior**: What does it do? Input → Output?
2. **Identify test cases**:
   - Happy path (normal success flow)
   - Edge cases (empty, max, concurrent)
   - Error cases (what should fail?)
3. **Write tests FIRST** — Tests must fail before implementation exists

### Minimum Tests by Change Type

| Change Type | Required Tests |
|-------------|----------------|
| New feature | Happy path + edge cases + error handling |
| Bug fix | Reproduces bug + regression guard |
| Refactor | Existing tests must pass; add if coverage insufficient |

If writing a test feels impossible, that usually means the requirement itself isn't clear yet. Clarify before coding — it's cheaper than debugging later.

<details>
<summary>→ Deep dive: references/design.md — read when defining test cases or unsure how to structure tests</summary>
Design checklist, test case questions, refactor test requirements.
</details>

---

## Phase 2-B: Bug Fix (Alternative to Phase 2)

> Reproduce the bug first. If you can't see it fail, you can't verify your fix actually works — and you risk "fixing" something that wasn't broken while the real bug persists.

### Required Steps

1. **Reproduce** — Confirm bug exists; if cannot reproduce, ask for more info
2. **Write failing test** — The test IS your bug report
3. **Understand root cause** — Why it fails, not just where
4. **Fix minimally** — Smallest change that makes test pass
5. **Verify** — Failing test passes; full suite passes

### When Fix Attempt Fails

| Signal | Action |
|--------|--------|
| Test passes but bug persists | You're testing wrong thing → get real user data |
| Fix works but breaks something | Patching symptoms → find actual root cause |
| Adding more edge cases | Approach flawed → consider architecture change |

When a fix fails, resist the urge to add another patch. Each failed attempt usually means your mental model of the bug is wrong — step back and re-examine assumptions from scratch.

<details>
<summary>→ Deep dive: references/bugfix.md — read when a fix attempt fails or you need a more systematic debug process</summary>
Multi-round debugging guidance, what data to request, architecture checks.
</details>

---

## Phase 3: Implementation

> **Prerequisite**: Tests are written and failing.

### Required Steps

1. **Run failing tests** — Confirm they fail for expected reason
2. **Write minimal code** — Just enough to make tests pass
3. **Run tests again** — Confirm they pass
4. **Refactor if needed** — Tests must still pass

### Code Standards

- Type annotations on function signatures
- Small, testable functions
- Explicit error handling (no silent `except:`)
- No secrets in code — use env vars

If tests don't pass, stop and investigate. Moving forward with failing tests means you're building on a broken foundation — every subsequent change compounds the problem.

<details>
<summary>→ Deep dive: references/implementation.md — read when handling flaky tests, LLM/API calls, or dependency issues</summary>
Handling flaky tests, LLM/API usage, dependency management.
</details>

---

## Phase 4: Pre-Commit

> Complete these steps before committing. Each one catches a different class of mistake — skipping any of them means that class of error ships silently.

### Required Checklist

```text
[ ] All tests pass
[ ] CHANGELOG.md updated (if user-facing change)
[ ] README.md updated (if CLI/config changed)
[ ] No debug code (console.log, print, commented code)
[ ] No secrets in code
```

### CHANGELOG Sections

| Change Type | Section |
|-------------|---------|
| New feature | `### Added` |
| Bug fix | `### Fixed` |
| Breaking change | `### Changed` |

### Commit Format

`type(scope): summary`

Types: `feat` | `fix` | `docs` | `test` | `chore` | `refactor`

```bash
git commit -m "feat(auth): add OAuth2 support"
git commit -m "fix(parser): handle empty input"
```

<details>
<summary>→ Deep dive: references/precommit.md — read when unsure which docs need updating or how to mark task status</summary>
Full doc sync table, task status updates.
</details>

---

## Phase 5: Pull Request

> **Prerequisite**: Pre-commit checklist complete.

### PR Guidelines

- **One PR = One concern** — Don't mix features, fixes, refactors
- **Small PRs** — Aim for <400 lines; split large changes
- **Complete** — Code + Tests + Docs in same PR

### PR Description

```markdown
## What
Brief description.

## Why
Link to issue or explain motivation.
Closes #123  <!-- if applicable -->

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing (if applicable)
```

### Self-Review Before Submit

1. Read your own diff
2. Remove debug code
3. Check for secrets
4. Verify CI passes

<details>
<summary>→ Deep dive: references/pullrequest.md — read when creating PR descriptions, responding to review feedback, or choosing merge strategy</summary>
Responding to feedback, merge strategies, GitHub issue linking.
</details>

---

## Code Review (for reviewers)

### Review Checklist

| Priority | Check |
|----------|-------|
| 1. Security | No secrets, input validation |
| 2. Correctness | Logic matches intent, edge cases handled |
| 3. Tests | Tests exist for changes, CI green |
| 4. Docs | CHANGELOG/README updated |

### Feedback Severity

| Severity | Action |
|----------|--------|
| Security/Logic error | Block merge |
| Missing tests/docs | Block merge |
| Style/naming | Comment as nit; don't block |

<details>
<summary>→ Deep dive: references/review.md — read when reviewing someone else's PR</summary>
Feedback format examples, PR size guidance.
</details>

---

## Refactoring

> **Refactor = change structure, NOT behavior.**

### Before Refactoring

Ask: "If I break something, will existing tests catch it?"

| Answer | Action |
|--------|--------|
| Yes | Proceed |
| No / Unsure | **Add tests first** |

Without confidence that existing tests will catch regressions, refactoring is risky — you could break behavior without knowing. Add tests first, then refactor safely.

<details>
<summary>→ Deep dive: references/refactoring.md — read when refactoring involves state isolation, config handling, or graceful termination</summary>
State isolation, config handling, graceful termination.
</details>

---

## Multi-Agent Collaboration

When multiple agents work in parallel:

```bash
# Each agent uses isolated worktree
git worktree add ../project-<role> <branch>
```

| Role | Workflow |
|------|----------|
| Planning | Exploration → define scope |
| Implementation | Exploration → Design → Implementation → Commit → PR |
| Bug fix | Exploration → Bug Fix → Commit → PR |
| Review | Review checklist |

Each agent follows the full workflow for their role. Cutting corners in multi-agent mode is especially dangerous because no single agent has full context — the workflow compensates for that.

<details>
<summary>→ Deep dive: references/multi-agent.md — read when setting up worktrees or coordinating parallel agents</summary>
Worktree naming, branch strategy, merge flow.
</details>

---

## Domain Review (Conditional)

If the project's `AGENTS.md` contains `## Domain Review Protocol`, load `references/domain-review.md` and apply these additional intervention points:

- **Brief-In** before exploration: explain what will be built and list upcoming domain decisions
- **Checkpoint** during design/implementation: pause at domain-laden decisions for human confirmation
- **Brief-Out** before commit: summarize embedded assumptions, structural vs tunable decisions

Checkpoints are **blocking** (wait for human). Brief-Out is a **soft gate** (no objection = proceed).

Skip checkpoint if the decision is already explicit in the design doc and confirmed during project-init. In non-interactive contexts, use design doc defaults and list all decisions in the PR description.

<details>
<summary>→ Deep dive: references/domain-review.md — read when project AGENTS.md has a Domain Review Protocol section</summary>
Decision weight matrix, intervention templates, non-interactive fallback rules.
</details>

---

## Quick Reference

### How to Choose

- "I need to add something new" → Feature flow
- "Something is broken" → Bug Fix flow
- "The code works but needs restructuring" → Refactor flow
- "I need to review someone's code" → Code Review section
- "Multiple agents working together" → Multi-Agent section

### Typical Flows

**Feature**: Exploration → Design → Implementation → Pre-Commit → PR

**Bug Fix**: Exploration → Bug Fix → Pre-Commit → PR

**Refactor**: Exploration → (verify test coverage) → Design → Implementation → Pre-Commit → PR

### Task Status (if project uses tracking)

`Pending` → `In Progress` → `In Review` → `Done`

Roadmap format: `| ID | Priority | Item | Status | GH |`
