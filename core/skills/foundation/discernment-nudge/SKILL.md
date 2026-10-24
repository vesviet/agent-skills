---
name: discernment-nudge
description: "Use when evaluating high-stakes architectural plans, financial projections, or critical code reviews, appending 2 to 3 sharp Socratic follow-up questions to probe unstated assumptions, verify critical facts, and surface missing context."
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# discernment-nudge

## Core Rules

1. **Trigger Boundary on Substantive Outputs:** Trigger exclusively on substantive, high-stakes deliverables (system design specifications, database migration plans touching financial balances, ADRs, and deployment release plans). Never trigger on simple lookups, syntax questions, or conversational status messages.
2. **Frequency Ceiling Invariant:** Trigger at most once per conversation or review phase to prevent fatigue.
3. **Exact Standard Lead-In:** Always preface the nudge with the exact canonical phrase:
   `A few things worth a second look:`
4. **Tripartite Discernment Taxonomy:** Formulate exactly 2 to 3 concise, pointed bullet points targeting:
   - **Fact Checking:** Specific numbers, SLA thresholds, or regulatory constraints that require empirical verification.
   - **Reasoning Probing:** Hidden assumptions regarding concurrency, distributed state, or single points of failure.
   - **Missing Context:** Environmental variables, legacy edge cases, or client quirks assumed by the proposal.
5. **Concise & Non-Preachy Posture:** Keep each question under 30 words. Focus strictly on actionable engineering risks.

## Suggested Process

1. **Output Classification:** Review draft recommendations or architectural decisions. Check if the output impacts data integrity, money, or core uptime.
2. **Assumption Auditing:** Identify the top 3 unstated assumptions necessary for the plan to succeed.
3. **Question Formulation:** Draft 2–3 sharp questions mapping to Fact Checking, Reasoning Probing, and Missing Context.
4. **Placement:** Append the nudge to the bottom of the artifact or review report under the exact header format.
5. **Assumptions Ledger Bridge:** If questions reveal unresolved blockers, route them into `assumptions-ledger.json`.

## Checklist

- [ ] Output is a high-stakes architectural, financial, or data model deliverable.
- [ ] Exactly 2 to 3 concise Socratic questions are formulated.
- [ ] Exact lead-in phrase `A few things worth a second look:` is used.
- [ ] Questions explicitly target facts, reasoning assumptions, or missing operational context.
- [ ] Questions are objective, specific, and actionable (each $< 30$ words).

## Related Skills

- **review-code**: Incorporates discernment probing into code change reviews.
- **security-audit**: Audits adversarial assumptions in architecture specs.
- **review-service**: Evaluates service architecture and runtime assumptions.

## Output Contracts

When unblocking open questions from a discernment nudge, emit:
- **Assumptions Ledger:** `core/contracts/schemas/assumptions-ledger.json`
- **Code Review Finding:** `core/contracts/schemas/code-review-finding.json`
