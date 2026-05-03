---
name: agent-handoff
description: Produce concise agent handoffs, status updates, and completion summaries that preserve phase state, decisions, changed files, validation evidence, blockers, and next actions. Use when pausing, resuming, handing work to another session, or reporting completed engineering work across bug or feature control flows.
---

# Agent Handoff

Use this skill when another person or future session needs to understand the current state without rereading the entire conversation, especially when work is moving across phases or owners.

## Core Rules

- lead with the current outcome or blocker
- include the current phase and whether it may advance
- include validation evidence, not just confidence
- separate completed work from remaining work
- keep the summary concise enough to act on
- avoid internal process labels in user-facing artifacts such as commits, changelogs, and release notes

## Suggested Process

### 1. Identify The Handoff Type

Decide whether the output is:

- progress update
- completion summary
- blocker report
- resume context
- review or validation summary
- phase-transition handoff

### 2. Capture Current State

Summarize:

- work type
- current phase and active owner
- user goal
- preserved behavior or success criteria
- files or areas changed
- important decisions
- validation run
- known failures or skipped checks
- impact radius or dependent areas when relevant

### 3. Make Next Actions Explicit

If work remains, state the next concrete step, owner when known, and any prerequisite decision.

### 4. Keep User-Facing Text Clean

When the handoff may be reused in docs, commits, release notes, or changelogs, remove internal workflow wording and sensitive information.

### 5. Verify Against The Latest Request

Before sending the handoff, confirm it answers the newest user request and does not describe stale work as current.

## Output Format

```markdown
## Handoff

Work type:
- ...

Current phase:
- ...

Active owner:
- ...

Goal or issue:
- ...

Preserved behavior or success criteria:
- ...

Changed areas:
- ...

Validation evidence:
- ...

Skipped checks and residual risk:
- ...

Next action:
- ...
```

## Checklist

- [ ] handoff type identified
- [ ] current goal and outcome summarized
- [ ] current phase and owner included
- [ ] changed areas or files listed when useful
- [ ] validation evidence included
- [ ] blockers, skipped checks, and residual risk called out
- [ ] next action clear when work remains

## Related Skills

- **agent-context-management**: Preserve working state before handoff
- **agent-quality-gate**: Provide validation evidence for the summary
- **agent-tool-orchestration**: Explain relevant tool or command outcomes
- **write-documentation**: Turn handoff context into durable docs
- **commit-code**: Prepare approved changes after completion
