---
name: plan-technical-delivery
description: Turn architecture decisions and requirements into a delivery-ready technical plan with slices, quality gates, impact radius, and rollout notes. Use when Technical Lead breaks down implementation work for developers, QA, and release.
---

# Plan Technical Delivery

Use with the **Technical Lead** role after requirements and architecture inputs exist.

## When to Use

- Technical Lead breaking down implementation work
- producing slices with quality gates
- defining impact radius and rollout notes
- planning for dev/QA/release

## Core Rules

- preserve business and system behavior called out in feature-ticket.json and adr-spec.json
- slice work so each piece is reviewable and testable independently — target ≤400 lines of diff per slice to stay in review-friendly range
- decompose features into thin vertical slices (UI → API → DB) that deliver independent user value — horizontal layer slicing (DB sprint 1, API sprint 2, UI sprint 3) is an anti-pattern
- name impact_radius modules, shared logic, and regression-prone areas explicitly
- define quality_gates matching change risk — not schedule pressure
- emit `contracts/schemas/technical-delivery-plan.json` for machine handoff
- do not implement production code — delegate slices to developer roles
- **Feature flag-first delivery**: every user-visible slice needs flag name, kill-switch, rollout plan (internal → canary → GA), and cleanup target date — permanent flags without retirement schedule are an anti-pattern
- **Hybrid human+agent slice ownership**: specify compute budget, HITL checkpoints, and agent output gates for agent-implemented slices
- **AI estimation with explicit uncertainty bounds**: use three-point estimates (optimistic P10, expected P50, pessimistic P90) rather than point estimates — measure delivery health with DORA (Deployment Frequency, Lead Time, CFR, MTTR) and SPACE (Satisfaction, Performance, Activity, Communication, Efficiency) balanced signals

## Suggested Process

### 1. Ingest Constraints

Read feature-ticket.json, adr-spec.json, and any UX/API specs. List non-negotiables: accepted ADR, scope boundaries, and rollout constraints.

### 2. Decompose Slices

Break work into independently reviewable slices with owners, dependencies, and acceptance signals. Order by dependency and risk. Define whether the slice is owned by an Agent, Human, or Hybrid team, setting up necessary compute budgets and human-in-the-loop checkpoints.

### 3. Define Impact And Gates

Document impact_radius (modules, shared logic, regression-prone areas). Set quality_gates per slice — tests, review depth, staging checks — proportional to risk. Apply three-point AI estimation to each slice, capturing optimistic (P10), expected (P50), and pessimistic (P90) duration bounds with a confidence interval.

### 4. Plan Rollout And Docs

Note rollout/rollback steps and documentation_deltas for Technical Writer. Flag slices that need Coordinator sequencing. For every user-visible slice, design the feature flag configuration (flag name, kill-switch strategy, progressive rollout stages, and cleanup target date).

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
- [ ] every user-visible slice has feature flag name, kill-switch, rollout plan, and cleanup target date
- [ ] hybrid slices have compute budgets, HITL checkpoints, and agent output gates defined
- [ ] all slices estimated with explicit uncertainty bounds (optimistic, expected, pessimistic)
- [ ] documentation_deltas listed for Technical Writer
- [ ] technical-delivery-plan.json valid

## Related Skills

- **review-code**: Validate implementation against plan
- **review-service**: Service-level readiness
- **agent-delegation**: Assign slices to specialist roles
- **write-documentation**: Downstream doc work — Technical Writer role

## Output Contracts

- `contracts/schemas/technical-delivery-plan.json`

