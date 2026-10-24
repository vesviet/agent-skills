# SaaS Unit Economics, 32 Financial Metrics & Van Westendorp Pricing

> Authoritative mathematical and operational reference guide for SaaS unit economics, capital efficiency, willingness-to-pay surveys, and AI Total Cost of Ownership.

---

## 1. Master Index: 32 SaaS Financial & Operational Metrics

### Category A: Revenue & Growth Metrics
1. **MRR (Monthly Recurring Revenue)**: Normalized monthly subscription revenue. $\\text{MRR} = \\sum \\text{Monthly Contract Values}$.
2. **ARR (Annual Recurring Revenue)**: Annualized recurring contract value. $\\text{ARR} = \\text{MRR} \\times 12$.
3. **Net New ARR**: $\\text{New ARR} + \\text{Expansion ARR} - \\text{Contraction ARR} - \\text{Churned ARR}$.
4. **ARPU / ARPA (Average Revenue Per User/Account)**: $\\text{Total MRR} / \\text{Total Active Accounts}$.
5. **YoY Revenue Growth Rate**: $[(\\text{ARR}_t - \\text{ARR}_{t-1}) / \\text{ARR}_{t-1}] \\times 100\\%$.
6. **Compound Monthly Growth Rate (CMGR)**: $[(\\text{MRR}_t / \\text{MRR}_0)^{1/t} - 1] \\times 100\\%$.

### Category B: Retention & Churn Dynamics
7. **Gross Revenue Retention (GRR)**: $[(\\text{Beginning ARR} - \\text{Contraction} - \\text{Churn}) / \\text{Beginning ARR}] \\times 100\\%$. Max $100\\%$. Target $>85\\%$ SMB, $>90\\%$ Enterprise.
8. **Net Revenue Retention (NRR)**: $[(\\text{Beginning ARR} + \\text{Expansion} - \\text{Contraction} - \\text{Churn}) / \\text{Beginning ARR}] \\times 100\\%$. Target $>110\\%$.
9. **Logo Churn Rate**: $[\\text{Lost Customers in Period} / \\text{Beginning Customers}] \\times 100\\%$.
10. **Revenue Churn Rate**: $[\\text{Lost ARR in Period} / \\text{Beginning ARR}] \\times 100\\%$.
11. **Expansion MRR %**: $[\\text{Expansion MRR} / \\text{Beginning MRR}] \\times 100\\%$.
12. **Cohort Retention Half-Life**: Number of months until a customer cohort loses 50% of initial revenue.

### Category C: Unit Economics & Acquisition Efficiency
13. **Customer Acquisition Cost (CAC)**: $\\frac{\\text{Fully Loaded Sales \\& Marketing Expense}}{\\text{Number of New Customers Acquired}}$.
14. **Customer Lifetime Value (LTV)**: $\\frac{\\text{ARPU} \\times \\text{Gross Margin \\%}}{\\text{Revenue Churn Rate}}$.
15. **LTV / CAC Ratio**: $\\text{LTV} / \\text{CAC}$. Healthy: $\\ge 3.0$; World-Class: $4.0 - 5.0$.
16. **CAC Payback Period (Months)**: $\\frac{\\text{CAC}}{\\text{ARPU} \\times \\text{Gross Margin \\%}}$. Target $\\le 12$ mos (SMB), $\\le 18$ mos (Enterprise).
17. **Blended CAC vs. Paid CAC**: Separates organic viral acquisition from paid acquisition channels.
18. **Lead-to-Win Conversion Rate**: $[\\text{Closed-Won Deals} / \\text{Qualified Opportunities}] \\times 100\\%$.

### Category D: Capital Efficiency & Cash Health
19. **Magic Number**: $[(\\text{Q}_n \\text{ ARR} - \\text{Q}_{n-1} \\text{ ARR}) \\times 4] / \\text{Q}_{n-1} \\text{ S\\&M Expense}$. Benchmark: $\\ge 0.75$.
20. **Rule of 40**: $\\text{YoY Growth Rate (\\%)} + \\text{Free Cash Flow Margin (\\%)}$. Target $\\ge 40\\%$.
21. **Burn Multiple**: $\\text{Net Burn} / \\text{Net New ARR}$. Top-tier: $<1.0$; Good: $1.0-1.5$; Inefficient: $>2.0$.
22. **Haspelmath SaaS Quick Ratio**: $\\frac{\\text{New ARR} + \\text{Expansion ARR}}{\\text{Churned ARR} + \\text{Contraction ARR}}$. Target $>4.0$.
23. **Runway (Months)**: $\\text{Current Cash Balance} / \\text{Monthly Net Burn}$.
24. **Gross Margin %**: $[(\\text{Revenue} - \\text{COGS}) / \\text{Revenue}] \\times 100\\%$. Target $>75\\%$ for pure SaaS.

### Category E: Customer Engagement & Expansion
25. **DAU / MAU (Stickiness Ratio)**: $\\text{Daily Active Users} / \\text{Monthly Active Users}$. Target $>20\\%$.
26. **Activation Rate**: Percentage of signups reaching "Aha! Moment" within first 7 days.
27. **Time to First Value (TTFV)**: Elapsed hours/days from contract sign to primary workflow execution.
28. **Feature Adoption Depth**: Percentage of monthly users utilizing $\\ge 3$ core platform features.
29. **NPS (Net Promoter Score)**: $\\% \\text{Promoters} - \\% \\text{Detractors}$. Target $>50$.
30. **CSAT (Customer Satisfaction Score)**: Average satisfaction score post-interaction.

### Category F: AI Product Economics
31. **Cost per Verified Outcome (CPVO)**: $\\frac{\\text{Total AI Ops Cost (Inference + Guardrails + Evals + Human Review)}}{\\text{Total Successful Verified Outcomes}}$.
32. **Human Handoff Rate**: Percentage of AI-assisted sessions requiring human agent intervention.

---

## 2. Van Westendorp Price Sensitivity Meter (PSM)

The Van Westendorp PSM determines the price elasticity and optimal price range for new or repackaged products.

### The 4 Survey Questions
1. At what price would you consider the product to be **so inexpensive that you would question its quality**? (*Too Cheap*)
2. At what price would you consider the product to be a **bargain / great value**? (*Cheap / Good Value*)
3. At what price would you consider the product to be **expensive, but you would still consider buying it**? (*Expensive*)
4. At what price would you consider the product to be **so expensive that you would never consider it**? (*Too Expensive*)

### Key Intersections & Price Band
```
Cumulative %
 100% │          [Too Cheap]                [Too Expensive]
      │               \                          /
      │                \   Point of             /
      │                 \  Marginal            /  Point of Marginal
      │                  \ Cheapness          /   Expensiveness
      │                   \ (PMC)            /    (PME)
      │                    \       IPP      /
      │                     \       X      /
      │                      \     / \    /
      │                       \   /   \  /
      │                        \ /     \/
      │                         X  OPP  /
      │                        / \     / \
      │                       /   \   /   \
      │                      /     \ /     \
      │                     /       X       \
      │                    /                 \
   0% └───────────────────┴─────────┴─────────┴────────────────► Price ($)
                         PMC       OPP       PME
```

- **Point of Marginal Cheapness (PMC)**: Intersection of *Too Cheap* and *Expensive*. Lower bound of pricing.
- **Point of Marginal Expensiveness (PME)**: Intersection of *Too Expensive* and *Cheap*. Upper bound of pricing.
- **Optimum Price Point (OPP)**: Intersection of *Too Cheap* and *Too Expensive*. Minimal customer resistance.
- **Indifference Price Point (IPP)**: Intersection of *Cheap* and *Expensive*. Median market price anchor.

---

## 3. AI Total Cost of Ownership (TCO) per Verified Outcome

Raw token inference pricing from API providers represents only the visible tip of the AI cost iceberg.

### The 80/20 AI Cost Iceberg
- **20% Model API Inference**: Direct tokens consumed by LLM input and output.
- **80% Production Ops & Human Review**:
  - Embedding generation, vector database hosting, and hybrid retrieval.
  - Guardrail execution (input jailbreak detection, PII masking, schema validators).
  - Continuous Golden Eval benchmarking and automated regression testing.
  - Human-in-the-Loop (HITL) review escalations for low-confidence or high-stakes outputs.
  - Telemetry, logging, compliance auditing, and EU AI Act Article 50 provenance marking.

### Unit Cost Calculation Formula
$$\\text{Cost per Outcome} = \\frac{(\\text{Token Tokens} \\times \\text{Rate}) + \\text{Guardrail Cost} + \\text{Infra Ops} + (\\text{Handoff Rate} \\times \\text{Human Review Hourly Rate})}{\\text{Successful Outcomes}}$$
