# Cross-Agent Compatibility

How different AI coding agents discover and consume project context files. Use this reference when generating files in Phase 3 to ensure all agents are served.

---

## File Generation Matrix

| Generated File | Claude Code | Cursor | Codex | Human |
|---|---|---|---|---|
| AGENTS.md | via `@` import in CLAUDE.md | direct read | direct read | — |
| CLAUDE.md | auto-load at session start | — | — | — |
| .cursor/rules/*.mdc | — | auto-inject by glob match | — | — |
| .claude/rules/*.md | auto-inject by path match | — | — | — |
| README.md | — | — | — | primary audience |
| FUTURE_ROADMAP.md | reads on demand | reads on demand | reads on demand | primary audience |
| docs/decisions/*.md | reads on demand | reads on demand | reads on demand | primary audience |

---

## CLAUDE.md Strategy: @import

Claude Code auto-reads `CLAUDE.md` at session start. It does NOT auto-read `AGENTS.md`. To bridge the gap without duplication:

```markdown
@AGENTS.md
```

Place this as the sole content of `CLAUDE.md`. Claude Code's `@path` import syntax expands the referenced file inline at launch. The result: Claude Code sees the full AGENTS.md content automatically, while other agents read AGENTS.md directly.

### When to add Claude Code-specific content

Only add content below the `@AGENTS.md` import if you have rules that apply exclusively to Claude Code sessions and would be noise for other agents. Example:

```markdown
@AGENTS.md

## Claude Code Only

- Use `.claude/rules/` for path-specific constraints (Cursor uses `.cursor/rules/` instead)
- Auto memory is enabled; Claude will save learnings to `~/.claude/projects/`
```

### Git tracking

Both `AGENTS.md` and `CLAUDE.md` should be committed to git. This ensures any developer cloning the repo gets full AI context regardless of which agent they use.

---

## Rules File Syntax Differences

Cursor and Claude Code both support path-scoped rules that auto-inject when the agent works with matching files. The mechanism is identical; the syntax differs.

### Cursor: `.cursor/rules/*.mdc`

```markdown
---
globs: "src/**/collectors/**"
---

# Collector Rules

- Rule 1
- Rule 2
```

- File extension: `.mdc`
- Directory: `.cursor/rules/`
- Frontmatter key: `globs`
- Glob syntax: standard glob patterns
- Files without `globs` frontmatter load unconditionally

### Claude Code: `.claude/rules/*.md`

```markdown
---
paths:
  - "src/**/collectors/**"
---

# Collector Rules

- Rule 1
- Rule 2
```

- File extension: `.md`
- Directory: `.claude/rules/`
- Frontmatter key: `paths` (YAML list)
- Glob syntax: standard glob patterns with brace expansion (`*.{ts,tsx}`)
- Files without `paths` frontmatter load unconditionally

### Generation Strategy

When the skill generates rules files, create both versions with identical content body. Only the frontmatter and file location differ:

1. Write the rules content once (mentally or in a variable)
2. Emit `.cursor/rules/{name}.mdc` with `globs:` frontmatter
3. Emit `.claude/rules/{name}.md` with `paths:` frontmatter

For simple projects with 1-2 rules files, the duplication is minimal. For complex projects, consider documenting in AGENTS.md that both dirs contain equivalent rules.

---

## Agent Context Loading Summary

### Global instructions (unified)

All three agents receive the same user-level instructions from a single file (`global-instructions.md` in dotfiles), symlinked to each agent's expected path:

- `~/.claude/CLAUDE.md` -> `global-instructions.md`
- `~/.codex/AGENTS.md` -> `global-instructions.md` (same file)
- Cursor User Rules -> manually synced from the "Approach" section

This ensures consistent methodology, environment awareness, and conventions across agents.

### Claude Code

1. Auto-reads `~/.claude/CLAUDE.md` (global instructions, symlinked from dotfiles) at session start
2. Auto-reads project `CLAUDE.md` (walks up directory tree from cwd)
3. Expands `@path` imports in CLAUDE.md files
4. Auto-reads `.claude/rules/*.md` (unconditional rules at launch, path-scoped on demand)
5. Has auto-memory at `~/.claude/projects/<project>/memory/`
6. Does NOT auto-read `AGENTS.md` unless imported via CLAUDE.md

### Cursor

1. Reads `AGENTS.md` when instructed by `.cursor/rules/project.mdc` (the project rule should include "Read AGENTS.md for full context"); AGENTS.md is NOT auto-injected into the system prompt
2. Auto-injects `.cursor/rules/*.mdc` based on glob matches
3. Has user-level rules in Cursor Settings > Rules for AI (manually synced from `global-instructions.md`)
4. Supports skills via `~/.claude/skills/` and `~/.cursor/skills/` directories

### Codex

1. Auto-reads `~/.codex/AGENTS.md` (global instructions, symlinked from same dotfile as Claude Code)
2. Reads project-level `AGENTS.md` (concatenated after global)
3. Supports `~/.codex/AGENTS.override.md` for temporary session overrides
4. Receives task instructions via `prompt` or `prompt-file` in GitHub Actions
5. Has its own skill system at `~/.codex/skills/`
6. No auto-discovery of `.cursor/rules/` or `.claude/rules/`

---

## Codex Cold-Start Requirements

When Codex picks up a task from GitHub Actions, it starts with zero prior context. AGENTS.md must be self-sufficient:

- **Implementation status table**: So Codex knows what exists and what doesn't
- **Directory responsibilities**: So Codex knows where to put new code
- **Design conventions**: So Codex follows project patterns
- **Entry commands**: So Codex can verify its work
- **Security constraints**: So Codex doesn't commit secrets

The task-specific instructions come from the GitHub Actions `prompt` parameter or a prompt file, not from AGENTS.md. AGENTS.md provides the project context; the prompt provides the task.
