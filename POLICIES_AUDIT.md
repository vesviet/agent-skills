# Policies Upgrade Audit (`core/policies`)

**Scope:** 3 policy YAML files + 1 README under `core/policies/`
**Baseline:** `validate-policy-consistency.py` and `validate-2026-compliance.py` currently pass (0 errors).
**Goal of this audit:** identify gaps in policy depth, 2026 standardization, and operational usability before applying upgrades.
**Standard chosen for upgrades:** *2026 Standardization* — preserve every existing verb and role mapping, add 2026 metadata where missing, normalize the `check-policy.py` hook contract, expand the README and tier distribution to make 2026 compliance obvious.

---

## 1. Inventory Snapshot

| Metric | Value |
| --- | --- |
| Total policy files audited | 3 (+ 1 README) |
| Currently passing `validate-policy-consistency.py` | pass |
| Currently passing `validate-2026-compliance.py` (policy coverage slice) | pass |
| Total action verbs in `action-boundaries.yaml` | 46 |
| Total role profiles | 34 (all roles covered) |
| Default policy | `requires_approval` (zero-trust) |
| Compliance metadata | EU AI Act Article 9 + NIST AI RMF + ATF 2026, OCSF 99001 audit trail |
| `data-classification.yaml` levels | 5 (untrusted, public, internal, confidential, restricted) |
| `mcp-tool-map.yaml` tool_actions | 65 |
| `mcp-tool-map.yaml` destructive_patterns | 53 |
| Tool map actions missing in policy | 0 (full coverage) |
| Skills referencing policies | 23 / 97 (24%) |
| Role files referencing policies | 6 / 34 (18%) |
| Adapter hook `core/scripts/hooks/check-policy.py` | 287 lines, supports text/json/sarif output |

**Bottom line:** every policy passes the validator. The "gaps" the audit finds are **enhancement opportunities**, not validator failures.

---

## 2. Detailed Findings

### 2.1 `action-boundaries.yaml` — `core/policies/action-boundaries.yaml` (1,020 lines, 26 KB)

**Strengths**
- Full coverage of 34 roles × 46 action verbs
- Always-denied set `{bypass_ai_guardrail}` is denied for all 34 roles (security-by-default)
- Always-irreversible set `NEVER_ALLOWED` (15 verbs) is gated or denied for every role
- Audit trail format (`ocsf-99001`), retention (90 days), and hook script path are explicit
- Default policy is `requires_approval` (zero-trust)
- `self_approve_iam` is correctly denied for `aws-engineer`

**Gaps / inconsistencies**
- **6 actions have ≥ 5 unclassified roles** (would fall back to `default_policy: requires_approval`):
  - `apply_iac` — 31 unclassified (only aws-engineer, system-engineer, ai-systems-engineer classify it)
  - `delete_cloudflare_resource` — 33 unclassified
  - `drop_storage_volume` — 31 unclassified
  - `modify_iam_policy` — 33 unclassified
  - `modify_network_topology_production` — 32 unclassified
  - `modify_payment_gateway_config` — 33 unclassified
  - `self_approve_iam` — 33 unclassified
  - `shipping_label_generation` — 33 unclassified
  - `terminate_instance` — 31 unclassified
  - `write_database` — 29 unclassified
  - `delete_file` — 2 unclassified (likely a bug; sre and reviewer have it denied but others don't classify it)
  - `modify_environment_config` — 2 unclassified
  - `run_migration` — 1 unclassified
  - `run_build` — 1 unclassified
  - `modify_prompt_template` — 1 unclassified
  - `push_to_production` — 0 unclassified (clean)
- **README count is stale**: README says "26 delivery roles" but the file declares 34 profiles.
- **No schema_version changelog**: `schema_version: "2"` is set but there is no migration guide.
- **`compliance` block is dense but undocumented in the README**: the README does not explain the EU AI Act / NIST AI RMF / OCSF linkage.

### 2.2 `data-classification.yaml` — `core/policies/data-classification.yaml` (105 lines, 4 KB)

**Strengths**
- 5 levels (untrusted, public, internal, confidential, restricted)
- `restricted` includes 8 explicit PII categories (PII catalog)
- Each level has `logging`, `memory_storage`, `agent_access`, `retention_in_context`, and 2-4 handling rules
- Levels: low → high, with "when in doubt, treat higher" rule

**Gaps / inconsistencies**
- **No `schema_version` field** (unlike `action-boundaries.yaml`). The file is implicit version 1, but consumers cannot detect drift.
- **No cross-link to roles**: 28 of 34 roles could reference this policy at the points where they touch data, but only 6 do.
- **`untrusted` is unique vs. the others** — has `agent_access: allowed` while `restricted` has `agent_access: denied`; some readers may not parse this inversion. Recommend a comment clarifying the inversion.
- **No example for "ephemeral session tokens" or "short-lived OIDC"** in `restricted` examples, even though `action-boundaries.yaml` calls these out.
- **No PII field for `internal`** — only `restricted` lists PII categories. Some orgs tag `internal` with soft PII (org chart, internal emails).

### 2.3 `mcp-tool-map.yaml` — `core/policies/mcp-tool-map.yaml` (232 lines, 6 KB)

**Strengths**
- 65 tool → action mappings covering file ops, code nav, build/test/lint, terminal, database, network/MCP, deployment, delegation, export, dependency mgmt, Laravel, Bun, PNPM, Astro
- 53 destructive patterns with explicit priority over tool_actions
- Comments explain resolution order

**Gaps / inconsistencies**
- **Duplicate `drop database` pattern** (lines 124 and 125) — harmless but dead weight; should be deduplicated.
- **No Python/uv coverage** — only npm/pip/yarn/cargo/bun/pnpm/composer/gem. Python's `uv` (2026 default) and `poetry add` are missing.
- **No `pnpm dlx`** (executes a package without installing).
- **No Docker `docker run` / `docker compose up`** — these can trigger deployment-shaped actions.
- **No `kubectl delete`** — only `kubectl apply` is mapped.
- **No `npm exec` / `npx`** beyond Bun/PNPM coverage.
- **No `gh` (GitHub CLI)** — `gh pr create`, `gh release create` are state-changing but absent.
- **No `redis-cli`, `psql`, `mysql`** direct shell mappings.

### 2.4 `check-policy.py` hook — `core/scripts/hooks/check-policy.py` (287 lines)

**Strengths**
- 2026 features: text/json/sarif output, exit code 2 for `requires_approval`, exit code 1 for `denied`, exit code 0 for `allowed`
- W3C Trace Context `trace_id` propagation in JSON/SARIF output
- `AGENT_ACTIVE_ROLE_LEVEL` env var for tier-aware checks (mentioned in docstring; not yet wired in `check_action`)
- `AGENT_SKILLS_ROOT` env var for pack resolution
- Has a minimal YAML parser fallback when `yaml` is missing (good for hook environments)

**Gaps / inconsistencies**
- **Docstring says "exit code 2 for script errors vs 1 for policy violations"** but the actual code returns 2 for `requires_approval` and 1 for `denied`. The convention is right (0=ok, 1=denied, 2=approval-required) but the docstring is misleading.
- **AGENT_ACTIVE_ROLE_LEVEL is documented but not implemented** in `check_action()`. Either implement or remove the docstring claim.
- **SARIF emission is incomplete**: the `if decision != "allowed" else []` modifier is on the wrong list (the `results` list, not the run block), so SARIF output structure may be malformed when decision is `allowed`. Need to verify and fix.
- **No retry / re-eval on stale policy file**: the policy is loaded once at startup. If a role changes mid-session, the new policy won't be picked up.
- **No `policy_decision_log` integration**: the comment says "audit events for every policy decision via ocsf-99001 format" but the script does not emit an audit event; it just prints the decision.

### 2.5 `README.md` — `core/policies/README.md` (37 lines)

**Strengths**
- 3 policy types clearly explained
- Usage 5-step pattern (role → action → boundary → data classification → verdict) matches the runtime check
- "Relationship to rules" clarifies the policy vs. rule precedence

**Gaps**
- **Stale count**: "26 delivery roles" but there are 34.
- **No mention of `check-policy.py` hook**, OCSF 99001 audit format, EU AI Act Article 9 link.
- **No version field** matching the other 3 files.
- **No example decision table** showing `allowed / requires_approval / denied` for a sample role.

---

## 3. Cross-Cutting Gaps

- **Role files do not all reference policies**: only 6 of 34 roles mention `action-boundaries` or `data-classification`. The README explains the 5-step pattern but roles do not operationalize it.
- **Skills that should reference policies don't**: `agent-delegation` (A2A delegation) does not name `action-boundaries`; `manage-secrets` does not name `data-classification`.
- **Validator (validate-policy-consistency.py) does not catch unclassified roles**: a role with `delete_file` unclassified falls through to `default_policy: requires_approval`, which is safe but should be explicit.

---

## 4. Priority Tiers

### Tier 1 — HIGH PRIORITY (must-fix in this pass)

| # | File | Issue | Action |
| --- | --- | --- | --- |
| 1 | `action-boundaries.yaml` | README says 26 roles, file has 34 | Bump README count; add a comment in YAML header |
| 2 | `action-boundaries.yaml` | 16 actions have ≥ 1 unclassified role | Add explicit tier placement (mostly `denied` for irreversible verbs in non-deploy roles) |
| 3 | `data-classification.yaml` | No `schema_version` | Add `schema_version: "1"` at the top |
| 4 | `check-policy.py` | Docstring says "exit 2 = script error" but actual is "exit 2 = requires_approval" | Update docstring to match convention (0=ok, 1=denied, 2=approval-required) |
| 5 | `check-policy.py` | SARIF list comprehension `if decision != "allowed" else []` is on wrong line | Fix the SARIF emission structure |
| 6 | `check-policy.py` | `AGENT_ACTIVE_ROLE_LEVEL` is documented but not implemented | Either implement (read env, modulate verdict) or remove the docstring claim |
| 7 | `mcp-tool-map.yaml` | Duplicate `drop database` pattern | Deduplicate |
| 8 | `mcp-tool-map.yaml` | No Python `uv`, `poetry add`, `pipx` | Add Python tooling patterns |
| 9 | `mcp-tool-map.yaml` | No `docker`, `kubectl delete`, `gh`, `redis-cli`, `psql`, `npx` | Add at least docker, kubectl delete, gh, npx |
| 10 | `README.md` | No version field | Add `Last updated: 2026-09-01` footer |

### Tier 2 — MEDIUM (additions to bring 2026 completeness)

| # | File | Issue | Action |
| --- | --- | --- | --- |
| 11 | `data-classification.yaml` | No `untrusted` inversion comment | Add a comment explaining `agent_access: allowed` for untrusted (sanitized) |
| 12 | `data-classification.yaml` | PII catalog only in `restricted` | Add a soft-PII note under `internal` |
| 13 | `action-boundaries.yaml` | No schema_version changelog | Add a comment block with v1 → v2 changes |
| 14 | `README.md` | No example decision table | Add a 3-row example: `allowed`, `requires_approval`, `denied` |
| 15 | `check-policy.py` | No audit event emission | Add a `policy_decision.json` write hook (optional, behind env flag) |

### Tier 3 — LOW (nice-to-have, not in this pass)

- `check-policy.py`: re-eval on stale policy file
- `mcp-tool-map.yaml`: Redis/psql/mysql direct shell
- `data-classification.yaml`: expand PII catalog with `passport`, `tax_id` (already present), `health_id`

---

## 5. Upgrade Template (per file)

### `action-boundaries.yaml`
- Bump `schema_version` to `"2"` (already there) and add a CHANGELOG comment block
- Add explicit tier placement for unclassified actions (mostly `denied` for irreversible)
- Update header comment with 34-role count

### `data-classification.yaml`
- Add `schema_version: "1"` at top
- Add comments explaining the `untrusted` inversion
- Add soft-PII note under `internal`

### `mcp-tool-map.yaml`
- Deduplicate `drop database` pattern
- Add Python tooling: `uv`, `poetry add`, `poetry install`, `pipx install`
- Add `docker run`, `docker compose up`
- Add `kubectl delete`, `kubectl rollout`
- Add `gh pr create`, `gh release create`
- Add `npx`

### `check-policy.py`
- Fix docstring convention
- Fix SARIF emission structure (move `if/else` to the correct list)
- Either implement `AGENT_ACTIVE_ROLE_LEVEL` or remove the claim
- Add a `--emit-audit` flag that writes a `policy_decision.json` file in OCSF 99001 format

### `README.md`
- Bump count: "34 delivery roles"
- Add a version footer
- Add a 3-row example decision table
- Add the EU AI Act / OCSF / check-policy.py references

---

## 6. Hard rules

- **Never break the validator**: `validate-policy-consistency.py` and `validate-2026-compliance.py` must continue to pass.
- **Never remove an action verb from a role profile**: only add or reclassify.
- **Never add a verb to `allowed` for an irreversible action** (validator enforces this).
- **Keep YAML syntax 100% backward compatible**: external hooks parse the same shape.
- **Do not change `default_policy: requires_approval`**.
- **Do not remove `bypass_ai_guardrail` from any role's `denied` list** (always-denied invariant).
- **No comment on the policy verb meanings** in the YAML header — the comments there are an interface contract.

---

## 7. Out of Scope (this audit only — flag if user wants)

- Adding new roles or action verbs (out of scope; the audit is for upgrades).
- Removing existing roles (out of scope; the audit does not delete anything).
- Changing default policy posture (out of scope; would be a major governance change).
- New policy types (e.g., `cost-boundaries.yaml`) — the audit is for upgrades, not additions.
- `core/rules/code.md` updates — the rules layer is separate.
- Adapter (`adapters/antigravity/`, `adapters/cursor/`) policy wiring — separate work.

---

## 8. Execution Order (after user approval)

| Batch | Tier | Count | Approach |
| --- | --- | ---: | --- |
| 1 | T1 action-boundaries | 1 file | Add comments + explicit tier for 16 unclassified actions |
| 2 | T1 data-classification | 1 file | Add `schema_version` + comments |
| 3 | T1 mcp-tool-map | 1 file | Dedupe + add Python/Docker/kubectl/gh/npx |
| 4 | T1 check-policy.py | 1 file | Fix docstring + SARIF + implement AGENT_ACTIVE_ROLE_LEVEL |
| 5 | T1+T2 README | 1 file | Bump count, add example, add version footer |
| 6 | T2 action-boundaries + data-classification | 2 files | Schema-version changelog, soft-PII note |

After each batch: re-run `validate-policy-consistency.py` and `validate-all.py` to confirm 0 errors.

---

## 9. Questions for User Before Apply

1. **Scope:** T1 only (10 fixes) or T1+T2 (15 fixes)?
2. **Action-boundaries unclassified verbs:** OK to add explicit `denied` (not `requires_approval`) for irreversible verbs in non-deploy roles, so the check is fail-closed? Or do you prefer to keep them at `default_policy: requires_approval`?
3. **MCP tool map additions:** OK to add Python `uv`/`poetry`/`pipx`, Docker, kubectl delete, gh, npx, kubectl rollout? Or do you want a smaller set?
4. **check-policy.py AGENT_ACTIVE_ROLE_LEVEL:** implement tier-aware modulation (read env, treat as `requires_approval` downgrade when set to "read_only"), or remove the claim?
5. **check-policy.py audit event:** add `--emit-audit` flag (writes a `policy_decision.json` next to the hook), or skip?
6. **Commit/push policy:** per `core/rules/code.md` META-RULE — do NOT commit unless user confirms. Default: edits applied, validators re-run, no commit.

---

*Awaiting user direction before applying changes.*
