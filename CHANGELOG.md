# Changelog

All notable changes to the agent-skills engineering pack.

## [3.3.1] - 2026-07-22

### Changed
- Hardened runtime policy hooks: approval-required operations now stop with a distinct non-zero status, denied operations remain blocked, and the bundled YAML fallback correctly reads nested policy mappings without PyYAML.
- Updated the Cursor hook configuration to use portable repository-relative commands and documented the blocking behavior.
- Corrected bundled JSON contract examples and extended contract validation to check example required fields and discriminators.
- Synced contract documentation with the current 40-schema inventory.

## [3.3.0] - 2026-07-22

### Added
- `agent-panel-meeting` skill (`core/skills/agent/agent-panel-meeting/SKILL.md`) for orchestrating 6-round multi-role cross-examination panel meetings for feature and architecture designs.

### Changed
- Standardized all 32 role definitions in `core/roles/` with 2026 guardrail LOCKs (`BOUNDARY LOCK`, `SECURITY LOCK`, `IRREVERSIBLE ACTION LOCK`, `TRACE LOCK`, `UNCERTAINTY LOCK`) and optimized skill toolbox token footprints.
- Updated policy boundaries in `core/policies/action-boundaries.yaml` to include complete policy definitions for `3d-graphics-engineer`.

## [3.2.0] - 2026-07-16

### Added
- `## When to Use` section (with concrete trigger bullets) to all 74 skills and roles that previously lacked it, improving execution consistency across the pack.
- Concrete code examples to 12 thin infrastructure/MMO skills (`aws-infrastructure`, `deploy-mmo-infrastructure`, `deploy-proxyware-fleet`, `create-automation-script`, `debug-runtime-platform`, `turnstile-spin`, `add-api-endpoint`, `setup-tracking-system`, `manage-mmo-assets`, `analyze-campaign-roi`, `generate-mmo-content`, `repurpose-content`).

## [3.1.0] - 2026-07-01

### Added
- `mmo-engineer` role to handle Performance Marketing and MMO automation.
- `manage-agent-identity` skill to manage NHI lifecycle, aligned with OWASP ASI03.
- `rotate_agent_credentials` action to `action-boundaries.yaml`.
- AP2 (Agent Payments Protocol) capability support to `agent-card.json`.
- OTel GenAI experimental observability guide (`otel-genai.md`).
- Missing `donthan-web` overlay README.

### Changed
- Expanded `role-standard.md` to cover all 10 OWASP ASI risks.
- Added MCP 2026-07-28 stateless migration steps to `configure-mcp` skill.
- Added `contract_type` discriminator to all 5 SEO schemas.

### Fixed
- Fixed trigger phrases, checklist requirements, and `playwright-stealth` references across 7 MMO skills.
- Fixed `mmo-engineer` decision boundaries and added to role inventory.

## [3.0.0] - 2026-06-22

### Changed
- **Major 2026 Standards Upgrade:** Upgraded all 85 skills across 9 clusters (Agent, Backend, Commerce, Documentation, Education, Foundation, Frontend, Platform, Security-Data) to 2026 industry standards.
- **Roles Upgrade:** Upgraded all 31 Agent Roles (Tech Lead, Tech Architect, Frontend Developer, UI/UX Designer, etc.) with new 2026 guardrails (e.g., `AI-PAIR-GOVERNANCE`, `AGENT-UX-LOCK`, `ZERO-TRUST-A2A`).
- **A2A Security:** Introduced strict Zero-Trust A2A communication rules and Confused Deputy Prevention (OWASP ASI03) to delegation skills.
- **Platform Enhancements:** Added support for Wrangler v4, Cloudflare Remote Bindings, and Durable Objects Actor Model patterns.
- **Data & Security:** Upgraded pgvector index maintenance (`CONCURRENTLY`) for Postgres 17 and added K8s debugging tools.

## [2.11.0] - 2026-06-17

### Added
- `seo-content-lifecycle` workflow: End-to-end topic plan, SEO brief, deep research, draft, audit, and publish lifecycle for content roles.

### Fixed
- `action-boundaries.yaml`: Added missing capability policies for `content-manager` and `solution-architect` roles.
- `agent-coordinator.md`: Fixed heading formatting to pass strict `validate-roles.py` checks.
- `validate-skills.py`: Updated `PLACEHOLDER_REFS` to allow backticked terms from `business-analyst.md`.

## [2.10.0] - 2026-06-16

### Added — Content Manager Role

- **`content-manager` role**: Principal-level role owning full website content strategy — content pillar architecture, editorial calendar, brand voice, content audit & lifecycle, performance measurement, content distribution & repurposing, and SME collaboration. Bridges business goals with daily content production.
- **A2A agent card** `content-manager.agent-card.json` registered in `core/a2a/.well-known/agent-registry.json`
- **Content Distribution & Repurposing** responsibility block: content loop design, repurposing matrix (long-form → social → email → video → newsletter), distribution gate guardrail (`DISTRIBUTION GATE`)
- **SME Collaboration & Thought Leadership** responsibility block: SME roster, structured interview process, YMYL review gate (`SME LOCK`), E-E-A-T experience signal enforcement
- **Product-led content** direction: `/tools`, `/templates`, `/glossary`, `/calculators` — coordinated with Frontend Developer and Product Manager
- New guardrails: `DISTRIBUTION GATE`, `SME LOCK`
- Distribution Plan and SME Roster tables in Output Template
- Review checklist groups: Distribution & Repurposing, SME & Thought Leadership
- New collaboration partners: Frontend Developer (interactive tools), Social Media Manager, Email Marketing Specialist, SMEs

### Changed — Roles & Registry

- **`core/roles/README.md`**: added `Content Strategy And Editorial` lifecycle section; `content-manager` registered in Release and Content And SEO lifecycle phases; workflow mapping table updated
- **`core/a2a/.well-known/agent-registry.json`**: `content-manager` entry added (alphabetical order, between `cloudflare-engineer` and `content-writer`)
- **`content-manager.md` Mission**: expanded from production-only scope to full lifecycle: sản xuất → phân phối → SME → AI search optimisation



### Added — E-commerce Engineer Role & Commerce Skill Taxonomy

- **`ecommerce-engineer` role**: Principal-level role owning the full e-commerce stack (catalog, checkout, payment, fulfillment) with 5 primary skills and commerce-specific LOCK guardrails (`PAYMENT-LOCK`, `PRICE-TRUST LOCK`, `IDEMPOTENCY LOCK`, `STATE-MACHINE LOCK`)
- **`integrate-payment-gateway` skill** (`commerce/`): Stripe, VNPay, PayPal, Momo integration with idempotency keys, webhook signature validation, and PCI-safe tokenization
- **`handle-checkout-flow` skill** (`commerce/`): End-to-end checkout funnel — cart, tax, shipping, coupon, payment, confirmation — with server-side price enforcement
- **`manage-product-catalog` skill** (`commerce/`): Product and variant data model, SKU uniqueness, atomic inventory operations, pricing versioning, multi-channel sync
- **`manage-order-fulfillment` skill** (`commerce/`): Order state machine, carrier label generation, tracking webhooks, return/refund flows
- New **Commerce** taxonomy in `core/skills/` (4 skills)
- `ecommerce-engineer` action boundary policy (`action-boundaries.yaml`) — `modify_payment_gateway_config` and `shipping_label_generation` require approval
- A2A agent card for `ecommerce-engineer` generated and registered in `core/a2a/.well-known/agent-registry.json`

### Changed — Core Rules & Skills Audit

- **`core/rules/code.md`**: Added mandatory `POLICY-AS-CODE` rule requiring all agents to verify against `action-boundaries.yaml` and `data-classification.yaml` before state-changing actions
- **`validate-rules.py`**: Added `policy_enforcement` parity group to enforce that all adapters reference both policy files
- **`.github/copilot-instructions.md`**: Added missing `data-classification.yaml` reference to pass policy parity check
- **`core/skills/security-data/data-engineer/`**: Removed deprecated redirect skill (zero remaining references confirmed); skill count updated accordingly
- **Education skills** (`create-exercises`, `design-learning-plan`, `grade-and-review`): Generalized from hardcoded Vietnamese MOET / THCS to portable global education standards (Bloom's Taxonomy, configurable grading scale, standard academic calendar). Vietnamese-specific conventions may be provided as context by the caller or via overlay.
- **`teacher` role**: Generalized to portable educator role (removed hardcoded MOET references); Output Template now in English with bilingual-friendly structure
- **`core/skills/README.md`**: Updated taxonomy counts, added Commerce section; counts now 76 core + 7 overlay = 83 total
- **`core/roles/README.md`**: Registered `ecommerce-engineer` in Architecture & Engineering, Implementation lifecycle, and Workflow mapping table
- **`overlays/sport-icm/`**: Restored missing directory and `rules/sport-project-rules.md` referenced by `packs/sport-team/manifest.yaml`
- **Root `README.md`**: Updated Overlay list (added `astro-cloudflare`, `data-analyst-stack`, `go-microservices`); fixed stale skill references (`manage-wrangler-deploy` → `wrangler`, `data-engineer` → `build-data-pipeline`); added Commerce domain to delivery domains table

### Validation — All Validators Green

- Rules: ✅ | Skills: ✅ 83 checked | Roles: ✅ 27 checked | Workflows: ✅ 16 checked
- Packs: ✅ 12 checked | Overlays: ✅ 15 checked | Contracts: ✅ 38 checked
- 2026 Compliance: ✅ 27 roles / 27 policies / graph + coordinator A2A wired
- A2A Full Compliance: ✅ | Agent Cards: ✅ 27 checked | Standardization: ✅ 100%

## [2.8.0] - 2026-06-05

### Changed — 2026 AI Governance & Standards Upgrade Wave

Systematic upgrade of **17 roles** to 2025–2026 industry standards. Each role received two new domain sections with concrete guardrails (LOCK rules), expanded review checklists, updated anti-patterns, and updated Definition of Done.

#### Universal Additions Across All Upgraded Roles
- **AI-generated code/artifact governance**: tiered trust validation proportional to risk (High: Auth/Payments/PII; Medium: Logic/Async; Low: Scaffolding)
- **Guardrail naming convention**: `LOCK` suffix on all hard-stop rules (e.g., `AI-CODE LOCK`, `HITL-SPEC LOCK`)
- **Probabilistic thinking**: requirements, SLOs, and acceptance criteria updated to accommodate non-deterministic AI system behavior
- **EU AI Act awareness**: risk tier classification embedded in relevant role outputs (BA ticket, Security review, Architecture ADR)

#### Role-by-Role Changes

**`role-standard.md`** — Added AI Governance universal layer (hard locks: `AI-CODE LOCK`, `OBSERVABILITY LOCK`); Fail-Safe Protocol section; Agent Governance Standards

**`agent-coordinator.md`** — Added Multi-Agent Governance (trust verification, blast-radius analysis before delegation, kill-switch); Progressive Delivery orchestration

**`content-writer.md`** — Added GEO/AEO (Generative Engine Optimization); E-E-A-T signal engineering; AI-assisted draft discipline; AI-Disclosure requirements

**`researcher.md`** — Added AI-Augmented Research Methodology (source triangulation, AI hallucination detection); Research Provenance standards; Epistemic Confidence framework

**`seo-analyst.md`** — Added GEO/AEO optimization layer; AI-native SERP features (SGE, featured snippets); semantic content clustering; entity-based SEO

**`technical-lead.md`** — Added Technical Debt Governance (quantified register, interest rate tracking); AI-Assisted Development Oversight (tiered code validation); Progressive Delivery (feature flags, canary releases)

**`technical-architect.md`** — Added AI/ML System Architecture patterns (RAG, agent orchestration, feature store, vector DB); Architecture Decision Record discipline with AI-specific risk tiers

**`qa-engineer.md`** — Added AI/LLM Testing Discipline (probabilistic AC, LLM-as-Judge, adversarial prompting, hallucination detection); Non-Deterministic Test Architecture (golden datasets, property-based testing)

**`product-manager.md`** — Added AI Product Stewardship (EU AI Act, XAI, HITL); Hypothesis-Driven Discovery (kill-early protocol); Outcome Metrics Framework

**`backend-developer.md`** — Added AI-Assisted Development Governance (tiered trust validation); Observability-First Engineering (OpenTelemetry universal standard, GenAI observability); `AI-CODE LOCK`, `OBSERVABILITY LOCK`, `LLM-INTEGRATION LOCK`, `PROMPT-INJECTION LOCK`

**`frontend-developer.md`** — Added AI-Generated UI Governance (tiered trust model, visual regression discipline); Performance-as-a-Product (INP-first CWV metrics, CI-enforced budgets, rendering strategy framework); `AI-UI LOCK`, `PERFORMANCE-BUDGET LOCK`, `RENDERING-STRATEGY LOCK`, `PERMISSION-BOUNDARY LOCK`

**`data-engineer.md`** — Added AI/ML Data Product Engineering (embedding pipelines, feature stores with training-serving parity, multimodal lakehouse, context engineering, training data quality gates); Data Contracts as Engineering Artifacts (machine-readable, version-controlled, CI/CD validated); `AI-PIPELINE LOCK`, `FEATURE-STORE LOCK`, `DATA-CONTRACT LOCK`, `TRAINING-DATA LOCK`

**`data-analyst.md`** — Added AI-Augmented Analysis (LLM-assisted SQL validation discipline, AI narrative validation, semantic layer alignment); Causal Reasoning Standards (mandatory correlation-causation disclosure, causal methods table, statistical vs. practical significance); `AI-SQL LOCK`, `AI-NARRATIVE LOCK`, `CAUSATION LOCK`, `SEMANTIC-LAYER LOCK`

**`business-analyst.md`** — Added AI Feature Requirements Specification (behavioral boundaries not deterministic outputs, probabilistic AC format, HITL escalation trigger specification, AI accountability model, EU AI Act tier in ticket); Assumption Mapping & Continuous Discovery (living assumption register with risk scoring, Event Storming, JTBD, Impact Mapping, kill-early signals); `AI-AC LOCK`, `HITL-SPEC LOCK`, `ASSUMPTION LOCK`, `EU-AI-ACT LOCK`; expanded Output Template with AI Feature Requirements section and Assumption Register table

**`ui-ux-designer.md`** — Added AI Interaction Design (5-state AI model: Generating/Uncertain/Fallback/Overridden/Corrected; confidence indicators; transparency hooks; human override patterns; Red Path design; HITL interface requirements; AI accessibility extensions beyond WCAG 2.2); Design System as Living Infrastructure (W3C DTCG three-tier token architecture; automated design-to-code pipeline; AI governance for design system); `AI-STATE LOCK`, `AI-OVERCONFIDENCE LOCK`, `TRUST-DESIGN LOCK`, `TOKEN-EXPORT LOCK`

**`devops-engineer.md`** — Added AI/ML Pipeline Governance (model promotion gates, shadow testing, canary rollout with model-specific rollback triggers, inference deployment safety, monitoring gates); GitOps-First Infrastructure & Supply Chain Security (SLSA framework, SBOM, dependency provenance, pinned CI action SHAs); `GITOPS LOCK`, `AI-DEPLOY LOCK`, `SUPPLY-CHAIN LOCK`

**`security-engineer.md`** — Added AI/LLM Security (prompt injection as OWASP LLM01 #1 attack vector, training data poisoning, model output exploitation, LLM-specific STRIDE threat model extensions, EU AI Act high-risk compliance sign-off); Shift-Left Security Engineering (threat modeling before design sign-off, SAST/DAST in CI, dependency and secret scanning gates); `PROMPT-INJECTION LOCK`, `AI-THREAT-MODEL LOCK`, `SHIFT-LEFT LOCK`

**`sre.md`** — Added AI/ML System Reliability (AI-specific SLO dimensions: output quality, inference latency, token cost, model availability, context window utilization; model degradation as P1 reliability incident; LLM-specific operational considerations); Proactive Reliability Engineering (error budget burn rate alerts, chaos engineering, game days, automated runbooks with dry-run mode); `AI-SLO LOCK`, `ERROR-BUDGET LOCK`

## [2.7.0] - 2026-06-02

### Added
- `build-data-pipeline` skill (replaces `data-engineer` skill to resolve naming collision)
- `mobile-engineer` role and corresponding action boundary policy
- `incident-report` and `release-notes` foundation skills
- 100% role compliance: `Role Boundaries` and `Deliverable Routing` added to 8 previously non-compliant roles
- `agents/openai.yaml` stubs added for all missing education and foundation skills

### Changed
- `data-engineer` skill deprecated (redirects to `build-data-pipeline`)
- Education skills (`create-exercises`, `design-learning-plan`, `grade-and-review`) expanded from Grade 6-7 to full Grade 6-9 range
- `setup-deployment`, `database-maintenance`, `add-service-client` skills hardened with extra safety and output format checks
- `write-article` broken overlay references replaced with generic guidance
- All 25 roles and 68 skills now fully compliant with validation scripts

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
