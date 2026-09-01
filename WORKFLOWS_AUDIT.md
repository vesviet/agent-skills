# Workflows Upgrade Audit (`core/workflows`)

**Scope:** 18 workflow files + 1 README under `core/workflows/`
**Baseline:** `validate-workflows.py` currently passes for all 18 workflows (0 errors).
**Goal of this audit:** identify gaps in workflow depth, 2026 standardization, and operational usability before applying upgrades.
**Standard chosen for upgrades:** *2026 Standardization* — preserve every existing required section, add the optional `## Failure Modes` and `## Output Contracts` sections as the new pack norm, add OWASP ASI / Security Guardrails where the workflow touches security/irreversible steps, and standardize the frontmatter trigger.

---

## 1. Inventory Snapshot

| Metric | Value |
| --- | --- |
| Total workflow files audited | 18 |
| Currently passing `validate-workflows.py` | 18 (100%) |
| Workflows with all 5 required sections (`### Prerequisites`, `### Workflow Steps`, `### Checklist`, `### Related Workflows`, `### Related Skills`) | 18 |
| Workflows with exactly 1 H2 (per validator) | 18 (the 2nd H2 in `service-review-release.md` and `tech-repo-review.md` is inside a fenced template) |
| Workflows with sequential #### N. steps from 1 | 18 |
| Workflows with `Role:` line under every step | 18 |
| Workflows with checklist ≥ 5 items | 18 (min 6, max 12) |
| Workflows with `### Related Skills` ≥ 3 items | 18 (min 3, max 6) |
| Workflows with `### Related Workflows` ≥ 2 links | 18 (min 2, max 5) |
| Inline `Use skill:` references | 70 (all resolve to known skills) |
| Workflows mentioning OWASP / ASI01-ASI10 | **0** |
| Workflows with `## Failure Modes` section | **0** (some have ad-hoc "Common Failure Areas" H3 lists) |
| Workflows with `## Security Guardrails` / `## Guardrails` section | 2 (`security-incident-response.md`, `tech-repo-review.md`) |
| Workflows with `## Output Contracts` section | 0 |
| Frontmatter `Use when` / `Use for` trigger | 0 (only plain `description`) |
| Average workflow size | 166 lines |
| Smallest workflow | `seo-content-lifecycle.md` (72 lines) |
| Largest workflow | `tech-repo-review.md` (222 lines) |

**Bottom line:** every workflow already passes the validator. The "gaps" the audit finds are **enhancement opportunities** that match the 2026 standardization we just applied to skills, roles, and policies.

---

## 2. Detailed Findings

### 2.1 Pattern coverage by workflow

Each workflow has:
- YAML frontmatter with `description` (no `Use when` / `Use for` trigger)
- One H2 title ending with "Workflow"
- `### Prerequisites`
- `### Workflow Steps` with sequential `#### N.` steps
- `Role:` line on every step (uses `**Role Name**` syntax; validator maps `SRE` → "Site Reliability Engineer")
- `### Checklist` with 6-12 actionable items
- `### Related Workflows` (links to sibling workflows)
- `### Related Skills` (uses `- **skill-name**: description` items)

**Strengths**
- All 70 inline `Use skill: \`name\`` references resolve to known skills
- All `### Related Skills` items resolve
- All `### Related Workflows` links resolve
- README is in sync with disk (no missing/extra entries)
- 2 workflows already have H3 `#### <Name>` Failure Areas / Escalation Triggers (good ad-hoc but inconsistent)

**Gaps**
- **0 workflows mention OWASP ASI** — unlike roles and skills
- **0 workflows have `## Failure Modes` section** — but `troubleshooting.md`, `tech-repo-review.md`, `data-migration.md`, etc. have ad-hoc H3 failure lists under different names
- **0 workflows have `## Output Contracts` section** — workflows emit deliverables (briefs, audits, plans) but don't explicitly name the JSON contract
- **Frontmatter has only `description`** — no `Use when` / `Use for` trigger phrase (like skills)
- **`Use skill:` is text-anchored** — the validator matches `Use skill: \`name\`` literally; a workflow that says "use the `navigate-service` skill" inline would not be caught as a reference

### 2.2 Per-workflow upgrade opportunities

| Workflow | Lines | Has failure list? | Has output contract? | Has OWASP? | Notes |
| --- | ---: | --- | --- | --- | --- |
| add-new-feature | 191 | no (no failure section) | implicit feature-ticket.json | no | Tier 1 candidate |
| agent-a2a-delegation | 119 | no | implicit a2a-task.json | no | Tier 1 — A2A is security-sensitive |
| build-deploy | 185 | no | implicit implementation-result.json | no | Tier 1 — deploy is irreversible |
| content-audit | 128 | no | implicit seo-audit-report.json | no | Tier 2 |
| content-publishing | 175 | no | implicit content-handoff.json | no | Tier 2 |
| data-migration | 170 | H3 "Common Migration Patterns" + "Common Gotchas" | implicit schema-migration.json | no | Tier 1 — migration is irreversible |
| dependency-upgrade | 170 | no | implicit dependency-update artifacts | no | Tier 1 — supply chain |
| hotfix-production | 149 | no | implicit incident-report.json | no | Tier 1 — production blast radius |
| qa-validation | 209 | no | implicit test-report.json | no | Tier 2 |
| refactoring | 133 | no | implicit implementation-result.json | no | Tier 2 |
| revert-deployment | 124 | no | implicit deployment-plan.json rollback | no | Tier 1 — irreversible |
| security-incident-response | 168 | no (H3 "Escalation Triggers") | implicit incident-report.json | no | Tier 1 — has Guardrails already |
| seo-content-lifecycle | 72 | no | implicit seo-metadata.json | no | Tier 3 — small but central |
| seo-keyword-brief | 159 | no | implicit seo-content-brief.json | no | Tier 3 |
| service-review-release | 200 | no (H3 "Escalation Triggers") | implicit release-readiness | no | Tier 1 — release blast radius |
| setup-new-service | 192 | no | implicit implementation-result.json | no | Tier 2 |
| tech-repo-review | 222 | no (H3 "Escalation Triggers") | implicit security-audit.json | no | Tier 1 — repo-wide audit |
| troubleshooting | 218 | H3 "Common Failure Areas" + "Escalation Triggers" | implicit incident-report.json | no | Tier 1 — high-traffic |

### 2.3 Frontmatter consistency

- All 18 have a `description` field
- No `Use when` / `Use for` trigger phrase (skills/roles/contracts require this; workflows do not)
- No `version` or `last_updated` metadata
- No `owner_role` field (would let a coordinator route to the right role)

### 2.4 Cross-cutting gaps (no per-workflow file change)

- **Workflows don't reference policies** (`action-boundaries.yaml`, `data-classification.yaml`) — the README mentions policies, but no workflow explicitly invokes them. A workflow like `hotfix-production.md` should reference `action-boundaries.yaml` for the deploy/rollback actions.
- **No workflow references the A2A contracts** — `agent-a2a-delegation.md` is the only one that uses A2A; it should name `a2a-task.json` / `a2a-artifact.json` explicitly in an Output Contracts section.

---

## 3. Priority Tiers

### Tier 1 — HIGH PRIORITY (8 workflows)
Workflows that drive irreversible, security-sensitive, or blast-radius actions. They need explicit Failure Modes, Security Guardrails (OWASP ASI), and Output Contracts.

| # | Workflow | Why T1 |
| --- | --- | --- |
| 1 | `agent-a2a-delegation` | A2A task dispatch — security-sensitive, schema drift risk |
| 2 | `build-deploy` | Production deploy — irreversible, OWASP ASI03 (privilege abuse) |
| 3 | `data-migration` | DB migration — irreversible, already has ad-hoc failure list to convert |
| 4 | `dependency-upgrade` | Supply chain — OWASP ASI04 (supply chain attacks) |
| 5 | `hotfix-production` | Production incident — irreversible, OWASP ASI09 (human-agent trust) |
| 6 | `revert-deployment` | Production rollback — irreversible |
| 7 | `security-incident-response` | Security response — already has Guardrails; add Failure Modes + Contracts |
| 8 | `tech-repo-review` | Repo audit — touches everything; high visibility |
| 9 | `service-review-release` | Release readiness — blast-radius decisions |
| 10 | `troubleshooting` | Most-used workflow — already has Common Failure Areas; convert to standard Failure Modes |

### Tier 2 — MEDIUM (6 workflows)
Workflows that emit structured artifacts but are not security-critical. Add Output Contracts and compact Failure Modes.

| # | Workflow | Why T2 |
| --- | --- | --- |
| 11 | `add-new-feature` | Most-used delivery workflow — full Failure Modes |
| 12 | `content-audit` | Editorial workflow — Output Contracts |
| 13 | `content-publishing` | Editorial workflow — Output Contracts |
| 14 | `qa-validation` | Test gate — Failure Modes + Contracts |
| 15 | `refactoring` | Behavior-preserving — compact Failure Modes |
| 16 | `setup-new-service` | Bootstrap — Failure Modes + Contracts |

### Tier 3 — LOW (2 workflows)
Smaller, narrow workflows. Add only Output Contracts.

| # | Workflow | Why T3 |
| --- | --- | --- |
| 17 | `seo-content-lifecycle` | Already small (72 lines); just Contracts |
| 18 | `seo-keyword-brief` | Add Output Contracts (seo-content-brief.json) |

---

## 4. Upgrade Template

For every Tier 1/2/3 workflow, the upgrade will:

1. **Add `## Failure Modes` section** (4-5 entries) — inserted before `## Related Workflows`. Each entry names a concrete failure scenario for the workflow (not generic), with mitigation that names the responsible role.
2. **Add `## Output Contracts` section** (1-3 entries) — inserted before `## Related Workflows`. Each entry names a JSON contract from `core/contracts/schemas/` that the workflow produces.
3. **Add `## Security Guardrails (OWASP ASI)` section** (3-4 entries) for Tier 1 only. Each entry names an ASI item relevant to the workflow.
4. **Add `## Security Guardrails` upgrade** for Tier 1 workflows that don't have one (most).
5. **No structural rewrites** — keep all 5 required sections intact and in the same order. The validator enforces the H2 / H3 / `Role:` / checklist structure.
6. **No `Use skill:` / `Related Skills` changes** — those are validated and resolve cleanly.
7. **No README changes** — already in sync.
8. **No new workflows** — out of scope.

### Standard upgrade blocks

```markdown
## Failure Modes

- **<pattern>**: <concrete failure scenario>. **Mitigation:** <what this workflow does to detect/prevent/recover>.
- **<pattern>**: <...>
- ...

## Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/<name>.json`** — <what it contains, when it is emitted>.
- ...

## Security Guardrails (OWASP ASI)

For Tier 1 workflows only:

- **ASI<NN>**: <one-line summary of the guardrail for this workflow>.
- ...
```

---

## 5. Hard rules

- **Never break the validator**: `validate-workflows.py` must continue to pass.
- **Never remove or rename a required section** (`### Prerequisites`, `### Workflow Steps`, `### Checklist`, `### Related Workflows`, `### Related Skills`).
- **Never add a 2nd H2 outside a fenced block** — the validator requires exactly 1 H2.
- **Never change a `#### N.` step's number** — must remain sequential from 1.
- **Never remove a `Role:` line** under a step.
- **Never remove a `Use skill:` inline reference** that resolves.
- **Never add a Related Skill that doesn't exist** in `core/skills/` (validator checks).
- **Never add a Related Workflow that doesn't exist** in `core/workflows/`.

---

## 6. Out of Scope (this audit only — flag if user wants)

- New workflows (out of scope; the audit is for upgrades).
- Removing workflows (out of scope).
- Renaming files (out of scope; the validator matches by stem).
- Changing the validator (out of scope; the audit is data-only).
- Adding `Use when` to frontmatter (would require validator change; could be a T3 follow-up).
- Adding `owner_role` to frontmatter (T3 follow-up).
- Cross-referencing policies in workflow prose (T2 follow-up).

---

## 7. Execution Order (after user approval)

| Batch | Tier | Count | Approach |
| --- | --- | ---: | --- |
| 1 | T1 | 10 | Add Failure Modes + Output Contracts + Security Guardrails per role-specific content |
| 2 | T2 | 6 | Add Failure Modes + Output Contracts (no Security Guardrails) |
| 3 | T3 | 2 | Add Output Contracts only |

After each batch: re-run `validate-workflows.py` and `validate-all.py` to confirm 0 errors and 0 warnings.

---

## 8. Questions for User Before Apply

1. **Tier scope:** T1 only (10), T1+T2 (16), or T1+T2+T3 (18)?
2. **Failure Modes depth:** 4-5 items per workflow acceptable (T1=5, T2=4, T3=4)? Or fixed 4 per workflow?
3. **Security Guardrails scope:** T1 only (10 workflows), or extend to T2 too (16 workflows)?
4. **Convert ad-hoc failure lists:** in `troubleshooting.md`, `data-migration.md`, `tech-repo-review.md`, `service-review-release.md`, the existing H3 failure areas should be **kept** (they're workflow-specific) but supplemented with a `## Failure Modes` section? Or replaced by the new `## Failure Modes`?
5. **Output Contracts naming:** should we name the exact JSON schemas the workflow emits (e.g., `feature-ticket.json`, `a2a-task.json`, `incident-report.json`)? Or keep them implicit?
6. **Commit/push policy:** per `core/rules/code.md` META-RULE — do NOT commit unless user confirms. Default: edits applied, validators re-run, no commit.

---

*Awaiting user direction before applying changes.*
