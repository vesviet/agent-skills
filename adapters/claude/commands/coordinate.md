---
description: "Coordinate a multi-agent or multi-phase task using the agent-coordinator role and A2A 1.0 protocols."
---

# Agent Coordination Command

Use this command when a request spans multiple roles or requires phased execution:

1. Assume the role of `agent-coordinator` (`core/roles/agent-coordinator.md`).
2. Read the user requirements: $ARGUMENTS.
3. Query `core/a2a/.well-known/agent-registry.json` to identify the required specialized agents.
4. Generate an execution DAG conforming to `core/contracts/schemas/coordination-plan.json`.
5. For each phase:
   - Formulate `a2a-task.json` targeting the assignee agent card.
   - Execute the assigned task and collect `a2a-artifact.json`.
   - Validate artifact schema compliance before advancing to the subsequent phase.
6. Present a consolidated summary to the user upon pipeline completion.
