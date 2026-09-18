---
name: elicit-requirements
description: Elicit business requirements from stakeholders using Funnel Questioning (Open, Probing, Closed), the Colombo Method, and the 9 BABOK v3 requirement quality criteria. Use when scoping ambiguous business needs, conducting stakeholder interviews, uncovering tacit domain knowledge, or validating requirement quality before architecture handoff.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Elicit Requirements

Use this skill to extract, clarify, and validate business requirements from stakeholders and domain experts using disciplined questioning techniques and BABOK v3 quality criteria.

## When to Use

- scoping ambiguous, conflicting, or underspecified business requests
- preparing and running structured stakeholder requirement interviews
- uncovering tacit assumptions and unstated constraints from non-technical stakeholders
- validating requirement drafts against the 9 BABOK v3 quality characteristics
- converting unstructured interview transcripts into atomic, testable business requirements
- applying System 2 reflective pause before locking requirement baselines

## Core Rules

- **Enforce Funnel Questioning Protocol**: structure interviews sequentially through three distinct phases:
  1. *Open-ended phase*: explore domain space, user goals, and current pain points without premature constraints ("How does the team currently handle X?")
  2. *Probing phase*: drill down into edge cases, volumes, exceptions, and business rules ("What happens when an approval exceeds 48 hours?")
  3. *Closed confirmation phase*: lock specific thresholds, states, and acceptance boundaries ("Is 50,000 USD the absolute hard ceiling for Level 2 approval?")
- **Apply the Colombo Method for Tacit Knowledge**: adopt a deliberate, structured curiosity posture to surface hidden assumptions; ask "naive" boundary questions that force stakeholders to articulate unwritten organizational habits and tribal knowledge
- **Mandate 9 BABOK v3 Requirement Quality Criteria**: every requirement item must pass the 9 characteristics:
  - *Atomic*: captures a single requirement, never joined with compound "and/or" clauses
  - *Complete*: includes context, preconditions, error states, and measurable outcomes
  - *Consistent*: zero contradictions with existing policy or neighboring requirements
  - *Concise*: free from superfluous prose, marketing jargon, or redundant phrasing
  - *Feasible*: technically achievable within architectural, cost, and time constraints
  - *Unambiguous*: allows exactly one interpretation by engineering and QA
  - *Testable*: verifiable through deterministic assertions or explicit probabilistic thresholds
  - *Prioritized*: tagged with a quantifiable priority score (MoSCoW or WSJF)
  - *Understandable*: clear to both domain business sponsors and technical implementers
- **Trigger System 2 Reflective Pause**: before outputting requirement specifications, the agent must execute a reflective self-check:
  - *Did I hallucinate or assume unstated business logic?*
  - *Are numerical targets backed by cited data or verified reports?*
  - *Are exception paths fully specified or merely hinted at?*
- **Ban Implementation Prescription**: specify *what* the business needs and *why*, never prescribe database schemas, programming frameworks, or UI widget internals unless explicitly mandated as architectural constraints
- Detailed techniques and templates: [`references/elicitation-techniques-and-babok-criteria.md`](references/elicitation-techniques-and-babok-criteria.md)

## Suggested Process

### 1. Profile Stakeholders & Frame Objectives
Map interview participants, their organizational roles, decision authority, and primary concerns. Define the elicitation scope, business outcome targets, and known non-goals.

### 2. Execute Funnel Questioning
Lead the inquiry using open questions to capture the macro workflow, transition to probing questions to uncover exceptions and data volumes, and conclude with closed questions to confirm explicit boundaries.

### 3. Surface Hidden Assumptions via Colombo Probing
Probe "obvious" concepts. Identify unstated dependencies on legacy systems, batch jobs, manual offline workarounds, and cross-departmental handoffs.

### 4. Audit Draft Requirements Against BABOK 9 Criteria
Inspect each candidate requirement. Refactor compound sentences into atomic units. Eliminate passive voice and vague quantifiers ("fast", "user-friendly", "sufficient").

### 5. Execute System 2 Reflective Check & Handoff
Review candidate requirements against the anti-rationalization checklist. Flag remaining ambiguities as formal Open Questions with proposed interpretations. Emit machine handoff via `contracts/schemas/feature-ticket.json`.

## Checklist

- [ ] interview questions structured along the Funnel Protocol (Open → Probing → Closed)
- [ ] tacit domain rules and unstated assumptions probed via Colombo technique
- [ ] all requirements satisfy all 9 BABOK v3 criteria (Atomic, Complete, Consistent, etc.)
- [ ] passive or subjective adjectives ("robust", "scalable", "intuitive") eliminated
- [ ] System 2 reflective pause completed; zero unverified business rules assumed
- [ ] unresolved business decisions documented as explicit Open Questions with options

## Related Skills

- **analyze-business-requirements**: analyze and write implementation-ready requirements
- **write-use-cases**: structure user interactions into Karl Wiegers 13-field templates
- **trace-requirements-impact**: maintain RTM and evaluate change request blast radius
- **conduct-research**: explore market, legal, and compliance context
