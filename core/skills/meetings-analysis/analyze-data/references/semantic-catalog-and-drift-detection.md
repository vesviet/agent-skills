# Semantic Metric Catalog & Statistical Drift Detection — Reference

This reference provides implementation standards, metric query protocols, and statistical tests to prevent Text-to-SQL hallucinations and detect covariate data distribution drift before publishing analytical deliverables.

---

## 1. Semantic Metric Catalog & Anti-Text-to-SQL Protocol

Direct Text-to-SQL generation by AI models or ad-hoc querying by analysts frequently produces silent analytical defects: joining on non-unique keys, recalculating conflicting metric formulas, or averaging already-averaged ratios. Modern data architectures mandate querying through a unified Semantic Layer (dbt Semantic Layer / MetricFlow, Cube.js).

### 1.1 Canonical Semantic Metric Definition
Metrics must be defined once in semantic repository specifications:

```yaml
# Example: dbt semantic layer metric specification
semantic_models:
  - name: orders
    model: ref('silver_orders')
    entities:
      - name: order_id
        type: primary
      - name: customer_id
        type: foreign
    dimensions:
      - name: order_timestamp
        type: time
        type_params:
          time_granularity: day
      - name: status
        type: categorical
    measures:
      - name: gross_revenue
        expr: gross_amount_usd
        agg: sum

metrics:
  - name: net_revenue
    type: simple
    label: "Net Revenue (USD)"
    type_params:
      measure: gross_revenue
    filter: |
      status IN ('PAID', 'SHIPPED')
```

### 1.2 Canonical Metric Querying
Queries must target semantic interfaces rather than arbitrary table joins:

```bash
# Querying canonical metrics via MetricFlow CLI
mf query --metrics net_revenue \
         --group-by order_timestamp__month,status \
         --where "order_timestamp >= '2026-01-01'"
```

### 1.3 Anti-Text-to-SQL Guardrails
1. **Forbidden Ad-Hoc Joins**: Disallow AI-generated joins across raw lakehouse tables unless verified against the semantic relationship graph.
2. **Dimension Hierarchy Enforcement**: Enforce standard dimension drill-downs (e.g. `district` → `province` → `country`) defined in the catalog.
3. **Metric Granularity Check**: Reject queries that aggregate measures across mismatched grain without explicit fanout protection.

---

## 2. Statistical Distribution Drift Detection

Before reporting comparative findings or training machine learning models, analysts must verify that underlying data distributions remain stationary.

### 2.1 Population Stability Index (PSI)
Use PSI to measure the magnitude of distribution shifts between a baseline dataset (expected $E$) and a target dataset (actual $A$) partitioned into $k$ buckets:

$$\text{PSI} = \sum_{i=1}^k (A_i - E_i) \times \ln\left(\frac{A_i}{E_i}\right)$$

| PSI Value | Interpretation | Required Action |
|---|---|---|
| **$\text{PSI} < 0.10$** | Insignificant shift | Data distribution is stable; proceed with analysis. |
| **$0.10 \le \text{PSI} \le 0.20$** | Moderate shift | Flag drift in report; inspect feature bins and trend lines. |
| **$\text{PSI} > 0.20$** | Significant shift | Alert data engineers; halt downstream modeling; investigate pipeline or market anomaly. |

### 2.2 Continuous Distribution Tests: Kolmogorov-Smirnov (KS)
For continuous numeric features (e.g. transaction amounts, session latencies), execute the two-sample KS test:
- **Null Hypothesis ($H_0$)**: Baseline and evaluation distributions are identical.
- **Decision Threshold**: Reject $H_0$ if $p\text{-value} < 0.01$. Compute maximum vertical divergence $D$:
  $$D = \sup_x |F_1(x) - F_2(x)|$$

### 2.3 Categorical Distribution Tests: Chi-Square ($\chi^2$)
For categorical features (e.g. customer tier, payment method), run the Pearson Chi-Square test of independence:
$$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$$
Flag significant category migration when $p < 0.01$.
