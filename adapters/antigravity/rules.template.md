# Antigravity Project Rules — Agent Skills Pack (A2A 1.0)

Apply these rules when Antigravity agents work in a repository using the agent-skills pack.

## Always-On

- Follow `core/rules/code.md` (commit/push approval, no secrets in artifacts).
- Verify actions against pack policies before tool use.

## Role Assignment

- Read `core/roles/role-standard.md` then `core/roles/<role>.md`.
- Respect Skill Toolbox Lock and Boundary Lock.
- Discover other agents via `core/a2a/.well-known/agent-registry.json`.

## A2A 1.0 Compliance

- Every delegating agent MUST compose `a2a-task.json` with UUID `task_id`, `interaction_mode`, and `output_schema_ref`.
- Worker agents MUST return `a2a-artifact.json` validated against the task schema.
- Long-running work MUST emit `a2a-task-progress.json` events (`task.status`, `task.artifact`) when streaming.
- Use lifecycle states: `submitted` → `working` → `completed` | `failed` | `canceled`.
- Task IDs MUST be UUID v4 when integrating with Antigravity AgentKit.
- Errors on wire transports MUST use `a2a-jsonrpc-envelope.json` error objects.

## Structured Outputs

- Do not hand off delivery artifacts as unstructured prose when a schema exists in `core/contracts/schemas/`.
- Prefer JSON blocks validated against the named schema file.

## Policy

- Check `core/policies/action-boundaries.yaml` for the active role before write/delete/deploy/migration.
- Classify sensitive output with `core/policies/data-classification.yaml`.

## Antigravity-Specific

- Serve or reference Agent Cards from `core/a2a/registry/<role>.agent-card.json`.
- Coordinator-led work MUST use `coordination-plan.json` plus per-phase A2A tasks.
- Use `agent.stream` / SSE for engineering-tier tasks exceeding 2 minutes expected runtime.
