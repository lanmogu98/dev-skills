# AGENTS.md — dev-skills-repo

## What This Repo Is

Source of truth for user-created AI coding skills. Skills here are distributed to Claude Code (and other agents) via symlink — edits take immediate effect.

## Distribution Chain

```text
This Repo (source, git-tracked)
  ~/iCloud/Personal/my-project/my-skills/dev-skills-repo/
      ↓ symlink (relative, 4 levels up)
dotfiles/agent-config/skills/ (install dir, gitignored by dotfiles)
      ↓ symlink (whole dir)
~/.claude/skills/ (active — Claude Code reads from here)
```

**Key rule**: Only edit files in this repo. Never edit copies in dotfiles or ~/.claude/skills/ — they are symlinks pointing here.

## Current Skills

| Skill | Purpose | Relationship |
|-------|---------|-------------|
| `dev-workflow/` | Feature/fix/refactor/PR cycle | Ongoing development workflow |
| `project-init/` | Repo initialization for AI-assisted dev | One-time scaffold, then hand off to dev-workflow |

`domain-review` is not a standalone skill — it's a conditional extension inside `dev-workflow/references/domain-review.md`, activated by a project's `AGENTS.md`.

## Skill Format Conventions

### Normative Reference

The `skill-creator` skill (installed at `~/.claude/skills/skill-creator/`) defines Anthropic's official format. **Before creating a new skill, check for updates:**

```bash
~/iCloud/dev-env/dotfiles/agent-config/scripts/manage-skills.sh update skill-creator
```

Then read `~/.claude/skills/skill-creator/SKILL.md` for the latest conventions. Key rules from skill-creator:

- **SKILL.md frontmatter**: only `name` and `description` fields. Description is the primary trigger mechanism — be comprehensive and slightly "pushy" about when to use the skill.
- **Directory structure**: `SKILL.md` (required) + optional `scripts/`, `references/`, `assets/`
- **Progressive disclosure**: metadata (~100 words) → SKILL.md body (<500 lines) → references (loaded on demand)
- **References one level deep**: all reference files link directly from SKILL.md, with guidance on when to read them
- **Writing style**: explain the "why" behind instructions; avoid heavy-handed MUSTs; prefer reasoning over rigid rules
- **Concise by default**: only add context Claude doesn't already have

### What We Override

Our distribution model differs from skill-creator's assumptions:

| skill-creator says | We do instead | Why |
|---|---|---|
| Eval-driven iteration with subagents + benchmark viewer | Test by using in a real project, then iterate | No formal eval infra; skills are validated through real usage |
| `scripts/package_skill.py` to distribute `.skill` files | Symlink chain (no packaging) | Zero-sync-friction distribution |
| Description optimization via `scripts/run_loop.py` | Available but not yet adopted | Will adopt if undertriggering issues observed |

## Development Rules

1. **Test by using**: No pytest suite for skills. Validate by using the skill in a real project, then iterate.
2. **One concern per skill**: Each skill should have a single, clear purpose. Use references for sub-topics (like domain-review within dev-workflow).
3. **Conditional extensions pattern**: To add optional behavior to an existing skill, create a reference file and gate it on a project-level config (e.g., `## Domain Review Protocol` in AGENTS.md). Do not create a separate skill for it.
4. **SKILL.md < 500 lines**: Move detailed content to `references/`. Include `<details>` links so Claude loads them on demand.
5. **Relative symlink paths**: When documenting or creating symlinks, use relative paths (4 levels up: `../../../../Personal/my-project/my-skills/dev-skills-repo/<skill>`).

## Git Workflow

- Branch: `main` only (small repo, single contributor)
- Commits: conventional commits (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`)
- Push: `git push` distributes to other machines via GitHub remote
- No CI/CD — validation is manual (use in real project, then iterate)

## Related Documentation

- Distribution chain details: this repo's `README.md` (Development section)
- Install/update commands: `~/iCloud/dev-env/dotfiles/agent-config/skills.manifest.md`
- Dotfiles context: `~/iCloud/dev-env/dotfiles/agent-config/AGENTS.md`
