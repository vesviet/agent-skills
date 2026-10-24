# analyze-data — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Apache Ossie (Incubating) — Universal Semantic Layer Standard (2026)
- **Accepted into Apache Incubator** (July 10, 2026): Formerly Open Semantic Interchange (OSI)
- **Vendor-neutral YAML standard** for metrics, dimensions, joins — single source of truth across AI agents, BI platforms, analytics tools
- **50+ organizations** in coalition: Alation, Anomalo, Atlan, AtScale, Bigeye, BlackRock, Blue, Collate, Databao, Denodo, Kyvos, Qlik, Salesforce, Snowflake, AtScale
- **Core Classes**: Metrics defined at semantic model level (not dataset), reference fields from multiple datasets; multiple SQL dialects (ANSI_SQL, SNOWFLAKE, DATABRICKS, MDX, TABLEAU)
- **DuckDB Community Extension**: Reads Ossie YAML/JSON, answers semantic queries, exposes via MCP
- **Dosi + Ossie**: 10-minute semantic layer for AI agents (CLI, API, MCP unified)

### DuckDB v2.0 Readiness (2026)
- **Breaking storage format** — prepare migration
- **VARIANT type support** — semi-structured data handling
- **Quack server mode** — remote query execution via HTTP-based client-server protocol
- **Iceberg extension**: full DML (INSERT/UPDATE/DELETE), process 1TB in 30 seconds
- **Local-first ETL/ELT studio (duckle)**: Drag-and-drop visual pipeline designer compiling to SQL, git-friendly JSON workspaces
- **quack-on-demand**: Arrow FlightSQL gateway for DuckDB + DuckLake with multi-tenant pools
- **quacklake**: DuckLake catalog on quack deployed to Cloudflare Workers with Durable Objects + JWT auth

### FastMCP Anti-Hallucination Gateway (2026)
- **sqlglot AST validation**: single read-only SELECT, join depth ≤ 3, row limit ≤ 1000
- **agent_accessible: true allowlist** with "Show-The-Definition" attribution (lineage + SQL formula)
- **MCP Registry Integration**: External tools via MCP Registry for developer workflows

### Polars 0.20+ / DuckDB 1.2+ Performance (2026)
- **Polars 11.4× speedup** over Pandas on 10M rows (filter + groupby aggregation)
- **DuckDB 9.7× speedup** with zero Python boilerplate
- **Peak memory**: DuckDB 0.5 GB vs Pandas 4.2 GB (5.3× less)
- **Zero-copy Arrow C Data Interface**: `con.execute(q).pl()` between DuckDB and Polars
- **Polars LazyFrames streaming**: `collect(streaming=True)` for datasets larger than RAM

### Causal Inference & A/B Testing Standards (2026)
- **DoWhy 3-way refutations**: Placebo Treatment (p > 0.05), Random Common Cause (< 10% shift), Data Subset (< 15% shift)
- **Pearson's Chi-squared SRM pre-check**: ABORT if p < 0.001
- **Causal DAG in DOT format**: Backdoor Criterion verification, Collider Bias avoidance
- **Pearl's Hierarchy enforcement**: No observational regression as causal proof

### Statistical Distribution Drift Testing (2026)
- **Population Stability Index (PSI)**: baseline decile quantile bins; <0.10 stable, 0.10-0.25 moderate, >0.25 significant (halt pipelines)
- **Two-Sample Kolmogorov-Smirnov**: p < 0.01 flag shifts
- **Tukey's IQR fences**: Q1 - 1.5×IQR, Q3 + 1.5×IQR for non-parametric outlier boundaries

### Agent Query Cost FinOps (2026)
- **Token usage, compute time, scanned bytes** tracked per agent query
- **Per-agent query cost budgets** with alerting thresholds
- **Dedicated FinOps line item** in data-analysis-report.json

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Apache Ossie interchange mentioned | **Apache Ossie (Incubating) as universal standard**: YAML config, vendor-neutral, 50+ org coalition, DuckDB extension, Dosi 10-min setup |
| DuckDB v1.x assumptions | **DuckDB v2.0 readiness**: breaking storage format, VARIANT type, Quack server mode, Iceberg full DML |
| FastMCP gateway mentioned | **sqlglot AST validation**: read-only SELECT, join depth ≤ 3, row limit ≤ 1000, agent_accessible allowlist, Show-The-Definition |
| Polars/DuckDB performance | **Polars 0.20+/DuckDB 1.2+**: 11.4×/9.7× speedup, zero-copy Arrow, streaming LazyFrames |
| Causal inference with DoWhy | **DoWhy 3-way refutations + SRM abort gate**: Placebo, Random Common Cause, Data Subset; Pearson Chi-squared p < 0.001 = ABORT |
| Agent query cost tracking | **FinOps line item**: token usage, compute time, scanned bytes per agent query with budgets |

### 2. New 2026 Patterns to Add
- **Apache Ossie Semantic Model YAML** authoring and import/export workflow
- **Dosi + Ossie 10-minute AI agent semantic layer** (CLI/API/MCP unified)
- **DuckDB v2.0 migration readiness** checklist (storage format, VARIANT, Quack)
- **FastMCP sqlglot AST validation** pipeline with MCP Registry integration
- **Zero-copy DuckDB→Polars Arrow interface** for in-process analytics
- **DuckLake ACID lakehouse** with time-travel queries via quacklake
- **DoWhy causal inference API** (simplified: model → estimate → identify → refute)
- **Automated PSI/KS/IQR drift testing** pipeline with pipeline halt on PSI > 0.25
- **FinOps agent query cost tracking** with per-agent budgets and alerting

### 3. Checklist Additions
- [ ] Apache Ossie YAML semantic model authored/imported for all canonical metrics
- [ ] Ossie interchange format used for vendor-neutral portability (MetricFlow ↔ Cube.js ↔ Ossie)
- [ ] DuckDB v2.0 readiness assessed: breaking storage format, VARIANT support, Quack server mode
- [ ] FastMCP sqlglot AST validation: read-only SELECT, join depth ≤ 3, row limit ≤ 1000
- [ ] agent_accessible: true allowlist enforced with Show-The-Definition attribution
- [ ] MCP Registry integration for external tool workflows
- [ ] Zero-copy Arrow C Data Interface: `con.execute(q).pl()` DuckDB → Polars
- [ ] Polars LazyFrames streaming: `collect(streaming=True)` for >RAM datasets
- [ ] DuckLake ACID time-travel queries via quacklake (Cloudflare Workers + Durable Objects)
- [ ] DoWhy 3-way refutations: Placebo (p > 0.05), Random Common Cause (< 10%), Data Subset (< 15%)
- [ ] Pearson Chi-squared SRM pre-check: ABORT if p < 0.001
- [ ] Causal DAG in DOT format with Backdoor Criterion verified
- [ ] PSI computed against baseline deciles: <0.10 stable, 0.10-0.25 moderate, >0.25 halt pipelines
- [ ] Two-Sample KS-test on continuous metrics: flag shifts at p < 0.01
- [ ] Tukey's IQR fences for non-parametric outlier detection
- [ ] Agent query costs tracked: token usage, compute time, scanned bytes as FinOps line item
- [ ] Per-agent query cost budgets with alerting thresholds enforced
- [ ] Input Parquet SHA-256 hashes recorded; PII masked per data-classification.yaml
- [ ] Two-Column Table of Evidence: empirical facts vs analytical interpretations separated

### 4. Failure Mode Additions
- **Ossie model drift**: Semantic definitions diverge across tools. Mitigation: Ossie as single source of truth, automated sync validation.
- **DuckDB v2.0 migration break**: Storage format change breaks existing Parquet/Iceberg. Mitigation: Pre-migration compatibility testing, dual-format support during transition.
- **FastMCP bypass**: Agent crafts raw SQL bypassing semantic gateway. Mitigation: Enforce MCP Registry as only access path, audit query logs.
- **SRM-tainted A/B test**: Proceeding with evaluation despite allocation corruption. Mitigation: Hard ABORT gate at p < 0.001, no override.
- **Collider bias in causal inference**: Conditioning on T → C ← Y. Mitigation: DOT DAG verification, automated collider detection.
- **Unbounded agent query costs**: AI agent scans petabytes unchecked. Mitigation: Per-agent budget enforcement, automatic query termination.
- **Quack server mode security**: Remote query execution exposure. Mitigation: JWT auth, Durable Objects isolation, rate limiting.

### 5. Output Contract Updates
- Add `contracts/schemas/apache-ossie-semantic-spec.json` for YAML model definitions
- Add `contracts/schemas/dosi-ossie-agent-spec.json` for 10-min AI agent setup
- Add `contracts/schemas/fastmcp-sqlglot-spec.json` for AST validation config
- Add `contracts/schemas/duckdb-v2-readiness-spec.json` for migration checklist
- Add `contracts/schemas/dowhy-causal-spec.json` for DOT DAG + refutation config
- Add `contracts/schemas/finops-agent-query-spec.json` for cost tracking
- Update `contracts/schemas/data-analysis-report.json` with 2026 fields

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Apache Ossie as universal semantic standard (YAML, vendor-neutral) | High |
| P0 | DuckDB v2.0 readiness (breaking format, VARIANT, Quack) | High |
| P0 | FastMCP sqlglot AST validation + MCP Registry | High |
| P0 | DoWhy 3-way refutations + SRM hard abort gate | High |
| P1 | FinOps agent query cost tracking with budgets | Medium |
| P1 | Dosi + Ossie 10-min AI agent semantic layer | Medium |
| P1 | Zero-copy Arrow DuckDB→Polars + streaming LazyFrames | Medium |
| P1 | Automated PSI/KS/IQR drift testing with pipeline halt | Medium |
| P2 | DuckLake/quacklake time-travel queries | Medium |
| P2 | Expanded failure modes | Low |
| P2 | Output contract updates | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test Apache Ossie YAML round-trip (MetricFlow → Ossie → Cube.js)
- Validate DuckDB v2.0 storage format migration on test datasets
- Test FastMCP sqlglot AST validation rejects invalid queries
- Verify DoWhy 3-way refutations catch known causal inference errors
- Test PSI > 0.25 triggers pipeline halt
- Verify FinOps cost tracking per agent query with budget enforcement