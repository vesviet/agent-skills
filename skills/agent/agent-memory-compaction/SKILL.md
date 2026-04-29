---
name: agent-memory-compaction
description: Compact long-running agent conversation context into a minimal working state by preserving goals, constraints, decisions, changed files, validation, blockers, and next actions while dropping stale detail. Use when a chat grows long, context becomes noisy, or work needs a clean resume checkpoint.
---

# Agent Memory Compaction

Use this skill when accumulated conversation context is larger than the task needs and the work should continue from a smaller, accurate state.

## Core Rules

- preserve the newest user request and any explicit corrections
- keep only information needed to continue safely
- separate durable facts from temporary exploration detail
- retain validation status, blockers, and next actions
- drop obsolete plans, failed guesses, duplicate command output, and stale intermediate reasoning

## Suggested Process

### 1. Identify The Active Thread

Determine the current goal, latest user instruction, and whether any earlier request has been superseded.

### 2. Classify Context

Sort accumulated context into:

- must keep: active goal, constraints, files changed, decisions, validation state, blockers
- useful later: relevant discovered patterns, commands that proved something, unresolved risks
- safe to drop: duplicate logs, old plans, superseded assumptions, broad exploration notes

### 3. Build A Compact Working State

Write a short checkpoint with:

- current objective
- repo rules or role/workflow constraints that still matter
- files changed or important files inspected
- decisions made and why they still apply
- validation already run and current results
- remaining work and next command or edit

### 4. Verify Continuity

Before discarding detail, confirm the compact state can answer:

- what are we doing now?
- what must not be changed?
- what has already been completed?
- what check proves the current state?
- what is the next safe step?

### 5. Resume From The Checkpoint

Continue using the compact state as the source of truth. Re-read only the specific files or command output needed for the next action.

## Output Format

Use this format for a compaction checkpoint:

```markdown
## Compact Working State

Current goal:
- ...

Keep:
- ...

Changed or inspected:
- ...

Decisions:
- ...

Validation:
- ...

Remaining work:
- ...

Next action:
- ...
```

## Checklist

- [ ] latest user request preserved
- [ ] active constraints retained
- [ ] completed work and changed files summarized
- [ ] validation state captured
- [ ] blockers and residual risks retained
- [ ] stale plans, duplicate logs, and superseded assumptions dropped
- [ ] next action is clear from the compact state

## Related Skills

- **agent-context-management**: Track the working context before compaction
- **agent-handoff**: Turn compact state into a user-facing or resume summary
- **agent-quality-gate**: Preserve validation evidence before dropping detail
- **agent-tool-orchestration**: Re-read only the next necessary evidence after compaction
- **write-documentation**: Convert durable context into repository documentation
