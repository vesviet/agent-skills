---
name: meeting-review
description: Run a structured multi-perspective technical review of a topic, proposal, code area, or risky change. Use when a user wants a discussion-style review that combines architecture, delivery, quality, product, security, or operations perspectives.
---

# Meeting Review

Use this skill when a normal single-angle review is not enough and the user wants a broader discussion before deciding, building, or refactoring.

This skill does not require real subagents. By default, simulate a disciplined review panel in one response. Only use delegated or parallel agents when the user explicitly asks for them.

## Core Rules

- keep the review focused on a decision, risk, or next action
- choose only the perspectives that add useful signal
- ground concerns in code, requirements, docs, or stated assumptions
- make trade-offs explicit without inventing disagreement
- avoid broad panel theater when a simple review would do

## When To Use

- architecture or design reviews
- large refactors
- risky implementation plans
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

If the request is too vague, ask one narrow clarifying question. Otherwise, state the assumptions and continue.

### 2. Gather Context

Read only what is needed:

- the key code paths
- related config or migration files
- contracts or interfaces
- docs, ADRs, or review notes if they exist

### 3. Select Perspectives

Pick the smallest useful panel. Examples:

- feature design: Product + Architecture + Engineering + QA
- performance issue: Engineering + Risk + Operations + Data
- release hardening: Engineering + Risk + QA + Operations
- schema change: Architecture + Engineering + Data + QA

### 4. Run A Structured Discussion

For each major issue:

- present the concern
- show where it appears in the code or plan
- summarize each perspective briefly
- call out disagreements or trade-offs explicitly
- end with a recommendation

### 5. Conclude With Decisions

Finish with:

- key findings
- decisions or recommendations
- open questions
- next actions

## Output Format

```markdown
# Meeting Review: <topic>

## Scope

- what is being reviewed
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
- Recommendation: concrete next step

### Issue 2: <title>

- ...

## Summary

- strongest reasons to proceed
- strongest reasons to change course
- final recommendation

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

## Checklist

- [ ] topic and decision under review identified
- [ ] scope and assumptions stated
- [ ] relevant context gathered
- [ ] useful perspectives selected
- [ ] major concerns and trade-offs discussed
- [ ] recommendation and next actions captured

## Related Skills

- **review-code**: Review concrete implementation changes
- **review-service**: Expand into release-readiness review
- **navigate-service**: Gather service context before discussion
- **troubleshoot-service**: Investigate a live issue before deciding
