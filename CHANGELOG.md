# Changelog

All notable changes to the agent-skills engineering pack.

## [2.6.6] - 2026-05-22

### Added
- Skills `design-review` and `accessibility-review` (foundation)
- `build-deploy` workflow: optional Cloudflare edge release step (4b) and `debug-workers-edge` verification

### Changed
- `core/skills/README.md`: full inventory sync (57 core), `conduct-research`, skill boundary table, backlog cleanup
- `data-engineer` skill: *When To Use Data Analyst Instead* boundary section
- `agent-model-routing`: *When Agent Coordinator Enables This* guidance
- Role toolboxes: UI/UX, Reviewer, QA, Frontend, Data Engineer, Agent Coordinator notes for new skills

## [2.6.5] - 2026-05-22

### Changed
- Deliverable Routing and Role Boundaries: `business-analyst`, `content-writer`, `seo-analyst`, `technical-architect`, `agent-coordinator`
- Personalized workspace `AGENTS.md`: Astro Cloudflare sites, cloudflare-engineer mapping, engineering handoffs

## [2.6.4] - 2026-05-22

### Added
- Contract `learning-handoff.json` for Teacher role MOET handoffs

### Changed
- Role hygiene audit: Deliverable Routing and Role Boundaries for DevOps, QA, SRE, PM, Product, Security, Reviewer, Data Engineer, Task Planner, Teacher
- `data-analyst`: fix `contracts/schemas/data-analysis-report.json` in Outputs (A2A card)
- `devops-engineer`, `teacher`: structured contract emission in Definition of Done

## [2.6.3] - 2026-05-22

### Added
- Role `cloudflare-engineer` for Wrangler, Pages/Workers, bindings, and edge incidents
- Contract `edge-deployment-spec.json`
- Skills `manage-wrangler-deploy`, `configure-cloudflare-bindings`, `debug-workers-edge`
- Policy profile `cloudflare-engineer` in action-boundaries.yaml

### Changed
- `devops-engineer`, `sre`, `frontend-developer`: Cloudflare Engineer handoff references
- `overlays/astro-cloudflare`: recommended role pairing

## [2.6.2] - 2026-05-22

### Added
- `research-report.json`: `depth_mode` (deep|scoped), `recommended_next_roles`, `inferences`, `residual_risks`, optional `feature_ticket_ref`

### Changed
- `researcher`: R1 toolbox (Primary `conduct-research` only), R2 handoff parity, R3 contract depth alignment
- `conduct-research` skill: depth_mode rules and scoped waiver

## [2.6.1] - 2026-05-22

### Changed
- `frontend-developer`, `backend-developer`, `3d-graphics-engineer`: D1–D3 developer handoff parity
- All three: `implementation-result.json` in Outputs; Inputs path-ified; Deliverable Routing tables
- `frontend-developer`: Role Handoff aligned with UX/Architect/Lead triangle; FE↔3D two-way handoff
- `backend-developer`: Collaboration expanded; Technical Writer and Lead consumption paths
- `3d-graphics-engineer`: Lead/UX/Architect integration; Primary toolbox cleanup; optional overlays

## [2.6.0] - 2026-05-22

### Added
- Contracts: `architecture-options.json`, `technical-delivery-plan.json`, `documentation-handoff.json`
- Skill `plan-technical-delivery` for Technical Lead

### Changed
- `adr-spec.json`: affected_services, api_contract_refs, supersedes_adr, rollback_plan, feature_ticket_ref
- `technical-architect`, `technical-lead`, `technical-writer`: full triangle handoffs (packages A/B/C)
- `business-analyst`, `agent-coordinator`, `backend-developer`, `frontend-developer`: aligned contracts
- `write-tech-radar`: role routing vs ADR and Technical Writer

## [2.5.4] - 2026-05-22

### Added
- `ux-flow-spec.json` contract for multi-screen UX handoff
- `overlays/ui-design-system` with flow/component handoff conventions
- UI/UX Designer: BA/Researcher/Data Analyst handoffs, deliverable decision table, optional overlays

### Changed
- `ui-component-spec.json`: flow_id, events, copy_per_state, api_fields, feature_ticket_ref
- `design-ux-flow` skill: layered contracts and deliverable decision table
- `frontend-developer`, `business-analyst`, `researcher`, `data-analyst`: UX spec handoffs

## [2.5.3] - 2026-05-22

### Added
- `write-article` foundation skill for editorial drafting
- `content-handoff.json` contract for article deliverables
- Content Writer: Research Depth table, overlay activation, publish-log duty under seo-publishing

### Changed
- `content-writer`: primary toolbox write-article + write-documentation; supporting overlay site skills
- `write-documentation`: role routing (articles vs Technical Writer)
- `researcher`, `business-analyst`, `task-planner`, `seo-publishing`: Content Writer handoffs

## [2.5.2] - 2026-05-22

### Added
- `feature-ticket.json`: business_rules, preserved/changed behavior, open_questions, analytics_request, seo_content_request
- Business Analyst: Research and SEO handoffs; Research Request and SEO Content Request template sections

### Changed
- `business-analyst`: conduct-research supporting skill; expanded collaboration and guardrails
- `analyze-business-requirements` skill: ticket JSON, delegation table, checklist
- `generate-a2a-registry.py`: output schemas derived from Outputs Produced only (fixes BA agent card)
- `researcher`, `seo-analyst`: explicit handoff from Business Analyst

## [2.5.1] - 2026-05-22

### Added
- `overlays/seo-publishing`: dual-site sprint cadence, plan/baiviet board, publish-log, and cannibalization rules
- Contract `seo-weekly-board.json` for structured 7-day topic boards

### Changed
- `seo-analyst` and `task-planner`: optional seo-publishing overlay activation

## [2.5.0] - 2026-05-22

### Added
- `seo-analyst` role with skill `optimize-seo`
- Contracts `seo-content-brief.json` and `seo-audit-report.json`
- A2A agent card and policy profile for SEO Analyst

### Changed
- `content-writer` and `task-planner`: explicit SEO Analyst handoff for briefs, audits, and topic boards
- `core/roles/README.md`: Content And SEO lifecycle mapping

## [2.4.2] - 2026-05-22

### Added
- `overlays/data-analyst-stack`: DuckDB, Metabase, and BI conventions for the data-analyst role

### Changed
- `business-analyst`: analytics handoff to Data Analyst, guardrails on unverified KPIs, optional Analytics Request template section

## [2.4.1] - 2026-05-22

### Added
- `data-analyst` role: business-facing metrics, SQL/tabular analysis, and `data-analysis-report.json`
- `analyze-data` foundation skill for analyst workflows

### Changed
- `data-engineer` role refocused on pipelines, ETL, migrations, and operational data platforms (analyst work moved to Data Analyst)

## [2.4.0] - 2026-05-22

### Added
- Schemas: `a2a-push-notification-config.json`, `a2a-task-cancel.json`, `agent-trace-span.json`; optional JWS `signature` on `agent-card.json`
- `validate-agent-cards.py`, `validate-standardization.py` (>=90% gate)
- Cursor adapter: `adapters/cursor/hooks.template.json`, `check-policy.py`, `log-trace-span.py`
- `core/policies/mcp-tool-map.yaml`, `core/prompts/golden/` sample dataset
- `capability-role-map.generated.yaml` from `generate-a2a-registry.py`

### Changed
- Wired `agent-prompt-lifecycle` and `agent-semantic-memory` to Coordinator, Technical Lead, SRE, Researcher
- QA role: `validation-result.json`, `agent-quality-gate`, `agent-observability`
- `CLAUDE.md`, `.cursor/rules/agent-skills.md`, Copilot instructions — A2A/Antigravity parity
- `validate-all.py` includes agent-card and standardization validators

## [2.3.0] - 2026-05-22

### Added
- Full **A2A 1.0** contracts: `agent-card.json`, `a2a-task-status.json`, `a2a-task-progress.json`, `a2a-message.json`, `a2a-jsonrpc-envelope.json`
- `agent-a2a-protocol` skill: discover, invoke, stream, get/list/cancel, scatter-gather
- **Antigravity adapter**: `adapters/antigravity/` (`ANTIGRAVITY.md`, `rules.template.md`, `a2a-config.template.yaml`)
- `core/a2a/` registry with `generate-a2a-registry.py` (21 role Agent Cards)
- Workflow `/agent-a2a-delegation`
- Validators: `validate-contracts.py`, `validate-a2a-compliance.py`

### Changed
- `a2a-task.json` / `a2a-artifact.json`: A2A lifecycle states, streaming, multimodal `parts`
- `agent-coordinator`: primary `agent-a2a-protocol`, registry discovery, progress/status contracts
- `AGENTS.md`: Antigravity + full A2A lifecycle requirements

## [2.2.0] - 2026-05-22

### Added
- `agent-graph-orchestration` skill: phase graphs, parallel groups, merge gates, and coordination-plan publishing
- `core/contracts/schemas/coordination-plan.json`: structured phase graph for Agent Coordinator
- `core/scripts/validate-2026-compliance.py`: validates A2A coverage, coordinator wiring, policy coverage, and policy hooks in tool orchestration

### Changed
- `agent-coordinator` role: primary `agent-delegation` and `agent-graph-orchestration`; A2A and JSON contract handoffs
- `project-manager`, `technical-writer`, `teacher` roles: Collaboration & A2A Delegation and contract references
- `agent-tool-orchestration` skill: Policy-as-Code checks for `action-boundaries.yaml` and `data-classification.yaml`
- `action-boundaries.yaml`: policy entries for all 21 delivery roles (was 9)
- `validate-all.py`: includes 2026 compliance validator

## [2.1.0] - 2026-05-13

### Fixed
- `core/scripts/common.py`: `parse_frontmatter` now supports YAML block scalars (`>`, `|`, `>-`, `|-`). Multi-line descriptions no longer trigger false "invalid frontmatter line" errors.
- `core/skills/security-data/data-engineer/SKILL.md`: restored multi-line description now that the parser handles it correctly.

### Added
- `overlays/vesviet-content/rules/content-brand.md`: populated with real voice/tone guidelines, style constraints (meta ≤ 160 chars, Production Failure template, code linting rules), and publishing constraints for Vesviet and Learn sites.
- `overlays/vesviet-content/workflows/publish-series.md`: end-to-end workflow for producing and publishing multi-part technical series across both Hugo sites. Covers planning, drafting, translation, review, and go-live steps.
- `core/contracts/schemas/series-article.json`: JSON Schema contract for series article output, validating frontmatter fields (date timezone, description length, weight ordering) and body structure (prerequisite block, production failure, CTA link).

### Changed
- `VERSION`: bumped from 2.0.0 to 2.1.0.

## [2.0.0] - 2026-05-09

### Added
- `core/contracts/` directory with JSON Schema output contracts for structured agent communication
  - `code-review-finding.json`, `implementation-result.json`, `validation-result.json`
  - `a2a-task.json`, `a2a-artifact.json` for Agent-to-Agent delegation
- `core/policies/` directory with machine-readable governance
  - `action-boundaries.yaml` defining role-based action permissions
  - `data-classification.yaml` defining sensitivity levels (public, internal, confidential, restricted)
- `agent-delegation` skill: A2A protocol-based task delegation between supervisor and worker agents
- `agent-semantic-memory` skill: persistent episodic and semantic memory across conversations
- `agent-observability` skill: session-level tracing, cost attribution, and virtuous evaluation cycle
- `agent-model-routing` skill: cost-aware model selection with tier-based routing strategies

### Changed
- `README.md`: added contracts and policies to Core Structure, expanded Agent Operations to 10 skills
- `core/skills/README.md`: updated Agent taxonomy from 6 to 10 skills
- Pack philosophy now reflects 8 core 2026 standards: Structured Outputs, A2A Protocol, Graph Orchestration, Layered Memory, Observability, Policy-as-Code, Model Routing, and Agentic Engineering Tiers

## [1.1.0] - 2026-05-09

### Added
- `agent-prompt-lifecycle` skill: full PromptOps pipeline with versioning, golden datasets, LLM-as-a-Judge evaluation, environment promotion, and drift detection

### Changed
- `agent-tool-orchestration`: added MCP (Model Context Protocol) section with discovery, contracts, auth, idempotency, and cost awareness guidance
- `agent-context-management`: added Context Engineering section covering dynamic context assembly, RAG validation, relevance filtering, context budgeting, and provenance tracking
- `agent-quality-gate`: added prompt evaluation as a quality gate for prompt asset changes
- `README.md`: updated pack philosophy to reflect 2026 Context Engineering and PromptOps standards
- `core/skills/README.md`: added `agent-prompt-lifecycle` to Agent taxonomy (now 6 agent skills)

## [1.0.0] - 2026-05-07

### Added
- Core pack with 35 skills across 7 taxonomy domains
- 19 principal-level delivery roles with skill toolbox enforcement
- 8 reusable workflows with role ownership per step
- 5 agent adapter files (Cursor, Claude Code, AGENTS, Copilot, OpenAI Codex)
- 5 Python validation scripts with adapter parity checking
- 3 overlays (vesviet-content, lease-content, ecommerce-microservices)
- 3 pack manifests (global-engineering, lease-team, vesviet-team)
- Adapter parity standard with automated checking
- OpenAI Codex skill adapters for all applicable skills
