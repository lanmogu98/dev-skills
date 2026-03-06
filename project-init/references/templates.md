# File Templates

Templates for files generated during Phase 3 (Document). Replace `{{PLACEHOLDERS}}` with project-specific values. The AI agent fills these contextually from the design doc / user description — no templating engine required.

---

## AGENTS.md

```markdown
# AGENTS.md — {{PROJECT_NAME}} AI Context

## Project Overview

{{1-2 sentence description of what the project does and who it's for.}}

## Tech Stack

- **Language**: {{LANGUAGE}} {{VERSION}}
- **Python Environment**: {{e.g., "uv manages Python independently (~/.local/share/uv/python/), do not use conda/miniforge"}}
- **Package Manager**: {{PACKAGE_MANAGER}}
- **Project Layout**: {{LAYOUT_DESCRIPTION}}
- **Storage**: {{DATABASE}}
- **Key Libraries**: {{COMMA_SEPARATED_LIST}}
- **Lint/Format**: {{LINTER}}
- **Type Check**: {{TYPE_CHECKER}}
- **Test**: {{TEST_RUNNER}}

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

## Entry Commands

\`\`\`bash
{{primary run command}}
{{secondary run command}}
\`\`\`

## Development Commands

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

# Install dependencies
{{INSTALL_COMMAND}}

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
{{RUN_COMMAND}}
\`\`\`

## Directory Structure

\`\`\`
{{PROJECT_DIR}}/
├── {{src_layout}}
├── tests/
├── docs/
│   └── decisions/
├── scripts/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── FUTURE_ROADMAP.md
├── {{DEPENDENCY_FILE}}
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

- Project root detected by locating `{{DEPENDENCY_FILE}}`
- Runtime dirs (data/, logs/) resolved from project root
- Package manager: `{{PACKAGE_MANAGER}}`

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

- Project root detected by locating `{{DEPENDENCY_FILE}}`
- Runtime dirs (data/, logs/) resolved from project root
- Package manager: `{{PACKAGE_MANAGER}}`

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

| ID | Item | Completed |
|----|------|-----------|

---

*Archive: `docs/roadmap/ROADMAP_ARCHIVE.md`*
*Details: `docs/DESIGN_REMAINING_ISSUES.md`*
```

---

## docs/DESIGN_REMAINING_ISSUES.md

```markdown
# Design & Implementation Notes

> Detailed implementation paths for roadmap items. When picking an item from FUTURE_ROADMAP.md, open the matching section here.

## {{Milestone_1_Name}}

### {{Action_Node_ID}}: {{Title}}

**Approach**: {{How to implement this}}

**Key decisions**:
- {{Decision 1}}
- {{Decision 2}}

**Testing notes**:
- {{What to test}}

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
