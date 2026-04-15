# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2026-04-15

Recalibrated against anthropics/skills@main skill-creator (PRs #547 + #350 merged). Targets remaining gaps from the v2.2.0 alignment pass plus new skill-creator guidance: "look for repeated work → bundle scripts", descriptive eval names, caution against subjective assertions.

### Added
- **dev-workflow** + **project-init** + **file-issue**: prior-session CFG-003 completion — three-skill prefix-strategy coordination (project-init Phase 1 prefix choice + priority scale confirm, Phase 5 seeding with chosen prefix; exploration.md "Discovering New Issues" subsection; templates.md prefix variable rendering rules)
- **dev-workflow**: cross-skill handoff note after Phase 1 Step 4 — when exploration surfaces out-of-scope bugs/debt, use `file-issue` rather than expanding scope
- **file-issue**: cross-skill return-to-work note after Step 7 — when filed mid-`dev-workflow` session, return to the interrupted phase instead of starting a new workflow
- **project-init**: "why" reasoning added to Phase 1 intro (decomposition granularity), Phase 2 Step 0 (existing-state check), Phase 3 §3a (AGENTS.md SSOT rationale), Phase 5 Step 3 (issue seeding as cold-start solution)
- **file-issue**: complete input-to-output example covering both GitHub (`gh issue create` with labels/body) and non-GitHub (`ISSUES.md` row append) destinations
- **file-issue**: bundled helper script `scripts/append_local_issue.py` — handles deterministic non-GitHub mechanics (parse prefix declaration, scan for max existing ID, append formatted row) previously re-derived inline on every invocation. Multi-prefix *selection* remains LLM judgment per the plan's scope boundary. Runnable with `--dry-run`; exits non-zero with clear messages for undeclared prefixes or missing Active tables.
- **dev-workflow** / **project-init** / **file-issue**: bootstrap `evals/evals.json` with 3 descriptive test prompts each (9 total) — descriptive kebab-case IDs per latest skill-creator guidance (line 188), assertions left empty pending first eval run to avoid subjective-check bloat (line 203).

### Changed
- **dev-workflow**: remove Task Status subsection from Quick Reference — redundant with Phase 4 precommit content
- **repo**: update AGENTS.md "What We Override" table — evals bootstrapped; description optimization now ready to run on demand (PR #547 removed `ANTHROPIC_API_KEY` requirement)

### Not Adopted
- `compatibility` frontmatter field (PR #350): evaluated per latest skill-creator guidance (line 68). All three skills depend on ambient dev-environment tooling (git, gh) — field is documented as "optional, rarely needed" and doesn't warrant adoption.

## [2.2.0] - 2026-03-07

### Changed
- **Both skills**: Rewrite descriptions for better triggering — narrative "pushy" style per updated skill-creator guidance
- **Both skills**: Remove non-standard `metadata.version` from SKILL.md frontmatter (versions tracked here only)
- **dev-workflow**: Soften all prescriptive language (STOP/Rule:/Do NOT) across SKILL.md and 7 reference files — explain the "why" behind each instruction instead of commanding
- **dev-workflow**: Add scene-specific guidance to all 8 `<details>` blocks (when to load each reference)
- **dev-workflow**: Add Core Principles reasoning ("because...")
- **dev-workflow**: Add Phase 2 vs 2-B routing guidance
- **dev-workflow**: Add Step 0 (task status update) to Phase 1
- **dev-workflow**: Add decision router to Quick Reference
- **dev-workflow**: Change reference file `→ Next:` navigation to "Return to SKILL.md" (SKILL.md controls flow)
- **project-init**: Add existing file detection step to Phase 2 (Scaffold)
- **project-init**: Add review verification step to Phase 5 (Handoff)
- **project-init**: Add table of contents to `templates.md` (>300 lines per skill-creator guidance)
- **repo**: Update AGENTS.md "What We Override" — description optimization now available but not yet adopted

## [2.1.0] - 2026-03-06

### Added
- **project-init** skill: Cross-agent project initialization protocol
  - 5-phase workflow: Ingest → Plan → Scaffold → Document → Review → Handoff
  - File templates for AGENTS.md, CLAUDE.md, rules files, .gitignore, .env.example
  - Cross-agent compatibility matrix (Cursor, Claude Code, Codex)
  - GitHub Actions templates for both Claude Code Action and Codex Action
  - Multi-dimensional review checklists
- README updated to describe both skills and their relationship

## [2.0.0] - 2026-01-12

### Changed
- **Major restructure**: Embed core steps from all references directly into SKILL.md
- SKILL.md now self-sufficient: agent can follow workflow without loading references
- References become optional "deep dive" supplements using `<details>` blocks
- Description expanded with more trigger keywords for better agent discovery
- Reduced agent decision overhead: no Task Router lookup required

### Why This Change
- Problem: Agents weren't loading reference files before starting work
- Solution: SKILL.md now contains all essential guidance (307 lines, under 500 limit)
- References remain for detailed context when needed

## [1.5.0] - 2026-01-12

### Added
- "When Fix Attempt Fails" section in `bugfix.md`: guidance for multi-round bug fixes
- "When to Ask User for More Data" subsection: specific artifacts to request per bug type
- "Check Architectural Assumptions" subsection: evaluate if architecture needs change
- "Signs You're Skipping TDD" self-check list: identify when TDD is being bypassed

### Changed
- `bugfix.md` now addresses iterative debugging scenarios (not just single-attempt fixes)
- Enhanced Phase 1, 2, 3 with practical insights from real bug fix retrospectives

## [1.4.0] - 2026-01-09

### Added
- `FUTURE_ROADMAP.md` template with `GH` column for GitHub issue linking
- Bug reporting flow documentation: GitHub Issues → Roadmap → PR closes issue
- Issue closing guidance in `bugfix.md` and `pullrequest.md`
- "Closing GitHub Issues" section in `pullrequest.md` with keyword reference

### Changed
- Task System section in `SKILL.md` now documents the full bug reporting flow
- Status flow expanded: added "In Review" state

## [1.3.0] - 2026-01-09

### Added
- Pre-flight Checklist: branch creation, task status, code reading — visible immediately
- "Relationship with Plan Mode" section: clarifies how to use with IDE planning tools
- Imperative language in description: "REQUIRED", "MUST load FIRST"

### Changed
- Description rewritten for stronger agent triggering
- "When to Load This Skill" now uses "MUST" instead of "Load immediately"
- Moved critical steps (branch, status) from exploration.md to SKILL.md top

### Fixed
- Agent skipping workflow when entering Plan Mode first (now explicitly addressed)

## [1.2.0] - 2026-01-08

### Changed
- Make skill language-agnostic: multi-language test commands, generic terminology
- "Type hints" → "Type annotations" (universal terminology)
- Remove Python-specific examples (DataFrame, pyproject.toml hardcoding)

## [1.1.0] - 2026-01-08

### Added
- `bugfix.md`: Dedicated bug fix workflow (reproduce → test → fix → verify)
- Version field in SKILL.md frontmatter
- Prerequisites checklist in `implementation.md` as gate
- Navigation links (`→ Next`) to `review.md` and `multi-agent.md`
- "Integration with Main Workflow" section in `multi-agent.md`

### Changed
- `exploration.md`: Fix navigation to point to `design.md` (was `implementation.md`)
- Make `FUTURE_ROADMAP.md` references conditional ("if project uses task tracking")
- Update Task Router to include bug fix entry

## [1.0.0] - 2026-01-08

### Added
- `design.md`: Separate design phase emphasizing "tests are design"
- "When to Load This Skill" section in SKILL.md for better agent discovery
- Refactoring test rules: coverage verification before refactoring

### Changed
- Simplify `implementation.md`: focus on coding standards only
- Unify test requirements across `design.md` and `refactoring.md`
- Update Task Router to include design phase

## [0.1.0] - Initial Release

### Added
- Initial dev-workflow skill
- Core references: exploration, implementation, precommit, pullrequest, refactoring, review, multi-agent
