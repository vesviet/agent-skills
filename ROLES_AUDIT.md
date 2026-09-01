# Roles Upgrade Audit (`core/roles`)

**Scope:** 34 role files under `core/roles/*.md` (+ `role-standard.md` + `README.md`)
**Baseline:** `validate-roles.py` currently passes for all 34 roles (0 errors).
**Goal of this audit:** identify gaps in role depth, 2026 standardization, and operational usability before applying upgrades.
**Standard chosen for upgrades:** *2026 Standardization* — preserve every existing mandatory section, add the optional `## Failure Modes` section everywhere (matches what we just did for skills), add a `## Related Skills` cross-link block where missing, and ensure `## Definition Of Done` is explicitly aligned with `role-standard.md` 2026 standards.

---

## 1. Inventory Snapshot

| Metric | Value |
| --- | --- |
| Total role files audited | 34 |
| Currently passing `validate-roles.py` | 34 (100%) |
| Roles with all 17 mandatory sections (per `role-standard.md`) | 34 |
| Roles with the exact `## Collaboration` header (vs. `## Collaboration & ...`) | 33 (agent-coordinator uses `## Collaboration & A2A Delegation`) |
| Roles with `Mission:` + `Level:` lines | 34 |
| Roles with the role-standard reference line | 34 |
| Roles with `Last updated: YYYY-MM-DD` footer | 34 |
| Roles with `## Outputs Produced` referencing ≥ 1 contract | 34 |
| Roles referencing contracts that don't exist in `core/contracts/schemas/` | 0 (43 contracts exist, 36 referenced) |
| Roles mentioning OWASP ASI / ASI01–ASI10 | 34 |
| Roles mentioning `action-boundaries.yaml` / `irreversible` policy | 34 |
| Roles with `## Failure Modes` section | **0** |
| Roles with `## Anti-Patterns To Reject` (correct header) | 34 |
| Roles with `## Review Checklist` | 34 |
| Roles with `## Role Boundaries` (table) | 34 |
| Roles with `## Optional Overlays` (last trailing element before footer) | varies (only roles that need overlays) |
| Roles with 0 Primary skills | 0 |
| Roles with overlap Primary × Supporting skills | 0 |
| Roles referencing a missing skill (in core/ or overlays/) | 0 (3d-graphics-engineer Primary skills live in `overlays/r3f-stack/skills/` — valid because overlays are checked) |
| Average role file size | 373 lines |
| Smallest role file | mmo-engineer (205 lines) |
| Largest role file | frontend-developer (621 lines) |

**Bottom line:** every role already passes the validator. The "gaps" the audit finds are **enhancement opportunities**, not validator failures.

---

## 2. Why upgrade if it already passes?

Three reasons:

1. **The skills we just upgraded all added `## Failure Modes`.** Roles should match: a 2026 reader skimming a role file should see the same 5-section mental model they just saw in the skill files (Mission, Failure Modes, Output Contracts, Definition of Done, etc.).
2. **`role-standard.md` is descriptive, not prescriptive on Failure Modes.** The standard asks roles to "think in failure modes" but does not require a `## Failure Modes` section. Adding it is a low-risk consistency win.
3. **Universal 2026 standards (OWASP ASI, irreversible actions, NHI) are referenced but not always indexed.** Some roles mention ASI01–ASI10 in Guardrails but do not give the reader a quick-reference table of which ASI items this role most commonly encounters.

---

## 3. Priority Tiers

### Tier 1 — HIGH PRIORITY (12 roles)
Roles whose Mission, Principal Expectations, or Domain already have a heavy "2026" extension section (AI, agentic, irreversible, OWASP) but are missing the matching `## Failure Modes` companion section. Adding Failure Modes here makes the 2026 content navigable.

| Role | Lines | Why T1 |
| --- | ---: | --- |
| technical-lead | 453 | Delivery / AI risk / debt; needs Failure Modes for delivery & rollback |
| technical-architect | 486 | ADR / architecture; needs Failure Modes for architecture drift |
| solution-architect | 464 | Solution-brief / build-vs-buy; needs Failure Modes for vendor lock-in |
| system-engineer | 454 | Capacity / IaC; needs Failure Modes for capacity model drift |
| backend-developer | 511 | Code risk; needs Failure Modes for backend service outages |
| frontend-developer | 621 | Component / a11y; needs Failure Modes for visual regression break |
| qa-engineer | 512 | Test gap; needs Failure Modes for test coverage false positives |
| security-engineer | 327 | OWASP / secrets; needs Failure Modes for security audit gaps |
| sre | 231 | SLO / on-call; needs Failure Modes for incident response blind spots |
| data-engineer | 274 | Pipeline / lineage; needs Failure Modes for silent data corruption |
| data-analyst | 323 | Metric / causal; needs Failure Modes for correlation-as-causation |
| researcher | 362 | CoVe / grounding; needs Failure Modes for hallucinated citations |

### Tier 2 — MEDIUM (16 roles)
Roles that touch AI-assisted work or external contracts but are less AI-heavy. Adding Failure Modes improves navigation but is not critical.

| Role | Lines | Why T2 |
| --- | ---: | --- |
| agent-coordinator | 441 | Already has Collaboration & A2A Delegation; Failure Modes for orchestration deadlock |
| agent-discovery-engineer | 219 | Discovery + registry; Failure Modes for stale registry drift |
| 3d-graphics-engineer | 277 | R3F / Three; Failure Modes for render regression |
| ai-systems-engineer | 243 | LLM deployment; Failure Modes for eval regression |
| aws-engineer | 366 | IaC; Failure Modes for IAM drift |
| cloudflare-engineer | 286 | Edge deploy; Failure Modes for regional failure |
| content-manager | 512 | Editorial workflow; Failure Modes for stale content drift |
| content-writer | 449 | Article quality; Failure Modes for unverified claims |
| devops-engineer | 434 | CI/CD; Failure Modes for pipeline regression |
| ecommerce-engineer | 258 | Checkout; Failure Modes for payment failure |
| mobile-engineer | 401 | Mobile release; Failure Modes for app store rejection |
| product-manager | 357 | Roadmap; Failure Modes for scope creep |
| project-manager | 260 | Schedule; Failure Modes for dependency slip |
| reviewer | 297 | Review rigor; Failure Modes for rubber-stamp review |
| seo-analyst | 409 | AI search; Failure Modes for citation drift |
| task-planner | 253 | Sprint scope; Failure Modes for hidden dependency |

### Tier 3 — LOW (6 roles)
Roles that are domain-specialized and less AI-impacted. Minimal but consistent Failure Modes addition.

| Role | Lines | Why T3 |
| --- | ---: | --- |
| business-analyst | 614 | Already huge; Failure Modes for requirement drift |
| technical-writer | 348 | Docs; Failure Modes for doc drift |
| ui-ux-designer | 468 | UX flow; Failure Modes for accessibility regression |
| teacher | 274 | Curriculum; Failure Modes for assessment drift |
| vietnam-accounting-specialist | 292 | Already has Vietnam regulatory guardrails; Failure Modes for compliance lapse |
| mmo-engineer | 205 | Already has Legal & Compliance Notices; Failure Modes for compliance gap |

---

## 4. Upgrade Template

For every Tier 1/2/3 role, the upgrade will:

1. **Add `## Failure Modes`** — 4-6 named failure paths with mitigations, inserted just before `## Anti-Patterns To Reject`. Each entry names a concrete failure pattern (not a generic category) and a concrete mitigation that the role can actually do.
2. **No new mandatory sections** — `## Failure Modes` is optional in the standard, but adopted as the pack's 2026 norm to mirror the skills.
3. **No structural rewrites** — keep all 17 mandatory sections intact and in the same order. No H1, Mission, or Level changes.
4. **No contract path rewrites** — keep `contracts/schemas/<name>.json` (logical) convention.
5. **No footer changes** — preserve `Last updated: YYYY-MM-DD` as the last non-empty line.
6. **No file rename or H1 change** — every validator check passes only if filename matches H1 slug.
7. **No removal of existing 2026 / OWASP content** — only add.
8. **Respect optional overlays** — do not duplicate overlay content into core roles.

### Standard Failure Modes block (adapt per role)

```markdown
## Failure Modes

- **<pattern>**: <concrete failure scenario>. **Mitigation:** <what this role does to detect/prevent/recover>.
- **<pattern>**: <...>
- ...
```

Each entry must be **role-specific** (not generic), cite the role's declared **tools/skills** when relevant, and connect to a **Definition of Done** or **Output Contract** line when applicable.

---

## 5. Out of Scope (this audit only — flag if user wants)

- `role-standard.md` — already at 2026 standard with OWASP ASI section. No changes proposed.
- `core/roles/README.md` — index file. Only needs a count update if role numbers change (they won't).
- New roles — the audit is for upgrades, not additions.
- Role responsibilities / Decision Boundaries rewrites — too invasive for a polish pass; the user can request separately.
- H1 / Mission / Level rewrites — out of scope; the validator enforces them.
- Contract schema changes — out of scope; the audit is about role files.
- Overlay roles (`overlays/*/roles/*.md`) — separate from core; not in this pass.

---

## 6. Execution Order (after user approval)

| Batch | Tier | Count | Approach |
| --- | --- | ---: | --- |
| 1 | Tier 1 | 12 | Read each role's existing 2026 content; draft role-specific Failure Modes; insert before `## Anti-Patterns To Reject` |
| 2 | Tier 2 | 16 | Same approach; slightly shorter entries (4 items vs 6) |
| 3 | Tier 3 | 6 | Same approach; minimum 4 items |

After each batch: re-run `validate-roles.py` and `validate-all.py` to confirm 0 errors and 0 warnings.

---

## 7. Questions for User Before Apply

1. **Tier scope:** apply upgrades to all 34 roles, or just Tier 1 (12) first?
2. **Failure Modes depth:** 4-6 items per role (T1 = 6, T2 = 5, T3 = 4) acceptable, or do you want a fixed minimum (e.g., exactly 4 per role)?
3. **New optional section:** OK to add `## Failure Modes` as the de-facto 2026 standard even though `role-standard.md` lists it as optional?
4. **3d-graphics-engineer overlay skills:** those 3 Primary skills live in `overlays/r3f-stack/skills/`. The validator passes today; confirm we should not move them into core.
5. **Commit/push policy:** per `core/rules/code.md` META-RULE — do NOT commit unless user confirms in-session. Default will be: edits applied, `validate-roles.py` + `validate-all.py` re-run, no commit.

---

*Awaiting user direction before applying changes.*
