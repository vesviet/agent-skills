---
name: meeting-review
description: Run a structured multi-perspective review of a topic, proposal, code area, bug, feature, or risky change by producing a decision-ready artifact with trade-offs, preserved behavior, impact radius, and next actions. Use when a user wants cross-functional review signal before deciding, building, shipping, or changing course.
---

# Meeting Review

Use this skill when a normal single-angle review is not enough and the user needs a decision-ready artifact before deciding, building, fixing, shipping, or refactoring.

This skill does not require real subagents. By default, synthesize the needed perspectives in one response. Only use delegated or parallel agents when the user explicitly asks for them.

## Core Rules

- keep the review focused on a decision, risk, or next action
- choose only the perspectives that add useful signal
- ground concerns in code, requirements, docs, or stated assumptions
- make trade-offs explicit without inventing disagreement
- make preserved versus changed behavior explicit when the topic affects a bug fix, feature, or policy
- identify who or what is impacted before recommending a path
- avoid broad panel theater when a simple review would do

## When To Use

- architecture or design reviews
- large refactors
- risky implementation plans
- bug triage or bug-fix direction reviews
- feature scope or acceptance reviews
- release-readiness discussions
- technical debt prioritization
- cross-functional trade-off discussions

## Review Perspectives

Choose only the perspectives that fit the topic.

### Core Perspectives

- Architecture: boundaries, coupling, long-term maintainability
- Engineering: implementation quality, simplicity, testability
- Risk: security, performance, reliability, rollout risk

### Optional Perspectives

- Product: user value, scope, and business trade-offs
- QA: regression risk, test coverage, validation strategy
- Operations: deployability, observability, recovery, runbook impact
- Data: schema, migration, indexing, consistency, retention
- UX: interaction clarity, accessibility, flow friction

## Suggested Process

### 1. Define Scope

Identify:

- the topic or decision under review
- the files, modules, or systems in scope
- the decision the user is trying to make
- what behavior must stay stable
- what may change if the recommendation is accepted

If the request is too vague, ask one narrow clarifying question. Otherwise, state the assumptions and continue.

### 2. Gather Context

Read only what is needed:

- the key code paths
- related config or migration files
- contracts or interfaces
- docs, ADRs, or review notes if they exist
- user-facing requirements, acceptance criteria, or bug reports when relevant

### 3. Select Perspectives

Pick the smallest useful panel. Examples:

- feature design: Product + Architecture + Engineering + QA
- performance issue: Engineering + Risk + Operations + Data
- release hardening: Engineering + Risk + QA + Operations
- schema change: Architecture + Engineering + Data + QA
- bug-fix direction: Product + Engineering + QA + Risk
- UX-sensitive behavior change: Product + UX + Engineering + QA

### 4. Run A Structured Discussion

For each major issue:

- present the concern
- show where it appears in the code or plan
- summarize each perspective briefly
- call out disagreements or trade-offs explicitly
- state affected users, systems, or downstream teams when relevant
- end with a recommendation

### 5. Conclude With Decisions

Finish with:

- key findings
- decisions or recommendations
- decision owner or escalation owner when needed
- residual risk and what remains unverified
- open questions
- next actions

## Output Artifact Guidance

This skill should produce something that another role can use directly, not just a conversational debate recap.

Aim to leave behind one of these:

- a go / no-go recommendation
- a bug-fix direction
- a feature-scope decision
- a release-risk decision
- a refactor recommendation with trade-offs

## Output Format

```markdown
# Meeting Review: <topic>

## Scope

- what is being reviewed
- work type (bug / feature / design / release / refactor)
- preserved behavior or constraint
- assumptions if any

## Panel

- Architecture
- Engineering
- Risk
- QA

## Discussion

### Issue 1: <title>

- Architecture: concern or support
- Engineering: implementation view
- Risk: failure mode or safety concern
- QA: validation impact
- Product / UX / Operations / Data: only if relevant
- Impact radius: users, systems, or teams affected
- Recommendation: concrete next step

### Issue 2: <title>

- ...

## Decision

- Recommended path:
- Why this path:
- What stays stable:
- What changes:
- Decision owner or escalation owner:

## Risks

- strongest reasons to proceed
- strongest reasons to change course
- residual risk or unverified assumptions

## Next Actions

1. action
2. action
3. action
```

## Guardrails

- do not invent disagreement when none exists
- do not simulate fake certainty when the evidence is weak
- do not use broad panel theater when a simple review would do
- do not let the discussion drift away from a decision or action
- do not end with "it depends" unless the missing decision owner or evidence is stated explicitly
- do not recommend change without naming impact radius when it is broader than one file or one team

## Checklist

- [ ] topic and decision under review identified
- [ ] preserved behavior or hard constraint identified
- [ ] scope and assumptions stated
- [ ] relevant context gathered
- [ ] useful perspectives selected
- [ ] major concerns and trade-offs discussed
- [ ] impact radius identified where relevant
- [ ] recommendation and next actions captured

## Related Skills

- **review-code**: Review concrete implementation changes
- **review-service**: Expand into release-readiness review
- **navigate-service**: Gather service context before discussion
- **troubleshoot-service**: Investigate a live issue before deciding
