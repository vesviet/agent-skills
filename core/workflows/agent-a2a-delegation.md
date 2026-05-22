---
description: Full A2A 1.0 delegation with Agent Card discovery, streaming progress, artifact validation, and Antigravity-compatible handoffs
---

## Agent A2A Delegation Workflow

Use this workflow when work must cross role boundaries with structured A2A tasks, streaming updates, and schema-validated artifacts (Antigravity or pack-local file handoff).

### Prerequisites

- agent-skills pack v2.3+ installed
- A2A registry generated: `python3 core/scripts/generate-a2a-registry.py`
- delegating role assigned (typically Agent Coordinator or Technical Lead)
- output schema identified for the worker deliverable

### Workflow Steps

#### 1. Discover Worker Agent Cards

Role: **Agent Coordinator**

Load `core/a2a/.well-known/agent-registry.json` and the assignee `core/a2a/registry/<role>.agent-card.json`.

Confirm:

- worker skills cover the requested capability
- defaultOutputSchemas include the expected handoff file
- streaming capability when work may exceed a few minutes

Use skill: `agent-a2a-protocol`

#### 2. Publish Coordination Plan (Multi-Phase Work)

Role: **Agent Coordinator**

When the effort has multiple phases or parallel tracks, publish `coordination-plan.json` with owners, dependencies, and exit criteria.

Use skill: `agent-graph-orchestration`

#### 3. Compose And Submit A2A Task

Role: **Agent Coordinator** (or delegating role)

Create `a2a-task.json` with:

- UUID v4 task_id (required for Antigravity AgentKit)
- state submitted
- assignee_role and optional assignee_agent_card from registry
- self-contained input_data and success_criteria
- output_schema_ref pointing to an existing pack schema
- interaction_mode sync, stream, or push

Use skills: `agent-a2a-protocol`, `agent-delegation`

#### 4. Execute Worker Phase

Role: **Backend Developer**, **Frontend Developer**, **QA Engineer**, or other specialist named in assignee_role

Transition to working state. For stream mode, emit `a2a-task-progress.json` events (task.status, task.artifact).

Produce `a2a-artifact.json` conforming to the task output schema.

#### 5. Validate Artifact And Update Status

Role: **Agent Coordinator**

Build `a2a-task-status.json` from the latest task state.

Validate artifact against output_schema_ref. If validation fails, retry, reassign, or mark failed with blockers.

Use skills: `agent-a2a-protocol`, `agent-quality-gate`

#### 6. Merge Parallel Branches

Role: **Agent Coordinator**

When coordination-plan parallel groups complete, merge artifacts before opening dependent phases.

Use skill: `agent-graph-orchestration`

#### 7. Close Delivery Handoff

Role: **Agent Coordinator**

Emit domain contracts (for example implementation-result.json, test-report.json) plus residual risks.

Do not commit or push unless the user explicitly requests a commit-capable role.

Use skill: `agent-handoff`

### Checklist

- [ ] registry and assignee Agent Card loaded
- [ ] coordination-plan published when multi-phase
- [ ] a2a-task.json submitted with UUID and output_schema_ref
- [ ] worker emitted progress events when streaming
- [ ] a2a-artifact.json validated
- [ ] a2a-task-status.json reflects terminal state
- [ ] parallel branches merged before downstream phases
- [ ] final domain handoff and risks documented

### Related Workflows

- [add-new-feature](add-new-feature.md)
- [troubleshooting](troubleshooting.md)
- [service-review-release](service-review-release.md)

### Related Skills

- **agent-a2a-protocol**: Full task lifecycle and Antigravity wire formats
- **agent-delegation**: Single-hop scoped delegation
- **agent-graph-orchestration**: Phase graphs and parallel merge gates
- **agent-quality-gate**: Validate artifacts and repo checks
- **agent-handoff**: Summarize closure and residual risk

### Antigravity Notes

Copy `adapters/antigravity/rules.template.md` to `.antigravity/rules.md`. See `adapters/antigravity/ANTIGRAVITY.md`.
