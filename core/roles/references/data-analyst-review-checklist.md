## Data Analyst Review Checklist

This reference checklist provides comprehensive evaluation criteria for data analysis, semantic querying, statistical drift verification, causal inference, and quantitative reporting to meet 2027 Agentic SWE standards.

### 1. Semantic Metric Querying & Text-to-SQL Hallucination Defense
- **Canonical Semantic Layer Precedence**: All analytical metrics are derived from canonical Semantic Layer definitions (dbt MetricFlow, Cube, Looker Explores) as the sole source of truth; ad-hoc redefined metrics are strictly prohibited.
- **Ungrounded Text-to-SQL Prohibition**: Unvalidated LLM-generated SQL queries are forbidden from executing directly against production warehouse tables without schema verification against the official catalog.
- **Pre-Execution Schema Dry-Run**: Every query undergoes pre-execution validation: column existence verified against data dictionary, join cardinalities checked for unintended cartesian multiplication, aggregation grain matches inquiry, and filter completeness confirmed.
- **Read-Only Scoping & Timeout Ceilings**: Queries execute exclusively against read-only replicas or analytical views with enforced query execution timeouts and memory quotas; write primaries are never touched.
- **Discrepancy Reconciliation Disclosure**: Whenever an ad-hoc exploratory calculation produces results that diverge from official semantic KPIs, the mathematical variance, cause, and rationale must be formally reconciled and disclosed before sharing.

### 2. DuckDB & Polars In-Process Analytics Architecture
- **In-Process Compute Offloading**: Exploratory data analysis on local Parquet extracts and Iceberg snapshots is executed in-process via DuckDB and Polars, eliminating unnecessary cloud data warehouse compute expenditure for sub-terabyte workloads.
- **Strict Memory Ceilings**: In-process DuckDB sessions strictly enforce memory limits (`SET max_memory = '4GB'`) and thread constraints to guarantee that local analytical runs cannot exhaust host system memory or destabilize concurrent tasks.
- **Hardened Sandbox Isolation**: All data analysis scripts and notebook execution occur within isolated execution environments (`sandbox-sdk`) with restricted filesystem access and blocked outbound internet egress.
- **Zero-Copy Apache Arrow Interchange**: Tabular data transformations between DuckDB, Polars, and Python analytical libraries leverage zero-copy Apache Arrow memory sharing to maximize throughput and minimize RAM footprint.
- **Deterministic Script Reproducibility**: Analysis workflows are committed as standalone, fully deterministic scripts (DuckDB SQL, Polars Python) capable of clean execution in fresh environments without hidden state.

### 3. Statistical Drift & Anomaly Detection
- **Population Stability Index (PSI) Quantification**: Feature distributions, categorical breakdowns, and user cohort demographics are evaluated using PSI across reporting periods; significant shifts (PSI ≥ 0.2) must be documented and accounted for before publishing comparative trends.
- **Continuous Distribution Drift Verification**: Continuous metric distributions across treatment and control or time periods are evaluated using two-sample Kolmogorov-Smirnov (KS) tests; statistically significant distribution shifts must be explicitly reported.
- **Z-Score & IQR Outlier Segregation**: Transient outliers and anomalous data spikes are isolated using Z-score (>3 sigma) and Interquartile Range (IQR) methods to prevent extreme anomalies from distorting business conclusions.
- **Sample Size Adequacy & Statistical Power**: Sample size, statistical power (minimum 80%), and minimum detectable effect (MDE) are calculated and validated before asserting conclusions on filtered segments or low-volume cohorts.
- **Data Quality & Missingness Disclosure**: Dataset null rates, duplicate records, collection gaps, and sensor noise are explicitly audited, logged, and disclosed in report appendices.

### 4. Causal Inference & DAG Confounder Elimination
- **Explicit Causal DAG Specification**: Directed Acyclic Graphs (DAGs) are constructed for all high-stakes causal inquiries, formally specifying treatments, outcomes, observed confounders, and potential colliders.
- **Bias & Paradox Elimination**: Analytical methods actively test for and eliminate selection bias, survivorship bias, and Simpson's Paradox before attributing observed metric changes to specific product or business interventions.
- **Quasi-Experimental Method Selection & Validation**:
  - **Randomized Controlled Trials (A/B Testing)**: Verify randomization balance across covariates and pass Sample Ratio Mismatch (SRM) checks before evaluating treatment effect.
  - **Difference-in-Differences (DiD)**: Validate the parallel trends assumption across pre-intervention windows; include placebo test verification.
  - **Regression Discontinuity (RD)**: Verify continuity of baseline covariates and density of running variable around the decision threshold (McCrary test).
  - **Synthetic Controls**: Verify pre-treatment fit and donor pool weights; run in-space and in-time placebo checks.
  - **Instrumental Variables (IV)**: Verify instrument relevance (first-stage F-statistic > 10) and document exclusion restriction justification.
- **Strict Correlation-Causation Linguistic Boundary**: Explicitly disclose whether causal evidence exists; strictly require associative language ("associated with", "correlated with") when causal conditions are unproven; prohibit causal verbs ("causes", "drives", "impacts") without formal proof.

### 5. Quantitative Evidence & Verifiable Reporting
- **Machine-Readable Contract Handoff**: Primary analytical findings are emitted via `contracts/schemas/data-analysis-report.json`, satisfying automated validation gates and multi-agent coordination requirements.
- **Confidence Intervals & Standardized Effect Sizes**: Every primary point estimate is presented with a 95% Confidence Interval (CI) and standardized effect size (Cohen's d, percentage delta) rather than isolated p-values or point percentages.
- **Cryptographic Provenance Artifacts**: Reports record immutable provenance: input Parquet SHA-256 hashes, query execution run IDs, source lakehouse snapshot IDs, and query timestamps.
- **Independent Auditability**: All findings can be reproduced end-to-end by independent auditors or automated reviewer agents using the committed script and recorded source hashes.
- **Information Gain & Decision Utility**: Reports provide novel primary insights, counter-intuitive findings, and strategic trade-off options rather than descriptive restatements of trivial metrics.

### 6. Data Privacy, Classification & OWASP ASI Governance
- **Pre-Analysis Sensitivity Classification**: Analyzed datasets are classified according to `data-classification.yaml` (Public, Internal, Confidential, Restricted) prior to ingestion or exploration.
- **Comprehensive PII Masking & Redaction**: Customer identifiers, email addresses, phone numbers, and financial details are hashed, masked, or aggregated in all shared reports, dashboards, and CSV exports.
- **OWASP ASI06 Context Poisoning Defense**: Historical analyst memory, external briefings, and LLM prompts are treated as untrusted inputs; all assertions are verified against live verified datasets before incorporation.
- **OWASP ASI03 Least-Agency Sandbox Compliance**: AI-assisted analytical code and exploratory scripts execute under least-agency sandbox policies, preventing unauthorized credential exfiltration or lateral database access.
