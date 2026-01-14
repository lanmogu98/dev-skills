# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2026-01-14

### Added
- `references/release.md`: Release management workflow (SemVer, CHANGELOG flow, build artifacts, migration notes, hotfix process)
- Phase 6: Release section in SKILL.md with embedded quick reference
- Release flow added to Quick Reference typical flows

### Why This Change
- Dev workflow covered exploration → PR, but lacked guidance for the release phase
- Users need clear versioning strategy, CHANGELOG conventions, and distribution best practices
- Generalizes Chrome extension advice into language/platform-agnostic guidance

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

## [1.4.0] - 2025-01-09

### Added
- `FUTURE_ROADMAP.md` template with `GH` column for GitHub issue linking
- Bug reporting flow documentation: GitHub Issues → Roadmap → PR closes issue
- Issue closing guidance in `bugfix.md` and `pullrequest.md`
- "Closing GitHub Issues" section in `pullrequest.md` with keyword reference

### Changed
- Task System section in `SKILL.md` now documents the full bug reporting flow
- Status flow expanded: added "In Review" state

## [1.3.0] - 2025-01-09

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

## [1.2.0] - 2025-01-08

### Changed
- Make skill language-agnostic: multi-language test commands, generic terminology
- "Type hints" → "Type annotations" (universal terminology)
- Remove Python-specific examples (DataFrame, pyproject.toml hardcoding)

## [1.1.0] - 2025-01-08

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

## [1.0.0] - 2025-01-08

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
