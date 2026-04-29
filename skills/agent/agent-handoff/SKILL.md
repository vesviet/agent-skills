---
name: agent-handoff
description: Produce concise agent handoffs, status updates, and completion summaries that preserve decisions, changed files, validation evidence, blockers, and next actions. Use when pausing, resuming, handing work to another session, or reporting completed engineering work.
---

# Agent Handoff

Use this skill when another person or future session needs to understand the current state without rereading the entire conversation.

## Core Rules

- lead with the current outcome or blocker
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

### 2. Capture Current State

Summarize:

- user goal
- files or areas changed
- important decisions
- validation run
- known failures or skipped checks

### 3. Make Next Actions Explicit

If work remains, state the next concrete step, owner when known, and any prerequisite decision.

### 4. Keep User-Facing Text Clean

When the handoff may be reused in docs, commits, release notes, or changelogs, remove internal workflow wording and sensitive information.

### 5. Verify Against The Latest Request

Before sending the handoff, confirm it answers the newest user request and does not describe stale work as current.

## Checklist

- [ ] handoff type identified
- [ ] current goal and outcome summarized
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
