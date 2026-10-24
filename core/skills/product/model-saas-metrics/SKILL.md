---
name: model-saas-metrics
description: Model SaaS unit economics, deterministic financial metrics, Van Westendorp price sensitivity, and AI Total Cost of Ownership (TCO). Use when calculating CAC, LTV, Magic Number, Rule of 40, Burn Multiple, Net Revenue Retention, analyzing pricing tiers and willingness-to-pay, or budgeting AI inference and orchestration costs per verified outcome.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Model SaaS Metrics

Use this skill to model SaaS financial health, evaluate unit economics, optimize pricing models via willingness-to-pay analysis, and calculate AI Total Cost of Ownership (TCO) per verified outcome.

## When to Use

- calculating SaaS business health metrics (CAC, LTV, Magic Number, Rule of 40, NRR, Burn Multiple)
- evaluating pricing tiers, value metric selection, and packaging strategies
- conducting Van Westendorp Price Sensitivity Meter (PSM) survey analysis
- modeling Total Cost of Ownership (TCO) for AI products and agentic workflows
- analyzing payback periods and unit economic feasibility before scaling marketing spend
- establishing financial sanity gates for executive and investor briefings

## Core Rules

- **Enforce Deterministic Financial Calculations**:
  - Never fabricate or hand-wave unit economics; apply strict mathematical definitions
  - Target benchmark ratios: $\text{LTV}/\text{CAC} \ge 3.0$, $\text{CAC Payback} \le 12$ months (SMB/Mid-Market) or $\le 18$ months (Enterprise)
  - Enforce the **Rule of 40**: $\text{YoY Revenue Growth Rate (\%)} + \text{Free Cash Flow Margin (\%)} \ge 40\%$
  - Track **Net Revenue Retention (NRR)**: $> 110\%$ indicates top-quartile product expansion power
- **Calculate Magic Number for Go-To-Market Efficiency**:
  - $\text{Magic Number} = \frac{(\text{Q}_n \text{ ARR} - \text{Q}_{n-1} \text{ ARR}) \times 4}{\text{Q}_{n-1} \text{ Sales \& Marketing Expense}}$
  - $\ge 1.0$: High efficiency; accelerate S&M spend
  - $0.75 - 1.0$: Healthy efficiency; maintain pace
  - $< 0.75$: Inefficient growth; fix onboarding, retention, and product-market fit before scaling spend
- **Apply Van Westendorp Price Sensitivity Meter (PSM)**:
  - Collect responses across 4 price points: Too Cheap, Cheap (Good Value), Expensive, Too Expensive
  - Map the 4 cumulative curves to determine the Price Sensitivity Envelope:
    - Point of Marginal Cheapness (PMC)
    - Point of Marginal Expensiveness (PME)
    - Optimum Price Point (OPP)
    - Indifference Price Point (IPP)
- **Model AI Product TCO per Verified Outcome (80/20 Rule)**:
  - Never budget based on raw token inference costs alone
  - Model the complete economic envelope: raw model inference represents ~20% of operating cost; orchestration, eval pipelines, guardrails, embeddings, caching, and human-in-the-loop review represent ~80%
  - Measure unit economics in **Cost per Verified Outcome** (e.g. Cost per Resolved Support Ticket)
- Detailed formulas, benchmarks, and PSM calculation worksheets: [`references/saas-unit-economics-and-pricing.md`](references/saas-unit-economics-and-pricing.md)

## Suggested Process

### 1. Collect Baseline Operating & Financial Inputs
Gather New Bookings, MRR/ARR, Churn, S&M Expenses, Gross Margin %, and active customer counts.

### 2. Compute Core Unit Economics & Efficiency Ratios
Calculate CAC, LTV, CAC Payback Period, Net Revenue Retention (NRR), and Magic Number. Assess against industry benchmarks.

### 3. Analyze Pricing Architecture & Willingness-to-Pay
Evaluate current value metrics (seats, consumption, outcomes). If pricing is under review, analyze Van Westendorp survey data to establish the optimal price band.

### 4. Build AI Outcome Economic Envelope
If AI/LLM components are involved, model total inference, embedding, retrieval, guardrail, and human escalation costs per user transaction.

### 5. Synthesize Executive Financial Report
Produce a standardized metrics dashboard highlighting unit economic health, expansion efficiency, runway implications, and recommendations.

## Checklist

- [ ] LTV calculated with Gross Margin adjustment: $\text{LTV} = \frac{\text{ARPU} \times \text{Gross Margin (\%)}}{\text{Churn Rate}}$
- [ ] CAC includes fully loaded S&M costs (salaries, commissions, tools, ad spend)
- [ ] CAC Payback Period accurately accounted for in months
- [ ] Magic Number calculated using sequential quarters
- [ ] Rule of 40 computed with Free Cash Flow or EBITDA margin
- [ ] Van Westendorp Price Sensitivity Envelope identifies OPP and IPP
- [ ] AI TCO accounts for 80/20 cost ratio (evals, guardrails, and human review included)

## Related Skills

- **define-product-strategy**: formulate value proposition and 7 Powers pricing power
- **prioritize-roadmap**: incorporate financial ROI and effort into RICE scoring
- **build-story-map**: align release scope with capacity and budget envelopes
- **manage-vietnam-accounting**: reconcile financial statements and statutory accounts
