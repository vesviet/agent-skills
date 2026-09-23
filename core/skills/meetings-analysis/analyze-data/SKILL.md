---
name: analyze-data
description: Explore analytical datasets using DuckDB/Polars, query canonical Semantic Metric Catalogs (dbt MetricFlow, Cube.js, Apache Ossie) to eliminate Text-to-SQL hallucinations, detect statistical distribution drift, track agent query costs as FinOps line item, and deliver quantitatively verified insights with explicit fact/interpretation separation. Use when answering business questions from data without owning production pipeline infrastructure.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests, execute_command]
---

# Analyze Data

Use this skill for **decision science and analytical** work: querying canonical metrics, profiling data in-process, evaluating statistical drift, conducting causal inference, and producing verifiable stakeholder reports.

## When to Use

- answering business, product, and KPI questions using conformed lakehouse tables
- querying certified metrics via Semantic Metric Layers (dbt MetricFlow, Cube.js, **Apache Ossie**)
- executing fast in-process exploratory analytics on Parquet/Iceberg extracts via DuckDB and Polars
- auditing statistical feature and cohort distribution drift (PSI, Two-Sample KS-test, Tukey's IQR)
- evaluating A/B tests with automated Sample Ratio Mismatch (SRM) checks and causal DAG inference
- producing decision-ready quantitative reports with explicit fact vs interpretation separation
- **tracking agent query costs as a FinOps line item** for AI agent data access

## Core Rules

- **Read-Only Access**: treat all source tables, lakehouse catalogs, and databases as strictly read-only.
- **Canonical Semantic Layer Precedence**: query metrics exclusively through version-controlled semantic models (dbt MetricFlow, Cube.js, **Apache Ossie**); never invent ad-hoc SQL joins across unverified tables.
- **Apache Ossie Interchange**: leverage Apache Ossie (Open Semantic Specification Interchange) for portable semantic model definitions across MetricFlow, Cube.js, and other semantic layers — enables vendor-neutral metric portability.
- **FastMCP Anti-Hallucination Gateway**: mediate agent access through FastMCP with `sqlglot` AST validation:
  - assert single read-only `SELECT` (prohibit mutations, multi-statements, and arbitrary subqueries)
  - enforce join complexity depth $\le 3$ joins to prevent Cartesian fanout and chasm traps
  - enforce hard row limit $\le 1000$ rows
  - honor `agent_accessible: true` allowlist and enforce "Show-The-Definition" attribution (lineage + SQL formula)
- **DuckDB/Polars In-Process Resource Ceilings**:
  - enforce local memory caps: `SET max_memory = '4GB';` with temporary NVMe disk spilling (`/tmp/duckdb_spill`)
  - use zero-copy Apache Arrow C Data Interface between DuckDB and Polars (`con.execute(q).pl()`)
  - evaluate datasets larger than RAM using Polars LazyFrames with streaming engine (`collect(streaming=True)`)
  - **DuckDB v2.0 readiness**: prepare for breaking storage format, VARIANT type support, and Quack server mode for remote query execution
- **Agent Query Cost FinOps**: track AI agent query execution costs (token usage, compute time, scanned bytes) as a dedicated FinOps line item; enforce per-agent query cost budgets and alerting thresholds
- **Statistical Distribution Drift Testing**:
  - compute Population Stability Index (PSI) using baseline decile quantile bins: $<0.10$ (stable), $0.10\text{--}0.25$ (moderate drift), $>0.25$ (significant drift; halt automated pipelines)
  - run Two-Sample Kolmogorov-Smirnov (KS) tests on continuous metrics; flag shifts when $p < 0.01$
  - compute non-parametric outlier boundaries using Tukey's IQR fences ($Q_1 - 1.5\text{IQR}$, $Q_3 + 1.5\text{IQR}$)
- **Causal Inference & Pearson SRM Pre-Checks**:
  - execute Pearson's Chi-squared SRM test on A/B test sample counts; if $p < 0.001$, **ABORT EVALUATION IMMEDIATELY**
  - formalize causal hypotheses in DOT-formatted Causal DAGs; identify treatment effects via Backdoor Criterion
  - strictly avoid Collider Bias (Berkson's Paradox): never condition on colliders ($T \rightarrow C \leftarrow Y$)
  - execute 3-way DoWhy refutations: Placebo Treatment ($p > 0.05$), Random Common Cause ($< 10%$ shift), Data Subset ($< 15%$ shift)
- **Two-Column Table of Evidence**: separate empirical observations (facts) from analytical interpretations in all outputs.
- **Uncertainty Calibration & Provenance**: report 95% confidence intervals, standardized effect sizes, Parquet SHA-256 hashes, and verify 0.00% variance against independent ledger control totals.
- **PII & Security**: classify datasets per `data-classification.yaml`; mask PII; enforce OWASP ASI guardrails.

## Suggested Process

### 1. Frame Question & Query FastMCP Semantic Gateway
Define business decision context, target grain, and time range. Retrieve canonical metrics and dimensions via the FastMCP semantic tool interface. Verify `agent_accessible: true` and obtain underlying SQL formulas. **Query through Apache Ossie interchange format for vendor-neutral semantic model portability.**

### 2. In-Process Profiling via DuckDB/Polars (< 4GB RAM)
Scan partitioned Parquet files or Iceberg snapshots locally using DuckDB with `SET max_memory = '4GB';` and NVMe spill. Profile column null rates, cardinalities, and transfer Arrow batches zero-copy into Polars. **Prepare for DuckDB v2.0 breaking storage format, VARIANT support, and Quack server mode.**

### 3. Execute Statistical Drift & Anomaly Tests
Compute vectorized PSI against historical baseline deciles. Evaluate continuous variables using Two-Sample KS-tests ($p < 0.01$). Isolate transient spikes using Tukey's IQR fences to score anomalies.

### 4. Causal Identification, SRM Gate & DoWhy Refutations
For A/B experiments or policy decisions:
1. Run Pearson's Chi-squared SRM pre-check; halt if $p < 0.001$.
2. Construct Causal DAG in DOT format; verify Backdoor Criterion; avoid conditioning on colliders.
3. Estimate Average Treatment Effect (ATE) with 95% CI (or apply CUPED / DML).
4. Subject estimate to Placebo, Random Common Cause, and Data Subset refuters.

### 5. Track Agent Query Costs (FinOps)
Record token usage, compute time, and scanned bytes per agent query. Enforce per-agent cost budgets and alerting. Tag as FinOps line item in `contracts/schemas/data-analysis-report.json`.

### 6. Populate Table of Evidence & Emit Analysis Report
Populate the two-column Table of Evidence separating empirical data from narrative inferences. Validate and emit `contracts/schemas/data-analysis-report.json`.

## Checklist

- [ ] business question, decision context, and temporal grain explicitly framed
- [ ] canonical metrics retrieved from FastMCP / Semantic Layer (dbt MetricFlow / Cube.js / Apache Ossie); zero ungrounded ad-hoc joins
- [ ] queries validated via `sqlglot` AST (read-only `SELECT`, join depth $\le 3$, row limit $\le 1000$)
- [ ] exploratory queries executed in DuckDB/Polars under 4GB RAM limit with out-of-core spilling
- [ ] statistical distribution drift (PSI, Two-Sample KS-test, IQR fences) calculated and evaluated
- [ ] A/B experiments pass Pearson's Chi-squared SRM pre-check ($p \ge 0.001$); aborted if $p < 0.001$
- [ ] causal claims backed by DOT Causal DAG, Backdoor adjustment, and 3-way DoWhy refutations
- [ ] deliverables strictly separate empirical facts from analytical interpretations in Table of Evidence
- [ ] point estimates accompanied by 95% confidence intervals and 0.00% variance against ledger control totals
- [ ] input Parquet SHA-256 hashes recorded; PII masked per `data-classification.yaml`
- [ ] report emitted and validated against `contracts/schemas/data-analysis-report.json`
- [ ] Apache Ossie interchange format used for vendor-neutral semantic model portability
- [ ] DuckDB v2.0 readiness assessed (breaking storage format, VARIANT support, Quack server mode)
- [ ] agent query costs tracked as FinOps line item (token usage, compute time, scanned bytes)

## Related Skills

- **build-data-pipeline**: Reusable ingestion, lakehouse modeling, and production ETL infrastructure
- **analyze-business-requirements**: Align quantitative metrics with business rules and stakeholder outcomes
- **database-maintenance**: Operational lakehouse maintenance, compaction, and read-only query tuning
- **conduct-research**: External benchmarks and industry data when internal datasets are insufficient
- **write-documentation**: Data dictionaries, metric definitions, and analytical knowledge bases

## Output Contracts

When delivering analysis to stakeholders, BI engineers, or downstream agent workflows, emit:

- `contracts/schemas/data-analysis-report.json` — structured business context, metric definitions, dataset lineage, findings with fact/interpretation indices, anomalies, drift metrics, causal estimates, recommendations, **and agent query costs as FinOps line item**.
- Markdown summary brief providing executive findings, narrative context, and recommended decisions.

## Failure Modes

- **Text-to-SQL hallucination**: AI or analyst crafts ad-hoc SQL with invalid join logic or chasm traps. Mitigation: query through FastMCP Semantic Gateway with `sqlglot` AST validation.
- **Reporting SRM-tainted A/B tests**: computing treatment effect when allocation mechanism is corrupt. Mitigation: mandate automated Pearson Chi-squared SRM abort gate ($p < 0.001$).
- **Conflating correlation with causation**: presenting observational regression as causal proof. Mitigation: enforce Pearl's hierarchy, Causal DAG Backdoor adjustment, and DoWhy refutations.
- **Silent covariate drift**: underlying population shifts invalidate historical conclusions. Mitigation: enforce automated PSI and KS-test distribution drift evaluations before reporting.
- **Unmanaged in-memory spill**: large unpartitioned queries exhaust local RAM. Mitigation: enforce DuckDB `max_memory = '4GB';` and Polars streaming scans.
- **Missing Apache Ossie interchange**: semantic models not portable across vendor layers. Mitigation: adopt Apache Ossie interchange format for vendor-neutral metric portability.
- **Unprepared for DuckDB v2.0**: storage format changes break compatibility. Mitigation: assess breaking storage format, VARIANT support, and Quack server mode readiness.
- **Untracked agent query costs**: AI agent data access lacks FinOps visibility. Mitigation: track token usage, compute time, scanned bytes as dedicated line item.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: classify and mask customer PII; use aggregate summaries in cross-role handoffs.
- **ASI04 Supply Chain**: validate versions of analytics libraries (DuckDB, Polars, scipy, dowhy) against trusted package indexes.
- **ASI05 RCE Guard**: parameterize all analytical scripts; reject string-concatenated SQL queries; enforce AST read-only validation.
- **ASI06 Context & Memory Poisoning**: treat cached analysis and prompt memory as untrusted until verified against live data.
- **ASI07 Inter-Agent Communication**: emit structured `data-analysis-report.json` so downstream decision agents share identical evidence **including agent query costs as FinOps line item**.
- **ASI09 Human-Agent Trust Exploitation**: disclose confidence intervals, statistical limitations, and residual uncertainties honestly.
