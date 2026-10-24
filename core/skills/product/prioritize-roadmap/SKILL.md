---
name: prioritize-roadmap
description: Score, sequence, and balance product roadmaps using calibrated quantitative RICE, WSJF, Kano classification, weighted scoring decision matrices, and capacity timeboxing. Use when resolving competing feature requests, evaluating build vs. buy decisions, prioritizing quarterly roadmaps, conducting vendor evaluations, or enforcing the Kill-Early protocol on underperforming bets.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Prioritize Roadmap

Use this skill to apply quantitative, objective prioritization frameworks to backlogs, roadmaps, vendor evaluations, and build-vs-buy decisions, eliminating subjective opinion bias and protecting engineering capacity.

## When to Use

- prioritizing quarterly product roadmaps across competing stakeholder initiatives
- ranking feature backlogs using calibrated RICE scoring or Weighted Shortest Job First (WSJF)
- categorizing customer requirements into Must-Be, Performance, and Delighters using the Kano Model
- evaluating Build vs. Buy options and third-party vendors via Weighted Scoring Decision Matrices
- sizing roadmap commitments against team capacity and velocity timeboxes
- executing the **Kill-Early Protocol** to terminate lagging experiments without sunk-cost bias

## Core Rules

- **Enforce Calibrated Quantitative RICE Scoring**:
  - $\text{RICE} = \frac{\text{Reach} \times \text{Impact} \times \text{Confidence}}{\text{Effort}}$
  - *Reach*: Number of unique active users/accounts impacted per quarter (measured via telemetry)
  - *Impact*: Standardized discrete rubric (3 = Massive, 2 = High, 1 = Medium, 0.5 = Low, 0.25 = Minimal)
  - *Confidence*: Strictly grounded (100% = Controlled A/B or heavy data, 80% = User interviews + analytics, 50% = Low / exploratory gut-feel)
  - *Effort*: Total person-months across Eng, Product, Design, QA (minimum unit: 0.5)
- **Categorize via Kano Model**:
  - *Must-Be (M)*: Table stakes / hygiene factors; absent causes outrage, present yields neutral satisfaction
  - *One-Dimensional / Performance (P)*: Linear satisfaction; more is better (speed, battery life, cost reduction)
  - *Attractive / Delighter (A)*: Unexpected capability; absent causes zero dissatisfaction, present drives viral NPS
  - *Indifferent (I)* / *Reverse (R)*: Explicitly eliminate from roadmap consideration
- **Construct Weighted Scoring Decision Matrices (MCDA)**:
  - Define explicit evaluation criteria normalized to 100% total weight
  - Score candidates independently on a 1-5 scale against objective rubrics
  - Conduct Sensitivity Analysis: vary top criterion weight by ±20% to verify ranking robustness
- **Enforce Capacity Timeboxing (70/30 Rule)**:
  - Commit maximum 70% of engineering velocity to scheduled roadmap features
  - Reserve 30% strictly for technical debt, bug triage, regression fixes, and operational resilience
- **Execute Kill-Early Protocol**:
  - Every prioritized bet must define explicit pre-committed kill metrics before implementation begins
  - If leading indicators fail to reach milestone threshold, terminate or pivot immediately
- Detailed formulas, rubrics, and templates: [`references/prioritization-scoring-and-kill-criteria.md`](references/prioritization-scoring-and-kill-criteria.md)

## Suggested Process

### 1. Collect & Normalize Candidate Initiatives
Compile backlog items. Normalize descriptions to outcome-oriented statements with clear user segments and target metrics.

### 2. Calculate Objective RICE / WSJF Scores
Gather telemetry data for Reach. Calibrate Impact using the standardized rubric. Apply strict Confidence discounting. Estimate cross-functional Effort. Calculate composite scores.

### 3. Overlay Kano Model Classification
Classify features into Must-Be, Performance, and Delighters. Ensure the release candidate contains 100% of critical Must-Bes, balanced with high-ROI Performance and 1-2 Delighters.

### 4. Apply Capacity & Dependency Timeboxing
Sort by composite priority. Fit initiatives into quarterly sprints respecting team capacity limits (capping at 70% available velocity). Sequence based on architectural dependencies.

### 5. Document Trade-offs & Kill Criteria
Explicitly publish non-goals and deferred candidates. Document kill criteria and milestone checkpoints for every approved bet.

## Checklist

- [ ] RICE Confidence discounted appropriately (no ungrounded 100% scores)
- [ ] Impact scored against standard discrete tiers (0.25 to 3.0)
- [ ] Effort accounts for cross-functional cost (Eng + Design + QA + Docs)
- [ ] Kano classifications verified with customer feedback
- [ ] 70/30 capacity buffer preserved for bugs and tech debt
- [ ] Weighted Decision Matrix includes sensitivity analysis if used for vendor or build-vs-buy
- [ ] Kill-early criteria and checkpoint review dates documented

## Related Skills

- **define-product-strategy**: establish strategic outcomes and 7 Powers defensibility
- **model-saas-metrics**: evaluate revenue impact, CAC payback, and AI TCO
- **build-story-map**: slice prioritized epics into user stories and release swimlanes
- **write-product-brief**: document approved scope and trade-offs
- **trace-requirements-impact**: assess change impact on dependent requirements
