---
name: dev-workflow
description: "Engineering workflow for development tasks in existing codebases. Use when: implementing features, fixing bugs, writing tests, refactoring code, preparing commits, creating PRs, reviewing code, or planning development tasks. Covers the full cycle from code exploration to pull request. Not needed for one-off scripts or general code explanations outside project context."
---

# Dev Workflow

Engineering standards for humans and LLM agents working in codebases.

## When to Load This Skill

**Load this skill immediately if the task involves ANY of:**
- Implementing a feature or enhancement
- Fixing a bug
- Writing or modifying tests
- Refactoring existing code
- Preparing a commit or PR
- Reviewing code changes

**Do NOT skip this skill** just because the task seems simple. Even "small" changes benefit from the design-first approach.

## Core Principles

1. **Code is truth** — Read codebase first; docs may be outdated
2. **Design before code** — Define behavior via tests before implementation
3. **Tests are design** — Writing tests = specifying behavior, not just verification
4. **Docs are not optional** — Code + Tests + Docs = Complete commit
5. **Minimal blast radius** — Touch only necessary files; no drive-by refactors

## Priority Stack (When Rules Conflict)

1. **Security** — No secrets exposed, no vulnerabilities
2. **Correctness** — Code does what it's supposed to
3. **Data Integrity** — No data loss or corruption
4. **Availability** — System remains operational
5. **Performance** — Acceptable speed/resource usage
6. **Documentation** — Docs reflect reality
7. **Speed of Delivery** — Ship fast (but not at cost of above)

## Task Router

Load references based on current task. Use `cat <base_directory>/references/<file>` to load.

| Task Type | Reference File |
|-----------|----------------|
| Start new task / understand code | `exploration.md` |
| Design feature / write tests | `design.md` |
| Write implementation code | `implementation.md` |
| Prepare commit | `precommit.md` |
| Create or update PR | `pullrequest.md` |
| Refactor (no behavior change) | `design.md` + `refactoring.md` |
| Review code | `review.md` |
| Multiple agents in parallel | `multi-agent.md` |

For tasks spanning multiple phases, load references in sequence.

## Quick Reference

### Commit Format

`type(scope): summary`

Types: `feat` | `fix` | `docs` | `test` | `chore` | `refactor`

### Task System (Roadmap-centric)

- **Read first**: `FUTURE_ROADMAP.md` (Now/Next, ≤1-2 screens)
- **Implementation details**: `docs/DESIGN_REMAINING_ISSUES.md`
- **History**: `docs/roadmap/ROADMAP_ARCHIVE.md` (read-only, don't pollute)

Status flow: `Pending` → `In Progress` → `Done (recent)` → `Archived`

### Typical Task Flow

For a complete task, load references in sequence:
1. `exploration.md` — Understand code, confirm scope, set status to In Progress
2. `design.md` — **Define behavior via tests BEFORE coding**
3. `implementation.md` — Write code to make tests pass
4. `precommit.md` — Run tests, update docs, commit
5. `pullrequest.md` — Create PR, self-review, respond to feedback

> **Critical:** Do NOT skip step 2. If you find yourself writing implementation code without tests, STOP and go back to `design.md`.
