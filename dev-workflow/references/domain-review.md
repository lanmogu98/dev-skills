# Domain Review Protocol

Human-in-the-loop protocol for projects where implementation decisions have real-world domain consequences. Ensures that domain-laden choices (thresholds, formulas, data models, priority assignments) are surfaced to the human for review rather than silently embedded.

## Activation

This protocol activates when the project's `AGENTS.md` contains a `## Domain Review Protocol` section. That section defines:

- The project's domain context (what kind of real-world decisions depend on the system)
- Communication style preferences (language, tone, level of technicality)
- Which domain dimensions require review
- Design doc references

If no `## Domain Review Protocol` section exists, skip this protocol entirely.

## Three Intervention Types

The protocol adds three intervention points to the standard dev-workflow phases:

```text
Exploration ──→ Design ──→ Implementation ──→ Pre-Commit ──→ PR
    │              │              │                │
    ▼              ▼              ▼                ▼
  Brief-In    Checkpoint(s)   Checkpoint(s)    Brief-Out
```

### 1. Brief-In (before implementation starts)

**Nature:** FYI — does not block unless the human raises concerns.

**When:** At the start of each action node or task, after exploration, before design/implementation.

**Purpose:** Tell the human what is about to be built, why it matters, and what decisions will come up.

**Template:**

```markdown
## Brief-In: [Action Node ID] — [Title]

### What are we building?
[1-3 sentences in plain language. Explain what this module does
and why it matters for the overall system. Avoid jargon.]

### How does this fit in?
[Which modules depend on this? What must exist before this?
Simple dependency list, not a diagram.]

### Decisions ahead
[Numbered list. For each upcoming decision:]
1. **[Decision name]** — [one sentence description]
   - Weight: [S or T] + [D3, D2, or D1] → [CHECKPOINT / Brief-Out mention / Skip]
   - Already decided? [Yes — design doc Section X / No — needs your input]

### Design doc reference
[Which section of the design doc governs this, and any gaps found.]

### Estimated scope
[Files to create/modify, approximate size.]
```

### 2. Checkpoint (at domain decision points)

**Nature:** BLOCKING — implementation pauses until the human responds.

**When:** During design or implementation, when a decision meets the checkpoint threshold (see Decision Weight Matrix below).

**Purpose:** Present a specific decision, explain its real-world consequences, offer options, get human confirmation.

**Template:**

```markdown
## Checkpoint: [Decision Title]

### The question
[One sentence: what needs to be decided.]

### Why this matters
[2-3 sentences explaining the DOMAIN consequence of this decision.
Not the technical consequence — the real-world impact on the human's goals.
Use concrete scenarios from the project's domain.
Adapt language to the style specified in the project's Domain Review Protocol.]

### Options

**Option A: [Name]** ([design doc default / recommended / etc.])
- How it works: [plain language]
- Upside: [...]
- Downside: [...]
- Reversibility: [Easy — config change / Hard — requires migration / etc.]

**Option B: [Name]**
- How it works: [...]
- Upside: [...]
- Downside: [...]
- Reversibility: [...]

[Add Option C if warranted. Keep to 2-3 options.]

### Recommendation
[Which option and why, based on design doc. Do not invent preferences
— ground recommendations in the project's design documents.]

### Default if no response
[Which option will be used if the human does not respond, and what
is the worst case if that default is wrong.]
```

### 3. Brief-Out (before commit)

**Nature:** Soft gate — present the summary, give the human a window to object. If no objection, proceed with commit.

**When:** After implementation, before pre-commit phase.

**Purpose:** Summarize what was built, what assumptions are embedded, what is easy vs hard to change later.

**Template:**

```markdown
## Brief-Out: [Action Node ID] — What Was Built

### Summary
[2-3 sentences in plain language: what was implemented.]

### Structural decisions (hard to change later)
[For each structural decision:]
- **[Decision]**: [What was chosen]
  - Domain implication: [What this means for the human's goals]
  - To change later: [What it would take — migration, rewrite, etc.]

### Tunable parameters (change in config anytime)
| Parameter | Current value | Config location | Controls |
|-----------|---------------|-----------------|----------|
| ... | ... | `file:line` | ... |

### Assumptions embedded
[Numbered list of assumptions that could produce wrong results if violated:]
1. **[Assumption]**: [What could go wrong]

### Not included in this commit
[Deliberately deferred items with reasoning.]

### Persistence
[Save this Brief-Out to the project's decision records per the
project's Domain Review Protocol instructions.]
```

## Decision Weight Matrix

Not every decision warrants a blocking checkpoint. Classify each decision along two dimensions:

### Dimension A — Reversibility

| Level | Name | Description | Examples |
|-------|------|-------------|----------|
| **S** | Structural | Requires migration, re-architecture, or data reprocessing to change | DB schema, API contracts, state machine states, data granularity |
| **T** | Tunable | Can be changed in configuration without code changes | Numeric thresholds, keyword lists, polling intervals, retry counts |

### Dimension B — Domain Depth

| Level | Name | Description | Examples |
|-------|------|-------------|----------|
| **D3** | Deep domain | Requires domain expertise to evaluate correctness | Formulas, detection logic, priority assignments, state transition rules |
| **D2** | Moderate domain | General domain familiarity is sufficient | Sanity ranges, dedup thresholds, scheduling |
| **D1** | Technical only | No domain knowledge needed | Log rotation, DB pragmas, retry backoff timing |

### Checkpoint trigger rules

| | D3 | D2 | D1 |
|---|---|---|---|
| **S** | CHECKPOINT | CHECKPOINT | Brief-Out mention |
| **T** | CHECKPOINT | Brief-Out mention | Skip |

### Skip rules

Even when a decision meets the checkpoint threshold, **skip the checkpoint** if:

1. The design doc explicitly specifies the value/choice AND the user confirmed it during project initialization (project-init Phase 0-1).
2. The decision is a direct, unambiguous implementation of a design doc specification with no room for interpretation.

Trigger a checkpoint when:

- The design doc is ambiguous or leaves the decision open
- The design doc lists it as an "open question"
- The agent needs to make a choice beyond what the design doc specifies
- The agent disagrees with or has concerns about the design doc's specification

## Non-Interactive Environments

When running in non-interactive contexts (Codex CI, GitHub Actions, automated pipelines):

- **Brief-In / Brief-Out**: Do not output (no interactive audience).
- **Checkpoints**: Cannot block. Instead:
  1. Use the design doc's default for all checkpoint-level decisions.
  2. In the PR description or commit message, add a section listing all domain decisions made, each marked with "Pending human confirmation."
  3. If a decision has no clear design doc default, flag it as a blocker in the PR and request human review before merge.

## Communication Style

The specific tone, language, and framing for domain explanations is defined per-project in the `## Domain Review Protocol` section of the project's `AGENTS.md`. The templates above use placeholder language ("domain consequence", "real-world impact") — replace these with the project's preferred framing.

Common customizations projects may specify:

- Natural language for explanations (e.g., Chinese for domain, English for code identifiers)
- Level of technicality (e.g., accessible/educational vs expert-level)
- Concrete scenario style (e.g., reference user's actual holdings, use cases, or operational context)
- Whether to explain investment consequences, clinical outcomes, regulatory impact, etc.
