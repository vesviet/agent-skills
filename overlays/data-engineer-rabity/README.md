# Data Engineer Rabity — Learning Overlay

Personal learning overlay for the `data-engineer` role. This overlay extends
`core/roles/data-engineer.md` with a structured 10-phase self-study roadmap,
hands-on project conventions, and skill-gating rules calibrated to Rabity's
current progression.

This overlay is **persona-scoped**: it applies only when operating in the context
of Rabity's personal data engineering practice. It does NOT replace the global
`core/roles/data-engineer.md` — it composes on top of it.

## Scope

- **Learner:** Rabity
- **Base Role:** `core/roles/data-engineer.md`
- **Goal:** Structured progression from SQL fundamentals to production-grade
  data engineering (Lakehouse, Streaming, Observability)
- **Horizon:** ~25 weeks (continuous thereafter for portfolio)

## Roadmap Overview

| Phase | Module                       | Duration | Status   |
| ----- | ---------------------------- | -------- | -------- |
| 1     | SQL + Analytics Foundation   | 2 tuần   | Active   |
| 2     | Python Data Stack            | 3 tuần   | Upcoming |
| 3     | Parquet + DuckDB + Polars    | 2 tuần   | Upcoming |
| 4     | ETL/ELT Architecture         | 3 tuần   | Upcoming |
| 5     | Airflow + Scheduling         | 2 tuần   | Upcoming |
| 6     | Data Warehouse Modeling      | 3 tuần   | Upcoming |
| 7     | Streaming / Kafka            | 4 tuần   | Upcoming |
| 8     | Lakehouse + Big Data         | 4 tuần   | Upcoming |
| 9     | Observability + Data Quality | 2 tuần   | Upcoming |
| 10    | Portfolio Projects           | Liên tục | Ongoing  |

## Included

- `rules/learning-conventions.md` — Session protocol, phase gates, output standards
- `rules/phase-roadmap.md` — Per-phase curriculum, tools, deliverables, exit criteria

## Activation

When Rabity begins a study or practice session, load this overlay:

```
Role: data-engineer
Overlay: overlays/data-engineer-rabity
```

The agent MUST then enforce phase gates (see `rules/learning-conventions.md`)
before allowing work on a module that has not yet been unlocked.
