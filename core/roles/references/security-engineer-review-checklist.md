## Security Engineer Review Checklist

This reference checklist provides comprehensive security architecture, threat modeling, agentic runtime defense, identity federation, and compliance verification criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across OWASP ASI Top 10 (2026), OWASP Agentic Skills Top 10 (AST10), Non-Human Identity (NHI) governance, SPIFFE/SVID workload federation, SLSA Level 3 supply-chain security, automated secret leak defenses, and EU AI Act Article 15 adversarial resilience testing.

### 1. Shift-Left Threat Modeling & Trust Boundary Analysis (`SHIFT-LEFT LOCK`)
- **Systematic Trust Boundary Identification**:
  - data flow diagrams (DFD) explicitly enumerate every boundary crossing: client-to-edge, edge-to-service, service-to-database, and agent-to-tool
  - STRIDE-per-element analysis conducted on all new architecture endpoints before any code implementation begins
  - entry points, untrusted input surfaces, and sensitive data persistence paths cataloged in `contracts/schemas/security-audit.json`
- **Blast Radius & Exploit Path Quantification**:
  - worst-case impact radius calculated for each credential, tool permission, and API token:
    $$\text{Impact Radius} = \text{Data Classification Tier} \times \text{Blast Scope Tiers (1--4)}$$
  - single-tool exploit radius isolated from chained multi-tool exploit paths; automated kill-switch and blast-radius fences verified prior to deployment

### 2. OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10) Defense
- **Prompt Injection & Goal Hijacking (ASI01 / `PROMPT-INJECTION LOCK`)**:
  - user-supplied inputs and external web retrieval content strictly isolated from system prompt instructions via delimiter boundaries and token sanitization
  - output verification layers inspect LLM responses before tool argument interpolation or user delivery
  - indirect prompt injection payloads (hidden in HTML comments, markdown images, or retrieved documents) actively filtered
- **Tool Misuse & Unauthorized Execution (ASI02 / `TOOL-MISUSE LOCK`)**:
  - tool invocations validated against the active role's declared toolbox and action-boundaries policy profile
  - dynamic command construction from untrusted content rejected fail-closed; parameter types strictly enforced via JSON Schema
- **Memory & Inter-Agent Context Poisoning (ASI06 / ASI07 / `MEMORY-ISOLATION LOCK`)**:
  - persistent vector stores and episodic memory repositories treat write operations as untrusted surfaces
  - memory retrieval sanitization strips prompt injection triggers and PII before injecting into agent context windows
  - peer agent messages authenticated via cryptographic signatures; no implicit trust based on claimed sender role

### 3. In-Kernel Synchronous Enforcement via Cilium Tetragon
- **Synchronous In-Kernel Sigkill Policies**:
  - Tetragon `TracingPolicy` attached to kernel system calls (`sys_execve`) triggers synchronous in-kernel `Sigkill` upon detection of unauthorized interactive shells or scripting runtimes in production namespaces before execution returns to userspace:
    ```yaml
    apiVersion: cilium.io/v1alpha1
    kind: TracingPolicy
    metadata:
      name: block-production-exec
    spec:
      kprobes:
        - call: "sys_execve"
          syscall: true
          args:
            - index: 0
              type: "string"
          selectors:
            - matchArgs:
                - index: 0
                  operator: "Prefix"
                  values: ["/bin/sh", "/bin/bash", "/usr/bin/python", "/bin/busybox"]
              matchNamespaces:
                - "production"
                - "payment-processing"
              matchActions:
                - action: Sigkill
    ```
  - worker nodes enforce Linux kernel $\ge 5.15$ with BPF Type Format (BTF) and $\ge 32\text{MB}$ ring buffer allocation

### 4. OWASP Agentic Skills Top 10 (AST01–AST10) Governance
- **Lethal Trifecta Detection & Outright Rejection (AST03 / `EGRESS-ALLOWLIST LOCK`)**:
  - any skill or tool combining the lethal trifecta — (1) access to private sensitive data + (2) ingestion of untrusted external content + (3) external network egress capability — must be rejected fail-closed
  - network egress restricted to explicitly declared domain allowlists in `core/policies/action-boundaries.yaml`
- **Agent Identity & Config File Immutability (`IDENTITY-FILE-PROTECTION LOCK`)**:
  - agent identity files (`MEMORY.md`, `SOUL.md`, `AGENTS.md`) protected with immutable deny-write locks; subagent attempts to overwrite orchestrator rules trigger immediate P0 security alarms

### 5. Non-Human Identity (NHI) Architecture & SPIFFE/SVID Workload Federation (`NHI-LIFECYCLE LOCK`)
- **Zero Static Credentials & Centralized NHI Inventory**:
  - all autonomous agents, background daemons, and microservices registered in the centralized Non-Human Identity (NHI) inventory with documented business purpose, owner, and lifecycle SLA
  - static API keys, standing database passwords, and long-lived cloud access keys (`AKIA*`) strictly eliminated in production
- **Workload Identity in Multi-System Environments (WIMSE / SPIFFE/SVID)**:
  - agent workloads issued short-lived cryptographic X.509 SVIDs or JWT-SVIDs via SPIFFE/SPIRE with TTL $\le 1\text{h}$
  - cross-cluster and cross-cloud authentication utilizes RFC 8693 token exchange; credentials dynamically requested just-in-time (JIT) and auto-expired

### 6. Secret Management & Automated Leak Defenses (`NO-SECRETS LOCK`)
- **Secret Scanning & Pre-Commit Enforcement**:
  - pre-commit hooks (TruffleHog / Gitleaks) and CI scanning active across 100% of repositories; high-entropy string detection blocks commits before push
  - zero plaintext secrets in `.env`, `.dev.vars`, Dockerfiles, Kubernetes manifests, or commit history
  - detection of leaked credential triggers immediate automated revocation and security alert within 15 minutes SLA

### 7. Supply Chain Security, SLSA Level 3 & Kyverno Admission
- **SLSA Level 3 Attestation & Fail-Closed Admission**:
  - container images signed with Cosign / Sigstore and verified in Kyverno admission controllers with fail-closed enforcement:
    ```yaml
    apiVersion: kyverno.io/v1
    kind: ClusterPolicy
    metadata:
      name: verify-image-signatures
    spec:
      validationFailureAction: Enforce
      rules:
      - name: check-cosign-signature
        match:
          any:
          - resources:
              kinds: ["Pod"]
        verifyImages:
        - imageReferences: ["ghcr.io/internal/*"]
          attestors:
          - entries:
            - keyless:
                issuer: "https://token.actions.githubusercontent.com"
                subject: "https://github.com/org/repo/.github/workflows/*"
    ```
  - comprehensive Syft CycloneDX 1.6 / SPDX 2.3 SBOM attached to build artifacts

### 8. Operational Telemetry & Threat Invariants
- **PromQL Real-Time Security Metrics**:
  ```promql
  # In-kernel synchronous process termination alert
  rate(tetragon_events_total{action="Sigkill"}[5m]) > 0
  
  # Elevated authentication failure velocity
  rate(security_auth_failures_total[5m]) > 5
  ```

### 9. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Tetragon Kernel Sigkill**| Synchronous termination | `kubectl exec -n production -- /bin/sh` | Command killed immediately |
| **Cosign Signature** | Valid Fulcio/Rekor proof | `cosign verify --certificate-identity ...` | Valid keyless signature |
| **Zero Secrets Gate** | Entropy $< 4.5$, 0 keys | `trufflehog git file://. --since-commit HEAD~1` | 0 secret findings |
| **Lethal Trifecta Gate** | 0 uncontained skills | `python3 core/scripts/validate-policy-consistency.py` | 0 trifecta violations |
| **SPIFFE SVID Expiry** | TTL $\le 1\text{h}$ | `spire-agent api fetch x509` | Lifetime $\le 3600\text{s}$ |
| **Audit Log Integrity** | WORM storage valid | S3 Object Lock configuration check | Immutability active, retention $\ge 180\text{d}$ |
| **Audit Contract** | Valid `security-audit.json` | `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
