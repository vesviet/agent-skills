# Output Contracts

This directory defines machine-readable schemas for structured data exchange between agents, tools, and workflow steps.

## Why Contracts Exist

In 2026, agents must produce outputs that are not just human-readable but **machine-parseable and schema-validated**. When one agent hands off work to another, the receiving agent must be able to trust the format without guessing.

Contracts use JSON Schema (draft 2020-12) and are enforced via native constrained decoding (Structured Outputs) or post-generation validation (Pydantic/Zod).

## Quick Reference

See [`schemas/INDEX.md`](schemas/INDEX.md) for the full schema index with descriptions, ownership table, and cross-reference chain.

## Delivery Chain (Primary Workflow)

```
solution-brief.json          ← Solution Architect (when solution scoping precedes requirements)
  → feature-ticket.json          ← Business Analyst
    → technical-delivery-plan.json  ← Technical Lead
      → implementation-result.json  ← Developer (per slice)
        → code-review-finding.json  ← Reviewer
          → test-report.json        ← QA Engineer
            → validation-result.json ← Agent Coordinator (phase gate)
```

## All Schemas (43 total)

### Solution & Governance
- `solution-brief.json` — Solution Architect scoping handoff (build-vs-buy, capability gaps, AI feasibility, compliance)
- `ai-risk-register.json` — AI risk register (NIST AI RMF + 600-1, EU AI Act tier, OWASP ASI alignment)

### Engineering Delivery
- `feature-ticket.json` — Business requirements and AC
- `technical-delivery-plan.json` — Sliced implementation plan from Technical Lead
- `adr-spec.json` — Architecture Decision Record
- `architecture-options.json` — Options analysis before ADR
- `implementation-result.json` — Code change handoff from Developer
- `api-contract-spec.json` — API endpoint definition
- `deployment-plan.json` — General deployment steps
- `edge-deployment-spec.json` — Cloudflare-specific deployment
- `system-design-spec.json` — System Engineer topology, capacity, and AI-infra design
- `aws-infra-spec.json` — AWS Engineer managed-service and IAM infrastructure spec

### Quality & Review
- `code-review-finding.json` — Full code review with findings matrix
- `test-report.json` — QA test execution report
- `validation-result.json` — Phase gate validation
- `security-audit.json` — Security audit findings
- `performance-audit.json` — Performance profiling report
- `incident-report.json` — SRE incident post-mortem

### Finance, Accounting & Compliance
- `accounting-compliance-review.json` — Vietnam Accounting Specialist accounting-regime, evidence, reconciliation, close, retention, and human-approval handoff; not a tax filing, legal opinion, audit opinion, or authorization for external action

### Design & Content
- `ux-flow-spec.json` — Multi-screen UX flow handoff
- `ui-component-spec.json` — UI component specification
- `content-handoff.json` — Article/content completion handoff
- `documentation-handoff.json` — Technical doc update handoff
- `learning-handoff.json` — Teaching/exercise handoff
- `research-report.json` — Research findings
- `data-analysis-report.json` — Data analysis findings
- `schema-migration.json` — Database migration definition

### SEO & Publishing
- `seo-content-brief.json` — SEO keyword brief and content plan
- `seo-audit-report.json` — On-page SEO audit
- `seo-metadata.json` — Page metadata (title, description, OG)
- `seo-weekly-board.json` — Weekly content sprint board
- `series-article.json` — Article series navigation

### A2A Protocol
- `coordination-plan.json` — Multi-agent phase graph
- `a2a-task.json` — A2A task envelope
- `a2a-task-status.json` — Task status update
- `a2a-task-progress.json` — Task progress notification
- `a2a-artifact.json` — Task output artifact
- `a2a-task-cancel.json` — Task cancellation
- `a2a-message.json` — A2A message unit
- `a2a-jsonrpc-envelope.json` — JSON-RPC wrapper
- `a2a-push-notification-config.json` — Push notification config

### Agent Infrastructure
- `agent-card.json` — Agent capability descriptor
- `agent-trace-span.json` — OpenTelemetry trace span

## Usage In Skills

Every skill that produces structured output should reference a contract:

```markdown
## Output Schema

Use: `contracts/schemas/implementation-result.json`
```

## Validation

```bash
# Validate a contract instance (requires ajv-cli)
npx ajv validate -s contracts/schemas/implementation-result.json -d my-output.json
```

The bundled validator verifies JSON parsing, required top-level metadata, and required fields/discriminators in each bundled example. Validate production payloads with a Draft 2020-12 implementation before constrained decoding or cross-system exchange.

## When To Create A New Schema

- when a new handoff type is needed between agents or workflow steps
- when an existing skill output is consumed programmatically
- when a tool server needs a typed input or output contract

## Related

- A2A registry: `core/a2a/.well-known/agent-registry.json`
- Adapters: `adapters/antigravity/ANTIGRAVITY.md`, `adapters/cursor/README.md`
