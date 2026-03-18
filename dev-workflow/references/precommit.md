# Pre-Commit Checklist

> Complete these steps before committing — each catches a different class of mistake that's hard to fix after the fact.

## Step 1: VERIFY TESTS PASS

```bash
# Run project's test command
pytest tests/ -v        # Python
npm test                # Node.js
go test ./...           # Go
cargo test              # Rust
```

- ✅ All tests must pass (tests should already exist from implementation phase)
- ❌ If tests fail → fix before committing
- ❓ If no tests for your change → go back to implementation phase and add them

## Step 2: UPDATE CHANGELOG

**Per commit rule:**
- Behavior change (user-facing or operational) → Update `CHANGELOG.md` under `## [Unreleased]`
- Internal-only (comments/formatting/dead code) → Optional; note in PR if skipped

| Change Type | Section |
|-------------|---------|
| New feature | `### Added` |
| Bug fix | `### Fixed` |
| Breaking change | `### Changed` |
| Removed feature | `### Removed` |

## Step 3: SYNC DOCUMENTATION

| If you changed... | You MUST update... |
|-------------------|---------------------|
| Behavior (user-facing) | `CHANGELOG.md`, `README.md` |
| CLI / Configuration | `README.md` (usage), `DEVELOPER_GUIDE.md` (config) |
| Project Structure | `DEVELOPER_GUIDE.md` (architecture) |
| Dependencies | Dependency file + `README.md` (installation) |

## Step 4: UPDATE TASK STATUS (if applicable)

- If project uses GitHub Issues, close the issue via PR (`Closes #N`). If it uses `ISSUES.md`, set task status to **Done**
- Keep `ISSUES.md` short; remove completed items periodically

## Step 5: COMMIT

Format: `type(scope): summary`

Types: `feat` | `fix` | `docs` | `test` | `chore` | `refactor`

```bash
git commit -m "feat(scraper): add video content type detection"
git commit -m "fix(cli): handle empty input edge case"
git commit -m "docs: update README with new CLI flags"
```

---

**→ Phase complete.** Return to SKILL.md for the next step.
