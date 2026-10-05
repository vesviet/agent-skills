# Engineering Agent Skills

Global engineering skill pack for multi-agent software delivery, platform architecture, and autonomous swarms.

> **Master Catalog**: **35 Roles** | **138 Skills** (126 Core + 12 Overlays) | **25 Workflows** | **54 Data Contract Schemas**  
> **Master Index & Router**: [`INDEX.md`](INDEX.md) | **Machine Registry**: [`core/a2a/.well-known/role-skill-index.json`](core/a2a/.well-known/role-skill-index.json)  
> **Engineering Baseline**: SOTA 2026–2027 Standards (Go 1.25+, Python 3.12+/3.13, React 19, Node 22/24 LTS, K8s 1.30+/1.31, vLLM v1 PagedAttention, OpenTofu v1.8+ KMS, Crossplane v1.16+, Bottlerocket, OWASP ASI, EU AI Act, PDPL 2025)  
> **Authoritative SOTA Audit**: [`reports/role-skill-matrix-sota-audit-2026-2027.md`](reports/role-skill-matrix-sota-audit-2026-2027.md)

**Version 5.0.0** (SOTA 2026–2027 Baseline) is a major engineering and architectural evolution. It standardizes multi-agent swarms under the A2A 1.0 JSON-RPC/SSE protocol, equips key roles with rigorous Architectural Guardrail Locks and dedicated multi-section review checklists, and integrates cutting-edge cloud-native and AI serving primitives:
- **AI Systems & LLM Serving**: Upgraded `ai-systems-engineer` with vLLM v1 PagedAttention, chunked prefill, prefix caching, K8s 1.31+ Dynamic Resource Allocation (DRA), NVIDIA MIG GPU slicing, DeepSeek-R1 SLM distillation, FastMCP, and LiteLLM spend governance; accompanied by the exclusive `deploy-vllm-inference` skill.
- **Cloud Infrastructure & AWS**: Upgraded `aws-engineer` with OpenTofu v1.8+ client-side state KMS encryption, Crossplane v1.16+ Go compositions, Bottlerocket distroless worker nodes, Graviton4 (`c8g`, `m8g`), Trainium2 / Inferentia2 accelerators, and Zero-Trust IAM Identity Center; and `devops-engineer` with Pillar 8 AWS Cloud-Native Delivery (EKS Pod Identity, Karpenter v1.0, VPC Lattice Gateway API) and the exclusive `deploy-aws-eks-workloads` skill.
- **Site Reliability & Resilience**: Upgraded `sre` with Multi-Window Multi-Burn-Rate (MWMBR) SLO alerting, eBPF Tetragon runtime telemetry, Toxiproxy chaos injection, and GenAI blameless RCA.
- **Product & Requirements Governance**: Upgraded `business-analyst` with Event Storming, Elephant Carpentry vertical slicing, BDD invariants, and EU AI Act / PDPL 2025 conformity.
- **Domain Accounting & Legal**: Hardened `vietnam-accounting-specialist` (VAS 14, Circular 200/99, Balanced Ledger $\sum \text{Debits} \equiv \sum \text{Credits}$) and `vietnam-legal-counsel` (PDPL 2025, AI Law 134/2025/QH15).
- **Core Governance & Fail-Closed Policies**: Added `## Failure Modes` and `## Output Contracts` sections to all skills and roles, `## Security Guardrails (OWASP ASI)` for security-critical actions, fail-closed `action-boundaries.yaml`, and 17 automated core validators.

Version 4.0.0 was a corrective release from a full-pack audit. It fixed external-standard claims (WCAG 2.2 criterion numbering, x402 v2 header names, ACP discovery paths, A2A event and signing details, MCP baseline revision), resolved role ownership contradictions, and restored strict commit gates across all workflows.

Version 3.4.0 refreshed the pack to 2026 standards — the MCP 2026-07-28 stateless spec with AAIF (Linux Foundation) governance, corrected EU AI Act timeline, agentic commerce protocol landscape (ACP, UCP, MPP, x402, AP2), first-party on-device LLM frameworks, and the European Accessibility Act.

The repository is organized into a portable **core** plus optional **overlays** so global engineering teams can reuse the foundation without inheriting repo-specific or brand-specific assumptions.

As of 2026–2027, the core pack reflects the industry shift from ad-hoc prompting to **Context Engineering**, **PromptOps**, and **Autonomous Multi-Agent Swarms**: prompts are treated as versioned, testable assets; tool integration follows the **Model Context Protocol (MCP)** standard; and agent outputs validate against formal JSON Schema contracts.

## Repository Layout

- `core/`: portable source of truth for rules, roles, skills, workflows, validators, and helper config
- `overlays/`: optional extensions for specific repos, brands, or domains
- `packs/`: assembly manifests that describe which core plus overlays belong in a packaged distribution
- root adapter files: entrypoints for Codex, Cursor, Claude Code, AGENTS-compatible tools, and Copilot

Start with [core/README.md](core/README.md) if you want the reusable foundation.
See [overlays/README.md](overlays/README.md) if you need repo-specific extensions.
See [packs/README.md](packs/README.md) for composition and distribution.

**Antigravity IDE:** [adapters/antigravity/ANTIGRAVITY.md](adapters/antigravity/ANTIGRAVITY.md)

## Core Structure

- [core/rules](core/rules/README.md): always-on global rules
- [core/roles](core/roles/README.md): reusable software delivery role definitions
- [core/skills](core/skills/README.md): taxonomy-organized skills for delivery work
- [core/workflows](core/workflows/README.md): longer end-to-end operating procedures
- [core/contracts](core/contracts/README.md): JSON Schema output contracts for structured agent communication
- [core/policies](core/policies/README.md): machine-readable action boundaries and data classification
- [core/scripts](core/scripts/README.md): validation utilities for pack maintenance
- [core/config](core/config/README.md): optional environment helpers

## Overlay Structure

Current overlays:

- `vesviet-content`: content-writing helpers for Vesviet and Learn Hugo sites
- `lease-content`: content-writing helpers for Lease in Vietnam Astro content trees
- `maylanhtreotuong-content`: HVAC engineering, empirical testing, and content/SEO conventions for May Lanh Treo Tuong Astro site
- `ecommerce-microservices`: reserved for service-level or platform-specific conventions
- `astro-cloudflare`: Astro v5 on Cloudflare Pages/Workers conventions
- `data-analyst-stack`: DuckDB + Metabase + Excel/BI workflow conventions
- `go-microservices`: Go service and gRPC conventions
- `data-warehouse`: omnichannel retail conventions (DuckDB Single-Writer, MISA AMIS, VAS 14, PWA stocktake) with the `learning/` data-engineering track
- `donthan-web`: web content/SEO helpers for Don Than site
- `golf-icm`: Golf catalog conventions for the ICM Cloudflare site
- `icm-main`: ICM Factory main site conventions
- `laravel-filament`: Laravel + Filament admin conventions
- `maydiengiaisaigon`: content/SEO helpers for May Dien Gia Sai Gon
- `obj-configurator`: OBJ product configurator conventions
- `r3f-stack`: React Three Fiber / Three.js (WebGL) skills cluster — `debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets` (migrated v4.0.0)
- `seo-publishing`: SEO publishing cadence and board conventions
- `sport-icm`: Sport catalog conventions for the ICM Cloudflare site
- `ui-design-system`: shared UI/design-system conventions

Overlay-specific skills are intentionally kept out of the global core inventory.

## Core Skill Highlights

### Agent Operations

| Skill | What it covers |
|-------|----------------|
| [agent-context-management](core/skills/agent/agent-context-management/SKILL.md) | Preserve intent, evidence, assumptions, continuity, and dynamic context assembly |
| [agent-a2a-protocol](core/skills/agent/agent-a2a-protocol/SKILL.md) | Full A2A 1.0 lifecycle, JSON-RPC, streaming, Antigravity registry |
| [agent-delegation](core/skills/agent/agent-delegation/SKILL.md) | Delegate scoped sub-tasks to specialist agents via A2A protocol |
| [agent-graph-orchestration](core/skills/agent/agent-graph-orchestration/SKILL.md) | Phase graphs, parallel branches, merge gates, and coordination-plan.json |
| [agent-memory-compaction](core/skills/agent/agent-memory-compaction/SKILL.md) | Compact long conversations into a minimal working state |
| [agent-model-routing](core/skills/agent/agent-model-routing/SKILL.md) | Select cost-effective models per task based on complexity and risk tier |
| [agent-observability](core/skills/agent/agent-observability/SKILL.md) | Trace reasoning chains, tool calls, and token costs for debugging and eval |
| [agent-prompt-lifecycle](core/skills/agent/agent-prompt-lifecycle/SKILL.md) | Version, evaluate, and monitor prompt assets through PromptOps pipeline |
| [agent-semantic-memory](core/skills/agent/agent-semantic-memory/SKILL.md) | Persist and retrieve codebase patterns and past fixes across conversations |
| [agent-tool-orchestration](core/skills/agent/agent-tool-orchestration/SKILL.md) | Choose, sequence, and validate tool use safely with MCP awareness |
| [agent-quality-gate](core/skills/agent/agent-quality-gate/SKILL.md) | Run validators, lints, tests, builds, and diff checks |
| [agent-handoff](core/skills/agent/agent-handoff/SKILL.md) | Summarize state, validation, blockers, and next actions |
| [agent-panel-meeting](core/skills/agent/agent-panel-meeting/SKILL.md) | Orchestrate 6-round multi-role cross-examination panel meetings |


### Foundation

| Skill | What it covers |
|-------|----------------|
| [create-migration](core/skills/foundation/create-migration/SKILL.md) | Add safe schema migrations |
| [performance-profiling](core/skills/foundation/performance-profiling/SKILL.md) | Profile hot paths and regressions |
| [write-tests](core/skills/foundation/write-tests/SKILL.md) | Add or improve unit and integration tests |
| [conduct-research](core/skills/foundation/conduct-research/SKILL.md) | Deep or scoped research before decisions |
| [design-review](core/skills/foundation/design-review/SKILL.md) | UX/spec design critique before build |
| [accessibility-review](core/skills/foundation/accessibility-review/SKILL.md) | WCAG-oriented a11y audit |

### Repo Ops

| Skill | What it covers |
|-------|----------------|
| [commit-code](core/skills/repo-ops/commit-code/SKILL.md) | Pre-commit validation and commit flow |
| [navigate-service](core/skills/repo-ops/navigate-service/SKILL.md) | Understand an unfamiliar service quickly |
| [review-code](core/skills/repo-ops/review-code/SKILL.md) | Review code changes with prioritized findings |
| [review-service](core/skills/repo-ops/review-service/SKILL.md) | Full service readiness and release review |
| [troubleshoot-service](core/skills/repo-ops/troubleshoot-service/SKILL.md) | Diagnose build, startup, and runtime failures |

### Meetings And Analysis

| Skill | What it covers |
|-------|----------------|
| [meeting-review](core/skills/meetings-analysis/meeting-review/SKILL.md) | Structured multi-angle technical review |
| [analyze-business-requirements](core/skills/meetings-analysis/analyze-business-requirements/SKILL.md) | Convert requests into feature tickets |
| [analyze-data](core/skills/meetings-analysis/analyze-data/SKILL.md) | Ad-hoc metrics and stakeholder reports |

### Content

| Skill | What it covers |
|-------|----------------|
| [write-article](core/skills/content/write-article/SKILL.md) | Draft long-form articles with GEO/AEO and E-E-A-T gates |
| [audit-content](core/skills/content/audit-content/SKILL.md) | Content refresh cycle: audit, read, research latest standards, update, re-audit |
| [optimize-seo](core/skills/content/optimize-seo/SKILL.md) | Intent, keywords, on-page, GEO/AEO specifications |
| [repurpose-content](core/skills/content/repurpose-content/SKILL.md) | Syndicate and reshape articles across channels |

### Delivery Domains

| Domain | Representative skills |
|--------|-----------------------|
| AI | `deploy-vllm-inference`, `build-mcp-server`, `setup-llm-gateway`, `setup-gpu-finops` |
| Backend | `add-api-endpoint`, `add-event-handler`, `add-service-client`, `scaffold-new-service` |
| Frontend | `add-ui-component`, `add-page-route`, `integrate-api-client`, `frontend-testing` |
| R3F / 3D (overlay) | `debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets` — under `overlays/r3f-stack/` |
| Platform | `deploy-aws-eks-workloads`, `aws-infrastructure`, `setup-deployment`, `wrangler`, `debug-runtime-platform`, `add-telemetry-instrumentation` |
| Commerce | `integrate-payment-gateway`, `handle-checkout-flow`, `manage-product-catalog`, `manage-order-fulfillment` |
| Security and Data | `manage-secrets`, `database-maintenance`, `security-audit`, `build-data-pipeline`, `manage-vietnam-accounting` |
| Documentation | `write-documentation`, `write-tech-radar` |

Full inventory: [core/skills/README.md](core/skills/README.md)

## Workflows

Core workflows live in [core/workflows/README.md](core/workflows/README.md).

- `/add-new-feature`
- `/feature-delivery`
- `/bug-fix`
- `/code-review`
- `/build-deploy`
- `/hotfix-production`
- `/revert-deployment`
- `/refactoring`
- `/service-review-release`
- `/setup-new-service`
- `/troubleshooting`
- `/agent-a2a-delegation`
- `/content-publishing`
- `/content-audit`
- `/data-migration`
- `/data-pipeline-incident`
- `/dependency-upgrade`
- `/qa-validation`
- `/security-incident-response`
- `/seo-content-lifecycle`
- `/seo-keyword-brief`
- `/tech-repo-review`
- `/period-end-closing`
- `/curriculum-delivery`
- `/mmo-campaign-lifecycle`

## Quality Gates & Verification

Run these validators after editing core rules, skills, roles, or workflows (includes 2026–2027 compliance):

```bash
python3 core/scripts/validate-all.py
```

`validate-all.py` runs all **17 core validators** (rules, skills, roles, workflows, packs, overlays, 2026/2027 compliance, contracts, A2A, agent cards, standardization, version sync, indexes, policies, skill ownership, contract coverage, golden prompt evals).

Individual gates when iterating:

```bash
python3 core/scripts/validate-rules.py
python3 core/scripts/validate-skills.py
python3 core/scripts/validate-roles.py
python3 core/scripts/validate-workflows.py
python3 core/scripts/validate-version-sync.py        # VERSION vs registry, cards, adapters
python3 core/scripts/validate-indexes.py             # index coverage and declared counts
python3 core/scripts/validate-policy-consistency.py  # action-boundaries vs roles
python3 core/scripts/validate-skill-ownership.py     # Primary owners and workflow reachability
```

After editing `core/roles/` or bumping `VERSION`, regenerate the A2A registry and master index:

```bash
python3 core/scripts/generate-a2a-registry.py
python3 core/scripts/generate-index.py
python3 core/scripts/generate-index.py --check       # verify zero index drift
```

### Empirical Challenge Test Suites

The repository enforces strict continuous verification through dedicated challenge test suites in `tests/` (>530 tests, 100% pass):

- `tests/test_ai_systems_engineer_platform_challenge.py`: vLLM v1, K8s DRA, MIG slicing, SLM distillation, and guardrails
- `tests/test_aws_engineer_platform_challenge.py`: OpenTofu v1.8+ KMS, Crossplane Go compositions, Bottlerocket, and IAM zero-trust
- `tests/test_devops_engineer_platform_challenge.py`: Pillar 8 EKS Pod Identity, Karpenter v1.0, VPC Lattice Gateway API
- `tests/test_sre_reliability_challenge.py`: Multi-window burn-rate alerts, Tetragon telemetry, and chaos engineering
- `tests/test_business_analyst_requirements_challenge.py`: Event Storming, BDD invariants, and EU AI Act / PDPL compliance
- `tests/test_data_analyst_decision_science_challenge.py`: DuckDB analytics, Text-to-SQL hallucination guard, and SRM checks
- `tests/test_data_engineer_lakehouse_challenge.py`: Apache Iceberg REST catalog, WAP pattern, and OpenLineage
- `tests/test_qa_engineer_verification_challenge.py`: G-Eval scoring, PactV3 contract tests, Tracetest OTel spans
- `tests/test_m2_accounting_challenge.py`: Balanced ledger invariants, VAS 14, Circular 200/99, and MISA AMIS
- `tests/test_vietnam_legal_pack_challenge.py`: PDPL 2025 Decree 356, AI Law 134/2025, and statutory parity

## Agent Compatibility

This pack includes adapter files for all major AI coding agents:

| Agent | Adapter File | Auto-Loads |
|-------|-------------|------------|
| Google Antigravity | `adapters/antigravity/ANTIGRAVITY.md` + `adapters/antigravity/role-skill-index.json` | Full A2A 1.0, role & skill fast-resolution (`@role`, `@skill`), structured JSON contracts |
| OpenAI Codex | `AGENTS.md` + `core/codex/` (README + `.a2a-config.json`) + `core/skills/*/*/agents/openai.yaml` | Rules via AGENTS.md; skills via `$skill-name` |
| Cursor | `.cursorrules` + `.cursor/rules/agent-skills.md` | Rules, roles, skills, workflows |
| Claude Code | `CLAUDE.md` | Rules, roles, skills, workflows |
| Kiro | `.kiro/steering/agent-skills.md` (always-on) + `.kiro/hooks/*.json` | Rules via steering; policy/role/trace hooks |
| Kilo Code | `AGENTS.md` + `.kilocode/rules/agent-skills.md` | Rules, roles, skills, workflows |
| VS Code (Copilot) | `.github/copilot-instructions.md` + `AGENTS.md` (+ MCP via `.vscode/mcp.json`) | Rules and pack navigation |
| AGENTS-compatible tools (Windsurf, etc.) | `AGENTS.md` | Rules, roles, skills, workflows |

`AGENTS.md` is the shared open standard read natively by Codex, Cursor, Kilo Code, Windsurf, and VS Code Copilot. All adapters point back to the same source of truth in `core/`.

## Installation

### Option 1: Clone Into Your Project

```bash
git submodule add <repo-url> agent-skills
```

### Option 2: Use Only The Core Pack

Install or reference only:

- `core/rules`
- `core/roles`
- `core/skills`
- `core/workflows`
- the root adapter file(s) your agent requires

### Option 3: Compose A Pack

Use a manifest from `packs/` to combine the core with one or more overlays for a specific team or repository.

## Scope

The core pack is intended to remain broadly reusable across stacks and repositories.

Repo-specific content, absolute paths, brand voice, and org-local conventions belong in overlays rather than the global core.

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-01
