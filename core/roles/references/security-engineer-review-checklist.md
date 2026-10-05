## Security Engineer Review Checklist

This reference checklist provides comprehensive security architecture, threat modeling, agentic runtime defense, identity federation, and compliance verification criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across OWASP ASI Top 10 (2026), OWASP Agentic Skills Top 10 (AST10), Non-Human Identity (NHI) governance, SPIFFE/SVID workload federation, SLSA Level 3 supply-chain security, automated secret leak defenses, and EU AI Act Article 15 adversarial resilience testing.

### 1. Shift-Left Threat Modeling & Trust Boundary Analysis (`SHIFT-LEFT LOCK`)
- **Systematic Trust Boundary Identification**:
  - data flow diagrams (DFD) explicitly enumerate every boundary crossing: client-to-edge, edge-to-service, service-to-database, and agent-to-tool
  - STRIDE-per-element analysis conducted on all new architecture endpoints before any code implementation begins
  - entry points, untrusted input surfaces, and sensitive data persistence paths cataloged in `contracts/schemas/security-audit.json`
- **Blast Radius & Exploit Path Quantification**:
  - worst-case impact radius calculated for each credential, tool permission, and API token:
    - single-tool exploit radius vs chained multi-tool exploit path
    - automated kill-switch and blast-radius fences verified prior to deployment

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

### 3. OWASP Agentic Skills Top 10 (AST01–AST10) Governance
- **Lethal Trifecta Detection & Outright Rejection (AST03 / `EGRESS-ALLOWLIST LOCK`)**:
  - any skill or tool combining the lethal trifecta — (1) access to private sensitive data + (2) ingestion of untrusted external content + (3) external network egress capability — must be rejected fail-closed
  - network egress restricted to explicitly declared domain allowlists
- **Skill Provenance, Sandboxing & Integrity (AST01 / AST02 / AST06 / `SKILL-PROVENANCE LOCK`)**:
  - skills imported from external registries must provide cryptographic publisher signatures and immutable commit/content hashes
  - skills executed inside isolated container or WebAssembly (WASM) sandboxes with read-only filesystems except for designated output scratch directories
  - agent identity files (`MEMORY.md`, `SOUL.md`, `AGENTS.md`) protected with immutable deny-write locks (`IDENTITY-FILE-PROTECTION LOCK`)

### 4. Non-Human Identity (NHI) Architecture & WIMSE Workload Federation (`NHI-LIFECYCLE LOCK`)
- **Zero Static Credentials & Centralized NHI Inventory**:
  - all autonomous agents, background daemons, and microservices registered in the centralized Non-Human Identity (NHI) inventory with documented business purpose, owner, and lifecycle SLA
  - static API keys, standing database passwords, and long-lived cloud access keys (`AKIA*`) strictly eliminated in production
- **Workload Identity in Multi-System Environments (WIMSE / SPIFFE/SVID)**:
  - agent workloads issued short-lived cryptographic X.509 SVIDs or JWT-SVIDs via SPIFFE/SPIRE with TTL $\le 1\text{h}$
  - cross-cluster and cross-cloud authentication utilizes RFC 8693 token exchange; credentials dynamically requested just-in-time (JIT) and auto-expired

### 5. Secret Management & Automated Leak Defenses (`NO-SECRETS LOCK`)
- **Secret Scanning & Pre-Commit Enforcement**:
  - pre-commit hooks (TruffleHog / Gitleaks) and CI scanning active across 100% of repositories; high-entropy string detection blocks commits before push
  - zero plaintext secrets in `.env`, `.dev.vars`, Dockerfiles, Kubernetes manifests, or commit history
- **Secret Lifecycle & Rotation Automation**:
  - credentials stored in AWS Secrets Manager, HashiCorp Vault, or Cloudflare Secrets with automated rotation schedules ($\le 90$ days)
  - detection of leaked credential triggers immediate automated revocation and security alert within 15 minutes SLA

### 6. Supply Chain Security, SLSA Level 3 & SBOM Integrity
- **Software Bill of Materials (SBOM)**:
  - CycloneDX or SPDX SBOM generated automatically on every build artifact; dependencies scanned for CVEs via Grype/Trivy
  - zero critical or high vulnerabilities with available fixes allowed in production release artifacts
- **Build Reproducibility & SLSA Level 3 Attestation**:
  - container images signed with Cosign / Sigstore; provenance attestations verified in Kubernetes admission controllers (Kyverno / OPA Gatekeeper)
  - dependencies pinned to immutable SHA-256 hashes; floating version tags (`:latest`, `^1.0.0`) prohibited

### 7. MCP Server Sandboxing, Version Pinning & OAuth 2.1 PKCE (`MCP-SERVER-INTEGRITY LOCK`)
- **Mandatory OAuth 2.1 & PKCE Authentication**:
  - all external or network-exposed Model Context Protocol (MCP) server endpoints mandate OAuth 2.1 authentication with Proof Key for Code Exchange (PKCE)
  - authorization scopes enforced at endpoint grain; unauthenticated MCP tool calls rejected fail-closed
- **Immutable Version Pinning & Static Analysis**:
  - MCP server implementations pinned to immutable release tags and cryptographic package hashes
  - tool descriptions scanned for embedded prompt injection payloads, hidden escape characters, or prompt manipulation directives

### 8. EU AI Act Article 15 Adversarial Resilience & Auditability
- **Adversarial Red-Teaming & Stress Testing**:
  - high-risk AI systems and GPAI integrations evaluated against automated adversarial test harnesses (PyRIT, Garak) covering jailbreaks, prompt leakage, and extraction attacks
  - resilience test reports and pass-rates archived for regulatory inspection
- **WORM Tamper-Evident Audit Logging**:
  - input prompts, output responses, decision timestamps, model IDs, and policy evaluation results logged to Write-Once-Read-Many (WORM) compliant tamper-evident storage with $\ge 6$-month retention
