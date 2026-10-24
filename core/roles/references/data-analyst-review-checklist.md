## Data Analyst Review Checklist

This reference checklist provides comprehensive evaluation criteria for data analysis, semantic querying, statistical drift verification, causal inference, and quantitative reporting to meet 2026–2027 Agentic SWE standards.

### 1. Semantic Metric Querying & Text-to-SQL Hallucination Defense
- **Canonical Semantic Layer Precedence**: All analytical metrics are derived from canonical Semantic Layer definitions (dbt MetricFlow, Cube.js, Apache Ossie) as the sole source of truth; ad-hoc redefined metrics are strictly prohibited.
- **Ungrounded Text-to-SQL Prohibition**: Unvalidated LLM-generated SQL queries are forbidden from executing directly against production warehouse tables without schema verification against the official catalog.
- **FastMCP Gateway & AST Validation**: Queries execute through the FastMCP gateway enforcing sqlglot AST verification: single read-only `SELECT` (prohibiting DDL/DML mutations), join complexity depth $\le 3$ joins, and hard row limits $\le 1000$ rows.
- **Show-The-Definition Attribution**: Every natural language or tabular metric deliverable quotes canonical mathematical formulas and dbt model lineage.
- **Discrepancy Reconciliation Disclosure**: Whenever an ad-hoc exploratory calculation produces results that diverge from official semantic KPIs, the mathematical variance, cause, and rationale must be formally reconciled and disclosed before sharing.

### 2. DuckDB & Polars In-Process Analytics Architecture
- **In-Process Compute Offloading**: Exploratory data analysis on local Parquet extracts and Iceberg snapshots is executed in-process via DuckDB v1.1+ and Polars 1.x+, eliminating unnecessary cloud data warehouse compute expenditure for sub-terabyte workloads.
- **Strict Memory Ceilings**: In-process DuckDB sessions strictly enforce memory limits (`SET max_memory = '4GB'`) and temporary NVMe disk spilling (`SET temp_directory = '/tmp/duckdb_spill'`) to guarantee that local analytical runs cannot exhaust host system memory or destabilize concurrent tasks.
- **Zero-Copy Apache Arrow Interchange**: Tabular data transformations between DuckDB, Polars, and Python analytical libraries leverage zero-copy Apache Arrow C Data Interface memory sharing (`con.execute(q).pl()`) to maximize throughput and minimize RAM footprint.
- **Polars LazyFrames Streaming**: Data volumes exceeding physical RAM leverage Polars LazyFrames with streaming execution (`collect(streaming=True)`) to eliminate Out-Of-Memory crashes.
- **DuckDB v2.0 Readiness**: Code and queries are audited for DuckDB v2.0 readiness (breaking storage format, VARIANT type support, and Quack server mode).

### 3. Statistical Distribution Drift & Anomaly Detection
- **Population Stability Index (PSI) Quantification**: Feature distributions, categorical breakdowns, and user cohort demographics are evaluated using vectorized PSI across reporting periods: $\text{PSI} < 0.10$ (Stable), $0.10 \le \text{PSI} \le 0.25$ (Moderate Drift), $\text{PSI} > 0.25$ (Significant Drift — pipeline halt triggered).
- **Continuous Distribution Drift Verification**: Continuous metric distributions across treatment and control or time periods are evaluated using two-sample Kolmogorov-Smirnov (KS) tests; statistically significant distribution shifts ($p < 0.01$) must be explicitly reported.
- **Tukey's IQR Outlier Fences**: Transient outliers and anomalous data spikes are isolated using non-parametric Interquartile Range fences ($Q_1 - 1.5\text{IQR}$, $Q_3 + 1.5\text{IQR}$) to prevent extreme anomalies from distorting business conclusions.
- **Sample Size Adequacy & Statistical Power**: Sample size, statistical power (minimum 80%), and minimum detectable effect (MDE) are calculated and validated before asserting conclusions on filtered segments or low-volume cohorts.
- **Data Quality & Missingness Disclosure**: Dataset null rates, duplicate records, collection gaps, and sensor noise are explicitly audited, logged, and disclosed in report appendices.

### 4. Causal DAG Modeling & Confounder Elimination
- **Pearl's Causal Hierarchy Discipline**: Rigorously separate Rung 1 Associations ($P(y|x)$) from Rung 2 Interventions ($P(y|do(x))$); strictly prohibit causal verbs ("causes", "drives", "impacts") when only observational correlations exist.
- **Explicit Causal DAG Specification**: Directed Acyclic Graphs (DAGs) are constructed for all high-stakes causal inquiries in DOT format, formally specifying treatments, outcomes, observed confounders, and potential colliders.
- **Backdoor Criterion Satisfaction**: All non-causal backdoor paths between treatment and outcome are blocked via conditioning on observed confounders ($W$).
- **Strict Collider Bias Avoidance**: Methods actively avoid conditioning on post-treatment colliders ($T \rightarrow C \leftarrow Y$, Berkson's Paradox) by prohibiting conditioning on post-treatment variables.
- **Elimination of Common Biases**: Methodologies actively test for and eliminate selection bias, survivorship bias, and Simpson's Paradox before attributing observed metric changes to specific product or business interventions.

### 5. DoWhy 4-Step Robustness Framework & Quasi-Experimental Methods
- **The DoWhy 4-Step Lifecycle**: Every causal business claim executes Model $\rightarrow$ Identify $\rightarrow$ Estimate $\rightarrow$ Refute.
- **Mandatory 3-Way DoWhy Robustness Refutations**:
  1. *Placebo Treatment Refuter*: Permute treatment randomly; estimated effect must drop to 0 ($p > 0.05$).
  2. *Random Common Cause Refuter*: Inject synthetic confounder; estimated effect must shift $< 10\%$.
  3. *Data Subset Refuter*: Re-estimate on 80% bootstrap subset; estimated effect must shift $< 15\%$.
- **Quasi-Experimental Methods Landscape**:
  - *Difference-in-Differences (DiD)*: Validate parallel trends across pre-intervention windows; utilize Callaway-Sant'Anna for staggered adoption.
  - *Synthetic Control Method (SCM)*: Construct convex donor pool weights ($\sum w_j = 1, w_j \ge 0$); run in-space and in-time placebo checks.
  - *Regression Discontinuity (RD)*: Verify continuity of baseline covariates and density of running variable around decision cutoff (McCrary density test).
  - *Double Machine Learning (DML)*: Apply Neyman-orthogonal score equations with cross-fitting to control high-dimensional confounders.
- **CUPED Variance Reduction**: Adjust target metric using pre-experiment baseline covariates ($\tilde{Y} = Y - \theta(X - \bar{X})$), cutting metric variance by up to 50%+ to double statistical power.

### 6. Automated Sample Ratio Mismatch (SRM) Integrity Gate
- **Pearson's Chi-squared Goodness-of-Fit**: Automated SRM test evaluates assignment counts across control and treatment arms:
  $$\chi^2 = \sum_{i \in \{C, T\}} \frac{(O_i - E_i)^2}{E_i} \sim \chi^2(1)$$
- **Automated Hard Abort Gate**: If $p < 0.001$, **ABORT EVALUATION IMMEDIATELY**; declare experiment invalid due to tracking loss, bot interference, or selective attrition.
- **Zero Override Policy**: Never report conversion lift or treatment metrics on an SRM-tainted experiment under any circumstances.

### 7. Two-Column Table of Evidence: Empirical Facts vs Analytical Interpretations
- **Mandatory Structural Segregation**: All analysis deliverables strictly segregate empirical data from narrative interpretation via the two-column Table of Evidence (`FACT-INTERPRETATION-LOCK`).
- **Left Column — Empirical Observations (Facts)**: Statistically verified metric values, sample sizes ($N$), 95% confidence intervals, p-values, PSI scores, and ledger reconciliation variances.
- **Right Column — Analytical Interpretations (Inference)**: Hypothesized business drivers, strategic implications, risk assessments, and policy recommendations.
- **Disambiguation of Speculation**: Speculative hypotheses or subjective opinions must never be conflated with statistically verified observations.

### 8. Quantitative Evidence, Verifiable Provenance & Cryptographic Auditability
- **Machine-Readable Contract Handoff**: Primary analytical findings are emitted via `contracts/schemas/data-analysis-report.json`, satisfying automated validation gates and multi-agent coordination requirements.
- **Confidence Intervals & Standardized Effect Sizes**: Every primary point estimate is presented with a 95% Confidence Interval (CI) and standardized effect size (Cohen's d, percentage delta) rather than isolated p-values.
- **Cryptographic Provenance Artifacts**: Reports record immutable provenance: input Parquet SHA-256 hashes, query execution run IDs, source lakehouse snapshot IDs, and query timestamps.
- **Deterministic Script Reproducibility**: Analysis workflows are committed as standalone, fully deterministic scripts (DuckDB SQL, Polars Python) capable of clean execution in fresh environments without hidden state.
- **Independent Control Total Reconciliation**: Verify 0.00% financial variance against independent source ledgers on critical corporate figures.

### 9. Data Privacy, Classification & OWASP ASI Governance
- **Pre-Analysis Sensitivity Classification**: Analyzed datasets are classified according to `data-classification.yaml` (Public, Internal, Confidential, Restricted) prior to ingestion or exploration.
- **Comprehensive PII Masking & Redaction**: Customer identifiers, email addresses, phone numbers, and financial details are hashed, masked, or aggregated in all shared reports, dashboards, and CSV exports.
- **OWASP ASI06 Context Poisoning Defense**: Historical analyst memory, external briefings, and LLM prompts are treated as untrusted inputs; all assertions are verified against live verified datasets before incorporation.
- **OWASP ASI03 Least-Agency Sandbox Compliance**: AI-assisted analytical code and exploratory scripts execute under least-agency sandbox policies (`sandbox-sdk`), preventing unauthorized credential exfiltration or lateral database access.

### 10. Embedded In-Process Analytical SQL & Cross-Source Zero-ETL Federation
- **Embedded In-Process SQL Execution (chDB & DuckDB)**: Analytical queries on local extracts and lakehouse files execute in-process via embedded engines (chDB SQL/DataStore, DuckDB v1.1+) utilizing vectorized morsels and 1000+ ClickHouse analytical functions without external database server infrastructure.
- **Stateful Multi-Step Session Pipelines**: Multi-step exploratory transformations utilize stateful sessions (`chdb.session.Session`) with ephemeral or disk-backed temporary storage (`/tmp/chdb_session`), persisting intermediate views and temporary tables across script steps without memory leakage.
- **Cross-Source Zero-ETL Federation**: Analytical queries join disparate remote and local data sources directly (joining AWS S3 Parquet datasets via `s3()`, transactional PostgreSQL tables via `postgresql()`, MySQL via `mysql()`, and Delta Lake / Iceberg) in a single unified SQL statement.
- **Zero-Copy Arrow Memory Interoperability**: In-process tabular data exchanges between chDB, DuckDB, Polars, and PyArrow utilize the Apache Arrow C Data Interface (`to_arrow()`, `from_arrow()`) ensuring zero-copy memory pointer sharing and sub-second analytical processing under strict RAM ceilings.
- **Agent Query Cost FinOps Tracking**: Track AI agent query execution costs (token usage, compute time, scanned bytes) as a dedicated FinOps line item in `contracts/schemas/data-analysis-report.json`; enforce per-agent query cost budgets and alerting thresholds.
