---
name: manage-secrets
description: Add, update, rotate, or review secret handling by following the repo's source-of-truth, access-control, and rollout patterns. Use when code or deployment work touches credentials, tokens, keys, or sensitive configuration.
---

# Manage Secrets

Use this skill when a change involves creating, rotating, wiring, or auditing secrets and other sensitive configuration.

## When to Use

- code/deploy touches credentials or tokens
- adding, updating, or rotating keys
- reviewing secret access control
- sensitive configuration rollout

## Core Rules

- never place real secret values in source-controlled user-visible artifacts unless the repo explicitly stores encrypted secret material that way
- treat secret creation, rotation, consumption, and rollback as separate concerns
- follow the repo's source of truth for secret storage and delivery
- minimize secret exposure in logs, examples, screenshots, and commits
- verify runtime consumers can read the updated secret before treating the change as complete
- prefer dynamic, short-lived credentials via OIDC workload identity federation (e.g., GitHub Actions to Vault/OpenBao, GCP Workload Identity, AWS IRSA) over static, long-lived access keys in CI/CD and deployments
- mitigate the elevated risk (2× secrets leakage rate) in AI-assisted code generation by enforcing automated pre-commit and CI pipeline scanning using Gitleaks or TruffleHog
- evaluate secret storage provider choices (e.g., OpenBao vs. HashiCorp Vault) against the organization's governance policies, licensing models (MPL vs. BSL), and migration/support requirements

## Suggested Process

### 1. Identify The Secret Boundary

Clarify:

- what secret or credential is changing
- which systems produce and consume it
- where the source of truth lives
- what environments are affected

### 2. Inspect Existing Secret Patterns

Look for:

- secret naming conventions
- storage mechanism
- environment wiring
- access or permission model
- rotation or expiration rules

### 3. Apply The Smallest Safe Change

Examples:

- add a new secret reference
- rotate an existing credential
- update a secret mount or env var mapping
- remove unused secret consumption

Do not expand secret scope or audience unless required.

### 4. Check Rollout And Recovery

Verify:

- consumers can tolerate old and new credentials during rollout if needed
- restart or refresh behavior is understood
- revocation or rollback path is clear
- operational owners know if manual steps are required

### 5. Validate Safely

Confirm without exposing values:

- the secret reference resolves correctly
- the application starts and authenticates
- dependent calls succeed
- no sensitive value appears in logs or docs

## 2026 Secrets Management Patterns

### 2026: OIDC Workload Identity Federation

When designing or auditing deployment workflows:

- **Configure OIDC Trust:** Establish trust relationships between the CI/CD platform (e.g., GitHub Actions) and the cloud provider or secrets manager (AWS, GCP, Vault/OpenBao). Avoid storing static IAM credentials.
- **Enforce Claims Constraints:** Restrict token exchange by specifying claims filters (e.g., matching the exact GitHub organization, repository, branch, or environment) to prevent unauthorized repositories from obtaining credentials.
- **Implement Temporary Token Exchange:** Use dynamic credential retrieval in pipeline steps, requesting short-lived session tokens that automatically expire after the job finishes.

### 2026: AI-Generated Code Secrets Scanning

To combat the 2× increase in secrets leakage rates when developers use AI coding assistants:

- **Enforce Pre-Commit Scanning:** Wire automated scanners (Gitleaks, TruffleHog) into local pre-commit hooks to detect credentials before commits are made.
- **Run Scan in CI/CD:** Establish a mandatory blocking CI check on all Pull Requests to analyze the commit history for high-entropy strings and known signature patterns.
- **Execute Active Verification:** Use scanner features (like TruffleHog's verification engines) to check if any flagged credentials are active in the target APIs before initiating rotation protocols.

### 2026: OpenBao vs HashiCorp Vault Governance

When choosing or transitioning secret management infrastructure:

- **Analyze Licensing:** Understand the licensing implications of the solution (OpenBao's fully open-source MPL v2 vs. HashiCorp Vault's BSL v1.1) relative to organization usage and redistributions.
- **Assess Feature Parity:** Verify API compatibility (OpenBao remains compatible with Vault up to 1.14.x) and catalog any proprietary features that could cause vendor lock-in.
- **Establish Migration Strategy:** Plan the transition path (APIs, mounts, auth backends, and policies) to ensure zero downtime if migrating between Vault and OpenBao.

## Checklist

- [ ] secret boundary identified
- [ ] local secret pattern reviewed
- [ ] source-of-truth update applied
- [ ] rollout and rollback checked
- [ ] runtime validation completed safely
- [ ] sensitive values not exposed in artifacts
- [ ] OIDC workload identity federation configured for pipeline authentication
- [ ] pre-commit and CI/CD secret scanning (Gitleaks/TruffleHog) active for AI-generated code validation
- [ ] governance alignment (OpenBao vs HashiCorp Vault) reviewed and documented

## Related Skills

- **setup-deployment**: Wire secret references into deployment config
- **security-audit**: Review blast radius and access risk
- **debug-runtime-platform**: Diagnose secret injection or permission issues
- **review-service**: Check release readiness for secret changes
- **commit-code**: Prepare safe, non-sensitive changes for delivery
