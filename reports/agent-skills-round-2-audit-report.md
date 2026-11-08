# Round 2 Forensic Audit & Deep Research Report: Agent Skills Ecosystem (v5.8.0)

**Repository**: `agent-skills`  
**Pack Version**: `v5.8.0`  
**Git HEAD**: `c8b3640`  
**Audit Date**: 2026-11-08  
**Auditor**: Senior Fullstack & Forensic Audit Engineering Team (`m1_worker_report`)  
**Target Path**: `reports/agent-skills-round-2-audit-report.md`  
**Classification**: Authoritative Engineering Baseline & SOTA Strategic Roadmap  

---

## 1. Executive Summary & Comparison with Round 1 Baseline

### 1.1 Scope & Context
This report establishes the definitive Round 2 Forensic Audit and Deep Research assessment for the `agent-skills` repository at version **5.8.0** (`c8b3640`). Following the preliminary Round 1 assessment (which awarded a provisional `🟢 A-` grade based on static file counts, schema validation, and surface linter execution), this second-round audit applies adversarial forensic analysis across the entire codebase.

The investigation evaluates four core dimensions:
1. **Asset Depth & The 104 Un-Expanded Skills**: A deep structural taxonomy of all 183 skills (169 core, 14 overlays), asset distribution, domain vulnerabilities, role reliance exposure, and concrete defect discoveries.
2. **Golden Evaluation & Dynamic Model Reasoning**: Coverage across all 39 engineering roles and 25 SOP workflows, analyzing the dangerous gap between 100% static CI passing rates and actual model behavioral alignment under production edge cases.
3. **Test Suite Robustness & Content Quality Regression**: Deconstruction of the 924 collected test cases, revealing extreme role bias (65.8% of tests test roles, while 84.7% of skills are never read from disk), superficial line-count assertions, and blind spots across the 22 validation scripts.
4. **Repository Packaging & Knowledge Hygiene**: An audit of publishing boundaries, npm tarball whitelist invariants (832 files, 2.30 MB), untracked publishing manifests (`.npmignore`), and an active rule violation in `reports/` where 18 research dossiers (1.9 MB) violate the 5-file root threshold mandated by `core/rules/knowledge.md`.

---

### 1.2 Comparative Scorecard: Round 1 Baseline vs. Round 2 Forensic Audit

| Evaluation Dimension | Round 1 Baseline (Provisional) | Round 2 Forensic Audit (Empirical) | Forensic Delta & Critical Finding |
|:---|:---:|:---:|:---|
| **Overall Ecosystem Grade** | `🟢 A-` (Ready to ship) | `🟡 B+` (Production-Hardened with Gaps) | Static checks mask deep behavioral and asset-layer deficiencies. |
| **Cataloged Skills Inventory** | 169 Core + 14 Overlay (183) | 169 Core + 14 Overlay (183) | Census confirmed; taxonomy revealed 118 total un-expanded skills. |
| **Skill Asset Depth** | "104 of 169 lack assets (~61%)" | **104 Core (61.5%) + 14 Overlay (100%) = 118 Un-expanded** | 37 pure standalone, 67 pseudo-expanded; **only 3 skills (1.6%)** have worked examples. |
| **Role Evaluation Coverage** | "Golden evals cover 5 assets" | **5 of 39 roles (12.8%) full eval; 34 roles (87.2%) zero eval** | 20 of 39 roles (51.3%) have $> 50\%$ un-expanded primary skills (23 of 39 or 59.0% have $\ge 50\%$); 9 roles 100% un-expanded. |
| **Workflow Dynamic Coverage** | Not evaluated | **0 of 25 workflows (0.0%) dynamically evaluated** | Zero golden traces; zero state-machine contract handoff tests. |
| **Test Suite Composition** | 915 passed, 9 skipped | **924 collected tests (65.8% role challenge, 0% skill behavior)** | **54.1% of skills never named**; **84.7% of skills never read from disk** by tests. |
| **Validator Suite Health** | 100% Pass (23 validators) | 100% Pass (23 validators, ~2.5s) | Confirmed, but uncovered semantic blind spots in `validate-packs.py` and `validate-overlays.py`. |
| **Packaging & Repository Hygiene** | "reports/ is 1.9 MB" | **Direct violation of `knowledge.md` ($\le 5$ root files)** | 18 unorganized files in `reports/` root; untracked `.npmignore`; npm excludes reports via `package.json`. |
| **Runtime Defects Discovered** | 8 description strings | **2 Critical Runtime Defects + 11 Orphaned Upgrade Plans** | Phantom scripts in `document/pdf`; hardcoded Windows path in `ai/openrouter-task`. |

---

### 1.3 Key Forensic Discoveries (Executive Callout)

> 🚨 **CRITICAL FINDINGS SUMMARY**:
> 1. **Phantom Script Invocations**: `core/skills/document/pdf/SKILL.md` instructs agents to execute `check_fillable_fields.py` and `fill_fillable_fields.py`. Neither script exists in the repository, guaranteeing fatal runtime crashes (`FileNotFoundError`).
> 2. **Non-Portable Windows Hardcoding**: `core/skills/ai/openrouter-task/SKILL.md` hardcodes `D:\myproject\.agents\.env` and `python D:\myproject\tools\openrouter_worker.py` across 4 separate lines, breaking POSIX environments and multi-platform agent execution.
> 3. **The "Example Desert"**: While 65 skills claim standard asset status, 57 of them contain only text reference notes (`references/`). Only **3 skills in the entire repository** provide concrete, worked code examples (`examples/`). 98.4% of skills lack canonical implementation code.
> 4. **The False Confidence of 100% CI**: 924 passing tests test markdown headers, lock strings, and JSON schemas. Zero tests verify that an LLM following these prompts produces compliant code, handles edge cases, or adheres to negative constraints.
> 5. **Knowledge Hygiene Rule Violation**: `reports/` contains 18 markdown dossiers (1.9 MB) at its root, directly violating `core/rules/knowledge.md` (which strictly caps root files at $\le 5$).

---

## 2. Track 1: Forensic Audit of the 104 Un-Expanded Skills

### 2.1 Complete Skill Inventory & Taxonomy
The repository catalogs **183 skills** across two primary physical locations:
- **Core Skills**: 169 skills distributed across 22 domain categories in `core/skills/`.
- **Overlay Skills**: 14 skills distributed across 21 stack overlay directories in `overlays/`.

A deterministic filesystem inspection evaluating standard supporting assets (`references/`, `examples/`, `scripts/`) establishes the ground truth:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TOTAL SKILLS CATALOGED: 183                                           │
├────────────────────────────────────────────────────────────────────────┤
│ Core Skills (169):                                                     │
│   ├── Expanded with Standard Assets:   65 skills (38.5%)               │
│   └── Un-Expanded Skills:             104 skills (61.5%)               │
│                                                                        │
│ Overlay Skills (14):                                                   │
│   ├── Expanded with Standard Assets:    0 skills (0.0%)                │
│   └── Un-Expanded Skills:              14 skills (100.0%)              │
│                                                                        │
│ Total Repository-Wide Un-Expanded:   118 skills (64.5%)               │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 2.2 Structural Taxonomy of the 104 Un-Expanded Core Skills
A microscopic review of the 104 un-expanded core skill directories reveals that they do not share a uniform file layout. They divide into two distinct structural archetypes:

```
                     ┌──────────────────────────────────────────────┐
                     │     104 Un-Expanded Core Skills Archetype     │
                     └──────────────────────┬───────────────────────┘
                                            │
                 ┌──────────────────────────┴──────────────────────────┐
                 ▼                                                     ▼
    Pure Standalone (37 Skills)                          Pseudo-Expanded (67 Skills)
    - Strictly SKILL.md                                  Contains non-standard metadata:
    - 0 subdirectories                                   - 56 skills: `agents/openai.yaml` only
    - 0 supplementary files                              - 11 skills: `UPGRADE_PLAN_2026.md` +
                                                           `agents/openai.yaml`
```

1. **Pure Standalone (`SKILL.md` Only) — 37 Skills (35.6%)**:
   These directories contain strictly a single `SKILL.md` file. They have zero subdirectories, zero examples, zero scripts, and zero metadata manifests.
   - *Distribution*: All 20 `gamedev` skills; 7 SOTA `frontend` skills (`anti-ui-slop-finish-gate`, `design-md-specification`, `design-system-engineering`, `frontend-micro-polish`, `interactive-component-workbench`, `motion-performance-engineering`, `web-quality-audit`); 3 `foundation` skills (`discernment-nudge`, `hostile-component-stress-testing`, `playwright-evidence-qa`); 2 `document` skills (`docx`, `pdf`); 2 `ai-agent` skills (`context-optimization`, `memory-hygiene`); 2 `security-data` skills (`prompt-injection-defense`, `skill-preflight-ast-check`); and 1 `platform` skill (`agents-sdk`).
2. **Pseudo-Expanded (Metadata Manifests Present) — 67 Skills (64.4%)**:
   These directories contain subdirectories or supplementary markdown files, but lack canonical engineering assets:
   - **`agents/openai.yaml` Only (56 skills)**: Contains only an OpenAI Assistant configuration (`openai.yaml`), specifying model selection and tool bindings, but providing no software engineering reference patterns, schemas, or code.
   - **Orphaned `UPGRADE_PLAN_2026.md` + `agents/openai.yaml` (11 skills)**: Contains extensive technical specifications detailing modern 2026 SOTA patterns (React 19 Server Components, TanStack Query invalidation, Stripe Payment Intents, WebMCP), which were drafted during previous refactoring rounds but never converted into actual supporting asset files.
     - *Affected Commerce Skills (4)*: `handle-checkout-flow`, `integrate-payment-gateway`, `manage-order-fulfillment`, `manage-product-catalog`.
     - *Affected Frontend Skills (7)*: `add-page-route`, `add-ui-component`, `frontend-testing`, `implement-webmcp`, `integrate-api-client`, `setup-design-system`, `setup-visual-regression`.

---

### 2.3 The "Example Desert": Asset Scarcity in Expanded Skills
Even among the 65 skills classified as "expanded," asset richness is severely lopsided:
- **`references/` Only**: **57 skills (87.7%)** contain only 1–2 markdown reference files.
- **`scripts/` Only**: **4 skills (6.2%)** (`ai-agent/agent-evaluation`, `document/pptx`, `document/xlsx`, `foundation/webapp-server-runner`).
- **`references/` + `scripts/`**: **1 skill (1.5%)** (`platform/turnstile-spin`).
- **`examples/` + `references/`**: **Only 3 skills in the entire repository (1.6%)**:
  1. `backend/add-api-endpoint` (`examples/kratos-go-clean-architecture-endpoint.md`, `examples/express-zod-rfc9457-endpoint.md`)
  2. `foundation/write-tests` (`examples/anti-tautological-tdd-walkthrough.md`, `examples/testcontainers-kratos-integration-test.md`)
  3. `repo-ops/review-code` (`examples/ai-vibe-slop-remediation.md`, `examples/adversarial-two-axis-pr-review.md`)

> **The Gold Standard Trinity**:
> A truly production-ready engineering skill must not consist solely of abstract advice in `SKILL.md`. It requires three physical pillars:
> 1. **Architectural Reference (`references/`)**: Normative specifications, API contracts, sequence diagrams, and error taxonomies.
> 2. **Canonical Worked Example (`examples/`)**: Real-world, copy-pasteable, production-grade source code demonstrating end-to-end execution.
> 3. **Automated Verification Harness (`scripts/` or schema check)**: Deterministic scripts or linters to validate outputs.
>
> Today, **98.4% of the skills in the repository (180/183) fail to provide canonical worked examples**, forcing AI agents to invent implementations from unstructured pre-training memory.

---

### 2.4 Domain Category Distribution (Core Skills)

| Category | Total Skills | Expanded | Un-expanded | % Un-expanded | Domain Health & Vulnerability Assessment |
|:---|:---:|:---:|:---:|:---:|:---|
| **`gamedev`** | 20 | 0 | 20 | **100.0%** | **Critical Blank**: 100% of game development skills are single-file `SKILL.md`. |
| **`mmo`** | 7 | 0 | 7 | **100.0%** | **Critical Blank**: All anti-detect, proxy, and campaign automation skills lack assets. |
| **`commerce`** | 4 | 0 | 4 | **100.0%** | **Critical Blank**: All 4 core e-commerce skills have orphaned upgrade plans. |
| **`documentation`** | 3 | 0 | 3 | **100.0%** | **Critical Blank**: Technical writing standards lack reference templates and styles. |
| **`frontend`** | 16 | 2 | 14 | **87.5%** | **Severe Exposure**: 7 skills have orphaned upgrade plans, 7 pure standalone. |
| **`agent`** | 24 | 7 | 17 | **70.8%** | **Severe Exposure**: Core orchestration, A2A, and memory skills lack references. |
| **`foundation`** | 18 | 6 | 12 | **66.7%** | **High Exposure**: Root-cause analysis, triage, and debugging tools un-expanded. |
| **`ai-agent`** | 3 | 1 | 2 | **66.7%** | **Moderate Exposure**: Context optimization & memory hygiene lack references. |
| **`platform`** | 19 | 8 | 11 | **57.9%** | **High Exposure**: K8s, runtime triage, and telemetry instrumentation lack assets. |
| **`backend`** | 8 | 4 | 4 | **50.0%** | **High Exposure**: Outbox, event handlers, and service clients lack code examples. |
| **`security-data`** | 10 | 5 | 5 | **50.0%** | **High Exposure**: Security audit, secret rotation, and AST checking lack references. |
| **`document`** | 4 | 2 | 2 | **50.0%** | **Defect Exposure**: `docx` and `pdf` lack scripts; `pdf` references phantom scripts. |
| **`ai`** | 2 | 1 | 1 | **50.0%** | **Defect Exposure**: `openrouter-task` has hardcoded Windows paths. |
| **`repo-ops`** | 5 | 3 | 2 | **40.0%** | **High Exposure**: `navigate-service` and `review-service` lack service maps. |
| **`business`** | 3 | 3 | 0 | 0.0% | **Healthy**: BABOK requirements, use cases, and impact matrices expanded. |
| **`content`** | 6 | 6 | 0 | 0.0% | **Healthy**: Writing, editing, and content strategy references present. |
| **`education`** | 3 | 3 | 0 | 0.0% | **Healthy**: Learning plans, exercises, and grading rubrics expanded. |
| **`legal-compliance`**| 3 | 3 | 0 | 0.0% | **Healthy**: Vietnamese PDPL, AI Law, and legal opinion references present. |
| **`meetings-analysis`**| 3 | 3 | 0 | 0.0% | **Healthy**: Meeting review, business requirements, and transcripts expanded. |
| **`mobile`** | 2 | 2 | 0 | 0.0% | **Healthy**: React Native New Architecture and EAS deployment expanded. |
| **`product`** | 4 | 4 | 0 | 0.0% | **Healthy**: Story mapping, roadmap prioritization, and SaaS unit economics expanded. |
| **`seo`** | 2 | 2 | 0 | 0.0% | **Healthy**: Technical SEO audits and content optimization expanded. |
| **Total Core** | **169** | **65** | **104** | **61.5%** | **Overall Core Un-Expanded Proportion** |

---

### 2.5 Role Dependency Risk & Workflow Blast Radius

#### Role Reliance Analysis (39 Roles)
Cross-referencing `adapters/antigravity/role-skill-index.json` and role profiles in `core/roles/*.md` uncovers that role capabilities are heavily crippled by un-expanded primary skills:

1. **Roles with 100% Un-Expanded Primary Skills (9 Roles — Critical Vulnerability)**:
   - `game-developer`: 20/20 primary skills un-expanded (100.0%)
   - `mmo-engineer`: 7/7 primary skills un-expanded (100.0%)
   - `security-engineer`: 7/7 primary skills un-expanded (100.0%)
   - `ecommerce-engineer`: 5/5 primary skills un-expanded (100.0%)
   - `3d-graphics-engineer`: 4/4 primary skills un-expanded (100.0%)
   - `technical-writer`: 4/4 primary skills un-expanded (100.0%)
   - `aws-engineer`: 3/3 primary skills un-expanded (100.0%)
   - `prompt-engineer`: 2/2 primary skills un-expanded (100.0%)
   - `reverse-engineer`: 1/1 primary skills un-expanded (100.0%)

2. **Core Engineering Roles with High Un-Expanded Ratios (11 Roles — Severe Vulnerability)**:
   - `agent-discovery-engineer`: 7/8 primary skills un-expanded (**87.5%**)
   - `ai-systems-engineer`: 5/6 primary skills un-expanded (**83.3%**)
   - `ui-ux-designer`: 5/6 primary skills un-expanded (**83.3%**)
   - `frontend-developer`: 12/15 primary skills un-expanded (**80.0%**)
   - `qa-engineer`: 9/12 primary skills un-expanded (**75.0%**)
   - `devops-engineer`: 6/8 primary skills un-expanded (**75.0%**)
   - `system-engineer`: 6/8 primary skills un-expanded (**75.0%**)
   - `agent-coordinator`: 9/13 primary skills un-expanded (**69.2%**)
   - `reviewer`: 3/5 primary skills un-expanded (**60.0%**)
   - `cloudflare-engineer`: 8/14 primary skills un-expanded (**57.1%**)
   - `mobile-engineer`: 5/9 primary skills un-expanded (**55.6%**)

3. **Roles at Exactly 50.0% Un-Expanded Boundary (3 Roles)**:
   - `solution-architect`: 1/2 primary skills un-expanded (**50.0%**)
   - `sre`: 3/6 primary skills un-expanded (**50.0%**)
   - `task-planner`: 1/2 primary skills un-expanded (**50.0%**)

> **Role Risk Summary**: **20 out of 39 roles (51.3%) have strictly more than 50% of their primary skills un-expanded, rising to 23 out of 39 roles (59.0%) with $\ge 50\%$ un-expanded primary skills when accounting for the 3 roles at the exact 50.0% boundary.**
> When an agent assumes one of these roles, half or more of its specialized tools lack supporting assets, forcing it to fall back on generic training and increasing the risk of code hallucinations and architectural violations.

#### Workflow Blast Radius (25 Workflows)
Workflows orchestrate end-to-end delivery by chaining skills across roles. Auditing all 25 workflows in `core/workflows/*.md` reveals:
- **23 of 25 workflows (92.0%) invoke un-expanded skills in their critical execution path**.
- Top un-expanded skills by workflow invocations:
  - `navigate-service`: invoked across **10 workflows**
  - `incident-report`: invoked across **9 workflows**
  - `agent-quality-gate`: invoked across **5 workflows**
  - `review-service`: invoked across **4 workflows**
  - `agent-delegation`: invoked across **3 workflows**
  - `security-audit`: invoked across **3 workflows**
  - `write-documentation`: invoked across **3 workflows**

#### Composite Criticality Score Formula
To eliminate arbitrary prioritization, skills are ranked using an objective, multi-variable formula:
$$\text{Criticality Score} = 3 \times (\text{Primary Roles}) + 1 \times (\text{Supporting Roles}) + 2 \times (\text{Workflow Invocations})$$

---

### 2.6 Concrete Defect Discoveries in Skills

#### Defect 1: Phantom Script References in `core/skills/document/pdf/SKILL.md`
- **Location**: `core/skills/document/pdf/SKILL.md`, lines 20–23:
  ```markdown
  - Run check_fillable_fields.py to list field names and types.
  - Author a JSON mapping payload matching form keys.
  - Run fill_fillable_fields.py input.pdf values.json output.pdf.
  ```
- **Forensic Evidence**: A recursive filesystem scan confirms that neither `check_fillable_fields.py` nor `fill_fillable_fields.py` exists anywhere in the repository. The directory contains only `SKILL.md`.
- **Impact**: Any agent delegated to perform PDF form operations that attempts to follow these instructions will immediately fail with `command not found` or `FileNotFoundError`.

#### Defect 2: Hardcoded Non-Portable Windows Paths in `core/skills/ai/openrouter-task/SKILL.md`
- **Location**: `core/skills/ai/openrouter-task/SKILL.md`, lines 3, 22, 42, 48:
  ```markdown
  Line 3:  description: ... using the local environment key at D:\myproject\.agents\.env ...
  Line 22: load OPENROUTER_API_KEY exclusively from the local environment file (D:\myproject\.agents\.env)
  Line 42: python D:\myproject\tools\openrouter_worker.py --check
  Line 48: python D:\myproject\tools\openrouter_worker.py --prompt "<task_description>"
  ```
- **Forensic Evidence**: Hardcoded Windows drive letters (`D:\`) and specific user directory structures (`myproject`) directly violate repository portability rules, break POSIX environments (macOS/Linux), and point to non-existent scripts (`openrouter_worker.py`).
- **Impact**: Breaks execution on any platform other than the author's local Windows workstation.

#### Defect 3: 11 Orphaned `UPGRADE_PLAN_2026.md` Specifications
- **Location**: 4 commerce skills and 7 frontend skills contain `UPGRADE_PLAN_2026.md` alongside `agents/openai.yaml`.
- **Forensic Evidence**: These files contain complete, production-grade 2026 architectural designs (e.g. React 19 RSC boundaries, TanStack Query cache keys, WebMCP tool definitions), but their contents were never materialized into `references/` or `examples/`.
- **Impact**: Domain research was conducted but left unbundled, depriving agents of active guidance.

---

### 2.7 3-Tier Skill Expansion Roadmap

#### Tier 1: Immediate High-Impact Core Dev Loop (22 Skills)
These 22 skills form the active backbone of daily software delivery across backend, frontend, devops, security, and coordination. They have the highest Criticality Scores and must be prioritized for immediate expansion.

| # | Skill Name | Category | Score | Prim Roles | Supp Roles | Wfs | Target Supporting Asset Additions |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| 1 | **`navigate-service`** | `repo-ops` | **48** | 3 | 19 | 10 | `references/service-topography.md`, `examples/kratos-service-map.md` |
| 2 | **`agent-delegation`** | `agent` | **40** | 1 | 31 | 3 | `references/a2a-protocol-lifecycle.md`, `examples/task-delegation-trace.json` |
| 3 | **`security-audit`** | `security-data` | **28** | 2 | 16 | 3 | `references/owasp-asi-threat-model.md`, `examples/audited-service-report.md` |
| 4 | **`incident-report`** | `foundation` | **25** | 1 | 4 | 9 | `references/blameless-rca-guide.md`, `examples/p1-outage-postmortem.md` |
| 5 | **`write-documentation`** | `documentation` | **23** | 1 | 14 | 3 | `references/diataxis-framework-guide.md`, `examples/microservice-readme.md` |
| 6 | **`agent-quality-gate`** | `agent` | **22** | 3 | 3 | 5 | `references/phase-exit-evidence-rubric.md`, `examples/verification-matrix.md` |
| 7 | **`add-telemetry-instrumentation`** | `platform` | **21** | 5 | 6 | 0 | `references/otel-semantic-conventions.md`, `examples/otel-kratos-middleware.go` |
| 8 | **`review-service`** | `repo-ops` | **21** | 1 | 10 | 4 | `references/production-readiness-gates.md`, `examples/service-audit-deliverable.md` |
| 9 | **`ai-risk-assessment`** | `foundation` | **16** | 3 | 7 | 0 | `references/nist-ai-rmf-rubric.md`, `examples/genai-risk-register.md` |
| 10 | **`debug-runtime-platform`** | `platform` | **14** | 3 | 3 | 1 | `references/runtime-triage-playbook.md`, `scripts/k8s-pod-diagnostic.sh` |
| 11 | **`implement-structured-outputs`** | `backend` | **13** | 4 | 1 | 0 | `references/json-schema-decoding-rules.md`, `examples/pydantic-zod-schemas.md` |
| 12 | **`setup-llm-gateway`** | `platform` | **13** | 4 | 1 | 0 | `references/gateway-failover-topology.md`, `examples/litellm-proxy-config.yaml` |
| 13 | **`supply-chain-security`** | `platform` | **13** | 3 | 4 | 0 | `references/slsa-sbom-sigstore-guide.md`, `examples/github-actions-sbom.yaml` |
| 14 | **`setup-deployment`** | `platform` | **12** | 2 | 4 | 1 | `references/k8s-manifest-invariants.md`, `examples/kustomize-production-app.yaml` |
| 15 | **`manage-secrets`** | `security-data` | **11** | 2 | 5 | 0 | `references/zero-trust-secret-rotation.md`, `examples/external-secrets-vault.yaml` |
| 16 | **`frontend-testing`** | `frontend` | **10** | 3 | 1 | 0 | `references/rtl-a11y-testing-rubrics.md`, `examples/rtl-msw-integration-test.tsx` |
| 17 | **`systematic-debugging`** | `foundation` | **7** | 1 | 4 | 0 | `references/four-phase-rca-method.md`, `examples/goroutine-race-triage.md` |
| 18 | **`add-ui-component`** | `frontend` | **6** | 2 | 0 | 0 | `references/rsc-and-anti-slop.md`, `examples/compound-dialog-react19.tsx` |
| 19 | **`add-page-route`** | `frontend` | **3** | 1 | 0 | 0 | `references/nextjs-app-router-layouts.md`, `examples/streaming-crud-page.tsx` |
| 20 | **`integrate-api-client`** | `frontend` | **6** | 2 | 0 | 0 | `references/tanstack-query-invalidation.md`, `examples/optimistic-mutation-hook.ts` |
| 21 | **`add-event-handler`** | `backend` | **4** | 1 | 1 | 0 | `references/transactional-outbox-pattern.md`, `examples/kratos-dapr-subscriber.go` |
| 22 | **`add-service-client`** | `backend` | **3** | 1 | 0 | 0 | `references/circuit-breaker-retry-policies.md`, `examples/resilient-grpc-client.go` |

#### Tier 2: Domain Specialists & Emerging SOTA (52 Skills)
Skills supporting advanced agent discovery, stateful edge computing, modern design systems, and commerce workflows:
- **Cloudflare Edge & Agent Discovery (11 skills)**: `agents-sdk`, `debug-workers-edge`, `wrangler`, `web-perf`, `configure-agent-headers`, `configure-agent-skills`, `configure-oauth-metadata`, `debug-identity-provider`, `manage-agent-identity`, `manage-api-catalog`, `manage-auth-md`.
- **Agent Architecture, Panel & Memory (9 skills)**: `agent-context-management`, `agent-graph-orchestration`, `agent-handoff`, `agent-model-routing`, `agent-observability`, `agent-panel-meeting`, `agent-semantic-memory`, `context-optimization`, `memory-hygiene`.
- **SOTA Frontend & Verification (15 skills)**: `accessibility-review`, `anti-ui-slop-finish-gate`, `design-md-specification`, `design-review`, `design-system-engineering`, `design-ux-flow`, `frontend-micro-polish`, `hostile-component-stress-testing`, `implement-webmcp`, `interactive-component-workbench`, `motion-performance-engineering`, `playwright-evidence-qa`, `setup-design-system`, `setup-visual-regression`, `web-quality-audit`.
- **Backend & AI Tooling (2 skills)**: `build-mcp-server`, `setup-gpu-finops`.
- **E-Commerce Suite (5 skills)**: `configure-agent-commerce`, `handle-checkout-flow`, `integrate-payment-gateway`, `manage-order-fulfillment`, `manage-product-catalog`.
- **Documentation & Product Strategy (5 skills)**: `configure-llms-txt`, `discernment-nudge`, `release-notes`, `write-product-brief`, `write-tech-radar`.
- **Document & Office Operations (2 skills)**: `docx`, `pdf` *(requires fixing phantom scripts)*.
- **Testing & Security Foundation (3 skills)**: `combinatorial-testing`, `prompt-injection-defense`, `skill-preflight-ast-check`.

#### Tier 3: Domain Verticals & Stack Overlays (44 Skills)
Niche vertical domains and repo-specific stack extensions, expandable on-demand when specific customer projects require them:
- **Game Development Vertical (`gamedev`, 20 skills)**: `abstract-input-actions`, `architect-ecs-systems`, `author-game-ai`, `automate-game-publishing`, `build-game-ui-ux`, `configure-physics-collision`, `design-procedural-generation`, `develop-gameplay-systems`, `direct-camera-systems`, `generate-game-assets-pipeline`, `implement-save-persistence`, `inspect-blender-rigs-motion`, `integrate-dialogue-narrative`, `integrate-game-engine`, `manage-scene-lifecycle`, `mix-dynamic-game-audio`, `profile-game-performance`, `program-game-shaders`, `render-webgl-threejs`, `tune-game-feel`.
- **MMO Operations (`mmo`, 7 skills)**: `analyze-campaign-roi`, `create-automation-script`, `deploy-mmo-infrastructure`, `deploy-proxyware-fleet`, `generate-mmo-content`, `manage-mmo-assets`, `setup-tracking-system`.
- **Specialized Systems & Legacy (3 skills)**: `openrouter-task` *(requires immediate portability fix)*, `aws-infrastructure`, `reverse-engineer-binary`.
- **Stack Overlays (`overlays/`, 14 skills)**: `develop-b2b-golf-feature`, `develop-b2b-catalog-feature`, `isometric-svg-projection`, `build-credit-scorecard`, `audit-technical-article`, `write-hugo-twin-content`, `write-hvac-authority-content`, `develop-laravel-ecommerce-feature`, `develop-laravel-feature`, `develop-obj-feature`, `debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets`, `write-real-estate-astro-data`.

---

## 3. Track 2: Golden Evaluation Coverage Across Roles & Workflows

### 3.1 Census of Existing Fixtures & Dynamic Harnesses
The repository contains two evaluation subsystems on disk:

#### A. PromptOps Golden Evaluation Fixtures (`core/prompts/golden/`)
Versioned test datasets adhering to PromptOps standards, containing paired `*-input.json` and `*-expected.json` files validated by `manifest.yaml`:
- **Total Assets**: **6 promoted assets**
- **Total Case Pairs**: **68 case pairs**
- **Roles Evaluated**: 5 roles (`agent-coordinator`, `technical-lead`, `content-manager`, `ecommerce-engineer`, `security-engineer`)
- **Skills Evaluated**: 5 skills (`agent-a2a-protocol`, `review-code`, `audit-content`, `integrate-payment-gateway`, `security-audit`)
- **Contract Schemas Checked**: 5 schemas (`coordination-plan.json`, `implementation-result.json`, `content-audit-report.json`, `api-contract-spec.json`, `security-audit.json`)
- **Documentation Drift**: Both `core/prompts/README.md` and `core/prompts/golden/README.md` list `"4. Promoted Datasets Index (58 Total Cases)"` across 5 assets, failing to document the newly added `content-quality` asset (10 cases).

#### B. Dynamic Agent Evaluation Benchmark Runner (`core/skills/ai-agent/agent-evaluation/`)
- Implements an automated benchmark runner: `core/skills/ai-agent/agent-evaluation/scripts/run-eval-benchmark.py` (857 lines).
- Evaluates **15 benchmark cases** across 4 domains (A2A uppercase states, Two-Tier JIT skill discovery via BM25, MCP prefix policy gating, and prompt cache layer volatility).
- Validates output strictly against `core/contracts/schemas/agent-eval-report.json`.

---

### 3.2 Exhaustive Role Census & Evaluation Coverage Mapping (39 Roles)

| # | Role Slug | Role Title | Dedicated Pytest Challenge File in `tests/` | Golden Prompt Fixtures (`core/prompts/golden/`) | Net Evaluation Status |
|---|-----------|------------|---------------------------------------------|:-----------------------------------------------:|:---------------------:|
| 1 | `3d-graphics-engineer` | 3D Graphics Engineer | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 2 | `agent-coordinator` | Agent Coordinator | None *(generic checks in `test_a2a_v1`)* | `a2a-coordination` (10), `agent-coordinator-phase-gate` (18) | **FULL EVALUATION (28 cases)** |
| 3 | `agent-discovery-engineer` | Agent Discovery Engineer | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 4 | `ai-systems-engineer` | AI Systems Engineer | `test_ai_systems_engineer_platform_challenge.py` (30 tests) | None | **STATIC LINTER ONLY** |
| 5 | `aws-engineer` | AWS Engineer | `test_aws_engineer_platform_challenge.py` (28 tests) | None | **STATIC LINTER ONLY** |
| 6 | `backend-developer` | Backend Developer | None *(generic checks in `test_phase3_e2e`)* | None | **ZERO EVALUATION** |
| 7 | `business-analyst` | Business Analyst | `test_business_analyst_requirements_challenge.py` (30 tests) | None | **STATIC LINTER ONLY** |
| 8 | `cloudflare-engineer` | Cloudflare Engineer | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 9 | `content-manager` | Content Manager | None *(generic checks in `test_lease`)* | `content-quality` (10 cases) | **FULL EVALUATION (10 cases)** |
| 10 | `content-writer` | Content Writer | None *(generic checks in `test_lease`)* | None | **ZERO EVALUATION** |
| 11 | `data-analyst` | Data Analyst | `test_data_analyst_decision_science_challenge.py` (19 tests) | None | **STATIC LINTER ONLY** |
| 12 | `data-engineer` | Data Engineer | `test_data_engineer_lakehouse_challenge.py` (27 tests) | None | **STATIC LINTER ONLY** |
| 13 | `devops-engineer` | DevOps Engineer | `test_devops_engineer_platform_challenge.py` (27 tests) | None | **STATIC LINTER ONLY** |
| 14 | `ecommerce-engineer` | Ecommerce Engineer | None *(generic checks in `test_tier3`)* | `payment-integration` (10 cases) | **FULL EVALUATION (10 cases)** |
| 15 | `frontend-developer` | Frontend Developer | None *(generic checks in `test_p6_m2`)* | None | **ZERO EVALUATION** |
| 16 | `game-developer` | Game Developer | `test_gamedev_catalog_challenge.py` (8 tests) | None | **STATIC LINTER ONLY** |
| 17 | `mmo-engineer` | MMO Engineer | `test_mmo_pack_challenge.py` (16 tests) | None | **STATIC LINTER ONLY** |
| 18 | `mobile-engineer` | Mobile Engineer | None *(generic checks in `test_tier5`)* | None | **ZERO EVALUATION** |
| 19 | `product-manager` | Product Manager | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 20 | `project-manager` | Project Manager | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 21 | `prompt-engineer` | Prompt Engineer | None *(generic checks in `test_memory_hygiene`)*| None | **ZERO EVALUATION** |
| 22 | `qa-engineer` | QA Engineer | `test_qa_engineer_verification_challenge.py` (33 tests) | None | **STATIC LINTER ONLY** |
| 23 | `researcher` | Researcher | `test_researcher_sota_challenge.py` (33 tests) | None | **STATIC LINTER ONLY** |
| 24 | `reverse-engineer` | Reverse Engineer | `test_reverse_engineer_challenge.py` (28 tests) | None | **STATIC LINTER ONLY** |
| 25 | `reviewer` | Reviewer | None *(generic checks in `test_shoppe`)* | None | **ZERO EVALUATION** |
| 26 | `sdet` | SDET | None *(generic checks in `test_qa_engineer`)* | None | **ZERO EVALUATION** |
| 27 | `security-engineer` | Security Engineer | None *(generic checks in `test_memory_hygiene`)*| `security-audit` (10 cases) | **FULL EVALUATION (10 cases)** |
| 28 | `seo-analyst` | SEO Analyst | None *(generic checks in `test_lease`)* | None | **ZERO EVALUATION** |
| 29 | `solution-architect` | Solution Architect | None *(generic checks in `test_shoppe`)* | None | **ZERO EVALUATION** |
| 30 | `sre` | Site Reliability Engineer | `test_sre_reliability_challenge.py` (39 tests) | None | **STATIC LINTER ONLY** |
| 31 | `system-engineer` | System Engineer | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 32 | `task-planner` | Task Planner | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 33 | `teacher` | Teacher | None *(generic checks in `test_m1_schemas`)* | None | **ZERO EVALUATION** |
| 34 | `technical-architect` | Technical Architect | None *(generic checks in `test_shoppe`)* | None | **ZERO EVALUATION** |
| 35 | `technical-lead` | Technical Lead | None *(generic checks in `test_shoppe`)* | `code-refactoring` (10 cases) | **FULL EVALUATION (10 cases)** |
| 36 | `technical-writer` | Technical Writer | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 37 | `ui-ux-designer` | UI/UX Designer | None *(generic checks in `test_tier3`)* | None | **ZERO EVALUATION** |
| 38 | `vietnam-accounting-specialist` | Vietnam Accounting Specialist | `test_m2_accounting_challenge.py` (22 tests) | None | **STATIC LINTER ONLY** |
| 39 | `vietnam-legal-counsel` | Vietnam Legal Counsel | `test_vietnam_legal_pack_challenge.py` (41 tests) | None | **STATIC LINTER ONLY** |

#### Summary Role Metrics:
- **Roles with Full Golden Prompt Evaluation**: **5 of 39 roles (12.8%)**
- **Roles with Dedicated Static Pytest Challenge Suites**: **14 of 39 roles (35.9%)**
- **Roles with ZERO Golden Evaluation Fixtures**: **34 of 39 roles (87.2%)**
- **Roles with ZERO Dedicated Challenge Tests**: **25 of 39 roles (64.1%)**
- **Critical Foundation Engineering Roles Lacking Golden Evals**: `backend-developer`, `frontend-developer`, `devops-engineer`, `qa-engineer`, `solution-architect`, `technical-architect`, `product-manager`, `sre`, `data-engineer`, `ai-systems-engineer`.

---

### 3.3 Exhaustive Workflow Census & Evaluation Coverage Mapping (25 Workflows)

All 25 SOP workflows declared in `core/workflows/*.md` were evaluated:

| # | Workflow Slug | Step Count | Participating Roles | Expected Output Contracts | Automated Test Runs in `tests/` | Golden Traces / State Machine Evals | Net Coverage Status |
|---|---------------|:----------:|:-------------------:|:-------------------------:|:-------------------------------:|:----------------------------------:|:-------------------:|
| 1 | `add-new-feature` | 9 | 11 roles | `feature-ticket.json`, `implementation-result.json` | None | None | **ZERO COVERAGE** |
| 2 | `agent-a2a-delegation` | 7 | 4 roles | `coordination-plan.json`, `a2a-task.json`, `a2a-artifact.json` | None | None | **ZERO COVERAGE** |
| 3 | `bug-fix` | 6 | 6 roles | `code-review-finding.json`, `pull-request-spec.json`, `test-report.json` | None | None | **ZERO COVERAGE** |
| 4 | `build-deploy` | 7 | 8 roles | `deployment-plan.json`, `edge-deployment-spec.json`, `incident-report.json` | None | None | **ZERO COVERAGE** |
| 5 | `code-review` | 5 | 4 roles | `code-review-finding.json`, `pull-request-spec.json`, `test-report.json` | None | None | **ZERO COVERAGE** |
| 6 | `content-audit` | 7 | 5 roles | `content-audit-report.json`, `data-analysis-report.json`, `seo-audit-report.json`| None | None | **ZERO COVERAGE** |
| 7 | `content-publishing` | 8 | 4 roles | `content-handoff.json`, `research-report.json`, `seo-content-brief.json` | None | None | **ZERO COVERAGE** |
| 8 | `curriculum-delivery` | 5 | 1 role | `learning-assessment-report.json`, `learning-handoff.json` | None | None | **ZERO COVERAGE** |
| 9 | `data-migration` | 8 | 8 roles | `data-pipeline-spec.json`, `deployment-plan.json`, `schema-migration.json` | None | None | **ZERO COVERAGE** |
| 10 | `data-pipeline-incident` | 7 | 7 roles | `data-pipeline-spec.json`, `incident-report.json` | None | None | **ZERO COVERAGE** |
| 11 | `dependency-upgrade` | 8 | 7 roles | `document-manifest.json`, `implementation-result.json` | None | None | **ZERO COVERAGE** |
| 12 | `feature-delivery` | 6 | 8 roles | `api-contract-spec.json`, `code-review-finding.json`, `test-report.json` | None | None | **ZERO COVERAGE** |
| 13 | `hotfix-production` | 7 | 7 roles | `deployment-plan.json`, `implementation-result.json`, `incident-report.json` | None | None | **ZERO COVERAGE** |
| 14 | `mmo-campaign-lifecycle` | 5 | 5 roles | `content-handoff.json`, `mmo-campaign-spec.json`, `mmo-roi-report.json` | File assertion in `test_mmo` | None | **STATIC LINTER ONLY** |
| 15 | `period-end-closing` | 8 | 1 role | `accounting-compliance-review.json`, `period-end-closing-report.json` | Schema tests in `test_m1` | None | **STATIC LINTER ONLY** |
| 16 | `qa-validation` | 8 | 2 roles | `code-review-finding.json`, `test-report.json` | None | None | **ZERO COVERAGE** |
| 17 | `refactoring` | 7 | 6 roles | `code-review-finding.json`, `implementation-result.json` | None | None | **ZERO COVERAGE** |
| 18 | `revert-deployment` | 6 | 5 roles | `coordination-plan.json`, `deployment-plan.json`, `incident-report.json` | None | None | **ZERO COVERAGE** |
| 19 | `security-incident-response` | 8 | 8 roles | `coordination-plan.json`, `incident-report.json` | None | None | **ZERO COVERAGE** |
| 20 | `seo-content-lifecycle` | 3 | 6 roles | `content-handoff.json`, `seo-audit-report.json`, `seo-content-brief.json` | None | None | **ZERO COVERAGE** |
| 21 | `seo-keyword-brief` | 8 | 1 role | `seo-content-brief.json` | None | None | **ZERO COVERAGE** |
| 22 | `service-review-release` | 9 | 10 roles | `coordination-plan.json`, `deployment-plan.json`, `incident-report.json` | None | None | **ZERO COVERAGE** |
| 23 | `setup-new-service` | 10 | 8 roles | `edge-deployment-spec.json`, `implementation-result.json` | None | None | **ZERO COVERAGE** |
| 24 | `tech-repo-review` | 8 | 3 roles | `architecture-options.json`, `code-review-finding.json`, `security-audit.json`| None | None | **ZERO COVERAGE** |
| 25 | `troubleshooting` | 9 | 6 roles | `coordination-plan.json`, `implementation-result.json`, `incident-report.json` | None | None | **ZERO COVERAGE** |

#### Summary Workflow Metrics:
- **Workflows with Dynamic Execution Evaluation**: **0 of 25 (0.0%)**
- **Workflows with Golden Execution Traces**: **0 of 25 (0.0%)**
- **Workflows with Multi-Agent Step Handshake Assertions**: **0 of 25 (0.0%)**

---

### 3.4 Static vs. Dynamic Gap Analysis
The repository's 23 validator scripts and 924 test cases create a dangerous **illusion of verification**.
- **What CI Actually Checks**: File existence, markdown header syntax, regex string matches (e.g. asserting that `VLLM-CACHE-LOCK` appears in text), line count bounds ($\le 200$), and JSON Schema Draft 2020-12 compilation.
- **What CI Cannot See**:
  1. **Prompt Bloat & Attention Degradation**: Role files range up to 624 lines. When compiled into an LLM context window alongside system rules, the model suffers from attention attenuation ("lost-in-the-middle"), missing mid-document constraints.
  2. **Instruction Conflicts**: Conflicting directives between global rules and role toolboxes are never detected because no model is ever prompted to act on them.
  3. **Adversarial Non-Compliance**: Whether an agent under pressure respects boundary locks (e.g., declining to write code when acting as `product-manager`) is verified only by regex checking the prohibition string in markdown, never by observing actual tool invocation.

---

### 3.5 Golden Evaluation Framework (GEF) Architecture
To resolve the dynamic evaluation deficit, we specify the **Golden Evaluation Framework (GEF)**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     Golden Evaluation Framework (GEF)                  │
├────────────────────┬───────────────────────────────────────────────────┤
│ 1. Fixture Layer   │ core/prompts/golden/<role-id>/                    │
│                    │   manifest.yaml + cases/NNN-input/expected.json   │
├────────────────────┼───────────────────────────────────────────────────┤
│ 2. Workflow Traces │ core/evals/workflows/<workflow-id>/               │
│                    │   scenario.json + step-NN-handoff.json            │
├────────────────────┼───────────────────────────────────────────────────┤
│ 3. Execution Engine│ core/scripts/run-golden-evals.py                  │
│                    │   - Backend connector (OpenRouter / Local / Mock) │
│                    │   - Context compiler (Role + Skill + Schemas)     │
├────────────────────┼───────────────────────────────────────────────────┤
│ 4. Hybrid Grader   │ Tier 1: Deterministic Schema & Token Assertions   │
│    Hierarchy       │ Tier 2: Latency, Step Budget & Token Heuristics   │
│                    │ Tier 3: LLM-as-a-Judge Anchor-Graded Rubrics      │
├────────────────────┼───────────────────────────────────────────────────┤
│ 5. Gating Contract │ core/contracts/schemas/agent-eval-report.json     │
│                    │   Emits pass^k reliability & defect taxonomy      │
└────────────────────┴───────────────────────────────────────────────────┘
```

#### Multi-Agent Workflow State Machine Traces
For workflows, evaluate transitions using **Contract Handoff Verification**:
$$\text{Contract}_{\text{produced}}(Step_N) \models \text{Contract}_{\text{required}}(Step_{N+1})$$
The evaluation harness executes step fixtures sequentially, verifying that each role emits valid JSON schemas conforming to the recipient role's boundary requirements.

---

## 4. Track 3: Test Suite Robustness & Repository Packaging/Hygiene

### 4.1 Test Suite Composition & Distribution Breakdown
The pytest test suite comprises 32 Python test files (`tests/test_*.py`) and 1 Node.js test file (`tests/npm/cli.test.mjs`):

| Category | File Count | Test Count | % of Suite | Scope Checked |
|:---|:---:|:---:|:---:|:---|
| **Role & Domain Challenge Suites** | 22 files | 608 tests | 65.8% | Invariant strings in `core/roles/*.md`, architectural lock strings, schema drafts. |
| **Phase & E2E Integration Suites** | 2 files (`phase3`, `phase4`) | 154 tests | 16.7% | Cross-layer wiring, A2A task states, policy evaluation. |
| **Memory & Context Tooling** | 4 files | 90 tests | 9.7% | Context compaction, memory pruning scripts, span logging. |
| **Contract Schemas & Packaging** | 5 files | 72 tests | 7.8% | Schema Draft 2020-12 compilation, npm CLI execution. |
| **Total** | **33 files** | **924 tests** | **100%** | **915 passed, 9 skipped** |

#### Analysis of the 9 Skipped Tests
All 9 skipped tests occur exclusively within `tests/test_vesviet_v5_challenge.py`:
- Lines 114, 149, 227, 264, 283, 348, 378, 411, 478 skip due to missing external sibling repositories (`authority-blog` and `learn`).
- *Finding*: The core repository tests have a 100% execution pass rate; the skips represent architectural coupling to external workspaces that should be isolated with pytest markers (`@pytest.mark.external_site`).

---

### 4.2 Empirical Skill Coverage Gap Analysis
A systematic regex and string scan across all 32 Python test files against all 183 skills reveals:
- **99 of 183 skills (54.1%) are NEVER referenced by name in `tests/`**.
  - Unreferenced operational skills include: `add-event-handler`, `add-page-route`, `add-service-client`, `agent-a2a-protocol`, `agent-context-management`, `agent-graph-orchestration`, `agent-handoff`, `agent-model-routing`, `agent-observability`, `agent-panel-meeting`, `agents-sdk`, `architect-mcp-server`, `audit-content`, `audit-technical-seo`.
- **Only 28 of 183 skills (15.3%) are loaded or inspected from disk** by any pytest test case.
- **155 of 183 skills (84.7%) have ZERO direct test assertions** on their `SKILL.md` content.
- **Superficial Testing**: For the 28 skills inspected, tests assert only that the file exists, line count $\le 200$, and frontmatter starts with `---`. Zero tests verify action verbs, negative constraints, failure modes, or code snippet syntax.

---

### 4.3 Validation Script Blind Spots (22 Pack Scripts)
Reviewing the 22 validator scripts in `core/scripts/` reveals critical blind spots:
1. **`validate-packs.py` (55 lines)**:
   - Does NOT parse YAML via `yaml.safe_load`.
   - Uses naive string matching: `if "name:" not in text:`.
   - *Blind Spot*: Malformed YAML, invalid data types, or duplicate keys pass undetected.
2. **`validate-overlays.py` (66 lines)**:
   - Verifies only that `README.md` exists and is $\ge 20$ chars, and that `rules/` has at least one file.
   - *Blind Spot*: Overlay skills are completely exempt from `validate-skills.py` frontmatter, tool lock, and section rules.
3. **`validate-skill-sections.py` (44 lines)**:
   - Checks only regex presence for `## Failure Modes`, `## Output Contracts`, `## Security Guardrails`.
   - *Blind Spot*: A placeholder section containing only "None." passes without error.
4. **Duplicate Policy Scripts**:
   - `validate-policies.py` and `validate-policy-consistency.py` perform redundant checks. `validate-all.py` executes the older script, bypassing the CLI `--strict` mode in the newer script.

---

### 4.4 The 5-Gate Skill Content Quality Regression Framework
To prevent skill quality degradation, we specify a new validator: `core/scripts/validate-skill-content-quality.py`:

```
┌────────────────────────────────────────────────────────────────────────┐
│             5-Gate Skill Content Quality Regression Engine             │
├────────────────────┬───────────────────────────────────────────────────┤
│ Gate 1: Process    │ >= 3 numbered steps in `## Suggested Process`     │
│ Depth & Verbs      │ Must begin with approved imperative action verbs  │
│                    │ (Execute, Run, Verify, Analyze, Inspect, etc.)    │
├────────────────────┼───────────────────────────────────────────────────┤
│ Gate 2: Negative   │ >= 2 explicit negative constraints in `## Core    │
│ Constraints        │ Rules` (Do NOT, Never, Must NOT, Forbidden)       │
├────────────────────┼───────────────────────────────────────────────────┤
│ Gate 3: Substantive│ Security Guardrails >= 2 items (>= 40 chars each) │
│ Governance         │ Failure Modes >= 2 items with symptoms + fixes    │
├────────────────────┼───────────────────────────────────────────────────┤
│ Gate 4: Code Block │ Extracts all fenced code blocks (bash, json, yaml)│
│ Syntax Integrity   │ Validates JSON/YAML ASTs; checks bash safety      │
├────────────────────┼───────────────────────────────────────────────────┤
│ Gate 5: Contract   │ Verifies all referenced .json schemas exist in   │
│ Resolution         │ `core/contracts/schemas/`                         │
└────────────────────┴───────────────────────────────────────────────────┘
```

---

### 4.5 Repository Packaging Audit & Clean 4-Tier Separation

#### Audit of `reports/` Rule Violation
- `reports/` currently contains **18 files** (1.9 MB):
  `RESEARCH_2026_2027_SOTA.md`, `ROADMAP_2026_2027.md`, `agent-skills-audit-report.md`, `roles-standardization-audit-2026.md`, `solution-architect-repo-research.md`, `data-engineer-data-analyst-repo-research.md`, `qa-qc-engineer-repo-research.md`, `backend-developer-repo-research.md`, `vietnam-legal-counsel-repo-research.md`, `devops-engineer-repo-research.md`, `external-skills-ecosystem-benchmark-research.md`, `role-skill-matrix-sota-audit-2026-2027.md`, `business-analyst-repo-research.md`, `repository-audit-and-drift-analysis-2026-10-25.md`, `cloudflare-skills-ecosystem-benchmark.md`, `anthropics-skills-ecosystem-benchmark-and-upgrade-plan.md`, `gamedev-skills-repo-research.md`, `sprint-2-modernization-completion-report.md`, plus `research/mmo-2027-sota-dossier.json`.
- **Direct Rule Violation**: `core/rules/knowledge.md` (lines 26–35) mandates:
  > **Root Directory Limit ($\le 5$ files)**: The root of `reports/` must only contain active, authoritative platform files... All raw research dossiers and legacy audit snapshots must reside in `reports/archive/research-dossiers/` and `reports/archive/historical-audits/`.
- **Test Assertion Blast Radius Guardrail**: Moving these historical dossiers carries an active downstream test dependency: 3 pytest test files assert explicit paths under `reports/` (`tests/test_data_engineer_lakehouse_challenge.py:397`, `tests/test_vietnam_legal_pack_challenge.py:976`, and `tests/test_business_analyst_requirements_challenge.py:491`). Reorganizing `reports/` must be accompanied by updating these fixtures to check both primary and archive locations to prevent breaking CI.

#### NPM Packaging Whitelist Audit
- `package.json` specifies `"files": ["bin/", "core/skills/", "core/roles/", "core/workflows/", "core/rules/", "core/policies/", "core/contracts/", "adapters/", "overlays/", "packs/", "INDEX.md", "README.md", "LICENSE", "VERSION"]`.
- `npm pack --dry-run` confirms: **832 files included**, tarball size **2.30 MB**, unpacked size **7.38 MB**.
- `reports/` and `tests/` are excluded from the tarball by `package.json`.
- However, npm emits a warning: `npm warn gitignore-fallback No .npmignore file found`. An untracked `.npmignore` exists in the workspace and must be committed.

#### Proposed 4-Tier Packaging Separation Architecture

```
agent-skills/
├── bin/                               # Tier 1: Distribution (CLI runner)
├── core/
│   ├── skills/                        # Tier 1: Distribution (183 atomic skills)
│   ├── roles/                         # Tier 1: Distribution (39 role standards)
│   ├── workflows/                     # Tier 1: Distribution (25 SOP workflows)
│   ├── rules/                         # Tier 1: Distribution (Global governance rules)
│   ├── policies/                      # Tier 1: Distribution (Action boundaries)
│   ├── contracts/schemas/             # Tier 1: Distribution (63 JSON schemas)
│   ├── prompts/golden/                # Tier 2: Developer QA (Golden benchmark pairs)
│   └── scripts/                       # Tier 2: Developer QA (Validators & hooks)
├── adapters/                          # Tier 1: Distribution (Antigravity Tier-1 index)
├── overlays/                          # Tier 1: Distribution (Domain stack overlays)
├── packs/                             # Tier 1: Distribution (Team compositions)
├── tests/                             # Tier 2: Developer QA (Pytest suites & Node tests)
├── reports/                           # Tier 3: Historical Research & Living Indexes
│   ├── KNOWLEDGE_INDEX.md             # Living Index (<= 5 files in root)
│   ├── ROADMAP_2026_2027.md           # Active Strategic Roadmap
│   ├── RESEARCH_2026_2027_SOTA.md     # Active SOTA Architecture
│   └── archive/                       # Historical Snapshot Vault (Git-tracked)
│       ├── research-dossiers/         # 100-round domain research dossiers
│       └── historical-audits/         # Past sprint and drift audits
└── .npmignore                         # Explicit publishing boundary
```

---

## 5. Master Prioritized Action Roadmap

### 5.1 Status Categorization & Issue Management

#### 🚩 PENDING ISSUES (Unfixed)
- **🚨 [P0-01] Eliminate Phantom Script Defect in `document/pdf`**:
  - *Description*: Remove phantom script commands or implement runnable helper scripts (`scripts/check_fillable_fields.py`, `scripts/fill_fillable_fields.py`) using `pypdf`/`pdfplumber`.
  - *Target*: `core/skills/document/pdf/SKILL.md`.
- **🚨 [P0-02] Eliminate Non-Portable Windows Hardcoding in `ai/openrouter-task`**:
  - *Description*: Strip `D:\myproject...` paths; replace with cross-platform environment variables (`OPENROUTER_API_KEY`, `OPENROUTER_CONFIG_PATH`).
  - *Target*: `core/skills/ai/openrouter-task/SKILL.md`.
- **🚨 [P0-03] Resolve `reports/` Knowledge Rule Violation with Test Guardrails**:
  - *Description*: Create `reports/archive/research-dossiers/` and `reports/archive/historical-audits/`; move 15 historical files into archive, restoring root count $\le 5$. **Explicit Blast Radius Guardrail**: Moving historical dossiers from `reports/` to `reports/archive/` must be accompanied by updating the hardcoded path assertions in `test_data_engineer_lakehouse_challenge.py:397`, `test_vietnam_legal_pack_challenge.py:976`, and `test_business_analyst_requirements_challenge.py:491` to check both primary and archive locations, preventing immediate CI test failure.
  - *Target*: `reports/` directory structure and dependent pytest fixtures (`tests/test_data_engineer_lakehouse_challenge.py`, `tests/test_vietnam_legal_pack_challenge.py`, `tests/test_business_analyst_requirements_challenge.py`).
- **🚨 [P0-04] Stage and Commit `.npmignore`**:
  - *Description*: Commit the existing untracked `.npmignore` file to silence npm packaging warnings and enforce defense-in-depth publishing boundaries.
  - *Target*: `.npmignore`.
- **🟡 [P1-01] Implement 5-Gate Skill Content Quality Validator**:
  - *Description*: Create `core/scripts/validate-skill-content-quality.py` enforcing imperative verbs, negative constraints, substantive guardrails, and code syntax; integrate into `validate-all.py`.
  - *Target*: `core/scripts/`.
- **🟡 [P1-02] Materialize 11 Orphaned `UPGRADE_PLAN_2026.md` Skills**:
  - *Description*: Convert technical specifications in 4 commerce and 7 frontend skills into canonical `references/` and `examples/`.
  - *Target*: `core/skills/commerce/*`, `core/skills/frontend/*`.
- **🟡 [P1-03] Execute Tier 1 Skill Expansion Batch 1 (Top 5 Core Dev Loop)**:
  - *Description*: Add `references/` and `examples/` to `navigate-service`, `agent-delegation`, `security-audit`, `incident-report`, `write-documentation`.
  - *Target*: Corresponding `core/skills/` directories.
- **🟡 [P1-04] Harden `validate-packs.py` and `validate-overlays.py`**:
  - *Description*: Replace string parsing with `yaml.safe_load`; validate overlay skills against `validate-skills.py` standards.
  - *Target*: `core/scripts/validate-packs.py`, `core/scripts/validate-overlays.py`.
- **🟡 [P1-05] Implement Golden Evaluation Framework (GEF) Phase 1**:
  - *Description*: Build `core/scripts/run-golden-evals.py` and author 10 golden test case pairs each for Tier 1 roles (`backend-developer`, `frontend-developer`, `qa-engineer`, `devops-engineer`).
  - *Target*: `core/prompts/golden/`, `core/scripts/`.
- **🔵 [P2-01] Sync Documentation Drift in `core/prompts/README.md`**:
  - *Description*: Update index counts from 58 cases across 5 assets to 68 cases across 6 assets (including `content-quality`).
  - *Target*: `core/prompts/README.md`, `core/prompts/golden/README.md`.
- **🔵 [P2-02] Tag External Site Tests in Pytest**:
  - *Description*: Decorate the 9 site-coupled tests in `tests/test_vesviet_v5_challenge.py` with `@pytest.mark.external_site`.
  - *Target*: `tests/test_vesviet_v5_challenge.py`.

#### 🆕 NEWLY DISCOVERED ISSUES
- **[Architecture] Lacks Python Packaging Metadata**: `pyproject.toml` declares setuptools dependencies but lacks `[tool.setuptools.packages]` configuration. Clarify documentation that Python is used solely for developer tooling and testing, with npm as the canonical distribution vehicle.
- **[Tooling] Redundant Policy Validators**: `validate-policies.py` and `validate-policy-consistency.py` duplicate checks. Consolidate into a single script.

#### ✅ RESOLVED / FIXED (Round 1 to Round 2 Progress)
- **[Fixed ✅] Skill Description "Use when..." Syntax**: Corrected across the 8 identified skills; verified by `validate-skills.py`.
- **[Fixed ✅] Canonical Catalog Sync**: Verified version 5.8.0, 183 skills, 39 roles, 25 workflows, 63 schemas across all internal repository catalogs.
- **[Fixed ✅] AST Lethal Trifecta Scanner Clean**: 169 skills scanned with zero violations, zero unhandled escapes.
- **[Fixed ✅] PromptOps Golden Fixture Expansion**: Added `content-quality` asset (10 case pairs), raising total from 58 to 68 cases.

---

## 6. Empirical Verification & Reproduction Guide

To independently verify every empirical metric, count, and finding in this report, run the following commands in the workspace terminal:

### 6.1 Verify Inventory & Asset Counts
```bash
python3 -c "
import os
core = 'core/skills'
unexp, exp = 0, 0
for cat in os.listdir(core):
    cp = os.path.join(core, cat)
    if os.path.isdir(cp) and not cat.startswith('.'):
        for s in os.listdir(cp):
            sp = os.path.join(cp, s)
            if os.path.isdir(sp) and not s.startswith('.'):
                subs = [e for e in os.listdir(sp) if os.path.isdir(os.path.join(sp, e))]
                if any(d in ('references', 'examples', 'scripts') for d in subs): exp += 1
                else: unexp += 1
print(f'Core Expanded: {exp}, Core Un-expanded: {unexp}, Total Core: {exp + unexp}')
"
# Expected Output: Core Expanded: 65, Core Un-expanded: 104, Total Core: 169
```

### 6.2 Verify Role Risk Ratios
```bash
python3 -c "
import json, os
repo = '.'
with open('adapters/antigravity/role-skill-index.json') as f:
    roles = json.load(f)['roles']
gt_50, gte_50 = [], []
for r, d in roles.items():
    prim = d.get('primary_skills', [])
    unexp = sum(1 for s in prim if not any(os.path.exists(os.path.join('core/skills', c, s, sub)) for c in os.listdir('core/skills') if os.path.isdir(os.path.join('core/skills', c)) for sub in ('references', 'examples', 'scripts')))
    pct = (unexp / len(prim) * 100) if prim else 0
    if pct > 50: gt_50.append(r)
    if pct >= 50: gte_50.append(r)
print(f'Roles with >50%: {len(gt_50)} / {len(roles)} ({len(gt_50)/len(roles)*100:.1f}%); Roles with >=50%: {len(gte_50)} / {len(roles)} ({len(gte_50)/len(roles)*100:.1f}%)')
"
# Expected Output: Roles with >50%: 20 / 39 (51.3%); Roles with >=50%: 23 / 39 (59.0%)
```

### 6.3 Verify Golden Prompt Assets & Dynamic Benchmark Runner
```bash
# 1. Verify Golden Prompt Cases
python3 core/scripts/validate-golden-evals.py
# Expected Output: Golden prompt evals validation passed: 6 assets checked, 68 case pairs verified.

# 2. Run Dynamic Benchmark Evaluation
# Note: run-eval-benchmark.py can be executed directly with zero CLI arguments (defaults resolve to absolute paths):
.venv/bin/python core/skills/ai-agent/agent-evaluation/scripts/run-eval-benchmark.py

# Alternatively, if passing CLI flags, use absolute resolved paths (or $(pwd)/...) to satisfy Path.relative_to():
# .venv/bin/python core/skills/ai-agent/agent-evaluation/scripts/run-eval-benchmark.py \
#   --manifest "$(pwd)/core/skills/ai-agent/agent-evaluation/resources/eval-benchmarks/eval-manifest.yaml" \
#   --cases "$(pwd)/core/skills/ai-agent/agent-evaluation/resources/eval-benchmarks/eval-cases.json" \
#   --output output/agent-eval-report.json
# Expected Output: 15/15 cases passed, valid output/agent-eval-report.json emitted.
```

### 6.4 Verify Test Suite Coverage & Reports File Count
```bash
# 1. Count unreferenced skills in tests
python3 -c "
import glob, os
skills = [os.path.basename(s) for s in glob.glob('core/skills/*/*') + glob.glob('overlays/*/skills/*') if os.path.isdir(s)]
test_code = '\n'.join(open(f).read() for f in glob.glob('tests/test_*.py'))
unreferenced = [s for s in skills if s not in test_code]
print(f'Total skills: {len(skills)}, Unreferenced: {len(unreferenced)} ({len(unreferenced)/len(skills)*100:.1f}%)')
"
# Expected Output: Total skills: 183, Unreferenced: 99 (54.1%)

# 2. Count reports/ root markdown files
ls -1 reports/*.md | wc -l
# Expected Output: 18 (violates core/rules/knowledge.md limit <= 5)
```

### 6.5 Master Verification Suite Execution
```bash
# Core parallel validators
python3 core/scripts/validate-all.py --parallel
# Expected Output: All core validators passed (exit code 0)

# Pytest test suite
.venv/bin/python -m pytest tests -q
# Expected Output: 915 passed, 9 skipped in ~53s (exit code 0)

# Node CLI packaging & test suite
node --test tests/npm/cli.test.mjs
# Expected Output: 8 passed (exit code 0)
```

---
*Report concluded. All findings backed by deterministic code execution and filesystem proof. Master copy authored at `reports/agent-skills-round-2-audit-report.md`.*
