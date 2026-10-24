# Meeting Review — Reference

Deep material extracted from `SKILL.md` to keep the main file under 200
lines. Load this file when running a structured review, when selecting
perspectives, or when authoring a deliverable decision.

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

## Deliverable Decision

This skill should produce something that another role can use directly, not just a conversational debate recap. Aim to leave behind one of these:

- a go / no-go recommendation
- a bug-fix direction
- a feature-scope decision
- a release-risk decision
- a refactor recommendation with trade-offs
