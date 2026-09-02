# Remaining Upgrade Audit (post-4.1.0 sweep)

**Scope:** every directory in the pack, after the 4.1.0 upgrade pass.
**Baseline:** `validate-all.py` passes 16/16 validators, 0 errors, 0 warnings.
**Goal:** identify the remaining gaps and decide whether they need an upgrade.

## 1. Recap — what is already at Standard 2026 (4.1.0)

| Area | Files | FM | OC | SG | 2026 footer |
|---|---:|---:|---:|---:|---:|
| `core/skills/` (97) | 65 | yes | yes | yes | (skill-internal) |
| `core/skills/` (32 Tier 2) | 32 | **NO** | yes | yes | (skill-internal) |
| `overlays/*/skills/` (10) | 10 | yes | yes | yes | (skill-internal) |
| `core/roles/` (34) | 34 | yes | (implicit via contract refs) | yes | (role-internal) |
| `core/policies/` (3 + README) | 4 | (YAML, prose) | n/a | n/a | (n/a) |
| `core/workflows/` (18) | 10 T1 + 8 T2/3 | yes | yes | T1 only | (workflow-internal) |
| `overlays/*/workflows/` (6) | 6 | yes | yes | (n/a) | (workflow-internal) |
| `overlays/*/rules/` (25) | 25 | (footer) | (footer) | (footer) | yes |
| Overlay READMEs (22 substantive) | 22 | n/a | n/a | n/a | yes |
| Root docs (6) | 6 | (header) | (header) | (header) | yes |
| Editor boilerplate (4) | 4 | (footer) | (footer) | (footer) | yes |
| `adapters/{antigravity,claude,cursor}` (3) | 3 | yes | yes | yes | (Tier A) |
| `core/adapter-parity.md` | 1 | yes | (n/a) | yes | (Tier A) |
| `packs/README.md` | 1 | yes | yes | yes | (Tier A) |

## 2. Remaining gaps (3 categories)

### 2.1 Tier 2 skills lacking `## Failure Modes` (32 skills)

These are the skills I upgraded in the original Tier 2 pass (per your plan: "T2 = 4-5 items Failure Modes"). The Tier 2 plan was: Failure Modes + Output Contracts (no Security Guardrails). But I only added Output Contracts + Security Guardrails, not Failure Modes. The 32 skills are:

- **agent/**: agent-a2a-protocol, agent-delegation, agent-model-routing, agent-observability, agent-prompt-lifecycle, agent-quality-gate
- **backend/**: add-api-endpoint, add-event-handler, build-mcp-server, implement-structured-outputs, scaffold-new-service
- **commerce/**: handle-checkout-flow, integrate-payment-gateway, manage-order-fulfillment
- **documentation/**: configure-llms-txt
- **foundation/**: accessibility-review, ai-risk-assessment, design-ux-flow, incident-report
- **frontend/**: add-page-route, add-ui-component, frontend-testing, integrate-api-client, setup-visual-regression
- **meetings-analysis/**: analyze-business-requirements
- **platform/**: add-telemetry-instrumentation, debug-runtime-platform, sandbox-sdk, setup-deployment
- **repo-ops/**: review-service
- **security-data/**: build-data-pipeline, database-maintenance

**Action:** add 4-5 `## Failure Modes` items to each (per original Tier 2 plan).

### 2.2 Core workflows lacking `### Security Guardrails (OWASP ASI)` (8 workflows)

By your original plan, only Tier 1 (10 workflows) gets Security Guardrails. The remaining 8 (Tier 2 + Tier 3) lack it:

- add-new-feature, content-audit, content-publishing, qa-validation, refactoring, seo-content-lifecycle, seo-keyword-brief, setup-new-service

**Action:** optional — add 3-4 `### Security Guardrails` items if you want consistency, or leave as-is per the original plan.

### 2.3 `core/*` READMEs lacking Standard 2026 footer (14 files)

These are root-area READMEs and one rule file (`.cursorrules` is a Cursor adapter mirror):

- `core/README.md` (26 lines) — top-level core index
- `core/rules/code.md` (23 lines) — the always-on rule file (intentionally terse)
- `core/observability/otel-genai.md` (206 lines) — comprehensive OTel guide
- `core/observability/README.md` (20 lines)
- `core/prompts/README.md` (36 lines)
- `core/a2a/README.md` (60 lines)
- `core/codex/README.md` (37 lines)
- `core/config/README.md` (5 lines)
- `core/contracts/README.md` (116 lines)
- `core/roles/README.md` (281 lines)
- `core/skills/README.md` (268 lines)
- `core/workflows/README.md` (113 lines)
- `core/policies/README.md` (79 lines)
- `.cursorrules` (77 lines)

**Action:** add the Standard 2026 footer to all 14 (or skip — the footers are mostly index files where a footer is decorative).

## 3. Per-tier recommendation

### Tier 1 (recommended): Add Failure Modes to the 32 Tier 2 skills

This is the only substantive content gap. 32 skills × 4 items = 128 new failure scenarios. Same pattern as the original Tier 2 plan, just delayed. This brings all 97 core skills to 100% FM coverage.

### Tier 2 (optional): Add Security Guardrails to 8 core workflows

Brings the 18 core workflows to 100% SG coverage. But this deviates from the original plan (T2/3 explicitly excluded SG).

### Tier 3 (optional): Add Standard 2026 footer to 14 `core/*` READMEs and `.cursorrules`

Pure decoration. The READMEs are indexes and `.cursorrules` is a rule mirror — none of them produce artifacts, so the failure-mode / output-contract / security-guardrail pattern does not apply. A footer would be cosmetic.

## 4. Already at 2026 standard — no action

- `core/rules/code.md` content (it's the META-RULE; terse by design, footer would be noise)
- `core/observability/otel-genai.md` (comprehensive 2026 content; footer would be noise)
- `core/codex/README.md`, `core/config/README.md` (5-line stubs)
- `packs/README.md` (already Tier A)
- All 13 pack manifests (`packs/*/manifest.yaml`)

## 5. Out of scope

- Generator scripts (`generate-*.py`, `validate-*.py`) — code, not prose
- 3-line stub READMEs (`overlays/*/rules/README.md`, `overlays/*/config/README.md`, etc.) — empty placeholders
- Generated artifacts (`INDEX.md`, `role-skill-index.json`, `*.agent-card.json`) — already 4.1.0 consistent

## 6. Questions for User Before Apply

1. **Tier 1:** add Failure Modes to the 32 Tier 2 skills (apply original plan now)?
2. **Tier 2:** add Security Guardrails to the 8 core workflows (T2/3 of workflows)?
3. **Tier 3:** add Standard 2026 footer to the 14 `core/*` READMEs + `.cursorrules`?
4. **Commit policy:** per `core/rules/code.md` META-RULE, no commit unless you confirm. Default: edits applied, validators re-run, no commit.

---

*Awaiting user direction before applying changes.*
