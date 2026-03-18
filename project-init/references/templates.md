# File Templates

Templates for files generated during Phase 3 (Document). Replace `{{PLACEHOLDERS}}` with project-specific values. The AI agent fills these contextually from the design doc / user description — no templating engine required.

These templates apply to software, automation, docs, config, research, and similar git-tracked projects. Omit or adapt sections that do not apply; do not force app-style structure onto non-code-first repos.

## Contents

- [AGENTS.md](#agentsmd)
- [CLAUDE.md](#claudemd)
- [README.md](#readmemd)
- `.cursor/rules/project.mdc`
- `.claude/rules/project.md`
- [Module-specific rules](#cursorrulesmodulemdc-example-collectors)
- [docs/decisions/000-template.md](#docsdecisions000-templatemd)
- [ROADMAP.md](#roadmapmd) — strategic direction (all projects)
- [ISSUES.md](#issuesmd) — local issue tracker (non-GitHub projects)
- [docs/ISSUE_DETAILS.md](#docsissue_detailsmd) — assignment packets (non-GitHub projects)
- [.github/ISSUE_TEMPLATE/task.md](#githubissue_templatetaskmd) — GitHub issue templates
- [.github/ISSUE_TEMPLATE/bug-report.md](#githubissue_templatebug-reportmd)
- [.github/ISSUE_TEMPLATE/design-note.md](#githubissue_templatedesign-notemd)
- [.agents/projects/README.md](#agentsprojectsreadmemd) — evolution logs directory
- [.gitignore](#gitignore-universal-base)
- [.env.example](#envexample)

---

## AGENTS.md

```markdown
# AGENTS.md — {{PROJECT_NAME}} AI Context

## Project Overview

{{1-2 sentence description of what the project does and who it's for.}}

## Project Shape

- **Project Type**: {{software | automation | docs | config | research | other}}
- **Primary Artifacts**: {{scripts, docs, templates, configs, datasets, etc.}}
- **Language / Runtime**: {{LANGUAGE_AND_VERSION_IF_APPLICABLE}}
- **Package Manager**: {{PACKAGE_MANAGER_IF_APPLICABLE}}
- **Project Layout**: {{LAYOUT_DESCRIPTION}}
- **Storage**: {{DATABASE_OR_NA}}
- **Key Tools / Libraries**: {{COMMA_SEPARATED_LIST}}
- **Verification**: {{tests, lint, manual checklist, or other quality gates}}

## Current Implementation Status

> Update this table as each action node completes. AI agents should read this first in new sessions.

| Module | Status | Note |
|--------|--------|------|
| {{module_name}} | **skeleton** / empty / done | {{brief note}} |

## Key Design Conventions

### {{Convention Category 1}}

- {{Rule 1}}
- {{Rule 2}}

### {{Convention Category 2}}

- {{Rule 1}}

## Directory Responsibilities

| Directory | Responsibility | Key Files |
|-----------|---------------|-----------|
| {{dir}} | {{what it does}} | {{important files}} |

## Code Style

- {{style rule 1}}
- {{style rule 2}}

## Entry / Workflow Commands

\`\`\`bash
{{primary run command}}
{{secondary run command}}
\`\`\`

## Workflow Commands (optional)

- Add dependency: `{{add dep command}}`
- Lint: `{{lint command}}`
- Format: `{{format command}}`
- Test: `{{test command}}`

## Commit Conventions

Use conventional commits: `<type>: <subject>`

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`

## Task Entry

{{Choose one of the two blocks below based on project hosting. Delete the other.}}

{{For GitHub-hosted projects:}}
- **Direction**: See `ROADMAP.md` for milestones and project phases
- **Current work**: `gh issue list --label p1` for high-priority items
- **Pick a task**: `gh issue list --state open --assignee @me` or unassigned p1/p2 issues
- **Deep context**: Check `.agents/projects/` for evolution logs on complex work
- **File new issues**: Use the `file-issue` skill or `gh issue create`
- **Recommended labels**: Priority — `p1` (this week), `p2` (this quarter), `p3` (later). Type — `bug`, `enhancement`, `docs`, `agent-generated`

{{For non-GitHub projects:}}
- **Direction**: See `ROADMAP.md` for milestones and project phases
- **Current work**: See `ISSUES.md` for active items
- **Detailed notes**: See `docs/ISSUE_DETAILS.md` for assignment packets (if exists)

## Security Constraints

- Never commit: `.env`, `*.db`, API keys, tokens
- Test API calls must be mocked
- `.env.example` contains key names only, no real values
- Logs must not contain full API keys or tokens

## Open Questions

1. {{Question from design doc or discussion}}
2. {{Another open question}}

## Design Document

Full design: `{{DESIGN_DOC_FILENAME}}`
```

---

## CLAUDE.md

```markdown
@AGENTS.md
```

That's it. Claude Code's `@path` import expands AGENTS.md inline at session start. Add Claude Code-specific instructions below only if there are rules that apply exclusively to Claude Code and not other agents.

Do not move canonical project facts into `CLAUDE.md`; keep them in `AGENTS.md`.

---

## README.md

```markdown
# {{PROJECT_NAME}}

{{One-paragraph project description.}}

## Architecture

{{Brief architecture description or mermaid diagram.}}

## Quick Start

\`\`\`bash
# Clone
git clone {{REPO_URL}}
cd {{PROJECT_DIR}}

# Install or prepare project tools (if applicable)
{{INSTALL_COMMAND}}

# Configure (if applicable)
{{CONFIG_COMMANDS}}

# Run or perform the main workflow
{{RUN_COMMAND}}
\`\`\`

## Directory Structure

\`\`\`
{{PROJECT_DIR}}/
├── {{primary_dirs}}
├── docs/                # if applicable
│   └── decisions/
├── scripts/             # if applicable
├── AGENTS.md
├── CLAUDE.md
├── ROADMAP.md
├── README.md
├── {{DEPENDENCY_FILE_OR_PRIMARY_PROJECT_FILE}}
└── .gitignore
\`\`\`

## Development

\`\`\`bash
{{DEV_INSTALL_COMMAND}}
{{LINT_COMMAND}}
{{FORMAT_COMMAND}}
{{TEST_COMMAND}}
\`\`\`

## Roadmap

See [ROADMAP.md](ROADMAP.md) for project direction and milestones.

## License

{{LICENSE}}
```

---

## .cursor/rules/project.mdc

```markdown
---
globs: "**/*"
---

# {{PROJECT_NAME}} — Project Rules

Read `AGENTS.md` at project root for full context before making any changes.

## Critical Constraints

- {{constraint_1, e.g., "All timestamps in UTC"}}
- {{constraint_2, e.g., "API keys from .env only, never hardcoded"}}
- {{constraint_3, e.g., "All data validated before storage"}}

## Code Style

- {{style_rule_1}}
- {{style_rule_2}}

## Architecture

- Project root detected by locating `{{PROJECT_ROOT_MARKER}}`
- Runtime dirs (data/, logs/) resolved from project root when such dirs exist
- Package manager / toolchain: `{{PACKAGE_MANAGER_OR_TOOLCHAIN}}`

## Do NOT

- Commit secrets (.env, *.db, tokens)
- Use `{{ANTI_PATTERN_1}}`
- {{other prohibitions}}
```

---

## .claude/rules/project.md

```markdown
---
paths:
  - "**/*"
---

# {{PROJECT_NAME}} — Project Rules

Read `AGENTS.md` at project root for full context before making any changes.

## Critical Constraints

- {{constraint_1}}
- {{constraint_2}}
- {{constraint_3}}

## Code Style

- {{style_rule_1}}
- {{style_rule_2}}

## Architecture

- Project root detected by locating `{{PROJECT_ROOT_MARKER}}`
- Runtime dirs (data/, logs/) resolved from project root when such dirs exist
- Package manager / toolchain: `{{PACKAGE_MANAGER_OR_TOOLCHAIN}}`

## Do NOT

- Commit secrets (.env, *.db, tokens)
- Use `{{ANTI_PATTERN_1}}`
- {{other prohibitions}}
```

Note: Content is identical to `.cursor/rules/project.mdc`. The only difference is the frontmatter syntax (`globs` vs `paths`) and file extension (`.mdc` vs `.md`).

---

## .cursor/rules/{module}.mdc (example: collectors)

```markdown
---
globs: "src/**/collectors/**"
---

# Collector Module Rules

- {{module-specific rule 1}}
- {{module-specific rule 2}}
- {{module-specific rule 3}}
```

## .claude/rules/{module}.md (example: collectors)

```markdown
---
paths:
  - "src/**/collectors/**"
---

# Collector Module Rules

- {{module-specific rule 1}}
- {{module-specific rule 2}}
- {{module-specific rule 3}}
```

---

## docs/decisions/000-template.md

```markdown
# ADR-NNN: {{Title}}

**Date**: {{YYYY-MM-DD}}
**Status**: proposed | accepted | deprecated | superseded

## Context

{{What is the issue or decision we're facing?}}

## Decision

{{What did we decide and why?}}

## Consequences

**Positive**:
- {{benefit 1}}

**Negative**:
- {{tradeoff 1}}

**Neutral**:
- {{observation}}
```

---

## ROADMAP.md

> All projects get this file. It captures strategic direction, NOT individual tasks.

```markdown
# Roadmap

> Strategic direction and milestones for {{PROJECT_NAME}}.
> For current work items, see {{GitHub Issues | `ISSUES.md`}}.

## Vision

{{What does "done" look like for this project? 1-2 sentences.}}

## Current Phase: {{Phase Name}}

{{What the project is focused on right now. 2-3 sentences.}}

### Milestones

| Milestone | Target | Theme |
|-----------|--------|-------|
| {{M1}} | {{timeframe}} | {{what it achieves}} |
| {{M2}} | {{timeframe}} | {{what it achieves}} |

## Future Phases

### {{Next Phase Name}}

{{Brief description of what comes after the current phase.}}

## Non-Goals (for now)

- {{Thing that is explicitly deferred}}
- {{Another non-goal}}
```

---

## ISSUES.md

> Non-GitHub projects only. Lightweight local issue tracker.

```markdown
# Issues

> Active work items for {{PROJECT_NAME}}.
> Agents: read `AGENTS.md` first, then this file.
> For project direction, see `ROADMAP.md`.

## Active

| ID | Priority | Item | Status | Assigned |
|----|----------|------|--------|----------|
| {{T-001}} | p1 | {{description}} | Pending | — |
| {{T-002}} | p2 | {{description}} | Pending | — |

## Done (recent)

| ID | Item | Completed | Note |
|----|------|-----------|------|

---

Status flow: `Pending` → `In Progress` → `Done`
Priority: `p1` (this week) · `p2` (this quarter) · `p3` (later)
*Details for complex items: `docs/ISSUE_DETAILS.md`*
```

---

## docs/ISSUE_DETAILS.md

> Non-GitHub projects only. Detailed assignment packets for complex tasks.
> For GitHub projects, this content lives in the GitHub Issue body (using the design-note template).

```markdown
# Issue Details

> Detailed implementation notes for complex issues from `ISSUES.md`.
> Each section should be usable as an agent assignment packet without additional verbal handoff.

## {{Issue_ID}}: {{Title}}

**Status**: Pending | In Progress | Done

**Objective**: {{What this work changes and why}}

**Background / evidence**:
- {{Evidence 1}}
- {{Evidence 2}}

**Read first**:
- {{File path 1}}
- {{File path 2}}

**Editable scope**:
- {{Allowed file or directory 1}}
- {{Allowed file or directory 2}}

**Out of scope**:
- {{Nearby file or concern that should not be absorbed into this task}}

**Done criteria**:
- {{Completion check 1}}
- {{Completion check 2}}

**Approach**: {{How to implement this}}

**Key decisions**:
- {{Decision 1}}
- {{Decision 2}}

**Verification / closeout notes**:
- {{What to test or how the issue was closed}}

---

*This file can be long. Agents should read `ISSUES.md` first for the overview.*
```

---

## .github/ISSUE_TEMPLATE/task.md

> GitHub-hosted projects only. Standard task template.

```markdown
---
name: Task
about: Something that needs to be done (improvement, refactor, feature)
title: ''
labels: ''
assignees: ''
---

- [ ] set a priority label (p1, p2, p3)
- [ ] assign it to someone if applicable
- [ ] delete this checklist

## Description

(Add enough context that anyone on the team — or an AI agent — could understand what needs to be done. Doesn't need to be long.)

### Definition of Done

(What does it mean for this task to be complete? Be as specific as possible.
For example: running command X should produce output Y, or test Z passes.)
```

---

## .github/ISSUE_TEMPLATE/bug-report.md

> GitHub-hosted projects only. Bug report template.

```markdown
---
name: Bug Report
about: Report a bug or regression
title: ''
labels: bug
assignees: ''
---

**Describe the bug**

(What is broken — concrete symptoms, error messages.)

**To Reproduce**

1. Step one
2. Step two

**Expected behavior**

(What should happen instead.)

**Additional context**

(Root cause analysis if known, file:line references, environment details.)
```

---

## .github/ISSUE_TEMPLATE/design-note.md

> GitHub-hosted projects only. Assignment packet for complex work that needs detailed implementation context.

```markdown
---
name: Design Note
about: Complex work requiring detailed implementation context
title: ''
labels: ''
assignees: ''
---

- [ ] set a priority label (p1, p2, p3)
- [ ] delete this checklist

## Objective

(What this work changes and why — one paragraph.)

## Background / Evidence

- (Evidence or context 1)
- (Evidence or context 2)

## Scope

**In scope:**
- (File or area 1)
- (File or area 2)

**Out of scope:**
- (Explicitly excluded concern)

## Approach

(Implementation strategy — can be brief or detailed.)

## Definition of Done

- [ ] (Completion criterion 1)
- [ ] (Completion criterion 2)
```

---

## .agents/projects/README.md

> Tracked in git. Created at init, content grows organically during dev-workflow.

```markdown
# Evolution Logs

This directory contains narrative logs for complex, multi-step work that spans
multiple issues or sessions — architecture evolution, large refactors, research
experiments, etc.

Each file tracks ONE topic over time. Create a new file when starting a
significant multi-issue effort. Format:

\`\`\`
{topic}.md — e.g., auth-migration.md, perf-optimization.md
\`\`\`

These are NOT issue bodies — they are living documents that accumulate context,
decisions, benchmarks, and status over time. Reference related GitHub Issues
or ISSUES.md entries by ID.
```

---

## .gitignore (universal base)

```gitignore
# Environment
.env
.env.local

# Database
*.db
*.sqlite3

# Runtime directories (keep dir via .gitkeep)
data/*
!data/.gitkeep
logs/*
!logs/.gitkeep
backup/*
!backup/.gitkeep

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/

# Node (include if applicable)
# node_modules/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Cursor plans (local to developer)
.cursor/plans/
```

---

## .env.example

```bash
# {{PROJECT_NAME}} — Environment Variables
# Copy to .env and fill in real values

# Required
{{KEY_1}}=
{{KEY_2}}=

# Optional
{{OPTIONAL_KEY}}=
```
