---
name: manage-secrets
description: Add, update, rotate, or review secret handling by following the repo's source-of-truth, access-control, and rollout patterns. Use when code or deployment work touches credentials, tokens, keys, or sensitive configuration.
---

# Manage Secrets

Use this skill when a change involves creating, rotating, wiring, or auditing secrets and other sensitive configuration.

## Core Rules

- never place real secret values in source-controlled user-visible artifacts unless the repo explicitly stores encrypted secret material that way
- treat secret creation, rotation, consumption, and rollback as separate concerns
- follow the repo's source of truth for secret storage and delivery
- minimize secret exposure in logs, examples, screenshots, and commits
- verify runtime consumers can read the updated secret before treating the change as complete

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

## Checklist

- [ ] secret boundary identified
- [ ] local secret pattern reviewed
- [ ] source-of-truth update applied
- [ ] rollout and rollback checked
- [ ] runtime validation completed safely
- [ ] sensitive values not exposed in artifacts

## Related Skills

- **setup-deployment**: Wire secret references into deployment config
- **security-audit**: Review blast radius and access risk
- **debug-runtime-platform**: Diagnose secret injection or permission issues
- **review-service**: Check release readiness for secret changes
- **commit-code**: Prepare safe, non-sensitive changes for delivery
