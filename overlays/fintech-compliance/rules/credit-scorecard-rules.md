# Credit Scorecard Rules

Regulatory standards and mathematical formulas governing credit risk scorecard development, Weight of Evidence (WOE) transformations, Information Value (IV) variable selection, score calibration, and Population Stability Index (PSI) monitoring.

## 1. Monotonic Weight of Evidence (WOE) Binning

Weight of Evidence measures the relative risk contribution of each attribute bin for a binary credit outcome ($Y=0$ Good loan, $Y=1$ Bad loan / default):

$$\text{WOE}_i = \ln\left(\frac{\text{Distribution of Goods}_i}{\text{Distribution of Bads}_i}\right) = \ln\left(\frac{G_i / G_{\text{total}}}{B_i / B_{\text{total}}}\right)$$

### Monotonicity Invariant
- **Continuous and Ordinal Variables**: Must exhibit strictly monotonic (strictly increasing or strictly decreasing) WOE curves across ordered bins.
- **Regulatory Rationale (Basel II/III IRB & Fair Lending)**: Non-monotonic WOE curves indicate arbitrary risk fluctuations, lack economic rationale, and violate regulatory model explainability standards.
- **Bin Constraints**:
  - Every bin must contain at least $5\%$ of the total development sample population to prevent sparse bin instability.
  - Zero-default or zero-good bins are strictly prohibited (apply Laplace smoothing or pool adjacent bins).
  - Missing/unknown values (`NULL`, `NaN`) must be isolated into a dedicated special category bin with independent WOE tracking.
- **Automated Bin Pooling**: If initial quantile binning produces non-monotonicity or sparse bins, adjacent bins must be merged iteratively using Chi-Square ($\chi^2$) pooling or CHAID clustering until strict monotonicity is achieved. If monotonicity cannot be established with at least 3 bins, the variable must be rejected.

## 2. Information Value (IV) Screening Thresholds

Information Value assesses the overall predictive power of an independent feature across all $k$ bins:

$$\text{IV} = \sum_{i=1}^k \left(\frac{G_i}{G_{\text{total}}} - \frac{B_i}{B_{\text{total}}}\right) \cdot \text{WOE}_i$$

Candidate predictors must be evaluated against standard regulatory IV bands:

| IV Range | Predictive Power Classification | Action / Governance Decision |
| :--- | :--- | :--- |
| $\text{IV} < 0.02$ | Unpredictive / Noise | **Exclude** from model candidate pool |
| $0.02 \le \text{IV} < 0.10$ | Weak Predictor | Use with caution; acceptable only as control or domain-essential feature |
| $0.10 \le \text{IV} < 0.30$ | Medium Predictor | **Standard core predictor**; ideal for regulatory scorecards |
| $0.30 \le \text{IV} \le 0.50$ | Strong Predictor | **High-value predictor**; inspect for correlation / collinearity |
| $\text{IV} > 0.50$ | Suspicious / Target Leakage | **Mandatory audit**; investigate post-default leakage or overfit; reject if leaking |

Multi-collinearity constraint: Features sharing Spearman correlation $|\rho| \ge 0.60$ or Variance Inflation Factor $\text{VIF} \ge 3.0$ must be pruned, retaining the candidate with higher IV and cleaner economic logic.

## 3. Scorecard Point Scaling & Calibration (PDO)

A logistic regression model predicting $\ln(\text{Odds}) = \ln(P(\text{Good})/P(\text{Bad})) = \beta_0 + \sum \beta_j \text{WOE}_j$ is scaled to an intuitive integer credit score using Points to Double Odds (PDO):

$$\text{Score} = \text{Offset} - \text{Factor} \cdot \ln(\text{Odds})$$

Where:
$$\text{Factor} = \frac{\text{PDO}}{\ln(2)}$$
$$\text{Offset} = \text{TargetScore} - \text{Factor} \cdot \ln(\text{TargetOdds})$$

### Standard Benchmark Calibration
- **Target Score**: $600$ points
- **Target Odds**: $50 : 1$ (50 Good loans per 1 Bad loan)
- **Points to Double Odds (PDO)**: $20$ points (score increases by 20 points whenever the Good:Bad odds double)

Individual bin points are computed as:
$$\text{Points}_{ij} = -(\beta_j \cdot \text{WOE}_{ij} + \frac{\beta_0}{m}) \cdot \text{Factor} + \frac{\text{Offset}}{m}$$
where $m$ is the total number of features in the final scorecard. Total credit score equals the sum of base points plus assigned bin points for each applicant, rounded to the nearest integer.

## 4. Population Stability Index (PSI) Drift Monitoring

Population Stability Index evaluates distribution shift between the reference validation population ($E$, Expected) and the live production scoring population ($A$, Actual) across $m$ score deciles:

$$\text{PSI} = \sum_{j=1}^m (A_j - E_j) \cdot \ln\left(\frac{A_j}{E_j}\right)$$

### Action Thresholds
- $\text{PSI} < 0.10$: **Stable Distribution**. Model continues in standard production monitoring without intervention.
- $0.10 \le \text{PSI} \le 0.25$: **Moderate Shift**. Requires increased monitoring frequency, origination channel audit, and segment-level Characteristic Stability Index (CSI) analysis.
- $\text{PSI} > 0.25$: **Significant Population Drift**. Triggers mandatory model risk alert; scorecard requires formal recalibration or retraining.

## 5. Model Validation & Fair Lending Compliance

1. **Discrimination Metrics**:
   - Kolmogorov-Smirnov ($\text{KS}$) statistic must satisfy $\text{KS} \ge 0.30$ (benchmark target $0.35 - 0.50$).
   - Area Under ROC Curve ($\text{AUC}$) must satisfy $\text{AUC} \ge 0.70$ ($\text{Gini} \ge 0.40$).
2. **Out-of-Time (OOT) Testing**: The model must be validated on a holdout temporal sample drawn at least 6–12 months after the training observation window to prove stability over credit cycles.
3. **Fair Lending & Anti-Bias (ECOA / FCRA)**:
   - Protected demographic variables (race, gender, marital status, religion, nationality, age under ECOA constraints) are strictly prohibited as model inputs.
   - For every rejected applicant, the scorecard engine must produce the top 3–4 Adverse Action Reason Codes based on the largest point deficits relative to maximum possible score per characteristic.

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-10-15
