# Release Notes — Core Commerce Platform v3.0.0 (2026-11-08)

---
version: "3.0.0"
release_date: "2026-11-08"
breaking_changes:
  - id: "BC-301"
    summary: "Sunset of legacy v1 checkout REST endpoints in favor of UCP v2026-08-25"
    migration_guide_url: "https://docs.example.com/migrations/v3-checkout"
new_features:
  - id: "FEAT-881"
    summary: "Support for Machine Payments Protocol (MPP) and x402 V2 settlement"
security_fixes:
  - cve: "CVE-2026-4401"
    severity: "High"
    advisory: "Patched timing discrepancy in webhook signature validation"
---

## ⚠️ Breaking Changes

- **[API]** Deprecated `/api/v1/checkout` endpoints have been removed. All client SDKs must migrate to Universal Commerce Protocol (`/api/ucp/v1/sessions`). See [Migration Guide](https://docs.example.com/migrations/v3-checkout).
- **[Operator]** Database migration `0042_add_spiffe_workload_id.sql` must be executed before deploying v3.0.0 container pods.

## ✨ New Features

- **[Commerce]** Native support for **Machine Payments Protocol (MPP)** and **x402 V2** payment negotiation for autonomous agents.
- **[Platform]** SPIFFE/SPIRE workload attestation for all internal service-to-service communication.

## 🐛 Defect Fixes

- **[Checkout]** Resolved race condition in inventory reservation locking under high concurrency.
- **[Telemetry]** Corrected OpenTelemetry trace context propagation across async Kafka worker consumers.

## 🔒 Security

- **[Auth]** Upgraded webhook signature verification to constant-time comparison, mitigating timing attack risks (advisory CVE-2026-4401).

## 📋 Operator & Infrastructure Notes

- **Environment Variables**: Added mandatory `SPIFFE_ENDPOINT_SOCKET` configuration.
- **Database Migrations**: Zero-downtime migration tested on PostgreSQL 17; run `migrate up` during rolling upgrade.
- **Rollback Runbook**: If deployment is aborted, rollback deployment image to `v2.14.2`; migration `0042` is backwards-compatible.
