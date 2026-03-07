---
name: project-init
description: |
  One-time project initialization protocol for setting up new repositories optimized for human-AI collaborative development. Use this skill whenever the user wants to start a new project, bootstrap a repo, scaffold a codebase from a design doc, create AGENTS.md or CLAUDE.md context files, or set up a project for use with Cursor, Claude Code, or Codex. Also trigger when the user mentions "new repo", "project setup", "design doc to code", "create project structure", or asks about AI context files or cross-agent compatibility. This skill runs once to create the scaffold, then hands off to dev-workflow for ongoing development.
---

# Project Init

Set up a new project repository optimized for human-AI collaborative development across Cursor, Claude Code, and Codex.

## Scope

This skill covers **project initialization** (one-time) and **ongoing project health** (review methodology, ADR).

- Runs BEFORE `dev-workflow` — creates the scaffold that `dev-workflow` operates within
- After init completes, hand off to `dev-workflow` for feature/fix/refactor cycles
- The review methodology (Phase 4) can be invoked any time, not just during init

## Phase 0: Ingest

> Understand the project before touching files.

1. Read the design document, requirements, or user description
2. Identify: project name, language/framework, key modules, data sources, deployment model
3. Ask clarifying questions if critical info is missing:
   - What is the primary language and package manager?
   - Is there a design doc or spec to follow?
   - Which agents will be used (Cursor / Claude Code / Codex)?
   - Will there be cloud-triggered tasks (GitHub Actions)?
4. If no design doc exists, help the user articulate scope before proceeding

**Decision gate**: Do not proceed to Phase 1 until the project's purpose, tech stack, and rough module list are clear.

## Phase 1: Plan

> Decompose the project into actionable nodes.

1. Extract milestones from the design doc or requirements
2. For each milestone, define action nodes:
   - **ID**: short identifier (e.g., `A1.1`)
   - **Task**: one-sentence description
   - **Dependencies**: which nodes must complete first
   - **Acceptance criteria**: how to verify completion
3. Create a dependency graph (use mermaid if the agent supports it)
4. Present the plan to the user for review before proceeding

**Decision gate**: User approves the plan or requests changes.

## Phase 2: Scaffold

> Create the project structure and enable version control.

Read `references/templates.md` for `.gitignore` and `.env.example` templates. Execute these steps in order:

0. **Check existing state**: If the directory already has files, assess what exists before scaffolding. Preserve user work — don't overwrite existing files without asking. If a design doc exists but no scaffold, proceed normally. If a partial scaffold exists, identify gaps and fill them.
1. **Directory structure** based on language conventions:
   - Python: `src/{package}/` layout with `pyproject.toml`
   - Node: `src/` with `package.json`
   - Other: follow the ecosystem's standard layout
2. **Dependency management**:
   - Python: `pyproject.toml` (PEP 621) with `uv` as package manager; create `.python-version` for version pinning. `uv` manages its own Python installations independently — even if the system uses conda/miniforge/pyenv, `uv` downloads and maintains separate Python binaries at `~/.local/share/uv/python/`. Do NOT create a conda env for uv-managed projects.
   - Node: `package.json` with lockfile
   - Include dev dependencies (linter, formatter, type checker, test runner)
3. **Git init + .gitignore**:
   - Language-appropriate ignores
   - Always ignore: `.env`, `*.db`, IDE-specific dirs
   - Use `dir/*` + `!dir/.gitkeep` for runtime dirs (data/, logs/, backup/)
4. **GitHub repo**: create with `gh repo create` if requested
5. **Environment template**: `.env.example` with key names only (no real values)
6. **Entry point skeleton**: CLI with argument parsing, importable package `__init__.py`

## Phase 3: Document

> Generate the multi-layer documentation hierarchy.

Read `references/templates.md` for full templates. Read `references/cross-agent.md` for agent-specific file generation rules.

Generate these files:

### 3a. AGENTS.md (universal AI context)

The single source of truth for all AI agents. Must contain:
- Project positioning (1-2 sentences)
- Tech stack summary
- Current implementation status table
- Key design conventions and constraints
- Directory responsibilities
- Code style rules
- Entry point commands
- Security constraints
- Open questions / decisions pending

### 3b. CLAUDE.md (Claude Code bridge)

A minimal file that imports AGENTS.md using Claude Code's native `@path` syntax:

```
@AGENTS.md
```

This gives Claude Code auto-loaded access to the full AGENTS.md content at session start. Add Claude Code-specific instructions below the import only if needed.

### 3c. Agent-specific rules

Generate path-scoped rules for **both** Cursor and Claude Code:

- `.cursor/rules/project.mdc` — project-wide constraints (globs frontmatter)
- `.cursor/rules/{module}.mdc` — module-specific rules
- `.claude/rules/project.md` — same content, `paths` frontmatter syntax
- `.claude/rules/{module}.md` — module-specific rules

See `references/cross-agent.md` for syntax differences between the two systems.

### 3d. README.md (human-facing)

- Project overview with architecture diagram
- Quick start (clone, install deps, run)
- Directory structure
- Development commands
- Roadmap / action nodes summary

### 3e. ADR system

- `docs/decisions/000-template.md` with Context / Decision / Consequences structure
- First ADR documenting the tech stack / toolchain choice

### 3f. Task management

If the project uses roadmap-centric task management:
- `FUTURE_ROADMAP.md` — short Now/Next task hub from Phase 1 action nodes
- `docs/DESIGN_REMAINING_ISSUES.md` — detailed implementation notes

### 3g. GitHub Actions (if cloud dispatch requested)

Read `references/cloud-dispatch.md` for workflow templates. Generate:
- `.github/workflows/claude.yml` — Claude Code Action for @claude mentions + automation
- `.github/workflows/codex.yml` — Codex Action for automated tasks
- `.github/prompts/` — shared prompt files for task definitions

## Phase 4: Review

> Iterative multi-dimensional review until stable.

Read `references/review-checklists.md` for the full framework. Execute up to 3 review rounds:

### Round 1: Consistency

- Cross-reference all generated files for naming consistency
- Verify file paths mentioned in docs match actual files
- Check .gitignore covers all sensitive/runtime files
- Ensure README commands actually work

### Round 2: Dimensional review

Two perspectives:

**Collaboration quality**: Are docs sufficient for a cold-start agent to understand and contribute? Is AGENTS.md complete enough for Codex to pick up a task from FUTURE_ROADMAP.md?

**Functional correctness**: Does the scaffold match the design doc? Are all modules represented? Are constraints captured in rules files?

### Round 3: Review-the-review

- Check that Round 1-2 fixes didn't introduce new issues
- Verify no duplication across AGENTS.md / README / rules files
- Confirm git status is clean

**Stop condition**: No high or medium severity issues found in a round.

## Phase 5: Handoff

> Prepare the project for ongoing development.

0. **Verify review clean**: Confirm Phase 4 review completed with no remaining high/medium issues. If issues remain, resolve them before handoff.
1. **Initial commit**: Stage all files, commit with `chore: init project scaffold`
2. **Status table**: Ensure AGENTS.md has a current implementation status table with all modules listed
3. **Next actions**: First 1-3 action nodes from Phase 1 are listed in FUTURE_ROADMAP.md as Pending
4. **Announce**: Summarize what was created, what the next development step is, and which skill (`dev-workflow`) takes over

After handoff, the `dev-workflow` skill governs the development cycle (explore -> design -> implement -> commit -> PR).
