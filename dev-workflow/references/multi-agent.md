# Multi-Agent Collaboration

> Load when multiple agents work on the same codebase in parallel.

## Worktree Isolation

Each agent should work in an isolated worktree to avoid file conflicts.

```bash
# Create worktree for a task
git worktree add ../project-<agent-role> <branch-name>

# Examples
git worktree add ../project-impl feature/auth
git worktree add ../project-planning planning/sprint-3
```

### Naming Convention

| Pattern | Example |
|---------|---------|
| By role | `../project-impl`, `../project-review` |
| By task | `../project-feat-auth`, `../project-fix-123` |
| By agent ID | `../project-agent-1`, `../project-agent-2` |

### Lifecycle

```bash
# List all worktrees
git worktree list

# Remove when done (after merge)
git worktree remove ../project-impl
```

## Branch Strategy for Agents

```
main (protected)
  │
  ├── agent/planning     ← 任务规划
  ├── agent/impl-1       ← 编码实现 #1
  ├── agent/impl-2       ← 编码实现 #2 (parallel task)
  └── agent/review       ← 审核 (may not need worktree)
```

### Rules

- **Never push directly to main** — Always PR
- **One branch per task** — Don't mix concerns
- **Rebase before PR** — Keep history clean

## Agent Role Boundaries

| Role | Responsibilities | Worktree Needed? |
|------|------------------|------------------|
| Planning | Read code, define scope, update roadmap | Optional |
| Implementation | Write code, tests, docs | Yes |
| Review | Check PR, request changes | No (read-only) |

### Avoiding Overlap

- Planning agent sets task scope in `FUTURE_ROADMAP.md` **before** impl starts
- Impl agents work on **disjoint files** when possible
- Review agent waits for impl to **create PR** before reviewing

## Merge Flow

```
1. Impl agent completes task in worktree
2. Impl agent: git push origin agent/impl-1
3. Impl agent: create PR → main
4. Review agent: review PR
5. After approval: squash merge to main
6. Cleanup: git worktree remove ../project-impl-1
```

## Mode Selection (Cursor/IDE)

| Mode | Use When |
|------|----------|
| **Local** | Single agent, simple task, fast iteration |
| **Worktree** | Multi-agent, complex task, need isolation |
| **Cloud** | Need clean environment, long-running tasks |
