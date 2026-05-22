---
name: plan-technical-delivery
description: Turn architecture decisions and requirements into a delivery-ready technical plan with slices, quality gates, impact radius, and rollout notes. Use when Technical Lead breaks down implementation work for developers, QA, and release.
---

# Plan Technical Delivery

Use with the **Technical Lead** role after requirements and architecture inputs exist.

## Core Rules

- preserve business and system behavior called out in feature-ticket.json and adr-spec.json
- slice work so each piece is reviewable and testable independently when possible
- name impact_radius modules, shared logic, and regression-prone areas explicitly
- define quality_gates matching change risk — not schedule pressure
- emit `contracts/schemas/technical-delivery-plan.json` for machine handoff
- do not implement production code — delegate slices to developer roles

## Suggested Process

### 1. Ingest Constraints

Read feature-ticket.json, adr-spec.json, and any UX/API specs. List non-negotiables: accepted ADR, scope boundaries, and rollout constraints.

### 2. Decompose Slices

Break work into independently reviewable slices with owners, dependencies, and acceptance signals. Order by dependency and risk.

### 3. Define Impact And Gates

Document impact_radius (modules, shared logic, regression-prone areas). Set quality_gates per slice — tests, review depth, staging checks — proportional to risk.

### 4. Plan Rollout And Docs

Note rollout/rollback steps and documentation_deltas for Technical Writer. Flag slices that need Coordinator sequencing.

### 5. Emit Plan

Validate and output `contracts/schemas/technical-delivery-plan.json`. Hand off to developers, QA, and Reviewer with explicit slice references.

## Inputs

- `contracts/schemas/feature-ticket.json` from Business Analyst
- `contracts/schemas/adr-spec.json` from Technical Architect
- `contracts/schemas/ux-flow-spec.json` and component specs when UI is in scope
- `contracts/schemas/api-contract-spec.json` when API work is in scope
- `contracts/schemas/implementation-result.json` from developers when updating readiness

## Role Boundaries

| Role | Owns |
| ---- | ---- |
| Technical Lead | This plan, slices, gates, readiness |
| Technical Architect | adr-spec.json, boundaries |
| Reviewer | code-review-finding disposition |
| QA Engineer | test-report.json, validation-result.json |
| Agent Coordinator | coordination-plan.json phase graph |

## Checklist

- [ ] adr and ticket constraints reflected in slices
- [ ] dependencies and owners explicit
- [ ] impact_radius and rollback documented
- [ ] documentation_deltas listed for Technical Writer
- [ ] technical-delivery-plan.json valid

## Related Skills

- **review-code**: Validate implementation against plan
- **review-service**: Service-level readiness
- **agent-delegation**: Assign slices to specialist roles
- **write-documentation**: Downstream doc work — Technical Writer role
