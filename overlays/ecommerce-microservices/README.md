# Ecommerce Microservices Overlay

**Status: planned** — this overlay is a reserved placeholder. It is not yet populated with rules or skills.

Reserved for service-level, deployment-level, or architecture-level conventions that apply to the ecommerce microservices family but do not belong in the portable core.

**Depends on:** `overlays/go-microservices`

## Intended Scope (when populated)

- inter-service API contract conventions (gRPC + REST gateway)
- event schema standards (Kafka topic naming, CloudEvents envelope)
- service-to-service auth patterns (mTLS, JWT claims)
- shared observability conventions (trace propagation, structured log fields)
- local development setup (docker-compose, env wiring)

## Usage

Load via `packs/ecommerce-team/manifest.yaml`:

```yaml
includes:
  - core
  - overlays/go-microservices
  - overlays/ecommerce-microservices
```

Until this overlay is populated, the `ecommerce-team` pack effectively loads `core` + `overlays/go-microservices` only.
