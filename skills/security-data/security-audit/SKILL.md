---
name: security-audit
description: Review code, configuration, and service behavior for security risks by checking trust boundaries, secret handling, auth, validation, and operational exposure. Use for focused security review of changes or full-service risk assessment.
---

# Security Audit

Use this skill when reviewing a change, service, or deployment for security posture and obvious risk.

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

## Checklist

- [ ] trust boundary identified
- [ ] sensitive data paths reviewed
- [ ] auth and validation checked
- [ ] secret handling checked
- [ ] runtime exposure checked
- [ ] findings reported with clear severity

## Related Skills

- **review-code**: Review concrete code changes with broader quality checks
- **review-service**: Expand into full release-readiness review
- **manage-secrets**: Fix secret-handling issues safely
- **meeting-review**: Run a broader multi-role risk review
- **commit-code**: Prepare remediation changes for delivery
