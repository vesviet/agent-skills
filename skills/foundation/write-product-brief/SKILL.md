---
name: write-product-brief
description: Write or refine a product brief that makes user value, business outcome, preserved behavior, affected users, acceptance boundaries, and trade-offs explicit. Use when a feature, bug fix, workaround, rollback, or scope decision needs a product-facing decision artifact before implementation or release.
---

# Write Product Brief

Use this skill when product direction needs to be turned into a decision-ready brief that engineering, QA, UX, and stakeholders can act on without guessing.

## Core Rules

- define the user or business outcome before discussing implementation
- make preserved versus changed behavior explicit
- identify affected users, workflows, and support impact
- make trade-offs explicit when scope, quality, timing, or rollback options conflict
- do not hide uncertainty, accepted degradation, or residual release risk

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

## Checklist

- [ ] user or business outcome defined
- [ ] work type and preserved behavior identified
- [ ] affected users or workflows named
- [ ] scope boundaries made explicit
- [ ] acceptance and trade-offs captured
- [ ] risks and next owner stated

## Related Skills

- **meeting-review**: Stress-test the brief through cross-functional trade-offs
- **analyze-business-requirements**: Turn the brief into testable requirements
- **design-ux-flow**: Translate the brief into user journeys and interaction rules
- **review-service**: Judge whether release readiness matches the brief
- **write-documentation**: Turn the brief into durable product or release notes
