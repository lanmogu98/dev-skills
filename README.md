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

## dev-workflow

Comprehensive engineering workflow for LLM agents and human developers.

**Use when:** implementing features, fixing bugs, writing tests, refactoring, preparing commits, creating PRs, or reviewing code.

**Structure:**
- `SKILL.md` — Core principles + task router
- `references/exploration.md` — Code reading, scope confirmation
- `references/design.md` — **Design via tests (tests = specification)**
- `references/bugfix.md` — **Bug fix workflow (reproduce → test → fix)**
- `references/implementation.md` — Coding standards
- `references/precommit.md` — Pre-commit checklist
- `references/pullrequest.md` — PR creation guidelines
- `references/refactoring.md` — Refactoring-specific guidance
- `references/review.md` — Code review checklist
- `references/multi-agent.md` — Worktree isolation for parallel agents

## License

Apache 2.0
