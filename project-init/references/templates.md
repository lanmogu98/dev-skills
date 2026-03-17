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
- [FUTURE_ROADMAP.md](#future_roadmapmd)
- [docs/DESIGN_REMAINING_ISSUES.md](#docsdesign_remaining_issuesmd)
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
├── FUTURE_ROADMAP.md
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

See [FUTURE_ROADMAP.md](FUTURE_ROADMAP.md) for current and next tasks.

If the repo also keeps a long-lived backlog file such as `TASKS.md`, use that for backlog/history and keep `FUTURE_ROADMAP.md` focused on active multi-agent work.

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

## FUTURE_ROADMAP.md

```markdown
# Roadmap

> Short, high-signal index of current and next work.
> Agents: read this first. Do not read archive unless needed.
> If the repo also uses `TASKS.md`, keep backlog/history there.

## Now (In Progress)

| ID | Item | Status | Dependencies |
|----|------|--------|-------------|

## Next (Pending)

| ID | Item | Status | Dependencies |
|----|------|--------|-------------|
| {{A1.1}} | {{first action node description}} | Pending | — |
| {{A1.2}} | {{second action node}} | Pending | A1.1 |
| {{A1.3}} | {{third action node}} | Pending | — |

## Done (recent)

| ID | Item | Completed | Note |
|----|------|-----------|------|

---

*Archive: `docs/roadmap/ROADMAP_ARCHIVE.md`*
*Details: `docs/DESIGN_REMAINING_ISSUES.md`*
```

---

## docs/DESIGN_REMAINING_ISSUES.md

```markdown
# Design & Implementation Notes

> Detailed implementation paths for roadmap items. When picking an item from FUTURE_ROADMAP.md, open the matching section here.
> Each section should be usable as an agent assignment packet without additional verbal handoff.

## {{Milestone_1_Name}}

### {{Action_Node_ID}}: {{Title}}

**Status**: Pending | In Progress | Done (recent)

**Objective**: {{What this work is responsible for changing and why}}

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

*This file can be long. It is not the default agent entrypoint — agents should read FUTURE_ROADMAP.md first.*
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
