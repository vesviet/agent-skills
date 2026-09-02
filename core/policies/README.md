# Policies

This directory contains machine-readable policies that define action boundaries, data classification, and governance rules for agent operations.

## Why Policies Exist

Text-based rules in `core/rules/code.md` are advisory. Policies in this directory are structured YAML definitions that can be checked programmatically at runtime.

Policies answer: "Is this agent, in this role, allowed to perform this action on this data?"

## Policy Files

| File | Purpose | Schema |
| --- | --- | --- |
| `action-boundaries.yaml` | 34 delivery roles × 46 action verbs (allowed / requires_approval / denied) | `2` |
| `data-classification.yaml` | 5 sensitivity levels (untrusted, public, internal, confidential, restricted) | `1` |
| `mcp-tool-map.yaml` | 75 tool-action mappings + 79 destructive patterns | implicit `1` |

## Policy Types

### Action Boundaries

`action-boundaries.yaml` defines what each of the 34 delivery roles is allowed, requires approval for, or denied from doing.

The default for any action not listed for a role is `requires_approval` (zero-trust). Unclassified actions in irreversible verbs (apply_iac, drop_storage_volume, terminate_instance, modify_iam_policy, modify_network_topology_production, modify_payment_gateway_config, self_approve_iam, shipping_label_generation, delete_cloudflare_resource) are now explicitly `denied` for non-owner roles per 2026 T1/T2 upgrade.

### Data Classification

`data-classification.yaml` defines sensitivity levels for different data types to prevent accidental exposure. Levels (low → high): public → internal → confidential → restricted, plus the inversion level `untrusted`.

The `restricted` level carries an explicit PII catalog (8 categories: full_name, email_address, phone_number, physical_address, date_of_birth, national_id_or_passport, financial_account_number, biometric_data, ip_address_when_linked_to_person). The `internal` level now lists soft-PII examples (internal emails, org-chart data, non-customer phones and chat handles).

### MCP Tool Mapping

`mcp-tool-map.yaml` maps IDE/MCP tool names to policy action ids for `agent-tool-orchestration` and Cursor hooks. 2026 coverage: Python (uv, poetry, pipx), Docker, kubectl (delete, rollout, scale, exec), GitHub CLI (gh pr/release/repo/secret), and npx/pnpm dlx.

## Example Decision Table (backend-developer)

| Action | Tier | Verdict |
| --- | --- | --- |
| `read_file` | allowed | pass-through |
| `write_file` | allowed | pass-through |
| `delete_file` | requires_approval | HITL gate |
| `npm install` | requires_approval (via mcp-tool-map) | HITL gate |
| `push_to_production` | denied | always block |

## Compliance Posture (2026)

- **EU AI Act Article 9**: risk tier `minimal_risk`; enforcement active since 2026-08-02; quarterly review cycle; six actions require human oversight (`push_to_production`, `run_migration`, `modify_secrets`, `deploy_ai_model`, `apply_iac`, `rotate_agent_credentials`).
- **NIST AI RMF 1.0**: govern (roles), map (gated/denied lists), measure (OCSF 99001 audit trail), manage (HITL).
- **ATF 2026**: zero-trust fail-closed posture; 90-day retention; OCSF 99001 audit format; hook `core/scripts/hooks/check-policy.py`.
- **Access control**: short-lived OIDC; signing key `env:AGENT_SIGNING_KEY`.

## Runtime Hook

`core/scripts/hooks/check-policy.py` is the runtime policy gate. It supports:

- **text / json / sarif** output modes (SARIF 2.1.0 for GitHub Code Scanning).
- **Exit codes**: 0 = allowed, 1 = policy violation (denied), 2 = approval required.
- **Trace context**: `AGENT_TRACE_ID` env var propagates W3C Trace Context.
- **Role level** (2026 T1): `AGENT_ACTIVE_ROLE_LEVEL=read_only` downgrades any non-allowed verdict to `denied` (block writes for observe-only sessions). `supervised` (default) and `unsupervised` keep the policy verdict.
- **Audit emission** (2026 T1): `--emit-audit` writes an OCSF 99001 event per decision to the configured path (`--audit-path`, default `policy_decision.jsonl`).

## Usage

Skills and adapters should reference policies when making decisions about state-changing actions:

1. identify the current role (set `AGENT_ACTIVE_ROLE` env var)
2. identify the action being attempted (resolve tool name to action id via `mcp-tool-map.yaml`)
3. check the action against `action-boundaries.yaml`
4. if the action involves data, check sensitivity against `data-classification.yaml`
5. proceed, request approval, or deny based on the policy result
6. (optional) emit an OCSF 99001 audit event with `--emit-audit`

## Relationship To Rules

`core/rules/code.md` remains the human-readable always-on rules. Policies provide the structured, machine-checkable complement. When both exist, policies take precedence for enforcement.

Last updated: 2026-09-01

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-02
