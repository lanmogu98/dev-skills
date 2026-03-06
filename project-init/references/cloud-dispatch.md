# Cloud Dispatch: GitHub Actions

Workflow templates for dispatching tasks to Claude Code and Codex via GitHub Actions. Generate these files in `.github/workflows/` during Phase 3 when the user requests cloud-triggered automation.

---

## Overview

| Aspect | Claude Code Action | Codex Action |
|---|---|---|
| Action | `anthropics/claude-code-action@v1` | `openai/codex-action@v1` |
| Context file | `CLAUDE.md` (auto-read) | Repo files (via prompt) |
| Auth secret | `ANTHROPIC_API_KEY` | `OPENAI_API_KEY` |
| Task input | `prompt` param or `@claude` mention | `prompt` or `prompt-file` param |
| Trigger modes | Interactive + automation | Automation only |
| Output | Comments on PR/issue | `final-message` output + `output-file` |
| Key config | `claude_args` passthrough | `sandbox`, `safety-strategy`, `model` |

---

## Claude Code Action Workflow

### `.github/workflows/claude.yml`

```yaml
name: Claude Code

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned]

jobs:
  claude:
    if: |
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

This minimal workflow responds to `@claude` mentions in issues and PR comments. Claude auto-reads `CLAUDE.md` (which imports `AGENTS.md`) for project context.

### Claude Code: Automation Mode

For scheduled or event-driven tasks (no human trigger):

```yaml
name: Claude Automation

on:
  schedule:
    - cron: "0 9 * * 1"  # Every Monday at 9am UTC
  workflow_dispatch:
    inputs:
      task:
        description: "Task for Claude to execute"
        required: true

jobs:
  automate:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: ${{ github.event.inputs.task || 'Read FUTURE_ROADMAP.md, pick the first Pending item, implement it, and create a PR.' }}
          claude_args: "--max-turns 20 --model claude-sonnet-4-6"
```

---

## Codex Action Workflow

### `.github/workflows/codex.yml`

```yaml
name: Codex Task

on:
  workflow_dispatch:
    inputs:
      task:
        description: "Task description or path to prompt file"
        required: true
      sandbox:
        description: "Sandbox level"
        required: false
        default: "workspace-write"

jobs:
  codex:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Run Codex
        id: run_codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt: ${{ github.event.inputs.task }}
          sandbox: ${{ github.event.inputs.sandbox }}
          safety-strategy: drop-sudo
          output-file: codex-output.md

      - name: Create PR with changes
        if: steps.run_codex.outputs.final-message != ''
        uses: peter-evans/create-pull-request@v7
        with:
          title: "feat: codex automated implementation"
          body: ${{ steps.run_codex.outputs.final-message }}
          branch: codex/auto-${{ github.run_id }}
```

### Codex: PR Review

```yaml
name: Codex PR Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    outputs:
      final_message: ${{ steps.run_codex.outputs.final-message }}
    steps:
      - uses: actions/checkout@v4
        with:
          ref: refs/pull/${{ github.event.pull_request.number }}/merge

      - name: Pre-fetch refs
        run: |
          git fetch --no-tags origin \
            ${{ github.event.pull_request.base.ref }} \
            +refs/pull/${{ github.event.pull_request.number }}/head

      - name: Run Codex Review
        id: run_codex
        uses: openai/codex-action@v1
        with:
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          prompt-file: .github/prompts/review.md
          sandbox: read-only
          safety-strategy: drop-sudo

  post_feedback:
    runs-on: ubuntu-latest
    needs: review
    if: needs.review.outputs.final_message != ''
    steps:
      - name: Post feedback
        uses: actions/github-script@v7
        with:
          github-token: ${{ github.token }}
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.pull_request.number,
              body: process.env.CODEX_MSG,
            });
        env:
          CODEX_MSG: ${{ needs.review.outputs.final_message }}
```

---

## Prompt Files

Store reusable task definitions in `.github/prompts/`. Both agents can reference these.

### `.github/prompts/review.md`

```markdown
Review this pull request for:
1. Correctness — does the logic match the intent?
2. Security — no secrets, input validation, safe error handling
3. Tests — are there tests for the changes?
4. Docs — CHANGELOG and README updated if needed?

Read AGENTS.md for project conventions. Follow the code style defined there.
Provide actionable feedback with specific file and line references.
```

### `.github/prompts/implement-next.md`

```markdown
Read FUTURE_ROADMAP.md and find the first item with status "Pending".
Read AGENTS.md for project conventions and architecture.
Read docs/DESIGN_REMAINING_ISSUES.md for the matching section if it exists.

Implement the item following these rules:
1. Create a feature branch: `feat/<item-id>-<short-name>`
2. Write tests first (see dev-workflow skill conventions)
3. Implement the minimal code to pass tests
4. Update AGENTS.md implementation status table
5. Update FUTURE_ROADMAP.md status to "In Progress"
6. Commit with conventional commit format

Do NOT modify unrelated files. Do NOT skip tests.
```

---

## Required GitHub Secrets

| Secret | Used By | How to Get |
|--------|---------|-----------|
| `ANTHROPIC_API_KEY` | Claude Code Action | [console.anthropic.com](https://console.anthropic.com/) |
| `OPENAI_API_KEY` | Codex Action | [platform.openai.com](https://platform.openai.com/) |

Add via: Repository Settings > Secrets and variables > Actions > New repository secret

---

## Security Notes

- Use `safety-strategy: drop-sudo` for Codex to prevent privilege escalation
- Set `--max-turns` for Claude Code to cap token usage
- Codex `sandbox: workspace-write` limits filesystem access to the repo checkout
- Never use `danger-full-access` sandbox in Codex unless absolutely required
- Both agents run on GitHub-hosted runners — code stays on GitHub infrastructure
- Review all agent-created PRs before merging; do not auto-merge

---

## Cost Awareness

Both actions consume API tokens and GitHub Actions minutes:

- Claude Code: token cost depends on model (Sonnet vs Opus) and conversation length
- Codex: token cost depends on model and effort level
- GitHub Actions: runner minutes (free tier has limits; see GitHub billing docs)

Recommendations:
- Use `--max-turns 10-20` for bounded tasks
- Use `sandbox: read-only` for review-only workflows
- Set workflow-level `timeout-minutes` to prevent runaway jobs
