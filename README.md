# Skills

Personal skill collection for AI coding agents. Compatible with [OpenSkills](https://github.com/numman-ali/openskills) and Claude Code.

## Installation

```bash
npm i -g openskills
openskills install lanmogu98/dev-skills-repo
openskills sync
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [dev-workflow](./dev-workflow/) | Engineering workflow for development tasks in existing codebases |
| [project-init](./project-init/) | Repository initialization protocol for AI-assisted development |

The two skills are complementary: `project-init` creates the scaffold (one-time), then `dev-workflow` operates within it (ongoing).

## dev-workflow

Comprehensive engineering workflow for LLM agents and human developers.

**Use when:** implementing features, fixing bugs, writing tests, refactoring, preparing commits, creating PRs, or reviewing code.

**Structure:**

- `SKILL.md` — Core principles + task router
- `references/exploration.md` — Code reading, scope confirmation
- `references/design.md` — Design via tests (tests = specification)
- `references/bugfix.md` — Bug fix workflow (reproduce → test → fix)
- `references/implementation.md` — Coding standards
- `references/precommit.md` — Pre-commit checklist
- `references/pullrequest.md` — PR creation guidelines
- `references/refactoring.md` — Refactoring-specific guidance
- `references/review.md` — Code review checklist
- `references/multi-agent.md` — Worktree isolation for parallel agents
- `references/domain-review.md` — HITL domain review protocol (conditional)

## project-init

Cross-agent project initialization protocol. Sets up a new repository optimized for human-AI collaborative development across Cursor, Claude Code, and Codex.

**Use when:** bootstrapping a project, starting from a design doc, setting up a repo for multi-agent collaboration, or initializing git/GitHub with AI context files.

**Structure:**

- `SKILL.md` — 5-phase protocol (Ingest → Plan → Scaffold → Document → Review → Handoff)
- `references/templates.md` — File templates for AGENTS.md, CLAUDE.md, rules, .gitignore, etc.
- `references/cross-agent.md` — Agent compatibility matrix and context loading reference
- `references/cloud-dispatch.md` — GitHub Actions workflow templates (Claude Code Action + Codex Action)
- `references/review-checklists.md` — Multi-dimensional review framework

## Development

This repo is the **source of truth** for user-created skills. The distribution chain:

```text
Source Repo (this repo, development)
  ~/iCloud/Personal/my-project/my-skills/dev-skills-repo/
      ↓ symlink (local machine, immediate effect)
Install Directory (dotfiles, gitignored)
  ~/iCloud/dev-env/dotfiles/agent-config/skills/
  ├── dev-workflow → ../../../../Personal/.../dev-skills-repo/dev-workflow
  └── project-init → ../../../../Personal/.../dev-skills-repo/project-init
      ↓ symlink (already configured)
Active (Claude Code / Codex)
  ~/.claude/skills/ → dotfiles/agent-config/skills/
```

**How it works:**

- Edit files in this repo → changes take effect immediately in Claude Code (via symlink chain)
- `git push` distributes changes to remote for other machines
- New machine setup: clone this repo → create symlinks in dotfiles (see `skills.manifest.md`)

**Why symlink, not copy:**

- `cp -r` requires manual re-copy after every edit — easy to forget, causes version drift
- Symlinks keep a single source of truth with zero sync friction

## License

Apache 2.0
