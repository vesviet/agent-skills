# Skills Inventory

This directory contains the **portable core** skill inventory for the global engineering pack.

**Counts:** 57 core skills under `core/skills/` + overlay skills under `overlays/*/skills/` (run `validate-skills.py` for the live total).

## Taxonomy

### Agent (12)

Agent operating discipline and orchestration:

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

### Foundation (19)

Cross-cutting portable skills:

- `analyze-business-requirements`
- `analyze-data`
- `accessibility-review`
- `commit-code`
- `conduct-research`
- `create-migration`
- `design-review`
- `design-ux-flow`
- `meeting-review`
- `navigate-service`
- `optimize-seo`
- `performance-profiling`
- `plan-technical-delivery`
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

### Frontend (7)

- `add-ui-component`
- `add-page-route`
- `debug-3d-scene`
- `frontend-testing`
- `integrate-api-client`
- `integrate-r3f-three-legacy`
- `optimize-3d-assets`

### Platform (6)

Delivery and runtime:

- `setup-deployment`
- `manage-wrangler-deploy`
- `configure-cloudflare-bindings`
- `debug-workers-edge`
- `debug-runtime-platform`
- `add-telemetry-instrumentation`

### Security And Data (4)

- `manage-secrets`
- `database-maintenance`
- `security-audit`
- `data-engineer`

### Documentation (2)

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
| Pipelines / ETL / warehouse | `data-engineer` | Data Engineer role; analysis-only → `analyze-data` |
| UX flows and specs | `design-ux-flow` | UI/UX Designer |
| Visual / IA critique (no code) | `design-review` | UI/UX or Reviewer |
| a11y conformance | `accessibility-review` | QA + Frontend |
| Generic CI/CD deploy | `setup-deployment` | DevOps Engineer |
| Cloudflare Workers/Pages | `manage-wrangler-deploy` | Cloudflare Engineer |

## Backlog (not yet skills)

### Priority 2

- `3d-material-pipeline`
- `incident-report`
- `release-notes`
- `product-discovery`

### Priority 3

- `frontend-state-management`

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
