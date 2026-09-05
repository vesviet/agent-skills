# In-Process Analytics & Quantitative Hallucination Prevention — Reference

This reference details procedures for executing local, zero-copy analytical queries using DuckDB and Polars, along with the strict quantitative verification protocols required to eliminate analytical hallucinations.

---

## 1. In-Process Analytics Playbook (DuckDB & Polars)

For exploratory datasets (< 100 GB), avoid the latency, egress fees, and compute expenses of spinning up cloud warehouse clusters. In-process engines execute vectorized SQL directly over columnar Parquet and lakehouse stores.

### 1.1 DuckDB Vectorized Querying
Directly query partitioned Parquet files or Iceberg metadata catalogs with memory bounds:

```python
import duckdb

con = duckdb.connect()
con.execute("SET max_memory = '4GB';")
con.execute("SET threads = 4;")

query = """
    SELECT
        date_trunc('month', order_timestamp) AS order_month,
        status,
        count(order_id) AS total_orders,
        round(sum(gross_amount_usd), 2) AS total_gross_usd,
        round(avg(gross_amount_usd), 2) AS avg_order_usd
    FROM read_parquet('store/silver/orders/*.parquet')
    WHERE order_timestamp >= '2026-01-01'
    GROUP BY 1, 2
    ORDER BY 1, 2;
"""
result_df = con.execute(query).pl()  # Zero-copy export to Polars
```

### 1.2 Polars Lazy Streaming Evaluation
For datasets that exceed available RAM, use Polars streaming engine to process data in micro-chunks without out-of-memory errors:

```python
import polars as pl

lazy_plan = (
    pl.scan_parquet("store/silver/orders/*.parquet")
    .filter(pl.col("status").is_in(["PAID", "SHIPPED"]))
    .group_by(["customer_tier", "payment_method"])
    .agg([
        pl.len().alias("transaction_count"),
        pl.col("gross_amount_usd").sum().alias("total_spend"),
        pl.col("gross_amount_usd").quantile(0.95).alias("p95_spend")
    ])
)

# Stream chunks through memory without full materialization
summary = lazy_plan.collect(streaming=True)
```

---

## 2. Quantitative Hallucination Elimination Protocol

To maintain zero-trust reliability, deliverables produced by data analysts or AI agents must never mix unsubstantiated narrative speculation with empirical observations.

### 2.1 Two-Column Table of Evidence
All conclusions in `data-analysis-report.json` or markdown briefs must be structured using explicit Fact vs Interpretation separation:

| Observable Fact (Empirical Data) | Analytical Interpretation (Inference) |
|---|---|
| In Q2 2026, Tier-1 customer churn increased from 2.1% (42/2,000) to 3.8% (76/2,000), $p = 0.003$. | Churn was driven by price increases enacted in May 2026; accounts citing pricing in exit surveys rose from 12% to 48%. |
| Mean order value for mobile checkout declined by \$14.20 (-18.3%) following release v2.4.0. | The redesigned checkout interface introduced friction on iOS devices; mobile drop-off rate at step 2 jumped by 24%. |

### 2.2 Independent Control Total Reconciliation
Before publishing analytical figures:
1. **Source Ledger Sum**: Calculate unadjusted aggregate metric directly from immutable ledger or Bronze tables.
2. **Analysis Sum**: Calculate sum from final transformed model.
3. **Reconciliation Variance**:
   $$\text{Variance} = |\text{Ledger Total} - \text{Analysis Total}|$$
   - Financial totals: Variance must be exactly **\$0.00**.
   - Event counters: Variance must not exceed **0.01%** (explainable by documented filtering rules).

### 2.3 Statistical Confidence Interval Calibration
Never report point estimates without confidence intervals:
- **Proportions / Conversion Rates**: Compute Wilson score intervals (95% confidence).
- **Skewed Financial Distributions**: Compute non-parametric bootstrap confidence intervals (1,000 iterations) reporting $[\text{P}_{2.5}, \text{P}_{97.5}]$.
