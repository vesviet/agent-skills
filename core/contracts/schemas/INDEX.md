# Contract Schemas Index

**42 schemas** | Bundled examples checked by `validate-contracts.py` | Examples: 41/42

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
| **Quality & Review** | | | |
| `code-review-finding.json` | Code Review Finding | ✅ | ✅ |
| `test-report.json` | QA Test Report | ✅ | ✅ |
| `validation-result.json` | Validation Result | ✅ | ✅ |
| `security-audit.json` | Security Audit Report | ✅ | ✅ |
| `performance-audit.json` | Performance Audit Result | ✅ | ✅ |
| `incident-report.json` | Incident Report | ✅ | ✅ |
| **Design & Content** | | | |
| `ux-flow-spec.json` | UX Flow Specification | ✅ | ✅ |
| `ui-component-spec.json` | UI Component Specification | ✅ | ✅ |
| `content-handoff.json` | Content Handoff | ✅ | ✅ |
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

### Solution & Governance

#### `solution-brief.json`

**Solution Brief**  
Primary machine-readable handoff from the Solution Architect, produced before requirements or architecture are locked. Consumed by Technical Architect (for adr-spec.json), Business Analyst (for feature-ticket.json), Product Manager (go/no-go), and Agent Coordinator (solution scoping gate). Captures problem framing, capability gaps, build-vs-buy decision (including MCP marketplace evaluation), AI feasibility, agent ROI, and compliance constraints.

Required fields: `contract_type`, `problem_statement`, `options_considered`, `build_vs_buy_decision`, `recommendation`  
✅ Has example

#### `ai-risk-register.json`

**AI Risk Register**  
Structured output from the ai-risk-assessment skill (owned by Business Analyst, Project Manager, or Security Engineer). Applies NIST AI RMF 1.0, the NIST AI 600-1 GenAI Profile, EU AI Act risk classification, and OWASP ASI alignment. A living lifecycle artifact consumed by Product Manager, Technical Architect, Security Engineer, and Agent Coordinator before delivery commitment.

Required fields: `contract_type`, `governance`, `eu_ai_act`, `nist_600_1_risks`, `residual_risks`  
✅ Has example

### Engineering Delivery

#### `feature-ticket.json`

**Feature Ticket Specification**  
Structured output from Business Analyst. Consumed by Technical Architect (for adr-spec.json), Technical Lead (for technical-delivery-plan.json), and Backend/Frontend Developers as the source of truth for scope, acceptance criteria, and business rules. Also optionally triggers Data Analyst and SEO Analyst handoffs.

Required fields: `contract_type`, `title`, `type`, `acceptance_criteria`  
Size: 8,811 bytes  
✅ Has example

#### `technical-delivery-plan.json`

**Technical Delivery Plan**  
Structured implementation plan produced by Technical Lead. Consumed by Backend Developer, Frontend Developer, Mobile Engineer, QA Engineer, Reviewer, Agent Coordinator, and Technical Writer. One plan per feature or major slice grouping. Slices map directly to implementation-result.json emits.

Required fields: `contract_type`, `work_title`, `goal_summary`, `slices`, `quality_gates`, `readiness_status`  
Size: 7,879 bytes  
✅ Has example

#### `adr-spec.json`

**Architecture Decision Record**  
Structured output from Technical Architect documenting an Architecture Decision Record (ADR). Consumed by Backend Developer, Frontend Developer, Mobile Engineer, Cloudflare Engineer, Technical Lead, and Reviewer as a binding technical constraint. Supersedes earlier ADRs when architecture evolves.

Required fields: `contract_type`, `title`, `status`, `context`, `options_considered`, `decision`, `consequences`  
Size: 6,884 bytes  
✅ Has example

#### `architecture-options.json`

**Architecture Options Brief**  
Structured options analysis before an ADR is accepted.

Required fields: `contract_type`, `title`, `context`, `options`  
Size: 3,107 bytes  
✅ Has example

#### `implementation-result.json`

**Implementation Result**  
Structured output from a code implementation step. Emitted by Backend Developer, Frontend Developer, Mobile Engineer, 3D Graphics Engineer, or Cloudflare Engineer per delivery slice. Used by Technical Lead, Reviewer, Agent Coordinator, and QA Engineer for phase gate evidence. One document per slice.

Required fields: `contract_type`, `files_changed`, `breaking_changes`, `validation_run`  
Size: 6,448 bytes  
✅ Has example

#### `api-contract-spec.json`

**API Contract Specification**  
Structured output defining an API endpoint contract. Used for backend-to-frontend handoff and A2A delegation.

Required fields: `contract_type`, `endpoint`, `method`, `response_success`, `response_errors`  
Size: 3,605 bytes  
✅ Has example

#### `deployment-plan.json`

**Deployment Plan**  
Structured output for a deployment strategy and execution plan.

Required fields: `contract_type`, `version`, `environments`, `steps`, `rollback_plan`  
Size: 3,276 bytes  
✅ Has example

#### `edge-deployment-spec.json`

**Edge Deployment Specification**  
Structured Cloudflare edge deployment handoff: Wrangler, bindings, DNS/cache, rollout, and rollback.

Required fields: `contract_type`, `platform`, `project_ref`, `deployment_target`, `version`, `environments`, `wrangler_config_path`, `deploy_steps`, `rollback_plan`  
Size: 6,794 bytes  
✅ Has example

#### `system-design-spec.json`

**System Design Specification**  
Structured output from System Engineer for cloud-agnostic system topology, capacity models, and AI infrastructure specifications. Consumed by AWS Engineer (as upstream input for managed service provisioning), DevOps Engineer (as infrastructure baseline), Cloudflare Engineer (origin topology), and SRE (SLO design inputs).

Required fields: `contract_type`, `spec_id`, `system_name`, `design_trigger`, `nfr_targets`, `topology`, `capacity_model`  
Size: varies  
✅ Has example

#### `aws-infra-spec.json`

**AWS Infrastructure Specification**  
Machine-readable AWS infrastructure handoff produced by the AWS Engineer. Consumed by DevOps Engineer (EKS cluster endpoint, ECR repo URIs, pipeline inputs), SRE (Multi-AZ topology for SLO design), Security Engineer (IAM roles for review), and System Engineer (cross-layer integration). Contains resource_map, iam_roles (with review status), cost_attribution, monitoring_config, and iac_reference.

Required fields: `contract_type`, `spec_id`, `system_name`, `aws_account`, `region`, `resource_map`, `iam_roles`, `cost_attribution`  
Size: varies  
❌ No example yet

### Quality & Review

#### `code-review-finding.json`

**Code Review Finding**  
Structured output from the Reviewer role using the review-code skill. Emitted per change set or PR. Consumed by developers (for fixes), Technical Lead (for delivery readiness), Agent Coordinator (as phase gate evidence), and QA (for validation gaps). One document covers the full review; findings[] contains individual issues.

Required fields: `contract_type`, `change_ref`, `findings`, `review_matrix`, `blast_radius_assessment`, `merge_recommendation`  
Size: 7,905 bytes  
✅ Has example

#### `test-report.json`

**QA Test Report**  
Structured output from QA Engineer using write-tests, frontend-testing, or review-service skills. Emitted after test execution. Consumed by Technical Lead, Reviewer, Project Manager, and Agent Coordinator as release confidence evidence. Complements code-review-finding.json — review catches code issues, test-report catches behavior risk.

Required fields: `contract_type`, `ticket_ref`, `environment`, `status`, `scenarios_executed`, `release_recommendation`  
Size: 6,341 bytes  
✅ Has example

#### `validation-result.json`

**Validation Result**  
Structured output from a validation or quality gate step.

Required fields: `contract_type`, `phase_reviewed`, `checks_run`, `passed`, `decision`  
Size: 2,651 bytes  
✅ Has example

#### `security-audit.json`

**Security Audit Report**  
Structured output for a security audit or vulnerability assessment.

Required fields: `contract_type`, `target`, `audit_type`, `findings`, `overall_risk_score`  
Size: 2,776 bytes  
✅ Has example

#### `performance-audit.json`

**Performance Audit Result**  
Structured output for a frontend or 3D performance audit.

Required fields: `contract_type`, `target`, `findings`, `verdict`  
Size: 3,286 bytes  
✅ Has example

#### `incident-report.json`

**Incident Report**  
Structured output for SRE incident response and post-mortems.

Required fields: `contract_type`, `severity`, `status`, `impact`, `timeline`  
Size: 3,524 bytes  
✅ Has example

### Design & Content

#### `ux-flow-spec.json`

**UX Flow Specification**  
Structured multi-screen flow handoff from UI/UX Designer to Frontend, QA, and Backend.

Required fields: `contract_type`, `flow_id`, `flow_name`, `user_goal`, `screens`, `component_spec_refs`  
Size: 5,782 bytes  
✅ Has example

#### `ui-component-spec.json`

**UI Component Specification**  
Structured component spec for handoff between UI/UX Designer and Frontend Developer.

Required fields: `component_name`, `type`, `states`  
Size: 4,683 bytes  
✅ Has example

#### `content-handoff.json`

**Content Handoff**
Structured handoff from Content Writer to SEO Analyst, Reviewer, or publisher upon completing an article. Includes typed information gain gate (`information_gain.type` enum with 6 categories), GEO/AEO execution evidence (`geo_aeo_fields_applied`: answer-first, fan-out coverage, answer formats, fact density), E-E-A-T signal audit (`eeat_signals`: experience proof type, YMYL flag), and source credibility tracking aligned with research-report.json source hierarchy. Pairs with seo-metadata.json for final publication metadata.

Required fields: `contract_type`, `content_path`, `status`
Size: 12,064 bytes
✅ Has example

#### `documentation-handoff.json`

**Documentation Handoff**  
Structured documentation deliverable from Technical Writer.

Required fields: `contract_type`, `topic`, `audience`, `doc_paths`, `doc_type`, `status`  
Size: 2,973 bytes  
✅ Has example

#### `learning-handoff.json`

**Learning Handoff**  
Structured handoff for MOET-aligned middle-school learning plans, exercises, and evaluations.

Required fields: `contract_type`, `subject`, `grade`, `topic`, `artifact_type`, `goals`, `next_steps`  
Size: 2,792 bytes  
✅ Has example

#### `research-report.json`

**Research Report Specification**  
Structured output for iterative research synthesis with deep (10+ rounds) or scoped depth.

Required fields: `contract_type`, `objective`, `execution_metrics`, `synthesis`, `raw_data_references`, `recommended_next_roles`  
Size: 6,782 bytes  
✅ Has example

#### `data-analysis-report.json`

**Data Analysis Report**  
Structured analyst deliverable for metrics, findings, and recommendations.

Required fields: `contract_type`, `business_question`, `metrics`, `sources`, `findings`, `confidence`  
Size: 3,347 bytes  
✅ Has example

#### `schema-migration.json`

**Schema Migration Plan**  
Structured output for a database migration plan.

Required fields: `contract_type`, `migration_name`, `database`, `changes`, `is_destructive`, `requires_downtime`, `up_script`, `down_script`  
Size: 2,118 bytes  
✅ Has example

### SEO & Publishing

#### `seo-content-brief.json`

**SEO Content Brief**  
Pre-draft handoff from SEO Analyst to Content Writer. Produced by the optimize-seo skill. Validates against seo-analyst.md Output Template and Review Checklist.

Required fields: `brief_id`, `created_at`, `site`, `context`, `topical_authority`, `keywords`, `geo_aeo`, `on_page_plan`, `eeat_gates`, `schema_requirements`, `internal_links`, `handoff`  
Size: 25,539 bytes  
✅ Has example

#### `seo-audit-report.json`

**SEO Audit Report**  
Pre/post-publish audit produced by SEO Analyst using optimize-seo skill. Covers traditional SEO issues, AI extractability, metadata compliance, and technical escalation items. Validates against seo-analyst.md Review Checklist.

Required fields: `audit_id`, `created_at`, `site`, `audited_url_or_path`, `audit_type`, `traditional_seo`, `ai_extractability`, `metadata_audit`, `cannibalization_check`, `handoff`  
Size: 20,547 bytes  
✅ Has example

#### `seo-metadata.json`

**SEO Metadata**  
Publisher-ready metadata produced by SEO Analyst. Used at publish time to set title, meta description, slug, and social metadata. Does not include full article content — that is in content-handoff.json. Validates against seo-analyst.md Outputs Produced section and overlay slug/frontmatter rules.

Required fields: `metadata_id`, `created_at`, `site`, `url_or_path`, `title`, `meta_description`, `slug`, `primary_keyword`, `secondary_keywords`, `schema_types`, `status`  
Size: 8,838 bytes  
✅ Has example

#### `seo-weekly-board.json`

**SEO Weekly Board**  
7-day dual-site topic board for machine handoff between Task Planner, SEO Analyst, and Content Writer. Produced by the optimize-seo skill under the seo-publishing overlay. Mirrors the markdown plan/baiviet/plan-YYYY-MM-DD.md board in structured JSON. Validates against overlays/seo-publishing/rules/topic-board-template.md and site-mix-and-cannibalization.md.

Required fields: `board_id`, `created_at`, `week_start`, `week_end`, `timezone`, `sites`, `entries`, `guardrails_check`, `handoff`  
Size: 22,945 bytes  
✅ Has example

#### `series-article.json`

**Series Article**  
Schema for a series article output, validating required frontmatter fields and body structure before publishing.

Required fields: `frontmatter`, `body`  
Size: 3,422 bytes  
✅ Has example

### A2A Protocol (Agent-to-Agent)

#### `a2a-task.json`

**A2A Task Delegation**  
Task unit for A2A 1.0 delegation (submit, stream, get, cancel). Extends pack delegation with full lifecycle.

Required fields: `task_id`, `delegator`, `assignee_role`, `task_description`, `output_schema_ref`, `success_criteria`, `risk_tier`  
Size: 3,660 bytes  
✅ Has example

#### `a2a-task-status.json`

**A2A Task Status**  
Response for Get Task / List Tasks operations (A2A 1.0).

Required fields: `task_id`, `state`, `updated_at`  
Size: 1,717 bytes  
✅ Has example

#### `a2a-task-progress.json`

**A2A Task Progress Event**  
Server-Sent Event payload for streaming task updates (A2A Send Streaming Message / Antigravity agent.stream).

Required fields: `event`, `task_id`, `timestamp`  
Size: 1,614 bytes  
✅ Has example

#### `a2a-artifact.json`

**A2A Task Artifact**  
Deliverable returned by a worker agent (A2A Artifact / Antigravity task result).

Required fields: `task_id`, `status`  
Size: 3,042 bytes  
✅ Has example

#### `a2a-task-cancel.json`

**A2A Task Cancel Request**  
Request body for tasks/cancel (A2A 1.0).

Required fields: `task_id`, `cancel_reason`  
Size: 800 bytes  
✅ Has example

#### `a2a-message.json`

**A2A Message**  
Single message in an A2A task conversation history.

Required fields: `message_id`, `role`, `parts`  
Size: 1,403 bytes  
✅ Has example

#### `a2a-jsonrpc-envelope.json`

**A2A JSON-RPC 2.0 Envelope**  
Wire-format wrapper for A2A operations (agent.invoke, agent.stream, tasks/get, tasks/cancel).

Required fields: `jsonrpc`  
Size: 1,422 bytes  
✅ Has example

#### `a2a-push-notification-config.json`

**A2A Push Notification Config**  
Webhook configuration for async task completion (A2A 1.0 push notifications).

Required fields: `task_id`, `callback_url`, `events`  
Size: 1,254 bytes  
✅ Has example

#### `coordination-plan.json`

**Coordination Plan**

Structured multi-agent execution plan produced by Agent Coordinator. Defines phases, dependencies, gate conditions, circuit breakers, per-phase token budgets, confidence levels, and interruption recovery checkpoints for complex multi-role workflows. Consumed by all execution roles to understand their phase, sequencing, and reporting obligations. Pairs with a2a-task.json for per-phase task dispatch.

Required fields: `contract_type`, `goal`, `phases`, `execution_state`
Size: 13,665 bytes
✅ Has example

### Agent Infrastructure

#### `agent-card.json`

**A2A Agent Card**  
Self-describing manifest for agent discovery (A2A 1.0 / Antigravity). Publish at /.well-known/agent.json per role or use pack registry.

Required fields: `name`, `description`, `url`, `version`, `protocol_version`, `capabilities`, `skills`  
Size: 4,901 bytes  
✅ Has example

#### `agent-trace-span.json`

**Agent Trace Span**  
Lightweight observability span for agent sessions (OpenTelemetry GenAI-aligned fields).

Required fields: `trace_id`, `span_id`, `role`, `operation`, `status`  
Size: 1,867 bytes  
✅ Has example

---

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
| `code-review-finding.json` | Reviewer | Developers, Technical Lead, QA Engineer, Agent Coordinator |
| `test-report.json` | QA Engineer | Technical Lead, Reviewer, Project Manager, Agent Coordinator |
| `validation-result.json` | QA Engineer, Agent Coordinator | Technical Lead, Agent Coordinator (phase gate) |
| `security-audit.json` | Security Engineer | Technical Lead, Reviewer, DevOps Engineer |
| `performance-audit.json` | Frontend Developer (via perf-profiling), SRE | Technical Lead, Backend Developer |
| `incident-report.json` | SRE | Technical Writer, Technical Lead, Project Manager |
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
