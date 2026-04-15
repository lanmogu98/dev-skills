---
name: project-init
description: |
  One-time project initialization protocol for setting up new repositories or organized project workspaces optimized for human-AI collaborative development. Use this skill whenever the user wants to start a new project, bootstrap a repo, scaffold work from a design doc, create AGENTS.md or CLAUDE.md context files, or set up a project for use with Cursor, Claude Code, or Codex. This applies to software, automation, documentation, configuration, research, and similar git-tracked projects. Also trigger when the user mentions "new repo", "project setup", "design doc to code", "create project structure", or asks about AI context files or cross-agent compatibility. This skill runs once to create the scaffold, then hands off to dev-workflow for ongoing development.
---

# Project Init

Set up a new project repository or organized workspace optimized for human-AI collaborative development across Cursor, Claude Code, and Codex.

## Scope

This skill covers **project initialization** (one-time) and **ongoing project health** (review methodology, ADR).

- Applies to software repos and non-software repos alike (automation, docs, config, research, operations, etc.)
- Adapt the scaffold to the project's actual artifacts; do **not** force app-style directories, package files, or test runners onto repos that do not need them

- Runs BEFORE `dev-workflow` — creates the scaffold that `dev-workflow` operates within
- After init completes, hand off to `dev-workflow` for feature/fix/refactor cycles
- The review methodology (Phase 4) can be invoked any time, not just during init

## Phase 0: Ingest

> Understand the project before touching files.

1. Read the design document, requirements, or user description
2. Identify: project name, project type, primary artifacts, key modules, tooling/runtime, and deployment or operating model
3. Ask clarifying questions if critical info is missing:
   - What are the primary artifacts in this project (code, docs, configs, scripts, datasets, templates)?
   - What is the primary language/runtime and package manager, if applicable?
   - Is there a design doc or spec to follow?
   - Which agents will be used (Cursor / Claude Code / Codex)?
   - Will there be cloud-triggered tasks (GitHub Actions)?
4. **Determine project hosting**: Is this project on GitHub? Check `git remote -v` for a `github.com` URL, or ask the user. This determines the issue tracking strategy:
   - **GitHub-hosted** → GitHub Issues as SSOT for task tracking
   - **Non-GitHub** (local, GitLab, Bitbucket, etc.) → local `ISSUES.md` for task tracking
5. If no design doc exists, help the user articulate scope before proceeding

**Decision gate**: Do not proceed to Phase 1 until the project's purpose, tech stack, hosting model, and rough module list are clear.

## Phase 1: Plan

> Decompose the project into actionable nodes.

**Why decomposition matters here**: The point isn't to produce a Gantt chart — it's to give a cold-start agent (human or AI) enough context to pick up *any* single node and make forward progress without re-reading the entire design doc. Nodes that are too coarse ("build the backend") force every future agent to re-derive the substructure. Nodes that are too fine become noise. Aim for the level where acceptance criteria are obvious from the node description alone.

1. Extract milestones from the design doc or requirements
2. For each milestone, define action nodes:
   - **ID**: short identifier (e.g., `A1.1`)
   - **Task**: one-sentence description
   - **Dependencies**: which nodes must complete first
   - **Acceptance criteria**: how to verify completion
3. Create a dependency graph (use mermaid if the agent supports it)
4. **Determine issue destination** based on hosting (from Phase 0):
   - **GitHub-hosted**: action nodes will become GitHub Issues via `gh issue create` in Phase 5
   - **Non-GitHub**: action nodes will populate `ISSUES.md` in Phase 5
5. **Choose issue prefix strategy** (non-GitHub projects only):
   - **Single prefix** (default): one prefix for all issues (e.g., `T`). Good for most projects.
   - **Multiple prefixes**: category-based prefixes (e.g., `SEC`, `CFG`, `AGENT`). Use when the project has distinct workstreams that benefit from visual grouping.
   - Ask the user which strategy to use. Record the choice for Phase 5 seeding.
6. **Confirm priority scale** (non-GitHub projects only) — present the default (`p1` this week / `p2` this quarter / `p3` later) and ask if the user wants to customize the time horizons.
7. Present the plan to the user for review before proceeding

**Decision gate**: User approves the plan or requests changes.

## Phase 2: Scaffold

> Create the project structure and enable version control.

Read `references/templates.md` for `.gitignore` and `.env.example` templates. Execute these steps in order:

0. **Check existing state**: If the directory already has files, assess what exists before scaffolding. Preserve user work — don't overwrite existing files without asking. If a design doc exists but no scaffold, proceed normally. If a partial scaffold exists, identify gaps and fill them.

   *Why this step comes first*: The most common failure mode for init skills is silently clobbering a user's in-progress work (a half-written README, a custom `.gitignore`, an existing `AGENTS.md`). Even a partial scaffold often encodes decisions the user has already committed to. Asking first is always cheaper than restoring from git reflog.
1. **Directory structure** based on project type and ecosystem conventions:
   - Python app/lib: `src/{package}/` layout with `pyproject.toml`
   - Node app/lib: `src/` with `package.json`
   - Docs / config / ops / research repos: create only the directories that match the real artifacts (`docs/`, `scripts/`, `templates/`, `references/`, domain-specific folders, etc.)
   - Other: follow the ecosystem's standard layout
2. **Dependency management / tooling**:
   - Python: `pyproject.toml` (PEP 621) with `uv` as package manager; create `.python-version` for version pinning. `uv` manages its own Python installations independently — even if the system uses conda/miniforge/pyenv, `uv` downloads and maintains separate Python binaries at `~/.local/share/uv/python/`. Do NOT create a conda env for uv-managed projects.
   - Node: `package.json` with lockfile
   - Non-code-first repos: only add manifests, linters, or checkers that the project will actually use
   - Include dev dependencies (linter, formatter, type checker, test runner) only when they are part of the real workflow
3. **Git init + .gitignore**:
   - Language-appropriate ignores
   - Always ignore: `.env`, `*.db`, IDE-specific dirs
   - Use `dir/*` + `!dir/.gitkeep` for runtime dirs (data/, logs/, backup/)
4. **GitHub repo**: create with `gh repo create` if requested
5. **Environment template (if needed)**: `.env.example` with key names only (no real values)
6. **Entry point or workflow skeleton**: CLI, script, docs index, runbook, or equivalent artifact that anchors the project
7. **Working memory directory**: Create `.memory/MEMORY.md` as the project-level memory index.
   - **Projects you own**: track `.memory/` in git
   - **Upstream/open-source projects**: add `.memory/` to `.gitignore`
   - This directory serves as the cross-agent memory location (Claude Code, Cursor, Codex)

## Phase 3: Document

> Generate the multi-layer documentation hierarchy.

Read `references/templates.md` for full templates. Read `references/cross-agent.md` for agent-specific file generation rules.

Generate these files:

### 3a. AGENTS.md (universal AI context)

**Why AGENTS.md is the SSOT**: Cursor, Claude Code, and Codex each have their own native context-loading mechanism (`.cursorrules`, `CLAUDE.md`, `AGENTS.md`), but duplicating project facts across three files guarantees drift. Instead, keep all durable facts in `AGENTS.md` and have each tool's native file *import* from it. CLAUDE.md uses `@AGENTS.md`; Cursor reads `AGENTS.md` natively; Codex reads `AGENTS.md` natively. One write, three readers.

The single source of truth for all AI agents. Must contain:

- Project positioning (1-2 sentences)
- Project shape / tech stack summary
- Current implementation status table
- Key design conventions and constraints
- Directory responsibilities
- Code style rules
- Entry point commands
- **Task entry** — how to find current work (see template in `references/templates.md`):
  - GitHub-hosted: point to `gh issue list` commands
  - Non-GitHub: point to `ISSUES.md`
  - All projects: reference `ROADMAP.md` for strategic direction
- Security constraints
- Open questions / decisions pending

### 3b. CLAUDE.md (Claude Code bridge)

A minimal file that imports AGENTS.md using Claude Code's native `@path` syntax:

```markdown
@AGENTS.md
```

This gives Claude Code auto-loaded access to the full AGENTS.md content at session start. Keep project facts in `AGENTS.md`; add Claude Code-specific instructions below the import only if needed.

### 3c. Agent-specific rules (only when needed)

Generate path-scoped rules for **both** Cursor and Claude Code only when the project has meaningful subtree-specific constraints that would benefit from scoped auto-injection. For simple repos, `AGENTS.md` alone may be enough.

When scoped rules are needed:

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
- Roadmap summary (link to `ROADMAP.md`)

### 3e. ADR system

- `docs/decisions/000-template.md` with Context / Decision / Consequences structure
- First ADR documenting the tech stack / toolchain choice

### 3f. Project direction and task management

Generate based on project hosting (determined in Phase 0). GitHub Issues provides labels, assignees, cross-references, and PR auto-close — so GitHub-hosted projects should use it as the single source of truth for work items. Non-GitHub projects need a local equivalent that agents can read and update without external tooling.

**All projects:**

- `ROADMAP.md` — strategic direction, milestones, vision. This is NOT an issue list — it answers "where is this project going?" and changes infrequently. See template in `references/templates.md`.

**GitHub-hosted projects:**

- `.github/ISSUE_TEMPLATE/task.md` — standard task template (description + Definition of Done)
- `.github/ISSUE_TEMPLATE/bug-report.md` — bug report template (symptoms + repro steps + expected behavior)
- `.github/ISSUE_TEMPLATE/design-note.md` — assignment packet template for complex work (objective, scope, approach, done criteria)
- `.agents/projects/` — directory for evolution logs on complex multi-step work (create with README, content grows organically during dev-workflow). Tracked in git.
- Add recommended labels to AGENTS.md: `p1`/`p2`/`p3` (priority) + `bug`/`enhancement`/`docs`/`agent-generated` (type)
- Do NOT generate local issue files — GitHub Issues is the SSOT

**Non-GitHub projects:**

- `ISSUES.md` — lightweight local issue tracker (active items + recent done). See template in `references/templates.md`.
- `docs/ISSUE_DETAILS.md` (optional) — detailed assignment packets for complex tasks. Generate only if the project has work that needs rich implementation notes beyond what fits in `ISSUES.md`.

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

**Collaboration quality**: Are docs sufficient for a cold-start agent to understand and contribute? Is AGENTS.md complete enough for Codex to pick up a task from GitHub Issues (or `ISSUES.md`)?

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
3. **Seed initial work items** from Phase 1 action nodes:
   - **GitHub-hosted**: file first 1-3 action nodes as GitHub Issues via `gh issue create`, using the appropriate issue template. Add priority labels.
   - **Non-GitHub**: list first 1-3 action nodes in `ISSUES.md` as Pending, using the prefix strategy chosen in Phase 1. Populate the footer's prefix declaration and priority scale from the user's choices. For multi-prefix projects, assign each seeded issue to the prefix matching its workstream category.

   *Why seeding matters*: An empty tracker is the cold-start problem in miniature — the next agent (or the user themselves, a week later) opens an empty `ISSUES.md` and has to rediscover what work exists. Seeding 1-3 concrete items gives the next session an obvious entry point, and also serves as a worked example of the project's own issue format so future issues stay consistent.
4. **Announce**: Summarize what was created, what the next development step is, and which skill (`dev-workflow`) takes over

After handoff, the `dev-workflow` skill governs the development cycle (explore -> design -> implement -> commit -> PR).
