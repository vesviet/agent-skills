# Engineering Agent Skills

Global engineering skill pack for software delivery work.

The repository is now split into a portable **core** plus optional **overlays** so global teams can reuse the foundation without inheriting repo-specific or brand-specific assumptions.

As of 2026, the core pack reflects the industry shift from ad-hoc prompting to **Context Engineering** and **PromptOps**: prompts are treated as versioned, testable assets; tool integration follows the **Model Context Protocol (MCP)** standard; and prompt quality is measured through automated evaluation rather than gut-feel assessment.

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
- `lease-content`: content-writing helpers for Lease in Vietnam and May Lanh Treo Tuong Astro content trees
- `ecommerce-microservices`: reserved for service-level or platform-specific conventions
- `astro-cloudflare`: Astro v5 on Cloudflare Pages/Workers conventions
- `data-analyst-stack`: DuckDB + Metabase + Excel/BI workflow conventions
- `go-microservices`: Go service and gRPC conventions
- `data-engineer-rabity`: data engineering conventions for the Rabity stack
- `donthan-web`: web content/SEO helpers for Don Than site
- `golf-icm`: Golf catalog conventions for the ICM Cloudflare site
- `icm-main`: ICM Factory main site conventions
- `laravel-filament`: Laravel + Filament admin conventions
- `maydiengiaisaigon`: content/SEO helpers for May Dien Gia Sai Gon
- `obj-configurator`: OBJ product configurator conventions
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
| [commit-code](core/skills/foundation/commit-code/SKILL.md) | Pre-commit validation and commit flow |
| [create-migration](core/skills/foundation/create-migration/SKILL.md) | Add safe schema migrations |
| [meeting-review](core/skills/foundation/meeting-review/SKILL.md) | Structured multi-angle technical review |
| [navigate-service](core/skills/foundation/navigate-service/SKILL.md) | Understand an unfamiliar service quickly |
| [performance-profiling](core/skills/foundation/performance-profiling/SKILL.md) | Profile hot paths and regressions |
| [review-code](core/skills/foundation/review-code/SKILL.md) | Review code changes with prioritized findings |
| [review-service](core/skills/foundation/review-service/SKILL.md) | Full service readiness and release review |
| [troubleshoot-service](core/skills/foundation/troubleshoot-service/SKILL.md) | Diagnose build, startup, and runtime failures |
| [write-tests](core/skills/foundation/write-tests/SKILL.md) | Add or improve unit and integration tests |
| [conduct-research](core/skills/foundation/conduct-research/SKILL.md) | Deep or scoped research before decisions |
| [design-review](core/skills/foundation/design-review/SKILL.md) | UX/spec design critique before build |
| [accessibility-review](core/skills/foundation/accessibility-review/SKILL.md) | WCAG-oriented a11y audit |

### Delivery Domains

| Domain | Representative skills |
|--------|-----------------------|
| Backend | `add-api-endpoint`, `add-event-handler`, `add-service-client`, `scaffold-new-service` |
| Frontend | `add-ui-component`, `add-page-route`, `integrate-api-client`, `frontend-testing` |
| Platform | `setup-deployment`, `wrangler`, `debug-runtime-platform`, `add-telemetry-instrumentation` |
| Commerce | `integrate-payment-gateway`, `handle-checkout-flow`, `manage-product-catalog`, `manage-order-fulfillment` |
| Security and Data | `manage-secrets`, `database-maintenance`, `security-audit`, `build-data-pipeline` |
| Documentation | `write-documentation`, `write-tech-radar` |

Full inventory: [core/skills/README.md](core/skills/README.md)

## Workflows

Core workflows live in [core/workflows/README.md](core/workflows/README.md).

- `/add-new-feature`
- `/build-deploy`
- `/hotfix-production`
- `/revert-deployment`
- `/refactoring`
- `/service-review-release`
- `/setup-new-service`
- `/troubleshooting`
- `/agent-a2a-delegation`
- `/content-publishing`
- `/data-migration`
- `/dependency-upgrade`
- `/qa-validation`
- `/security-incident-response`
- `/seo-content-lifecycle`
- `/seo-keyword-brief`
- `/tech-repo-review`

## Quality Gates

Run these validators after editing core rules, skills, roles, or workflows (includes 2026 compliance):

```bash
python3 core/scripts/validate-rules.py
python3 core/scripts/validate-skills.py
python3 core/scripts/validate-roles.py
python3 core/scripts/validate-workflows.py
python3 core/scripts/validate-all.py
```

The validators enforce structure and references inside the **core** pack. Overlays can adopt the same patterns, but the current validation gate treats core as the portable source of truth.

## Agent Compatibility

This pack includes adapter files for all major AI coding agents:

| Agent | Adapter File | Auto-Loads |
|-------|-------------|------------|
| OpenAI Codex | `core/skills/*/*/agents/openai.yaml` plus overlay skill adapters when installed | Skills via `$skill-name` |
| Cursor | `.cursorrules` + `.cursor/rules/agent-skills.md` | Rules, roles, skills, workflows |
| Claude Code | `CLAUDE.md` | Rules, roles, skills, workflows |
| AGENTS-compatible tools | `AGENTS.md` | Rules, roles, skills, workflows |
| GitHub Copilot | `.github/copilot-instructions.md` | Rules and pack navigation |

All adapters point back to the same source of truth in `core/`.

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
