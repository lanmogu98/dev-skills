# Skills

Personal skill collection for AI coding agents. Compatible with Claude Code, Cursor, and Codex.

## Installation

```bash
# Via manage-skills.sh (recommended)
manage-skills.sh link-user

# Or manual symlinks (see skills.manifest.md for details)
```

## Available Skills

| Skill | Description |
| --- | --- |
| [dev-workflow](./dev-workflow/) | Engineering workflow for code changes in existing codebases |
| [project-init](./project-init/) | Repository initialization protocol for AI-assisted development |
| [research-mermaid](./research-mermaid/) | Mermaid diagrams for scientific methods, mathematical relationships, and research systems |

`project-init` and `dev-workflow` are complementary: `project-init` creates the scaffold (one-time), then `dev-workflow` operates within it (ongoing).

## dev-workflow

Engineering workflow for LLM agents and human developers working on code.

**Use when:** implementing features, fixing bugs, refactoring, or preparing commits and PRs in a project whose deliverable is running code. Not for documentation-only edits, research notes, or repos whose artifact is a proof, dataset, or slide deck.

**Delegation:** where a dedicated skill owns a phase — `superpowers:test-driven-development`, `superpowers:systematic-debugging`, `superpowers:using-git-worktrees`, `superpowers:verification-before-completion`, `superpowers:finishing-a-development-branch`, `superpowers:receiving-code-review`, `/code-review` — SKILL.md routes to it. The `references/` files stay as the portable fallback for agents without those plugins installed (Codex, Cursor). What this skill owns outright: doc-to-code drift checks, scope discipline via `file-issue`, conditional pre-commit doc sync, refactoring safety, merge-conflict resolution, and Domain Review.

**Structure:**

- `SKILL.md` — Core principles + task router
- `references/exploration.md` — Code reading, scope confirmation
- `references/design.md` — Design via tests (tests = specification)
- `references/bugfix.md` — Bug fix workflow (reproduce → test → fix)
- `references/implementation.md` — Coding standards
- `references/precommit.md` — Pre-commit checklist
- `references/pullrequest.md` — PR creation guidelines
- `references/merge-conflicts.md` — Resolving conflicts at rebase/merge time
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

## research-mermaid

Create, revise, or review Mermaid diagrams for research methods, experiments, mathematical mappings, proof dependencies, and scientific systems, including architectural contributions and iterative feedback. It first establishes the reader takeaway from the conversation, asking one high-level question only when the focus is unclear. The skill reads the destination repository's constraints and preserves the distinction between proposed relationships, proved results, and empirical evidence.

The entrypoint routes to research semantics, rendering checks, a visual baseline, and seven diagram frameworks as needed. Architectural change, iteration, and supporting-information roles extend those frameworks rather than adding new families. `assets/templates/` contains ten runnable Mermaid examples, including branching methods, architecture change, and retained feedback across iterations; `assets/themes/` provides light and dark configurations.

`evals/evals.json` contains seven artifact-generation tasks: the original Map theorem, controlled systems benchmark, and branching tiled kernel, plus selective recomputation, counterexample-guided repair, interacting feedback loops, and a protocol with contextual and constraint inputs. Their source packets live in `evals/files/`. `evals/trigger-evals.json` contains positive Mermaid cases and adjacent exclusions for quantitative plotting, prose-only explanation, and explicitly requested other formats. These are evaluation inputs, not a claim that all runs or user reviews have passed. This adaptation of robust-skills retains its pinned upstream source and MIT notice inside the skill directory.

Local plans, baseline snapshots, generated diagrams, checks, and user feedback live in `draft/research-mermaid/`; evaluation outputs go under `draft/research-mermaid/evaluation-artifacts/` (Git-ignored). Reusable test cases remain in `research-mermaid/evals/`.

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
Active (Claude Code / Cursor / Codex)
  ~/.claude/skills/ → dotfiles/agent-config/skills/  (whole dir)
  ~/.cursor/skills/ → dotfiles/agent-config/skills/  (whole dir)
  ~/.codex/skills/{name} → dotfiles/agent-config/skills/{name}  (per-skill)
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
