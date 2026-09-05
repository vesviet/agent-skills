# Contract Schemas Index

**46 schemas** | Bundled examples checked by `validate-contracts.py` | Examples: 45/46

These schemas define machine-readable handoff contracts between agent roles. Each schema follows the `contract_type` discriminator convention for structured outputs.

---

## Quick Reference

| Schema | Title | Has Example | Has `contract_type` |
|--------|-------|:-----------:|:-------------------:|
| **Solution & Governance** | | | |
| `solution-brief.json` | Solution Brief | ✅ | ✅ |
| `ai-risk-register.json` | AI Risk Register | ✅ | ✅ |
| **Engineering Delivery** | | | |
| `feature-ticket.json` | Feature Ticket Specification | ✅ | ✅ |
| `technical-delivery-plan.json` | Technical Delivery Plan | ✅ | ✅ |
| `adr-spec.json` | Architecture Decision Record | ✅ | ✅ |
| `architecture-options.json` | Architecture Options Brief | ✅ | ✅ |
| `implementation-result.json` | Implementation Result | ✅ | ✅ |
| `api-contract-spec.json` | API Contract Specification | ✅ | ✅ |
| `deployment-plan.json` | Deployment Plan | ✅ | ✅ |
| `edge-deployment-spec.json` | Edge Deployment Specification | ✅ | ✅ |
| `system-design-spec.json` | System Design Specification | ✅ | ✅ |
| `aws-infra-spec.json` | AWS Infrastructure Specification | ❌ | ✅ |
| `pull-request-spec.json` | Pull Request Specification | ✅ | ✅ |
| `data-pipeline-spec.json` | Data Pipeline Specification | ✅ | ✅ |
| **Quality & Review** | | | |
| `code-review-finding.json` | Code Review Finding | ✅ | ✅ |
| `test-report.json` | QA Test Report | ✅ | ✅ |
| `validation-result.json` | Validation Result | ✅ | ✅ |
| `security-audit.json` | Security Audit Report | ✅ | ✅ |
| `performance-audit.json` | Performance Audit Result | ✅ | ✅ |
| `incident-report.json` | Incident Report | ✅ | ✅ |
| **Finance, Accounting & Compliance** | | | |
| `accounting-compliance-review.json` | Vietnam Accounting Compliance Review | ✅ | ✅ |
| **Design & Content** | | | |
| `ux-flow-spec.json` | UX Flow Specification | ✅ | ✅ |
| `ui-component-spec.json` | UI Component Specification | ✅ | ✅ |
| `content-handoff.json` | Content Handoff | ✅ | ✅ |
| `content-audit-report.json` | Content Audit Report | ✅ | ✅ |
| `documentation-handoff.json` | Documentation Handoff | ✅ | ✅ |
| `learning-handoff.json` | Learning Handoff | ✅ | ✅ |
| `research-report.json` | Research Report Specification | ✅ | ✅ |
| `data-analysis-report.json` | Data Analysis Report | ✅ | ✅ |
| `schema-migration.json` | Schema Migration Plan | ✅ | ✅ |
| **SEO & Publishing** | | | |
| `seo-content-brief.json` | SEO Content Brief | ✅ | ✅ |
| `seo-audit-report.json` | SEO Audit Report | ✅ | ✅ |
| `seo-metadata.json` | SEO Metadata | ✅ | ✅ |
| `seo-weekly-board.json` | SEO Weekly Board | ✅ | ✅ |
| `series-article.json` | Series Article | ✅ | ✅ |
| **A2A Protocol (Agent-to-Agent)** | | | |
| `a2a-task.json` | A2A Task Delegation | ✅ | — |
| `a2a-task-status.json` | A2A Task Status | ✅ | — |
| `a2a-task-progress.json` | A2A Task Progress Event | ✅ | — |
| `a2a-artifact.json` | A2A Task Artifact | ✅ | — |
| `a2a-task-cancel.json` | A2A Task Cancel Request | ✅ | — |
| `a2a-message.json` | A2A Message | ✅ | — |
| `a2a-jsonrpc-envelope.json` | A2A JSON-RPC 2.0 Envelope | ✅ | — |
| `a2a-push-notification-config.json` | A2A Push Notification Config | ✅ | — |
| `coordination-plan.json` | Coordination Plan | ✅ | ✅ |
| **Agent Infrastructure** | | | |
| `agent-card.json` | A2A Agent Card | ✅ | — |
| `agent-trace-span.json` | Agent Trace Span | ✅ | — |

---

## Detailed Schema Descriptions

See the per-category files below for the full description of each schema. The schema files themselves live next to this index in `core/contracts/schemas/`.

### Solution & Governance

See [`references/detailed/01-solution-and-governance.md`](references/detailed/01-solution-and-governance.md).

### Engineering Delivery

See [`references/detailed/02-engineering-delivery.md`](references/detailed/02-engineering-delivery.md).

### Quality & Review

See [`references/detailed/03-quality-and-review.md`](references/detailed/03-quality-and-review.md).

### Finance, Accounting & Compliance

See [`references/detailed/04-finance-accounting-and-compliance.md`](references/detailed/04-finance-accounting-and-compliance.md).

### Design & Content

See [`references/detailed/05-design-and-content.md`](references/detailed/05-design-and-content.md).

### SEO & Publishing

See [`references/detailed/06-seo-and-publishing.md`](references/detailed/06-seo-and-publishing.md).

### A2A Protocol (Agent-to-Agent)

See [`references/detailed/07-a2a-protocol.md`](references/detailed/07-a2a-protocol.md).

### Agent Infrastructure

See [`references/detailed/08-agent-infrastructure.md`](references/detailed/08-agent-infrastructure.md).

## Usage

### In Skills

Every skill that produces structured output references a contract in its `## Output Schema` section:

```markdown
## Output Schema

Use: `contracts/schemas/implementation-result.json`
```

### Validation

```bash
# Validate a contract instance against its schema (requires ajv-cli)
npx ajv validate -s contracts/schemas/implementation-result.json -d my-output.json
```

### Cross-references

The primary delivery chain references:

```
feature-ticket.json
  → technical-delivery-plan.json (Technical Lead)
    → implementation-result.json (per slice, Developer)
      → code-review-finding.json (Reviewer)
        → test-report.json (QA Engineer)
          → validation-result.json (phase gate, Agent Coordinator)
```

---

## Ownership

| Schema | Produced by | Consumed by |
|--------|-------------|-------------|
| `solution-brief.json` | Solution Architect | Technical Architect, Business Analyst, Product Manager, Agent Coordinator, Researcher |
| `ai-risk-register.json` | Business Analyst, Project Manager, Security Engineer | Product Manager, Technical Architect, Security Engineer, Agent Coordinator |
| `feature-ticket.json` | Business Analyst | Technical Architect, Technical Lead, Backend/Frontend Developer, Data Analyst, SEO Analyst |
| `technical-delivery-plan.json` | Technical Lead | Backend Developer, Frontend Developer, Mobile Engineer, QA Engineer, Reviewer, Agent Coordinator |
| `adr-spec.json` | Technical Architect | Backend Developer, Frontend Developer, Mobile Engineer, Cloudflare Engineer |
| `architecture-options.json` | Technical Architect, Researcher | Technical Architect (for ADR), Technical Lead |
| `implementation-result.json` | Backend/Frontend/Mobile/3D/Cloudflare Engineer | Technical Lead, Reviewer, QA Engineer, Agent Coordinator |
| `api-contract-spec.json` | Backend Developer | Frontend Developer, Mobile Engineer, Technical Writer, Technical Lead |
| `deployment-plan.json` | DevOps Engineer | Project Manager, SRE, Technical Lead |
| `edge-deployment-spec.json` | Cloudflare Engineer | DevOps Engineer, SRE, Agent Coordinator |
| `system-design-spec.json` | System Engineer | AWS Engineer, DevOps Engineer, Cloudflare Engineer, SRE |
| `aws-infra-spec.json` | AWS Engineer | DevOps Engineer, SRE, Security Engineer, System Engineer |
| `pull-request-spec.json` | Backend/Frontend/Mobile Engineer, Technical Lead | Reviewer, Technical Lead, Product Manager, Agent Coordinator |
| `code-review-finding.json` | Reviewer | Developers, Technical Lead, QA Engineer, Agent Coordinator |
| `test-report.json` | QA Engineer | Technical Lead, Reviewer, Project Manager, Agent Coordinator |
| `validation-result.json` | QA Engineer, Agent Coordinator | Technical Lead, Agent Coordinator (phase gate) |
| `security-audit.json` | Security Engineer | Technical Lead, Reviewer, DevOps Engineer |
| `performance-audit.json` | Frontend Developer (via perf-profiling), SRE | Technical Lead, Backend Developer |
| `incident-report.json` | SRE | Technical Writer, Technical Lead, Project Manager |
| `accounting-compliance-review.json` | Vietnam Accounting Specialist | Business Analyst, Backend Developer, E-commerce Engineer, Data Analyst, QA Engineer, Security Engineer, Agent Coordinator, qualified human reviewers |
| `ux-flow-spec.json` | UI/UX Designer | Frontend Developer, Backend Developer, QA Engineer, Technical Lead |
| `ui-component-spec.json` | UI/UX Designer | Frontend Developer, Mobile Engineer, QA Engineer |
| `content-handoff.json` | Content Writer | SEO Analyst, Publisher, Editor |
| `documentation-handoff.json` | Technical Writer | DevOps Engineer, SRE, Publisher |
| `learning-handoff.json` | Teacher | Learner, Content Writer |
| `research-report.json` | Researcher | Business Analyst, Technical Architect, Data Analyst |
| `data-analysis-report.json` | Data Analyst | Business Analyst, Product Manager, Researcher |
| `schema-migration.json` | Data Engineer, Backend Developer | DevOps Engineer, SRE, QA Engineer |
| `seo-content-brief.json` | SEO Analyst | Content Writer |
| `seo-audit-report.json` | SEO Analyst | Content Writer, Technical Lead (site fixes) |
| `seo-metadata.json` | SEO Analyst | Content Writer, Frontend Developer |
| `seo-weekly-board.json` | Task Planner, SEO Analyst | Content Writer, Project Manager |
| `series-article.json` | Content Writer, SEO Analyst | Publisher, Frontend Developer |
| `coordination-plan.json` | Agent Coordinator | All execution roles, Project Manager |
| `a2a-task.json` | Agent Coordinator | All agent roles |
| `a2a-task-status.json` | Any agent role | Agent Coordinator |
| `a2a-task-progress.json` | Any agent role | Agent Coordinator |
| `a2a-artifact.json` | Any agent role | Agent Coordinator, receiving agent |
| `agent-card.json` | Agent Infrastructure | Agent Coordinator, client systems |
| `agent-trace-span.json` | Any instrumented role | Agent Coordinator, SRE, Observability stack |
