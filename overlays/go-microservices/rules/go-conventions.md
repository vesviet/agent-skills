# Go Microservices Conventions

Standards for the `go-microservices` overlay. All roles working in this overlay MUST follow these rules.

## Project Structure And Architecture

- Follow Clean Architecture / Hexagonal Architecture (Ports and Adapters).
- Keep business logic isolated from transport concerns (HTTP, gRPC, ConnectRPC).
- Use constructor-based dependency injection for testability and decoupling.
- Kratos layout: `api` (contracts), `internal/service` (adapter), `internal/biz` (business logic), `internal/data` (persistence).

## Go 1.25 Features To Adopt

```go
// Container-aware GOMAXPROCS (Go 1.25) — no more uber-go/automaxprocs workaround
// Built-in: Go 1.25 automatically respects K8s CPU limits

// testing/synctest — eliminates flaky time-based concurrency tests
func TestTimeout(t *testing.T) {
    synctest.Run(func() {
        // ... time.Sleep and time.After are simulated
    })
}

// encoding/json/v2 (experimental in Go 1.25 — test it; faster + stricter)
import "encoding/json/v2"
```

## Dependency Injection (2026 Standard)

⚠️ `google/wire` original repo is **ARCHIVED and unmaintained**.

```go
// ✅ PREFERRED: Manual constructor injection (most idiomatic, 95% of apps)
func NewUserService(repo UserRepository, logger *slog.Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}

// ✅ Large codebases (30+ wiring lines): community-maintained fork
// go get github.com/goforj/wire
// Compile-time, zero reflection overhead

// ✅ Enterprise-scale lifecycle management (accept reflection tradeoff)
// go get go.uber.org/fx
```

## Kratos v3 (2026 Standard)

```go
// ✅ v3 import path (current)
import "github.com/go-kratos/kratos/v3"
// ❌ v2 is maintenance-only
```

v3 breaking changes:
- Logging: use standard `log/slog`, not kratos `log.Helper`
- JSON codec split: import `encoding/json` AND `encoding/protojson` separately
- `binding.EncodeURL` → `http.BuildPath`
- HTTP context: use `Bind`, `BindVars`, `BindQuery`, `BindForm` methods

## Database Layer (2026)

| Tool | Use Case |
|------|----------|
| `sqlc` + `pgx/v5` | ✅ **Preferred for new services** — type-safe, compile-time verified, no reflection |
| `golang-migrate` or `Atlas` | Schema migrations |
| GORM v2 | CRUD MVPs, rapid prototyping (reflection overhead matters at scale) |
| `pgx/v5` raw | LISTEN/NOTIFY, COPY protocol, advanced JSONB ops |

```go
// sqlc generated code example (compile-time type-safe)
type Queries struct { db *pgxpool.Pool }
func (q *Queries) GetUser(ctx context.Context, id int64) (User, error) { ... }
```

## Communication (2026)

| Option | When |
|--------|------|
| **ConnectRPC** | ✅ New services — works with HTTP/1.1, browser `fetch`, no proxy needed |
| **gRPC-Go** | Existing high-perf internal service-to-service |
| **grpc-gateway v2** | Expose gRPC as REST for external consumers |

```go
// ConnectRPC server setup (new projects)
import "connectrpc.com/connect"
mux := http.NewServeMux()
mux.Handle(userv1connect.NewUserServiceHandler(userSvc))
```

## Dapr 1.15 Patterns

```go
// Jobs API — replace cron bindings for scheduled tasks
daprClient.ScheduleJobAlpha1(ctx, &runtime.Job{
    Name:     "daily-report",
    Schedule: "@daily",
})

// Dapr Workflow — STABLE (fan-out/fan-in, task chaining)
daprClient.NewWorkflowRuntime().RegisterWorkflow(MyWorkflow)

// Binary state — avoids JSON serialization for non-textual data
daprClient.SaveState(ctx, storeName, key, binaryData, &dapr.StateOptions{})
```

## Concurrency

- Prefer channels for communication. Avoid shared state.
- Use `sync` package only when channels are not appropriate.
- `errgroup.WithContext()` for managed goroutine pools.
- No unmanaged goroutines in request-scoped handlers.

## Error Handling

- Check errors explicitly — never discard.
- Wrap with context: `fmt.Errorf("userService.GetByID(%d): %w", id, err)`.
- Map biz errors → gRPC/HTTP status codes in service layer only.
- Never expose raw database errors to API consumers.

## Logging (Standard `log/slog`)

```go
// ✅ Structured JSON logging (Go 1.21+ standard library)
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
logger.InfoContext(ctx, "user created",
    slog.Int64("user_id", user.ID),
    slog.String("trace_id", traceID),
)

// ❌ Never use unstructured fmt.Print or log.Print in production paths
```

## Observability (OTel 2026)

```go
// ✅ Compile-time instrumentation (zero-code, stable Jul 2026)
// Build flag: go build -toolexec otel-go-build-tool ./...
// Automatically instruments code + deps + stdlib

// ✅ Manual spans for business-critical paths
ctx, span := tracer.Start(ctx, "userService.CreateUser",
    trace.WithAttributes(
        attribute.Int64("user_id", userID),
    ),
)
defer span.End()

// Always implement graceful shutdown
defer tp.Shutdown(context.Background())
defer mp.Shutdown(context.Background())
```

- Export via OTLP only (vendor-agnostic).
- Watch metric cardinality — SDK has protections against unbounded memory growth.

## Testing

```go
// Table-driven tests (standard)
func TestUserService_Create(t *testing.T) {
    tests := []struct {
        name    string
        input   CreateInput
        wantErr bool
    }{
        {"valid user", CreateInput{Name: "Alice"}, false},
        {"empty name", CreateInput{Name: ""}, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) { ... })
    }
}

// Time-based concurrency tests (Go 1.25 testing/synctest)
func TestRateLimit_Resets(t *testing.T) {
    synctest.Run(func() { ... })
}
```

- Mock external dependencies at the interface boundary.
- Target critical business logic paths (state transitions, calculations, payments).

## APIs

- ConnectRPC for new internal services — HTTP/1.1 compatible, browser-native.
- gRPC for existing high-performance internal communication.
- REST/GraphQL for external-facing clients and gateways (grpc-gateway v2).

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/backend/add-api-endpoint/SKILL.md` and the `api-contract-spec.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/backend/add-api-endpoint/SKILL.md` and the `api-contract-spec.json` schema.

Last updated: 2026-09-01
