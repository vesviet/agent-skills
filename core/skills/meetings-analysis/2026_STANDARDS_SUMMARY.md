# 2026 Meetings-Analysis Standards & Patterns — Consolidated Research Summary

## Overview
Deep research conducted September 2026 across AI-assisted requirements engineering, data analysis with semantic layers, and structured meeting review with agentic ADR generation.

---

## 1. AI-Assisted Requirements Engineering (2026)

### Epic-Organized Gherkin Generation (arXiv:2607.01980, SEET 2026)
- **4-step async LLM pipeline**:
  1. **Relevance Classification** (LLM #1): Detect requirement-relevant content in transcriptions/inputs
  2. **Requirements Update** (LLM #2): Add/revise items in living requirements list
  3. **Epic & Mind Map Generation** (LLM #3): Group requirements into 3–6 epics with relationships
  4. **Gherkin Generation** (LLM #4): Produce Feature blocks + Scenarios (JSON-constrained)
- **Expert preference**: Epic-organized scores higher on Correctness (4.61 vs 4.14), Executability (4.61 vs 4.07), Completeness (4.31 vs 3.50)
- **Structural validity**: 99%+ for JSON-constrained pipeline
- **SSE real-time state updates**: Stream requirements/epic/Gherkin changes for living documentation

### LLM-as-Judge Validation (2026)
- **DeepEval/RAGAS**: Independent LLM evaluation for clarity, completeness, internal consistency
- **Critical finding**: AI-generated AC can pass human review while containing subtle contradictions
- **Blind expert assessment** required alongside automated evaluation

### Living Requirements Traceability (2026)
- **AI-assisted tools**: Trace.space, getleo.ai link requirements → design docs → code modules → test cases
- **Mandatory for EU AI Act compliance**: Chain-of-causality audit trails for regulated industries
- **Automated CI checks** for traceability freshness to prevent link rot

### Agentic AC Format (2026)
- **Deterministic observable assertions**: Not prose intent; agents auto-validate implementation output
- **Epic → Feature Block → Scenarios** hierarchy for agentic delivery

### Human BA Sign-Off Gate (2026)
- **Mandatory** for AI-assisted AC before sprint commitment
- **EU AI Act compliance** for high-risk features

---

## 2. Data Analysis with Semantic Layers (2026)

### Apache Ossie (Incubating) — Universal Semantic Layer Standard
- **Accepted into Apache Incubator** (July 10, 2026): Formerly Open Semantic Interchange (OSI)
- **Vendor-neutral YAML standard** for metrics, dimensions, joins — single source of truth
- **50+ organization coalition**: Alation, Anomalo, Atlan, AtScale, Bigeye, BlackRock, Blue, Collate, Databao, Denodo, Kyvos, Qlik, Salesforce, Snowflake
- **Core Classes**: Metrics at semantic model level (not dataset); reference fields from multiple datasets
- **Multiple SQL dialects**: ANSI_SQL, SNOWFLAKE, DATABRICKS, MDX, TABLEAU
- **DuckDB Community Extension**: Reads Ossie YAML/JSON, answers semantic queries, exposes via MCP
- **Dosi + Ossie**: 10-minute semantic layer for AI agents (CLI, API, MCP unified)

### DuckDB v2.0 Readiness (2026)
- **Breaking storage format** — prepare migration
- **VARIANT type support** — semi-structured data handling
- **Quack server mode** — remote query execution via HTTP-based client-server protocol
- **Iceberg extension**: full DML (INSERT/UPDATE/DELETE), process 1TB in 30 seconds
- **Local-first ETL/ELT studio (duckle)**: Drag-and-drop visual pipeline designer compiling to SQL
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
- **DoWhy simplified API**: `dowhy.api` for model → estimate → identify → refute workflow

### Statistical Distribution Drift Testing (2026)
- **Population Stability Index (PSI)**: baseline decile quantile bins; <0.10 stable, 0.10-0.25 moderate, >0.25 significant (halt pipelines)
- **Two-Sample Kolmogorov-Smirnov**: p < 0.01 flag shifts
- **Tukey's IQR fences**: Q1 - 1.5×IQR, Q3 + 1.5×IQR for non-parametric outlier boundaries

### Agent Query Cost FinOps (2026)
- **Token usage, compute time, scanned bytes** tracked per agent query
- **Per-agent query cost budgets** with alerting thresholds
- **Dedicated FinOps line item** in data-analysis-report.json

---

## 3. Structured Meeting Review & Agentic ADR Generation (2026)

### GADR Agentic ADR Pipeline (arXiv:2608.17694, SBES 2026)
- **Multi-agent, self-correcting workflow**: raw meeting transcriptions → critique → Nygard-formatted ADR drafts
- **Feasibility study**: 5 real project meetings, 4 senior architects, 15 students; captures most expert-identified decisions
- **Agentic RAG advantage**: Structural consistency + richer architectural explanations; critique stage reduces overlaps/fragmentation
- **Human-in-the-loop validation**: Every recorded meeting → reviewable ADR draft with human validation

### Nygard ADR Format with AI Controls (2026)
- **Structure**: Context → Decision → Rationale → Controls/Safeguards → Consequences → Related Records
- **AI Controls & Safeguards**: Model version control, prompt/output logging, human-in-loop validation, egress controls, rollback plan, DevSecOps integration
- **ADR Lifecycle**: Proposed → Accepted → Superseded (immutable after acceptance, never modified)
- **Supersession Pattern**: Old ADR status = superseded, linked to new ADR; never delete
- **Explicit ADR Ownership**: Team establishes definition of ownership per ADR

### Async-First Decision Protocol (2026)
- **Written RFC/brief + 48-72h async comment window** before any sync call
- **Decisions in ephemeral chat without ADR = anti-pattern**
- **DACI Framing**: Driver, Approver, Contributors, Informed; EXACTLY ONE Approver per decision
- **Consensus paralysis from committee approval = prohibited**

### AI-Synthesized Perspective Guardrails (2026)
- **Explicit labeling**: `[AI-synthesized]` for automated reasoning vs human domain knowledge
- **Inferred risks marked**: `[INFERRED — requires human validation]` when not grounded in code/docs
- **Prune ungrounded AI perspectives**: Cannot ground in code path, requirement, or stakeholder constraint → remove
- **Human sign-off gate MANDATORY** for architectural decisions, breaking changes, release-blocking recommendations
- **AI-synthesized consensus ≠ cross-functional team alignment**

### Decision Intelligence & Agentic AI Governance (2026)
- **DecisionCAMP 2026**: Intelligent Decision Services integrated into enterprise architectures
- **Agentic AI in EDA**: Multi-agent systems for autonomous goal-driven decision-making
- **Critical questions**: Who/what is in control? Trust, accountability, explainability, oversight
- **Interoperability standards**: Ontology-driven approaches for agentic AI adoption

---

## 4. Cross-Skill Integration Patterns

### Requirements → Data → Review Flow
```
1. analyze-business-requirements
   ├── Epic-organized Gherkin pipeline (4-step async LLM + SSE)
   ├── LLM-as-judge validation (DeepEval/RAGAS)
   ├── Living traceability (requirements → design → code → tests)
   ├── Agentic AC format (deterministic assertions)
   ├── Human BA sign-off gate (EU AI Act)
   └── Delegates to Data Analyst / SEO Analyst / Researcher via feature-ticket.json
       ↓
2. analyze-data
   ├── Apache Ossie semantic layer (vendor-neutral YAML)
   ├── FastMCP sqlglot AST validation (read-only, join≤3, rows≤1000)
   ├── DuckDB v2.0 readiness (breaking format, VARIANT, Quack)
   ├── Zero-copy Arrow DuckDB→Polars + streaming LazyFrames
   ├── DoWhy 3-way refutations + SRM hard abort (p<0.001)
   ├── PSI/KS/IQR drift testing (PSI>0.25 = halt)
   ├── FinOps agent query cost tracking (token/compute/bytes)
   └── Dosi + Ossie 10-min AI agent semantic layer
       ↓
3. meeting-review
   ├── GADR agentic ADR pipeline (transcript → critique → ADR)
   ├── Nygard ADR with AI Controls/Safeguards
   ├── Async-first RFC + 48-72h comment window
   ├── DACI single-approver framing
   ├── AI perspective guardrails ([AI-synthesized], [INFERRED], pruning)
   └── Human sign-off mandatory for architectural/breaking/release decisions
```

---

## 5. Required Contract Schemas (2026)

### New Schemas to Create
| Schema | Owner Skill | Purpose |
|--------|-------------|---------|
| `epic-organized-gherkin-spec.json` | analyze-business-requirements | 4-step pipeline config |
| `llm-as-judge-validation-spec.json` | analyze-business-requirements | DeepEval/RAGAS criteria |
| `living-traceability-spec.json` | analyze-business-requirements | Requirements→code links |
| `agentic-ac-spec.json` | analyze-business-requirements | Deterministic assertions |
| `apache-ossie-semantic-spec.json` | analyze-data | YAML model definitions |
| `dosi-ossie-agent-spec.json` | analyze-data | 10-min AI agent setup |
| `fastmcp-sqlglot-spec.json` | analyze-data | AST validation config |
| `duckdb-v2-readiness-spec.json` | analyze-data | Migration checklist |
| `dowhy-causal-spec.json` | analyze-data | DOT DAG + refutation config |
| `finops-agent-query-spec.json` | analyze-data | Cost tracking with budgets |
| `gadr-adr-pipeline-spec.json` | meeting-review | Agentic ADR generation |
| `nygard-adr-ai-controls-spec.json` | meeting-review | ADR format with AI safeguards |
| `async-decision-protocol-spec.json` | meeting-review | RFC + comment window |
| `daci-decision-spec.json` | meeting-review | Single-approver framing |
| `ai-perspective-guardrails-spec.json` | meeting-review | Labeling/pruning rules |

---

## 6. Implementation Priority Matrix

| Priority | analyze-business-requirements | analyze-data | meeting-review |
|----------|------------------------------|--------------|----------------|
| **P0** | Epic-organized Gherkin pipeline (4-step + SSE) | Apache Ossie universal semantic layer | GADR agentic ADR pipeline |
| **P0** | LLM-as-judge validation (DeepEval/RAGAS) | DuckDB v2.0 readiness | Nygard ADR with AI Controls |
| **P0** | Living traceability (Trace.space/getleo.ai) | FastMCP sqlglot AST + MCP Registry | Async-first RFC + 48-72h window |
| **P0** | Agentic AC format (deterministic assertions) | DoWhy 3-way refutations + SRM abort | DACI single-approver framing |
| **P0** | Human BA sign-off gate (EU AI Act) | FinOps agent query cost tracking | AI perspective guardrails |
| **P1** | SSE real-time state updates | Dosi + Ossie 10-min AI agent layer | Human sign-off gate for arch decisions |
| **P1** | | Zero-copy Arrow + streaming LazyFrames | ADR lifecycle management |
| **P1** | | DuckLake/quacklake time-travel queries | |
| **P2** | Expanded failure modes | Expanded failure modes | Expanded failure modes |
| **P2** | Output contract updates | Output contract updates | Output contract updates |

---

## 7. Validation Gates (All Skills)

1. **Pack validation**: `python3 core/scripts/validate-all.py` from agent-skills root
2. **INDEX.md regeneration**: `python3 core/scripts/generate-index.py` if VERSION bumped
3. **Adapter parity**: `validate-rules.py` (9 parity groups)
4. **Skill-specific tests**:
   - Epic-organized Gherkin pipeline on PURE dataset (107 requirements)
   - LLM-as-judge scores vs expert blind assessment
   - Traceability link freshness in CI
   - Apache Ossie YAML round-trip (MetricFlow → Ossie → Cube.js)
   - DuckDB v2.0 storage format migration on test datasets
   - FastMCP sqlglot AST validation rejects invalid queries
   - DoWhy 3-way refutations catch known causal errors
   - PSI > 0.25 triggers pipeline halt
   - FinOps cost tracking per agent query with budget enforcement
   - GADR pipeline on real transcripts with expert ground truth
   - ADR immutability enforcement in CI
   - Async-first protocol compliance (RFC before call)
   - DACI single-approver enforcement
   - AI perspective labeling and pruning logic
   - Human sign-off gate blocks AI-only consensus

---

## 8. Key References

- **Epic-Organized Gherkin**: arXiv:2607.01980 (SEET 2026)
- **AutoUAT Industrial Case Study**: arXiv:2504.07244
- **Gherkin Guidelines for AI**: github.com/AutomationPanda/gherkin-guidelines-for-ai
- **Apache Ossie**: ossie.apache.org (Incubating, July 2026)
- **DuckDB v2.0**: motherduck.com/duckdb-news
- **FastMCP**: sqlglot AST validation, MCP Registry
- **DoWhy Causal Inference**: pywhy.org/dowhy
- **GADR Agentic ADR**: arXiv:2608.17694 (SBES 2026)
- **Nygard ADR**: martinfowler.com/bliki/ArchitectureDecisionRecord.html
- **DecisionCAMP 2026**: 2026.declarativeai.net/decisioncamp
- **EU AI Act**: Regulation (EU) 2026/1744, Article 14 Human Oversight