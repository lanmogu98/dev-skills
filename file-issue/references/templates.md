# Issue Templates

Section structures for the three issue types. Use the matching template when drafting an issue body — it keeps issues scannable and gives agents enough context to act on them without follow-up questions.

---

## Task

For improvements, refactors, or feature requests.

```markdown
## Description

(What needs to be done and why — enough context for anyone on the team or an AI agent.)

### Definition of Done

(Specific, testable completion criteria.)
```

---

## Bug Report

For bugs and regressions. Numbered repro steps help others (and agents) reproduce the issue quickly.

```markdown
**Describe the bug**
(What is broken — concrete symptoms, error messages.)

**To Reproduce**
1. (step)
2. (step)

**Expected behavior**
(What should happen instead.)

**Additional context**
(Root cause analysis if known, file:line references.)
```

---

## Design Note

For complex work that needs a detailed assignment packet — the kind of issue an agent could pick up and implement without additional verbal handoff.

```markdown
## Objective

(What this work changes and why — one paragraph.)

## Background / Evidence

- (Evidence 1)
- (Evidence 2)

## Scope

**In scope:**
- (File or area 1)

**Out of scope:**
- (Explicitly excluded concern)

## Approach

(Implementation strategy.)

## Definition of Done

- [ ] (Completion criterion 1)
- [ ] (Completion criterion 2)
```
