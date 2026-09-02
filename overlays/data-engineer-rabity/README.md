# Data Engineer Rabity — Learning Overlay

Personal learning overlay for the `data-engineer` role. Extends `core/roles/data-engineer.md` with a structured 10-phase self-study roadmap, hands-on project conventions, and skill-gating rules.

**Persona-scoped**: applies only when operating in the context of Rabity's personal data engineering practice.

## Scope

- **Learner:** Rabity
- **Base Role:** `core/roles/data-engineer.md`
- **Goal:** Structured progression from SQL fundamentals to production-grade data engineering (Lakehouse, Streaming, Observability)
- **Horizon:** ~25 weeks (continuous thereafter for portfolio)

## 2026 Toolchain Updates

| Phase | Tool | 2026 Version |
|-------|------|-------------|
| 3 | DuckDB | Latest + Iceberg extension |
| 4 | ETL/ELT | dbt Core **1.9** (microbatch incremental strategy) |
| 5 | Airflow | 2.9+ |
| 6 | dbt modeling | dbt Core 1.9 + Kimball, Star Schema |
| 7 | Kafka | Confluent/Redpanda 2026 |
| 8 | Lakehouse | **Apache Iceberg** (REST Catalog) + Delta Lake + Spark 3.5 |
| 9 | Observability | Great Expectations v1 + dbt tests |

### Phase 8 Updated Focus (Lakehouse 2026)
Apache Iceberg is the **production standard** for analytics lakehouses. Phase 8 now covers:
- Iceberg REST Catalog (AWS Glue, Nessie, Lakekeeper) — NOT path-based scanning
- Table maintenance: compaction, snapshot expiration, orphan file removal
- DuckDB ↔ Iceberg integration (`INSTALL iceberg; LOAD iceberg;`)
- Medallion architecture: Bronze (raw) → Silver (staged) → Gold (marts)

### dbt 1.9 Microbatch (Phase 6 Addition)
```yaml
# microbatch incremental — parallelizable time-chunked processing
materialized: incremental
incremental_strategy: microbatch
event_time: created_at
batch_size: day
```

## Roadmap Overview

| Phase | Module | Duration | Status |
|-------|--------|----------|--------|
| 1 | SQL + Analytics Foundation | 2 tuần | Active |
| 2 | Python Data Stack | 3 tuần | Upcoming |
| 3 | Parquet + DuckDB + Polars | 2 tuần | Upcoming |
| 4 | ETL/ELT Architecture (dbt 1.9) | 3 tuần | Upcoming |
| 5 | Airflow + Scheduling | 2 tuần | Upcoming |
| 6 | Data Warehouse Modeling (dbt 1.9) | 3 tuần | Upcoming |
| 7 | Streaming / Kafka | 4 tuần | Upcoming |
| 8 | Lakehouse + Iceberg (REST Catalog) | 4 tuần | Upcoming |
| 9 | Observability + Data Quality | 2 tuần | Upcoming |
| 10 | Portfolio Projects | Liên tục | Ongoing |

## Included

- `rules/learning-conventions.md` — Session protocol, phase gates, output standards
- `rules/phase-roadmap.md` — Per-phase curriculum, tools, deliverables, exit criteria

## Activation

```
Role: data-engineer
Overlay: overlays/data-engineer-rabity
```

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

Last updated: 2026-09-01
