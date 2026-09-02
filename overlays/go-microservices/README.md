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
