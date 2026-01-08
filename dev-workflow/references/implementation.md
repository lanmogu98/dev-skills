# Implementation Phase

## Code Standards

- Type hints on all function parameters and return values
- Small, testable functions
- Keep failure modes explicit; avoid silent `except:` catches
- No secrets in code or logs — use env vars; prefer `.env` locally (not committed)

## Testing: Write First, Run Often

**Default: write tests before code.**

1. **Write/update tests** — Define expected behavior before implementation
2. **Implement code** — Make tests pass
3. **Run tests locally** — Verify before moving to precommit

### Exceptions (tests after is acceptable)

- Doc-only changes (no behavior change)
- Exploratory debugging to identify root cause
- Trivial config/typo fixes with no logic change
- Emergency hotfixes (add tests in immediate follow-up)

### Required Tests by Change Type

| Change Type | Required Tests |
|-------------|----------------|
| Logic change (functions, algorithms) | Unit tests: happy path + edge cases |
| API/IO change (endpoints, file ops) | Integration tests with mocked externals |
| CLI change | Smoke test for new flags/commands |
| Refactor (no behavior change) | Existing tests must pass; no new tests required |

### Handling Missing/Flaky Tests

- No tests exist → Add smallest covering test first
- Tests are flaky → Fix or skip with justification before proceeding
- Slow tests (>5s) → Mark and run separately; don't block fast feedback

## When Blocked

- Environment issues (network/SSL/quotas) → Surface issue, skip gracefully
- Be explicit about paid API usage; default to cheapest safe model

## LLM/Agent Usage

- Use cheapest safe model for tests/smoke; escalate only when accuracy requires
- API keys from env vars only; never embed or log plaintext
- Ask user which env var to use for LLM key
- Redact PII/secrets from prompts and logs

## CI & Lint

- Run linter/formatter during implementation; fix errors as you go
- Use project-defined tools (don't mix formatters)

## Dependency Management

- Pin versions in dependency files
- Update dependencies intentionally, not drive-by
- Prioritize security updates

---

**→ Next:** When implementation is complete, load `references/precommit.md` to prepare commit.
