# Output Contracts

This directory defines machine-readable schemas for structured data exchange between agents, tools, and workflow steps.

## Why Contracts Exist

In 2026, agents must produce outputs that are not just human-readable but **machine-parseable and schema-validated**. When one agent hands off work to another, the receiving agent must be able to trust the format without guessing.

Contracts use JSON Schema (draft 2020-12) and are enforced via native constrained decoding (Structured Outputs) or post-generation validation (Pydantic/Zod).

## Directory Structure

```
contracts/
  README.md
  schemas/
    code-review-finding.json
    implementation-result.json
    validation-result.json
    feature-ticket.json
    data-analysis-report.json
    content-handoff.json
    ux-flow-spec.json
    ui-component-spec.json
    architecture-options.json
    adr-spec.json
    technical-delivery-plan.json
    documentation-handoff.json
    edge-deployment-spec.json
    learning-handoff.json
    seo-content-brief.json
    seo-audit-report.json
    seo-metadata.json
    seo-weekly-board.json
    agent-card.json
    a2a-task.json
    a2a-artifact.json
    a2a-task-status.json
    a2a-task-progress.json
    a2a-message.json
    a2a-jsonrpc-envelope.json
    a2a-push-notification-config.json
    a2a-task-cancel.json
    agent-trace-span.json
    coordination-plan.json
```

A2A registry (generated): `core/a2a/.well-known/agent-registry.json`

Adapters: `adapters/antigravity/ANTIGRAVITY.md`, `adapters/cursor/README.md`

## Usage In Skills

Every skill that produces structured output should reference a contract:

```markdown
## Output Schema

Use: `contracts/schemas/code-review-finding.json`
```

## Validation

Contracts should be validated against the JSON Schema meta-schema before use. Invalid schemas will produce unpredictable constrained decoding behavior.

## When To Create A New Schema

- when a new handoff type is needed between agents or workflow steps
- when an existing skill output is consumed programmatically
- when a tool server needs a typed input or output contract
