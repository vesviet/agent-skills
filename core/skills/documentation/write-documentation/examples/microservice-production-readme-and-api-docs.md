# Production Microservice Documentation Example: Payment Orchestrator

---
title: "Payment Orchestrator Service"
description: "High-throughput payment gateway orchestrator supporting dual HTTP/gRPC contracts, idempotency, and Dapr pub/sub."
category: "howto"
last_verified_version: "v2.12.0"
maintainer: "backend-developer"
---

# Payment Orchestrator Service

The Payment Orchestrator coordinates machine-to-machine checkout, credit card authorizations, and stateful ledger reconciliation across global payment gateways.

## 1. Quickstart (How-To)

### Prerequisites
- Go 1.25+
- Docker & Docker Compose
- Kratos CLI v2.9.1+

### Local Execution
```bash
# Clone and enter service directory
cd services/payment-orchestrator

# Generate Wire dependencies
wire gen ./...

# Run service locally
go run ./cmd/payment-orchestrator -conf ./configs
```

## 2. Architecture & Quadrant Alignment (Explanation)

The service follows **Clean Architecture** and **Kratos Layer Separation**:
- `api/`: Protobuf service contracts generating gRPC stubs and HTTP OpenAPI v3 specs.
- `internal/service/`: Protocol adapter translating transport requests into business commands.
- `internal/biz/`: Pure domain business logic; strictly independent of `gorm.DB` or transport packages.
- `internal/data/`: Data access layer encapsulating PostgreSQL queries and Redis caches.

```
Transport (gRPC / HTTP)
         │
         ▼
  internal/service (Adapter)
         │
         ▼
  internal/biz (Domain Logic)
         │
         ▼
  internal/data (Persistence & External Clients)
```

## 3. Authoritative API Reference (Reference)

All REST and gRPC endpoints are strictly generated from Protobuf definitions. Do not edit hand-typed endpoints.

- **OpenAPI v3 Specification**: Auto-published at `https://api.internal.example.com/docs/openapi.json`
- **Interactive UI**: Rendered via Scalar at `https://api.internal.example.com/docs`
- **gRPC Reflection**: Enabled in `dev` and `staging` clusters.

### Key API Operations
| Method | Path | Description | Idempotency Header |
|---|---|---|---|
| `POST` | `/v1/payments/charges` | Authorize payment transaction | Required (`X-Idempotency-Key`) |
| `POST` | `/v1/payments/refunds` | Process full/partial refund | Required (`X-Idempotency-Key`) |
| `GET` | `/v1/payments/{id}` | Query payment settlement status | N/A |
| `GET` | `/health/live` | Liveness probe endpoint | N/A |
| `GET` | `/health/ready` | Readiness probe endpoint | N/A |
