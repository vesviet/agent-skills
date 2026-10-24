---
description: Workflow for detecting, containing, investigating, and recovering from data pipeline incidents with DLQ quarantine isolation, RCA, and idempotent replay.
---

## Data Pipeline Incident Workflow

Use this workflow when a data pipeline experiences execution failures, SLA breaches, data contract violations, schema drift, poison pill records, dead-letter surges, or unhandled exceptions in stream or batch processing.

### When To Use

- automated circuit breaker trips on an ingestion pipeline due to elevated error rates
- freshness SLA breached for critical operational or analytical lakehouse datasets
- data contract assertion failure detected by quality gates ("null_check", "uniqueness", "range_check")
- schema drift or unannounced producer schema changes crash ingestion workers
- poison pill payloads flood the pipeline and require Dead-Letter Queue (DLQ) quarantine
- downstream consumers report corrupted, missing, or duplicated metrics

### Prerequisites

- access to pipeline orchestration telemetry, monitoring dashboards, and error logs
- access to quarantine targets (Dead-Letter Queue Kafka topic, Iceberg DLQ table, or S3 quarantine bucket)
- access to version-controlled pipeline definitions and current `contracts/schemas/data-pipeline-spec.json`
- understanding of pipeline idempotency semantics (`MERGE INTO`, deduplication keys, microbatch windows)
- permission boundaries defined for emergency pausing, replay execution, and DDL updates

### Workflow Steps

#### 1. Detect And Classify Pipeline Incident

Role: **Data Engineer**, **SRE**

Identify the incident trigger, evaluate operational telemetry, and determine the blast radius:

- check pipeline alerting sources: circuit breaker trips, freshness SLA breaches, DLQ volume spikes, or contract assertion alarms.
- inspect worker logs and execution metadata: capture the failing job ID, task run ID, commit hash, and error stack trace.
- classify incident severity objectively using standard operational tiers:
  - **Blocking**: production ingestion fully halted, downstream SLAs actively violated, or critical financial/customer-facing metrics corrupted.
  - **Important**: partial partition failures, non-critical downstream delay, or moderate DLQ surge with healthy traffic still progressing.
  - **Follow-Up**: intermittent warnings, non-blocking quality gate alerts, or transient latency spikes within SLA margin.
  - Do not use numeric priority codes.

Use skill: `troubleshoot-service`

#### 2. Contain Blast Radius And Isolate DLQ Quarantine

Role: **Data Engineer**, **DevOps Engineer**

Immediately prevent toxic payloads from contaminating downstream Silver/Gold Medallion layers or AI vector embeddings:

- if the error rate exceeds the circuit breaker threshold (e.g. > 1.0%), verify that the automated circuit breaker has tripped, or manually pause ingestion to stop cascading failures.
- route malformed poison pill records to the designated Dead-Letter Queue (DLQ) or Iceberg quarantine partition (`iceberg_quarantine.dlq_*`) per `quarantine_policy`.
- enable healthy records to continue flowing through the pipeline whenever records can be safely partitioned from invalid payloads.
- verify that write-ahead logs or source event offsets (Kafka offsets, CDC logs) are retained and will not expire before recovery.

#### 3. Scope Impact And Lineage Blast Radius

Role: **Data Engineer**, **Data Analyst**

Determine exactly which downstream systems, tables, and stakeholders are affected by the incident:

- trace column-level and table-level lineage from the degraded node to all downstream consumers.
- identify impacted analytical dashboards, dbt models, feature stores, scheduled exports, and external API feeds.
- flag degraded datasets with metadata notices (e.g., in data catalog or semantic layer) to warn analysts and automated consumers against acting on incomplete or stale data.
- record pre-incident snapshot IDs or table versions for audit and reconciliation baselines.

Use skill: `analyze-data`

#### 4. Perform Root Cause Analysis (RCA) And Contract Audit

Role: **Data Engineer**, **Reviewer**

Inspect quarantined records and audit the ingestion boundary to determine the root cause:

- sample quarantined payloads from the DLQ to inspect exact payload structure, malformed datatypes, unannounced field renames, or invalid nulls.
- audit the producer data against the active `contracts/schemas/data-pipeline-spec.json`:
  - did an upstream producer mutate the schema without incrementing the ODCS contract version?
  - did an unexpected data volume surge cause compute slot or memory starvation?
  - was there an infrastructure network timeout, deadlocked database lock, or corrupted source file?
- document findings in the incident investigation log with reproduction queries.

Use skill: `review-code`

#### 5. Develop Fix And Verify Replay Idempotency

Role: **Data Engineer**, **QA Engineer**

Implement the code or configuration fix and verify that reprocessing will not duplicate or corrupt data:

- update pipeline parsing logic, type coercion, or schema evolution mapping to handle the edge case.
- if an upstream contract violation occurred, coordinate contract adjustments or enforce strict rejection at the boundary.
- author a regression test in an isolated environment using sanitized samples of the quarantined payloads.
- **verify replay idempotency**: confirm that the pipeline uses idempotent `MERGE INTO`, upsert keys, or clean microbatch partition overwrites, guaranteeing that re-processing previously processed windows produces identical results without row duplication.

Use skill: `write-tests`

#### 6. Execute Controlled Quarantine Replay And Recovery

Role: **Data Engineer**, **SRE**

Safely replay quarantined records from the DLQ through the repaired pipeline into the production lakehouse:

- run a canary replay batch (e.g., 5% of quarantined records) and monitor error rates and memory usage.
- upon successful canary verification, execute full DLQ replay in rate-limited batches to prevent exhausting downstream database connection pools or compute budgets.
- execute mathematical reconciliation:
  - verify that total source records = total processed records ($\Delta = 0$).
  - verify that DLQ backlog decreases to zero without new unexpected errors.
- reset the pipeline circuit breaker and restore normal automated scheduling.

Use skill: `build-data-pipeline`

#### 7. Post-Incident Review And Contract Hardening

Role: **Data Engineer**, **Technical Lead**

Capture learnings, formalize post-incident documentation, and harden contracts to prevent recurrence:

- author an incident postmortem and emit `contracts/schemas/incident-report.json`.
- update `contracts/schemas/data-pipeline-spec.json`:
  - harden quality gates ("null_check", "uniqueness", "range_check", "distribution_drift") to catch similar anomalies earlier.
  - adjust compute budget allocations, query timeouts, or DLQ retention policies if resource constraints contributed to the failure.
- review findings with upstream data producers and downstream consumers to close operational feedback loops.

Use skill: `write-documentation`

### Checklist

- [ ] Incident detected and classified by severity (Blocking, Important, Follow-Up) without using numeric priority codes
- [ ] Upstream ingestion circuit breaker evaluated and tripped if error threshold breached
- [ ] Malformed poison pill records isolated to DLQ or Iceberg quarantine table
- [ ] Column-level and table-level lineage traced to identify all downstream consumers and dashboards
- [ ] Impacted analytical tables and dashboards marked degraded to prevent corrupted decision-making
- [ ] Root cause identified through log inspection and audit against `data-pipeline-spec.json`
- [ ] Pipeline parser or transformation bugfix implemented and verified with regression tests
- [ ] Pipeline step idempotency verified (re-running the batch produces zero duplicate records)
- [ ] Controlled quarantine replay executed from DLQ with zero data loss verified
- [ ] Incident postmortem emitted via `incident-report.json` and `data-pipeline-spec.json` contract hardened

### Related Workflows

- [Data Migration](data-migration.md)
- [Troubleshooting](troubleshooting.md)
- [Hotfix Production](hotfix-production.md)
- [Security Incident Response](security-incident-response.md)

### Related Skills

- **build-data-pipeline**: Author, repair, and replay data ingestion pipelines
- **database-maintenance**: Maintain lakehouse storage, compact tables, and inspect partition states
- **troubleshoot-service**: Diagnose ingestion alerts, telemetry anomalies, and circuit breaker trips
- **review-code**: Review transformation logic, schema changes, and SQL queries against data contracts
- **write-tests**: Author regression tests and verify pipeline replay idempotency
- **analyze-data**: Trace lineage blast radius and audit affected downstream analytical metrics
- **write-documentation**: Author incident postmortem and update operational runbooks

### Failure Modes

- **Uncontained poison pill cascade**: malformed payloads bypass DLQ and pollute Silver/Gold Medallion tables. **Mitigation:** enforce pre-ingestion contract assertions with automated isolation on failure.
- **Non-idempotent replay duplication**: replaying DLQ records creates duplicate rows or increments aggregated metrics twice. **Mitigation:** enforce deterministic natural keys and `MERGE INTO` / partition overwrite semantics.
- **Lineage blindspot**: downstream stakeholders make financial or business decisions based on corrupted metrics before incident notification. **Mitigation:** automate downstream status propagation and mark affected datasets as degraded immediately.
- **Circuit breaker thrashing**: rapidly alternating between tripped and untripped states due to overly sensitive thresholds. **Mitigation:** establish evaluation windows (e.g. 15 minutes) and require manual or controlled recovery checks.
- **DLQ message expiration**: quarantined records expire before remediation is deployed. **Mitigation:** configure at least 14 to 30 days retention for quarantine topics and storage partitions.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/incident-report.json`** — capture incident timeline, root cause analysis, affected services/datasets, financial or operational impact, and preventative actions.
- **`contracts/schemas/data-pipeline-spec.json`** — updated data contract specification with hardened quality gates, modified schema fields, or updated quarantine policies.

### Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: restrict DLQ replay execution privileges to authorized Data Engineering identities; never run replay jobs with blanket superuser credentials.
- **ASI05 RCE Guard**: never evaluate raw string expressions from quarantined payloads directly in dynamic SQL or runtime execution engines.
- **ASI06 Memory & Context Poisoning**: prevent malformed or adversarial ingestion payloads from contaminating AI Agent retrieval stores or semantic layers.
- **ASI07 Inter-Agent Communication**: notify coordinating agents and consuming roles using structured contract status updates rather than unvalidated freeform logs.
- **ASI09 Human-Agent Trust Exploitation**: disclose incident blast radius, data loss metrics, and recovery status transparently without concealing anomalies.
