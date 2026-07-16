---
name: analyze-business-requirements
description: Analyze and write business requirements by making actors, business rules, state transitions, exceptions, preserved behavior, and downstream process impact explicit. Use when a feature, policy change, or bug fix needs implementation-ready requirements and testable acceptance criteria.
---

# Analyze Business Requirements

Use this skill when business needs, bug behavior, or process expectations must be turned into clear, testable requirements.

## When to Use

- a feature/policy change needs requirements
- making actors, rules, state transitions explicit
- defining testable acceptance criteria
- capturing preserved behavior + downstream impact

## Core Rules

- write requirements as observable behavior, not implementation guesses
- make actors, permissions, rules, and exceptions explicit
- define preserved_behavior versus changed_behavior clearly
- identify downstream teams, approvals, or systems affected by the change
- populate `contracts/schemas/feature-ticket.json` when machine handoff is required
- embed `analytics_request` or `seo_content_request` in the ticket when delegating — do not duplicate specialist deliverables in prose only
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

- business rules (structured in ticket `business_rules[]` when using JSON)
- approval or permission rules
- edge cases and exception paths
- state transitions or lifecycle steps

### 3. Trace Process Impact

Name what else is affected:

- downstream teams or systems (`process_impact`)
- compliance or audit expectations
- data or reporting touchpoints
- operational handoffs or manual steps

### 4. Delegate Before Locking AC (when needed)

| Signal | Delegate to | Ticket field / section |
| ------ | ------------- | ---------------------- |
| Unknown domain, policy, market | Researcher | Research Request → research-report.json |
| Metrics, baselines, funnel counts | Data Analyst | analytics_request → data-analysis-report.json |
| Content discoverability, CTA, linking | SEO Analyst | seo_content_request → seo-content-brief.json |

Do not lock metric-heavy or compliance-heavy AC until delegated artifacts return or risk is explicitly accepted.

### 5. Write Testable Acceptance Criteria

Express:

- primary success scenarios
- negative and exception cases
- observable outputs
- preserved constraints

### 6. Package For Delivery

Produce:

- `contracts/schemas/feature-ticket.json` for Technical Lead, QA, and coordinator handoffs
- markdown brief when JSON is not required (still mirror ticket sections)

## Output Format

```markdown
# <Topic> - Business Analysis Brief

## Business Context
- Problem:
- Actors:
- Outcome:
- Preserved behavior:
- Changed behavior:

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

## Research Request (optional)
## Analytics Request (optional)
## SEO Content Request (optional)
```

See `core/roles/business-analyst.md` for full handoff rules for Researcher, Data Analyst, and SEO Analyst.

## Checklist

- [ ] problem, actors, and expected outcome defined
- [ ] preserved versus changed behavior stated
- [ ] business rules and exceptions captured
- [ ] downstream process impact identified
- [ ] acceptance criteria made observable
- [ ] open_questions listed
- [ ] Research / Analytics / SEO requests issued when triggers apply
- [ ] feature-ticket.json valid when JSON handoff is required

## Related Skills

- **write-product-brief**: Supply product intent and scope boundaries from PM
- **conduct-research**: Light discovery only; deep work stays with Researcher role
- **design-ux-flow**: Turn requirements into user-facing interaction flow
- **meeting-review**: Resolve conflicting assumptions or policies
- **write-documentation**: Capture finalized terminology or process guidance
- **review-service**: Validate whether implementation still matches the intended process
\n### 2026: AI-Assisted Requirements Analysis

- **LLM-as-judge validation for AI-assisted AC:** When acceptance criteria were generated or refined with LLM assistance, validate using an independent LLM-as-judge evaluation (DeepEval, RAGAS) scoring for clarity, completeness, and internal consistency. AI-generated AC can pass human review while containing subtle contradictions.
- **Living requirements traceability:** Link requirements to design docs, code modules, and test cases using AI-assisted traceability tools (Trace.space, getleo.ai). This is especially critical for EU AI Act compliance and regulated industries requiring chain-of-causality audit trails.
- **Agentic AC format:** When the downstream delivery involves AI agents, write acceptance criteria as deterministic, observable assertions (not prose intent) so agents can auto-validate implementation output.\n