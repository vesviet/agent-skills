# Ecommerce Microservices Overlay

**Status: planned** — reserved placeholder not yet populated with rules or skills.

Reserved for service-level, deployment-level, or architecture-level conventions for the ecommerce microservices family that do not belong in the portable core.

**Depends on:** `overlays/go-microservices`

## 2026 Planned Tech Stack

When populated, this overlay will target:

| Component | Version | Notes |
|-----------|---------|-------|
| Go | 1.25+ | Container-aware GOMAXPROCS, `testing/synctest` |
| Kratos | **v3** | Breaking import path change from v2 |
| DI | Manual constructors / `goforj/wire` | `google/wire` archived |
| DB | `sqlc` + `pgx/v5` | Compile-time type-safe queries |
| Dapr | **1.15** | Jobs API GA, Workflow stable, binary state |
| Communication | **ConnectRPC** + gRPC-Go | ConnectRPC for new services |
| Observability | OTel Go 1.x | Compile-time instrumentation stable Jul 2026 |

## Intended Scope (when populated)

- Inter-service API contract conventions (ConnectRPC + gRPC + REST gateway)
- Event schema standards (Kafka topic naming, CloudEvents envelope, Dapr pub/sub)
- Service-to-service auth patterns (mTLS, JWT claims, Dapr Workflow secrets)
- Shared observability conventions (trace propagation, structured `log/slog` fields)
- Local development setup (docker-compose, Dapr sidecar, env wiring)
- Dapr Jobs API conventions for scheduled tasks

## Usage

Load via `packs/ecommerce-team/manifest.yaml`:

```yaml
includes:
  - core
  - overlays/go-microservices
  - overlays/ecommerce-microservices
```

Until populated, the `ecommerce-team` pack loads `core` + `overlays/go-microservices` only.

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
