---
name: dev-workflow
description: |
  Development workflow for code changes. Load when: implementing features, fixing bugs, writing tests, refactoring, creating PRs, reviewing code, releasing versions. Covers exploration → design → implementation → commit → PR → release cycle. Keywords: feature, bug, fix, test, refactor, PR, pull request, commit, code review, implement, develop, build, release, version, tag, changelog, publish, deploy.
metadata:
  version: "2.1.0"
---

# Dev Workflow

Engineering standards for code changes. Follow these phases in order.

## Core Principles

1. **Code is truth** — Read code first; docs may be outdated
2. **Design before code** — Write tests before implementation
3. **Tests are design** — Tests define behavior, not just verify it
4. **Minimal blast radius** — Touch only necessary files

## Priority Stack

Security → Correctness → Data Integrity → Availability → Performance → Docs → Speed

---

## Phase 1: Exploration

> **Do this FIRST before any planning or coding.**

### Required Steps

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
<summary>→ More details: references/exploration.md</summary>
Full exploration checklist, doc sync table, branch strategy.
</details>

---

## Phase 2: Design

> **STOP. Do not write implementation code until tests are written.**

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

**Rule**: If you can't write a test, you don't understand the requirement yet.

<details>
<summary>→ More details: references/design.md</summary>
Design checklist, test case questions, refactor test requirements.
</details>

---

## Phase 2-B: Bug Fix (Alternative to Phase 2)

> **STOP. Do not touch code until you can reproduce the bug.**

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

**Rule**: When a fix fails, don't patch it. Re-examine assumptions.

<details>
<summary>→ More details: references/bugfix.md</summary>
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

**Rule**: If tests don't pass, don't move forward.

<details>
<summary>→ More details: references/implementation.md</summary>
Handling flaky tests, LLM/API usage, dependency management.
</details>

---

## Phase 4: Pre-Commit

> **Complete ALL steps before `git commit`.**

### Required Checklist

```
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
<summary>→ More details: references/precommit.md</summary>
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
<summary>→ More details: references/pullrequest.md</summary>
Responding to feedback, merge strategies, GitHub issue linking.
</details>

---

## Phase 6: Release (when publishing)

> **When to use:** After merging PRs, ready to publish a new version.

### Semantic Versioning

`MAJOR.MINOR.PATCH` — e.g., `1.2.3`

| Bump | When |
|------|------|
| MAJOR | Breaking changes (config migration, behavior change) |
| MINOR | New backward-compatible features |
| PATCH | Bug fixes, performance fixes |

### Release Checklist

```
[ ] All tests pass
[ ] Version bumped in all version files (package.json, manifest.json, etc.)
[ ] CHANGELOG.md: [Unreleased] → [x.y.z] - date
[ ] No secrets in codebase
[ ] Migration notes (if breaking changes)
```

### Quick Release Flow

```bash
# 1. Bump version + update CHANGELOG
git commit -m "chore: bump version to x.y.z"
git push

# 2. Tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# 3. Create GitHub Release with CHANGELOG excerpt
```

<details>
<summary>→ More details: references/release.md</summary>
Version file sync, CHANGELOG flow, build artifacts, migration notes, hotfix process.
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
<summary>→ More details: references/review.md</summary>
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

**Rule**: No test coverage confidence = no permission to refactor.

<details>
<summary>→ More details: references/refactoring.md</summary>
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

**Rule**: Each agent still follows full workflow for their role.

<details>
<summary>→ More details: references/multi-agent.md</summary>
Worktree naming, branch strategy, merge flow.
</details>

---

## Quick Reference

### Typical Flows

**Feature**: Exploration → Design → Implementation → Pre-Commit → PR

**Bug Fix**: Exploration → Bug Fix → Pre-Commit → PR

**Refactor**: Exploration → (verify test coverage) → Design → Implementation → Pre-Commit → PR

**Release**: (After PRs merged) → Version bump → CHANGELOG update → Tag → GitHub Release

### Task Status (if project uses tracking)

`Pending` → `In Progress` → `In Review` → `Done`

Roadmap format: `| ID | Priority | Item | Status | GH |`
