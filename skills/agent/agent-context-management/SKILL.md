---
name: agent-context-management
description: Manage working context across long or multi-step agent tasks by tracking user intent, current phase, active owner, repo rules, explored evidence, assumptions, and remaining work. Use when a task spans many files, resumes after interruption, or needs reliable bug or feature control across phases.
---

# Agent Context Management

Use this skill when the work requires preserving the user's latest request, repository constraints, current phase state, evidence gathered so far, and the next safe action.

## Core Rules

- let the newest user request steer the current work
- keep repo rules, role boundaries, and active quality gates visible
- keep the current phase, active owner, and phase exit criteria visible
- distinguish confirmed facts from assumptions and open questions
- avoid restarting from scratch after interruption when enough context remains
- summarize only the context needed to continue safely

## Suggested Process

### 1. Restate The Active Goal Internally

Identify:

- the current user request
- any newer correction
- the expected output
- whether the work is a bug, feature, review, or documentation task
- what behavior must stay stable

### 2. Gather Required Constraints

Check the applicable source of truth:

- repo rules
- active role or workflow
- relevant skill instructions
- open validation requirements
- current phase exit criteria if already established

### 3. Track Evidence

Keep a compact record of:

- current phase and active owner
- phase entry condition and exit condition
- files inspected
- decisions already made
- commands or validators run
- failures and fixes attempted
- reproduction status or feature acceptance criteria when relevant
- likely impact radius and dependent areas
- unresolved assumptions

### 4. Preserve Continuity

After a long run, interruption, or context transition:

- continue from the last confirmed state
- re-check only the facts needed for the next action
- avoid duplicating completed exploration
- reopen the prior phase if new evidence invalidates an earlier conclusion
- verify the final answer matches the newest request

### 5. Report Clearly

When reporting progress or completion, include only high-signal context:

- current phase and active owner
- what changed
- what passed
- what remains risky
- what was skipped
- what must happen before the next phase begins

## Output Format

Use this format when a task needs an internal or user-visible state checkpoint:

```markdown
## Working State

Work type:
- ...

Current goal:
- ...

Phase control:
- Current phase:
- Active owner:
- Exit criteria:

Preserved behavior:
- ...

Evidence:
- ...

Impact radius:
- ...

Open questions or blockers:
- ...

Next safe action:
- ...
```

## Checklist

- [ ] latest user request identified
- [ ] work type and preserved behavior identified
- [ ] applicable rules and constraints noted
- [ ] current phase and active owner tracked
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
