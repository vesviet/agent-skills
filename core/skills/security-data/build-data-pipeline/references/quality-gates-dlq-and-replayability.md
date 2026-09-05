# Quality Gates, DLQ Quarantine & Deterministic Replayability — Reference

This reference establishes standards and implementation protocols for automated data quality gates (Great Expectations & dbt-expectations), Dead-Letter Queue (DLQ) quarantine isolation, and deterministic replayability for enterprise data pipelines.

---

## 1. Automated Data Quality (Great Expectations & dbt-expectations)

Data pipelines must enforce declarative quality assertions at each layer boundary (Bronze → Silver → Gold) to prevent data corruption from propagating downstream.

### 1.1 Quality Assertion Tiers

| Tier | Behavior on Failure | Scope of Rules | Example Assertions |
|---|---|---|---|
| **Critical** | Pipeline halted immediately; records routed to DLQ; alert dispatched | Primary keys, foreign key referential integrity, schema types, non-null guarantees | `expect_column_values_to_be_unique`<br>`expect_column_values_to_not_be_null` |
| **Advisory** | Warning emitted to monitoring catalog; processing continues | Statistical drift, expected volume bounds, categorical frequency | `expect_table_row_count_to_be_between`<br>`expect_column_quantile_values_to_be_between` |

### 1.2 Declarative dbt-expectations & Great Expectations Rules

```yaml
# Example: dbt schema test configuration
version: 2

models:
  - name: silver_orders
    tests:
      - dbt_expectations.expect_table_row_count_to_be_between:
          min_value: 1000
          max_value: 5000000
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: gross_amount_usd
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0.00
              max_value: 100000.00
      - name: status
        tests:
          - accepted_values:
              values: ['PENDING', 'PAID', 'SHIPPED', 'CANCELLED', 'REFUNDED']
```

---

## 2. Dead-Letter Queue (DLQ) Quarantine Architecture

Invalid, malformed, or contract-violating records must never be discarded silently, nor should single record defects crash multi-million-row batch pipelines. Defective records must be isolated into a structured DLQ quarantine store.

### 2.1 Standard DLQ Quarantine Schema

```json
{
  "quarantine_id": "7f8b89e2-3456-42ab-8c9e-10816b801a23",
  "source_system": "kafka.payments.raw",
  "payload_raw": "{\"order_id\": \"98124\", \"gross_amount\": -45.00, \"status\": \"UNKNOWN\"}",
  "failure_stage": "silver_contract_validation",
  "error_code": "ERR_CONTRACT_CHECK_FAILED",
  "violated_contract_rule": "chk_positive_order_amount",
  "quarantined_at": "2026-09-05T05:30:00Z",
  "trace_id": "trace-98a72b0c-4d32"
}
```

### 2.2 Quarantine Circuit-Breaker
- **Threshold Limit**: Ingestion workers calculate the quarantine ratio:
  $$\text{Quarantine Rate} = \frac{\text{Quarantined Rows}}{\text{Total Batch Rows}} \times 100\%$$
- **Circuit Trip**: If the quarantine rate exceeds **1.0%** of total batch volume, the pipeline halts immediately, rolls back the uncommitted transaction, and triggers high-severity incident notifications.

---

## 3. Deterministic Replayability & Idempotency Protocol

Data pipelines must support re-running any historical processing window without creating duplicates, losing state, or leaving orphaned records.

### 3.1 Transactional Upsert / MERGE Mechanics
All Silver and Gold writes must utilize idempotent `MERGE INTO` operations keyed on the immutable natural primary key:

```sql
MERGE INTO lakehouse.silver.orders AS target
USING staging_orders AS source
ON target.order_id = source.order_id
WHEN MATCHED AND source._ingested_at > target._ingested_at THEN
  UPDATE SET
    target.customer_id = source.customer_id,
    target.order_timestamp = source.order_timestamp,
    target.gross_amount_usd = source.gross_amount_usd,
    target.status = source.status,
    target._updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN
  INSERT (order_id, customer_id, order_timestamp, gross_amount_usd, status, _ingested_at, _updated_at)
  VALUES (source.order_id, source.customer_id, source.order_timestamp, source.gross_amount_usd, source.status, source._ingested_at, CURRENT_TIMESTAMP());
```

### 3.2 Reprocessing Quarantined Records Runbook
1. **Remediation**: Correct producer payload defects or apply approved contract amendment.
2. **Replay Ingestion**: Read records from DLQ quarantine store filtered by `quarantine_id` or time window.
3. **Re-Validation**: Re-evaluate against the amended schema contract.
4. **Target MERGE**: Merge repaired records into Silver tables via standard idempotent MERGE keys.
5. **DLQ Reconciliation**: Mark quarantine records as `RESOLVED_REPLAYED` with resolution audit metadata.
