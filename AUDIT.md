# Agent-Skills Upgrade Audit (Core Skills)

**Scope:** 97 portable core skills under `core/skills/*/*/SKILL.md` (agent-skills pack v4.0.1)
**Baseline:** `validate-skills.py` currently passes for all 107 skills (97 core + 10 overlay).
**Goal of this audit:** identify gaps in depth and 2026 standardization before applying upgrades.
**Standard chosen by user:** *Standard 2026* — frontmatter, baseline sections, Output Contracts (where applicable), OWASP ASI guardrails, Failure Modes.

---

## Inventory Snapshot

| Metric | Value |
| --- | --- |
| Total core skills audited | 97 |
| Currently passing `validate-skills.py` | 97 (100%) |
| Skills with all baseline fields filled | 97 |
| Skills > 200 lines (oversize risk, threshold 500) | 7 |
| Skills with checklist < 8 items | 19 |
| Skills with Related Skills < 4 | 22 |
| Skills lacking OWASP ASI mention | 87 |
| Skills lacking Output Contracts section | 47 |
| Skills lacking any Failure Modes coverage | 62 |

---

## Priority Tiers

### Tier 1 — HIGH PRIORITY (63 skills)
Multiple gaps (OWASP, contracts, failure modes, oversize, or thin checklist). These are where upgrades yield the largest lift.

#### Agent (15)
- agent/agent-graph-orchestration — `NO_OWASP,NO_FAILURE`
- agent/agent-handoff — `CHECKLIST<8,NO_OWASP,NO_CONTRACTS`
- agent/agent-memory-compaction — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- agent/agent-panel-meeting — `CHECKLIST<8,NO_OWASP,NO_FAILURE`
- agent/agent-semantic-memory — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- agent/agent-tool-orchestration — `OVERSIZE>200,NO_CONTRACTS`
- agent/configure-agent-commerce — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- agent/configure-agent-headers — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- agent/configure-agent-skills — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- agent/configure-mcp — `RELATED<4,NO_OWASP,NO_CONTRACTS`
- agent/configure-oauth-metadata — `RELATED<4,NO_OWASP,NO_CONTRACTS`
- agent/debug-identity-provider — `RELATED<4,NO_OWASP,NO_CONTRACTS`
- agent/manage-agent-identity — `NO_CONTRACTS,NO_FAILURE`
- agent/manage-api-catalog — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- agent/manage-auth-md — `RELATED<4,NO_OWASP,NO_CONTRACTS`

#### Backend (1)
- backend/add-service-client — `NO_OWASP,NO_FAILURE`

#### Commerce (1)
- commerce/manage-product-catalog — `CHECKLIST<8,NO_OWASP,NO_CONTRACTS`

#### Content (4)
- content/audit-content — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- content/optimize-seo — `OVERSIZE>200,NO_OWASP,NO_FAILURE`
- content/repurpose-content — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- content/write-article — `OVERSIZE>200,NO_OWASP,NO_FAILURE`

#### Documentation (2)
- documentation/write-documentation — `NO_OWASP,NO_FAILURE`
- documentation/write-tech-radar — `NO_OWASP,NO_FAILURE`

#### Education (3)
- education/create-exercises — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- education/design-learning-plan — `RELATED<4,NO_OWASP,NO_FAILURE`
- education/grade-and-review — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`

#### Foundation (8)
- foundation/conduct-research — `OVERSIZE>200,NO_OWASP,NO_FAILURE`
- foundation/create-migration — `OVERSIZE>200,NO_OWASP`
- foundation/design-review — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- foundation/performance-profiling — `OVERSIZE>200,CHECKLIST<8,NO_OWASP,NO_FAILURE`
- foundation/plan-technical-delivery — `NO_OWASP,NO_FAILURE`
- foundation/release-notes — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- foundation/write-product-brief — `CHECKLIST<8,NO_OWASP,NO_FAILURE`
- foundation/write-tests — `OVERSIZE>200,CHECKLIST<8,NO_OWASP`

#### Frontend (3)
- frontend/add-ui-component — `NO_OWASP,NO_FAILURE`
- frontend/implement-webmcp — `CHECKLIST<8,NO_OWASP,NO_FAILURE`
- frontend/setup-design-system — `NO_OWASP,NO_FAILURE`

#### Meetings-Analysis (2)
- meetings-analysis/analyze-data — `CHECKLIST<8,NO_OWASP,NO_FAILURE`
- meetings-analysis/meeting-review — `OVERSIZE>200,NO_OWASP,NO_CONTRACTS`

#### MMO (6)
- mmo/analyze-campaign-roi — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- mmo/deploy-mmo-infrastructure — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- mmo/deploy-proxyware-fleet — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- mmo/generate-mmo-content — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- mmo/manage-mmo-assets — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- mmo/setup-tracking-system — `RELATED<4,NO_OWASP,NO_CONTRACTS,NO_FAILURE`

#### Platform (12)
- platform/aws-infrastructure — `CHECKLIST<8,NO_OWASP,NO_FAILURE`
- platform/cloudflare-email-service — `CHECKLIST<8,RELATED<4,NO_OWASP`
- platform/debug-workers-edge — `CHECKLIST<8,RELATED<4,NO_OWASP`
- platform/durable-objects — `OVERSIZE>200,RELATED<4,NO_OWASP,NO_FAILURE`
- platform/sandbox-sdk — `CHECKLIST<8,RELATED<4,NO_OWASP,NO_FAILURE`
- platform/setup-gpu-finops — `CHECKLIST<8,NO_OWASP,NO_FAILURE`
- platform/setup-llm-gateway — `NO_OWASP,NO_FAILURE`
- platform/system-design — `NO_OWASP,NO_FAILURE`
- platform/turnstile-spin — `OVERSIZE>200,RELATED<4,NO_OWASP`
- platform/web-perf — `RELATED<4,NO_OWASP,NO_FAILURE`
- platform/workers-best-practices — `RELATED<4,NO_OWASP,NO_FAILURE`
- platform/wrangler — `CHECKLIST<8,RELATED<4,NO_OWASP`

#### Repo-Ops (4)
- repo-ops/commit-code — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- repo-ops/navigate-service — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- repo-ops/review-code — `NO_OWASP,NO_FAILURE`
- repo-ops/troubleshoot-service — `OVERSIZE>200,NO_OWASP,NO_CONTRACTS`

#### Security-Data (2)
- security-data/manage-secrets — `NO_OWASP,NO_CONTRACTS,NO_FAILURE`
- security-data/manage-vietnam-accounting — `NO_OWASP,NO_FAILURE`

---

### Tier 2 — MEDIUM (31 skills)
Single gap or minor incompleteness. Polish pass.

agent/agent-a2a-protocol, agent/agent-context-management, agent/agent-model-routing, agent/agent-observability, agent/agent-prompt-lifecycle, backend/add-api-endpoint, backend/add-event-handler, backend/build-mcp-server, backend/implement-structured-outputs, backend/scaffold-new-service, commerce/handle-checkout-flow, commerce/integrate-payment-gateway, commerce/manage-order-fulfillment, documentation/configure-llms-txt, foundation/accessibility-review, foundation/design-ux-flow, foundation/incident-report, frontend/add-page-route, frontend/frontend-testing, frontend/integrate-api-client, frontend/setup-visual-regression, meetings-analysis/analyze-business-requirements, mmo/create-automation-script, platform/add-telemetry-instrumentation, platform/debug-runtime-platform, platform/setup-deployment, platform/supply-chain-security, repo-ops/review-service, security-data/build-data-pipeline, security-data/database-maintenance, security-data/security-audit

---

### Tier 3 — OK (3 skills)
Already at Standard 2026 level — leave as reference templates.

- agent/agent-delegation — 150 lines, checklist 16, OWASP + contracts + failure
- agent/agent-quality-gate — 147 lines, checklist 8, OWASP + contracts + failure
- foundation/ai-risk-assessment — 189 lines, checklist 11, OWASP + contracts + failure

---

## Upgrade Template

For each Tier 1/2 skill, the upgrade will add or strengthen the following where missing or thin:

1. **YAML frontmatter** — already present; verify `Use when`/`Use for` trigger phrase.
2. **H1 title** — verified for all 97.
3. **`## Core Rules`** — already required; add OWASP ASI guardrails line where skill touches tools, agents, identity, or memory.
4. **`## Suggested Process`** — already present; expand with concrete Failure-Mode sub-bullets where missing.
5. **`## Checklist`** — verify ≥ 8 actionable `- [ ]` items (currently 19 skills below threshold).
6. **`## Related Skills`** — verify ≥ 4 items pointing to existing skills (currently 22 skills below).
7. **`## Output Contracts`** — add when the skill emits structured artifacts (A2A tasks, schemas, configs).
8. **`## Failure Modes`** *(new, recommended)* — short section naming 3-5 most-likely failure paths and mitigations. Will be optional and validator-not-enforced.
9. **`## Security Guardrails`** *(where applicable)* — short pointer to OWASP ASI items the skill must apply.
10. **Size guard** — extract deep content into `references/` if SKILL.md > 200 lines.

### Hard rules
- Never break `validate-skills.py` (frontmatter, H1 match, baseline sections, checklist ≥ 5, related format, no reserved words, no XML).
- Never change skill `name` (it is the agentskills.io identifier).
- Never add per-skill versions — pack `VERSION` governs.
- Keep content repo-agnostic; move stack-specific details into existing references/ or overlays.
- Do not edit overlay skills in this pass (out of scope of this audit unless user expands scope).

---

## Proposed Execution Order (after user approval)

| Batch | Category | Count | Estimated edits |
| --- | --- | --- | --- |
| 1 | agent/* (Tier 1) | 15 | large, since most are flagship agent skills |
| 2 | foundation/* (Tier 1) | 8 | medium; extract references where oversize |
| 3 | platform/* (Tier 1) | 12 | medium |
| 4 | content + commerce + security-data + repo-ops (Tier 1) | 13 | small |
| 5 | mmo + documentation + education + meetings-analysis + frontend + backend (Tier 1) | 15 | small |
| 6 | All Tier 2 polish | 31 | small (single-section adds) |

After each batch: re-run `validate-skills.py`. After all batches: re-run `validate-all.py`.

---

## Out of Scope (this audit only — flag if user wants)

- Overlay skills (`overlays/*/skills/`) — 10 files, validated together but separate from the core 97.
- Role files (`core/roles/*.md`) — 34 files; user asked specifically about **skills**, not roles.
- Workflows (`core/workflows/*.md`) — separate validator (`validate-workflows.py`).
- Contracts / schemas (`core/contracts/`) — owned by `validate-contracts.py`.
- INDEX.md count regeneration — handled by `generate-index.py` if VERSION or counts change.

---

## Questions for User Before Apply

1. **Tier scope:** apply upgrades to all Tier 1 (63) only, or include Tier 2 (31) and Tier 3 (3 = reference, no edits)?
2. **New sections:** OK to add `## Failure Modes` (3-5 bullets) and `## Security Guardrails` (when relevant) as new standard sections? Validator will not break (they are extras), but they do grow the file.
3. **Oversize files:** the 7 skills > 200 lines (agent-tool-orchestration, content/optimize-seo, content/write-article, foundation/conduct-research, foundation/create-migration, foundation/performance-profiling, foundation/write-tests, meetings-analysis/meeting-review, platform/durable-objects, platform/turnstile-spin, repo-ops/troubleshoot-service) — extract sub-topics into `references/<topic>.md` or keep inline? Note: validator hard cap is 500 lines, so we are well under.
4. **MMO cluster:** these 7 skills carry Legal & Compliance Notices. Upgrades will not modify those notices; OWASP additions will respect the existing REVIEW-SYSTEM LOCK.
5. **Commit/push policy:** per `core/rules/code.md` META-RULE — do NOT commit unless user confirms in-session. Default will be: edits applied, `validate-skills.py` re-run, no commit.

---

*Awaiting user direction before applying changes.*