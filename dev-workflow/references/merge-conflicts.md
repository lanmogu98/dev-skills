# Resolving Merge Conflicts

> Load when a `git rebase` onto main, a merge, or a parallel worktree landing reports conflicts.

A conflict is two intents colliding on the same lines — not a syntax puzzle to silence. Git can show *where* two edits overlap but not *what* either was trying to do. Resolving for a clean compile is easy; resolving for correct meaning is the actual work.

## Where Conflicts Surface Here

| Situation | Why it conflicts |
|-----------|------------------|
| Rebase before PR | Main moved on since you branched (see `pullrequest.md`) |
| Parallel worktrees landing | Two agents touched overlapping files (see `multi-agent.md`) |
| Long-lived branch | The longer a branch runs, the further main drifts from it |

This repo rebases to keep history linear (`multi-agent.md`, `pullrequest.md`), so conflicts surface at *your* rebase, one commit at a time — resolve each, then `git rebase --continue`.

## Resolve for Meaning

1. **Read both sides first.** For each `<<<<<<<` block, work out what *ours* was accomplishing and what *theirs* was accomplishing before you touch a character. You can't merge two intents you haven't understood.
2. **Satisfy both — don't pick a winner.** Blindly taking `--ours` or `--theirs` silently discards one side's intent. The resolved code should honor *both* changes' purpose, which usually means weaving them together rather than choosing.
3. **If the two intents genuinely can't coexist,** that's a design question, not a merge mechanic — surface it instead of papering over it with a guess.

## After Resolving

- **Re-run the full test suite.** A conflict that merges cleanly and compiles can still be semantically broken: each side's tests passed in isolation, but the *combined* behavior is new and unexercised.
- **Never commit conflict markers.** Search for `<<<<<<<`, `=======`, `>>>>>>>` before staging — a committed marker breaks the file for everyone downstream.

## Escalation Signal

If the *same file* conflicts on rebase after rebase, the branch has drifted too far. Rebase more often (`exploration.md`: "rebase regularly onto main to avoid conflicts") or split the work into smaller PRs that land before they diverge.

---

**→ Resolved.** Return to SKILL.md and finish the PR / merge step.
