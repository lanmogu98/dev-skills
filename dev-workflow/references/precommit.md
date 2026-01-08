# Pre-Commit Checklist

> **Complete ALL steps IN ORDER before every `git commit`. No exceptions.**

## Step 1: VERIFY TESTS PASS

```bash
pytest tests/ -v  # or project's test command
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
| Dependencies | `pyproject.toml` + `README.md` (installation) |

## Step 4: UPDATE TASK STATUS

- Set task status in `FUTURE_ROADMAP.md` to **Done (recent)**
- Keep `FUTURE_ROADMAP.md` short (≤1-2 screens)
- Move "Done (recent)" items to `docs/roadmap/ROADMAP_ARCHIVE.md` during periodic cleanup

## Step 5: COMMIT

Format: `type(scope): summary`

Types: `feat` | `fix` | `docs` | `test` | `chore` | `refactor`

```bash
git commit -m "feat(scraper): add video content type detection"
git commit -m "fix(cli): handle empty DataFrame edge case"
git commit -m "docs: update README with new CLI flags"
```

---

**→ Next:** Load `references/pullrequest.md` to create PR.
