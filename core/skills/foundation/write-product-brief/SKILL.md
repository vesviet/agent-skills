---
name: write-product-brief
description: Write or refine a product brief that makes user value, business outcome, preserved behavior, affected users, acceptance boundaries, and trade-offs explicit. Use when a feature, bug fix, workaround, rollback, or scope decision needs a product-facing decision artifact before implementation or release.
---

# Write Product Brief

Use this skill when product direction needs to be turned into a decision-ready brief that engineering, QA, UX, and stakeholders can act on without guessing.

## When to Use

- a feature/bugfix needs a decision artifact
- defining user value + business outcome
- setting acceptance boundaries and trade-offs
- before implementation or release

## Core Rules

- define the user or business outcome (Jobs-to-be-Done / underserved customer job) before discussing implementation — Feature Factory PRDs that specify buttons and database fields without a user problem are an anti-pattern
- measure success by customer behavior change and business outcome, not by shipped feature count or schedule compliance
- make preserved versus changed behavior explicit
- identify affected users, workflows, and support impact
- define explicit non-goals to prevent scope creep — unclear non-goals are a P1 defect in the brief
- make trade-offs explicit when scope, quality, timing, or rollback options conflict
- do not hide uncertainty, accepted degradation, or residual release risk
- for AI-backed features: include EU AI Act risk classification (Prohibited / High-Risk / Limited / Minimal) before any acceptance criteria — high-risk classification changes the delivery contract and requires conformity assessment
- for AI-backed features: state HITL requirement explicitly (trigger conditions, human gate scope); define AI transparency disclosure mechanism (label, tooltip, watermark) per EU AI Act Articles 50-52
- for AI-backed features: define deterministic fallback behavior when the AI component fails or returns low-confidence output — "fail-open" (show AI output regardless) is not acceptable for High-Risk features
- for AI-backed features: specify model version, data provenance (training corpus, geographic restrictions, PII flags), and model update cadence controls

## Suggested Process

### 1. Define The Decision

Clarify:

- what problem or opportunity is being addressed
- whether this is a feature, bug fix, workaround, rollback, or release decision
- what outcome must be achieved
- what behavior must remain stable

### 2. Gather Product Evidence

Collect only the signal needed:

- user feedback or support cases
- analytics or adoption indicators
- engineering constraints or delivery risk
- affected customer segments, roles, or commitments

### 3. Set Scope Boundaries

State:

- what is in scope
- what is explicitly out of scope
- what assumptions the decision depends on
- what changes are acceptable and what changes are not

### 4. Define Acceptance And Trade-Offs

Write:

- success metrics or outcome signals
- acceptance criteria or release acceptance
- negative cases or degraded modes that are still acceptable
- what gives way first if time, quality, or complexity conflict

### 5. Produce A Handoff-Ready Brief

Leave a brief that downstream roles can use directly:

- Product and BA can refine requirements from it
- UX can design from it
- Technical Lead can plan from it
- QA can derive validation scope from it

## Output Format

```markdown
# <Topic> - Product Brief

## Objective
- User or business goal:
- Success metric:
- Preserved behavior:

## Scope
- In scope:
- Out of scope:
- Assumptions:
- Affected users, roles, or journeys:

## Acceptance
- Success criteria:
- Negative or exception cases:
- Release or rollback acceptance:

## Trade-Offs
- Options considered:
- Recommended path:
- What gives way first if constraints tighten:

## Handoff
- Risks:
- Open questions:
- Next owner:
```

## Output Contracts

When the brief is intended as the intake artifact for Solution Architect or Technical Architect, emit a machine-readable twin so the next role can consume it without re-typing:

- **`contracts/schemas/solution-brief.json`** — emit when the brief describes a problem that needs architecture or solutioning (as opposed to a pure product/scope decision). Map directly from the markdown sections: `objective` ← Objective, `preserved_behavior` ← Objective → Preserved behavior, `in_scope` / `out_of_scope` ← Scope, `affected_users` ← Scope → Affected users, `acceptance_criteria` ← Acceptance → Success criteria, `trade_offs` ← Trade-Offs, `risks` ← Handoff → Risks. Set `produced_by_role: product-manager` (or whichever role authored the brief) so the architect can route follow-ups.

Skip emission for purely editorial marketing briefs (copy / campaign releases) — those stay as markdown only.

## Checklist

- [ ] user or business outcome defined
- [ ] work type and preserved behavior identified
- [ ] affected users or workflows named
- [ ] scope boundaries made explicit
- [ ] acceptance and trade-offs captured
- [ ] risks and next owner stated
- [ ] when handed to an architect role, matching `solution-brief.json` emitted alongside the markdown brief

## Related Skills

- **meeting-review**: Stress-test the brief through cross-functional trade-offs
- **analyze-business-requirements**: Turn the brief into testable requirements
- **design-ux-flow**: Translate the brief into user journeys and interaction rules
- **review-service**: Judge whether release readiness matches the brief
- **write-documentation**: Turn the brief into durable product or release notes
