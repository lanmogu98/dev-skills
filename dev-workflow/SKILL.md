---
name: dev-workflow
description: |
  Engineering workflow for development tasks in existing codebases. 
  Use when: implementing features, fixing bugs, writing tests, 
  refactoring code, preparing commits, creating PRs, reviewing code, 
  or planning development tasks. Covers the full cycle from code 
  exploration to pull request. Not needed for one-off scripts or 
  general code explanations outside project context.
---

# Dev Workflow

Engineering standards for humans and LLM agents working in codebases.

## Core Principles

1. **Code is truth** — Read codebase first; docs may be outdated
2. **Tests before code** — Write/update tests first, then implement
3. **Docs are not optional** — Code + Tests + Docs = Complete commit
4. **Minimal blast radius** — Touch only necessary files; no drive-by refactors
5. **Explicit over implicit** — Type hints, specific exceptions, no magic defaults

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
| Start new task / understand code | `references/exploration.md` |
| Write code or tests | `references/implementation.md` |
| Prepare commit | `references/precommit.md` |
| Create or update PR | `references/pullrequest.md` |
| Refactor (no behavior change) | `references/implementation.md` + `references/refactoring.md` |
| Review code | `references/review.md` |
| Multiple agents in parallel | `references/multi-agent.md` |

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
2. `implementation.md` — Write tests first, then code
3. `precommit.md` — Run tests, update docs, commit
4. `pullrequest.md` — Create PR, self-review, respond to feedback
