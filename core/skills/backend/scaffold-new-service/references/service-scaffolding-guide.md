# Service Scaffolding Guide, Hexagonal Layout & Sandbox Readiness — Reference

This reference provides 2027 standards for bootstrapping new services using Hexagonal Architecture, schema-first contracts, centralized RFC 9457 structured error handling, and containerized sandbox readiness.

---

## 1. Hexagonal / Clean Architecture Directory Layout

Every new microservice or bounded component must decouple core domain logic from transport protocols, external dependencies, and persistence mechanisms:

```
<service-root>/
├── api/                             # Invariant contract definitions & generated stubs
│   ├── openapi.yaml                 # OpenAPI 3.1 contract specification
│   └── v1/                          # Protobuf / JSON schema definitions
├── cmd/                             # Application entrypoints & dependency injection
│   └── server/
│       ├── main.go                  # Service startup & graceful shutdown
│       └── wire.go                  # Compile-time DI wiring (Wire / Fx / Awilix)
├── internal/
│   ├── conf/                        # Strongly typed configuration models (Zod / Pydantic)
│   ├── biz/                         # Core Domain: Business entities, rules & outbound ports
│   │   ├── order.go                 # Domain entity & state machines
│   │   └── order_repo.go            # Port interface (e.g. OrderRepository interface)
│   ├── service/                     # Inbound Adapters: Transport handlers
│   │   ├── http.go                  # REST / HTTP handler routing & validation
│   │   ├── grpc.go                  # gRPC service implementation
│   │   └── error_middleware.go      # RFC 9457 global error handler
│   └── data/                        # Outbound Adapters: Persistence & external clients
│       ├── db.go                    # Database client initialization & migrations
│       └── order_repo_impl.go       # Concrete repository implementation
├── Dockerfile                       # Multi-stage unprivileged sandbox container
├── docker-compose.test.yml          # Local Level 0 air-gapped test harness
└── README.md                        # Service ownership, runbook & contract links
```

### 1.1 Architectural Invariants
- **Dependency Inversion**: Outer layers (`service/`, `data/`, `cmd/`) depend on the inner domain (`biz/`). The domain layer has **zero dependencies** on databases, HTTP frameworks, or cloud SDKs.
- **Port Interfaces**: All persistence and external calls from domain logic must be mediated via interfaces (ports) defined in `internal/biz/`.

---

## 2. Centralized RFC 9457 Error Subsystem from Commit 1

Services must never emit ad-hoc error formats or unhandled 500 HTML pages. Bootstrap a unified error handling pipeline during initial scaffolding:

### 2.1 Domain Error Catalog & Mapping

```go
// internal/biz/errors.go
package biz

import "errors"

var (
    ErrNotFound         = errors.New("resource_not_found")
    ErrConflict         = errors.New("resource_conflict")
    ErrValidationFailed = errors.New("validation_failed")
    ErrUnauthorized     = errors.New("unauthorized")
)
```

### 2.2 Global RFC 9457 HTTP Middleware

```typescript
// internal/service/error_middleware.ts
import { Request, Response, NextFunction } from "express";

export function rfc9457ErrorHandler(err: any, req: Request, res: Response, next: NextFunction) {
  const status = err.statusCode || 500;
  const traceId = req.headers["x-trace-id"] || req.id || "opaque-trace-id";

  if (status >= 500) {
    // Sanitized 5xx: Never leak internal error messages or stack traces
    return res.status(500).contentType("application/problem+json").json({
      type: "https://api.example.com/errors/internal-server-error",
      title: "Internal Server Error",
      status: 500,
      detail: "An unexpected system error occurred. Please quote the trace ID to support.",
      instance: req.originalUrl,
      trace_id: traceId
    });
  }

  return res.status(status).contentType("application/problem+json").json({
    type: err.type || `https://api.example.com/errors/${err.code || "bad-request"}`,
    title: err.title || "Client Request Error",
    status: status,
    detail: err.message,
    instance: req.originalUrl,
    trace_id: traceId,
    invalid_params: err.invalidParams || undefined
  });
}
```

---

## 3. Sandbox Readiness & Multi-Stage Rootless Dockerfile

Scaffold the container build to comply with containerized sandbox execution policies (`core/policies/execution-sandbox.md`):

```dockerfile
# Stage 1: Build stage
FROM golang:1.24-alpine AS builder
WORKDIR /src
RUN apk add --no-cache git ca-certificates
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /bin/server ./cmd/server

# Stage 2: Runtime unprivileged container (Level 0 Airgap Compatible)
FROM gcr.io/distroless/static:nonroot
WORKDIR /app
COPY --from=builder /bin/server /app/server

# Enforce non-root execution (UID 1000:1000 / 65532:65532)
USER nonroot:nonroot

# Health check probe
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD ["/app/server", "-health-check"]

EXPOSE 8080
ENTRYPOINT ["/app/server"]
```

### 3.1 Sandbox Execution Flags
- **Read-Only Root Filesystem**: The container must be bootable with `--read-only`. Mount temporary writeable volumes only as memory `tmpfs` at `/tmp`.
- **Network Isolation Testing**: Test harnesses (`docker-compose.test.yml`) must support test execution with `--network=none`.

---

## 4. Observability & Health Probes from Commit 1

Every newly scaffolded service must register Kubernetes lifecycle probes and OpenTelemetry initialization before handling business requests:

1. **Liveness Probe (`/health/live`)**: Returns HTTP 200 if the process event loop is responsive.
2. **Readiness Probe (`/health/ready`)**: Returns HTTP 200 only when database connections and dependent queue clients have successfully initialized. Returns HTTP 503 during startup or graceful draining.
3. **OpenTelemetry Bootstrap**: Initialize the OTel trace provider and propagate context on all inbound requests and outbound HTTP/database clients.
