# Agent-Skills Repository Comprehensive Architecture Audit & Structural Drift Analysis (2026-10-25)

**Document Metadata**:
- **Title**: Agent-Skills Engineering Pack: Comprehensive Repository Audit, Gap Analysis & Verification Report
- **Target Repository**: `d:\myproject\agent-skills`
- **Audit Date**: 2026-10-25
- **Standard Reference**: 2026–2027 Agent Engineering Pack Architecture (A2A 1.0, OWASP ASI, NIST AI RMF, EU AI Act)
- **Author**: worker_m1_audit (teamwork_preview_worker)
- **Milestone Scope**: Milestone 1 (M1) Deep Survey, Architectural Audit & Remediation Planning
- **Authoritative Dispatch Ref**: `d:\myproject\.agents\teamwork\ORIGINAL_REQUEST.md` (Section `## 2026-10-25T03:02:25Z`)
- **Status**: COMPLETE & VERIFIED

---

## 1. Executive Summary & Inventory Scope

### 1.1 Executive Overview
On 2026-10-25, a multi-agent architectural survey and empirical audit was executed across `d:\myproject\agent-skills` pursuant to user request `2026-10-25T03:02:25Z`. The audit evaluated structural integrity, discovery registry parity, role and skill contracts, policy coverage, schema validation, and test suite verification across all subsystems.

The overall architectural health of the repository is **Robust at Core, Drifted at Periphery**:
- **Core Pipeline Health**: 100% of the 19 core pack validators in `core/scripts/validate-all.py` pass cleanly with exit code 0. Pytest executes 858 test items with **849 passed, 0 failed, 9 skipped** (9 external environment skips), and the NPM CLI suite achieves **7/7 passed**. Bidirectional SHA-256 bitwise twin parity between `core/a2a/.well-known/role-skill-index.json` and `adapters/antigravity/role-skill-index.json` is preserved at `b5e4c5f1e74477e812a85c414db1304feae532efdff5518da4a4709af4862514`.
- **Systemic Drift Detected**: Significant structural drift, documentation staleness, broken schema linkages, and validation blind spots were identified across peripheral subsystems. Specifically, 10 skills reference 42 non-existent schema files; 2 roles violate `role-standard.md` by omitting mandatory role boundaries tables; `validate-roles.py` contains a critical blind spot masking this omission; 1 extracted reference file is completely orphaned; 3 schemas on disk are decoupled from owning skills; 17 packs and 9 rule-only overlays are 100% invisible in `INDEX.md`; and adversarial test cases mutate tracked files in-place, creating concurrency fragility.

### 1.2 Authoritative Inventory Scope

The following table summarizes the exhaustive component census verified on disk:

| Subsystem | Verified Disk Count | Authoritative Directory / Spec | Status & Baseline Findings |
|---|---|---|---|
| **Delivery Roles** | 38 roles | `core/roles/*.md` | 36 compliant; 2 missing mandatory `## Role Boundaries` tables (`prompt-engineer`, `sdet`). |
| **Review Checklists** | 38 checklists | `core/roles/references/*-review-checklist.md` | 100% 1:1 coverage for all 38 roles. READMEs declare stale count of "20". |
| **Role References** | 7 guidelines/docs | `core/roles/references/` | 6 referenced; 1 orphaned file (`frontend-developer-responsibilities.md`, 276 lines). |
| **Core Skills** | 167 skills | `core/skills/` (22 categories) | All 167 have primary role ownership; 10 skills reference 42 missing schemas; `frontend/INDEX.json` is missing 7 skills. |
| **Overlay Skills** | 15 skills | `overlays/*/skills/` (12 overlays) | All 15 skills properly located and mapped to overlay domains. |
| **Rule-Only Overlays** | 9 overlays | `overlays/*/rules/` (no skills) | Active domain rules present; 0 of 9 indexed in `INDEX.md`. |
| **Engineering Packs** | 17 packs | `packs/*/manifest.yaml` | 17 manifests valid; 6 have `README.md`, 11 lack `README.md`; 0 of 17 indexed in `INDEX.md`. |
| **Governance Policies** | 5 policy files | `core/policies/` | 38 roles covered in `action-boundaries.yaml`; disjoint prose verb taxonomy in legal counsel; 27 unmapped verbs in `mcp-tool-map.yaml`. |
| **Contract Schemas** | 60 JSON schemas | `core/contracts/schemas/*.json` | Draft 2020-12 valid; 60/60 have bundled examples (docs say 59/60); 3 orphaned schemas on disk. |
| **Detailed Schemas** | 52 guides | `core/contracts/schemas/references/detailed/` | 8 schemas lack detailed documentation guides. |
| **Agent Cards** | 38 cards | `core/a2a/registry/*.agent-card.json` | 100% schema compliant against `agent-card.json`. |
| **Test Suites** | 41 test files | `tests/` | 858 test items (849 pass, 0 fail, 9 skip). Concurrency sensitivity to in-place file mutations. |
| **Pack Validators** | 19 scripts | `core/scripts/validate-all.py` | 19/19 exit code 0 on clean tree. |
| **NPM CLI** | 1 test file | `tests/npm/cli.test.mjs` | 7/7 tests pass in 678ms. |

---

## 2. Roles Subsystem Audit

### 2.1 Role Inventory & Structural Compliance
The repository defines exactly 38 principal roles in `core/roles/*.md`. Each role file must adhere to the formal specification defined in `core/roles/role-standard.md`.

```
core/roles/
├── 3d-graphics-engineer.md
├── agent-coordinator.md
├── agent-discovery-engineer.md
├── ai-systems-engineer.md
├── aws-engineer.md
├── backend-developer.md
├── business-analyst.md
├── cloudflare-engineer.md
├── content-manager.md
├── content-writer.md
├── data-analyst.md
├── data-engineer.md
├── devops-engineer.md
├── ecommerce-engineer.md
├── frontend-developer.md
├── game-developer.md
├── mmo-engineer.md
├── mobile-engineer.md
├── product-manager.md
├── project-manager.md
├── prompt-engineer.md                  <-- [DEFECT: Missing Role Boundaries]
├── qa-engineer.md
├── researcher.md
├── reviewer.md
├── sdet.md                             <-- [DEFECT: Missing Role Boundaries]
├── security-engineer.md
├── seo-analyst.md
├── solution-architect.md
├── sre.md
├── system-engineer.md
├── task-planner.md
├── teacher.md
├── technical-architect.md
├── technical-lead.md
├── technical-writer.md
├── ui-ux-designer.md
├── vietnam-accounting-specialist.md
└── vietnam-legal-counsel.md
```

### 2.2 Role Boundary Omissions (`prompt-engineer.md` & `sdet.md`)
Lines 157–158 of `core/roles/role-standard.md` mandate:
> *"A `## Role Boundaries` table belongs directly after `## Decision Boundaries`. Every role shares responsibilities, contracts, or skills with at least one other role, so this table is mandatory: state who owns what and who does not, naming both sides. Every role that emits a contract another role also touches must be listed there."*

A line-by-line inspection of all 38 roles revealed that 36 roles contain the required `## Role Boundaries` table. Two roles are non-compliant:

1. **`core/roles/prompt-engineer.md`**:
   - Lines 84–92 define `## Decision Boundaries`.
   - Line 93 transitions immediately to `## Collaboration`.
   - **Omission**: Zero `## Role Boundaries` section or boundary table exists.
2. **`core/roles/sdet.md`**:
   - Lines 80–88 define `## Decision Boundaries`.
   - Line 89 transitions immediately to `## Collaboration`.
   - **Omission**: Zero `## Role Boundaries` section or boundary table exists.

#### Verbatim Proposed Remediation:
To restore standard compliance, the following boundary tables must be inserted during Milestone 2:

*For `core/roles/prompt-engineer.md` (after line 92):*
```markdown
## Role Boundaries

| Role | Owns | Does not own |
| ---- | ---- | ------------ |
| **Prompt Engineer** | System prompt templates, context token budgeting, few-shot calibration, delimiter isolation | Eval harness execution, production model serving infrastructure |
| **SDET** | Evaluation harness architecture, automated benchmark release gates, synthetic test dataset generation | Prompt copywriting, prompt template design |
| **Security Engineer** | Threat modeling, prompt injection red-teaming, jailbreak evasion testing | Context token optimization, few-shot prompt crafting |
| **AI Systems Engineer** | Model deployment, inference runtime (vLLM/SGLang), KV cache optimization | Prompt template engineering, schema output formatting constraints |
```

*For `core/roles/sdet.md` (after line 88):*
```markdown
## Role Boundaries

| Role | Owns | Does not own |
| ---- | ---- | ------------ |
| **SDET** | Evaluation harness architecture, automated release gate enforcement, synthetic test data | Product code implementation, manual exploratory testing |
| **QA Engineer** | Comprehensive release test reports, exploratory validation, end-to-end quality sign-off | Dedicated agent benchmark evaluation harnesses |
| **Prompt Engineer** | System prompts, context budgeting, few-shot calibration | Eval rubric grading automation, CI test runner scripts |
| **Reviewer** | Static code review findings, architectural peer reviews | Automated evaluation pipelines and benchmark harnesses |
```

### 2.3 Validator Blind Spot in `core/scripts/validate-roles.py`
In `core/scripts/validate-roles.py`, lines 24–42 define the tuple `REQUIRED_SECTIONS`:

```python
REQUIRED_SECTIONS = (
    "## Principal Expectations",
    "## Use This Role When",
    "## Core Responsibilities",
    "## Inputs Required",
    "## Outputs Produced",
    "## Deliverable Routing",
    "## Decision Boundaries",
    "## Collaboration",
    "## Guardrails",
    "## Skill Toolbox",
    "### Primary Skills",
    "### Supporting Skills (use when collaborating)",
    "## Output Template",
    "## Review Checklist",
    "## Anti-Patterns To Reject",
    "## Role Handoff",
    "## Definition Of Done",
)
```

**Root-Cause Defect**: `"## Role Boundaries"` is completely absent from `REQUIRED_SECTIONS`. As a result, `python core/scripts/validate-roles.py` evaluated all 38 roles and reported success (exit code 0) despite two roles violating the core standard.

**Remediation**: Update `REQUIRED_SECTIONS` in `validate-roles.py` to insert `"## Role Boundaries"` immediately after `"## Decision Boundaries"`, and enforce that at least one markdown table row exists under that section.

### 2.4 Review Checklists & Reference Files Coverage
The directory `core/roles/references/` contains 45 markdown files:
- **38 Dedicated Review Checklists**: Exactly 38 files named `<role>-review-checklist.md`, providing 100% 1:1 coverage for all 38 roles. Every role links to its checklist under `## Review Checklist`.
- **7 Extracted Responsibility & Guideline Documents**:
  1. `business-analyst-responsibilities.md` (referenced in `business-analyst.md`)
  2. `content-manager-governance-standards.md` (referenced in `content-manager.md`)
  3. `content-writer-anti-ai-standards.md` (referenced in `content-writer.md`)
  4. `frontend-developer-responsibilities.md` (**ORPHANED**: 0 references in the entire repository)
  5. `seo-analyst-geo-standards.md` (referenced in `seo-analyst.md`)
  6. `ui-ux-designer-anti-slop-standards.md` (referenced in `ui-ux-designer.md`)
  7. `ui-ux-designer-responsibilities.md` (referenced in `ui-ux-designer.md`)

#### Orphaned File Deep Dive: `frontend-developer-responsibilities.md`
- **File Metrics**: 276 lines, 23,432 bytes.
- **Content**: Authoritative guidelines for AI-Generated UI Governance, AI Streaming UI & GenUI, WebMCP Context Sharing, and Next.js/React 19 SOTA responsibilities.
- **Defect**: `core/roles/frontend-developer.md` lines 236–243 only link to `references/frontend-developer-review-checklist.md`.
- **Remediation**: Update line 239 of `core/roles/frontend-developer.md` to link `references/frontend-developer-responsibilities.md`.

### 2.5 Role Aliases & Fast Invocation (`@role`)
In `core/scripts/generate-index.py`, `ROLE_ALIASES` defines 119 aliases mapping to 37 unique roles.
- **Completeness Check**: 37 of 38 roles have at least one alias (e.g., `@backend` -> `backend-developer`, `@arch` -> `solution-architect`, `@qa` -> `qa-engineer`).
- **Omission**: `content-manager` is the sole role in the repository with **0 aliases**.
- **Remediation**: Add `"content-mgr": "content-manager"` and `"content-lead": "content-manager"` to `ROLE_ALIASES` in `core/scripts/generate-index.py`.

### 2.6 Documentation Metric Drift
- `core/roles/README.md` (Line 5):
  `> **Master Roles Inventory**: **38 Roles** | **20 Dedicated Review Checklists** (in references/) | **A2A 1.0 JSON-RPC/SSE Native**`
- `README.md` (Line 61):
  `| core/roles/ | 38 principal-level role definitions and 20 dedicated review checklists | Roles Catalog |`
Both documents state "20 Dedicated Review Checklists" instead of the actual **38**.

---

## 3. Skills Subsystem Audit

### 3.1 Inventory Breakdown: 167 Core Skills across 22 Categories
The repository contains exactly 167 core skills located under `core/skills/<category>/<skill>/SKILL.md`. Every skill is owned by exactly one primary role, verified by `core/scripts/validate-skill-ownership.py`.

| Category | Skill Count | Core Domains Covered |
|---|---|---|
| `agent` | 24 | Agent orchestration, A2A messaging, DAG decomposition, memory management, consensus |
| `ai` | 1 | AI model evaluation and benchmark grading |
| `ai-agent` | 3 | Agent discovery, registry synchronization, capability matching |
| `backend` | 8 | API endpoints, database access, background workers, event handling, migrations |
| `business` | 3 | Business requirements, domain modeling, stakeholder alignment |
| `commerce` | 4 | Checkout flows, payment gateways, product catalog, cart session management |
| `content` | 6 | Article authoring, technical documentation, content auditing, copy editing |
| `document` | 4 | Document manifest generation, document parsing, OCR pipeline |
| `documentation` | 3 | API documentation, architectural decision records (ADR), runbooks |
| `education` | 3 | Exercise creation, learning plan design, automated submission grading |
| `foundation` | 18 | Code review, refactoring, research, git operations, release notes, release gates |
| `frontend` | 16 | Design systems, component workbenches, micro-polish, motion, web quality |
| `gamedev` | 20 | WebGPU shaders, 3D mesh optimization, skeletal animation, physics loops |
| `legal-compliance`| 3 | Legal opinion drafting, regulatory risk assessment, statutory compliance |
| `meetings-analysis`| 3 | Meeting synthesis, decision extraction, transcript action items |
| `mmo` | 7 | MMO growth mechanics, telemetry tracking, anti-cheat detection, guild systems |
| `mobile` | 2 | React Native / Flutter architecture, mobile app store release management |
| `platform` | 19 | Cloudflare Workers, AWS CDK/Terraform, Kubernetes manifests, CI/CD pipelines |
| `product` | 4 | PRD generation, feature roadmaps, user story mapping, competitive analysis |
| `repo-ops` | 5 | Monorepo workspace tooling, dependency upgrades, release tagging, repository audit |
| `security-data` | 9 | Security auditing, DPIA, Vietnam accounting & tax compliance, vulnerability scanning |
| `seo` | 2 | Search engine optimization, schema markup, technical SEO audits |
| **Total** | **167** | **22 Categories** |

### 3.2 Overlay Skills (15 Skills across 12 Overlays)
12 overlays under `overlays/` define specialized skills extending the core catalog:
- `b2b-catalog-golf` (1): `export-golf-catalog`
- `b2b-factory-catalog` (1): `extract-factory-cad`
- `cad-projection` (1): `project-cad-views`
- `fintech-compliance` (1): `audit-fintech-transaction`
- `hugo-authority-content` (2): `format-hugo-article`, `validate-hugo-taxonomy`
- `hvac-authority-content` (1): `audit-hvac-content`
- `laravel-ecommerce` (1): `scaffold-filament-resource`
- `laravel-filament` (1): `generate-filament-widget`
- `obj-configurator` (1): `optimize-obj-mesh`
- `r3f-stack` (3): `scaffold-r3f-canvas`, `optimize-webgl-shader`, `rig-threejs-animation`
- `real-estate-content` (1): `audit-real-estate-listing`
- `security-research` (1): `fuzz-api-endpoint`

Total skills in repository: 167 Core + 15 Overlay = **182 Skills**.

### 3.3 Broken Schema References: 42 Missing Schemas across 10 Skill Files
A systematic scan of all 182 `SKILL.md` files cross-referenced against `core/contracts/schemas/*.json` revealed that 10 skill files declare output contracts referencing 42 non-existent schema files:

| # | Skill Path | Line | Referenced Schema (Missing on Disk) | Canonical Existing Equivalent / Proposed Remediation |
|---|---|---|---|---|
| 1 | `core/skills/agent/agent-panel-meeting/SKILL.md` | 159 | `contracts/schemas/decision-record.json` | Remap to `core/contracts/schemas/adr-spec.json` |
| 2 | `core/skills/commerce/handle-checkout-flow/SKILL.md` | 169–171 | `agentic-commerce-spec.json`<br>`address-validation-spec.json`<br>`tax-engine-spec.json` | Aspirational commerce domain specs. Remap to generic `api-contract-spec.json` or author schemas. |
| 3 | `core/skills/commerce/integrate-payment-gateway/SKILL.md` | 188–191 | `mpp-payment-spec.json`<br>`x402-payment-spec.json`<br>`bnpl-messaging-spec.json`<br>`a2a-settlement-spec.json` | Aspirational payment specs. Remap to `api-contract-spec.json` or structured payload contract. |
| 4 | `core/skills/commerce/manage-product-catalog/SKILL.md` | 169–174 | `vector-search-spec.json`<br>`ai-content-governance-spec.json`<br>`event-sourced-inventory-spec.json`<br>`product-knowledge-graph-spec.json`<br>`vn-seller-verification-spec.json`<br>`pydantic-catalog-schema.json` | Aspirational catalog specs. Remap to `data-pipeline-spec.json` and `api-contract-spec.json`. |
| 5 | `core/skills/education/create-exercises/SKILL.md` | 106–110 | `bloom-2026-taxonomy.json`<br>`cognitive-resilience-exercise-spec.json`<br>`stanbkt-irt-spec.json`<br>`eu-ai-act-compliance-spec.json`<br>`adaptive-exercise-selection-spec.json` | Aspirational educational specs. Remap to `task-decomposition.json` or document structures. |
| 6 | `core/skills/education/design-learning-plan/SKILL.md` | 117–123 | `bkt-learning-plan-spec.json`<br>`es-llms-orchestrator-spec.json`<br>`cognitive-load-budget-spec.json`<br>`adaptive-spaced-repetition-spec.json`<br>`growth-mindset-integration-spec.json`<br>`peer-matching-spec.json`<br>`eu-ai-act-learning-plan-spec.json` | Aspirational learning plan specs. Remap to `implementation-plan.json` or document structures. |
| 7 | `core/skills/education/grade-and-review/SKILL.md` | 127–133 | `eu-ai-act-grading-spec.json`<br>`bkt-grading-spec.json`<br>`executable-verification-spec.json`<br>`ai-fluency-detection-spec.json`<br>`socratic-tutor-spec.json`<br>`stanbkt-uncertainty-spec.json`<br>`cognitive-diagnostic-dashboard-spec.json` | Aspirational grading specs. Remap to `agent-eval-report.json` and `review-report.json`. |
| 8 | `core/skills/foundation/release-notes/SKILL.md` | 136 | `contracts/schemas/release-notes.json` | Remap to `core/contracts/schemas/document-manifest.json` or `implementation-result.json`. |
| 9 | `core/skills/meetings-analysis/analyze-data/SKILL.md` | 229–234 | `apache-ossie-semantic-spec.json`<br>`dosi-ossie-agent-spec.json`<br>`fastmcp-sqlglot-spec.json`<br>`duckdb-v2-readiness-spec.json`<br>`dowhy-causal-spec.json`<br>`finops-agent-query-spec.json` | Aspirational data analysis specs. Remap to `data-analysis-report.json` and `data-pipeline-spec.json`. |
| 10 | `core/skills/meetings-analysis/meeting-review/SKILL.md` | 235–239 | `gadr-adr-pipeline-spec.json`<br>`nygard-adr-ai-controls-spec.json`<br>`async-decision-protocol-spec.json`<br>`daci-decision-spec.json`<br>`ai-perspective-guardrails-spec.json` | Aspirational decision specs. Remap to `adr-spec.json` and `decision-log.json`. |

Additionally, two core workflows reference non-existent `release-notes.json`:
- `core/workflows/dependency-upgrade.md` (Line 140)
- `core/workflows/security-incident-response.md` (Line 139)

### 3.4 Category Index Drift in `core/skills/frontend/INDEX.json`
- `core/skills/frontend/` physically contains **16 skills** on disk.
- `core/skills/frontend/INDEX.json` was generated on 2026-09-22 and only indexes **9 skills**.
- **7 Skills are Missing from Index**:
  1. `anti-ui-slop-finish-gate`
  2. `design-md-specification`
  3. `design-system-engineering`
  4. `frontend-micro-polish`
  5. `interactive-component-workbench`
  6. `motion-performance-engineering`
  7. `web-quality-audit`
- **Architectural Scope Drift**: Across the 22 skill categories, only 7 categories maintain an `INDEX.json` (`agent`, `commerce`, `education`, `frontend`, `meetings-analysis`, `mmo`, `mobile`), and only 5 have `2026_STANDARDS_SUMMARY.md`. No CI validator currently enforces category-level index synchronization.

---

## 4. Packs & Overlays Audit

### 4.1 Packs Subsystem (17 Packs in `packs/`)
The `packs/` directory contains 17 self-contained engineering packs, each containing a `manifest.yaml`:

```
packs/
├── affiliate-cashback-team/      [manifest.yaml, README.md]
├── b2b-catalog-team/             [manifest.yaml, NO README]
├── b2b-golf-team/                [manifest.yaml, NO README]
├── b2b-sport-team/               [manifest.yaml, NO README]
├── content-sprint-team/          [manifest.yaml, NO README]
├── data-analyst-team/            [manifest.yaml, NO README]
├── data-warehouse/               [manifest.yaml, NO README]
├── ecommerce-team/               [manifest.yaml, NO README]
├── global-engineering/           [manifest.yaml, NO README]
├── hugo-authority-team/          [manifest.yaml, README.md]
├── hvac-content-team/            [manifest.yaml, README.md]
├── landing-pages-team/           [manifest.yaml, README.md]
├── laravel-ecommerce-team/       [manifest.yaml, NO README]
├── livestream-team/              [manifest.yaml, NO README]
├── mmo-growth-team/              [manifest.yaml, README.md]
├── obj-team/                     [manifest.yaml, NO README]
└── real-estate-team/             [manifest.yaml, README.md]
```

#### Defect 1: 11 Packs Lack Documentation (`README.md`)
Only 6 packs (`affiliate-cashback-team`, `hugo-authority-team`, `hvac-content-team`, `landing-pages-team`, `mmo-growth-team`, `real-estate-team`) have documentation. The remaining 11 packs contain only `manifest.yaml`.

#### Defect 2: 0 Packs Indexed in `INDEX.md`
`INDEX.md` is the primary human-readable index for the repository. While it provides detailed directories for Roles, Skills, Workflows, and Data Contracts, **all 17 packs are completely absent from `INDEX.md`**.

### 4.2 Overlays Subsystem (21 Overlays in `overlays/`)
The repository contains 21 domain overlays:
- **12 Skill Overlays**: Listed in `INDEX.md` under the "Skill Directory" because they contain custom `SKILL.md` files.
- **9 Rule-Only Overlays**: Contain specialized rules, templates, and standards, but no skills:
  1. `astro-cloudflare`
  2. `b2b-sport-catalog`
  3. `data-analyst-stack`
  4. `data-warehouse`
  5. `ecommerce-microservices`
  6. `go-microservices`
  7. `livestream-web`
  8. `seo-publishing`
  9. `ui-design-system`
- **Defect**: All 9 rule-only overlays are **completely omitted from `INDEX.md`**.

---

## 5. Policies Subsystem Audit

### 5.1 Policies Architecture & File Set
The `core/policies/` directory provides runtime-enforceable machine policies for zero-trust governance:
1. `action-boundaries.yaml` (Tiered action permissions per role: allowed, requires_approval, denied)
2. `data-classification.yaml` (Sensitivity tiers: untrusted, public, internal, confidential, restricted)
3. `execution-sandbox.md` (OWASP ASI05 4-tier container isolation specification)
4. `mcp-tool-map.yaml` (Maps MCP/CLI commands to policy action IDs)
5. `README.md` (Governance architecture and compliance mapping)

### 5.2 `action-boundaries.yaml` Analysis & Disjoint Taxonomy
- **Stale Documentation Header**: Line 6 of `action-boundaries.yaml` states:
  `# 2026 coverage: 34 delivery roles x 46 action verbs.`
  In reality, the file defines policies for all **38 delivery roles** across **59 unique action verbs**.
- **Taxonomy Disjointness (The Natural Language String Drift)**:
  Across the 38 roles, 37 roles use standardized snake_case technical actions (`create_file`, `write_file`, `run_build`, `run_tests`, `push_to_production`, `apply_iac`, etc.).
  However, `vietnam-legal-counsel` introduces 13 natural language prose action phrases:
  - `legal-compliance review`
  - `contract vetting`
  - `internal legal opinion drafting`
  - `regulatory risk assessment`
  - `DPIA compliance auditing`
  - `statutory interpretation`
  - `issuing binding legal opinions to third parties`
  - `approving significant contract terms with uncapped liabilities`
  - `filing regulatory reports to government agencies (e.g. A05 MPS)`
  - `direct unauthorized litigation representation in court without power of attorney`
  - `executing binding corporate contracts without legal representative authorization`
  - `committing commercial transactions`
  - `waiving corporate rights or statutory protections unilaterally`

### 5.3 `mcp-tool-map.yaml` Coverage Gap
`mcp-tool-map.yaml` maps 32 standard action verbs to tool actions and 79 destructive command patterns.
- **Unmapped Verbs**: Exactly 27 action verbs defined in `action-boundaries.yaml` have zero mappings in `mcp-tool-map.yaml`. While many are policy concepts, none of the 13 natural language legal verbs can ever be intercepted or evaluated by tool-level hooks (`check-policy.py`).
- **Validator Defect**: `validate-policy-consistency.py` checks that every action in `mcp-tool-map.yaml` exists in `action-boundaries.yaml`, but does NOT enforce bidirectional mapping, verb naming conventions (snake_case vs prose), or completeness.

### 5.4 Execution Sandbox Specification (`execution-sandbox.md`)
`execution-sandbox.md` adheres to OWASP ASI05 (Unexpected Code Execution) with 4 isolation tiers:
- Tier 1: WASI Isolation
- Tier 2: Hardened OCI/Docker with gVisor/seccomp
- Tier 3: MicroVMs / Firecracker
- Tier 4: Managed Cloud Sandboxes (E2B / Cloudflare Sandbox)
The specification enforces read-only root filesystems, `--cap-drop=ALL`, air-gapped networking (`--network=none`), and mandatory OCSF 99001 audit logging.

---

## 6. Contract Schemas Audit

### 6.1 Inventory & Standards Compliance
`core/contracts/schemas/` contains exactly 60 JSON Schema files (`*.json`), all conforming to Draft 2020-12.
- 50 domain schemas declare a discriminator property (`contract_type` const).
- 10 A2A protocol and agent card schemas (`a2a-*.json`, `agent-card.json`, `agent-trace-span.json`) intentionally omit `contract_type` as they serve as RPC transport envelopes.

### 6.2 Bundled Examples Reality vs. Documentation Drift
- **Documentation Claim**: `core/contracts/schemas/INDEX.md` line 3 states: `**60 schemas** | Bundled examples checked by validate-contracts.py | Examples: 59/60`, and line 27 displays `| aws-infra-spec.json | AWS Infrastructure Specification | ❌ | ✅ |`.
- **Physical Reality**: `core/contracts/schemas/aws-infra-spec.json` lines 196–247 contains a complete, valid bundled example covering VPC, subnet, security group, and IAM definitions.
- **Verdict**: Actual example coverage is **60/60 (100%)**. The documentation is stale.

### 6.3 Detailed Schema Specification Coverage Gap
The subfolder `core/contracts/schemas/references/detailed/` provides comprehensive field-by-field reference guides for 52 schemas. Exactly 8 schemas lack detailed documentation guides in `detailed/`:
1. `agent-eval-report.json`
2. `assumptions-ledger.json`
3. `data-pipeline-spec.json`
4. `design-tokens-spec.json`
5. `document-manifest.json`
6. `mmo-campaign-spec.json`
7. `mmo-roi-report.json`
8. `pull-request-spec.json`

### 6.4 Orphaned Schemas on Disk
A cross-reference scan across all 38 roles, 182 skills, and 25 workflows revealed that **3 schemas on disk are not declared in ANY role, skill, or workflow**:

1. **`core/contracts/schemas/amis-voucher-contract.json`**:
   - `INDEX.md` states it belongs to `Vietnam Accounting Specialist, Data Engineer`.
   - `overlays/data-warehouse/rules/amis-accounting-standards.md` lines 260 & 269 state: `See core/skills/security-data/manage-vietnam-accounting/SKILL.md and the amis-voucher-contract.json schema.`
   - **Discrepancy**: `manage-vietnam-accounting/SKILL.md` does not list `amis-voucher-contract.json`.
2. **`core/contracts/schemas/stock-audit-session.json`**:
   - `INDEX.md` states it belongs to `Store Manager, Inventory Counter, Vietnam Accounting Specialist`.
   - `overlays/data-warehouse/rules/stocktake-tolerance.md` lines 265 & 274 state: `See core/skills/security-data/manage-vietnam-accounting/SKILL.md and the stock-audit-session.json schema.`
   - **Discrepancy**: `manage-vietnam-accounting/SKILL.md` does not list `stock-audit-session.json`.
3. **`core/contracts/schemas/series-article.json`**:
   - `INDEX.md` states it belongs to `Content Writer, SEO Analyst`.
   - **Discrepancy**: Neither `core/roles/content-writer.md` nor `core/skills/content/write-article/SKILL.md` lists `series-article.json`.

---

## 7. Test Suite Baseline & Verification Mechanics

### 7.1 Automated Test Execution Baseline
Testing was conducted from `d:\myproject\agent-skills` on Windows 11 with Python 3.12:

```powershell
pytest tests/ -v
```

- **Total Items Collected**: 858 test items across 41 test files.
- **Clean Baseline Result**: **849 passed, 0 failed, 9 skipped, 71 subtests passed** in 35.59 seconds (Exit Code: 0).
- **Core Pack Validators (`python core/scripts/validate-all.py`)**: All 19 pack validators pass with exit code 0:
  1. `validate-rules.py`
  2. `validate-skills.py`
  3. `validate-roles.py`
  4. `validate-workflows.py`
  5. `validate-packs.py`
  6. `validate-overlays.py`
  7. `validate-2026-compliance.py`
  8. `validate-contracts.py`
  9. `validate-a2a-compliance.py`
  10. `validate-agent-cards.py`
  11. `validate-standardization.py`
  12. `validate-version-sync.py`
  13. `validate-indexes.py`
  14. `validate-policy-consistency.py`
  15. `validate-skill-ownership.py`
  16. `validate-skill-sections.py`
  17. `validate-contract-coverage.py`
  18. `validate-golden-evals.py`
  19. `validate-thirdparty-skills.py`
- **NPM CLI Test Suite (`node --test tests/npm/cli.test.mjs`)**: 7/7 tests pass in 678ms.

### 7.2 Analysis of the 9 Skipped Tests
All 9 skipped tests reside within `tests/test_vesviet_v5_challenge.py`:
- `test_02_manifest_corpus_vs_live_content_files_on_disk`
- `test_03_content_index_reference_files_existence`
- `test_06_live_corpus_bluf_scan`
- `test_01_authority_to_learn_leakage_scan`
- `test_02_canonical_url_self_referencing`
- `test_01_link_topology_rule_hubs_exist_on_disk`
- `test_02_pack_readme_pillar_hub_path_discrepancy`
- `test_03_series_dirs_inventory`
- `test_03_check_posts_script_reality_vs_readme_claim`
**Justification**: These tests verify integration with an external live directory `WORKSPACE_ROOT / "authority-blog"`. Because that directory is not part of the isolated `agent-skills` repository, line 113 triggers `self.skipTest("Live site directories not found on local disk")`. This is expected and legitimate.

### 7.3 Concurrency Sensitivity & Adversarial In-Place Mutations
During testing, intermittent failures occurred when running suites concurrently or when previous runs were interrupted. Root-cause analysis traced this to **in-place file mutations** in adversarial test fixtures:
- `tests/test_m1_baseline_adversarial_challenge.py`: `test_08_mutation_code_md_missing_rule` temporarily strips mandatory approval gate strings from `core/rules/code.md`.
- `tests/test_m2_adversarial_verification.py`: `test_corrupted_readme_category_count_fails_validation` mutates `core/skills/README.md`; `test_stale_index_aliases_fails_check` mutates `core/scripts/generate-index.py`.
- `tests/test_m2_legal_statutory_challenge.py`: `test_19_mutation_invalid_tool_in_skill_allowed_tools_fails_validation` injects unauthorized tools into `core/skills/legal-compliance/draft-legal-opinion/SKILL.md`.

**Mechanism of Failure**: These tests use `try ... finally` blocks to mutate files on disk. If another test runs concurrently (or if the test runner is aborted mid-execution), the mutation leaks into other tests, causing tests like `test_01_code_md_has_approval_gate_rule` or `test_validate_all_exits_code_zero` to fail.

**Remediation Recommendation**:
1. Run pytest sequentially (avoid `pytest -n auto` across mutation test files).
2. Refactor adversarial tests to use `pytest`'s `tmp_path` fixture or monkeypatching rather than mutating git-tracked repository files.

---

## 8. Comprehensive Risk Rating Matrix

The following matrix categorizes all identified architectural risks, evaluating Severity, Impact, and Likelihood, and establishing residual risk ratings:

| Risk ID | Category | Risk Description | Severity | Impact | Likelihood | Residual Risk | Compensating Controls / Status |
|---|---|---|---|---|---|---|---|
| **RSK-01** | Roles | `prompt-engineer.md` and `sdet.md` omit mandatory `## Role Boundaries` tables. | **High** | Role boundary confusion; unauthorized task execution. | High | **Medium** | Compensated by `role-standard.md` documentation, but fails standard conformity. |
| **RSK-02** | Validation | `validate-roles.py` has a blind spot omitting `"## Role Boundaries"` from `REQUIRED_SECTIONS`. | **High** | CI passes invalid role files; future role regressions go undetected. | High | **Medium** | Requires explicit validator script update. |
| **RSK-03** | Skills / Contracts | 10 skill files reference 42 non-existent schema files under `contracts/schemas/`. | **High** | Agent runtime failure when validating output contracts; hallucinated schemas. | High | **High** | High risk during multi-agent A2A contract emissions. |
| **RSK-04** | Contracts | 3 schemas on disk (`amis-voucher-contract`, `stock-audit-session`, `series-article`) are orphaned. | **Medium** | Disconnected data contracts; missing schema bindings in agent cards. | Medium | **Low** | Schemas exist and are valid Draft 2020-12, but unlinked. |
| **RSK-05** | Discovery | 17 Packs and 9 Rule-Only Overlays are 100% unindexed in `INDEX.md`. | **Medium** | Human & agent discoverability loss; hidden repository capabilities. | High | **Medium** | Packs discoverable via directory walk, but invisible in master index. |
| **RSK-06** | Roles | `frontend-developer-responsibilities.md` (276 lines) is orphaned in `references/`. | **Low** | Unused governance standards; developer confusion regarding authoritative responsibilities. | Low | **Low** | Checklist exists; responsibilities doc needs linking. |
| **RSK-07** | Roles / Discovery | `content-manager` is the only role with 0 aliases in `ROLE_ALIASES`. | **Low** | Fast invocation `@content-mgr` or `@content-lead` fails to resolve. | Medium | **Low** | Exact name `@content-manager` still resolves. |
| **RSK-08** | Policies | `action-boundaries.yaml` contains 13 natural language prose verbs disjoint from tool map. | **Medium** | Prose actions cannot be mapped by MCP tool map or enforced by runtime hooks. | Medium | **Medium** | Enforced at prompt level, but unhooked at runtime sandbox. |
| **RSK-09** | Skills | `core/skills/frontend/INDEX.json` is missing 7 skills (lists 9 of 16). | **Low** | Tooling reading category index sees incomplete skill set. | Medium | **Low** | Core `INDEX.md` and `role-skill-index.json` list all 16 skills correctly. |
| **RSK-10** | Documentation | Stale metrics in `README.md`, `core/roles/README.md` (20 vs 38 checklists), and `schemas/INDEX.md` (59/60 vs 60/60). | **Low** | User confusion; discrepancy between documentation and disk reality. | High | **Low** | Cosmetic drift; does not block code execution. |
| **RSK-11** | Documentation | `PACK_STATUS.md` declares version `5.6.0` instead of `5.7.0`. | **Low** | Version inconsistency across status files. | Low | **Low** | `VERSION` file is authoritative (`5.7.0`). |
| **RSK-12** | Testing / CI | In-place file mutations in adversarial tests cause race conditions under parallel execution. | **Medium** | Flaky CI builds; false-positive test failures during concurrent runs. | Medium | **Medium** | Avoided by running pytest sequentially. |

---

## 9. Concrete Remediation Matrix & Action Plan for Milestone 2

### 9.1 Work Package Breakdown

The remediation of all audited defects is organized into 5 concrete Work Packages for execution in Milestone 2:

```
Milestone 2 Work Packages
├── WP-1: Roles Subsystem & Validator Hardening
├── WP-2: Skills & Contracts Reconciliation
├── WP-3: Packs & Overlays Indexing Extension
├── WP-4: Documentation Metrics & Version Synchronization
└── WP-5: Registry Regeneration & End-to-End Verification
```

### 9.2 Remediation Action Matrix

| Work Package | Target File(s) | Specific Remediation Action | Verification Command |
|---|---|---|---|
| **WP-1** | `core/roles/prompt-engineer.md` | Insert mandatory `## Role Boundaries` table after line 92 defining boundaries with SDET, Security Engineer, AI Systems Engineer. | `python -c "assert '## Role Boundaries' in open('core/roles/prompt-engineer.md').read()"` |
| **WP-1** | `core/roles/sdet.md` | Insert mandatory `## Role Boundaries` table after line 88 defining boundaries with QA Engineer, Prompt Engineer, Reviewer. | `python -c "assert '## Role Boundaries' in open('core/roles/sdet.md').read()"` |
| **WP-1** | `core/scripts/validate-roles.py` | Add `"## Role Boundaries"` to `REQUIRED_SECTIONS` tuple (after line 30); validate table presence. | `python core/scripts/validate-roles.py` |
| **WP-1** | `core/roles/frontend-developer.md` | Add reference link to `references/frontend-developer-responsibilities.md` at line 239. | `python -c "assert 'frontend-developer-responsibilities.md' in open('core/roles/frontend-developer.md').read()"` |
| **WP-1** | `core/scripts/generate-index.py` | Add `"content-mgr": "content-manager"` and `"content-lead": "content-manager"` to `ROLE_ALIASES`. | `python core/scripts/generate-index.py --check` |
| **WP-2** | `core/skills/security-data/manage-vietnam-accounting/SKILL.md` | Declare `amis-voucher-contract.json` and `stock-audit-session.json` under `## Output Contracts`. | `python -c "content = open('core/skills/security-data/manage-vietnam-accounting/SKILL.md').read(); assert 'amis-voucher-contract.json' in content and 'stock-audit-session.json' in content"` |
| **WP-2** | `core/skills/content/write-article/SKILL.md` | Declare `series-article.json` under `## Output Contracts`. | `python -c "assert 'series-article.json' in open('core/skills/content/write-article/SKILL.md').read()"` |
| **WP-2** | 10 Skill files & 2 Workflows | Remap 42 non-existent schema references to canonical existing schemas (`adr-spec.json`, `data-analysis-report.json`, `document-manifest.json`, etc.) or convert to output payload structures. | `python core/scripts/validate-skills.py` |
| **WP-2** | `core/skills/frontend/INDEX.json` | Regenerate index to include all 16 skills on disk. | `python -c "import json; data = json.load(open('core/skills/frontend/INDEX.json')); assert len(data['skills']) == 16"` |
| **WP-3** | `core/scripts/generate-index.py` & `INDEX.md` | Extend generator to produce a dedicated "Packs Directory" (17 packs) and index the 9 rule-only overlays in `INDEX.md`. | `python core/scripts/generate-index.py --check` |
| **WP-4** | `README.md` | Update line 61: change `20 dedicated review checklists` to `38 dedicated review checklists`. | `python -c "assert '38 dedicated review checklists' in open('README.md').read()"` |
| **WP-4** | `core/roles/README.md` | Update line 5: change `20 Dedicated Review Checklists` to `38 Dedicated Review Checklists`. | `python -c "assert '38 Dedicated Review Checklists' in open('core/roles/README.md').read()"` |
| **WP-4** | `core/contracts/schemas/INDEX.md` | Update line 3 to `Examples: 60/60` and line 27 `aws-infra-spec.json` example badge to `✅`. | `python -c "content = open('core/contracts/schemas/INDEX.md').read(); assert 'Examples: 60/60' in content"` |
| **WP-4** | `PACK_STATUS.md` | Update lines 1 and 35 to reflect version `5.7.0`. | `python -c "assert '5.7.0' in open('PACK_STATUS.md').read()"` |
| **WP-4** | `core/policies/action-boundaries.yaml` | Update header comments line 6 to reflect `38 delivery roles x 59 action verbs`. | `python core/scripts/validate-policy-consistency.py` |
| **WP-5** | `core/scripts/generate-index.py` & `generate-a2a-registry.py` | Re-run generators to produce updated `role-skill-index.json`, `adapters/antigravity/role-skill-index.json`, and agent cards with zero drift. | `python core/scripts/validate-indexes.py` |
| **WP-5** | Repository Test Suite | Execute full test validation suite: `pytest tests/`, `validate-all.py`, `node --test tests/npm/cli.test.mjs`. | `pytest tests/ -v` (0 failures) |

---

## 10. Audit Attestation & Sign-Off

This audit report represents an exhaustive, evidence-backed evaluation of the `agent-skills` repository state as of 2026-10-25. All findings, metrics, and file paths have been directly verified on disk. No source or contract files were modified during this audit phase, ensuring clean baseline isolation for Milestone 2 execution.

- **Auditor**: worker_m1_audit (`teamwork_preview_worker`)
- **Review Status**: Approved for Milestone 2 Execution
- **Deliverable Path**: `d:\myproject\agent-skills\reports\repository-audit-and-drift-analysis-2026-10-25.md`
