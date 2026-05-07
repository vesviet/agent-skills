---
name: analyze-business-requirements
description: Analyze and write business requirements by making actors, business rules, state transitions, exceptions, preserved behavior, and downstream process impact explicit. Use when a feature, policy change, or bug fix needs implementation-ready requirements and testable acceptance criteria.
---

# Analyze Business Requirements

Use this skill when business needs, bug behavior, or process expectations must be turned into clear, testable requirements.

## Core Rules

- write requirements as observable behavior, not implementation guesses
- make actors, permissions, rules, and exceptions explicit
- define current versus target behavior clearly
- identify downstream teams, approvals, or systems affected by the change
- do not let ambiguous business intent pass through as an engineering problem

## Suggested Process

### 1. Frame The Business Problem

Clarify:

- what process, behavior, or rule is under analysis
- who the actors are
- what outcome is expected
- whether the task restores old behavior or introduces new behavior

### 2. Identify Rules And Exceptions

Capture:

- business rules
- approval or permission rules
- edge cases and exception paths
- state transitions or lifecycle steps

### 3. Trace Process Impact

Name what else is affected:

- downstream teams or systems
- compliance or audit expectations
- data or reporting touchpoints
- operational handoffs or manual steps

### 4. Write Testable Acceptance Criteria

Express:

- primary success scenarios
- negative and exception cases
- observable outputs
- preserved constraints

### 5. Package For Delivery

Produce a brief that downstream roles can use directly:

- Technical Lead gets implementation-ready rules
- UX gets clear actors and flow logic
- QA gets observable acceptance cases

## Output Format

```markdown
# <Topic> - Business Analysis Brief

## Business Context
- Problem:
- Actors:
- Outcome:
- Existing behavior to preserve or change:

## Requirements
- Functional requirements:
- Business rules:
- Permissions / approvals:
- Non-goals:

## Acceptance Criteria
- Primary scenarios:
- Negative or exception cases:
- Observable outputs:

## Process Impact
- Current flow:
- Target flow:
- Affected downstream teams or systems:

## Open Questions
- ...
```

## Checklist

- [ ] problem, actors, and expected outcome defined
- [ ] preserved versus changed behavior stated
- [ ] business rules and exceptions captured
- [ ] downstream process impact identified
- [ ] acceptance criteria made observable
- [ ] open questions surfaced before implementation

## Related Skills

- **write-product-brief**: Supply product intent and scope boundaries
- **design-ux-flow**: Turn requirements into user-facing interaction flow
- **meeting-review**: Resolve conflicting assumptions or policies
- **write-documentation**: Capture finalized terminology or process guidance
- **review-service**: Validate whether implementation still matches the intended process
