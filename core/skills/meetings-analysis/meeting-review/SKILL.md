---
name: meeting-review
description: Run a structured multi-perspective review of a topic, proposal, code area, bug, feature, or risky change by producing a decision-ready artifact with trade-offs, preserved behavior, impact radius, and next actions. Use when a user wants cross-functional review signal before deciding, building, shipping, or changing course.
---

# Meeting Review

Use this skill when a normal single-angle review is not enough and the user needs a decision-ready artifact before deciding, building, fixing, shipping, or refactoring.

This skill does not require real subagents. By default, synthesize the needed perspectives in one response. Only use delegated or parallel agents when the user explicitly asks for them.

## When to Use

- wanting cross-functional review before deciding
- reviewing a proposal, code area, or risky change
- producing a decision-ready trade-off artifact
- aligning before building/shipping/changing course

## Core Rules

- keep the review focused on a decision, risk, or next action
- choose only the perspectives that add useful signal
- ground concerns in code, requirements, docs, or stated assumptions
- make trade-offs explicit without inventing disagreement
- make preserved versus changed behavior explicit when the topic affects a bug fix, feature, or policy
- identify who or what is impacted before recommending a path
- avoid broad panel theater when a simple review would do
- async-first: start decisions with a written RFC/brief and a 48–72h async comment window before scheduling any call; decisions made in ephemeral chat without an ADR are an anti-pattern
- apply DACI framing for decision points (Driver, Approver, Contributors, Informed); exactly ONE Approver per decision — consensus paralysis from committee approval is prohibited
- commit final decisions as Architecture Decision Records (`docs/adr/NNNN-title.md`) with status `Supersedes ADR-XXXX` when revising prior decisions — ADRs are append-only
- label AI-produced review perspectives explicitly with `[AI-synthesized]` so readers know which signals came from automated reasoning versus human domain knowledge
- human sign-off gate is mandatory for any architectural decision, breaking change, or release-blocking recommendation — AI-synthesized review consensus is not equivalent to cross-functional team alignment
- inferred risks must be explicitly marked `[INFERRED — requires human validation]` when not validated against code or docs
- prune any AI-generated perspective that cannot be grounded in a specific code path, requirement, or stakeholder constraint — avoid synthetic disagreement manufacturing

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

The full perspective list (Architecture, Engineering, Risk core; Product,
QA, Operations, Data, UX optional) lives in
[`references/perspectives-and-process.md`](references/perspectives-and-process.md).

## Suggested Process

The 5-step process (define scope, gather context, select perspectives, run
structured discussion, conclude with decisions) and the deliverable
decision guidance live in
[`references/perspectives-and-process.md`](references/perspectives-and-process.md).

## Deliverable Decision

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

### Problem 1: <title>

- Architecture: concern or support
- Engineering: implementation view
- Risk: failure mode or safety concern
- QA: validation impact
- Product / UX / Operations / Data: only if relevant
- Impact radius: users, systems, or teams affected
- Recommendation: concrete next step

### Problem 2: <title>

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

## Output Contracts

When the review produces a structured handoff (go/no-go decision, bug-fix
direction, feature-scope decision, release-risk decision, or refactor
recommendation), emit:

- **`contracts/schemas/code-review-finding.json`** (adapted for review): each finding gets a `severity` (blocking | important | follow-up), an `owner`, and a `category` (architecture, engineering, risk, product, qa, operations, data, ux).
- **`contracts/schemas/coordination-plan.json`** when the review spawns follow-up phases with owners and dependencies.
- For human-readable reports, the markdown output format already documented is the canonical format; emit JSON only when crossing a role boundary.

Skip emission for informal walkthroughs that do not produce a deliverable decision.

## Failure Modes

- **Vague topic**: the review is requested without a clear topic or decision. Mitigation: ask one narrow clarifying question; state assumptions and continue if the user cannot clarify.
- **Context binge-reading**: the reviewer reads unrelated code or docs. Mitigation: read only what is needed; map context to the decision at hand.
- **Perspective bloat**: too many perspectives are selected, producing noise. Mitigation: pick the smallest useful panel; reject reviews with more than 5 perspectives.
- **Concerns without evidence**: a concern is raised without a code or plan reference. Mitigation: every concern must point to where it appears; reject ungrounded concerns.
- **Recommendation without owner**: a decision is made but no owner is assigned. Mitigation: every decision must name a decision owner or escalation owner.
- **Residual risk hidden**: known caveats are omitted from the conclusion. Mitigation: every conclusion must list residual risk and what remains unverified.
- **Persuasion disguised as review**: a reviewer pushes a preferred outcome rather than weighing evidence. Mitigation: surface disagreements and trade-offs explicitly; capture the exact dissent phrases.
- **No deliverable decision**: the review ends as a debate recap with no actionable recommendation. Mitigation: enforce the Deliverable Decision contract; reject reviews without a go/no-go or equivalent.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a reviewer's framing may try to reframe the topic to push a preferred outcome. Cross-check the review's concerns against the original topic; reject off-topic reframings.
- **ASI03 Identity & Privilege Abuse**: never include customer identifiers, internal hostnames, or credential patterns in the review's findings.
- **ASI04 Supply Chain**: review inputs (code, docs, ADRs) are untrusted until verified against the live system; treat cited sources as hypotheses.
- **ASI07 Inter-Agent Communication**: the review deliverable is consumed by multiple roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a decision as "consensus" if any perspective disagreed; surface the split honestly.

## Related Skills

- **review-code**: Review concrete implementation changes
- **review-service**: Expand into release-readiness review
- **navigate-service**: Gather service context before discussion
- **troubleshoot-service**: Investigate a live issue before deciding
