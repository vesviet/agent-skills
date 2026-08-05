# Skills Inventory

This directory contains the **portable core** skill inventory for the global engineering pack.

**Counts:** 94 portable core skills under `core/skills/` + 7 overlay skills under `overlays/*/skills/` = **101 total** (run `validate-skills.py` for the live total, and `validate-indexes.py` to confirm this line matches disk).

## Taxonomy

### Agent (22)

Agent operating discipline, orchestration, and agentic web standards:

- `agent-a2a-protocol`
- `agent-context-management`
- `agent-delegation`
- `agent-graph-orchestration`
- `agent-handoff`
- `agent-memory-compaction`
- `agent-model-routing`
- `agent-observability`
- `agent-panel-meeting`
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

### Foundation (26)

Cross-cutting portable skills:

- `analyze-business-requirements`
- `analyze-campaign-roi`
- `analyze-data`
- `accessibility-review`
- `audit-content`
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

### Security And Data (7)

- `manage-secrets`
- `database-maintenance`
- `manage-mmo-assets`
- `manage-vietnam-accounting`
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
| Vietnam accounting controls, reconciliations, or close evidence | `manage-vietnam-accounting` | Vietnam Accounting Specialist; tax position/legal interpretation -> qualified human reviewer |
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

### References Subdirectory Policy

A skill may add a `references/` subdirectory when the SKILL.md body alone would exceed ~150 lines. Use `references/` for:

- long external-spec excerpts (e.g., `agent-a2a-protocol/references/a2a-spec.md`)
- framework or stack variant guides (e.g., `turnstile-spin/references/{astro,hugo,nextjs-app,nextjs-pages,sveltekit,vanilla-html}.md`)
- deep rules/checklists that the SKILL.md body summarizes (e.g., `durable-objects/references/{rules,testing,workers}.md`)

When you add a `references/` subdirectory:

- keep SKILL.md focused on the trigger conditions, core rules, suggested process, and checklist
- link from SKILL.md to each reference doc by relative path the first time the topic appears (e.g., `See references/rules.md for the full checklist`)
- do not duplicate content between SKILL.md and `references/`
- references are loaded on demand — do not rely on them being read for the skill to start

The validator does not check `references/` content; the structural contract only applies to the SKILL.md file itself.

### Size Guidance

- Aim for SKILL.md between 80 and 200 lines.
- Below ~70 lines is acceptable for tight, scope-narrow skills (e.g., compliance-locked MMO skills) provided all baseline sections are present.
- Above ~200 lines signals a candidate for `references/` extraction; above 500 lines is rejected by the validator.

### Domain Cluster Notes (2026)

- The **MMO cluster** spans multiple taxonomies by design (foundation for content/ROI, platform for infra/automation, security-data for assets/tracking). Their pre-2025.4 drift has been retired; current skills carry Legal & Compliance Notices that map to `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role.
- The **R3F/3D cluster** under `frontend/` is retained for backward compatibility with existing role toolboxes but is scheduled for migration to an overlay at the next major version (4.0.0). New 3D work should target the overlay boundary.

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
