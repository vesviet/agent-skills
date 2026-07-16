---
name: agent-memory-compaction
description: Compact long-running agent conversation context into a minimal working state by preserving goals, constraints, current phase, active owner, decisions, changed files, validation, blockers, and next actions while dropping stale detail. Use when a chat grows long, context becomes noisy, or work needs a clean resume checkpoint during bug or feature control work.
---

# Agent Memory Compaction

Use this skill when accumulated conversation context is larger than the task needs and the work should continue from a smaller, accurate state.

## When to Use

- a chat grows long and context gets noisy
- work needs a clean resume checkpoint
- dropping stale detail while keeping goals/constraints
- bug/feature control across many turns

## Core Rules

- preserve the newest user request and any explicit corrections
- keep only information needed to continue safely
- preserve the current phase, active owner, and phase-exit conditions
- separate durable facts from temporary exploration detail
- retain validation status, blockers, and next actions
- drop obsolete plans, failed guesses, duplicate command output, and stale intermediate reasoning

## Suggested Process

### 1. Identify The Active Thread

Determine the current goal, latest user instruction, and whether any earlier request has been superseded.

### 2. Classify Context

Sort accumulated context into:

- must keep: active goal, work type, current phase, active owner, constraints, files changed, decisions, validation state, blockers
- useful later: relevant discovered patterns, commands that proved something, unresolved risks
- safe to drop: duplicate logs, old plans, superseded assumptions, broad exploration notes

### 3. Build A Compact Working State

Write a short checkpoint with:

- current objective
- work type
- current phase, active owner, and exit criteria
- repo rules or role/workflow constraints that still matter
- files changed or important files inspected
- decisions made and why they still apply
- validation already run and current results
- preserved behavior or bug-success criteria
- remaining work and next command or edit

### 4. Verify Continuity

Before discarding detail, confirm the compact state can answer:

- what are we doing now?
- what must not be changed?
- what has already been completed?
- which phase are we in and what allows phase exit?
- what check proves the current state?
- what is the next safe step?

### 5. Resume From The Checkpoint

Continue using the compact state as the source of truth. Re-read only the specific files or command output needed for the next action.

### 2026: Production Patterns and Compaction Heuristics

- **mem0 and Zep v2 Production Patterns**: Use mem0 for simple user preference memory. Choose Zep v2 with a temporal knowledge graph when the validity of facts over time is required. Both platforms support automatic extraction and retrieval of long-term state.
- **Compaction Trigger Heuristics**: Initiate context compaction when context window utilization exceeds 60% of the model limit, which is safer than waiting for 80% when degradation may have already occurred. Alternatively, trigger compaction on a fixed turn count, such as every 20 turns. Always log pre-compaction and post-compaction token counts to monitor efficiency.

## Output Format

Use this format for a compaction checkpoint:

```markdown
## Compact Working State

Current goal:
- ...

Work type:
- ...

Phase control:
- Current phase:
- Active owner:
- Exit criteria:

Keep:
- ...

Changed or inspected:
- ...

Decisions:
- ...

Validation:
- ...

Preserved behavior:
- ...

Remaining work:
- ...

Next action:
- ...
```

## Checklist

- [ ] latest user request preserved
- [ ] work type and current phase preserved
- [ ] active constraints retained
- [ ] completed work and changed files summarized
- [ ] validation state captured
- [ ] preserved behavior or bug-success criteria captured
- [ ] blockers and residual risks retained
- [ ] stale plans, duplicate logs, and superseded assumptions dropped
- [ ] next action is clear from the compact state

## Related Skills

- **agent-context-management**: Track the working context before compaction
- **agent-handoff**: Turn compact state into a user-facing or resume summary
- **agent-quality-gate**: Preserve validation evidence before dropping detail
- **agent-tool-orchestration**: Re-read only the next necessary evidence after compaction
- **write-documentation**: Convert durable context into repository documentation
\n### 2026: Memory Strategies

- **mem0/Zep v2 production patterns:** mem0 provides an opinionated memory layer with automatic extraction, storage, and retrieval. Zep v2 adds temporal knowledge graph support. Choose mem0 for simple user preference memory, and Zep v2 when temporal fact validity matters (facts change over time).
- **Compaction trigger heuristics:** Trigger compaction when context window utilization exceeds 60 percent of the model's limit, not at 80 percent or higher (which is too late). Alternatively, trigger on a fixed turn count (e.g., every 20 turns). Log compaction events with pre/post token counts to measure effectiveness.\n