---
name: agent-context-management
description: Manage working context across long or multi-step agent tasks by tracking user intent, repo rules, explored evidence, assumptions, and remaining work. Use when a task spans many files, resumes after interruption, or risks losing important context.
---

# Agent Context Management

Use this skill when the work requires preserving the user's latest request, repository constraints, evidence gathered so far, and the next safe action.

## Core Rules

- let the newest user request steer the current work
- keep repo rules, role boundaries, and active quality gates visible
- distinguish confirmed facts from assumptions and open questions
- avoid restarting from scratch after interruption when enough context remains
- summarize only the context needed to continue safely

## Suggested Process

### 1. Restate The Active Goal Internally

Identify the current user request, any newer correction, and the expected output.

### 2. Gather Required Constraints

Check the applicable source of truth:

- repo rules
- active role or workflow
- relevant skill instructions
- open validation requirements

### 3. Track Evidence

Keep a compact record of:

- files inspected
- decisions already made
- commands or validators run
- failures and fixes attempted
- unresolved assumptions

### 4. Preserve Continuity

After a long run, interruption, or context transition:

- continue from the last confirmed state
- re-check only the facts needed for the next action
- avoid duplicating completed exploration
- verify the final answer matches the newest request

### 5. Report Clearly

When reporting progress or completion, include only high-signal context: what changed, what passed, what remains risky, and whether anything was skipped.

## Checklist

- [ ] latest user request identified
- [ ] applicable rules and constraints noted
- [ ] explored evidence tracked
- [ ] assumptions and open questions separated from facts
- [ ] next action follows the current state
- [ ] final response answers the newest request

## Related Skills

- **agent-tool-orchestration**: Choose and sequence tools without losing context
- **agent-quality-gate**: Run the right validators before completion
- **agent-handoff**: Produce a concise continuation or completion summary
- **navigate-service**: Gather codebase context for service work
- **meeting-review**: Structure multi-perspective decisions
