# Review Checklists

Multi-dimensional review framework for project initialization. Execute up to 3 rounds. Stop when no high or medium severity issues remain.

---

## Round 1: Consistency Check

Verify internal consistency across all generated files.

### File Cross-References

- [ ] Every directory mentioned in README.md exists on disk
- [ ] Every directory mentioned in AGENTS.md exists on disk
- [ ] File paths in `.cursor/rules/*.mdc` globs match actual directory structure
- [ ] File paths in `.claude/rules/*.md` paths match actual directory structure
- [ ] .gitignore covers all files/dirs listed as "never commit" in AGENTS.md
- [ ] Entry commands in AGENTS.md match README.md quick start section
- [ ] Dev commands (lint, format, test) are consistent across AGENTS.md and README.md

### Naming Consistency

- [ ] Package name is consistent across dependency file, directory names, and entry points
- [ ] Module names in AGENTS.md status table match actual directory/file names
- [ ] Conventional commit types listed in AGENTS.md match `dev-workflow` skill conventions

### Completeness

- [ ] Every module from the design doc has a directory or file
- [ ] Every module is listed in the AGENTS.md status table
- [ ] `.env.example` lists all API keys / secrets referenced in the design doc
- [ ] `.gitignore` exists and covers: `.env`, `*.db`, `__pycache__/`, `.venv/`, IDE dirs
- [ ] ADR template exists at `docs/decisions/000-template.md`
- [ ] At least one real ADR exists (e.g., `001-toolchain.md`)

### Commands Verification

- [ ] Dependency install command succeeds (or would succeed with real keys)
- [ ] Entry point runs without import errors (even if modules are stubs)
- [ ] Lint/format commands are valid for the chosen toolchain

---

## Round 2: Dimensional Review

Two perspectives evaluated independently.

### Dimension A: Human-AI Collaboration Quality

Assess whether the repository structure enables effective long-term collaboration.

| Check | Question | Severity |
|-------|----------|----------|
| Cold-start readability | Can a new AI session understand the project by reading only AGENTS.md? | High |
| Status currency | Does the implementation status table reflect actual file states? | High |
| Constraint discoverability | Are all critical constraints (security, data, conventions) in rules files, not just docs? | Medium |
| CLAUDE.md bridge | Does CLAUDE.md exist and contain `@AGENTS.md`? | Medium |
| Dual rules | Do `.cursor/rules/` and `.claude/rules/` exist with matching content? | Medium |
| ADR system | Are architectural decisions captured in `docs/decisions/`? | Low |
| Task entry | Does AGENTS.md Task Entry section point to the correct issue source (GitHub Issues or ISSUES.md)? | Medium |
| Redundancy | Is there content duplicated between AGENTS.md, README, and rules files? | Low |

### Dimension B: Functional Correctness & Architecture

Assess whether the scaffold serves the project's purpose.

| Check | Question | Severity |
|-------|----------|----------|
| Design fidelity | Does the directory structure match the design doc's architecture? | High |
| Module coverage | Are all functional modules from the design doc represented? | High |
| Dependency completeness | Are all required libraries in the dependency file? | High |
| Entry point wiring | Does the CLI skeleton parse expected arguments? | Medium |
| Configuration strategy | Is there a clear config loading path (env vars, yaml, defaults)? | Medium |
| Security posture | Are secrets excluded from git? Are API keys env-only? | High |
| Extensibility | Can new modules be added without modifying existing ones? | Low |
| Test foundation | Is the test directory structure ready (mirrors src)? | Low |

### Severity Definitions

- **High**: Must fix before handoff. Blocks agent collaboration or introduces security risk.
- **Medium**: Should fix. Improves quality but doesn't block.
- **Low**: Nice to have. Can be deferred to first dev-workflow cycle.

---

## Round 3: Review-the-Review

Verify that fixes from Rounds 1-2 didn't introduce new problems.

- [ ] All Round 1-2 fixes committed cleanly (no merge conflicts, no orphaned files)
- [ ] No new content duplication introduced between AGENTS.md / README / rules files
- [ ] Git status is clean (all changes staged and committed)
- [ ] No circular references between documentation files
- [ ] AGENTS.md status table still accurate after fixes
- [ ] README quick start still valid after any path changes
- [ ] No high or medium issues remain

If new high/medium issues are found, loop back to Round 2 for that specific issue only. Do not restart the full review.

---

## Issue Tracking Format

When reporting issues during review, use this format:

```
| # | Issue | Severity | File(s) | Fix |
|---|-------|----------|---------|-----|
| 1 | README references nonexistent dir | Medium | README.md | Update path |
| 2 | .env.example missing FRED_API_KEY | High | .env.example | Add key |
```

---

## When to Skip Reviews

- **Skip Round 2 Dimension B** if there is no design doc (ad-hoc project)
- **Skip Round 3** if Rounds 1-2 found zero issues
- **Skip all reviews** if the user explicitly says "skip review" — but warn about risks
