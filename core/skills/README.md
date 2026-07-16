# Skills Inventory

This directory contains the **portable core** skill inventory for the global engineering pack.

**Counts:** 91 portable core skills under `core/skills/` + 7 overlay skills under `overlays/*/skills/` = **98 total** (run `validate-skills.py` for the live total).

## Taxonomy

### Agent (21)

Agent operating discipline, orchestration, and agentic web standards:

- `agent-a2a-protocol`
- `agent-context-management`
- `agent-delegation`
- `agent-graph-orchestration`
- `agent-handoff`
- `agent-memory-compaction`
- `agent-model-routing`
- `agent-observability`
- `agent-prompt-lifecycle`
- `agent-semantic-memory`
- `agent-tool-orchestration`
- `agent-quality-gate`
- `manage-agent-identity`

#### Agent Infrastructure & Agentic Web Standards (8)

Configuration and compliance skills for agentic-ready web presence (MCP, RFC 9727, x402, WorkOS):

- `configure-agent-commerce`
- `configure-agent-headers`
- `configure-agent-skills`
- `configure-mcp`
- `configure-oauth-metadata`
- `debug-workos-integration`
- `manage-api-catalog`
- `manage-auth-md`

### Foundation (25)

Cross-cutting portable skills:

- `analyze-business-requirements`
- `analyze-campaign-roi`
- `analyze-data`
- `accessibility-review`
- `ai-risk-assessment`
- `commit-code`
- `conduct-research`
- `create-migration`
- `design-review`
- `design-ux-flow`
- `generate-mmo-content`
- `incident-report`
- `meeting-review`
- `navigate-service`
- `optimize-seo`
- `performance-profiling`
- `plan-technical-delivery`
- `release-notes`
- `repurpose-content`
- `review-code`
- `review-service`
- `troubleshoot-service`
- `write-article`
- `write-product-brief`
- `write-tests`

### Backend (4)

- `add-api-endpoint`
- `add-event-handler`
- `add-service-client`
- `scaffold-new-service`

### Frontend (8)

- `add-ui-component`
- `add-page-route`
- `debug-3d-scene`
- `frontend-testing`
- `integrate-api-client`
- `integrate-r3f-three-legacy`
- `optimize-3d-assets`
- `setup-design-system`

> Note: `create-automation-script` is classified under Platform (stealth/CDP automation is infrastructure-level).

### Platform (17)

Delivery, runtime, Cloudflare-specific, cloud, system infrastructure, and MMO automation skills:

- `aws-infrastructure`
- `setup-deployment`
- `supply-chain-security`
- `system-design`
- `wrangler`
- `debug-workers-edge`
- `debug-runtime-platform`
- `add-telemetry-instrumentation`
- `cloudflare-email-service`
- `create-automation-script`
- `durable-objects`
- `deploy-mmo-infrastructure`
- `deploy-proxyware-fleet`
- `sandbox-sdk`
- `turnstile-spin`
- `web-perf`
- `workers-best-practices`

### Commerce (4)

E-commerce catalog, checkout, payment, and fulfillment:

- `integrate-payment-gateway`
- `handle-checkout-flow`
- `manage-product-catalog`
- `manage-order-fulfillment`

### Security And Data (6)

- `manage-secrets`
- `database-maintenance`
- `manage-mmo-assets`
- `security-audit`
- `build-data-pipeline`
- `setup-tracking-system`

### Documentation (3)

- `configure-llms-txt`
- `write-documentation`
- `write-tech-radar`

### Education (3)

Teaching and curriculum:

- `design-learning-plan`
- `create-exercises`
- `grade-and-review`

Overlay-specific skills (site stacks, ICM, content data) live under `overlays/*/skills/` and are validated together with core.

## Skill Boundaries (quick reference)

| Topic | Primary skill | Escalate to |
| ----- | ------------- | ----------- |
| Deep discovery | `conduct-research` | Researcher role |
| Ad-hoc analysis / dashboards | `analyze-data` | Data Analyst role |
| Pipelines / ETL / warehouse | `build-data-pipeline` | Data Engineer role; analysis-only → `analyze-data` |
| UX flows and specs | `design-ux-flow` | UI/UX Designer |
| Visual / IA critique (no code) | `design-review` | UI/UX or Reviewer |
| a11y conformance | `accessibility-review` | QA + Frontend |
| Generic CI/CD deploy | `setup-deployment` | DevOps Engineer |
| System topology & capacity | `system-design` | System Engineer |
| Cloudflare Workers/Pages | `wrangler` | Cloudflare Engineer |
| MCP server configuration | `configure-mcp` | Cloudflare Engineer |
| Agentic commerce flows | `configure-agent-commerce` | Backend Developer |
| Agent-ready web discovery | `configure-agent-headers` + `manage-api-catalog` | Agent Discovery Engineer |

## Backlog (not yet skills)

### Priority 2

- `3d-material-pipeline` (not yet created)
- `product-discovery` (not yet created)

### Priority 3

- `frontend-state-management` (not yet created)

## Naming Rules

- prefer generic names over stack-specific names
- categorize skills under their respective taxonomy folders (agent, foundation, backend, frontend, platform, security-data, documentation, education)
- move stack-specific or org-specific variants into overlays when they are not portable

## Skill Authoring Standard

Every `SKILL.md` should use this baseline structure unless a skill has a clear reason to be shorter:

1. YAML frontmatter with `name` and `description`.
2. H1 title matching the skill name in title case.
3. One short "Use this skill..." paragraph.
4. `## Core Rules` for non-negotiable constraints.
5. `## Suggested Process` for the normal execution path.
6. `## Checklist` for completion checks.
7. `## Related Skills` with one-line descriptions.

Optional sections such as `## Output Format`, `## When to Use`, `## Deliverable Decision`, or domain-specific guidance are fine when they improve execution.

Descriptions should include both what the skill does and when to use it. Keep skills repo-agnostic by default; put stack-specific assumptions in adapters or overlays.

## Validation Gate

Run this before treating core skill changes as complete:

```bash
python3 core/scripts/validate-skills.py
```

The validator checks:

- every skill has valid `name` and `description` frontmatter
- descriptions include both capability and trigger language
- skill names match directory names
- every skill has the baseline sections
- checklists contain enough actionable completion checks
- related skill references point to existing skills
- role and workflow skill references resolve

Skill changes are not done until this check passes.
