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
- **CVSS 4.0**: Score vulnerabilities using CVSS 4.0 with CVSS-BTE nomenclature distinguishing Vulnerable System (VC/VI/VA) from Subsequent Systems (SC/SI/SA); MSS (Supplemental) metrics include Automatable and Recovery. Translate to P0/P1/P2/P3 severity tiers.
- **OWASP Top 10:2025 A10**: A10:2025 is "Mishandling of Exceptional Conditions" — audit error-handling paths and exception blocks; ensure fail-closed behavior (deny by default on uncaught exceptions, release DB connections, no stack trace leakage).
- **OWASP ASI01–10**: For agentic AI systems apply all 10 ASI controls: ASI01 Prompt Injection, ASI02 Agent Impersonation, ASI03 Excessive Agency, ASI04 Supply Chain, ASI05 Insecure Output Handling, ASI06 Data Leakage, ASI07 Cascading Delegation, ASI08 Missing HITL, ASI09 Insecure Retrieval, ASI10 Observability Gaps.
- **ZTA-MTLS**: Zero Trust Architecture deployments MUST enforce mTLS between all internal services using SPIFFE/SPIRE for workload identity issuance; block any service-to-service communication without a valid SVID.

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

## Checklist

- [ ] trust boundary identified
- [ ] sensitive data paths reviewed
- [ ] auth and validation checked
- [ ] secret handling checked
- [ ] runtime exposure checked
- [ ] findings reported with clear severity using CVSS 4.0 BTE nomenclature
- [ ] OWASP Top 10:2025 gaps reviewed (A03 Supply Chain, A10 Exceptional Conditions, Misconfiguration)
- [ ] OWASP ASI01–10 checks applied for agentic AI systems
- [ ] ZTA mTLS / SPIFFE/SPIRE verification for zero-trust deployments
- [ ] SLSA Level 3 supply chain integrity checked for production builds

## Related Skills

- **review-code**: Review concrete code changes with broader quality checks
- **review-service**: Expand into full release-readiness review
- **manage-secrets**: Fix secret-handling issues safely
- **meeting-review**: Run a broader multi-role risk review
- **commit-code**: Prepare remediation changes for delivery

## Output Contracts

- `contracts/schemas/security-audit.json`
