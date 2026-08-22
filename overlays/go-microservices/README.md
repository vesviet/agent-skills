# Go Microservices Overlay

Language-level and architecture-level conventions for Go (Golang) microservices. Bridges the portable core skills with Go-specific implementation details.

## Tech Stack (2026)

- **Language:** Go 1.25+ (container-aware GOMAXPROCS, `testing/synctest`, `encoding/json/v2`)
- **Framework:** Kratos **v3** (v2 is maintenance-only; import path changed)
- **Architecture:** Clean Architecture / Hexagonal Architecture (Ports and Adapters)
- **Database:** `sqlc` + `pgx/v5` (preferred) or GORM v2 (CRUD MVPs)
- **Pub/Sub & State:** Dapr **1.15** (Workflow stable, Jobs API GA, binary state)
- **DI:** Manual constructor injection (preferred) or `goforj/wire` (compile-time, for large codebases)
- **Communication:** ConnectRPC (new services) or gRPC-Go (existing)
- **Observability:** OpenTelemetry Go SDK 1.x — compile-time instrumentation stable (Jul 2026)
- **Logging:** Standard `log/slog`
- **Testing:** Standard `testing` + table-driven + `testing/synctest` for time-based concurrency

## ⚠️ 2026 Critical Changes

### Wire Dependency Injection — ARCHIVED
`google/wire` original repo is **ARCHIVED and unmaintained**.

| Option | Use When |
|--------|----------|
| Manual `NewXxx()` constructors | ✅ Default — most idiomatic Go, 95% of apps |
| `github.com/goforj/wire` | Large codebase (30+ wiring lines) — maintained community fork |
| `uber-go/fx` | Enterprise-scale lifecycle management (accept runtime DI tradeoff) |

### Kratos v3 — Breaking Import Path
```go
// ❌ v2 (maintenance-only)
import "github.com/go-kratos/kratos/v2"

// ✅ v3 (current)
import "github.com/go-kratos/kratos/v3"
```

Additional v3 changes:
- Logging: `log.Logger`/`log.Helper` → standard `log/slog`
- JSON codec: now split — import `encoding/json` AND `encoding/protojson` separately
- `binding.EncodeURL` → `http.BuildPath`

### Dapr 1.15 New APIs
- `Jobs API` → replace cron bindings for scheduled tasks
- Binary state → avoids JSON serialization for non-textual data
- `Dapr Workflow` → STABLE — use for durable execution (fan-out/fan-in, task chaining)

## Conventions

- **Dependency Management:** Go Modules (`go.mod`).
- **Concurrency:** Idiomatic goroutines/channels; no shared memory; `sync` pkg only when channels insufficient.
- **Testing:** Standard `testing` package, table-driven tests; `testing/synctest` for time-based concurrency.
- **Logging:** `log/slog` structured JSON — never `fmt.Print` or generic `log.Print` in production.
- **Error Handling:** Explicit checking; wrap with `fmt.Errorf("...: %w", err)`.
- **API:** ConnectRPC for new services (HTTP/1.1 + browser-native), gRPC-Go for existing high-perf internal services.
- **Observability:** OTel compile-time instrumentation (`-toolexec` flag) for zero-code coverage; manual spans for business paths.
