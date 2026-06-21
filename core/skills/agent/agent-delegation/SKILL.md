---
name: agent-delegation
description: Delegate scoped sub-tasks from a supervisor agent to specialist worker agents using structured A2A task contracts, validate returned artifacts against output schemas, and handle delegation failures. Use when a task exceeds one agent's role boundary, requires parallel specialist work, or benefits from isolated context to reduce hallucination risk.
---

# Agent Delegation

Use this skill when a task should be broken into scoped sub-tasks and assigned to specialist agents rather than handled monolithically in a single context.

## Core Rules

- every delegation must include a self-contained task description, input data, output schema reference, and success criteria
- the delegator must not assume the worker has any context beyond what is explicitly provided in the A2A task
- validate the returned artifact against the output schema before accepting it
- failed delegations trigger retry with clarified input, escalation, or explicit failure — never silent acceptance
- track token usage and model used for every delegation for cost observability
- respect the risk tier: vibe tasks need minimal oversight, engineering tasks need full validation
- prevent Confused Deputy vulnerabilities (OWASP ASI03) by ensuring delegators never delegate or grant permissions beyond their own authorization scope, and validate scope constraints at handoff
- issue only task-scoped, time-bound credentials for each delegation leg instead of using persistent shared tokens
- mitigate transitive trust exploitation in multi-hop delegations by cryptographically verifying the authorization chain (A→B→C) at every hop
- enforce Zero-Trust inter-agent communication by requiring every single request to be independently authenticated and authorized
- prevent Confused Deputy vulnerabilities (OWASP ASI03) by ensuring delegators never delegate or grant permissions beyond their own authorization scope, and validate scope constraints at handoff
- issue only task-scoped, time-bound credentials for each delegation leg instead of using persistent shared tokens
- mitigate transitive trust exploitation in multi-hop delegations by cryptographically verifying the authorization chain (A→B→C) at every hop
- enforce Zero-Trust inter-agent communication by requiring every single request to be independently authenticated and authorized

## Key Concepts

### A2A Protocol

Agent-to-Agent (A2A) is the 2026 industry standard for inter-agent communication. The core building blocks are:

- **Agent Cards**: agents advertise their capabilities (role, skills, supported output schemas)
- **Tasks**: structured delegation objects with clear input/output contracts
- **Artifacts**: structured results returned by the worker
- **Streaming**: real-time progress updates via SSE (`a2a-task-progress.json`) for long-running tasks
- **Full lifecycle**: use `agent-a2a-protocol` for get/list/cancel and Antigravity wire formats

### Supervisor-Worker Pattern

The delegating agent acts as a **Supervisor**: it plans the work, breaks it into sub-tasks, delegates each to the best-fit Worker, and assembles the results. The Supervisor never implements — it orchestrates.

## Suggested Process

### 1. Decide Whether To Delegate

Delegate when:

- the sub-task requires a different role's expertise
- the sub-task would benefit from an isolated, focused context
- parallel execution would speed up the workflow
- the current context is too large for reliable single-agent handling

Do not delegate when:

- the task is simple enough for the current agent to handle directly
- the delegation overhead exceeds the benefit
- the sub-task requires the full conversation history

### 2. Compose The A2A Task

Use schema: `contracts/schemas/a2a-task.json`

Include:

- a unique task ID
- the delegator's identity
- the required assignee role
- a self-contained task description (assume the worker has zero prior context)
- all input data the worker needs
- reference to the output schema the result must conform to
- explicit success criteria
- constraints and boundaries
- risk tier (vibe, agentic, or engineering)

### 3. Dispatch And Monitor

- send the task to the worker agent
- if streaming is available, monitor progress updates
- enforce the timeout specified in the task

### 4. Validate The Returned Artifact

Use schema: `contracts/schemas/a2a-artifact.json`

Check:

- status is `completed`
- the result field conforms to the referenced output schema
- all success criteria are satisfied by the evidence
- no unresolved blockers remain

### 5. Handle Failures

If the artifact status is `failed`, `blocked`, or `partial`:

- review the failure reasons and blockers
- decide: retry with clarified input, escalate to a different role, or accept partial results with documented risk
- never silently accept a failed delegation

### 6. 2026: Secure Inter-Agent Delegation

To satisfy the 2026 security requirements:

- **Confused Deputy Prevention**: Before dispatching a task, verify that the required permissions and data scopes do not exceed what the delegator currently holds. The receiving agent must perform scope-validation on the task payload during the handoff phase.
- **Task-Scoped Credentials**: Generate a unique, short-lived cryptographic credential for the specific delegation leg. Avoid reusing authorization keys or sharing persistent tokens.
- **Transitive Trust Chain Verification**: When an agent delegates a task that was itself delegated (multi-hop delegation, e.g., A→B→C), package a verifiable delegation chain. The final worker must validate the signatures and scopes of all preceding agents in the path.
- **Zero-Trust Communication**: Treat every interaction as untrusted. Authenticate and authorize every API call, status poll, or streaming update message independently.
- **Data Minimization**: Pass only the specific data subsets required for the sub-task; avoid leaking entire session history or broad PII to specialized workers.
- **Attestation Hooks**: Require workers to sign a hardware-backed attestation (if available) confirming their environment state before trusting sensitive payloads.

## Output Schema

Use: `contracts/schemas/a2a-task.json` (outgoing) and `contracts/schemas/a2a-artifact.json` (incoming)

## Checklist

- [ ] delegation need justified (not cheaper to do inline)
- [ ] A2A task composed with all required fields
- [ ] task description is self-contained (zero assumed context)
- [ ] output schema reference included
- [ ] success criteria are specific and verifiable
- [ ] risk tier assigned
- [ ] returned artifact validated against schema
- [ ] success criteria verified against evidence
- [ ] failures handled explicitly (retry, escalate, or document risk)
- [ ] token usage and model recorded for cost tracking
- [ ] delegation scope validated to prevent granting permissions exceeding delegator limits (Confused Deputy prevention)
- [ ] task-scoped, time-bound credentials generated for the delegation leg (no persistent shared tokens)
- [ ] transitive trust chain (multi-hop path validation) verified for all sub-delegations
- [ ] zero-trust inter-agent communication parameters configured and authenticated
- [ ] data minimization applied (scope-restricted payloads)
- [ ] attestation verified for high-risk specialized workers

## Related Skills

- **agent-context-management**: Ensure delegated context is complete and relevant
- **agent-tool-orchestration**: Sequence delegations alongside direct tool use
- **agent-quality-gate**: Validate delegation results as part of phase gates
- **agent-a2a-protocol**: Full A2A 1.0 lifecycle and Antigravity integration
- **agent-model-routing**: Select the right model tier for the delegated task
- **agent-prompt-lifecycle**: Version and evaluate prompts used in delegated tasks
