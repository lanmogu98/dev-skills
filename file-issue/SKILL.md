---
name: file-issue
description: |
  File a GitHub issue or local issue from the current conversation. Use when bugs, regressions, improvements, or design tasks are identified during a session and need to be captured as tracked work. Trigger when the user says "file an issue", "create an issue", "track this", "open a bug", "make a ticket", "note this down", "log this", or when a notable problem is discovered that should be recorded. Also use when you discover a code quality issue, notice a missing feature during code review, want to capture technical debt, or when the user says "we should track this", "that's a bug", or similar. Works with both GitHub-hosted projects (via gh CLI) and non-GitHub projects (appending to ISSUES.md).
---

# File Issue

Capture bugs, improvements, or design tasks as tracked issues — either on GitHub or in a local `ISSUES.md`.

## Detect Issue Destination

Before drafting, figure out where the project tracks issues. This matters because GitHub-hosted projects get labels, assignees, and PR auto-close for free, while non-GitHub projects need a local equivalent.

1. Check if project is GitHub-hosted: `git remote -v | grep github.com`
2. Check AGENTS.md `## Task Entry` section for the canonical tracking method
3. **GitHub-hosted** → file via `gh issue create`
4. **Non-GitHub** → append to `ISSUES.md` at project root

## Issue Templates

Read `references/templates.md` for the full template structures. Choose the template that best fits what was identified:

| Template | When to use | Labels |
|---|---|---|
| **task** | An improvement, refactor, or feature request | `agent-generated` + priority |
| **bug-report** | A bug or regression was found | `bug`, `agent-generated` |
| **design-note** | Complex work needing detailed implementation context | `agent-generated` + priority |

## Workflow

### 1. Gather Context from Conversation

Extract:

- **What is broken or missing** — concrete symptoms, error messages, failing test output
- **Where it happens** — file paths, line numbers, module names
- **How to reproduce** (for bugs) — steps, commands, or minimal config
- **Root cause** (if known) — what investigation revealed
- **Severity** — blocks work, causes data loss, or cosmetic?

If the conversation is ambiguous about what to file, ask the user to clarify before proceeding.

### 2. Classify the Issue

Pick the template (task, bug-report, or design-note) that best fits. If unsure, ask the user — getting the template right keeps issues scannable.

### 3. Duplicate Check

Before creating anything, check for existing issues on the same topic. Filing duplicates wastes everyone's time and fragments discussion.

**GitHub-hosted:**

```bash
gh issue list --state open --search "<keyword>"
```

**Non-GitHub:** scan `ISSUES.md` for similar items.

If a matching issue exists, tell the user and offer to comment on it (GitHub) or update it (local) instead.

### 4. Draft the Issue

**Title**: Short imperative sentence, optionally prefixed with a scope tag (e.g., `[auth] Fix session expiry`). Under 80 characters.

**Body**: Use the section structure from the matching template in `references/templates.md`.

Keep the body concise — reference code with `file:line` links rather than pasting inline, include error messages in trimmed code blocks, and aim for under ~200 words. The issue should read as if the human wrote it, not the agent.

### 5. Confirm or File Directly

When the user explicitly asked to file an issue, go ahead and file it — they can review and edit on GitHub. When the agent surfaced the issue on its own (not explicitly requested), show the drafted title and body first and wait for approval. This avoids surprising the user with unexpected issues in their tracker.

### 6. File the Issue

**GitHub-hosted:**

```bash
gh issue create \
  --title "<title>" \
  --label "agent-generated" \
  --body "$(cat <<'EOF'
<body>
EOF
)"
```

Add template-appropriate labels (`bug` for bug reports, priority `p1`/`p2`/`p3` if known). If a label doesn't exist, skip it rather than creating new labels — label management is a human decision.

**Non-GitHub:** Append a new row to the `## Active` table in `ISSUES.md`:

- Generate next ID (increment from highest existing, e.g., `T-003`)
- Set priority based on severity context
- Status: `Pending`

If the issue needs detailed notes (design-note type), also add a section to `docs/ISSUE_DETAILS.md`.

### 7. Report Back

Print the issue URL (GitHub) or the ID and location (local) so the user can see it.

## Writing Style

Issues are most useful when they're scannable. Every sentence should convey information the reader doesn't already have. Reference code with annotated links (`file.py:42` — description), not narrative explanations. No preamble ("I noticed...", "During our conversation...").
