# Non-Human Identity (NHI) Lifecycle & Token Rotation (2026)

## 1. Executive Summary & Standards Alignment

In autonomous multi-agent environments, Non-Human Identities (NHI) outnumber human credentials at scale. This reference defines the zero-trust governance model adhering to:
- **IMDA Model AI Governance Framework for Agentic AI (2026)**
- **NIST AI 100-2 (EIV & Identity Proofing)**
- **RFC 8693 (OAuth 2.0 Token Exchange) & RFC 8707 (Resource Indicators)**
- **SPIFFE/SPIRE Workload Attestation Standards**

## 2. SPIFFE ID Taxonomy for Autonomous Agents

Agent workloads are assigned deterministic SPIFFE IDs reflecting cluster domain, namespace, role identity, and session instance:

```
spiffe://prod.internal/ns/agents/role/{role_name}/session/{session_uuid}
```

### Attestation Invariants
1. **Node Attestation**: AWS IID (Instance Identity Document) or K8s PSAT (Projected Service Account Token).
2. **Workload Attestation**: Unix process UID, container cgroup, and execution binary SHA256 digest.
3. **SVID Issuance**: X.509 SVID (mTLS) or JWT-SVID carrying cryptographically signed claims verifying agent role membership.

## 3. Just-In-Time (JIT) Credential Attenuation (RFC 8693)

Static API keys are prohibited. Agents negotiate task-scoped, ephemeral tokens:
- **Token Request**: Agent exchanges its short-lived JWT-SVID for an attenuated OAuth 2.0 access token via the central Security Token Service (STS).
- **Scope Attenuation**: The requested scope must be an exact subset of the role's declared `action-boundaries.yaml`.
- **TTL Bounds**: `min(task_estimated_duration * 1.2, 60 minutes)`.
- **Resource Constraints (RFC 8707)**: Token explicitly names authorized downstream target URIs.

## 4. Behavioral Baseline & Circuit Breaker Triggers

Active agent monitoring compares telemetry spans against the declared session baseline:
- **Tool Invocations**: An invocation of a tool not registered in `expected_tools` increments the anomaly counter. Three unexpected invocations trigger an immediate kill signal.
- **Path Traversal / Resource Boundary**: Single attempt to write outside `expected_resources` revokes the JWT-SVID and triggers automated quarantine.
- **Token Velocity**: Consumption of token budget > 150% halts execution pending human-in-the-loop (HITL) approval.

## 5. Automated Offboarding & Revocation Flow

Upon task completion or anomaly tripwire:
1. Revocation broadcast to OAuth introspection cache (Redis cluster blacklist).
2. SPIRE Server issues workload un-registration and terminates SVID renew loops.
3. Vault dynamic lease cancellation and immediate database credential purge.
4. Comprehensive audit log emitted adhering to `incident-report.json`.
