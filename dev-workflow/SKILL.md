---
name: dev-workflow
description: |
  Engineering workflow for changing code in an existing codebase: exploration, test design, implementation, pre-commit, and shipping. Use when implementing a feature, fixing a bug, refactoring, or preparing a commit or PR in a project whose deliverable is running code. Carries the parts no other skill covers: doc-to-code drift checks, scope discipline via file-issue, conditional pre-commit doc sync, and the Domain Review Protocol for projects with real-world consequences. Routes the standard phases to dedicated skills where those are installed, and falls back to its own references where they are not. Do not use for documentation-only edits, research notes, prose, or repos whose artifact is a proof, dataset, or slide deck rather than executable code.
---

# Dev Workflow

Engineering standards for code changes, plus a routing table to the skills that own each phase.

## Core Principles

1. **Code is truth** — Read code first. Docs drift; the running code is what ships.
2. **Design before code** — Define "done" before writing it. For executable code that means tests; for other artifacts it means a stated acceptance check.
3. **Minimal blast radius** — Touch only necessary files. Every changed file is a potential regression.
4. **Adapt to the repo** — The phases below describe a repo with tests, a CHANGELOG, and a feature-branch policy. Read what the repo actually has and skip steps whose preconditions are absent.

Priority stack: Security → Correctness → Data Integrity → Availability → Performance → Docs → Speed.

## Delegation Map

Prefer the owning skill when it is installed. The fallback reference carries the same material in portable form for agents without the plugin (Codex, Cursor).

| Concern | Owning skill or command | Fallback reference |
|---|---|---|
| Test-first design | `superpowers:test-driven-development` | `references/design.md` |
| Debugging a reported bug | `superpowers:systematic-debugging` | `references/bugfix.md` |
| Isolated workspace for parallel work | `superpowers:using-git-worktrees`, native worktree tools | `references/multi-agent.md` |
| Claiming work is done | `superpowers:verification-before-completion` | `references/precommit.md` |
| Merge, push, or open a PR | `superpowers:finishing-a-development-branch` | `references/pullrequest.md` |
| Reviewing a diff or PR | `/code-review`, `/security-review` | `references/review.md` |
| Acting on review feedback | `superpowers:receiving-code-review` | `references/review.md` |

This skill owns what the table does not: exploration and doc-to-code sync, scope discipline, conditional pre-commit doc updates, refactoring safety, merge-conflict resolution, and Domain Review.

## Phase 1: Exploration

Do this before planning or coding.

1. **Set task status** — If the project tracks work in GitHub Issues or `ISSUES.md`, mark the task In Progress.
2. **Read the relevant code** — Find existing patterns and the exact insertion point. Search for a similar implementation before writing a new one.
3. **Check doc-to-code sync** — Where `README.md`, `CHANGELOG.md`, or a task tracker contradicts the code, fix the doc before building on it.
4. **Confirm scope** — Cross-reference the task definition against what the code actually does.

**Scope discipline**: when exploration surfaces a bug or debt item outside this task, capture it with the `file-issue` skill instead of widening the task. Scope creep is the most common cause of failed reviews.

**Branching**: if the repo works on feature branches, cut `feature/<name>` or `fix/<name>` now and rebase onto main regularly. Some repos are single-contributor and commit on `main`, and some gate commits behind owner approval — follow the repo's `AGENTS.md` over this default.

<details>
<summary>→ references/exploration.md — read when exploring an unfamiliar codebase or verifying doc-code sync</summary>
Exploration order table, doc sync verification table, branch strategy.
</details>

## Phase 2: Design and Implementation

Route to `superpowers:test-driven-development` for the full red-green-refactor discipline, or `superpowers:systematic-debugging` when the task is a reported bug. What this skill adds on top:

| Change type | What "done" must be defined as, before coding |
|---|---|
| New feature | Happy path, edge cases, error cases — as failing tests |
| Bug fix | A test that reproduces the bug, plus a regression guard |
| Refactor | Existing tests cover the behavior being restructured; if they do not, add them first |
| Code with no test harness | A written, checkable acceptance criterion and the command that demonstrates it |

If writing the test feels impossible, the requirement is not yet clear. Clarify before coding — it is cheaper than debugging later.

Code standards while implementing: type annotations on signatures, small testable functions, explicit error handling with no silent `except:`, and no secrets in code.

<details>
<summary>→ references/implementation.md — read when handling flaky tests, LLM/API calls, or dependency issues</summary>
Flaky test handling, LLM/API usage, dependency management.
</details>

<details>
<summary>→ references/refactoring.md — read when refactoring involves state isolation, config handling, or graceful termination</summary>
State isolation, config handling, graceful termination.
</details>

## Phase 3: Pre-Commit

Run the checks whose preconditions the repo actually meets. Skipping a check because the repo has no such file is correct; skipping it because it is inconvenient is not.

| Check | Applies when |
|---|---|
| Full test suite passes | The repo has tests |
| Lint and format clean | The repo defines a lint command |
| `CHANGELOG.md` updated | The file exists and the change alters behavior |
| `README.md` updated | The file documents a CLI flag, config key, or install step you changed |
| No debug code, no secrets | Always |

Commit format is `type(scope): summary` with types `feat` | `fix` | `docs` | `test` | `chore` | `refactor`.

```bash
git commit -m "feat(auth): add OAuth2 support"
git commit -m "fix(parser): handle empty input"
```

<details>
<summary>→ references/precommit.md — read when unsure which docs need updating or how to mark task status</summary>
Doc sync table by change type, task status updates, CHANGELOG sections.
</details>

## Phase 4: Ship

Hand merge, push, and PR creation to `superpowers:finishing-a-development-branch`. Constraints this skill adds:

- **One PR, one concern** — do not mix a feature, a fix, and a refactor.
- **Small PRs** — aim under 400 lines; split larger changes.
- **Complete** — code, tests, and docs land in the same PR.
- **Self-review the diff** before requesting review.

<details>
<summary>→ references/pullrequest.md — read when writing a PR description or choosing a merge strategy</summary>
PR description template, responding to feedback, merge strategies, GitHub issue linking.
</details>

<details>
<summary>→ references/merge-conflicts.md — read when a rebase or merge reports conflicts</summary>
Resolving conflicts by intent, re-testing after resolution, branch drift signals.
</details>

## Domain Review (Conditional)

Activates only when the project's `AGENTS.md` contains a `## Domain Review Protocol` section. It adds three intervention points so that domain-laden choices — thresholds, formulas, data models, priority assignments — reach the human instead of being silently embedded.

| Intervention | Placement | Blocking |
|---|---|---|
| Brief-In | Before design starts | No — FYI unless the human objects |
| Checkpoint | At each domain-laden decision | Yes — wait for the human |
| Brief-Out | Before commit | No — silence means proceed |

Skip a checkpoint when the design doc already fixes that decision and project-init confirmed it. In non-interactive runs, apply design-doc defaults and list every decision in the PR description.

<details>
<summary>→ references/domain-review.md — read when the project AGENTS.md has a Domain Review Protocol section</summary>
Decision weight matrix, intervention templates, non-interactive fallback rules.
</details>
