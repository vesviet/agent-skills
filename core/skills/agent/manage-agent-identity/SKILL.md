---
name: manage-agent-identity
description: Manages the full lifecycle of Non-Human Identities (NHI) for AI agent sessions — including provisioning scoped credentials, enforcing just-in-time access, behavioral baseline monitoring, and secure offboarding. Use when onboarding a new agent role to production, rotating agent credentials, auditing active agent sessions, or responding to anomalous agent behavior.
---

# Manage Agent Identity

Use this skill to govern the full **Non-Human Identity (NHI) lifecycle** for AI agent sessions. In 2025–2026, agents are privileged identities that often outnumber human identities at ratios of 82:1 or higher. Standard IAM service account patterns are insufficient — agents require task-scoped, just-in-time credentials with behavioral monitoring and formal offboarding.

Aligned with: **IMDA Model AI Governance Framework for Agentic AI (May 2026)**, **NIST AI 100-2**, **Cloud Security Alliance NHI guidance (2026)**, and **OWASP ASI03** (Identity & Privilege Abuse).

## Core Rules

- **Zero Standing Privileges**: never use static, long-lived API keys or persistent credentials for agent sessions. All agent tokens must be ephemeral (TTL ≤ 60 minutes or task duration + 20% buffer) and dynamically injected.
- **Task-scope permissions & attenuation (RFC 8693)**: issue down-scoped, attenuated delegation tokens. Agents must never inherit unconstrained human credentials or broad service-account scopes.
- **SPIFFE/SPIRE Workload Attestation**: attest agent workloads cryptographically using SPIFFE IDs and JWT/X.509 SVIDs bound to execution provenance (`spiffe://prod.internal/ns/agents/...`).
- **OAuth agent_auth metadata**: configure and validate the `agent_auth` discovery block in `/.well-known/oauth-protected-resource` and `/auth.md` before granting access.
- **Formal registration**: every agent role in production must be registered in the organization's identity registry before receiving any access. Shadow agents must be discovered and registered or decommissioned.
- **Behavioral baseline required**: every production agent role must declare a behavioral baseline (allowed tools, expected resource paths, rate limits). Out-of-baseline calls trigger immediate circuit breaker halts.
- **Immediate offboarding**: when a task completes, fails, or an agent role is decommissioned, all associated credentials, tokens, and active sessions must be revoked immediately.

## When to Use

- Onboarding a new agent role to production infrastructure
- Rotating compromised or expiring agent credentials
- Auditing existing agent sessions for privilege drift or stale access
- Responding to anomalous agent behavior (scope creep, unexpected tool calls, access spikes)
- Implementing just-in-time access patterns for a multi-agent workflow
- Decommissioning an agent role and revoking all associated access

## Suggested Process

### 1. Inventory & Registration

Before granting any access, register the agent identity:

```yaml
agent_identity:
  role: backend-developer          # must match agent-registry.json role slug
  session_type: task_scoped        # task_scoped | workflow_scoped | interactive
  owner: technical-lead            # human accountable for this identity
  pack_version: "2.12.0"
  registered_at: "2026-07-01T11:00:00Z"
  status: active
  policy_profile: backend-developer  # maps to action-boundaries.yaml
```

### 2. Credential Provisioning (Just-in-Time)

Issue task-scoped credentials at session start:

- **TTL**: set to the expected task duration + 20% buffer. Never open-ended.
- **Scope**: list only the specific resources, APIs, and tool actions declared in the task plan.
- **Injection method**: inject via environment variable or secret manager at runtime. Never embed in agent card, SKILL.md, or any committed file.
- **Rotation trigger**: rotate immediately if TTL approaches or if behavioral anomaly is detected.

```bash
# Example: Wrangler secret injection (Cloudflare)
wrangler secret put AGENT_ACCESS_TOKEN --env staging
# Never: hardcode in wrangler.toml or commit to any file
```

### 3. Session Baseline Declaration

Before delegating tasks, declare the expected behavioral baseline for the session:

```yaml
session_baseline:
  role: backend-developer
  task: add-api-endpoint
  expected_tools:
    - read_file
    - write_file
    - run_linter
    - run_tests
  expected_resources:
    - "src/api/**"
    - "tests/**"
  expected_duration_minutes: 30
  token_budget_estimated: 8000
  anomaly_thresholds:
    unexpected_tool_calls: 3       # halt after 3 out-of-baseline tool calls
    resource_access_outside_scope: 1  # halt immediately
    token_budget_overage_pct: 50   # halt if actual > 1.5× estimated
```

### 4. Active Session Monitoring

During execution, monitor against the baseline:

- **Tool call validation**: check every tool invocation against the declared expected_tools list and the role's `action-boundaries.yaml` profile. Out-of-scope calls are flagged.
- **Resource scope check**: verify file paths and API endpoints accessed are within declared scope.
- **Token budget tracking**: compare actual to estimated. Alert at 2× estimate.
- **Behavioral drift detection**: watch for unusual call sequences (e.g., read_file → write_file on files outside declared scope).

### 5. Offboarding & Revocation

When the session ends or the role is decommissioned:

```yaml
offboarding:
  role: backend-developer
  session_id: "task-add-api-2026-07-01"
  completed_at: "2026-07-01T12:30:00Z"
  actions:
    - revoke_access_token: true
    - clear_session_cache: true
    - archive_trace_spans: true    # for audit trail
    - notify_registry: true        # update identity registry status
  retention:
    trace_spans: 90d               # for compliance/audit
    session_context: 0             # do not retain context
```

### 6. Audit & Compliance

Produce an audit record for every production agent session:

| Field | Description |
|---|---|
| `session_id` | UUID v4 assigned at session start |
| `role` | Role slug from agent-registry.json |
| `owner` | Human accountable for this session |
| `task_ref` | A2A task ID or workflow name |
| `credentials_issued_at` | Timestamp |
| `credentials_revoked_at` | Timestamp |
| `tools_invoked` | List of tools actually called |
| `resources_accessed` | List of files/APIs accessed |
| `anomalies_detected` | Any out-of-baseline events |
| `policy_violations` | Any action-boundaries violations |

---

## Checklist

- [ ] Agent role is registered in identity registry before any access is granted.
- [ ] Credentials are task-scoped and short-lived (TTL ≤ task duration + buffer).
- [ ] Credentials are injected at runtime — not embedded in committed files or agent cards.
- [ ] Session behavioral baseline is declared before task delegation begins.
- [ ] Active session monitoring is enabled for tool calls and resource access.
- [ ] Token budget is declared and anomaly thresholds are set.
- [ ] Session is offboarded and credentials revoked when task completes.
- [ ] Audit record produced for every production session.
- [ ] Shadow agent inventory check completed (no unregistered agents in production).
- [ ] OWASP ASI03 (Identity & Privilege Abuse) threat mitigated: no privilege escalation chains.

---

## Output Format

- `agent_identity.yaml` — registration record for the identity registry
- `session_baseline.yaml` — behavioral baseline declaration for the session
- `session_audit.json` — post-session audit record
- Updated identity registry entry (offboarding status)

---

## Related Skills

- **agent-a2a-protocol**: A2A task delegation — session identity must be established before delegation.
- **agent-tool-orchestration**: Tool call validation against `action-boundaries.yaml` — works alongside session baseline monitoring.
- **manage-secrets**: Securely store and rotate agent credentials in secret managers.
- **security-audit**: Full security posture audit including NHI inventory review.
- **agent-observability**: Trace spans for session monitoring — NHI session ID is a required span attribute.
