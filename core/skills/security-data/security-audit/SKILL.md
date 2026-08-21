---
name: security-audit
description: Review code, configuration, and service behavior for security risks by checking trust boundaries, secret handling, auth, validation, and operational exposure. For AI/ML systems, apply OWASP ASI Top 10 2026 (ASI01–ASI10), NIST AI RMF Measure function, and ISO/IEC 42001:2023 controls assessment. Use for focused security review of changes or full-service risk assessment.
---

# Security Audit

Use this skill when reviewing a change, service, or deployment for security posture and obvious risk.

## When to Use

- focused security review of a change
- full-service risk assessment
- checking trust boundaries, secrets, auth, validation
- AI/ML review via OWASP ASI + NIST + ISO 42001

## Core Rules

- focus on real trust boundaries and attack surfaces
- prioritize exploitable risk over checklist theater
- treat code, config, and runtime exposure together
- call out unclear assumptions as risk, not as proof of safety
- avoid exposing real secrets or exploit details unnecessarily in user-visible artifacts

## Suggested Process

### 1. Identify The Security Boundary

Clarify:

- what data is sensitive
- who the actors are
- what external inputs are accepted
- what systems or credentials are trusted

### 2. Review The Main Risk Areas

Check:

- authn and authz
- input validation and output exposure
- secret and credential handling
- logging of sensitive data
- dependency and downstream trust assumptions
- unsafe default configuration or missing environment hardening

### 3. Check Change-Specific Risk

For a concrete change, verify:

- new endpoints or routes are protected appropriately
- new background or event paths do not bypass controls
- new config does not widen exposure unintentionally
- new dependencies are bounded and authenticated as expected

### 4. Check Operational Exposure

Review:

- debug or admin surfaces
- runtime permissions
- public network reachability
- auditability and rollback assumptions

### 5. Report Findings By Severity

Use:

- blocking risk for clear security flaws
- high-severity risk for likely misuse or privilege widening
- follow-up risk for hardening gaps that should be tracked

## 2026 Security Standards

### 2026: OWASP Top 10:2025 Standards

Verify the following 2025 additions during audits:
- **A03: Supply Chain Security**: Enforce Software Bill of Materials (SBOM) generation/validation, verify package signatures, and review third-party code and dependency updates.
- **A10: Exceptional Conditions**: Audit error-handling paths and exception blocks. Ensure systems fail-closed when encountering uncaught exceptions, properly release resources (e.g. database connections), and do not leak stack traces or internal diagnostic data.
- **#2 Misconfiguration (Security Misconfiguration)**: Audit configuration settings, default credentials, cloud IAM/resource policies, HTTP security headers, and debug endpoint states to ensure environments are hardened.

### 2026: OWASP Agentic Security Initiative (ASI) Top 10

Analyze vulnerabilities unique to agentic and AI systems:
- **Indirect Prompt Injection**: Treat external data (RAG documents, emails, search results) consumed by AI agents as untrusted input; do not allow external data to override system prompts.
- **Insecure Output Handling**: Validate, sanitize, and scope all agentic outputs (e.g. database queries, command lines, API calls) before downstream systems execute them.
- **Excessive Agency & Trust Boundaries**: Enforce the principle of least privilege on tool access and capabilities granted to AI agents.
- **Cascading Delegation & HITL**: Ensure multi-agent invocation paths are bounded and that irreversible actions (such as transactions or data deletions) require Human-in-the-Loop (HITL) approval.

### 2026: SLSA Level 3 Supply Chain Verification

Assess the delivery pipeline for supply chain integrity:
- **Isolated Build Environments**: Confirm that build steps execute on isolated, ephemeral build platforms to prevent cross-build contamination.
- **Non-Falsifiable Provenance**: Verify that the build platform produces cryptographically signed, authenticated provenance metadata (SBOM, source commits) that cannot be altered.
- **Hermetic Builds**: Ensure builds resolve dependencies from secure, immutable registries and that internet access is blocked or tightly restricted during execution.

## Checklist

- [ ] trust boundary identified
- [ ] sensitive data paths reviewed
- [ ] auth and validation checked
- [ ] secret handling checked
- [ ] runtime exposure checked
- [ ] findings reported with clear severity
- [ ] OWASP Top 10:2025 gaps reviewed (A03, A10, #2 Misconfiguration)
- [ ] OWASP ASI Top 10 checks applied for AI systems
- [ ] SLSA Level 3 supply chain verification assessed

## Related Skills

- **review-code**: Review concrete code changes with broader quality checks
- **review-service**: Expand into full release-readiness review
- **manage-secrets**: Fix secret-handling issues safely
- **meeting-review**: Run a broader multi-role risk review
- **commit-code**: Prepare remediation changes for delivery

## Output Contracts

- `contracts/schemas/security-audit.json`

