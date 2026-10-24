# Agent Skills — Engineering & Multi-Agent Pack

**Version 5.6.0** · Portable engineering standards, principal-level agent roles, modular skills, structured data contracts, and end-to-end workflows for AI coding assistants and autonomous multi-agent swarms.

> **Catalog**: **38 Roles** · **182 Skills** (167 Core + 15 Overlays) · **25 Workflows** · **60 JSON Schemas** · **17 Team Packs** · **21 Overlays**  
> **Navigation**: [Master Index (`INDEX.md`)](INDEX.md) · [Machine Registry (`role-skill-index.json`)](core/a2a/.well-known/role-skill-index.json) · [Contributing Guide](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

---

## Why Agent Skills?

Modern AI-assisted engineering shifts from ad-hoc prompting to **Context Engineering**, **PromptOps**, and **Autonomous Multi-Agent Swarms**:

- **Strict Role & Skill Boundaries**: 38 specialized roles with enforced Primary/Supporting Skill Toolboxes, architectural `*-LOCK` guardrails, and dedicated review checklists.
- **Contract-First Handoffs (A2A 1.0)**: Native Agent-to-Agent (JSON-RPC 2.0 / SSE) discovery and handoffs validated against 60 JSON Schema (Draft 2020-12) contracts.
- **Fail-Closed Policy Governance**: Machine-readable action boundaries (`core/policies/action-boundaries.yaml`), data classification, and OWASP ASI01–ASI10 guardrails.
- **Portable Core + Modular Overlays**: Keep `core/` 100% stack- and brand-agnostic while layering project- or domain-specific rules via `overlays/` and `packs/`.

---

## Quick Start

### 1. Install via npm (Node.js)

```bash
npm install @vesviet/agent-skills
npx agent-skills list --taxonomy gamedev
npx agent-skills install --target claude --taxonomy frontend,gamedev
```

The CLI copies selected skills into your agent platform's skills directory
(`zcode`, `claude`, or any directory via `--path`). Requires Node.js >= 20.
Validations and generators remain Python-side (`requirements-dev.txt`).

### 2. Add to Your Repository

```bash
git submodule add <repo-url> agent-skills
```

### 3. Activate Your AI Agent / IDE

| Agent / IDE | Entrypoint / Adapter | Activation & Capabilities |
|---|---|---|
| **Google Antigravity** | [`adapters/antigravity/ANTIGRAVITY.md`](adapters/antigravity/ANTIGRAVITY.md) | `@role` & `@skill` routing, full A2A 1.0 lifecycle, JSON contracts |
| **Claude Code** | [`CLAUDE.md`](CLAUDE.md) + [`adapters/claude/CLAUDE_ADAPTER.md`](adapters/claude/CLAUDE_ADAPTER.md) | Auto-loads rules, roles, skills, and slash commands |
| **Cursor** | [`.cursorrules`](.cursorrules) + [`.cursor/rules/agent-skills.md`](.cursor/rules/agent-skills.md) | Auto-loads rules, roles, skills, workflows, and policy hooks |
| **OpenAI Codex** | [`AGENTS.md`](AGENTS.md) + [`core/codex/README.md`](core/codex/README.md) | Rules via `AGENTS.md`; per-skill manifests via `$skill-name` |
| **Kiro** | [`.kiro/steering/agent-skills.md`](.kiro/steering/agent-skills.md) | Always-on steering rules + policy/role/trace hooks |
| **Kilo Code** | [`AGENTS.md`](AGENTS.md) + [`.kilocode/rules/agent-skills.md`](.kilocode/rules/agent-skills.md) | Auto-loads rules, roles, skills, and workflows |
| **VS Code Copilot** | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) + [`AGENTS.md`](AGENTS.md) | Workspace rules, role routing, and MCP integration |
| **Windsurf / Others** | [`AGENTS.md`](AGENTS.md) | Standard open `AGENTS.md` entrypoint |

---

## Repository Architecture

| Directory | Purpose | Documentation |
|---|---|---|
| [`core/rules/`](core/rules/README.md) | Always-on engineering rules, code standards, and commit/release safety gates | [Rules Guide](core/rules/README.md) |
| [`core/roles/`](core/roles/README.md) | 38 principal-level role definitions and 20 dedicated review checklists | [Roles Catalog](core/roles/README.md) |
| [`core/skills/`](core/skills/README.md) | 167 portable core skills organized across 22 engineering & domain categories | [Skills Inventory](core/skills/README.md) |
| [`core/workflows/`](core/workflows/README.md) | 25 multi-step, role-tagged standard operating procedures | [Workflows Index](core/workflows/README.md) |
| [`core/contracts/`](core/contracts/README.md) | 60 JSON Schema (Draft 2020-12) specifications for structured agent outputs | [Contracts Catalog](core/contracts/README.md) |
| [`core/policies/`](core/policies/README.md) | Zero-trust action boundaries, data classification, and execution sandbox specs | [Policies Guide](core/policies/README.md) |
| [`core/a2a/`](core/a2a/README.md) | A2A 1.0 JSON-RPC/SSE protocol specs, `.well-known` discovery, and 38 Agent Cards | [A2A Architecture](core/a2a/README.md) |
| [`core/prompts/`](core/prompts/README.md) | Golden prompt evaluation suites and PromptOps lifecycle assets | [PromptOps Guide](core/prompts/README.md) |
| [`overlays/`](overlays/README.md) | 21 optional stack, project, and domain extensions (15 overlay skills) | [Overlays Index](overlays/README.md) |
| [`packs/`](packs/README.md) | 17 ready-to-deploy team manifests combining `core/` with targeted `overlays/` | [Team Packs](packs/README.md) |

---

## Core Catalog Overview

### 1. Skills by Domain (182 Total: 167 Core + 15 Overlays)

Full searchable inventory: [`core/skills/README.md`](core/skills/README.md)

| Domain Group | Categories & Representative Capabilities |
|---|---|
| **Agent & AI Systems** | **`agent`** (24), **`ai`** (1), **`ai-agent`** (3) — A2A 1.0 protocol, graph orchestration, context compaction, semantic memory, MCP server architecture, vLLM v1 inference (`deploy-vllm-inference`) |
| **Software Engineering** | **`foundation`** (22), **`backend`** (8), **`frontend`** (16), **`mobile`** (4), **`repo-ops`** (5) — API endpoints, auth, Postgres optimization, UI components, design systems, systematic debugging, code/service review |
| **Cloud & Platform** | **`platform`** (18), **`security-data`** (10) — AWS OpenTofu/Crossplane (`aws-infrastructure`), EKS Karpenter (`deploy-aws-eks-workloads`), Cloudflare Workers/DO, GPU FinOps, LLM gateway, OWASP ASI security audits |
| **Product, Business & QA** | **`product`** (4), **`business`** (3), **`meetings-analysis`** (5) — RICE/WSJF roadmaps, SaaS metrics, BABOK requirements elicitation, story mapping, 6-round panel reviews |
| **Specialized Verticals** | **`gamedev`** (20), **`commerce`** (6), **`content`** (6), **`seo`** (2), **`mmo`** (8), **`legal-compliance`** (3), **`education`** (5), **`document`** (4), **`documentation`** (3) |

### 2. Standard Workflows (25 Procedures)

Full workflow specifications: [`core/workflows/README.md`](core/workflows/README.md)

| Category | Workflows |
|---|---|
| **Engineering Delivery** | - `/add-new-feature` · - `/feature-delivery` · - `/bug-fix` · - `/refactoring` · - `/code-review` · - `/qa-validation` · - `/dependency-upgrade` |
| **Platform & Operations** | - `/setup-new-service` · - `/build-deploy` · - `/service-review-release` · - `/troubleshooting` · - `/hotfix-production` · - `/revert-deployment` · - `/security-incident-response` |
| **Data & Architecture** | - `/agent-a2a-delegation` · - `/tech-repo-review` · - `/data-migration` · - `/data-pipeline-incident` · - `/period-end-closing` |
| **Content, Growth & Education** | - `/content-publishing` · - `/content-audit` · - `/seo-content-lifecycle` · - `/seo-keyword-brief` · - `/mmo-campaign-lifecycle` · - `/curriculum-delivery` |

### 3. Modular Overlays (21 Extensions)

Full overlay documentation: [`overlays/README.md`](overlays/README.md)

| Tier | Overlays |
|---|---|
| **Stack Overlays (4)** | `astro-cloudflare` · `laravel-filament` · `go-microservices` · `r3f-stack` |
| **Project Overlays (7)** | `laravel-ecommerce` · `b2b-factory-catalog` · `b2b-catalog-golf` · `b2b-sport-catalog` · `obj-configurator` · `ecommerce-microservices` · `livestream-web` |
| **Domain Overlays (10)** | `hugo-authority-content` · `real-estate-content` · `hvac-authority-content` · `seo-publishing` · `ui-design-system` · `data-analyst-stack` · `data-warehouse` · `cad-projection` · `fintech-compliance` · `security-research` |

---

## Quality Gates & Verification

Run the automated validation suite after modifying rules, roles, skills, workflows, schemas, or overlays:

```bash
# Run all 18 core pack validators (rules, skills, roles, workflows, packs, overlays, A2A, schemas, policies, indexes)
python3 core/scripts/validate-all.py

# Regenerate A2A Agent Cards and Master Index after role or version updates
python3 core/scripts/generate-a2a-registry.py
python3 core/scripts/generate-index.py --check

# Run the empirical pytest challenge suite (700 tests)
pytest tests/ -q
```

---

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade pass added this footer so every prose file in the pack carries a consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in [`core/roles/role-standard.md`](core/roles/role-standard.md) (ASI01–ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: concrete failure scenarios belong in each skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this pack conform to schemas in [`core/contracts/schemas/`](core/contracts/schemas/INDEX.md).
- **Skill Toolbox Lock**: enforced by the owning role and runtime gate [`core/scripts/hooks/check-policy.py`](core/scripts/hooks/check-policy.py).
- **Commit / Publish Gate**: changes follow the META-RULE in [`core/rules/code.md`](core/rules/code.md) — no commit, push, or publish without explicit user confirmation.

Last updated: 2026-10-24
