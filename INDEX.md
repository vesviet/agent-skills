# Agent-Skills Master Index & Router

> **Location:** `core/` & `overlays/` | **Version:** `5.7.1` (A2A 1.0 + Antigravity)
> **Total Catalog:** **38 Roles** | **182 Skills** (167 Core + 15 Overlays) | **25 Workflows** | **60 Data Contracts**

---

## ⚡ Fast Invocation Protocol (`@<role>` & `@<skill>`)

When you mention `@<role>` and/or `@<skill>` in chat, Antigravity resolves them immediately using this index:

```markdown
# Single Role + Skill Example
@writer @research_and_writing - Viết bài hướng dẫn về Antigravity 2.0

# Developer Example
@backend @add_api_endpoint - Tạo REST API endpoint quản lý user orders

# Swarm Coordinator Example
@coordinator @a2a - Phối hợp @frontend và @backend hoàn thiện tính năng checkout
```

### Resolution Rules
1. **Role Matching:** `@<role>` resolves by exact name (e.g., `@content-writer`) or common alias (e.g., `@writer` → `content-writer`, `@be` → `backend-developer`).
2. **Skill Matching:** `@<skill>` resolves by exact name (e.g., `@conduct-research`), snake_case (e.g., `@conduct_research`), or composite alias (e.g., `@research_and_writing` → `conduct-research` + `write-article`).
3. **Automatic Loading:** The agent loads `core/roles/<role>.md` and all resolved `core/skills/<cat>/<skill>/SKILL.md` before executing.
4. **Contract Output:** Structured outputs must validate against `core/contracts/schemas/<schema>.json`.

---

## 🎭 Role Directory (38 Roles)

| Role Slug | Title | Common Aliases | Primary Skills | Role File |
|:---|:---|:---|:---|:---|
| **`@3d-graphics-engineer`** | 3D Graphics Engineer | `@3d`, `@r3f`, `@threejs` | `debug-3d-scene`, `integrate-r3f-three-legacy`, `optimize-3d-assets` | [`core/roles/3d-graphics-engineer.md`](./core/roles/3d-graphics-engineer.md) |
| **`@agent-coordinator`** | Agent Coordinator | `@coordinator`, `@swarm-coordinator` | `agent-a2a-protocol`, `agent-delegation`, `agent-graph-orchestration` *(+10 more)* | [`core/roles/agent-coordinator.md`](./core/roles/agent-coordinator.md) |
| **`@agent-discovery-engineer`** | Agent Discovery Engineer | `@discovery`, `@agent-discovery` | `manage-auth-md`, `configure-oauth-metadata`, `debug-identity-provider` *(+5 more)* | [`core/roles/agent-discovery-engineer.md`](./core/roles/agent-discovery-engineer.md) |
| **`@ai-systems-engineer`** | AI Systems Engineer | `@ai`, `@ml`, `@llm` | `deploy-vllm-inference`, `setup-llm-gateway`, `setup-gpu-finops` *(+2 more)* | [`core/roles/ai-systems-engineer.md`](./core/roles/ai-systems-engineer.md) |
| **`@aws-engineer`** | AWS Engineer | `@aws`, `@cloud` | `aws-infrastructure`, `setup-deployment`, `add-telemetry-instrumentation` | [`core/roles/aws-engineer.md`](./core/roles/aws-engineer.md) |
| **`@backend-developer`** | Backend Developer | `@backend`, `@be`, `@backend-dev` | `add-api-endpoint`, `add-event-handler`, `add-service-client` *(+9 more)* | [`core/roles/backend-developer.md`](./core/roles/backend-developer.md) |
| **`@business-analyst`** | Business Analyst | `@ba`, `@business` | `analyze-business-requirements`, `elicit-requirements`, `write-use-cases` *(+3 more)* | [`core/roles/business-analyst.md`](./core/roles/business-analyst.md) |
| **`@cloudflare-engineer`** | Cloudflare Engineer | `@cloudflare`, `@cf`, `@workers` | `wrangler`, `durable-objects`, `agents-sdk` *(+11 more)* | [`core/roles/cloudflare-engineer.md`](./core/roles/cloudflare-engineer.md) |
| **`@content-manager`** | Content Manager | `@content-mgr`, `@content-lead` | `design-content-strategy`, `audit-content` | [`core/roles/content-manager.md`](./core/roles/content-manager.md) |
| **`@content-writer`** | Content Writer | `@writer`, `@copywriter`, `@author`, `@article-writer`, `@blog-writer` | `write-article`, `write-copy`, `repurpose-content` *(+1 more)* | [`core/roles/content-writer.md`](./core/roles/content-writer.md) |
| **`@data-analyst`** | Data Analyst | `@da`, `@data-analytics` | `analyze-data`, `query-analytical-engine`, `xlsx` | [`core/roles/data-analyst.md`](./core/roles/data-analyst.md) |
| **`@data-engineer`** | Data Engineer | `@de`, `@data-eng` | `build-data-pipeline`, `database-maintenance`, `create-migration` *(+1 more)* | [`core/roles/data-engineer.md`](./core/roles/data-engineer.md) |
| **`@devops-engineer`** | DevOps Engineer | `@devops`, `@infra`, `@infrastructure` | `setup-deployment`, `deploy-aws-eks-workloads`, `debug-runtime-platform` *(+5 more)* | [`core/roles/devops-engineer.md`](./core/roles/devops-engineer.md) |
| **`@ecommerce-engineer`** | Ecommerce Engineer | `@ecommerce`, `@ecom` | `integrate-payment-gateway`, `handle-checkout-flow`, `manage-product-catalog` *(+2 more)* | [`core/roles/ecommerce-engineer.md`](./core/roles/ecommerce-engineer.md) |
| **`@frontend-developer`** | Frontend Developer | `@frontend`, `@fe`, `@frontend-dev`, `@ui-developer` | `accessibility-review`, `add-page-route`, `add-ui-component` *(+12 more)* | [`core/roles/frontend-developer.md`](./core/roles/frontend-developer.md) |
| **`@game-developer`** | Game Developer | `@game-dev`, `@gamedev`, `@game`, `@game-engineer`, `@gameplay-engineer` | `integrate-game-engine`, `develop-gameplay-systems`, `architect-ecs-systems` *(+17 more)* | [`core/roles/game-developer.md`](./core/roles/game-developer.md) |
| **`@mmo-engineer`** | MMO Engineer | `@mmo`, `@affiliate`, `@growth`, `@growth-lead`, `@growth-engineer`, `@media-buyer`, `@affiliate-marketer` | `deploy-mmo-infrastructure`, `setup-tracking-system`, `create-automation-script` *(+4 more)* | [`core/roles/mmo-engineer.md`](./core/roles/mmo-engineer.md) |
| **`@mobile-engineer`** | Mobile Engineer | `@mobile`, `@flutter`, `@react-native` | `develop-mobile-app`, `deploy-mobile-app`, `add-ui-component` *(+5 more)* | [`core/roles/mobile-engineer.md`](./core/roles/mobile-engineer.md) |
| **`@product-manager`** | Product Manager | `@pm`, `@prod-mgr`, `@product-owner`, `@po` | `define-product-strategy`, `prioritize-roadmap`, `model-saas-metrics` *(+2 more)* | [`core/roles/product-manager.md`](./core/roles/product-manager.md) |
| **`@project-manager`** | Project Manager | `@pjm`, `@proj-mgr`, `@scrum-master` | `meeting-review` | [`core/roles/project-manager.md`](./core/roles/project-manager.md) |
| **`@prompt-engineer`** | Prompt Engineer | `@prompt`, `@promptops` | `context-optimization`, `memory-hygiene` | [`core/roles/prompt-engineer.md`](./core/roles/prompt-engineer.md) |
| **`@qa-engineer`** | QA Engineer | `@qa`, `@tester`, `@test-engineer` | `write-tests`, `frontend-testing`, `systematic-debugging` *(+9 more)* | [`core/roles/qa-engineer.md`](./core/roles/qa-engineer.md) |
| **`@researcher`** | Researcher | `@research`, `@deep-research` | `conduct-research` | [`core/roles/researcher.md`](./core/roles/researcher.md) |
| **`@reviewer`** | Reviewer | `@code-reviewer`, `@pr-reviewer` | `review-code`, `review-service`, `configure-mcp` *(+2 more)* | [`core/roles/reviewer.md`](./core/roles/reviewer.md) |
| **`@sdet`** | SDET | `@test-automation`, `@automation-engineer` | `agent-evaluation` | [`core/roles/sdet.md`](./core/roles/sdet.md) |
| **`@security-engineer`** | Security Engineer | `@security`, `@sec`, `@appsec`, `@secops` | `security-audit`, `manage-secrets`, `supply-chain-security` *(+4 more)* | [`core/roles/security-engineer.md`](./core/roles/security-engineer.md) |
| **`@seo-analyst`** | SEO Analyst | `@seo`, `@seo-specialist`, `@seo-expert` | `optimize-seo`, `audit-technical-seo`, `implement-schema-markup` *(+2 more)* | [`core/roles/seo-analyst.md`](./core/roles/seo-analyst.md) |
| **`@solution-architect`** | Solution Architect | `@architect`, `@solution-arch`, `@solutions-architect` | `write-tech-radar`, `meeting-review` | [`core/roles/solution-architect.md`](./core/roles/solution-architect.md) |
| **`@sre`** | Site Reliability Engineer | `@reliability` | `debug-runtime-platform`, `troubleshoot-service`, `add-telemetry-instrumentation` *(+3 more)* | [`core/roles/sre.md`](./core/roles/sre.md) |
| **`@system-engineer`** | System Engineer | `@sysadmin`, `@system`, `@systems-engineer` | `system-design`, `performance-profiling`, `debug-runtime-platform` *(+5 more)* | [`core/roles/system-engineer.md`](./core/roles/system-engineer.md) |
| **`@task-planner`** | Task Planner | `@planner`, `@task-scheduler` | `design-ux-flow`, `plan-technical-delivery` | [`core/roles/task-planner.md`](./core/roles/task-planner.md) |
| **`@teacher`** | Teacher | `@instructor`, `@educator`, `@mentor` | `design-learning-plan`, `create-exercises`, `grade-and-review` | [`core/roles/teacher.md`](./core/roles/teacher.md) |
| **`@technical-architect`** | Technical Architect | `@tech-architect`, `@enterprise-architect` | `system-design`, `agent-panel-meeting`, `meeting-review` *(+3 more)* | [`core/roles/technical-architect.md`](./core/roles/technical-architect.md) |
| **`@technical-lead`** | Technical Lead | `@lead`, `@tech-lead`, `@engineering-lead` | `plan-technical-delivery`, `review-code`, `meeting-review` *(+4 more)* | [`core/roles/technical-lead.md`](./core/roles/technical-lead.md) |
| **`@technical-writer`** | Technical Writer | `@tech-writer`, `@doc-writer`, `@docs`, `@documentation-writer` | `write-documentation`, `release-notes`, `configure-llms-txt` *(+1 more)* | [`core/roles/technical-writer.md`](./core/roles/technical-writer.md) |
| **`@ui-ux-designer`** | UI/UX Designer | `@designer`, `@ui`, `@ux`, `@ui-ux`, `@uiux` | `design-ux-flow`, `design-review`, `design-system-engineering` *(+3 more)* | [`core/roles/ui-ux-designer.md`](./core/roles/ui-ux-designer.md) |
| **`@vietnam-accounting-specialist`** | Vietnam Accounting Specialist | `@accounting`, `@accountant`, `@ke-toan`, `@vietnam-accounting` | `manage-vietnam-accounting` | [`core/roles/vietnam-accounting-specialist.md`](./core/roles/vietnam-accounting-specialist.md) |
| **`@vietnam-legal-counsel`** | Vietnam Legal Counsel | `@lawyer`, `@luat-su`, `@legal`, `@legal-counsel` | `manage-vietnam-legal`, `audit-ai-compliance`, `draft-legal-opinion` | [`core/roles/vietnam-legal-counsel.md`](./core/roles/vietnam-legal-counsel.md) |

---

## 🛠️ Skill Directory (182 Skills)

### Category: `agent` (24 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@agent-a2a-protocol`** | Implement the full A2A 1.0 task lifecycle including Agent Card discovery, JSON-RPC invoke/stream, ta... | [`core/skills/agent/agent-a2a-protocol/SKILL.md`](./core/skills/agent/agent-a2a-protocol/SKILL.md) |
| **`@agent-context-management`** | Manage working context across long or multi-step agent tasks by tracking user intent, current phase,... | [`core/skills/agent/agent-context-management/SKILL.md`](./core/skills/agent/agent-context-management/SKILL.md) |
| **`@agent-delegation`** | Delegate scoped sub-tasks from a supervisor agent to specialist worker agents using structured A2A t... | [`core/skills/agent/agent-delegation/SKILL.md`](./core/skills/agent/agent-delegation/SKILL.md) |
| **`@agent-graph-orchestration`** | Model multi-phase delivery as a directed graph with parallel branches, phase gates, and A2A delegati... | [`core/skills/agent/agent-graph-orchestration/SKILL.md`](./core/skills/agent/agent-graph-orchestration/SKILL.md) |
| **`@agent-handoff`** | Produce concise agent handoffs, status updates, and completion summaries that preserve phase state, ... | [`core/skills/agent/agent-handoff/SKILL.md`](./core/skills/agent/agent-handoff/SKILL.md) |
| **`@agent-memory-compaction`** | Use when compacting long-running agent conversation context into an anchored 10-slot working state, ... | [`core/skills/agent/agent-memory-compaction/SKILL.md`](./core/skills/agent/agent-memory-compaction/SKILL.md) |
| **`@agent-model-routing`** | Select the most cost-effective model for each task or sub-task based on complexity, risk tier, and b... | [`core/skills/agent/agent-model-routing/SKILL.md`](./core/skills/agent/agent-model-routing/SKILL.md) |
| **`@agent-observability`** | Trace agent reasoning chains, tool call sequences, context injections, and token costs to enable deb... | [`core/skills/agent/agent-observability/SKILL.md`](./core/skills/agent/agent-observability/SKILL.md) |
| **`@agent-panel-meeting`** | Orchestrate a 6-round, multi-role cross-examination panel meeting to debate architecture, code, or f... | [`core/skills/agent/agent-panel-meeting/SKILL.md`](./core/skills/agent/agent-panel-meeting/SKILL.md) |
| **`@agent-prompt-lifecycle`** | Manage prompt assets through their full lifecycle including versioning, evaluation against golden da... | [`core/skills/agent/agent-prompt-lifecycle/SKILL.md`](./core/skills/agent/agent-prompt-lifecycle/SKILL.md) |
| **`@agent-quality-gate`** | Run and interpret repository quality gates for agent-delivered changes, including validators, lint, ... | [`core/skills/agent/agent-quality-gate/SKILL.md`](./core/skills/agent/agent-quality-gate/SKILL.md) |
| **`@agent-semantic-memory`** | Read from and write to persistent memory stores so agents retain codebase patterns, past fixes, and ... | [`core/skills/agent/agent-semantic-memory/SKILL.md`](./core/skills/agent/agent-semantic-memory/SKILL.md) |
| **`@agent-tool-orchestration`** | Plan and sequence agent tool use by choosing the smallest reliable tool, controlling work phase by p... | [`core/skills/agent/agent-tool-orchestration/SKILL.md`](./core/skills/agent/agent-tool-orchestration/SKILL.md) |
| **`@architect-mcp-server`** | Architect enterprise-grade Model Context Protocol (MCP) servers, tool surfaces, schemas, transport p... | [`core/skills/agent/architect-mcp-server/SKILL.md`](./core/skills/agent/architect-mcp-server/SKILL.md) |
| **`@configure-agent-commerce`** | Implements agentic commerce standards — x402 and Stripe's Machine Payments Protocol (MPP) for HTTP 4... | [`core/skills/agent/configure-agent-commerce/SKILL.md`](./core/skills/agent/configure-agent-commerce/SKILL.md) |
| **`@configure-agent-headers`** | Exposes well-known agentic endpoints via RFC 8288 HTTP Link headers and optional DNS-AID SVCB record... | [`core/skills/agent/configure-agent-headers/SKILL.md`](./core/skills/agent/configure-agent-headers/SKILL.md) |
| **`@configure-agent-skills`** | Creates and manages the agentskills.io manifest index at `/.well-known/agent-skills/index.json`, exp... | [`core/skills/agent/configure-agent-skills/SKILL.md`](./core/skills/agent/configure-agent-skills/SKILL.md) |
| **`@configure-mcp`** | Sets up the full MCP presence for a web service — experimental Server Card discovery, WebMCP browser... | [`core/skills/agent/configure-mcp/SKILL.md`](./core/skills/agent/configure-mcp/SKILL.md) |
| **`@configure-oauth-metadata`** | Configures well-known OAuth 2.0 and OpenID Connect discovery endpoints (`oauth-protected-resource`, ... | [`core/skills/agent/configure-oauth-metadata/SKILL.md`](./core/skills/agent/configure-oauth-metadata/SKILL.md) |
| **`@debug-identity-provider`** | Diagnoses and resolves failures reported by WorkOS Agentic Registration scanners, `isitagentready.co... | [`core/skills/agent/debug-identity-provider/SKILL.md`](./core/skills/agent/debug-identity-provider/SKILL.md) |
| **`@decompose-agentic-system`** | Architect recursive system and task decomposition for large-scale multi-agent architectures (100+ fi... | [`core/skills/agent/decompose-agentic-system/SKILL.md`](./core/skills/agent/decompose-agentic-system/SKILL.md) |
| **`@manage-agent-identity`** | Manages the full lifecycle of Non-Human Identities (NHI) for AI agent sessions — including provision... | [`core/skills/agent/manage-agent-identity/SKILL.md`](./core/skills/agent/manage-agent-identity/SKILL.md) |
| **`@manage-api-catalog`** | Use when publishing and maintaining RFC 9727 API Catalog registries for automated API discovery by a... | [`core/skills/agent/manage-api-catalog/SKILL.md`](./core/skills/agent/manage-api-catalog/SKILL.md) |
| **`@manage-auth-md`** | Use when creating, updating, or auditing the /auth.md file at the repository or domain root to ensur... | [`core/skills/agent/manage-auth-md/SKILL.md`](./core/skills/agent/manage-auth-md/SKILL.md) |

### Category: `ai` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@deploy-vllm-inference`** | Deploy, configure, scale, and optimize high-throughput LLM inference workloads using the vLLM V1 eng... | [`core/skills/ai/deploy-vllm-inference/SKILL.md`](./core/skills/ai/deploy-vllm-inference/SKILL.md) |

### Category: `ai-agent` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@agent-evaluation`** | Use when constructing representative agent evaluation benchmark suites, defining scoring rubrics, im... | [`core/skills/ai-agent/agent-evaluation/SKILL.md`](./core/skills/ai-agent/agent-evaluation/SKILL.md) |
| **`@context-optimization`** | Use when optimizing LLM agent context windows, allocating token budgets, pruning semantic duplicates... | [`core/skills/ai-agent/context-optimization/SKILL.md`](./core/skills/ai-agent/context-optimization/SKILL.md) |
| **`@memory-hygiene`** | Use when auditing, triaging, compacting, and archiving agent persistent memory stores (MEMORY.md, .c... | [`core/skills/ai-agent/memory-hygiene/SKILL.md`](./core/skills/ai-agent/memory-hygiene/SKILL.md) |

### Category: `backend` (8 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@add-api-endpoint`** | Add or modify a service endpoint by updating the local API contract, boundary validation, handler fl... | [`core/skills/backend/add-api-endpoint/SKILL.md`](./core/skills/backend/add-api-endpoint/SKILL.md) |
| **`@add-event-handler`** | Add or modify event publishers, consumers, or subscriber flows by following the repo's event contrac... | [`core/skills/backend/add-event-handler/SKILL.md`](./core/skills/backend/add-event-handler/SKILL.md) |
| **`@add-service-client`** | Add or modify a service-to-service client or downstream integration by following the repo's transpor... | [`core/skills/backend/add-service-client/SKILL.md`](./core/skills/backend/add-service-client/SKILL.md) |
| **`@build-mcp-server`** | Scaffolds and implements a new Model Context Protocol (MCP) server. Use when exposing new backend to... | [`core/skills/backend/build-mcp-server/SKILL.md`](./core/skills/backend/build-mcp-server/SKILL.md) |
| **`@implement-auth`** | Implement secure authentication, OAuth2 PKCE flows, session lifecycles, JWT rotation with Redis revo... | [`core/skills/backend/implement-auth/SKILL.md`](./core/skills/backend/implement-auth/SKILL.md) |
| **`@implement-structured-outputs`** | Implements strict constrained decoding and validation for LLM responses. Use when enforcing JSON Sch... | [`core/skills/backend/implement-structured-outputs/SKILL.md`](./core/skills/backend/implement-structured-outputs/SKILL.md) |
| **`@optimize-postgres`** | Optimize PostgreSQL performance, serverless connection pooling, ephemeral database branching, EXPLAI... | [`core/skills/backend/optimize-postgres/SKILL.md`](./core/skills/backend/optimize-postgres/SKILL.md) |
| **`@scaffold-new-service`** | Bootstrap a new service or bounded component from repo-local templates and conventions. Use when cre... | [`core/skills/backend/scaffold-new-service/SKILL.md`](./core/skills/backend/scaffold-new-service/SKILL.md) |

### Category: `business` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@elicit-requirements`** | Elicit business requirements from stakeholders using Funnel Questioning (Open, Probing, Closed), the... | [`core/skills/business/elicit-requirements/SKILL.md`](./core/skills/business/elicit-requirements/SKILL.md) |
| **`@trace-requirements-impact`** | Build Requirements Traceability Matrices (RTM), run BFS change-request impact analysis across requir... | [`core/skills/business/trace-requirements-impact/SKILL.md`](./core/skills/business/trace-requirements-impact/SKILL.md) |
| **`@write-use-cases`** | Scope, structure, and document production-grade Use Cases using Karl Wiegers 13-field template, Alis... | [`core/skills/business/write-use-cases/SKILL.md`](./core/skills/business/write-use-cases/SKILL.md) |

### Category: `commerce` (4 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@handle-checkout-flow`** | Design and implement the end-to-end checkout flow including cart management, tax and shipping calcul... | [`core/skills/commerce/handle-checkout-flow/SKILL.md`](./core/skills/commerce/handle-checkout-flow/SKILL.md) |
| **`@integrate-payment-gateway`** | Integrate or extend a payment gateway (Stripe, VNPay, PayPal, Momo, etc.) into an e-commerce applica... | [`core/skills/commerce/integrate-payment-gateway/SKILL.md`](./core/skills/commerce/integrate-payment-gateway/SKILL.md) |
| **`@manage-order-fulfillment`** | Implement and manage the post-purchase order lifecycle including order status management, packing, s... | [`core/skills/commerce/manage-order-fulfillment/SKILL.md`](./core/skills/commerce/manage-order-fulfillment/SKILL.md) |
| **`@manage-product-catalog`** | Build or maintain a product catalog including product creation, variant management (size, color, SKU... | [`core/skills/commerce/manage-product-catalog/SKILL.md`](./core/skills/commerce/manage-product-catalog/SKILL.md) |

### Category: `content` (6 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@audit-content`** | Run a structured content refresh cycle on an existing published piece — audit current performance an... | [`core/skills/content/audit-content/SKILL.md`](./core/skills/content/audit-content/SKILL.md) |
| **`@design-content-strategy`** | Design holistic content portfolio strategies, pillar-and-cluster architectures, topical authority mo... | [`core/skills/content/design-content-strategy/SKILL.md`](./core/skills/content/design-content-strategy/SKILL.md) |
| **`@optimize-seo`** | Research search intent, define keywords, produce SEO content briefs, audit on-page elements, optimiz... | [`core/skills/content/optimize-seo/SKILL.md`](./core/skills/content/optimize-seo/SKILL.md) |
| **`@repurpose-content`** | Extract and format micro-content variants (social threads, newsletters, short video scripts) from a ... | [`core/skills/content/repurpose-content/SKILL.md`](./core/skills/content/repurpose-content/SKILL.md) |
| **`@write-article`** | Plan, research, outline, and draft long-form articles and blog posts with explicit evidence discipli... | [`core/skills/content/write-article/SKILL.md`](./core/skills/content/write-article/SKILL.md) |
| **`@write-copy`** | Craft high-conversion direct-response marketing copy, landing pages, sales funnels, email sequences,... | [`core/skills/content/write-copy/SKILL.md`](./core/skills/content/write-copy/SKILL.md) |

### Category: `document` (4 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@docx`** | "Use when creating, editing, inspecting, or formatting Microsoft Word (.docx) documents, enforcing D... | [`core/skills/document/docx/SKILL.md`](./core/skills/document/docx/SKILL.md) |
| **`@pdf`** | "Use when reading, extracting, creating, or modifying PDF documents, parsing text and tables via pdf... | [`core/skills/document/pdf/SKILL.md`](./core/skills/document/pdf/SKILL.md) |
| **`@pptx`** | "Use when creating, editing, or inspecting PowerPoint (.pptx/.potx) presentations, authoring decks v... | [`core/skills/document/pptx/SKILL.md`](./core/skills/document/pptx/SKILL.md) |
| **`@xlsx`** | "Use when creating, analyzing, or modifying Microsoft Excel (.xlsx/.xlsm) workbooks, enforcing the Z... | [`core/skills/document/xlsx/SKILL.md`](./core/skills/document/xlsx/SKILL.md) |

### Category: `documentation` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@configure-llms-txt`** | Create and maintain the llms.txt and llms-full.txt files for a domain or project, making documentati... | [`core/skills/documentation/configure-llms-txt/SKILL.md`](./core/skills/documentation/configure-llms-txt/SKILL.md) |
| **`@write-documentation`** | Draft or update technical documentation by following the repo's existing doc structure, audience nee... | [`core/skills/documentation/write-documentation/SKILL.md`](./core/skills/documentation/write-documentation/SKILL.md) |
| **`@write-tech-radar`** | Draft or update a technology radar entry by summarizing context, trade-offs, recommendation, and ado... | [`core/skills/documentation/write-tech-radar/SKILL.md`](./core/skills/documentation/write-tech-radar/SKILL.md) |

### Category: `education` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@create-exercises`** | Design educational assignments, practice tests, and quizzes following designated curriculum matrices... | [`core/skills/education/create-exercises/SKILL.md`](./core/skills/education/create-exercises/SKILL.md) |
| **`@design-learning-plan`** | Create a structured, curriculum-aligned learning plan or syllabus following ZPD pathways, SMART obje... | [`core/skills/education/design-learning-plan/SKILL.md`](./core/skills/education/design-learning-plan/SKILL.md) |
| **`@grade-and-review`** | Evaluate learner work and provide constructive feedback on the designated grading scale. Use when gr... | [`core/skills/education/grade-and-review/SKILL.md`](./core/skills/education/grade-and-review/SKILL.md) |

### Category: `foundation` (18 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@accessibility-review`** | Audit UI for keyboard navigation, focus order, screen-reader labels, color contrast, motion preferen... | [`core/skills/foundation/accessibility-review/SKILL.md`](./core/skills/foundation/accessibility-review/SKILL.md) |
| **`@ai-risk-assessment`** | Assess AI/ML system risks using NIST AI RMF 1.0 (Govern/Map/Measure/Manage) and NIST AI 600-1 GenAI ... | [`core/skills/foundation/ai-risk-assessment/SKILL.md`](./core/skills/foundation/ai-risk-assessment/SKILL.md) |
| **`@combinatorial-testing`** | Design pairwise and n-way combinatorial test suites using orthogonal arrays and covering parameter m... | [`core/skills/foundation/combinatorial-testing/SKILL.md`](./core/skills/foundation/combinatorial-testing/SKILL.md) |
| **`@conduct-research`** | Execute iterative, deeply-verified research to discover, validate, and synthesize complex informatio... | [`core/skills/foundation/conduct-research/SKILL.md`](./core/skills/foundation/conduct-research/SKILL.md) |
| **`@create-migration`** | Create safe schema or data migrations by following the repo's local migration tool, naming rules, ro... | [`core/skills/foundation/create-migration/SKILL.md`](./core/skills/foundation/create-migration/SKILL.md) |
| **`@design-review`** | Review UX flows, visual hierarchy, interaction patterns, and design-system alignment against specs a... | [`core/skills/foundation/design-review/SKILL.md`](./core/skills/foundation/design-review/SKILL.md) |
| **`@design-ux-flow`** | Design or refine a UX flow by defining user goals, preserved behavior, screen states, interaction ru... | [`core/skills/foundation/design-ux-flow/SKILL.md`](./core/skills/foundation/design-ux-flow/SKILL.md) |
| **`@discernment-nudge`** | "Use when evaluating high-stakes architectural plans, financial projections, or critical code review... | [`core/skills/foundation/discernment-nudge/SKILL.md`](./core/skills/foundation/discernment-nudge/SKILL.md) |
| **`@hostile-component-stress-testing`** | Use when subjecting UI components to hostile edge-case inputs across 6 scenario axes on an isolated ... | [`core/skills/foundation/hostile-component-stress-testing/SKILL.md`](./core/skills/foundation/hostile-component-stress-testing/SKILL.md) |
| **`@incident-report`** | Capture, structure, and communicate an incident from triage through resolution and prevention. Use w... | [`core/skills/foundation/incident-report/SKILL.md`](./core/skills/foundation/incident-report/SKILL.md) |
| **`@performance-profiling`** | Investigate latency, throughput, memory, and contention issues by baselining, profiling hot paths, a... | [`core/skills/foundation/performance-profiling/SKILL.md`](./core/skills/foundation/performance-profiling/SKILL.md) |
| **`@plan-technical-delivery`** | Turn architecture decisions and requirements into a delivery-ready technical plan with slices, quali... | [`core/skills/foundation/plan-technical-delivery/SKILL.md`](./core/skills/foundation/plan-technical-delivery/SKILL.md) |
| **`@playwright-evidence-qa`** | Use when diagnosing Playwright test failures using tripartite evidence triage (screenshot, DOM snaps... | [`core/skills/foundation/playwright-evidence-qa/SKILL.md`](./core/skills/foundation/playwright-evidence-qa/SKILL.md) |
| **`@release-notes`** | Draft, structure, and review release notes for a software change so that users, operators, and downs... | [`core/skills/foundation/release-notes/SKILL.md`](./core/skills/foundation/release-notes/SKILL.md) |
| **`@systematic-debugging`** | Apply 4-phase systematic root cause analysis (Observe, Hypothesize, Test, Fix) and verification-befo... | [`core/skills/foundation/systematic-debugging/SKILL.md`](./core/skills/foundation/systematic-debugging/SKILL.md) |
| **`@webapp-server-runner`** | "Use when executing local web application test suites, managing multi-server background lifecycles v... | [`core/skills/foundation/webapp-server-runner/SKILL.md`](./core/skills/foundation/webapp-server-runner/SKILL.md) |
| **`@write-product-brief`** | Write or refine a product brief that makes user value, business outcome, preserved behavior, affecte... | [`core/skills/foundation/write-product-brief/SKILL.md`](./core/skills/foundation/write-product-brief/SKILL.md) |
| **`@write-tests`** | Add or update tests by following repo-local test conventions, choosing the right test scope, isolati... | [`core/skills/foundation/write-tests/SKILL.md`](./core/skills/foundation/write-tests/SKILL.md) |

### Category: `frontend` (16 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@add-page-route`** | Add or modify a page, screen, or route by following the repo's navigation, data-loading, layout, and... | [`core/skills/frontend/add-page-route/SKILL.md`](./core/skills/frontend/add-page-route/SKILL.md) |
| **`@add-ui-component`** | Add or evolve a reusable UI component by following the repo's design system, composition patterns, a... | [`core/skills/frontend/add-ui-component/SKILL.md`](./core/skills/frontend/add-ui-component/SKILL.md) |
| **`@anti-ui-slop-finish-gate`** | Use when conducting pre-staging UI finish reviews, enforcing 100% interaction state coverage, and ap... | [`core/skills/frontend/anti-ui-slop-finish-gate/SKILL.md`](./core/skills/frontend/anti-ui-slop-finish-gate/SKILL.md) |
| **`@component-composition`** | Architect scalable UI components using compound components, Radix-style asChild slot delegation, hea... | [`core/skills/frontend/component-composition/SKILL.md`](./core/skills/frontend/component-composition/SKILL.md) |
| **`@design-md-specification`** | Use when generating machine-readable DESIGN.md documents, specifying YAML frontmatter design tokens,... | [`core/skills/frontend/design-md-specification/SKILL.md`](./core/skills/frontend/design-md-specification/SKILL.md) |
| **`@design-system-engineering`** | Use when engineering design token architectures, calculating concentric border radii, establishing p... | [`core/skills/frontend/design-system-engineering/SKILL.md`](./core/skills/frontend/design-system-engineering/SKILL.md) |
| **`@frontend-micro-polish`** | Use when applying micro-typographic polish, optical padding compensations, mobile input zoom guards,... | [`core/skills/frontend/frontend-micro-polish/SKILL.md`](./core/skills/frontend/frontend-micro-polish/SKILL.md) |
| **`@frontend-testing`** | Add or improve frontend test coverage by choosing the right UI test scope, reusing local tooling, an... | [`core/skills/frontend/frontend-testing/SKILL.md`](./core/skills/frontend/frontend-testing/SKILL.md) |
| **`@implement-view-transitions`** | Implement fluid, native-feeling page and state transitions using CSS View Transitions API, React 19 ... | [`core/skills/frontend/implement-view-transitions/SKILL.md`](./core/skills/frontend/implement-view-transitions/SKILL.md) |
| **`@implement-webmcp`** | Exposes browser context, DOM state, and client-side actions to AI agents via WebMCP. Use when enabli... | [`core/skills/frontend/implement-webmcp/SKILL.md`](./core/skills/frontend/implement-webmcp/SKILL.md) |
| **`@integrate-api-client`** | Connect frontend code to backend APIs by following the repo's request, caching, auth, error-handling... | [`core/skills/frontend/integrate-api-client/SKILL.md`](./core/skills/frontend/integrate-api-client/SKILL.md) |
| **`@interactive-component-workbench`** | Use when building scratch-route component workbenches with search-param state switchers and multi-va... | [`core/skills/frontend/interactive-component-workbench/SKILL.md`](./core/skills/frontend/interactive-component-workbench/SKILL.md) |
| **`@motion-performance-engineering`** | Use when engineering 60fps/120fps hardware-accelerated animations, restricting transitions to compos... | [`core/skills/frontend/motion-performance-engineering/SKILL.md`](./core/skills/frontend/motion-performance-engineering/SKILL.md) |
| **`@setup-design-system`** | Configure a scalable design system, styling framework, and component architecture for a frontend pro... | [`core/skills/frontend/setup-design-system/SKILL.md`](./core/skills/frontend/setup-design-system/SKILL.md) |
| **`@setup-visual-regression`** | Configure automated visual diffing for UI components and pages. Use when establishing pixel-level re... | [`core/skills/frontend/setup-visual-regression/SKILL.md`](./core/skills/frontend/setup-visual-regression/SKILL.md) |
| **`@web-quality-audit`** | Use when conducting Core Web Vitals audits, profiling Long Animation Frames and interaction responsi... | [`core/skills/frontend/web-quality-audit/SKILL.md`](./core/skills/frontend/web-quality-audit/SKILL.md) |

### Category: `gamedev` (20 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@abstract-input-actions`** | Abstracts hardware-agnostic input action mappings, chorded and buffered inputs, radial analog deadzo... | [`core/skills/gamedev/abstract-input-actions/SKILL.md`](./core/skills/gamedev/abstract-input-actions/SKILL.md) |
| **`@architect-ecs-systems`** | Architect data-oriented Entity Component System (ECS) architectures, archetype storages, and cache-f... | [`core/skills/gamedev/architect-ecs-systems/SKILL.md`](./core/skills/gamedev/architect-ecs-systems/SKILL.md) |
| **`@author-game-ai`** | Authors modular game AI architectures using Behavior Trees (BT), shared and local blackboards, Utili... | [`core/skills/gamedev/author-game-ai/SKILL.md`](./core/skills/gamedev/author-game-ai/SKILL.md) |
| **`@automate-game-publishing`** | Automate headless cross-platform game builds, Steamworks SteamPipe depot uploads, itch.io Butler CLI... | [`core/skills/gamedev/automate-game-publishing/SKILL.md`](./core/skills/gamedev/automate-game-publishing/SKILL.md) |
| **`@build-game-ui-ux`** | Builds responsive game UI and HUD architectures featuring multi-resolution canvas scaling, 9-slice a... | [`core/skills/gamedev/build-game-ui-ux/SKILL.md`](./core/skills/gamedev/build-game-ui-ux/SKILL.md) |
| **`@configure-physics-collision`** | Configures deterministic fixed timestep tuning, Continuous Collision Detection (CCD), spatial query ... | [`core/skills/gamedev/configure-physics-collision/SKILL.md`](./core/skills/gamedev/configure-physics-collision/SKILL.md) |
| **`@design-procedural-generation`** | Designs deterministic procedural content generation (PCG) pipelines using seeded PRNG streams, multi... | [`core/skills/gamedev/design-procedural-generation/SKILL.md`](./core/skills/gamedev/design-procedural-generation/SKILL.md) |
| **`@develop-gameplay-systems`** | Build deterministic, high-performance gameplay systems, character controllers, state machines, and c... | [`core/skills/gamedev/develop-gameplay-systems/SKILL.md`](./core/skills/gamedev/develop-gameplay-systems/SKILL.md) |
| **`@direct-camera-systems`** | Directs 2D and 3D virtual camera systems including frame-rate independent smooth dampening, deadzone... | [`core/skills/gamedev/direct-camera-systems/SKILL.md`](./core/skills/gamedev/direct-camera-systems/SKILL.md) |
| **`@generate-game-assets-pipeline`** | Automate procedural and AI-assisted game asset pipelines including pixel sprite sheets, texture atla... | [`core/skills/gamedev/generate-game-assets-pipeline/SKILL.md`](./core/skills/gamedev/generate-game-assets-pipeline/SKILL.md) |
| **`@implement-save-persistence`** | Implements monotonic save schemas, version migration pipelines, cryptographic integrity checksums, b... | [`core/skills/gamedev/implement-save-persistence/SKILL.md`](./core/skills/gamedev/implement-save-persistence/SKILL.md) |
| **`@inspect-blender-rigs-motion`** | Diagnose and repair Blender armatures, bone roll alignment, animation retargeting hierarchies, and r... | [`core/skills/gamedev/inspect-blender-rigs-motion/SKILL.md`](./core/skills/gamedev/inspect-blender-rigs-motion/SKILL.md) |
| **`@integrate-dialogue-narrative`** | Integrates branching narrative trees, deterministic condition flag evaluators, localization string t... | [`core/skills/gamedev/integrate-dialogue-narrative/SKILL.md`](./core/skills/gamedev/integrate-dialogue-narrative/SKILL.md) |
| **`@integrate-game-engine`** | Bridge game architecture across engines, manage headless test runners, configure export pipelines, a... | [`core/skills/gamedev/integrate-game-engine/SKILL.md`](./core/skills/gamedev/integrate-game-engine/SKILL.md) |
| **`@manage-scene-lifecycle`** | Orchestrate scene hierarchies, asynchronous level streaming, additive scene loading, and resource di... | [`core/skills/gamedev/manage-scene-lifecycle/SKILL.md`](./core/skills/gamedev/manage-scene-lifecycle/SKILL.md) |
| **`@mix-dynamic-game-audio`** | Architect dynamic game audio hierarchies, bus mixers, sidechain ducking, adaptive music stem crossfa... | [`core/skills/gamedev/mix-dynamic-game-audio/SKILL.md`](./core/skills/gamedev/mix-dynamic-game-audio/SKILL.md) |
| **`@profile-game-performance`** | Profile and optimize CPU/GPU frame budgets, eliminate garbage collection stalls, batch draw calls, m... | [`core/skills/gamedev/profile-game-performance/SKILL.md`](./core/skills/gamedev/profile-game-performance/SKILL.md) |
| **`@program-game-shaders`** | Author high-performance vertex and fragment shaders across GLSL, HLSL, and Godot Shader Language for... | [`core/skills/gamedev/program-game-shaders/SKILL.md`](./core/skills/gamedev/program-game-shaders/SKILL.md) |
| **`@render-webgl-threejs`** | Architect interactive WebGL2 and WebGPU 3D scenes using Three.js or React Three Fiber with compresse... | [`core/skills/gamedev/render-webgl-threejs/SKILL.md`](./core/skills/gamedev/render-webgl-threejs/SKILL.md) |
| **`@tune-game-feel`** | Tune responsiveness, input buffering, screen shake, hit-stop, and audiovisual juice to maximize game... | [`core/skills/gamedev/tune-game-feel/SKILL.md`](./core/skills/gamedev/tune-game-feel/SKILL.md) |

### Category: `legal-compliance` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@audit-ai-compliance`** | Use when auditing AI systems, agentic workflows, or automated decision engines for compliance with V... | [`core/skills/legal-compliance/audit-ai-compliance/SKILL.md`](./core/skills/legal-compliance/audit-ai-compliance/SKILL.md) |
| **`@draft-legal-opinion`** | Use when drafting a structured formal legal opinion on a Vietnamese legal matter — covering question... | [`core/skills/legal-compliance/draft-legal-opinion/SKILL.md`](./core/skills/legal-compliance/draft-legal-opinion/SKILL.md) |
| **`@manage-vietnam-legal`** | Use when assessing Vietnamese statutory compliance, vetting commercial contracts, auditing Personal ... | [`core/skills/legal-compliance/manage-vietnam-legal/SKILL.md`](./core/skills/legal-compliance/manage-vietnam-legal/SKILL.md) |

### Category: `meetings-analysis` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@analyze-business-requirements`** | Analyze and write business requirements by making actors, business rules, state transitions, excepti... | [`core/skills/meetings-analysis/analyze-business-requirements/SKILL.md`](./core/skills/meetings-analysis/analyze-business-requirements/SKILL.md) |
| **`@analyze-data`** | Explore analytical datasets using DuckDB/Polars, query canonical Semantic Metric Catalogs (dbt Metri... | [`core/skills/meetings-analysis/analyze-data/SKILL.md`](./core/skills/meetings-analysis/analyze-data/SKILL.md) |
| **`@meeting-review`** | Run a structured multi-perspective review of a topic, proposal, code area, bug, feature, or risky ch... | [`core/skills/meetings-analysis/meeting-review/SKILL.md`](./core/skills/meetings-analysis/meeting-review/SKILL.md) |

### Category: `mmo` (7 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@analyze-campaign-roi`** | Measure conversion rates, organic search traffic, and CPA of generated content. Use when launching a... | [`core/skills/mmo/analyze-campaign-roi/SKILL.md`](./core/skills/mmo/analyze-campaign-roi/SKILL.md) |
| **`@create-automation-script`** | Generate stealth automation scripts using Playwright/Puppeteer over CDP, C++ patched browsers (Camou... | [`core/skills/mmo/create-automation-script/SKILL.md`](./core/skills/mmo/create-automation-script/SKILL.md) |
| **`@deploy-mmo-infrastructure`** | Deploy and manage proxy pools (Residential/4G) with dynamic health probes and Anti-Detect Browser or... | [`core/skills/mmo/deploy-mmo-infrastructure/SKILL.md`](./core/skills/mmo/deploy-mmo-infrastructure/SKILL.md) |
| **`@deploy-proxyware-fleet`** | Containerize and orchestrate modern DePIN bandwidth monetization light nodes (Grass, Dawn, Nodepay) ... | [`core/skills/mmo/deploy-proxyware-fleet/SKILL.md`](./core/skills/mmo/deploy-proxyware-fleet/SKILL.md) |
| **`@generate-mmo-content`** | Generate Programmatic SEO (pSEO) Answer-First landing pages with JSON-LD schemas and multimodal shor... | [`core/skills/mmo/generate-mmo-content/SKILL.md`](./core/skills/mmo/generate-mmo-content/SKILL.md) |
| **`@manage-mmo-assets`** | Manage and share MMO assets (Business Managers, Via, Pixels/Datasets, Anti-Detect profiles) using Ro... | [`core/skills/mmo/manage-mmo-assets/SKILL.md`](./core/skills/mmo/manage-mmo-assets/SKILL.md) |
| **`@setup-tracking-system`** | Configure advanced privacy-first tracking including Server-to-Server (S2S) postbacks, Meta CAPI v20+... | [`core/skills/mmo/setup-tracking-system/SKILL.md`](./core/skills/mmo/setup-tracking-system/SKILL.md) |

### Category: `mobile` (2 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@deploy-mobile-app`** | Configure and execute mobile deployment pipelines using EAS Build, native code signing credentials, ... | [`core/skills/mobile/deploy-mobile-app/SKILL.md`](./core/skills/mobile/deploy-mobile-app/SKILL.md) |
| **`@develop-mobile-app`** | Architect high-performance mobile applications using React Native New Architecture, Hermes bytecode ... | [`core/skills/mobile/develop-mobile-app/SKILL.md`](./core/skills/mobile/develop-mobile-app/SKILL.md) |

### Category: `overlay/b2b-catalog-golf` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-b2b-golf-feature`** | Develop features for the B2B Golf niche catalog — an Astro v5 golf apparel site on Cloudflare Pages.... | [`overlays/b2b-catalog-golf/skills/develop-b2b-golf-feature/SKILL.md`](./overlays/b2b-catalog-golf/skills/develop-b2b-golf-feature/SKILL.md) |

### Category: `overlay/b2b-factory-catalog` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-b2b-catalog-feature`** | Develop features for the B2B factory direct catalog — an Astro v5 B2B manufacturing catalog on Cloud... | [`overlays/b2b-factory-catalog/skills/develop-b2b-catalog-feature/SKILL.md`](./overlays/b2b-factory-catalog/skills/develop-b2b-catalog-feature/SKILL.md) |

### Category: `overlay/cad-projection` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@isometric-svg-projection`** | Use when generating precision isometric vector diagrams, engineering schematics, and CAD projections... | [`overlays/cad-projection/skills/isometric-svg-projection/SKILL.md`](./overlays/cad-projection/skills/isometric-svg-projection/SKILL.md) |

### Category: `overlay/fintech-compliance` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@build-credit-scorecard`** | Use when building regulatory credit risk scorecards, performing monotonic WOE binning, evaluating IV... | [`overlays/fintech-compliance/skills/build-credit-scorecard/SKILL.md`](./overlays/fintech-compliance/skills/build-credit-scorecard/SKILL.md) |

### Category: `overlay/hugo-authority-content` (2 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@audit-technical-article`** | Audit a technical article or series part on authority-blog/learn against the 7 Technical Content Gat... | [`overlays/hugo-authority-content/skills/audit-technical-article/SKILL.md`](./overlays/hugo-authority-content/skills/audit-technical-article/SKILL.md) |
| **`@write-hugo-twin-content`** | Draft or update Hugo Markdown for the authority blog or the learn notes site. Use when creating or e... | [`overlays/hugo-authority-content/skills/write-hugo-twin-content/SKILL.md`](./overlays/hugo-authority-content/skills/write-hugo-twin-content/SKILL.md) |

### Category: `overlay/hvac-authority-content` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@write-hvac-authority-content`** | "Draft, optimize, and update technical HVAC Astro Content Collection Markdown/MDX for HVAC Authority... | [`overlays/hvac-authority-content/skills/write-hvac-authority-content/SKILL.md`](./overlays/hvac-authority-content/skills/write-hvac-authority-content/SKILL.md) |

### Category: `overlay/laravel-ecommerce` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-laravel-ecommerce-feature`** | Develop features for Laravel 13 + Filament v4 e-commerce. Use when adding Filament admin resources, ... | [`overlays/laravel-ecommerce/skills/develop-laravel-ecommerce-feature/SKILL.md`](./overlays/laravel-ecommerce/skills/develop-laravel-ecommerce-feature/SKILL.md) |

### Category: `overlay/laravel-filament` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-laravel-feature`** | Develop features in a Laravel 13 + Filament v4 + Livewire 3 monolith. Use when adding admin resource... | [`overlays/laravel-filament/skills/develop-laravel-feature/SKILL.md`](./overlays/laravel-filament/skills/develop-laravel-feature/SKILL.md) |

### Category: `overlay/obj-configurator` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@develop-obj-feature`** | Develop features for the OBJ 3D Product Configurator — an Astro + React Three Fiber app with Three.j... | [`overlays/obj-configurator/skills/develop-obj-feature/SKILL.md`](./overlays/obj-configurator/skills/develop-obj-feature/SKILL.md) |

### Category: `overlay/r3f-stack` (3 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@debug-3d-scene`** | Debug 3D scene behavior by tracing scene graph structure, transforms, raycasting, decals, materials,... | [`overlays/r3f-stack/skills/debug-3d-scene/SKILL.md`](./overlays/r3f-stack/skills/debug-3d-scene/SKILL.md) |
| **`@integrate-r3f-three-legacy`** | Integrate or migrate between React Three Fiber and legacy imperative Three.js code by controlling sc... | [`overlays/r3f-stack/skills/integrate-r3f-three-legacy/SKILL.md`](./overlays/r3f-stack/skills/integrate-r3f-three-legacy/SKILL.md) |
| **`@optimize-3d-assets`** | Optimize 3D assets and rendering inputs by reviewing model formats, geometry density, texture memory... | [`overlays/r3f-stack/skills/optimize-3d-assets/SKILL.md`](./overlays/r3f-stack/skills/optimize-3d-assets/SKILL.md) |

### Category: `overlay/real-estate-content` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@write-real-estate-astro-data`** | Draft or update Astro Content Collection Markdown/MDX for the Real Estate and HVAC portals. Use when... | [`overlays/real-estate-content/skills/write-real-estate-astro-data/SKILL.md`](./overlays/real-estate-content/skills/write-real-estate-astro-data/SKILL.md) |

### Category: `overlay/security-research` (1 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@reverse-engineer-binary`** | Use when deconstructing compiled binaries, Electron bundles, and firmware images in air-gapped sandb... | [`overlays/security-research/skills/reverse-engineer-binary/SKILL.md`](./overlays/security-research/skills/reverse-engineer-binary/SKILL.md) |

### Category: `platform` (19 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@add-telemetry-instrumentation`** | Add or update logging, metrics, and tracing by following the repo's observability patterns and OpenT... | [`core/skills/platform/add-telemetry-instrumentation/SKILL.md`](./core/skills/platform/add-telemetry-instrumentation/SKILL.md) |
| **`@agents-sdk`** | Builds, deploys, and maintains stateful AI agents on Cloudflare Workers and Durable Objects using th... | [`core/skills/platform/agents-sdk/SKILL.md`](./core/skills/platform/agents-sdk/SKILL.md) |
| **`@aws-infrastructure`** | Provision, configure, and optimize AWS cloud infrastructure via OpenTofu state KMS encryption, Cross... | [`core/skills/platform/aws-infrastructure/SKILL.md`](./core/skills/platform/aws-infrastructure/SKILL.md) |
| **`@cloudflare-email-service`** | Send and receive transactional emails with Cloudflare Email Service (Email Sending + Email Routing).... | [`core/skills/platform/cloudflare-email-service/SKILL.md`](./core/skills/platform/cloudflare-email-service/SKILL.md) |
| **`@debug-runtime-platform`** | Investigate deployment, environment, runtime, and rollout issues that are not purely application-cod... | [`core/skills/platform/debug-runtime-platform/SKILL.md`](./core/skills/platform/debug-runtime-platform/SKILL.md) |
| **`@debug-workers-edge`** | Diagnose Cloudflare Pages and Workers failures at the edge — 5xx, binding errors, Wrangler deploy fa... | [`core/skills/platform/debug-workers-edge/SKILL.md`](./core/skills/platform/debug-workers-edge/SKILL.md) |
| **`@deploy-aws-eks-workloads`** | Deploy, scale, and govern cloud-native application workloads on Amazon EKS using SOTA 2026-2027 AWS ... | [`core/skills/platform/deploy-aws-eks-workloads/SKILL.md`](./core/skills/platform/deploy-aws-eks-workloads/SKILL.md) |
| **`@durable-objects`** | Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, m... | [`core/skills/platform/durable-objects/SKILL.md`](./core/skills/platform/durable-objects/SKILL.md) |
| **`@orchestrate-chaos-experiment`** | Plan, execute, and verify controlled chaos engineering experiments and game days. Use when validatin... | [`core/skills/platform/orchestrate-chaos-experiment/SKILL.md`](./core/skills/platform/orchestrate-chaos-experiment/SKILL.md) |
| **`@sandbox-sdk`** | Builds secure, isolated code execution environments on Cloudflare Workers using the Cloudflare Sandb... | [`core/skills/platform/sandbox-sdk/SKILL.md`](./core/skills/platform/sandbox-sdk/SKILL.md) |
| **`@setup-deployment`** | Add or update deployment source-of-truth configuration for a service or component. Use when a change... | [`core/skills/platform/setup-deployment/SKILL.md`](./core/skills/platform/setup-deployment/SKILL.md) |
| **`@setup-gpu-finops`** | Configure GPU telemetry, DCGM metrics, and Kubecost to attribute AI compute costs to specific namesp... | [`core/skills/platform/setup-gpu-finops/SKILL.md`](./core/skills/platform/setup-gpu-finops/SKILL.md) |
| **`@setup-llm-gateway`** | Configure a centralized LLM proxy gateway for token routing, budgeting, and failover. Use when deplo... | [`core/skills/platform/setup-llm-gateway/SKILL.md`](./core/skills/platform/setup-llm-gateway/SKILL.md) |
| **`@supply-chain-security`** | Implement software supply chain security by generating SBOMs (CycloneDX/SPDX), enforcing SLSA build ... | [`core/skills/platform/supply-chain-security/SKILL.md`](./core/skills/platform/supply-chain-security/SKILL.md) |
| **`@system-design`** | Design, specify, and document complex system architectures covering compute, network, storage, middl... | [`core/skills/platform/system-design/SKILL.md`](./core/skills/platform/system-design/SKILL.md) |
| **`@turnstile-spin`** | Implements end-to-end Cloudflare Turnstile CAPTCHA protection — widget creation, managed siteverify ... | [`core/skills/platform/turnstile-spin/SKILL.md`](./core/skills/platform/turnstile-spin/SKILL.md) |
| **`@web-perf`** | Analyzes web page performance using Chrome DevTools MCP — measuring Core Web Vitals (LCP, INP, CLS),... | [`core/skills/platform/web-perf/SKILL.md`](./core/skills/platform/web-perf/SKILL.md) |
| **`@workers-best-practices`** | Reviews and authors Cloudflare Workers code against production best practices — covering async patte... | [`core/skills/platform/workers-best-practices/SKILL.md`](./core/skills/platform/workers-best-practices/SKILL.md) |
| **`@wrangler`** | Deploys, develops, and manages Cloudflare Workers and their bindings — KV, R2, D1, Vectorize, Hyperd... | [`core/skills/platform/wrangler/SKILL.md`](./core/skills/platform/wrangler/SKILL.md) |

### Category: `product` (4 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@build-story-map`** | Structure and visualize product backlogs using Jeff Patton User Story Mapping, MoSCoW release swimla... | [`core/skills/product/build-story-map/SKILL.md`](./core/skills/product/build-story-map/SKILL.md) |
| **`@define-product-strategy`** | Formulate, stress-test, and document product strategy using Amazon Working Backwards (PR/FAQ), Hamil... | [`core/skills/product/define-product-strategy/SKILL.md`](./core/skills/product/define-product-strategy/SKILL.md) |
| **`@model-saas-metrics`** | Model SaaS unit economics, deterministic financial metrics, Van Westendorp price sensitivity, and AI... | [`core/skills/product/model-saas-metrics/SKILL.md`](./core/skills/product/model-saas-metrics/SKILL.md) |
| **`@prioritize-roadmap`** | Score, sequence, and balance product roadmaps using calibrated quantitative RICE, WSJF, Kano classif... | [`core/skills/product/prioritize-roadmap/SKILL.md`](./core/skills/product/prioritize-roadmap/SKILL.md) |

### Category: `repo-ops` (5 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@commit-code`** | Validate and package a finished change into a clean commit by following repo-local validation, gener... | [`core/skills/repo-ops/commit-code/SKILL.md`](./core/skills/repo-ops/commit-code/SKILL.md) |
| **`@navigate-service`** | Navigate and understand an unfamiliar service by mapping its entrypoints, core flows, dependencies, ... | [`core/skills/repo-ops/navigate-service/SKILL.md`](./core/skills/repo-ops/navigate-service/SKILL.md) |
| **`@review-code`** | Review a diff since a fixed point along two separate axes — Standards (does the code follow this rep... | [`core/skills/repo-ops/review-code/SKILL.md`](./core/skills/repo-ops/review-code/SKILL.md) |
| **`@review-service`** | Review an entire service for release readiness. Use for full-service audits, production-readiness ch... | [`core/skills/repo-ops/review-service/SKILL.md`](./core/skills/repo-ops/review-service/SKILL.md) |
| **`@troubleshoot-service`** | Troubleshoot build, startup, runtime, dependency, and configuration issues by isolating the failing ... | [`core/skills/repo-ops/troubleshoot-service/SKILL.md`](./core/skills/repo-ops/troubleshoot-service/SKILL.md) |

### Category: `security-data` (9 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@build-data-pipeline`** | Design and implement transactional lakehouse pipelines (Iceberg v3/Delta 4.4), enforce ODCS v3.2.0 d... | [`core/skills/security-data/build-data-pipeline/SKILL.md`](./core/skills/security-data/build-data-pipeline/SKILL.md) |
| **`@database-maintenance`** | Plan and execute operational data store and modern lakehouse maintenance, including Apache Iceberg/D... | [`core/skills/security-data/database-maintenance/SKILL.md`](./core/skills/security-data/database-maintenance/SKILL.md) |
| **`@manage-secrets`** | Add, update, rotate, or review secret handling by following the repo's source-of-truth, access-contr... | [`core/skills/security-data/manage-secrets/SKILL.md`](./core/skills/security-data/manage-secrets/SKILL.md) |
| **`@manage-vietnam-accounting`** | Prepare and review Vietnam accounting controls, accounting-regime evidence, reconciliations, invoice... | [`core/skills/security-data/manage-vietnam-accounting/SKILL.md`](./core/skills/security-data/manage-vietnam-accounting/SKILL.md) |
| **`@optimize-olap-database`** | Design high-throughput OLAP schemas for Iceberg v3, tune ClickHouse/DuckDB columnar engines, configu... | [`core/skills/security-data/optimize-olap-database/SKILL.md`](./core/skills/security-data/optimize-olap-database/SKILL.md) |
| **`@prompt-injection-defense`** | Use when safeguarding AI agents against direct and indirect prompt injection attacks, implementing b... | [`core/skills/security-data/prompt-injection-defense/SKILL.md`](./core/skills/security-data/prompt-injection-defense/SKILL.md) |
| **`@query-analytical-engine`** | Execute in-process analytical SQL with chDB and DuckDB v1.5+, orchestrate multi-step stateful pipeli... | [`core/skills/security-data/query-analytical-engine/SKILL.md`](./core/skills/security-data/query-analytical-engine/SKILL.md) |
| **`@security-audit`** | Review code, configuration, and service behavior for security risks by checking trust boundaries, se... | [`core/skills/security-data/security-audit/SKILL.md`](./core/skills/security-data/security-audit/SKILL.md) |
| **`@skill-preflight-ast-check`** | Use when performing zero-execution static AST security vetting of third-party agent skills, enforcin... | [`core/skills/security-data/skill-preflight-ast-check/SKILL.md`](./core/skills/security-data/skill-preflight-ast-check/SKILL.md) |

### Category: `seo` (2 skills)

| Skill Slug | Description | File |
|:---|:---|:---|
| **`@audit-technical-seo`** | Audit crawl budgets, search and AI bot access in robots.txt (Googlebot, Bingbot, OAI-SearchBot, Perp... | [`core/skills/seo/audit-technical-seo/SKILL.md`](./core/skills/seo/audit-technical-seo/SKILL.md) |
| **`@implement-schema-markup`** | Architect, generate, and validate connected Schema.org @graph JSON-LD structured data linking WebSit... | [`core/skills/seo/implement-schema-markup/SKILL.md`](./core/skills/seo/implement-schema-markup/SKILL.md) |

---

## 🔀 Composite & Short Skill Aliases Matrix

| Mention / Shortcut | Resolves To Core Skills | Typical Role |
|:---|:---|:---|
| **`@7_powers`** | `define-product-strategy` | Active `@role` |
| **`@7powers`** | `define-product-strategy` | Active `@role` |
| **`@a2a`** | `agent-a2a-protocol` | Active `@role` |
| **`@a2a_protocol`** | `agent-a2a-protocol` | Active `@role` |
| **`@abstract-input-actions`** | `abstract-input-actions` | Active `@role` |
| **`@abstract_input_actions`** | `abstract-input-actions` | Active `@role` |
| **`@accounting`** | `manage-vietnam-accounting` | Active `@role` |
| **`@acroform`** | `pdf` | Active `@role` |
| **`@add_api_endpoint`** | `add-api-endpoint` | Active `@role` |
| **`@add_event_handler`** | `add-event-handler` | Active `@role` |
| **`@add_page_route`** | `add-page-route` | Active `@role` |
| **`@add_service_client`** | `add-service-client` | Active `@role` |
| **`@add_ui_component`** | `add-ui-component` | Active `@role` |
| **`@agent-memory-compaction`** | `agent-memory-compaction` | Active `@role` |
| **`@agent_delegation`** | `agent-delegation` | Active `@role` |
| **`@agent_memory_compaction`** | `agent-memory-compaction` | Active `@role` |
| **`@agentic_decomposition`** | `decompose-agentic-system` | Active `@role` |
| **`@agentic_task_decomposition`** | `decompose-agentic-system` | Active `@role` |
| **`@ai_law_audit`** | `audit-ai-compliance` | Active `@role` |
| **`@ai_risk_classification`** | `audit-ai-compliance` | Active `@role` |
| **`@analytical_sql`** | `query-analytical-engine` | Active `@role` |
| **`@analyze-campaign-roi`** | `analyze-campaign-roi` | Active `@role` |
| **`@analyze_business_requirements`** | `analyze-business-requirements` | Active `@role` |
| **`@analyze_campaign_roi`** | `analyze-campaign-roi` | Active `@role` |
| **`@analyze_data`** | `analyze-data` | Active `@role` |
| **`@anti-slop`** | `setup-design-system`, `component-composition` | Active `@role` |
| **`@anti_detect`** | `create-automation-script` | Active `@role` |
| **`@anti_slop`** | `setup-design-system`, `component-composition` | Active `@role` |
| **`@api`** | `add-api-endpoint` | Active `@role` |
| **`@app_store`** | `deploy-mobile-app` | Active `@role` |
| **`@architect-ecs-systems`** | `architect-ecs-systems` | Active `@role` |
| **`@architect-mcp-server`** | `architect-mcp-server` | Active `@role` |
| **`@architect_ecs_systems`** | `architect-ecs-systems` | Active `@role` |
| **`@architect_mcp_server`** | `architect-mcp-server` | Active `@role` |
| **`@asset-pipeline`** | `generate-game-assets-pipeline` | Active `@role` |
| **`@asset_pipeline`** | `generate-game-assets-pipeline` | Active `@role` |
| **`@audit-ai-compliance`** | `audit-ai-compliance` | Active `@role` |
| **`@audit-technical-seo`** | `audit-technical-seo` | Active `@role` |
| **`@audit_ai_compliance`** | `audit-ai-compliance` | Active `@role` |
| **`@audit_content`** | `audit-content` | Active `@role` |
| **`@audit_technical_seo`** | `audit-technical-seo` | Active `@role` |
| **`@auth`** | `implement-auth` | Active `@role` |
| **`@authentication`** | `implement-auth` | Active `@role` |
| **`@author-game-ai`** | `author-game-ai` | Active `@role` |
| **`@author_game_ai`** | `author-game-ai` | Active `@role` |
| **`@automate-game-publishing`** | `automate-game-publishing` | Active `@role` |
| **`@automate_game_publishing`** | `automate-game-publishing` | Active `@role` |
| **`@aws_eks`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@aws_infra`** | `aws-infrastructure` | Active `@role` |
| **`@aws_infrastructure`** | `aws-infrastructure` | Active `@role` |
| **`@ba`** | `analyze-business-requirements`, `elicit-requirements` | Active `@role` |
| **`@babok`** | `elicit-requirements`, `trace-requirements-impact` | Active `@role` |
| **`@bandwidth_monetization`** | `deploy-proxyware-fleet` | Active `@role` |
| **`@blended_roas`** | `analyze-campaign-roi` | Active `@role` |
| **`@blender-rigs`** | `inspect-blender-rigs-motion` | Active `@role` |
| **`@blender_rigs`** | `inspect-blender-rigs-motion` | Active `@role` |
| **`@build-game-ui-ux`** | `build-game-ui-ux` | Active `@role` |
| **`@build_data_pipeline`** | `build-data-pipeline` | Active `@role` |
| **`@build_game_ui_ux`** | `build-game-ui-ux` | Active `@role` |
| **`@build_mcp_server`** | `build-mcp-server` | Active `@role` |
| **`@business_requirements`** | `analyze-business-requirements` | Active `@role` |
| **`@camera-systems`** | `direct-camera-systems` | Active `@role` |
| **`@camera_systems`** | `direct-camera-systems` | Active `@role` |
| **`@campaign_roi`** | `analyze-campaign-roi` | Active `@role` |
| **`@capi`** | `setup-tracking-system` | Active `@role` |
| **`@cdp_automation`** | `create-automation-script` | Active `@role` |
| **`@chaos`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@chaos-engineering`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@chaos_engineering`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@chaos_experiment`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@chdb_query`** | `query-analytical-engine` | Active `@role` |
| **`@clean-memory`** | `memory-hygiene` | Active `@role` |
| **`@clean_memory`** | `memory-hygiene` | Active `@role` |
| **`@clickhouse_tuning`** | `optimize-olap-database` | Active `@role` |
| **`@columnar_database_optimization`** | `optimize-olap-database` | Active `@role` |
| **`@combinatorial_testing`** | `combinatorial-testing` | Active `@role` |
| **`@compact`** | `agent-memory-compaction` | Active `@role` |
| **`@compact-memory`** | `agent-memory-compaction` | Active `@role` |
| **`@compact_memory`** | `agent-memory-compaction` | Active `@role` |
| **`@compaction`** | `agent-memory-compaction` | Active `@role` |
| **`@component-composition`** | `component-composition` | Active `@role` |
| **`@component_composition`** | `component-composition` | Active `@role` |
| **`@composition`** | `component-composition` | Active `@role` |
| **`@compound-components`** | `component-composition` | Active `@role` |
| **`@compound_components`** | `component-composition` | Active `@role` |
| **`@conduct_research`** | `conduct-research` | Active `@role` |
| **`@configure-physics-collision`** | `configure-physics-collision` | Active `@role` |
| **`@configure_physics_collision`** | `configure-physics-collision` | Active `@role` |
| **`@connection_pooling`** | `optimize-postgres` | Active `@role` |
| **`@content_audit`** | `audit-content` | Active `@role` |
| **`@content_strategy`** | `design-content-strategy` | Active `@role` |
| **`@conversion_api`** | `setup-tracking-system` | Active `@role` |
| **`@copywriting`** | `write-copy` | Active `@role` |
| **`@cpm`** | `build-story-map` | Active `@role` |
| **`@crawlability`** | `audit-technical-seo` | Active `@role` |
| **`@create-automation-script`** | `create-automation-script` | Active `@role` |
| **`@create_api`** | `add-api-endpoint` | Active `@role` |
| **`@create_automation_script`** | `create-automation-script` | Active `@role` |
| **`@create_migration`** | `create-migration` | Active `@role` |
| **`@critical_path`** | `build-story-map` | Active `@role` |
| **`@cross_source_query`** | `query-analytical-engine` | Active `@role` |
| **`@data_pipeline`** | `build-data-pipeline` | Active `@role` |
| **`@database`** | `database-maintenance` | Active `@role` |
| **`@db_maintenance`** | `database-maintenance` | Active `@role` |
| **`@debugging`** | `systematic-debugging` | Active `@role` |
| **`@decompose-agentic-system`** | `decompose-agentic-system` | Active `@role` |
| **`@decompose_agentic_system`** | `decompose-agentic-system` | Active `@role` |
| **`@deep_research`** | `conduct-research` | Active `@role` |
| **`@delegation`** | `agent-delegation` | Active `@role` |
| **`@depin_bandwidth`** | `deploy-proxyware-fleet` | Active `@role` |
| **`@deploy`** | `setup-deployment` | Active `@role` |
| **`@deploy-aws-eks-workloads`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@deploy-mmo-infrastructure`** | `deploy-mmo-infrastructure` | Active `@role` |
| **`@deploy-mobile-app`** | `deploy-mobile-app` | Active `@role` |
| **`@deploy-proxyware-fleet`** | `deploy-proxyware-fleet` | Active `@role` |
| **`@deploy-vllm`** | `deploy-vllm-inference` | Active `@role` |
| **`@deploy_aws_eks_workloads`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@deploy_eks`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@deploy_mmo_infrastructure`** | `deploy-mmo-infrastructure` | Active `@role` |
| **`@deploy_mobile_app`** | `deploy-mobile-app` | Active `@role` |
| **`@deploy_proxyware_fleet`** | `deploy-proxyware-fleet` | Active `@role` |
| **`@deploy_vllm_inference`** | `deploy-vllm-inference` | Active `@role` |
| **`@deployment`** | `setup-deployment` | Active `@role` |
| **`@design-content-strategy`** | `design-content-strategy` | Active `@role` |
| **`@design-procedural-generation`** | `design-procedural-generation` | Active `@role` |
| **`@design_content_strategy`** | `design-content-strategy` | Active `@role` |
| **`@design_mcp_server`** | `architect-mcp-server` | Active `@role` |
| **`@design_procedural_generation`** | `design-procedural-generation` | Active `@role` |
| **`@design_system`** | `setup-design-system` | Active `@role` |
| **`@develop-gameplay-systems`** | `develop-gameplay-systems` | Active `@role` |
| **`@develop-mobile-app`** | `develop-mobile-app` | Active `@role` |
| **`@develop_gameplay_systems`** | `develop-gameplay-systems` | Active `@role` |
| **`@develop_mobile_app`** | `develop-mobile-app` | Active `@role` |
| **`@dialogue`** | `integrate-dialogue-narrative` | Active `@role` |
| **`@dialogue-system`** | `integrate-dialogue-narrative` | Active `@role` |
| **`@dialogue_system`** | `integrate-dialogue-narrative` | Active `@role` |
| **`@direct-camera-systems`** | `direct-camera-systems` | Active `@role` |
| **`@direct_camera_systems`** | `direct-camera-systems` | Active `@role` |
| **`@direct_response`** | `write-copy` | Active `@role` |
| **`@discernment-nudge`** | `discernment-nudge` | Active `@role` |
| **`@discernment_nudge`** | `discernment-nudge` | Active `@role` |
| **`@docs`** | `write-documentation` | Active `@role` |
| **`@documentation`** | `write-documentation` | Active `@role` |
| **`@docx`** | `docx` | Active `@role` |
| **`@draft-legal-opinion`** | `draft-legal-opinion` | Active `@role` |
| **`@draft_legal_opinion`** | `draft-legal-opinion` | Active `@role` |
| **`@e2e_tests`** | `write-tests` | Active `@role` |
| **`@eas_build`** | `deploy-mobile-app` | Active `@role` |
| **`@eas_deploy`** | `deploy-mobile-app` | Active `@role` |
| **`@eas_update`** | `deploy-mobile-app` | Active `@role` |
| **`@ecs`** | `architect-ecs-systems` | Active `@role` |
| **`@ecs-systems`** | `architect-ecs-systems` | Active `@role` |
| **`@ecs_systems`** | `architect-ecs-systems` | Active `@role` |
| **`@editorial_calendar`** | `design-content-strategy` | Active `@role` |
| **`@eks_workloads`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@embedded_sql`** | `query-analytical-engine` | Active `@role` |
| **`@event_handler`** | `add-event-handler` | Active `@role` |
| **`@excel`** | `xlsx` | Active `@role` |
| **`@expo`** | `develop-mobile-app` | Active `@role` |
| **`@faceless_video`** | `generate-mmo-content` | Active `@role` |
| **`@fault_injection`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@flashlist`** | `develop-mobile-app` | Active `@role` |
| **`@frontend_testing`** | `frontend-testing` | Active `@role` |
| **`@game-ai`** | `author-game-ai` | Active `@role` |
| **`@game-audio`** | `mix-dynamic-game-audio` | Active `@role` |
| **`@game-camera`** | `direct-camera-systems` | Active `@role` |
| **`@game-engine`** | `integrate-game-engine` | Active `@role` |
| **`@game-feel`** | `tune-game-feel` | Active `@role` |
| **`@game-input`** | `abstract-input-actions` | Active `@role` |
| **`@game-perf`** | `profile-game-performance` | Active `@role` |
| **`@game-publishing`** | `automate-game-publishing` | Active `@role` |
| **`@game-shaders`** | `program-game-shaders` | Active `@role` |
| **`@game-ui`** | `build-game-ui-ux` | Active `@role` |
| **`@game-ui-ux`** | `build-game-ui-ux` | Active `@role` |
| **`@game_ai`** | `author-game-ai` | Active `@role` |
| **`@game_audio`** | `mix-dynamic-game-audio` | Active `@role` |
| **`@game_camera`** | `direct-camera-systems` | Active `@role` |
| **`@game_day`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@game_engine`** | `integrate-game-engine` | Active `@role` |
| **`@game_feel`** | `tune-game-feel` | Active `@role` |
| **`@game_input`** | `abstract-input-actions` | Active `@role` |
| **`@game_perf`** | `profile-game-performance` | Active `@role` |
| **`@game_publishing`** | `automate-game-publishing` | Active `@role` |
| **`@game_shaders`** | `program-game-shaders` | Active `@role` |
| **`@game_ui`** | `build-game-ui-ux` | Active `@role` |
| **`@game_ui_ux`** | `build-game-ui-ux` | Active `@role` |
| **`@gameplay`** | `develop-gameplay-systems` | Active `@role` |
| **`@gameplay-systems`** | `develop-gameplay-systems` | Active `@role` |
| **`@gameplay_systems`** | `develop-gameplay-systems` | Active `@role` |
| **`@generate-game-assets-pipeline`** | `generate-game-assets-pipeline` | Active `@role` |
| **`@generate-mmo-content`** | `generate-mmo-content` | Active `@role` |
| **`@generate_game_assets_pipeline`** | `generate-game-assets-pipeline` | Active `@role` |
| **`@generate_mmo_content`** | `generate-mmo-content` | Active `@role` |
| **`@google_play`** | `deploy-mobile-app` | Active `@role` |
| **`@graph_orchestration`** | `agent-graph-orchestration` | Active `@role` |
| **`@growth_stack`** | `setup-tracking-system`, `analyze-campaign-roi` | Active `@role` |
| **`@handoff`** | `agent-handoff` | Active `@role` |
| **`@hermes`** | `develop-mobile-app` | Active `@role` |
| **`@humanizer`** | `write-copy` | Active `@role` |
| **`@implement-save-persistence`** | `implement-save-persistence` | Active `@role` |
| **`@implement-schema-markup`** | `implement-schema-markup` | Active `@role` |
| **`@implement-view-transitions`** | `implement-view-transitions` | Active `@role` |
| **`@implement_auth`** | `implement-auth` | Active `@role` |
| **`@implement_save_persistence`** | `implement-save-persistence` | Active `@role` |
| **`@implement_schema_markup`** | `implement-schema-markup` | Active `@role` |
| **`@implement_structured_outputs`** | `implement-structured-outputs` | Active `@role` |
| **`@implement_view_transitions`** | `implement-view-transitions` | Active `@role` |
| **`@incident`** | `incident-report` | Active `@role` |
| **`@incident_report`** | `incident-report` | Active `@role` |
| **`@input-actions`** | `abstract-input-actions` | Active `@role` |
| **`@input_actions`** | `abstract-input-actions` | Active `@role` |
| **`@inspect-blender-rigs-motion`** | `inspect-blender-rigs-motion` | Active `@role` |
| **`@inspect_blender_rigs_motion`** | `inspect-blender-rigs-motion` | Active `@role` |
| **`@instrumentation`** | `add-telemetry-instrumentation` | Active `@role` |
| **`@integrate-dialogue-narrative`** | `integrate-dialogue-narrative` | Active `@role` |
| **`@integrate-game-engine`** | `integrate-game-engine` | Active `@role` |
| **`@integrate_dialogue_narrative`** | `integrate-dialogue-narrative` | Active `@role` |
| **`@integrate_game_engine`** | `integrate-game-engine` | Active `@role` |
| **`@json_ld`** | `implement-schema-markup` | Active `@role` |
| **`@juice`** | `tune-game-feel` | Active `@role` |
| **`@kano`** | `prioritize-roadmap` | Active `@role` |
| **`@kano_model`** | `prioritize-roadmap` | Active `@role` |
| **`@karpenter`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@kill_early`** | `prioritize-roadmap` | Active `@role` |
| **`@legal`** | `manage-vietnam-legal` | Active `@role` |
| **`@legal_compliance`** | `manage-vietnam-legal` | Active `@role` |
| **`@legal_opinion`** | `draft-legal-opinion` | Active `@role` |
| **`@legal_opinion_drafting`** | `draft-legal-opinion` | Active `@role` |
| **`@ltv_roas`** | `analyze-campaign-roi` | Active `@role` |
| **`@luat`** | `manage-vietnam-legal` | Active `@role` |
| **`@manage-mmo-assets`** | `manage-mmo-assets` | Active `@role` |
| **`@manage-scene-lifecycle`** | `manage-scene-lifecycle` | Active `@role` |
| **`@manage-vietnam-legal`** | `manage-vietnam-legal` | Active `@role` |
| **`@manage_mmo_assets`** | `manage-mmo-assets` | Active `@role` |
| **`@manage_scene_lifecycle`** | `manage-scene-lifecycle` | Active `@role` |
| **`@manage_secrets`** | `manage-secrets` | Active `@role` |
| **`@manage_vietnam_legal`** | `manage-vietnam-legal` | Active `@role` |
| **`@marketing_copy`** | `write-copy` | Active `@role` |
| **`@mcp_architecture`** | `architect-mcp-server` | Active `@role` |
| **`@mcp_builder`** | `architect-mcp-server` | Active `@role` |
| **`@mcp_server`** | `build-mcp-server` | Active `@role` |
| **`@mcp_server_architecture`** | `architect-mcp-server` | Active `@role` |
| **`@memory-compaction`** | `agent-memory-compaction` | Active `@role` |
| **`@memory-hygiene`** | `memory-hygiene` | Active `@role` |
| **`@memory_compaction`** | `agent-memory-compaction` | Active `@role` |
| **`@memory_hygiene`** | `memory-hygiene` | Active `@role` |
| **`@migration`** | `create-migration` | Active `@role` |
| **`@mix-dynamic-game-audio`** | `mix-dynamic-game-audio` | Active `@role` |
| **`@mix_dynamic_game_audio`** | `mix-dynamic-game-audio` | Active `@role` |
| **`@mmo-assets`** | `manage-mmo-assets` | Active `@role` |
| **`@mmo-content`** | `generate-mmo-content` | Active `@role` |
| **`@mmo-infra`** | `deploy-mmo-infrastructure` | Active `@role` |
| **`@mmo_assets`** | `manage-mmo-assets` | Active `@role` |
| **`@mmo_campaign`** | `setup-tracking-system`, `generate-mmo-content`, `analyze-campaign-roi` | Active `@role` |
| **`@mmo_content`** | `generate-mmo-content` | Active `@role` |
| **`@mmo_growth`** | `deploy-mmo-infrastructure`, `create-automation-script`, `setup-tracking-system` | Active `@role` |
| **`@mmo_infra`** | `deploy-mmo-infrastructure` | Active `@role` |
| **`@mobile_app`** | `develop-mobile-app` | Active `@role` |
| **`@model_routing`** | `agent-model-routing` | Active `@role` |
| **`@mom-test`** | `define-product-strategy` | Active `@role` |
| **`@mom_test`** | `define-product-strategy` | Active `@role` |
| **`@motion-physics`** | `implement-view-transitions` | Active `@role` |
| **`@motion_physics`** | `implement-view-transitions` | Active `@role` |
| **`@narrative`** | `integrate-dialogue-narrative` | Active `@role` |
| **`@new_endpoint`** | `add-api-endpoint` | Active `@role` |
| **`@oauth`** | `implement-auth` | Active `@role` |
| **`@olap_optimization`** | `optimize-olap-database` | Active `@role` |
| **`@olap_tuning`** | `optimize-olap-database` | Active `@role` |
| **`@optimize-olap-database`** | `optimize-olap-database` | Active `@role` |
| **`@optimize_olap_database`** | `optimize-olap-database` | Active `@role` |
| **`@optimize_postgres`** | `optimize-postgres` | Active `@role` |
| **`@optimize_seo`** | `optimize-seo` | Active `@role` |
| **`@orchestrate-chaos-experiment`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@orchestrate_chaos_experiment`** | `orchestrate-chaos-experiment` | Active `@role` |
| **`@orchestration`** | `agent-graph-orchestration` | Active `@role` |
| **`@ost`** | `define-product-strategy` | Active `@role` |
| **`@page_route`** | `add-page-route` | Active `@role` |
| **`@paged_attention`** | `deploy-vllm-inference` | Active `@role` |
| **`@pairwise_testing`** | `combinatorial-testing` | Active `@role` |
| **`@pdf`** | `pdf` | Active `@role` |
| **`@perf`** | `performance-profiling` | Active `@role` |
| **`@performance`** | `performance-profiling` | Active `@role` |
| **`@performance_profiling`** | `performance-profiling` | Active `@role` |
| **`@physics`** | `configure-physics-collision` | Active `@role` |
| **`@physics-collision`** | `configure-physics-collision` | Active `@role` |
| **`@physics_collision`** | `configure-physics-collision` | Active `@role` |
| **`@pict`** | `combinatorial-testing` | Active `@role` |
| **`@pillar_cluster`** | `design-content-strategy` | Active `@role` |
| **`@planning_with_files`** | `decompose-agentic-system` | Active `@role` |
| **`@pm`** | `define-product-strategy`, `prioritize-roadmap` | Active `@role` |
| **`@pod_identity`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@postgres`** | `optimize-postgres` | Active `@role` |
| **`@postgresql`** | `optimize-postgres` | Active `@role` |
| **`@postmortem`** | `incident-report` | Active `@role` |
| **`@powerpoint`** | `pptx` | Active `@role` |
| **`@pptx`** | `pptx` | Active `@role` |
| **`@pr-faq`** | `define-product-strategy` | Active `@role` |
| **`@pr_faq`** | `define-product-strategy` | Active `@role` |
| **`@pricing`** | `model-saas-metrics` | Active `@role` |
| **`@pricing-strategy`** | `model-saas-metrics` | Active `@role` |
| **`@pricing_strategy`** | `model-saas-metrics` | Active `@role` |
| **`@prioritization`** | `prioritize-roadmap` | Active `@role` |
| **`@prioritize-roadmap`** | `prioritize-roadmap` | Active `@role` |
| **`@prioritize_roadmap`** | `prioritize-roadmap` | Active `@role` |
| **`@procedural-generation`** | `design-procedural-generation` | Active `@role` |
| **`@procedural_generation`** | `design-procedural-generation` | Active `@role` |
| **`@procgen`** | `design-procedural-generation` | Active `@role` |
| **`@product-strategy`** | `define-product-strategy` | Active `@role` |
| **`@product_brief`** | `write-product-brief` | Active `@role` |
| **`@product_strategy`** | `define-product-strategy` | Active `@role` |
| **`@profile-game-performance`** | `profile-game-performance` | Active `@role` |
| **`@profile_game_performance`** | `profile-game-performance` | Active `@role` |
| **`@program-game-shaders`** | `program-game-shaders` | Active `@role` |
| **`@program_game_shaders`** | `program-game-shaders` | Active `@role` |
| **`@proxy-fleet`** | `deploy-proxyware-fleet` | Active `@role` |
| **`@proxy_fleet`** | `deploy-proxyware-fleet` | Active `@role` |
| **`@proxyware`** | `deploy-proxyware-fleet` | Active `@role` |
| **`@prune_memory`** | `memory-hygiene` | Active `@role` |
| **`@pseo_landing`** | `generate-mmo-content` | Active `@role` |
| **`@quality_gate`** | `agent-quality-gate` | Active `@role` |
| **`@query-analytical-engine`** | `query-analytical-engine` | Active `@role` |
| **`@query_analytical_engine`** | `query-analytical-engine` | Active `@role` |
| **`@radix_cache`** | `deploy-vllm-inference` | Active `@role` |
| **`@rca`** | `systematic-debugging` | Active `@role` |
| **`@react_native`** | `develop-mobile-app` | Active `@role` |
| **`@recursive_decomposition`** | `decompose-agentic-system` | Active `@role` |
| **`@render-webgl-threejs`** | `render-webgl-threejs` | Active `@role` |
| **`@render_webgl_threejs`** | `render-webgl-threejs` | Active `@role` |
| **`@repurpose_content`** | `repurpose-content` | Active `@role` |
| **`@requirements`** | `analyze-business-requirements`, `elicit-requirements` | Active `@role` |
| **`@research`** | `conduct-research` | Active `@role` |
| **`@research-and-writing`** | `conduct-research`, `write-article` | Active `@role` |
| **`@research_and_writing`** | `conduct-research`, `write-article` | Active `@role` |
| **`@research_writing`** | `conduct-research`, `write-article` | Active `@role` |
| **`@residential_proxy`** | `deploy-mmo-infrastructure` | Active `@role` |
| **`@rice`** | `prioritize-roadmap` | Active `@role` |
| **`@rice_scoring`** | `prioritize-roadmap` | Active `@role` |
| **`@rls`** | `optimize-postgres` | Active `@role` |
| **`@roadmap`** | `prioritize-roadmap` | Active `@role` |
| **`@roi`** | `analyze-campaign-roi` | Active `@role` |
| **`@rtm`** | `trace-requirements-impact` | Active `@role` |
| **`@s2s`** | `setup-tracking-system` | Active `@role` |
| **`@s2s_tracking`** | `setup-tracking-system` | Active `@role` |
| **`@saas-metrics`** | `model-saas-metrics` | Active `@role` |
| **`@saas_metrics`** | `model-saas-metrics` | Active `@role` |
| **`@save-persistence`** | `implement-save-persistence` | Active `@role` |
| **`@save-system`** | `implement-save-persistence` | Active `@role` |
| **`@save_persistence`** | `implement-save-persistence` | Active `@role` |
| **`@save_system`** | `implement-save-persistence` | Active `@role` |
| **`@scaffold_new_service`** | `scaffold-new-service` | Active `@role` |
| **`@scaffold_service`** | `scaffold-new-service` | Active `@role` |
| **`@scene-lifecycle`** | `manage-scene-lifecycle` | Active `@role` |
| **`@scene_lifecycle`** | `manage-scene-lifecycle` | Active `@role` |
| **`@schema_graph`** | `implement-schema-markup` | Active `@role` |
| **`@schema_markup`** | `implement-schema-markup` | Active `@role` |
| **`@secrets`** | `manage-secrets` | Active `@role` |
| **`@security`** | `security-audit` | Active `@role` |
| **`@security_audit`** | `security-audit` | Active `@role` |
| **`@semantic_memory`** | `agent-semantic-memory` | Active `@role` |
| **`@seo`** | `optimize-seo` | Active `@role` |
| **`@seo_optimization`** | `optimize-seo` | Active `@role` |
| **`@service_client`** | `add-service-client` | Active `@role` |
| **`@session_management`** | `implement-auth` | Active `@role` |
| **`@setup-tracking-system`** | `setup-tracking-system` | Active `@role` |
| **`@setup_deployment`** | `setup-deployment` | Active `@role` |
| **`@setup_design_system`** | `setup-design-system` | Active `@role` |
| **`@setup_tracking`** | `setup-tracking-system` | Active `@role` |
| **`@setup_tracking_system`** | `setup-tracking-system` | Active `@role` |
| **`@setup_visual_regression`** | `setup-visual-regression` | Active `@role` |
| **`@shadcn`** | `component-composition` | Active `@role` |
| **`@slides`** | `pptx` | Active `@role` |
| **`@socratic_nudge`** | `discernment-nudge` | Active `@role` |
| **`@spreadsheet`** | `xlsx` | Active `@role` |
| **`@stealth-automation`** | `create-automation-script` | Active `@role` |
| **`@stealth_automation`** | `create-automation-script` | Active `@role` |
| **`@store_compliance`** | `deploy-mobile-app` | Active `@role` |
| **`@story-map`** | `build-story-map` | Active `@role` |
| **`@story-mapping`** | `build-story-map` | Active `@role` |
| **`@story_map`** | `build-story-map` | Active `@role` |
| **`@story_mapping`** | `build-story-map` | Active `@role` |
| **`@strategy`** | `define-product-strategy` | Active `@role` |
| **`@structured_data`** | `implement-schema-markup` | Active `@role` |
| **`@structured_outputs`** | `implement-structured-outputs` | Active `@role` |
| **`@supply_chain`** | `supply-chain-security` | Active `@role` |
| **`@systematic_debugging`** | `systematic-debugging` | Active `@role` |
| **`@taste`** | `setup-design-system` | Active `@role` |
| **`@tech_radar`** | `write-tech-radar` | Active `@role` |
| **`@technical_seo`** | `audit-technical-seo` | Active `@role` |
| **`@technical_seo_audit`** | `audit-technical-seo` | Active `@role` |
| **`@telemetry`** | `add-telemetry-instrumentation` | Active `@role` |
| **`@test_report`** | `write-tests` | Active `@role` |
| **`@tests`** | `write-tests` | Active `@role` |
| **`@tool_orchestration`** | `agent-tool-orchestration` | Active `@role` |
| **`@totp_verification`** | `manage-mmo-assets` | Active `@role` |
| **`@tracking`** | `setup-tracking-system` | Active `@role` |
| **`@tune-game-feel`** | `tune-game-feel` | Active `@role` |
| **`@tune_game_feel`** | `tune-game-feel` | Active `@role` |
| **`@ui_component`** | `add-ui-component` | Active `@role` |
| **`@unit-economics`** | `model-saas-metrics` | Active `@role` |
| **`@unit_economics`** | `model-saas-metrics` | Active `@role` |
| **`@unit_tests`** | `write-tests` | Active `@role` |
| **`@use-case`** | `write-use-cases` | Active `@role` |
| **`@use_case`** | `write-use-cases` | Active `@role` |
| **`@van_westendorp`** | `model-saas-metrics` | Active `@role` |
| **`@vcc_isolation`** | `manage-mmo-assets` | Active `@role` |
| **`@vietnam-legal`** | `manage-vietnam-legal` | Active `@role` |
| **`@vietnam_accounting`** | `manage-vietnam-accounting` | Active `@role` |
| **`@vietnam_ai_compliance`** | `audit-ai-compliance` | Active `@role` |
| **`@vietnam_legal`** | `manage-vietnam-legal` | Active `@role` |
| **`@view-transitions`** | `implement-view-transitions` | Active `@role` |
| **`@view_transitions`** | `implement-view-transitions` | Active `@role` |
| **`@visual_regression`** | `setup-visual-regression` | Active `@role` |
| **`@vllm`** | `deploy-vllm-inference` | Active `@role` |
| **`@vllm_inference`** | `deploy-vllm-inference` | Active `@role` |
| **`@vpc_lattice`** | `deploy-aws-eks-workloads` | Active `@role` |
| **`@walking_skeleton`** | `build-story-map` | Active `@role` |
| **`@webapp-server-runner`** | `webapp-server-runner` | Active `@role` |
| **`@webapp_server_runner`** | `webapp-server-runner` | Active `@role` |
| **`@webgl-threejs`** | `render-webgl-threejs` | Active `@role` |
| **`@webgl_threejs`** | `render-webgl-threejs` | Active `@role` |
| **`@with_server`** | `webapp-server-runner` | Active `@role` |
| **`@word`** | `docx` | Active `@role` |
| **`@word_document`** | `docx` | Active `@role` |
| **`@workers_best_practices`** | `workers-best-practices` | Active `@role` |
| **`@working-backwards`** | `define-product-strategy` | Active `@role` |
| **`@working_backwards`** | `define-product-strategy` | Active `@role` |
| **`@wrangler`** | `wrangler` | Active `@role` |
| **`@write-copy`** | `write-copy` | Active `@role` |
| **`@write_article`** | `write-article` | Active `@role` |
| **`@write_article_vietnamese`** | `write-article` | Active `@role` |
| **`@write_copy`** | `write-copy` | Active `@role` |
| **`@write_doc`** | `write-documentation` | Active `@role` |
| **`@write_docs`** | `write-documentation` | Active `@role` |
| **`@write_documentation`** | `write-documentation` | Active `@role` |
| **`@write_product_brief`** | `write-product-brief` | Active `@role` |
| **`@write_tech_radar`** | `write-tech-radar` | Active `@role` |
| **`@write_tests`** | `write-tests` | Active `@role` |
| **`@writing`** | `write-article` | Active `@role` |
| **`@xlsx`** | `xlsx` | Active `@role` |

---

## 🧩 Domain & Stack Overlays (21 Overlays)

| Overlay | Type | Description | Rules | Skills | File |
|:---|:---|:---|:---|:---|:---|
| **`astro-cloudflare`** | Rule-Only | Generic, reusable conventions for any Astro v5/6/7 project deployed to Cloudflare Pages/Workers. Thi... | 1 rule | 0 skills | [`overlays/astro-cloudflare/README.md`](./overlays/astro-cloudflare/README.md) |
| **`b2b-catalog-golf`** | Skill Overlay | Project-specific conventions for the B2B Golf niche catalog website — golf apparel and resort wear c... | 1 rule | 1 skill | [`overlays/b2b-catalog-golf/README.md`](./overlays/b2b-catalog-golf/README.md) |
| **`b2b-factory-catalog`** | Skill Overlay | Project-specific conventions for the B2B Factory Direct corporate website — the master brand site fo... | 1 rule | 1 skill | [`overlays/b2b-factory-catalog/README.md`](./overlays/b2b-factory-catalog/README.md) |
| **`b2b-sport-catalog`** | Rule-Only | Project-specific conventions for the B2B Sport niche catalog — custom sportswear, athletic uniforms,... | 1 rule | 0 skills | [`overlays/b2b-sport-catalog/README.md`](./overlays/b2b-sport-catalog/README.md) |
| **`cad-projection`** | Skill Overlay | Composable overlay for the `3d-graphics-engineer` role when generating precision engineering line ar... | 1 rule | 1 skill | [`overlays/cad-projection/README.md`](./overlays/cad-projection/README.md) |
| **`data-analyst-stack`** | Rule-Only | Stack overlay for the `data-analyst` role. Extends `core/roles/data-analyst.md` with conventions for... | 2 rules | 0 skills | [`overlays/data-analyst-stack/README.md`](./overlays/data-analyst-stack/README.md) |
| **`data-warehouse`** | Rule-Only | Omnichannel retail data warehouse overlay extending `core/roles/data-engineer.md`, `core/roles/data-... | 4 rules | 0 skills | [`overlays/data-warehouse/README.md`](./overlays/data-warehouse/README.md) |
| **`ecommerce-microservices`** | Rule-Only | **Status: planned** — reserved placeholder not yet populated with rules or skills. | 1 rule | 0 skills | [`overlays/ecommerce-microservices/README.md`](./overlays/ecommerce-microservices/README.md) |
| **`fintech-compliance`** | Skill Overlay | Composable overlay for the `data-analyst` and financial risk modeling roles when developing regulato... | 1 rule | 1 skill | [`overlays/fintech-compliance/README.md`](./overlays/fintech-compliance/README.md) |
| **`go-microservices`** | Rule-Only | Language-level and architecture-level conventions for Go (Golang) microservices. Bridges the portabl... | 1 rule | 0 skills | [`overlays/go-microservices/README.md`](./overlays/go-microservices/README.md) |
| **`hugo-authority-content`** | Skill Overlay | Content + SEO overlay for the authority blog (English flagship, authority-blog.example.com) and `lea... | 4 rules | 2 skills | [`overlays/hugo-authority-content/README.md`](./overlays/hugo-authority-content/README.md) |
| **`hvac-authority-content`** | Skill Overlay | This overlay provides domain-specific engineering rules, HVAC technical schemas, and publishing work... | 3 rules | 1 skill | [`overlays/hvac-authority-content/README.md`](./overlays/hvac-authority-content/README.md) |
| **`laravel-ecommerce`** | Skill Overlay | Project-specific conventions for the Laravel 13 e-commerce platform (~20 SKUs). | 2 rules | 1 skill | [`overlays/laravel-ecommerce/README.md`](./overlays/laravel-ecommerce/README.md) |
| **`laravel-filament`** | Skill Overlay | Generic, reusable conventions for any Laravel 13+ project using Filament v4 admin, Livewire 3 intera... | 1 rule | 1 skill | [`overlays/laravel-filament/README.md`](./overlays/laravel-filament/README.md) |
| **`livestream-web`** | Rule-Only | Project-specific conventions for the web-first live-streaming platform with desktop-priority UX. | 1 rule | 0 skills | [`overlays/livestream-web/README.md`](./overlays/livestream-web/README.md) |
| **`obj-configurator`** | Skill Overlay | Project-specific conventions for the 3D Product Configurator — an interactive WebGL application for ... | 1 rule | 1 skill | [`overlays/obj-configurator/README.md`](./overlays/obj-configurator/README.md) |
| **`r3f-stack`** | Skill Overlay | React Three Fiber / Three.js / WebGL+WebGPU skill cluster. Provides 3D rendering skills for projects... | 1 rule | 3 skills | [`overlays/r3f-stack/README.md`](./overlays/r3f-stack/README.md) |
| **`real-estate-content`** | Skill Overlay | This overlay contains content-specific extensions for the Real Estate Portal and HVAC Portal Astro c... | 3 rules | 1 skill | [`overlays/real-estate-content/README.md`](./overlays/real-estate-content/README.md) |
| **`security-research`** | Skill Overlay | Composable overlay for the `security-engineer` role when conducting binary disassembly, decompilatio... | 1 rule | 1 skill | [`overlays/security-research/README.md`](./overlays/security-research/README.md) |
| **`seo-publishing`** | Rule-Only | Publishing overlay for recurring SEO content on **Real Estate Portal** and **HVAC Authority Portal**... | 4 rules | 0 skills | [`overlays/seo-publishing/README.md`](./overlays/seo-publishing/README.md) |
| **`ui-design-system`** | Rule-Only | Composable overlay for the `ui-ux-designer` role when work must follow a **brand or project design s... | 1 rule | 0 skills | [`overlays/ui-design-system/README.md`](./overlays/ui-design-system/README.md) |

---

## 📦 Engineering Packs (17 Packs)

| Pack | Description | Includes | Manifest | Documentation |
|:---|:---|:---|:---|:---|
| **`affiliate-cashback-team`** | Tri-Engine Affiliate & Cashback Growth Engineering Pack for CashbackHub ecosystem (deal-bot-dispatch... | `core`, `overlays/seo-publishing`, `overlays/ui-design-system` | [`manifest.yaml`](./packs/affiliate-cashback-team/manifest.yaml) | [`README.md`](./packs/affiliate-cashback-team/README.md) |
| **`b2b-catalog-team`** | Global engineering core plus Astro v6/v7 + Cloudflare Workers conventions plus B2B Factory Direct ma... | `core`, `overlays/astro-cloudflare`, `overlays/b2b-factory-catalog` | [`manifest.yaml`](./packs/b2b-catalog-team/manifest.yaml) | — |
| **`b2b-golf-team`** | Global engineering core plus Astro v6/v7 + Cloudflare conventions plus B2B Golf niche catalog overla... | `core`, `overlays/astro-cloudflare`, `overlays/b2b-catalog-golf` | [`manifest.yaml`](./packs/b2b-golf-team/manifest.yaml) | — |
| **`b2b-sport-team`** | Global engineering core plus Astro v6/v7 + Cloudflare conventions plus B2B Sport niche catalog overl... | `core`, `overlays/astro-cloudflare`, `overlays/b2b-sport-catalog` | [`manifest.yaml`](./packs/b2b-sport-team/manifest.yaml) | — |
| **`content-sprint-team`** | Global engineering core plus SEO publishing sprint cadence overlay for generic dual-site sprints. Co... | `core`, `overlays/seo-publishing` | [`manifest.yaml`](./packs/content-sprint-team/manifest.yaml) | — |
| **`data-analyst-team`** | Global engineering core plus DuckDB, Metabase, dbt Core 1.9, and Apache Iceberg analytics stack over... | `core`, `overlays/data-analyst-stack` | [`manifest.yaml`](./packs/data-analyst-team/manifest.yaml) | — |
| **`data-warehouse`** | Comprehensive engineering pack for teams building, scaling, and maintaining the Omnichannel Retail D... | `core`, `overlays/data-warehouse` | [`manifest.yaml`](./packs/data-warehouse/manifest.yaml) | — |
| **`ecommerce-team`** | Global engineering core plus Go 1.25/Kratos v3 microservices conventions and Ecommerce Microservices... | `core`, `overlays/go-microservices`, `overlays/ecommerce-microservices` | [`manifest.yaml`](./packs/ecommerce-team/manifest.yaml) | — |
| **`global-engineering`** | Portable global engineering pack without repo-specific overlays. Loads for any project that does not... | `core` | [`manifest.yaml`](./packs/global-engineering/manifest.yaml) | — |
| **`hugo-authority-team`** | Content + SEO swarm pack for the Hugo twin sites. Enforces mandatory 100-round deep research before ... | `core`, `overlays/hugo-authority-content` | [`manifest.yaml`](./packs/hugo-authority-team/manifest.yaml) | [`README.md`](./packs/hugo-authority-team/README.md) |
| **`hvac-content-team`** | High-authority content, SEO engineering, and Cloudflare Pages pack for HVAC Authority Portal (https:... | `core`, `overlays/astro-cloudflare`, `overlays/hvac-authority-content`, `overlays/seo-publishing` | [`manifest.yaml`](./packs/hvac-content-team/manifest.yaml) | [`README.md`](./packs/hvac-content-team/README.md) |
| **`landing-pages-team`** | High-converting single-product landing page engine and merchant SaaS platform pack (landing-builder.... | `core`, `overlays/go-microservices`, `overlays/ui-design-system`, `overlays/seo-publishing` | [`manifest.yaml`](./packs/landing-pages-team/manifest.yaml) | [`README.md`](./packs/landing-pages-team/README.md) |
| **`laravel-ecommerce-team`** | Global engineering core plus Laravel 13 + Filament v4 + Livewire 3 conventions plus Laravel E-Commer... | `core`, `overlays/laravel-filament`, `overlays/laravel-ecommerce` | [`manifest.yaml`](./packs/laravel-ecommerce-team/manifest.yaml) | — |
| **`livestream-team`** | Global engineering core plus Livestream Platform web-first livestream UX overlay. Covers desktop-fir... | `core`, `overlays/livestream-web` | [`manifest.yaml`](./packs/livestream-team/manifest.yaml) | — |
| **`mmo-growth-team`** | Full-spectrum MMO growth engineering and traffic arbitrage swarm pack. Enforces 2027 SOTA standards ... | `core` | [`manifest.yaml`](./packs/mmo-growth-team/manifest.yaml) | [`README.md`](./packs/mmo-growth-team/README.md) |
| **`obj-team`** | Global engineering core plus Astro v6/v7 + Cloudflare conventions plus OBJ 3D Configurator overlay. ... | `core`, `overlays/astro-cloudflare`, `overlays/obj-configurator` | [`manifest.yaml`](./packs/obj-team/manifest.yaml) | — |
| **`real-estate-team`** | High-authority content engineering and SEO publishing pack for Real Estate Portal (https://real-esta... | `core`, `overlays/real-estate-content`, `overlays/seo-publishing` | [`manifest.yaml`](./packs/real-estate-team/manifest.yaml) | [`README.md`](./packs/real-estate-team/README.md) |

---

## 🔄 Workflows (25 Workflows)

| Workflow | Title | File |
|:---|:---|:---|
| **`/add-new-feature`** | add-new-feature | [`core/workflows/add-new-feature.md`](./core/workflows/add-new-feature.md) |
| **`/agent-a2a-delegation`** | agent-a2a-delegation | [`core/workflows/agent-a2a-delegation.md`](./core/workflows/agent-a2a-delegation.md) |
| **`/bug-fix`** | bug-fix | [`core/workflows/bug-fix.md`](./core/workflows/bug-fix.md) |
| **`/build-deploy`** | build-deploy | [`core/workflows/build-deploy.md`](./core/workflows/build-deploy.md) |
| **`/code-review`** | code-review | [`core/workflows/code-review.md`](./core/workflows/code-review.md) |
| **`/content-audit`** | content-audit | [`core/workflows/content-audit.md`](./core/workflows/content-audit.md) |
| **`/content-publishing`** | content-publishing | [`core/workflows/content-publishing.md`](./core/workflows/content-publishing.md) |
| **`/curriculum-delivery`** | curriculum-delivery | [`core/workflows/curriculum-delivery.md`](./core/workflows/curriculum-delivery.md) |
| **`/data-migration`** | data-migration | [`core/workflows/data-migration.md`](./core/workflows/data-migration.md) |
| **`/data-pipeline-incident`** | data-pipeline-incident | [`core/workflows/data-pipeline-incident.md`](./core/workflows/data-pipeline-incident.md) |
| **`/dependency-upgrade`** | dependency-upgrade | [`core/workflows/dependency-upgrade.md`](./core/workflows/dependency-upgrade.md) |
| **`/feature-delivery`** | feature-delivery | [`core/workflows/feature-delivery.md`](./core/workflows/feature-delivery.md) |
| **`/hotfix-production`** | hotfix-production | [`core/workflows/hotfix-production.md`](./core/workflows/hotfix-production.md) |
| **`/mmo-campaign-lifecycle`** | mmo-campaign-lifecycle | [`core/workflows/mmo-campaign-lifecycle.md`](./core/workflows/mmo-campaign-lifecycle.md) |
| **`/period-end-closing`** | period-end-closing | [`core/workflows/period-end-closing.md`](./core/workflows/period-end-closing.md) |
| **`/qa-validation`** | qa-validation | [`core/workflows/qa-validation.md`](./core/workflows/qa-validation.md) |
| **`/refactoring`** | refactoring | [`core/workflows/refactoring.md`](./core/workflows/refactoring.md) |
| **`/revert-deployment`** | revert-deployment | [`core/workflows/revert-deployment.md`](./core/workflows/revert-deployment.md) |
| **`/security-incident-response`** | security-incident-response | [`core/workflows/security-incident-response.md`](./core/workflows/security-incident-response.md) |
| **`/seo-content-lifecycle`** | seo-content-lifecycle | [`core/workflows/seo-content-lifecycle.md`](./core/workflows/seo-content-lifecycle.md) |
| **`/seo-keyword-brief`** | seo-keyword-brief | [`core/workflows/seo-keyword-brief.md`](./core/workflows/seo-keyword-brief.md) |
| **`/service-review-release`** | service-review-release | [`core/workflows/service-review-release.md`](./core/workflows/service-review-release.md) |
| **`/setup-new-service`** | setup-new-service | [`core/workflows/setup-new-service.md`](./core/workflows/setup-new-service.md) |
| **`/tech-repo-review`** | tech-repo-review | [`core/workflows/tech-repo-review.md`](./core/workflows/tech-repo-review.md) |
| **`/troubleshooting`** | troubleshooting | [`core/workflows/troubleshooting.md`](./core/workflows/troubleshooting.md) |

---

## 📑 Data Contracts & Schemas (60 Data Contract Schemas)

| Schema File | Schema Title | Path |
|:---|:---|:---|
| `a2a-artifact.json` | A2A Task Artifact | [`core/contracts/schemas/a2a-artifact.json`](./core/contracts/schemas/a2a-artifact.json) |
| `a2a-jsonrpc-envelope.json` | A2A JSON-RPC 2.0 Envelope | [`core/contracts/schemas/a2a-jsonrpc-envelope.json`](./core/contracts/schemas/a2a-jsonrpc-envelope.json) |
| `a2a-message.json` | A2A Message | [`core/contracts/schemas/a2a-message.json`](./core/contracts/schemas/a2a-message.json) |
| `a2a-push-notification-config.json` | A2A Push Notification Config | [`core/contracts/schemas/a2a-push-notification-config.json`](./core/contracts/schemas/a2a-push-notification-config.json) |
| `a2a-task-cancel.json` | A2A Task Cancel Request | [`core/contracts/schemas/a2a-task-cancel.json`](./core/contracts/schemas/a2a-task-cancel.json) |
| `a2a-task-progress.json` | A2A Task Progress Event | [`core/contracts/schemas/a2a-task-progress.json`](./core/contracts/schemas/a2a-task-progress.json) |
| `a2a-task-status.json` | A2A Task Status | [`core/contracts/schemas/a2a-task-status.json`](./core/contracts/schemas/a2a-task-status.json) |
| `a2a-task.json` | A2A Task Delegation | [`core/contracts/schemas/a2a-task.json`](./core/contracts/schemas/a2a-task.json) |
| `accounting-compliance-review.json` | Vietnam Accounting Compliance Review | [`core/contracts/schemas/accounting-compliance-review.json`](./core/contracts/schemas/accounting-compliance-review.json) |
| `adr-spec.json` | Architecture Decision Record | [`core/contracts/schemas/adr-spec.json`](./core/contracts/schemas/adr-spec.json) |
| `agent-card.json` | A2A Agent Card | [`core/contracts/schemas/agent-card.json`](./core/contracts/schemas/agent-card.json) |
| `agent-eval-report.json` | Agent Evaluation Report | [`core/contracts/schemas/agent-eval-report.json`](./core/contracts/schemas/agent-eval-report.json) |
| `agent-trace-span.json` | Agent Trace Span | [`core/contracts/schemas/agent-trace-span.json`](./core/contracts/schemas/agent-trace-span.json) |
| `ai-risk-register.json` | AI Risk Register | [`core/contracts/schemas/ai-risk-register.json`](./core/contracts/schemas/ai-risk-register.json) |
| `amis-voucher-contract.json` | AMIS Accounting Voucher Contract | [`core/contracts/schemas/amis-voucher-contract.json`](./core/contracts/schemas/amis-voucher-contract.json) |
| `api-contract-spec.json` | API Contract Specification | [`core/contracts/schemas/api-contract-spec.json`](./core/contracts/schemas/api-contract-spec.json) |
| `architecture-options.json` | Architecture Options Brief | [`core/contracts/schemas/architecture-options.json`](./core/contracts/schemas/architecture-options.json) |
| `assumptions-ledger.json` | Assumptions Ledger Specification | [`core/contracts/schemas/assumptions-ledger.json`](./core/contracts/schemas/assumptions-ledger.json) |
| `aws-infra-spec.json` | AWS Infrastructure Specification | [`core/contracts/schemas/aws-infra-spec.json`](./core/contracts/schemas/aws-infra-spec.json) |
| `code-review-finding.json` | Code Review Finding | [`core/contracts/schemas/code-review-finding.json`](./core/contracts/schemas/code-review-finding.json) |
| `compact-working-state.json` | Compact Working State Specification | [`core/contracts/schemas/compact-working-state.json`](./core/contracts/schemas/compact-working-state.json) |
| `content-audit-report.json` | Content Audit Report | [`core/contracts/schemas/content-audit-report.json`](./core/contracts/schemas/content-audit-report.json) |
| `content-handoff.json` | Content Handoff | [`core/contracts/schemas/content-handoff.json`](./core/contracts/schemas/content-handoff.json) |
| `coordination-plan.json` | Coordination Plan | [`core/contracts/schemas/coordination-plan.json`](./core/contracts/schemas/coordination-plan.json) |
| `data-analysis-report.json` | Data Analysis Report | [`core/contracts/schemas/data-analysis-report.json`](./core/contracts/schemas/data-analysis-report.json) |
| `data-pipeline-spec.json` | Data Pipeline Specification | [`core/contracts/schemas/data-pipeline-spec.json`](./core/contracts/schemas/data-pipeline-spec.json) |
| `deployment-plan.json` | Deployment Plan | [`core/contracts/schemas/deployment-plan.json`](./core/contracts/schemas/deployment-plan.json) |
| `design-tokens-spec.json` | Design Tokens Specification | [`core/contracts/schemas/design-tokens-spec.json`](./core/contracts/schemas/design-tokens-spec.json) |
| `document-manifest.json` | Document Manifest Specification | [`core/contracts/schemas/document-manifest.json`](./core/contracts/schemas/document-manifest.json) |
| `documentation-handoff.json` | Documentation Handoff | [`core/contracts/schemas/documentation-handoff.json`](./core/contracts/schemas/documentation-handoff.json) |
| `edge-deployment-spec.json` | Edge Deployment Specification | [`core/contracts/schemas/edge-deployment-spec.json`](./core/contracts/schemas/edge-deployment-spec.json) |
| `feature-ticket.json` | Feature Ticket Specification | [`core/contracts/schemas/feature-ticket.json`](./core/contracts/schemas/feature-ticket.json) |
| `implementation-result.json` | Implementation Result | [`core/contracts/schemas/implementation-result.json`](./core/contracts/schemas/implementation-result.json) |
| `incident-report.json` | Incident Report | [`core/contracts/schemas/incident-report.json`](./core/contracts/schemas/incident-report.json) |
| `learning-assessment-report.json` | Learning Assessment Report | [`core/contracts/schemas/learning-assessment-report.json`](./core/contracts/schemas/learning-assessment-report.json) |
| `learning-handoff.json` | Learning Handoff | [`core/contracts/schemas/learning-handoff.json`](./core/contracts/schemas/learning-handoff.json) |
| `legal-compliance-review.json` | Vietnam Legal Compliance Review | [`core/contracts/schemas/legal-compliance-review.json`](./core/contracts/schemas/legal-compliance-review.json) |
| `legal-opinion-contract.json` | Vietnam Legal Opinion Contract | [`core/contracts/schemas/legal-opinion-contract.json`](./core/contracts/schemas/legal-opinion-contract.json) |
| `memory-audit-report.json` | Memory Audit Report | [`core/contracts/schemas/memory-audit-report.json`](./core/contracts/schemas/memory-audit-report.json) |
| `mmo-campaign-spec.json` | MMO Campaign Specification | [`core/contracts/schemas/mmo-campaign-spec.json`](./core/contracts/schemas/mmo-campaign-spec.json) |
| `mmo-roi-report.json` | MMO Campaign ROI Report | [`core/contracts/schemas/mmo-roi-report.json`](./core/contracts/schemas/mmo-roi-report.json) |
| `performance-audit.json` | Performance Audit Result | [`core/contracts/schemas/performance-audit.json`](./core/contracts/schemas/performance-audit.json) |
| `period-end-closing-report.json` | Period-End Closing Report | [`core/contracts/schemas/period-end-closing-report.json`](./core/contracts/schemas/period-end-closing-report.json) |
| `pull-request-spec.json` | Pull Request Specification | [`core/contracts/schemas/pull-request-spec.json`](./core/contracts/schemas/pull-request-spec.json) |
| `research-report.json` | Research Report Specification | [`core/contracts/schemas/research-report.json`](./core/contracts/schemas/research-report.json) |
| `schema-migration.json` | Schema Migration Plan | [`core/contracts/schemas/schema-migration.json`](./core/contracts/schemas/schema-migration.json) |
| `security-audit.json` | Security Audit Report | [`core/contracts/schemas/security-audit.json`](./core/contracts/schemas/security-audit.json) |
| `seo-audit-report.json` | SEO Audit Report | [`core/contracts/schemas/seo-audit-report.json`](./core/contracts/schemas/seo-audit-report.json) |
| `seo-content-brief.json` | SEO Content Brief | [`core/contracts/schemas/seo-content-brief.json`](./core/contracts/schemas/seo-content-brief.json) |
| `seo-metadata.json` | SEO Metadata | [`core/contracts/schemas/seo-metadata.json`](./core/contracts/schemas/seo-metadata.json) |
| `seo-weekly-board.json` | SEO Weekly Board | [`core/contracts/schemas/seo-weekly-board.json`](./core/contracts/schemas/seo-weekly-board.json) |
| `series-article.json` | Series Article | [`core/contracts/schemas/series-article.json`](./core/contracts/schemas/series-article.json) |
| `solution-brief.json` | Solution Brief | [`core/contracts/schemas/solution-brief.json`](./core/contracts/schemas/solution-brief.json) |
| `stock-audit-session.json` | Stock Audit Session Contract | [`core/contracts/schemas/stock-audit-session.json`](./core/contracts/schemas/stock-audit-session.json) |
| `system-design-spec.json` | System Design Specification | [`core/contracts/schemas/system-design-spec.json`](./core/contracts/schemas/system-design-spec.json) |
| `technical-delivery-plan.json` | Technical Delivery Plan | [`core/contracts/schemas/technical-delivery-plan.json`](./core/contracts/schemas/technical-delivery-plan.json) |
| `test-report.json` | QA Test Report | [`core/contracts/schemas/test-report.json`](./core/contracts/schemas/test-report.json) |
| `ui-component-spec.json` | UI Component Specification | [`core/contracts/schemas/ui-component-spec.json`](./core/contracts/schemas/ui-component-spec.json) |
| `ux-flow-spec.json` | UX Flow Specification | [`core/contracts/schemas/ux-flow-spec.json`](./core/contracts/schemas/ux-flow-spec.json) |
| `validation-result.json` | Validation Result | [`core/contracts/schemas/validation-result.json`](./core/contracts/schemas/validation-result.json) |