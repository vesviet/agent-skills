# Master Engineering Dossier: Modern Backend Development Ecosystems (2025–2027)
**Focus Areas:** Go 1.25+ / Kratos / Wire, Modern PHP 8.3/8.4+ / Laravel 11/12+ / FrankenPHP / Saloon, Python 3.13+ / FastAPI / Dishka / Temporal / AI-Native OTel  
**Role:** Worker Backend (Synthesizing Research Findings from Explorer Go, Explorer PHP, and Explorer Python)  
**Deliverable Path:** `reports/backend-developer-repo-research.md`  
**Standard Alignment:** Standard 2026 / 2027 Architecture Standards, Clean Architecture, OWASP ASI, RFC 9457 / RFC 7807, OpenTelemetry GenAI Semantic Conventions  

---

## 1. Executive Summary: State of Backend Engineering (2025–2027)

### 1.1 The Post-Microservice Realism & The Compile-Time Revolution

Between 2018 and 2023, backend software engineering was dominated by unrestrained microservice sprawl. Teams prematurely fragmented unified domains into dozens of ephemeral micro-services, introducing severe distributed network overhead, dual-write consistency failures, unmanaged operational complexity, and difficult cross-service debugging.

As the industry enters the 2025–2027 cycle, a profound **architectural correction** has taken hold: **Post-Microservice Realism**. Modern engineering teams prioritize high-cohesion, low-coupling **Modular Monoliths** or strictly bounded, purpose-built **Domain Microservices**. Concurrently, an industry-wide **Compile-Time Revolution** has rendered runtime reflection, dynamic duck-typing, and untyped payload parsing obsolete:

1. **Static Invariance over Dynamic Interpretation**:
   - In Go, compile-time AST code generation (`google/wire`, `sqlc`) has replaced runtime reflection containers (`inject`, reflection-based ORMs), driving memory allocations toward zero and moving dependency graph validation entirely into the compilation phase.
   - In PHP, the runtime engine itself has evolved into a strictly typed environment. PHP 8.3 and 8.4 introduce typed class constants, property hooks, asymmetric visibility (`public private(set)`), and native JIT compilation, eliminating dynamic getter/setter overhead and catching contract mismatches during static analysis (PHPStan Level 9 / Larastan).
   - In Python, Python 3.13+ combined with Rust-backed `pydantic-core` (Pydantic v2) has transformed API boundaries into strictly typed contracts executed at compiled machine speeds, while scoped IoC engines (`dishka`) liberate business logic from web-framework bindings.

2. **The Tri-Ecosystem Convergence**:
   Despite syntax and runtime differences, modern backend architectures across Go, PHP, and Python have converged upon identical clean architecture fundamentals:
   - **Go**: Canonical high-throughput microservices using Protobuf-first Hexagonal Architecture (`go-kratos/kratos`), static dependency injection (`google/wire`), durable distributed workflows (`temporalio/sdk-go`), and sidecar abstraction (`dapr/go-sdk`).
   - **PHP**: Modern enterprise monoliths and APIs powered by streamlined zero-kernel architectures (`laravel/laravel` 11/12+), high-performance in-memory worker runtimes (`dunglas/frankenphp` Caddy worker mode with sub-3ms latencies), declarative API connectors (`saloonphp/saloon`), and automated architectural testing (`pestphp/pest`).
   - **Python**: High-throughput async ASGI backends (`fastapi`, `litestar`), framework-agnostic dependency injection (`dishka`), async SQLAlchemy 2.0 Unit of Work persistence, durable distributed execution (`temporalio/sdk-python`), and AI-Native service integration (LiteLLM proxy, Langfuse tracing, Instructor structured outputs, OpenTelemetry GenAI conventions).

---

### 1.2 Core Paradigm Shifts in Modern Backend Systems

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                          MODERN BACKEND PARADIGM SHIFTS (2025–2027)                   │
├──────────────────────────┬─────────────────────────────────┬──────────────────────────┤
│ Legacy Pattern (Pre-2024) │ Root Failure Vector             │ Modern Standard (2026+)  │
├──────────────────────────┼─────────────────────────────────┼──────────────────────────┤
│ Runtime Reflection DI     │ Boot panics, startup overhead   │ Compile-Time DI / Scoped │
│ (Reflection containers)  │ and hidden runtime graph cycles │ Containers (Wire, Dishka)│
├──────────────────────────┼─────────────────────────────────┼──────────────────────────┤
│ Direct Dual-Write Events │ Partial failure causes state vs │ Transactional Outbox     │
│ (DB write + Broker send) │ broker data desynchronization   │ (SKIP LOCKED relay daemon│
├──────────────────────────┼─────────────────────────────────┼──────────────────────────┤
│ Ad-hoc Synchronous Loops │ Network storms, cascading pod   │ Token Bucket + Breaker + │
│ and unmanaged retries    │ exhaustion, thundering herds    │ Full Jitter Exponential │
├──────────────────────────┼─────────────────────────────────┼──────────────────────────┤
│ Free-form Error Payloads │ Leaked DB schema/SQL passwords; │ RFC 9457 / RFC 7807      │
│ & Unmasked Exceptions    │ brittle client error parsing    │ Problem Details Envelopes│
├──────────────────────────┼─────────────────────────────────┼──────────────────────────┤
│ Naive Prompt Engineering │ JSON decode crashes, prompt     │ Instructor Schemas +     │
│ & String Regex Parsing   │ injections, model hallucinations│ OTel GenAI Semantic Traces│
└──────────────────────────┴─────────────────────────────────┴──────────────────────────┘
```

The four non-negotiable pillars of production-grade backend engineering in 2025–2027 are:

1. **Zero-Leak Clean Architecture**:
   Domain logic must remain completely agnostic of transport protocols (HTTP/gRPC) and database drivers (GORM, Eloquent, SQLAlchemy). Business invariants are validated inside pure domain entities; repository interfaces enforce the Dependency Inversion Principle (DIP).
2. **Atomic InTx Persistence & The Transactional Outbox**:
   Dual-writing to a relational database and a message broker (Kafka, RabbitMQ, Dapr) without two-phase commit guarantees message loss or distributed state drift. The Transactional Outbox pattern, backed by PostgreSQL `SELECT ... FOR UPDATE SKIP LOCKED`, is the production standard for reliable, at-least-once distributed messaging.
3. **Mathematical Resilience & Fault Tolerance**:
   Distributed systems assume downstream failure. External client integrations require token-bucket rate limiting, circuit breaker state machines (`CLOSED` -> `OPEN` -> `HALF-OPEN`), AWS full jitter exponential backoff, and idempotent request headers (`Idempotency-Key`).
4. **AI-Native Telemetry & Structured Execution**:
   AI agent and LLM workloads must be treated as untrusted, stochastic downstream services. All LLM calls must flow through gateway routing proxies (LiteLLM), enforce strict schema decoding with automated self-correction (Instructor with Pydantic v2), and emit OpenTelemetry GenAI Semantic Convention spans (`gen_ai.system`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`) for complete cost attribution and auditability.


---

## 2. Curated Repository Catalog & Architecture Classification

A rigorous audit of 23 premier, battle-tested open-source repositories across Go, PHP, and Python reveals the cutting edge of modern backend engineering. The following cross-ecosystem classification matrix details their maturity, architectural paradigms, key production strengths, and real-world engineering trade-offs.

### 2.1 Cross-Ecosystem Comparative Taxonomy Matrix

| # | Repository & URL | Ecosystem | Primary Category | Stars & Maturity | Architectural Style | Core Production Strengths | Production Trade-offs & Limitations |
| :- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [go-kratos/kratos](https://github.com/go-kratos/kratos) | Go 1.25+ | Microservices Framework | ~24,000+ (CNCF Landscape) | Hexagonal / Clean Architecture (Protobuf-First) | Dual gRPC/HTTP unified transport, compile-time Wire DI integration, standardized middleware pipeline, metadata context propagation | Strict 4-layer boilerplate; steep learning curve for developers unfamiliar with IDL-first API design |
| 2 | [google/wire](https://github.com/google/wire) | Go 1.25+ | Dependency Injection | ~13,000+ (Google OSS) | Compile-time Static AST Code Generator | Zero runtime overhead; compile-time failure on missing dependencies or dependency graph cycles; produces clean human-readable Go code | Requires build step code generation (`wire gen ./...`); does not manage runtime lifecycle hooks |
| 3 | [uber-go/fx](https://github.com/uber-go/fx) | Go 1.25+ | Dependency Injection | ~6,100+ (Uber OSS) | Runtime Modular Container | Comprehensive lifecycle management (`OnStart`/`OnStop` hooks), value groups for plug-in architectures, clean modular composition | Uses runtime reflection; graph errors or missing dependencies trigger runtime panics on boot rather than compile errors |
| 4 | [ThreeDotsLabs/watermill](https://github.com/ThreeDotsLabs/watermill) | Go 1.25+ | Event-Driven Messaging | ~8,200+ (Three Dots Labs) | Universal Event Router & CQRS | Universal pub/sub abstraction (Kafka, RabbitMQ, NATS, SQL), built-in SQL transactional outbox forwarder, composable middleware | At-least-once delivery requires idempotent downstream consumers; asynchronous debugging complexity |
| 5 | [temporalio/sdk-go](https://github.com/temporalio/sdk-go) | Go 1.25+ | Distributed Orchestration | ~4,500+ (Temporal Core ~16k) | Durable Virtual State Machine | Workflows survive server crashes and restarts; built-in automated exponential retries, Saga compensations, and determinism checks | Workflows must be 100% deterministic (no direct I/O); requires deploying and maintaining a Temporal server cluster |
| 6 | [dapr/go-sdk](https://github.com/dapr/go-sdk) | Go 1.25+ | Cloud-Native Runtime | ~1,300+ (Dapr Core ~25k, CNCF Graduated) | Distributed Application Runtime (Sidecar) | Decouples cloud infrastructure (PubSub, State Store, Bindings, Secrets) via standard local gRPC/HTTP sidecar APIs | Adds 1–2ms sidecar network hop latency; requires K8s sidecar injection and Dapr control plane |
| 7 | [sqlc-dev/sqlc](https://github.com/sqlc-dev/sqlc) | Go 1.25+ | Persistence & SQL | ~15,500+ (sqlc-dev) | SQL-First Compiler & Code Generator | 100% compile-time type safety; zero runtime reflection; generates pure Go structs from raw SQL DDL; optimal query execution | Dynamic queries with variable WHERE or ORDER BY clauses require multiple queries or query builder workarounds |
| 8 | [panjf2000/ants](https://github.com/panjf2000/ants) | Go 1.25+ | High-Performance Concurrency | ~14,200+ | Goroutine Recycling Worker Pool | Bounded memory consumption; prevents unmanaged goroutine leaks; built-in panic recovery handlers; zero GC thrashing under burst loads | Blocked tasks can starve the worker queue if capacity is misconfigured; requires task size tuning |
| 9 | [spatie/laravel-data](https://github.com/spatie/laravel-data) | PHP 8.3/8.4+ | Data Modeling & Schema | ~3,200+ (Spatie) | Strongly Typed DTO & Schema Engine | Transforms untyped HTTP inputs into strongly typed PHP 8.4 objects; unifies validation, TypeScript export, and OpenAPI documentation | Adds reflection overhead during object mapping; requires property caching in high-frequency loops |
| 10 | [spatie/laravel-event-sourcing](https://github.com/spatie/laravel-event-sourcing) | PHP 8.3/8.4+ | Event Sourcing & CQRS | ~1,600+ (Spatie) | Event Sourcing & CQRS Framework | Implements true Domain Aggregate Roots, transactional stored events, asynchronous projectors, and replayable read projections | Event schema evolution requires strict Upcaster discipline; storage footprint grows monotonically |
| 11 | [saloonphp/saloon](https://github.com/saloonphp/saloon) | PHP 8.3/8.4+ | API Integration Engine | ~2,500+ (Saloon) | Object-Oriented Declarative Integration | Declarative connectors and requests; built-in exponential backoff retries with jitter; MockClient fixture recording for offline testing | Additional abstraction layer over Guzzle; requires learning Saloon-specific plugin interfaces |
| 12 | [filamentphp/filament](https://github.com/filamentphp/filament) | PHP 8.3/8.4+ | Admin & Rapid App Engine | ~19,000+ (Filament) | Modular Admin & Unified Schema | Unified Schema API in v4; reactive forms; decoupled non-Eloquent data sources; built-in MFA and Passkey authentication | Deep reliance on Livewire state synchronization; complex dynamic forms require fine-grained debouncing |
| 13 | [pestphp/pest](https://github.com/pestphp/pest) | PHP 8.3/8.4+ | Testing & Architecture | ~9,500+ (Pest Core) | Functional & Architecture Testing | Architectural boundary testing (`arch()`); built-in mutation testing (`--mutate`); expressive fluent assertions; parallel test runner | Custom DSL syntax departs from PHPUnit attribute standards; requires team familiarity with functional test style |
| 14 | [dunglas/frankenphp](https://github.com/dunglas/frankenphp) | PHP 8.3/8.4+ | In-Memory Application Server | ~9,800+ (Les-Tilleuls) | Caddy-Integrated In-Memory Server | Embedded `libphp` via C-Go; zero IPC latency; native HTTP/3 QUIC; 103 Early Hints; built-in Mercure real-time push hub; worker mode | Long-running workers require elimination of static state bleed and strict worker memory recycling |
| 15 | [laravel/octane](https://github.com/laravel/octane) | PHP 8.3/8.4+ | High-Concurrency Engine | ~4,800+ (Laravel Official) | Multi-Worker In-Memory Daemon | Boots framework once in RAM; supports Swoole, RoadRunner, and FrankenPHP; drops request latency to 1–3ms | Request-scoped state singletons bleed across sequential requests unless explicitly flushed via listeners |
| 16 | [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | Python 3.13+ | Full-Stack Scaffolding | ~35,000+ (Tiangolo) | Layered ASGI API Router | Canonical production template; Alembic migrations; OAuth2 JWT authentication; automatic OpenAPI schema documentation | Tightly couples use cases to FastAPI `Depends`; SQLModel can cause subtle schema/ORM state bleeding in complex domains |
| 17 | [litestar-org/litestar](https://github.com/litestar-org/litestar) | Python 3.13+ | High-Performance ASGI | ~5,500+ (Litestar Organization) | Controller-Repository-Service with DTOs | Extreme ASGI throughput; native SQLAlchemy plugin with built-in async repositories; compile-time DTO mapping | Smaller community ecosystem than FastAPI; steeper initial learning curve |
| 18 | [reagento/dishka](https://github.com/reagento/dishka) | Python 3.13+ | Dependency Injection | ~1,200+ (Reagento) | Scoped IoC Container | Completely decouples domain logic from HTTP frameworks; identical provider resolution across FastAPI, Litestar, Celery, Arq, CLI | Requires disciplined constructor-based injection; less common in introductory tutorials |
| 19 | [pydantic/pydantic](https://github.com/pydantic/pydantic) | Python 3.13+ | Data Validation & Schema | ~25,000+ (Pydantic / Samuel Colvin) | Compiled Rust Core Engine (`pydantic-core`) | 5x–20x parsing speedup; strict mode validation; `TypeAdapter` for arbitrary types; zero-copy JSON parsing | Breaking changes between v1 and v2 required ecosystem migration; strict validation requires careful handling of coercion |
| 20 | [BerriAI/litellm](https://github.com/BerriAI/litellm) | Python 3.13+ | AI Gateway & Routing Proxy | ~18,000+ (BerriAI) | LLM Reverse Proxy & Load Balancer | Unified wire format across 100+ LLM providers; dynamic rate-limiting (TPM/RPM); automatic fallbacks on 429/5xx; token cost tracking | High operational footprint if self-hosting at scale; rapid upstream API adjustments require continuous updates |
| 21 | [langfuse/langfuse-python](https://github.com/langfuse/langfuse-python) | Python 3.13+ | LLM Observability & Tracing | ~7,500+ (Langfuse) | Async Telemetry & Decorator Tracing | Native multi-agent trace hierarchy; prompt template versioning; automated evaluation scoring; non-blocking background dispatch | Requires dedicated Langfuse server or cloud backend; detailed trace payloads increase telemetry storage volume |
| 22 | [jxnl/instructor](https://github.com/jxnl/instructor) | Python 3.13+ | Structured LLM Outputs | ~9,200+ (Jason Liu) | Schema Extraction with Self-Correction | 100% typed structured extraction via tool calling; automated re-prompting on validation failures; streaming partial objects | Repeated retries on complex validation failures increase latency and token consumption |
| 23 | [temporalio/sdk-python](https://github.com/temporalio/sdk-python) | Python 3.13+ | Distributed Orchestration | ~1,400+ (Temporal Core ~16k) | Event-Sourced Deterministic State Machine | Indestructible workflows surviving process crashes; native async event loop integration; non-breaking versioning with `workflow.patched` | Requires running Temporal cluster; strict determinism constraint (no direct I/O inside workflow functions) |

---

### 2.2 Deep Architectural Profiles

#### 1. Go Ecosystem Highlights
- **`go-kratos/kratos`**: Originating from Bilibili and widely adopted across CNCF enterprise deployments, Kratos establishes the golden standard for dual-protocol (gRPC + HTTP) microservices. It strictly enforces a 4-tier layer structure (`api`, `internal/service`, `internal/biz`, `internal/data`) and relies on Protobuf definitions as the single source of truth for contracts, input validation, and OpenAPI 3.0 generation.
- **`google/wire` vs `uber-go/fx`**: While `fx` provides rich lifecycle hooks via runtime reflection, `wire` is the industry benchmark for high-performance systems. By generating plain, unreflected Go code during the build process, `wire` guarantees zero startup latency, zero reflection allocations, and instant compile-time feedback when a dependency is missing.
- **`ThreeDotsLabs/watermill`**: Watermill acts as an enterprise event router, abstracting Kafka, RabbitMQ, NATS, and SQL. Its SQL outbox forwarder is a battle-tested reference implementation for guaranteed event delivery without distributed transactions.
- **`temporalio/sdk-go`**: Provides an event-sourced virtual state machine runtime. Workflows execute deterministically; when a worker pod dies, the Temporal cluster replays the event history to restore the exact stack state. Activities isolate external side-effects (payment calls, database writes) with declarative retry policies.

#### 2. PHP Ecosystem Highlights
- **`spatie/laravel-data`**: Revolutionized modern PHP data modeling by replacing untyped associative arrays and sprawling Form Requests with strictly typed, immutable DTOs that validate inputs, cast nested relations, and export TypeScript contracts.
- **`saloonphp/saloon`**: The definitive standard for third-party API integration in PHP. Replaces ad-hoc Guzzle clients with isolated Connector and Request classes, embedding circuit breakers, exponential backoff, rate limiters, and offline `MockClient` testing.
- **`dunglas/frankenphp` & `laravel/octane`**: Together, FrankenPHP and Octane have eliminated PHP's legacy shared-nothing penalty. By embedding PHP directly into Caddy's Go runtime and keeping the compiled application resident in memory, request latency drops from 35ms to under 2ms, with native support for RFC 8297 Early Hints.
- **`pestphp/pest`**: Pest v3/v5 has superseded PHPUnit in modern workflows, notably introducing `arch()` architectural tests that statically forbid Eloquent leaks in HTTP controllers, ban unmanaged static state, and enforce strict type declarations across the domain.

#### 3. Python Ecosystem Highlights
- **`fastapi` vs `litestar`**: While FastAPI leads the ecosystem in adoption and third-party integrations, Litestar represents the state-of-the-art in architectural rigor with compile-time DTOs, native async repository plugins, and zero-allocation parameter parsing.
- **`reagento/dishka`**: Solves the fundamental architectural flaw of FastAPI's `Depends`—tight coupling to HTTP requests. Dishka provides a framework-agnostic scoped IoC container supporting `Scope.APP`, `Scope.REQUEST`, and `Scope.ACTION`, allowing the exact same dependency graph to run inside ASGI web servers, Celery/Arq background workers, and CLI scripts.
- **`pydantic` v2**: Rewritten in Rust (`pydantic-core`), Pydantic v2 delivers a 20x performance leap, enabling sub-millisecond JSON deserialization and strict boundary validation without type coercion.
- **`BerriAI/litellm` & `jxnl/instructor`**: The foundation of modern AI-native backend engineering. LiteLLM acts as a resilient proxy gateway across 100+ LLM providers with automatic fallback on 429/500 errors, while Instructor leverages provider tool-calling and Pydantic v2 to enforce 100% strict structured extraction with automated self-correction.


---

## 3. Deep Architectural Case Studies & Cross-Language Code Blueprints

### 3.1 Case Study 1: Strict Layer Separation & Dependency Injection

#### 3.1.1 Architectural Foundations of Clean Architecture
The primary objective of Clean Architecture (Hexagonal / Ports and Adapters) is the **absolute isolation of business logic from infrastructure concerns**. Whether using Go, PHP, or Python, enterprise backends must uphold the following invariants:
1. **The Dependency Inversion Principle (DIP)**: High-level modules (business use cases) must not depend on low-level modules (database drivers, HTTP frameworks, message brokers). Both must depend on abstract port interfaces.
2. **The Zero-Leak Rule**: Domain entities must be pure data structures without ORM tags, database annotations, or framework-specific method inheritance.
3. **Inversion of Control (IoC)**: Dependencies are injected from the outside via constructors, never instantiated directly inside use cases.

---

#### 3.1.2 Go 1.25+: Kratos v2.9.1 Clean Architecture + Google Wire DI

In Go microservices, strict Clean Architecture is realized through four distinct packages:
- `api/`: Protobuf service contracts, gRPC stubs, and HTTP transcoding definitions.
- `internal/service/`: Inbound transport adapters. Unmarshals requests, invokes Biz use cases, and maps domain errors to transport status codes.
- `internal/biz/`: Pure domain business logic. Houses domain entities, business invariants, use cases, and repository interfaces. **Strictly zero database imports (`gorm.io/gorm` is banned).**
- `internal/data/`: Outbound persistence adapters. Implements Biz repository interfaces using GORM, sqlc, or pgx.
- `cmd/server/wire.go`: Compile-time static dependency injection declarations.

##### 1. Domain Layer: `internal/biz/user.go` (Zero DB Imports)
```go
package biz

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/go-kratos/kratos/v2/log"
)

var (
	ErrUserNotFound      = errors.New("user not found")
	ErrUserAlreadyExists = errors.New("user email already registered")
	ErrInvalidUserData   = errors.New("invalid user data")
)

// User represents the pure domain entity with zero ORM tags
type User struct {
	ID        int64
	Email     string
	Username  string
	CreatedAt time.Time
	UpdatedAt time.Time
}

// UserRepo defines the outbound port interface for persistence
type UserRepo interface {
	Save(ctx context.Context, u *User) (*User, error)
	FindByID(ctx context.Context, id int64) (*User, error)
	FindByEmail(ctx context.Context, email string) (*User, error)
}

// Transaction defines the outbound port interface for atomic boundaries
type Transaction interface {
	InTx(ctx context.Context, fn func(ctx context.Context) error) error
}

type UserUsecase struct {
	repo UserRepo
	tx   Transaction
	log  *log.Helper
}

func NewUserUsecase(repo UserRepo, tx Transaction, logger log.Logger) *UserUsecase {
	return &UserUsecase{
		repo: repo,
		tx:   tx,
		log:  log.NewHelper(logger),
	}
}

func (uc *UserUsecase) CreateUser(ctx context.Context, email, username string) (*User, error) {
	if email == "" || username == "" {
		return nil, ErrInvalidUserData
	}

	var createdUser *User
	err := uc.tx.InTx(ctx, func(ctx context.Context) error {
		existing, err := uc.repo.FindByEmail(ctx, email)
		if err != nil && !errors.Is(err, ErrUserNotFound) {
			return fmt.Errorf("failed checking email: %w", err)
		}
		if existing != nil {
			return ErrUserAlreadyExists
		}

		now := time.Now().UTC()
		user := &User{
			Email:     email,
			Username:  username,
			CreatedAt: now,
			UpdatedAt: now,
		}

		createdUser, err = uc.repo.Save(ctx, user)
		if err != nil {
			return fmt.Errorf("failed saving user: %w", err)
		}
		return nil
	})

	if err != nil {
		uc.log.WithContext(ctx).Errorf("CreateUser failed: %v", err)
		return nil, err
	}

	return createdUser, nil
}

func (uc *UserUsecase) GetUser(ctx context.Context, id int64) (*User, error) {
	if id <= 0 {
		return nil, ErrInvalidUserData
	}
	return uc.repo.FindByID(ctx, id)
}
```

##### 2. Data Layer: `internal/data/data.go` and `internal/data/user.go`
```go
package data

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/google/wire"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	gormlogger "gorm.io/gorm/logger"

	"agent-skills/internal/biz"
)

var ProviderSet = wire.NewSet(
	NewData,
	NewDB,
	NewUserRepo,
	NewTransaction,
)

type Data struct {
	db *gorm.DB
}

type contextTxKey struct{}

func NewData(db *gorm.DB) (*Data, func(), error) {
	cleanup := func() {
		sqlDB, err := db.DB()
		if err == nil {
			_ = sqlDB.Close()
		}
	}
	return &Data{db: db}, cleanup, nil
}

func NewDB() (*gorm.DB, error) {
	dsn := "host=localhost user=postgres password=postgres dbname=app port=5432 sslmode=disable TimeZone=UTC"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: gormlogger.Default.LogMode(gormlogger.Silent),
		NowFunc: func() time.Time {
			return time.Now().UTC()
		},
	})
	if err != nil {
		return nil, fmt.Errorf("failed connecting to postgres: %w", err)
	}

	sqlDB, err := db.DB()
	if err != nil {
		return nil, fmt.Errorf("failed getting generic db: %w", err)
	}

	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetMaxOpenConns(100)
	sqlDB.SetConnMaxLifetime(time.Hour)
	sqlDB.SetConnMaxIdleTime(10 * time.Minute)

	if err := db.AutoMigrate(&UserModel{}); err != nil {
		return nil, fmt.Errorf("failed auto-migration: %w", err)
	}

	return db, nil
}

func NewTransaction(d *Data) biz.Transaction {
	return d
}

// InTx encapsulates transaction execution and context propagation
func (d *Data) InTx(ctx context.Context, fn func(ctx context.Context) error) error {
	return d.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		ctxWithTx := context.WithValue(ctx, contextTxKey{}, tx)
		return fn(ctxWithTx)
	})
}

// DB retrieves the active transaction or default database connection
func (d *Data) DB(ctx context.Context) *gorm.DB {
	if tx, ok := ctx.Value(contextTxKey{}).(*gorm.DB); ok {
		return tx
	}
	return d.db.WithContext(ctx)
}

type UserModel struct {
	ID        int64     `gorm:"primaryKey;autoIncrement"`
	Email     string    `gorm:"type:varchar(255);uniqueIndex;not null"`
	Username  string    `gorm:"type:varchar(100);not null"`
	CreatedAt time.Time `gorm:"not null"`
	UpdatedAt time.Time `gorm:"not null"`
}

func (UserModel) TableName() string {
	return "users"
}

type userRepo struct {
	data *Data
}

func NewUserRepo(data *Data) biz.UserRepo {
	return &userRepo{data: data}
}

func (r *userRepo) Save(ctx context.Context, u *biz.User) (*biz.User, error) {
	po := &UserModel{
		ID:        u.ID,
		Email:     u.Email,
		Username:  u.Username,
		CreatedAt: u.CreatedAt,
		UpdatedAt: u.UpdatedAt,
	}

	err := r.data.DB(ctx).Save(po).Error
	if err != nil {
		return nil, fmt.Errorf("userRepo.Save failed: %w", err)
	}

	u.ID = po.ID
	return u, nil
}

func (r *userRepo) FindByID(ctx context.Context, id int64) (*biz.User, error) {
	var po UserModel
	err := r.data.DB(ctx).First(&po, id).Error
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, biz.ErrUserNotFound
		}
		return nil, fmt.Errorf("userRepo.FindByID failed: %w", err)
	}
	return &biz.User{
		ID:        po.ID,
		Email:     po.Email,
		Username:  po.Username,
		CreatedAt: po.CreatedAt,
		UpdatedAt: po.UpdatedAt,
	}, nil
}

func (r *userRepo) FindByEmail(ctx context.Context, email string) (*biz.User, error) {
	var po UserModel
	err := r.data.DB(ctx).Where("email = ?", email).First(&po).Error
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, biz.ErrUserNotFound
		}
		return nil, fmt.Errorf("userRepo.FindByEmail failed: %w", err)
	}
	return &biz.User{
		ID:        po.ID,
		Email:     po.Email,
		Username:  po.Username,
		CreatedAt: po.CreatedAt,
		UpdatedAt: po.UpdatedAt,
	}, nil
}
```

##### 3. Service Layer (Inbound Transport Adapter): `internal/service/user.go`
```go
package service

import (
	"context"
	"errors"

	kerrors "github.com/go-kratos/kratos/v2/errors"

	"agent-skills/internal/biz"
)

type CreateUserRequest struct {
	Email    string `json:"email"`
	Username string `json:"username"`
}

type CreateUserResponse struct {
	ID        int64  `json:"id"`
	Email     string `json:"email"`
	Username  string `json:"username"`
	CreatedAt string `json:"created_at"`
}

type GetUserRequest struct {
	ID int64 `json:"id"`
}

type UserService struct {
	uc *biz.UserUsecase
}

func NewUserService(uc *biz.UserUsecase) *UserService {
	return &UserService{uc: uc}
}

func (s *UserService) CreateUser(ctx context.Context, req *CreateUserRequest) (*CreateUserResponse, error) {
	if req.Email == "" || req.Username == "" {
		return nil, kerrors.BadRequest("INVALID_ARGUMENT", "email and username are required")
	}

	u, err := s.uc.CreateUser(ctx, req.Email, req.Username)
	if err != nil {
		switch {
		case errors.Is(err, biz.ErrUserAlreadyExists):
			return nil, kerrors.Conflict("USER_CONFLICT", "user with this email already exists")
		case errors.Is(err, biz.ErrInvalidUserData):
			return nil, kerrors.BadRequest("INVALID_ARGUMENT", err.Error())
		default:
			return nil, kerrors.InternalServer("INTERNAL_ERROR", "an unexpected error occurred")
		}
	}

	return &CreateUserResponse{
		ID:        u.ID,
		Email:     u.Email,
		Username:  u.Username,
		CreatedAt: u.CreatedAt.Format("2006-01-02T15:04:05Z07:00"),
	}, nil
}

func (s *UserService) GetUser(ctx context.Context, req *GetUserRequest) (*CreateUserResponse, error) {
	u, err := s.uc.GetUser(ctx, req.ID)
	if err != nil {
		if errors.Is(err, biz.ErrUserNotFound) {
			return nil, kerrors.NotFound("USER_NOT_FOUND", "requested user does not exist")
		}
		return nil, kerrors.InternalServer("INTERNAL_ERROR", "failed retrieving user")
	}

	return &CreateUserResponse{
		ID:        u.ID,
		Email:     u.Email,
		Username:  u.Username,
		CreatedAt: u.CreatedAt.Format("2006-01-02T15:04:05Z07:00"),
	}, nil
}
```

##### 4. Dependency Injection Declaration: `cmd/server/wire.go`
```go
//go:build wireinject
// +build wireinject

package main

import (
	"github.com/go-kratos/kratos/v2/log"
	"github.com/google/wire"

	"agent-skills/internal/biz"
	"agent-skills/internal/data"
	"agent-skills/internal/service"
)

func initApp(logger log.Logger) (*service.UserService, func(), error) {
	panic(wire.Build(
		data.ProviderSet,
		biz.NewUserUsecase,
		service.NewUserService,
	))
}
```

---

#### 3.1.3 PHP 8.3/8.4+: Laravel 11/12+ Domain-Driven Design (DDD)

In modern enterprise PHP, traditional anemic MVC (`app/Http/Controllers`, `app/Models`) is superseded by a Bounded Context DDD architecture:
- `Domain/<Context>/Data`: Strongly typed, immutable Spatie Laravel Data DTOs.
- `Domain/<Context>/Actions`: Single-responsibility invokable command actions.
- `Domain/<Context>/Repositories`: Domain repository interfaces.
- `Infrastructure/<Context>/Repositories`: Concrete Eloquent repository implementations.
- `Providers/Domain/`: Service Providers binding domain interfaces to infrastructure adapters.

##### 1. Strongly Typed DTO: `app/Domain/Order/Data/CreateOrderData.php`
```php
<?php

declare(strict_types=1);

namespace App\Domain\Order\Data;

use Spatie\LaravelData\Attributes\Validation\ArrayType;
use Spatie\LaravelData\Attributes\Validation\Email;
use Spatie\LaravelData\Attributes\Validation\Min;
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Data;

final class CreateOrderData extends Data
{
    /**
     * @param array<int, OrderItemData> $items
     */
    public function __construct(
        #[Required]
        public readonly string $customerId,

        #[Required, Email]
        public readonly string $customerEmail,

        #[Required]
        public readonly string $currency,

        #[Required, ArrayType, Min(1)]
        public readonly array $items,

        public readonly ?string $discountCode = null,
        public readonly string $traceparent = '',
    ) {}
}
```

##### 2. Sub-Item DTO: `app/Domain/Order/Data/OrderItemData.php`
```php
<?php

declare(strict_types=1);

namespace App\Domain\Order\Data;

use Spatie\LaravelData\Attributes\Validation\Min;
use Spatie\LaravelData\Attributes\Validation\Required;
use Spatie\LaravelData\Data;

final class OrderItemData extends Data
{
    public function __construct(
        #[Required]
        public readonly string $productId,

        #[Required, Min(1)]
        public readonly int $quantity,

        #[Required, Min(0)]
        public readonly int $unitPriceCents,
    ) {}

    // PHP 8.4 Property Hook computing line item subtotal
    public int $subtotalCents {
        get => $this->quantity * $this->unitPriceCents;
    }
}
```

##### 3. Domain Repository Interface: `app/Domain/Order/Repositories/OrderRepositoryInterface.php`
```php
<?php

declare(strict_types=1);

namespace App\Domain\Order\Repositories;

use App\Domain\Order\Data\OrderItemData;
use App\Domain\Order\Models\Order;

interface OrderRepositoryInterface
{
    public function findByIdForUpdate(string $id): ?Order;

    /**
     * @param array<int, OrderItemData> $items
     */
    public function save(Order $order, array $items = []): Order;
}
```

##### 4. Eloquent Repository Adapter: `app/Infrastructure/Order/Repositories/EloquentOrderRepository.php`
```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Order\Repositories;

use App\Domain\Order\Data\OrderItemData;
use App\Domain\Order\Models\Order;
use App\Domain\Order\Repositories\OrderRepositoryInterface;
use Illuminate\Database\DatabaseManager;
use Illuminate\Support\Str;

final readonly class EloquentOrderRepository implements OrderRepositoryInterface
{
    public function __construct(
        private DatabaseManager $databaseManager,
    ) {}

    public function findByIdForUpdate(string $id): ?Order
    {
        /** @var Order|null $order */
        $order = Order::query()
            ->where('id', $id)
            ->lockForUpdate()
            ->first();

        return $order;
    }

    /**
     * @param array<int, OrderItemData> $items
     */
    public function save(Order $order, array $items = []): Order
    {
        $this->databaseManager->transaction(function () use ($order, $items): void {
            $order->save();

            foreach ($items as $item) {
                $order->items()->create([
                    'id' => (string) Str::uuid(),
                    'product_id' => $item->productId,
                    'quantity' => $item->quantity,
                    'unit_price_cents' => $item->unitPriceCents,
                ]);
            }
        });

        return $order;
    }
}
```

##### 5. Invokable Domain Action: `app/Domain/Order/Actions/CreateOrderAction.php`
```php
<?php

declare(strict_types=1);

namespace App\Domain\Order\Actions;

use App\Domain\Order\Data\CreateOrderData;
use App\Domain\Order\Events\OrderCreatedEvent;
use App\Domain\Order\Exceptions\InvalidOrderTotalException;
use App\Domain\Order\Models\Order;
use App\Domain\Order\Repositories\OrderRepositoryInterface;
use Illuminate\Contracts\Events\Dispatcher;
use Illuminate\Database\DatabaseManager;
use Illuminate\Support\Str;

final readonly class CreateOrderAction
{
    public function __construct(
        private DatabaseManager $databaseManager,
        private OrderRepositoryInterface $orderRepository,
        private Dispatcher $eventDispatcher,
    ) {}

    public function __invoke(CreateOrderData $data): Order
    {
        return $this->databaseManager->transaction(function () use ($data): Order {
            $totalCents = 0;
            foreach ($data->items as $item) {
                $totalCents += $item->subtotalCents;
            }

            if ($totalCents <= 0) {
                throw new InvalidOrderTotalException('Order total must be greater than zero.');
            }

            $order = new Order();
            $order->id = (string) Str::uuid();
            $order->customer_id = $data->customerId;
            $order->customer_email = $data->customerEmail;
            $order->currency = $data->currency;
            $order->total_cents = $totalCents;
            $order->status = 'pending';

            // Persist aggregate root and child items via repository port
            $savedOrder = $this->orderRepository->save($order, $data->items);

            // Dispatch domain event carrying context facts; infrastructure event subscriber
            // handles transactional outbox record creation without domain model leakage
            $this->eventDispatcher->dispatch(new OrderCreatedEvent(
                orderId: $savedOrder->id,
                customerId: $savedOrder->customer_id,
                totalCents: $savedOrder->total_cents,
                currency: $savedOrder->currency,
                traceparent: $data->traceparent,
            ));

            return $savedOrder;
        });
    }
}
```

##### 6. Domain Service Provider: `app/Providers/Domain/OrderDomainServiceProvider.php`
```php
<?php

declare(strict_types=1);

namespace App\Providers\Domain;

use App\Domain\Order\Repositories\OrderRepositoryInterface;
use App\Infrastructure\Order\Repositories\EloquentOrderRepository;
use Illuminate\Support\ServiceProvider;

final class OrderDomainServiceProvider extends ServiceProvider
{
    /**
     * @var array<class-string, class-string>
     */
    public array $bindings = [
        OrderRepositoryInterface::class => EloquentOrderRepository::class,
    ];

    public function register(): void
    {
        // Custom domain bindings
    }

    public function boot(): void
    {
        // Register domain events or observer registrations
    }
}
```

---

#### 3.1.4 Python 3.13+: FastAPI + Dishka Scoped IoC + SQLAlchemy 2.0 Async Unit of Work

In Python, standard FastAPI dependency injection (`Depends`) tightly couples business logic to Starlette's HTTP request lifecycle. To achieve true Clean Architecture, **Dishka** is used as a framework-agnostic scoped IoC container, allowing use cases to run identically in FastAPI endpoints, background tasks, or CLI commands.

##### Complete Compiling Blueprint: Domain, Persistence, UoW, Dishka Providers, and Endpoint
```python
from abc import ABC, abstractmethod
from collections.abc import AsyncIterable
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Protocol
from uuid import UUID, uuid4

from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import FromDishka, inject, setup_dishka
from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Numeric, String, select
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# ==========================================
# 1. DOMAIN LAYER (Zero Framework Dependencies)
# ==========================================

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class DomainError(Exception):
    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

class OrderNotFoundError(DomainError):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(f"Order {order_id} not found", code="ORDER_NOT_FOUND")
        self.order_id = order_id

class OrderCannotBeCancelledError(DomainError):
    def __init__(self, order_id: UUID, current_status: OrderStatus) -> None:
        super().__init__(
            f"Order {order_id} with status {current_status.value} cannot be cancelled",
            code="ORDER_CANNOT_BE_CANCELLED",
        )
        self.order_id = order_id
        self.current_status = current_status

@dataclass
class Order:
    id: UUID
    customer_id: UUID
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    def cancel(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise OrderCannotBeCancelledError(self.id, self.status)
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)

class OrderRepository(Protocol):
    async def get_by_id(self, order_id: UUID) -> Order | None: ...
    async def save(self, order: Order) -> None: ...

class UnitOfWork(Protocol):
    orders: OrderRepository

    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

# ==========================================
# 2. INFRASTRUCTURE / PERSISTENCE LAYER
# ==========================================

class Base(DeclarativeBase):
    pass

class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def to_domain(self) -> Order:
        return Order(
            id=self.id,
            customer_id=self.customer_id,
            total_amount=float(self.total_amount),
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, order_id: UUID) -> Order | None:
        stmt = select(OrderORM).where(OrderORM.id == order_id)
        result = await self._session.execute(stmt)
        orm_order = result.scalar_one_or_none()
        return orm_order.to_domain() if orm_order else None

    async def save(self, order: Order) -> None:
        orm_order = await self._session.get(OrderORM, order.id)
        if orm_order is None:
            orm_order = OrderORM(
                id=order.id,
                customer_id=order.customer_id,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
            )
            self._session.add(orm_order)
        else:
            orm_order.status = order.status
            orm_order.updated_at = order.updated_at
            orm_order.total_amount = order.total_amount

class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker
        self._session: AsyncSession | None = None
        self.orders: OrderRepository

    async def __aenter__(self) -> UnitOfWork:
        self._session = self._sessionmaker()
        self.orders = SQLAlchemyOrderRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        if self._session:
            if exc_type is not None:
                await self.rollback()
            await self._session.close()

    async def commit(self) -> None:
        if self._session is None:
            raise RuntimeError("Session not initialized in UnitOfWork")
        await self._session.commit()

    async def rollback(self) -> None:
        if self._session is None:
            raise RuntimeError("Session not initialized in UnitOfWork")
        await self._session.rollback()

# ==========================================
# 3. APPLICATION LAYER (Use Cases)
# ==========================================

class CancelOrderUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, order_id: UUID) -> Order:
        async with self._uow:
            order = await self._uow.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(order_id)
            order.cancel()
            await self._uow.orders.save(order)
            await self._uow.commit()
            return order

# ==========================================
# 4. DISHKA DEPENDENCY INJECTION PROVIDERS
# ==========================================

class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self) -> AsyncEngine:
        return create_async_engine("postgresql+asyncpg://user:pass@localhost:5432/app")

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    def get_unit_of_work(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> UnitOfWork:
        return SQLAlchemyUnitOfWork(sessionmaker)

class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_cancel_order_use_case(self, uow: UnitOfWork) -> CancelOrderUseCase:
        return CancelOrderUseCase(uow)

# ==========================================
# 5. PRESENTATION LAYER (FastAPI)
# ==========================================

class OrderResponseDTO(BaseModel):
    id: UUID
    customer_id: UUID
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router.post("/{order_id}/cancel", response_model=OrderResponseDTO, status_code=status.HTTP_200_OK)
@inject
async def cancel_order_endpoint(
    order_id: UUID,
    use_case: FromDishka[CancelOrderUseCase],
) -> Any:
    order = await use_case.execute(order_id)
    return order

def create_app() -> FastAPI:
    app = FastAPI(title="Clean Architecture Service")
    app.include_router(router)
    container = make_async_container(DatabaseProvider(), ApplicationProvider())
    setup_dishka(container, app)
    return app
```


---

### 3.2 Case Study 2: Transaction Safety, Atomic InTx & The Transactional Outbox

#### 3.2.1 The Distributed Dual-Write Dilemma
In distributed microservices, a classic catastrophic failure vector is the **Dual-Write Anti-Pattern**:
```
Client Request ──> [ Service Handler ]
                         │
        ┌────────────────┴────────────────┐
        ▼ (1) DB Write                   ▼ (2) Broker Publish (Kafka/RabbitMQ)
  [ PostgreSQL ]                  [ Message Broker ]
```
If the database commit succeeds but the network connection to the broker times out, or the pod restarts before publishing, the event is permanently lost. If the broker publish happens first and the database transaction subsequently fails or rolls back, downstream services process phantom events that do not exist in the primary datastore.

Distributed two-phase commit (2PC / XA) protocols are strongly discouraged in cloud environments due to network latency, coordinator single points of failure, and row lock hold durations.

**The Production Solution: The Transactional Outbox Pattern**
1. **Atomic InTx Write**: The application mutates domain state and records an outbound event in an `outbox` table within the **exact same ACID database transaction**.
2. **Asynchronous Polling or CDC Forwarding**: A background relay daemon polls the `outbox` table using `SELECT ... FOR UPDATE SKIP LOCKED` and dispatches messages to the broker.
3. **At-Least-Once Delivery**: Once published, the outbox record is marked `PUBLISHED` or deleted. If the relay crashes mid-dispatch, another worker picks up the row; downstream consumers enforce idempotency.

---

#### 3.2.2 Go 1.25+: Atomic InTx Persistence & Outbox Relay Worker with `SKIP LOCKED`

```go
package outbox

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"time"

	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

type OutboxStatus string

const (
	StatusPending    OutboxStatus = "PENDING"
	StatusProcessing OutboxStatus = "PROCESSING"
	StatusPublished  OutboxStatus = "PUBLISHED"
	StatusFailed     OutboxStatus = "FAILED"
)

type OutboxRecord struct {
	ID            int64        `gorm:"primaryKey;autoIncrement"`
	AggregateType string       `gorm:"type:varchar(100);not null;index:idx_outbox_fetch"`
	AggregateID   string       `gorm:"type:varchar(100);not null"`
	EventType     string       `gorm:"type:varchar(100);not null"`
	Payload       []byte       `gorm:"type:jsonb;not null"`
	Headers       []byte       `gorm:"type:jsonb;not null"`
	Status        OutboxStatus `gorm:"type:varchar(20);not null;default:'PENDING';index:idx_outbox_fetch"`
	RetryCount    int          `gorm:"not null;default:0"`
	LastErr       string       `gorm:"type:text"`
	CreatedAt     time.Time    `gorm:"not null;index:idx_outbox_fetch"`
	LockedAt      *time.Time
	ProcessedAt   *time.Time
}

func (OutboxRecord) TableName() string {
	return "outbox_records"
}

type OrderRecord struct {
	ID        int64     `gorm:"primaryKey;autoIncrement"`
	UserID    int64     `gorm:"not null"`
	Amount    int64     `gorm:"not null"`
	Status    string    `gorm:"type:varchar(50);not null"`
	CreatedAt time.Time `gorm:"not null"`
}

func (OrderRecord) TableName() string {
	return "orders"
}

type OrderCreatedPayload struct {
	OrderID   int64 `json:"order_id"`
	UserID    int64 `json:"user_id"`
	Amount    int64 `json:"amount"`
	Timestamp int64 `json:"timestamp"`
}

type MessagePublisher interface {
	Publish(ctx context.Context, topic string, key string, payload []byte) error
}

type OrderService struct {
	db *gorm.DB
}

func NewOrderService(db *gorm.DB) *OrderService {
	return &OrderService{db: db}
}

// CreateOrder writes order and outbox record atomically in the same transaction
func (s *OrderService) CreateOrder(ctx context.Context, userID int64, amount int64) (*OrderRecord, error) {
	var order *OrderRecord

	err := s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		now := time.Now().UTC()
		order = &OrderRecord{
			UserID:    userID,
			Amount:    amount,
			Status:    "PENDING_PAYMENT",
			CreatedAt: now,
		}
		if err := tx.Create(order).Error; err != nil {
			return fmt.Errorf("failed creating order: %w", err)
		}

		payloadBytes, err := json.Marshal(OrderCreatedPayload{
			OrderID:   order.ID,
			UserID:    order.UserID,
			Amount:    order.Amount,
			Timestamp: now.Unix(),
		})
		if err != nil {
			return fmt.Errorf("failed marshaling payload: %w", err)
		}

		outboxMsg := &OutboxRecord{
			AggregateType: "order",
			AggregateID:   fmt.Sprintf("%d", order.ID),
			EventType:     "order.created",
			Payload:       payloadBytes,
			Headers:       []byte(`{"traceparent":"00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"}`),
			Status:        StatusPending,
			CreatedAt:     now,
		}
		if err := tx.Create(outboxMsg).Error; err != nil {
			return fmt.Errorf("failed creating outbox record: %w", err)
		}

		return nil
	})

	if err != nil {
		return nil, err
	}
	return order, nil
}

type OutboxRelayWorker struct {
	db        *gorm.DB
	publisher MessagePublisher
	batchSize int
}

func NewOutboxRelayWorker(db *gorm.DB, publisher MessagePublisher, batchSize int) *OutboxRelayWorker {
	if batchSize <= 0 {
		batchSize = 50
	}
	return &OutboxRelayWorker{
		db:        db,
		publisher: publisher,
		batchSize: batchSize,
	}
}

// ProcessBatch fetches pending records using SELECT ... FOR UPDATE SKIP LOCKED,
// decouples external broker publishing from DB transaction locks, and marks records processed.
func (w *OutboxRelayWorker) ProcessBatch(ctx context.Context) (int, error) {
	var records []OutboxRecord
	now := time.Now().UTC()

	// Step 1: Short DB transaction to fetch and transition records to PROCESSING with locked_at timestamp
	err := w.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		staleThreshold := now.Add(-5 * time.Minute)
		// Fetch PENDING records or recover stranded PROCESSING records from crashed worker pods
		err := tx.Clauses(clause.Locking{
			Strength: "UPDATE",
			Options:  "SKIP LOCKED",
		}).Where("(status = ? OR (status = ? AND locked_at < ?)) AND retry_count < ?",
			StatusPending, StatusProcessing, staleThreshold, 5).
			Order("created_at ASC").
			Limit(w.batchSize).
			Find(&records).Error

		if err != nil {
			return fmt.Errorf("failed selecting outbox records: %w", err)
		}

		if len(records) == 0 {
			return nil
		}

		recordIDs := make([]int64, len(records))
		for i := range records {
			recordIDs[i] = records[i].ID
		}

		return tx.Model(&OutboxRecord{}).
			Where("id IN ?", recordIDs).
			Updates(map[string]any{
				"status":    StatusProcessing,
				"locked_at": now,
			}).Error
	}, &sql.TxOptions{Isolation: sql.LevelReadCommitted})

	if err != nil {
		return 0, fmt.Errorf("outbox step 1 (claim) failed: %w", err)
	}

	if len(records) == 0 {
		return 0, nil
	}

	// Step 2: Publish messages to Kafka/RabbitMQ outside any database transaction,
	// preventing DB connection starvation during network broker latency.
	type publishResult struct {
		id      int64
		success bool
		errMsg  string
	}
	results := make([]publishResult, len(records))

	for i := range records {
		rec := &records[i]
		publishErr := w.publisher.Publish(ctx, rec.EventType, rec.AggregateID, rec.Payload)
		if publishErr == nil {
			results[i] = publishResult{id: rec.ID, success: true}
		} else {
			results[i] = publishResult{id: rec.ID, success: false, errMsg: publishErr.Error()}
		}
	}

	// Step 3: Second short DB transaction to mark published or failed messages
	processedTime := time.Now().UTC()
	err = w.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for _, res := range results {
			if res.success {
				if updateErr := tx.Model(&OutboxRecord{}).
					Where("id = ?", res.id).
					Updates(map[string]any{
						"status":       StatusPublished,
						"processed_at": processedTime,
					}).Error; updateErr != nil {
					return updateErr
				}
			} else {
				if updateErr := tx.Model(&OutboxRecord{}).
					Where("id = ?", res.id).
					Updates(map[string]any{
						"retry_count": gorm.Expr("retry_count + 1"),
						"last_err":    res.errMsg,
						"status":      gorm.Expr("CASE WHEN retry_count + 1 >= 5 THEN ? ELSE ? END", StatusFailed, StatusPending),
					}).Error; updateErr != nil {
					return updateErr
				}
			}
		}
		return nil
	}, &sql.TxOptions{Isolation: sql.LevelReadCommitted})

	if err != nil {
		return len(records), fmt.Errorf("outbox step 3 (finalize) failed: %w", err)
	}

	return len(records), nil
}

func (w *OutboxRelayWorker) Start(ctx context.Context, interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			for {
				count, err := w.ProcessBatch(ctx)
				if err != nil || count < w.batchSize {
					break
				}
			}
		}
	}
}
```

---

#### 3.2.3 PHP 8.3/8.4+: Laravel Outbox Migration & Daemon Relay Command with `skipLocked()`

##### 1. Database Migration: `database/migrations/2026_09_16_000001_create_outbox_messages_table.php`
```php
<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('outbox_messages', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->string('event_type', 128)->index();
            $table->string('aggregate_type', 64);
            $table->string('aggregate_id', 64)->index();
            $table->jsonb('payload');
            $table->jsonb('headers')->nullable();
            $table->string('status', 32)->default('PENDING')->index();
            $table->unsignedInteger('retry_count')->default(0);
            $table->text('last_error')->nullable();
            $table->timestampTz('scheduled_at')->index();
            $table->timestampTz('published_at')->nullable();
            $table->timestampsTz();

            $table->index(['status', 'scheduled_at'], 'idx_outbox_pending_scheduled');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('outbox_messages');
    }
};
```

##### 2. Concurrent Outbox Publisher Artisan Command: `app/Console/Commands/ProcessOutboxMessagesCommand.php`
```php
<?php

declare(strict_types=1);

namespace App\Console\Commands;

use App\Infrastructure\Outbox\Models\OutboxMessage;
use Illuminate\Console\Command;
use Illuminate\Database\DatabaseManager;
use Throwable;

final class ProcessOutboxMessagesCommand extends Command
{
    protected $signature = 'outbox:process {--batch=100} {--max-retries=5}';
    protected $description = 'Process and publish pending transactional outbox messages using PostgreSQL SKIP LOCKED';

    public function handle(DatabaseManager $database): int
    {
        $batchSize = (int) $this->option('batch');
        $maxRetries = (int) $this->option('max-retries');

        // Select and lock rows concurrently avoiding race conditions across workers
        $messages = $database->transaction(function () use ($batchSize): array {
            /** @var \Illuminate\Database\Eloquent\Collection<int, OutboxMessage> $lockedMessages */
            $lockedMessages = OutboxMessage::query()
                ->where(function ($query) {
                    $query->where('status', 'PENDING')
                        ->orWhere(function ($subQuery) {
                            // Recover stranded messages from crashed worker pods after 5 minutes
                            $subQuery->where('status', 'PROCESSING')
                                ->where('updated_at', '<=', now()->subMinutes(5));
                        });
                })
                ->where('scheduled_at', '<=', now())
                ->orderBy('scheduled_at')
                ->limit($batchSize)
                ->lockForUpdate()
                ->skipLocked() // PostgreSQL FOR UPDATE SKIP LOCKED
                ->get();

            if ($lockedMessages->isNotEmpty()) {
                OutboxMessage::query()
                    ->whereIn('id', $lockedMessages->pluck('id'))
                    ->update([
                        'status' => 'PROCESSING',
                        'updated_at' => now(),
                    ]);
            }

            return $lockedMessages->all();
        });

        if (empty($messages)) {
            return self::SUCCESS;
        }

        foreach ($messages as $message) {
            try {
                // Publish to external message broker (Kafka, RabbitMQ, Redis Streams, or Dapr)
                // e.g. DaprClient::publishEvent('pubsub', $message->event_type, $message->payload);
                
                $message->update([
                    'status' => 'PUBLISHED',
                    'published_at' => now(),
                    'last_error' => null,
                ]);
            } catch (Throwable $e) {
                $retryCount = $message->retry_count + 1;
                $isFailed = $retryCount >= $maxRetries;

                $message->update([
                    'status' => $isFailed ? 'FAILED' : 'PENDING',
                    'retry_count' => $retryCount,
                    'last_error' => $e->getMessage(),
                    'scheduled_at' => now()->addSeconds((int) pow(2, $retryCount) + rand(1, 5)), // Exponential backoff + jitter
                ]);
            }
        }

        $this->info(sprintf('Processed %d outbox messages successfully.', count($messages)));

        return self::SUCCESS;
    }
}
```

---

#### 3.2.4 Python 3.13+: Async SQLAlchemy 2.0 Outbox Pattern & SKIP LOCKED Polling Worker

```python
import asyncio
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Protocol
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Integer,
    String,
    Text,
    select,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

logger = logging.getLogger("outbox_processor")

class Base(DeclarativeBase):
    pass

class OutboxStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class OutboxEventORM(Base):
    __tablename__ = "outbox_events"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    aggregate_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    aggregate_id: Mapped[str] = mapped_column(String(128), nullable=False)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    status: Mapped[OutboxStatus] = mapped_column(
        SQLEnum(OutboxStatus),
        default=OutboxStatus.PENDING,
        nullable=False,
        index=True,
    )
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class AccountORM(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    balance: Mapped[float] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

class MessageBrokerPublisher(Protocol):
    async def publish(self, topic: str, key: str, payload: dict[str, Any]) -> None: ...

class AccountTransferService:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def transfer_balance(
        self,
        source_id: UUID,
        destination_id: UUID,
        amount: float,
    ) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        async with self._sessionmaker() as session:
            async with session.begin():
                # Enforce consistent global lock order to eliminate database deadlocks
                first_id, second_id = sorted([source_id, destination_id])
                
                stmt_first = select(AccountORM).where(AccountORM.id == first_id).with_for_update()
                stmt_second = select(AccountORM).where(AccountORM.id == second_id).with_for_update()
                
                acc_first = (await session.execute(stmt_first)).scalar_one_or_none()
                acc_second = (await session.execute(stmt_second)).scalar_one_or_none()
                
                if not acc_first or not acc_second:
                    raise ValueError("One or both accounts not found")

                src_acc = acc_first if acc_first.id == source_id else acc_second
                dst_acc = acc_second if acc_first.id == source_id else acc_first

                if src_acc.balance < amount:
                    raise ValueError("Insufficient funds")

                src_acc.balance -= amount
                dst_acc.balance += amount
                now = datetime.now(timezone.utc)
                src_acc.updated_at = now
                dst_acc.updated_at = now

                # Atomic outbox write in the exact same transaction
                event_payload = {
                    "source_id": str(source_id),
                    "destination_id": str(destination_id),
                    "amount": amount,
                    "timestamp": now.isoformat(),
                }
                outbox_event = OutboxEventORM(
                    id=uuid4(),
                    aggregate_type="Account",
                    aggregate_id=str(source_id),
                    event_type="TransferCompleted",
                    payload=event_payload,
                    status=OutboxStatus.PENDING,
                    created_at=now,
                )
                session.add(outbox_event)

class OutboxProcessorWorker:
    def __init__(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
        publisher: MessageBrokerPublisher,
        batch_size: int = 50,
        max_retries: int = 5,
        poll_interval_seconds: float = 1.0,
    ) -> None:
        self._sessionmaker = sessionmaker
        self._publisher = publisher
        self._batch_size = batch_size
        self._max_retries = max_retries
        self._poll_interval = poll_interval_seconds

    async def process_batch(self) -> int:
        async with self._sessionmaker() as session:
            async with session.begin():
                stmt = (
                    select(OutboxEventORM)
                    .where(OutboxEventORM.status == OutboxStatus.PENDING)
                    .order_by(OutboxEventORM.created_at.asc())
                    .limit(self._batch_size)
                    .with_for_update(skip_locked=True)
                )
                result = await session.execute(stmt)
                events = list(result.scalars().all())

                if not events:
                    return 0

                for event in events:
                    try:
                        await self._publisher.publish(
                            topic=f"{event.aggregate_type.lower()}-events",
                            key=event.aggregate_id,
                            payload=event.payload,
                        )
                        event.status = OutboxStatus.PROCESSED
                        event.processed_at = datetime.now(timezone.utc)
                    except Exception as pub_err:
                        event.retry_count += 1
                        event.error_message = str(pub_err)
                        if event.retry_count >= self._max_retries:
                            event.status = OutboxStatus.FAILED
                            logger.error(
                                f"Outbox event {event.id} permanently failed after {event.retry_count} retries: {pub_err}"
                            )
                        else:
                            logger.warning(
                                f"Transient error publishing outbox event {event.id} (attempt {event.retry_count}): {pub_err}"
                            )
                return len(events)
```

---

#### 3.2.5 Preventing N+1 Query Traps Across GORM, Eloquent, and SQLAlchemy

The N+1 query problem occurs when an application executes 1 query to fetch parent records, followed by N separate queries to fetch related child records in a loop. Under load, this exhausts connection pools and causes latency spikes.

##### 1. Go (GORM)
- **Anti-Pattern (N+1)**:
```go
var orders []Order
db.Find(&orders)
for _, o := range orders {
	db.Model(&o).Association("Items").Find(&o.Items) // N queries!
}
```
- **Production Standard**: Eager load associations using `Preload`:
```go
var orders []Order
err := db.Preload("Items").Where("user_id = ?", userID).Find(&orders).Error
```

##### 2. PHP (Laravel Eloquent)
- **Anti-Pattern (N+1)**:
```php
$orders = Order::all();
foreach ($orders as $order) {
    echo $order->customer->email; // N queries!
}
```
- **Production Standard**: Eager load via `with()`, and boot strict mode in `AppServiceProvider` to throw exceptions during local/CI test runs:
```php
// AppServiceProvider.php
public function boot(): void
{
    Model::shouldBeStrict(!app()->isProduction());
}

// Repository Call
$orders = Order::query()->with(['customer', 'items'])->get();
```

##### 3. Python (SQLAlchemy 2.0 Async)
- **Anti-Pattern (N+1 & MissingGreenlet)**:
```python
stmt = select(OrderORM)
orders = (await session.execute(stmt)).scalars().all()
for o in orders:
    print(o.items) # Crashes with sqlalchemy.exc.MissingGreenlet in async context!
```
- **Production Standard**: Explicit eager loading via `selectinload` (or `joinedload` for 1-to-1 relations):
```python
from sqlalchemy.orm import selectinload

stmt = select(OrderORM).options(selectinload(OrderORM.items)).where(OrderORM.customer_id == customer_id)
result = await session.execute(stmt)
orders = result.scalars().all()
```


---

### 3.3 Case Study 3: Resilience & Fault Tolerance

#### 3.3.1 Mathematical Resilience: Jitter, Rate Limiting, and Circuit Breaking

When downstream services (payment gateways, identity providers, AI model inference servers) degrade, naive retry loops create **Thundering Herd** cascades that amplify outages. Production resilience requires four mathematical mechanisms:

1. **Exponential Backoff with AWS Full Jitter**:
   - *Naive Exponential Backoff*: $t = \min(\text{cap}, \text{base} \times 2^{\text{attempt}})$. This synchronizes clients into periodic retry spikes.
   - *AWS Full Jitter*: Sleep duration is selected uniformly at random between 0 and the exponential backoff ceiling:
     $$t_{\text{sleep}} = \text{Uniform}(0, \min(\text{cap}, \text{base} \times 2^{\text{attempt}}))$$
   - This spreads retry requests evenly across time, maximizing downstream service recovery probability.
2. **Token Bucket Rate Limiting**:
   - Tokens refill at rate $r$ per second up to bucket capacity $b$. Requests consume $c$ tokens. This accommodates brief bursts while strictly bounding sustained throughput.
3. **Circuit Breaker Finite State Machine**:
   - `CLOSED`: Requests flow normally. Failures increment an error counter.
   - `OPEN`: If error rate exceeds a threshold (e.g., 50% failures over 10 calls), the circuit trips to `OPEN`. All subsequent calls fail immediately (fast-fail) without touching the network.
   - `HALF-OPEN`: After a recovery cooldown (e.g., 30s), the breaker enters `HALF-OPEN`, allowing a single probe request. If successful, the circuit resets to `CLOSED`; if it fails, the circuit re-trips to `OPEN`.
4. **Idempotency Key Enforcement**:
   - Mutating HTTP methods (`POST`, `PUT`, `PATCH`) accept an `Idempotency-Key` header. Distributed locks guard in-flight processing; successful responses are cached (e.g., in Redis for 24h) and replayed on duplicate requests.

---

#### 3.3.2 Go 1.25+: Token Bucket Limiter + Gobreaker + Exponential Full Jitter

```go
package resilience

import (
	"context"
	"errors"
	"fmt"
	"io"
	"math"
	"math/rand/v2"
	"net/http"
	"time"

	"github.com/sony/gobreaker"
	"golang.org/x/time/rate"
)

var (
	ErrRateLimitExceeded  = errors.New("resilience: rate limit exceeded")
	ErrCircuitBreakerOpen = errors.New("resilience: circuit breaker is open")
)

type BackoffConfig struct {
	BaseDelay  time.Duration
	MaxDelay   time.Duration
	MaxRetries int
}

func DefaultBackoffConfig() BackoffConfig {
	return BackoffConfig{
		BaseDelay:  100 * time.Millisecond,
		MaxDelay:   3 * time.Second,
		MaxRetries: 3,
	}
}

// FullJitterSleep implements the AWS Full Jitter backoff algorithm
func FullJitterSleep(attempt int, cfg BackoffConfig) time.Duration {
	if attempt < 0 {
		attempt = 0
	}
	multiplier := math.Pow(2, float64(attempt))
	temp := float64(cfg.BaseDelay) * multiplier
	maxSleep := math.Min(float64(cfg.MaxDelay), temp)
	if maxSleep <= 0 {
		return 0
	}
	return time.Duration(rand.Float64() * maxSleep)
}

type ResilientCaller struct {
	limiter *rate.Limiter
	cb      *gobreaker.CircuitBreaker
	backoff BackoffConfig
}

func NewResilientCaller(qps int, burst int, cbName string, backoff BackoffConfig) *ResilientCaller {
	st := gobreaker.Settings{
		Name:        cbName,
		MaxRequests: 5,
		Interval:    10 * time.Second,
		Timeout:     5 * time.Second,
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			failureRatio := float64(counts.TotalFailures) / float64(counts.Requests)
			return counts.Requests >= 10 && failureRatio >= 0.5
		},
	}

	return &ResilientCaller{
		limiter: rate.NewLimiter(rate.Limit(qps), burst),
		cb:      gobreaker.NewCircuitBreaker(st),
		backoff: backoff,
	}
}

func (rc *ResilientCaller) Execute(
	ctx context.Context,
	idempotencyKey string,
	op func(ctx context.Context, idempotencyKey string) (*http.Response, error),
) (*http.Response, error) {
	var lastErr error

	for attempt := 0; attempt <= rc.backoff.MaxRetries; attempt++ {
		if attempt > 0 {
			sleepDuration := FullJitterSleep(attempt, rc.backoff)
			select {
			case <-ctx.Done():
				return nil, ctx.Err()
			case <-time.After(sleepDuration):
			}
		}

		// Enforce local token bucket rate limiting
		if err := rc.limiter.Wait(ctx); err != nil {
			return nil, fmt.Errorf("%w: %v", ErrRateLimitExceeded, err)
		}

		// Execute through circuit breaker
		res, cbErr := rc.cb.Execute(func() (any, error) {
			resp, err := op(ctx, idempotencyKey)
			if err != nil {
				return nil, err
			}
			// 5xx errors trip the breaker; 4xx client errors do not trip the breaker.
			// Drain and close response body to prevent socket leaks under 5xx server errors.
			if resp.StatusCode >= 500 {
				_, _ = io.Copy(io.Discard, resp.Body)
				_ = resp.Body.Close()
				return resp, fmt.Errorf("server error with status: %d", resp.StatusCode)
			}
			return resp, nil
		})

		if cbErr == nil {
			return res.(*http.Response), nil
		}

		lastErr = cbErr
		if errors.Is(cbErr, gobreaker.ErrOpenState) || errors.Is(cbErr, gobreaker.ErrTooManyRequests) {
			return nil, fmt.Errorf("%w: %v", ErrCircuitBreakerOpen, cbErr)
		}
	}

	return nil, fmt.Errorf("resilience: operation failed after %d attempts: %w", rc.backoff.MaxRetries+1, lastErr)
}
```

---

#### 3.3.3 PHP 8.3/8.4+: Resilient Saloon v3 Connector with Circuit Breaker & Idempotency Keys

##### 1. Payment Gateway Connector: `app/Infrastructure/Payment/PaymentGatewayConnector.php`
```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Payment;

use Illuminate\Support\Facades\Cache;
use Saloon\Http\Connector;
use Saloon\Http\Request;
use Saloon\Http\Response;
use Saloon\Traits\Plugins\AlwaysThrowOnErrors;
use Saloon\Traits\Plugins\HasTimeout;
use RuntimeException;

final class PaymentGatewayConnector extends Connector
{
    use AlwaysThrowOnErrors;
    use HasTimeout;

    protected int $connectTimeout = 3;
    protected int $requestTimeout = 10;

    public function __construct(
        private readonly string $apiBaseUrl,
        private readonly string $apiSecretKey,
    ) {}

    public function resolveBaseUrl(): string
    {
        return $this->apiBaseUrl;
    }

    protected function defaultHeaders(): array
    {
        return [
            'Authorization' => 'Bearer ' . $this->apiSecretKey,
            'Content-Type' => 'application/json',
            'Accept' => 'application/json',
        ];
    }

    public function boot(Request $request): void
    {
        $circuitKey = 'circuit:payment_gateway:state';
        $cooldownKey = 'circuit:payment_gateway:cooldown_until';
        $probeKey = 'circuit:payment_gateway:half_open_probe';

        $state = Cache::get($circuitKey, 'CLOSED');

        if ($state === 'OPEN') {
            $cooldownUntil = (int) Cache::get($cooldownKey, 0);
            if (time() >= $cooldownUntil) {
                // Cooldown expired: transition to HALF_OPEN to admit a canary probe
                Cache::put($circuitKey, 'HALF_OPEN', 60);
                $state = 'HALF_OPEN';
            } else {
                throw new RuntimeException('Circuit breaker is OPEN. Payment gateway calls are currently suspended.');
            }
        }

        if ($state === 'HALF_OPEN') {
            // Atomic single-canary probe acquisition: only allow 1 probe request through
            // Cache::add() returns true only if the key did not exist
            $acquiredProbe = Cache::add($probeKey, '1', 15);
            if (!$acquiredProbe) {
                throw new RuntimeException('Circuit breaker is HALF_OPEN and canary probe is already in flight. Request rejected.');
            }
        }
    }

    /**
     * Execute request with exponential backoff and AWS full jitter
     */
    public function sendWithRetry(Request $request, int $maxAttempts = 3): Response
    {
        $circuitKey = 'circuit:payment_gateway:state';
        $cooldownKey = 'circuit:payment_gateway:cooldown_until';
        $failureCountKey = 'circuit:payment_gateway:failures';
        $probeKey = 'circuit:payment_gateway:half_open_probe';
        $attempt = 1;

        while ($attempt <= $maxAttempts) {
            try {
                $response = $this->send($request);
                // Success: reset failure counter, release probe lock, and restore CLOSED state
                Cache::forget($failureCountKey);
                Cache::forget($probeKey);
                Cache::put($circuitKey, 'CLOSED', 3600);

                return $response;
            } catch (\Throwable $e) {
                $currentState = Cache::get($circuitKey, 'CLOSED');

                if ($currentState === 'HALF_OPEN') {
                    // Canary probe failed in HALF_OPEN: immediately re-trip to OPEN for 30s!
                    Cache::forget($probeKey);
                    Cache::put($circuitKey, 'OPEN', 3600);
                    Cache::put($cooldownKey, time() + 30, 3600);
                    throw new RuntimeException('Canary probe failed in HALF_OPEN: circuit re-tripped to OPEN.', 0, $e);
                }

                $failures = Cache::increment($failureCountKey);

                if ($failures >= 5) {
                    Cache::put($circuitKey, 'OPEN', 3600);
                    Cache::put($cooldownKey, time() + 30, 3600); // Trip circuit for 30s cooldown
                    throw new RuntimeException('Circuit tripped to OPEN after 5 consecutive payment gateway failures.', 0, $e);
                }

                if ($attempt === $maxAttempts) {
                    throw $e;
                }

                // Full jitter backoff: uniform random between 0 and 2^attempt * 100ms
                $maxSleepMs = (int) (pow(2, $attempt) * 100);
                $jitterSleepMs = rand(10, $maxSleepMs);
                usleep($jitterSleepMs * 1000);
                $attempt++;
            }
        }

        throw new RuntimeException('Max retry attempts exhausted.');
    }
}
```

##### 2. Charge Payment Request with Idempotency Key: `app/Infrastructure/Payment/Requests/ChargePaymentRequest.php`
```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Payment\Requests;

use App\Domain\Order\Data\PaymentResultData;
use Saloon\Contracts\Body\HasBody;
use Saloon\Enums\Method;
use Saloon\Http\Request;
use Saloon\Http\Response;
use Saloon\Traits\Body\HasJsonBody;

final class ChargePaymentRequest extends Request implements HasBody
{
    use HasJsonBody;

    protected Method $method = Method::POST;

    public function __construct(
        private readonly int $amountCents,
        private readonly string $currency,
        private readonly string $paymentMethodToken,
        private readonly string $idempotencyKey,
    ) {}

    public function resolveEndpoint(): string
    {
        return '/v1/charges';
    }

    protected function defaultHeaders(): array
    {
        return [
            'Idempotency-Key' => $this->idempotencyKey,
        ];
    }

    protected function defaultBody(): array
    {
        return [
            'amount' => $this->amountCents,
            'currency' => $this->currency,
            'payment_method' => $this->paymentMethodToken,
        ];
    }

    public function createDtoFromResponse(Response $response): PaymentResultData
    {
        $data = $response->json();

        return new PaymentResultData(
            transactionId: (string) $data['id'],
            status: (string) $data['status'],
            amountCents: (int) $data['amount'],
            currency: (string) $data['currency'],
        );
    }
}
```

---

#### 3.3.4 Python 3.13+: Tenacity Jitter + Redis Lua Token Bucket + Circuit Breaker + Idempotency Middleware

```python
import asyncio
import hashlib
import json
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any
from fastapi import FastAPI, HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response as StarletteResponse
import httpx
from redis.asyncio import Redis
from tenacity import (
    AsyncRetrying,
    RetryCallState,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

logger = logging.getLogger("resilience")

# ==========================================
# 1. TENACITY RETRY WITH EXPONENTIAL FULL JITTER
# ==========================================

def log_retry_attempt(retry_state: RetryCallState) -> None:
    fn_name = retry_state.fn.__name__ if retry_state.fn else "callable"
    attempt = retry_state.attempt_number
    outcome = retry_state.outcome
    exception = outcome.exception() if outcome else None
    logger.warning(
        f"Retry attempt {attempt} for {fn_name} due to error: {exception}. Backing off with jitter..."
    )

async def call_external_payment_gateway(
    client: httpx.AsyncClient,
    payload: dict[str, Any],
    idempotency_key: str,
) -> dict[str, Any]:
    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(4),
        wait=wait_random_exponential(multiplier=0.5, max=8.0),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        before_sleep=log_retry_attempt,
        reraise=True,
    ):
        with attempt:
            response = await client.post(
                "https://api.payment.example.com/v1/charges",
                json=payload,
                headers={"Idempotency-Key": idempotency_key},
                timeout=5.0,
            )
            if response.status_code in (429, 500, 502, 503, 504):
                response.raise_for_status()
            return response.json()
    raise RuntimeError("Unreachable")

# ==========================================
# 2. REDIS TOKEN-BUCKET RATE LIMITER (Atomic Lua Script)
# ==========================================

LUA_TOKEN_BUCKET = '''
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local data = redis.call('HMGET', key, 'tokens', 'last_updated')
local tokens = tonumber(data[1])
local last_updated = tonumber(data[2])

if tokens == nil then
    tokens = capacity
    last_updated = now
else
    local elapsed = math.max(0, now - last_updated)
    tokens = math.min(capacity, tokens + (elapsed * refill_rate))
    last_updated = now
end

if tokens >= requested then
    tokens = tokens - requested
    redis.call('HMSET', key, 'tokens', tokens, 'last_updated', last_updated)
    redis.call('EXPIRE', key, math.ceil(capacity / refill_rate) * 2)
    return {1, tokens}
else
    redis.call('HMSET', key, 'tokens', tokens, 'last_updated', last_updated)
    redis.call('EXPIRE', key, math.ceil(capacity / refill_rate) * 2)
    return {0, tokens}
end
'''

class RedisTokenBucketRateLimiter:
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client
        self._script = self._redis.register_script(LUA_TOKEN_BUCKET)

    async def acquire(
        self,
        identifier: str,
        capacity: int = 60,
        refill_rate_per_sec: float = 1.0,
        cost: int = 1,
    ) -> bool:
        key = f"ratelimit:{identifier}"
        now = time.time()
        allowed, _ = await self._script(
            keys=[key],
            args=[capacity, refill_rate_per_sec, now, cost],
        )
        return bool(allowed == 1)

# ==========================================
# 3. ASYNC CIRCUIT BREAKER
# ==========================================

class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreakerOpenException(Exception):
    pass

class AsyncCircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        expected_exceptions: tuple[type[Exception], ...] = (Exception,),
    ) -> None:
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._expected_exceptions = expected_exceptions
        self._failure_count = 0
        self._last_state_change = time.time()
        self._state = CircuitState.CLOSED
        self._lock = asyncio.Lock()
        self._half_open_probe_in_flight: bool = False

    async def call(self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        async with self._lock:
            now = time.time()
            if self._state == CircuitState.OPEN:
                if now - self._last_state_change > self._recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_probe_in_flight = False
                    logger.info("Circuit state shifted to HALF_OPEN: probing dependency with single canary")
                else:
                    raise CircuitBreakerOpenException("Circuit breaker is OPEN. Fast failing request.")

            if self._state == CircuitState.HALF_OPEN:
                # Single canary probe gate: prevent thundering herd during recovery
                if self._half_open_probe_in_flight:
                    raise CircuitBreakerOpenException("Circuit breaker is HALF_OPEN and canary probe is in-flight. Fast failing request.")
                self._half_open_probe_in_flight = True

        try:
            result = await func(*args, **kwargs)
        except self._expected_exceptions as exc:
            async with self._lock:
                if self._state == CircuitState.HALF_OPEN:
                    # Single probe failed: immediately re-trip to OPEN without requiring failure threshold
                    self._state = CircuitState.OPEN
                    self._last_state_change = time.time()
                    self._half_open_probe_in_flight = False
                    self._failure_count = self._failure_threshold
                    logger.error("Canary probe failed in HALF_OPEN: immediately re-tripping circuit to OPEN")
                elif self._state == CircuitState.CLOSED:
                    self._failure_count += 1
                    if self._failure_count >= self._failure_threshold:
                        self._state = CircuitState.OPEN
                        self._last_state_change = time.time()
                        logger.error(f"Circuit tripped to OPEN after {self._failure_count} failures")
            raise exc

        async with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
                self._half_open_probe_in_flight = False
                logger.info("Circuit restored to CLOSED after successful canary probe")
            elif self._state == CircuitState.CLOSED and self._failure_count > 0:
                self._failure_count = 0
        return result

# ==========================================
# 4. FASTAPI IDEMPOTENCY MIDDLEWARE
# ==========================================

class IdempotencyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Any,
        redis_client: Redis,
        expiry_seconds: int = 86400,
        in_progress_timeout: int = 60,
    ) -> None:
        super().__init__(app)
        self._redis = redis_client
        self._expiry = expiry_seconds
        self._in_progress_timeout = in_progress_timeout

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if request.method not in ("POST", "PUT", "PATCH"):
            return await call_next(request)

        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return await call_next(request)

        redis_key = f"idempotency:{idempotency_key}"
        
        body = await request.body()
        async def receive() -> dict[str, Any]:
            return {"type": "http.request", "body": body, "more_body": False}
        request._receive = receive  # type: ignore[method-assign]

        payload_hash = hashlib.sha256(body).hexdigest()
        
        # Acquire atomic processing lock
        acquired = await self._redis.set(
            f"{redis_key}:lock",
            payload_hash,
            ex=self._in_progress_timeout,
            nx=True,
        )
        if not acquired:
            cached_data = await self._redis.get(redis_key)
            if cached_data:
                record = json.loads(cached_data)
                return JSONResponse(
                    content=record["body"],
                    status_code=record["status_code"],
                    headers={"X-Cache-Lookup": "HIT-IDEMPOTENT"},
                )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": "Concurrent operation in progress with this Idempotency-Key."},
            )

        try:
            response = await call_next(request)
            
            response_body = [chunk async for chunk in response.body_iterator]  # type: ignore[attr-defined]
            full_body = b"".join(response_body)
            
            if response.status_code < 500:
                try:
                    parsed_json = json.loads(full_body.decode("utf-8"))
                except Exception:
                    parsed_json = full_body.decode("utf-8", errors="replace")
                
                cache_payload = json.dumps({
                    "status_code": response.status_code,
                    "body": parsed_json,
                })
                await self._redis.set(redis_key, cache_payload, ex=self._expiry)

            return Response(
                content=full_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
        finally:
            await self._redis.delete(f"{redis_key}:lock")
```


---

### 3.4 Case Study 4: Deterministic Error Handling & Closed Envelopes

#### 3.4.1 The RFC 9457 / RFC 7807 Problem Details Standard
Historically, APIs emitted fragmented, inconsistent error formats. In production, unhandled exceptions frequently leaked raw SQL error strings (`SQLSTATE[23505]`, `pq: duplicate key value violates unique constraint`, table/column names, internal IP addresses) directly to external clients. This violates security standards and causes brittle client-side error handling.

The modern industry standard is **RFC 9457 (superseding RFC 7807): Problem Details for HTTP APIs** (`application/problem+json`):
```json
{
  "type": "https://api.example.com/errors/user-conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "A user with the specified email address already exists.",
  "instance": "/api/v1/users",
  "code": "USER_ALREADY_EXISTS",
  "trace_id": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "timestamp": "2026-09-16T08:00:00Z"
}
```

The core invariants of deterministic error handling are:
1. **Zero Database/Internal Leakage**: Database exceptions are caught at the infrastructure boundary. Internal queries and stack traces are logged securely for engineering triage, but never exposed to external clients.
2. **Domain-Driven Mapping**: Domain logic returns pure domain errors; transport adapters map domain errors to standardized HTTP/gRPC status codes.
3. **Traceability**: Every error envelope contains a correlation/trace ID (`trace_id` or `traceparent`) enabling instant log lookup in telemetry systems.

---

#### 3.4.2 Go 1.25+: Kratos Custom Error Encoder & RFC 9457 Problem Details

```go
package errorhandling

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"

	kerrors "github.com/go-kratos/kratos/v2/errors"
	khttp "github.com/go-kratos/kratos/v2/transport/http"
	"google.golang.org/grpc/codes"
)

type ProblemDetails struct {
	Type     string            `json:"type"`
	Title    string            `json:"title"`
	Status   int               `json:"status"`
	Detail   string            `json:"detail"`
	Instance string            `json:"instance,omitempty"`
	Reason   string            `json:"reason"`
	Metadata map[string]string `json:"metadata,omitempty"`
}

// CustomErrorEncoder encodes errors into RFC 9457 application/problem+json
func CustomErrorEncoder(w http.ResponseWriter, r *http.Request, err error) {
	if err == nil {
		return
	}

	kerr := kerrors.FromError(err)
	statusCode := int(kerr.Code)
	if statusCode < 100 || statusCode > 599 {
		statusCode = http.StatusInternalServerError
	}

	problem := ProblemDetails{
		Type:     "https://api.example.com/errors/" + kerr.Reason,
		Title:    http.StatusText(statusCode),
		Status:   statusCode,
		Detail:   kerr.Message,
		Instance: r.URL.Path,
		Reason:   kerr.Reason,
		Metadata: kerr.Metadata,
	}

	w.Header().Set("Content-Type", "application/problem+json")
	w.WriteHeader(statusCode)
	_ = json.NewEncoder(w).Encode(problem)
}

// MapDomainError translates domain errors into Kratos Status/gRPC codes
func MapDomainError(err error) error {
	if err == nil {
		return nil
	}

	var ke *kerrors.Error
	if errors.As(err, &ke) {
		return ke
	}

	switch {
	case errors.Is(err, context.Canceled):
		return kerrors.New(int(codes.Canceled), "CLIENT_CLOSED_REQUEST", "request canceled by client")
	case errors.Is(err, context.DeadlineExceeded):
		return kerrors.New(int(codes.DeadlineExceeded), "GATEWAY_TIMEOUT", "upstream operation timed out")
	default:
		// Mask raw database errors, returning sanitized internal error
		return kerrors.New(int(codes.Internal), "INTERNAL_ERROR", "an unexpected system error occurred")
	}
}

func RegisterCustomEncoder(srv *khttp.Server) {
	srv.SetErrorEncoder(CustomErrorEncoder)
}
```

---

#### 3.4.3 PHP 8.3/8.4+: Laravel 11/12 Closed Error Envelopes & SQL Leakage Prevention

##### 1. Domain Exception Hierarchy: `app/Domain/Common/Exceptions/DomainException.php`
```php
<?php

declare(strict_types=1);

namespace App\Domain\Common\Exceptions;

use Exception;
use Throwable;

abstract class DomainException extends Exception
{
    abstract public function getErrorCode(): string;

    abstract public function getHttpStatus(): int;

    /**
     * @return array<string, mixed>
     */
    public function getDetails(): array
    {
        return [];
    }

    public function __construct(string $message = '', int $code = 0, ?Throwable $previous = null)
    {
        parent::__construct($message, $code, $previous);
    }
}
```

##### 2. Concrete Domain Exception: `app/Domain/Order/Exceptions/InsufficientInventoryException.php`
```php
<?php

declare(strict_types=1);

namespace App\Domain\Order\Exceptions;

use App\Domain\Common\Exceptions\DomainException;
use Symfony\Component\HttpFoundation\Response;

final class InsufficientInventoryException extends DomainException
{
    public function __construct(
        private readonly string $productId,
        private readonly int $requestedQuantity,
        private readonly int $availableQuantity,
    ) {
        parent::__construct(sprintf(
            'Insufficient inventory for product %s. Requested: %d, Available: %d',
            $productId,
            $requestedQuantity,
            $availableQuantity
        ));
    }

    public function getErrorCode(): string
    {
        return 'INSUFFICIENT_INVENTORY';
    }

    public function getHttpStatus(): int
    {
        return Response::HTTP_UNPROCESSABLE_ENTITY;
    }

    public function getDetails(): array
    {
        return [
            'product_id' => $this->productId,
            'requested_quantity' => $this->requestedQuantity,
            'available_quantity' => $this->availableQuantity,
        ];
    }
}
```

##### 3. Exception Envelope & DB Error Masking: `bootstrap/app.php`
```php
<?php

declare(strict_types=1);

use App\Domain\Common\Exceptions\DomainException;
use Illuminate\Database\QueryException;
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__ . '/../routes/web.php',
        api: __DIR__ . '/../routes/api.php',
        commands: __DIR__ . '/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        // Global middleware registrations
    })
    ->withExceptions(function (Exceptions $exceptions) {
        // 1. Map Domain Exceptions into standardized RFC 9457 error envelope
        $exceptions->render(function (DomainException $e, Request $request): JsonResponse {
            $correlationId = (string) Str::uuid();

            return response()->json([
                'type' => 'https://api.example.com/errors/' . strtolower($e->getErrorCode()),
                'title' => str_replace('_', ' ', $e->getErrorCode()),
                'status' => $e->getHttpStatus(),
                'detail' => $e->getMessage(),
                'instance' => $request->path(),
                'code' => $e->getErrorCode(),
                'details' => $e->getDetails(),
                'trace_id' => $correlationId,
            ], $e->getHttpStatus(), ['Content-Type' => 'application/problem+json']);
        });

        // 2. Strictly intercept and mask raw database errors
        $exceptions->render(function (QueryException $e, Request $request): ?JsonResponse {
            $correlationId = (string) Str::uuid();

            // Secure internal logging for engineering forensics
            Log::error('Database execution failure occurred', [
                'correlation_id' => $correlationId,
                'sql' => $e->getSql(),
                'bindings' => $e->getBindings(),
                'error_code' => $e->getCode(),
                'message' => $e->getMessage(),
            ]);

            // Mask raw database schema and SQL from external client
            return response()->json([
                'type' => 'https://api.example.com/errors/internal-database-error',
                'title' => 'Internal Server Error',
                'status' => Response::HTTP_INTERNAL_SERVER_ERROR,
                'detail' => 'An unexpected database error occurred. Quote the trace_id when contacting support.',
                'instance' => $request->path(),
                'code' => 'INTERNAL_DATABASE_ERROR',
                'trace_id' => $correlationId,
            ], Response::HTTP_INTERNAL_SERVER_ERROR, ['Content-Type' => 'application/problem+json']);
        });
    })
    ->create();
```

---

#### 3.4.4 Python 3.13+: Deterministic Error Handling & RFC 9457 Handlers in FastAPI

```python
import logging
import uuid
from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

logger = logging.getLogger("api_error_handler")

# ==========================================
# 1. CLOSED DOMAIN EXCEPTION HIERARCHY
# ==========================================

class DomainException(Exception):
    def __init__(
        self,
        message: str,
        code: str = "DOMAIN_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

class EntityNotFoundError(DomainException):
    def __init__(self, entity_name: str, entity_id: Any) -> None:
        super().__init__(
            message=f"{entity_name} with id '{entity_id}' does not exist",
            code="RESOURCE_NOT_FOUND",
            details={"entity": entity_name, "id": str(entity_id)},
        )

class DuplicateEntityError(DomainException):
    def __init__(self, entity_name: str, identifier: str) -> None:
        super().__init__(
            message=f"{entity_name} '{identifier}' already exists",
            code="RESOURCE_ALREADY_EXISTS",
            details={"entity": entity_name, "identifier": identifier},
        )

class DomainInvariantViolationError(DomainException):
    def __init__(self, rule: str, reason: str) -> None:
        super().__init__(
            message=f"Invariant violated: {rule}. Reason: {reason}",
            code="INVARIANT_VIOLATION",
            details={"rule": rule, "reason": reason},
        )

# ==========================================
# 2. RFC 9457 PROBLEM DETAILS SCHEMA
# ==========================================

class ProblemDetails(BaseModel):
    type: str = Field(
        default="about:blank",
        description="A URI reference identifying the problem type",
    )
    title: str = Field(description="Short human-readable summary of problem type")
    status: int = Field(description="HTTP status code")
    detail: str = Field(description="Human-readable explanation specific to this occurrence")
    instance: str = Field(description="URI reference of the request endpoint")
    code: str = Field(description="Machine-readable error code")
    invalid_params: list[dict[str, Any]] | None = Field(default=None)
    details: dict[str, Any] | None = Field(default=None)
    trace_id: str = Field(description="Correlation ID for distributed tracing")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="UTC timestamp of error occurrence",
    )

DOMAIN_STATUS_MAP: dict[type[DomainException], int] = {
    EntityNotFoundError: status.HTTP_404_NOT_FOUND,
    DuplicateEntityError: status.HTTP_409_CONFLICT,
    DomainInvariantViolationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
}

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
        status_code = DOMAIN_STATUS_MAP.get(type(exc), status.HTTP_400_BAD_REQUEST)
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        
        problem = ProblemDetails(
            type=f"https://api.example.com/errors/{exc.code.lower()}",
            title=exc.code.replace("_", " ").title(),
            status=status_code,
            detail=exc.message,
            instance=str(request.url.path),
            code=exc.code,
            details=exc.details,
            trace_id=trace_id,
        )
        return JSONResponse(
            status_code=status_code,
            content=problem.model_dump(exclude_none=True),
            media_type="application/problem+json",
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        invalid_params = []
        for error in exc.errors():
            loc = ".".join(str(item) for item in error.get("loc", []))
            invalid_params.append({
                "field": loc,
                "reason": error.get("msg", "Invalid input"),
                "type": error.get("type", "value_error"),
            })

        problem = ProblemDetails(
            type="https://api.example.com/errors/validation-failed",
            title="Request Validation Failed",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The request payload failed boundary schema validation.",
            instance=str(request.url.path),
            code="VALIDATION_ERROR",
            invalid_params=invalid_params,
            trace_id=trace_id,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=problem.model_dump(exclude_none=True),
            media_type="application/problem+json",
        )

    @app.exception_handler(Exception)
    async def generic_unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        
        logger.error(
            f"Unhandled exception caught on {request.method} {request.url.path} [trace_id={trace_id}]: {exc}",
            exc_info=True,
            extra={"trace_id": trace_id, "path": str(request.url.path)},
        )

        problem = ProblemDetails(
            type="https://api.example.com/errors/internal-error",
            title="Internal Server Error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request. Quote the trace_id when contacting support.",
            instance=str(request.url.path),
            code="INTERNAL_SERVER_ERROR",
            trace_id=trace_id,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=problem.model_dump(exclude_none=True),
            media_type="application/problem+json",
        )
```


---

### 3.5 Case Study 5: Advanced Concurrency & AI-Native Systems

#### 3.5.1 Go 1.25+: Goroutine Pool Recycling & Zero-Alloc Serialization

While goroutines are lightweight (~2KB initial stack), spawning unbounded goroutines (`go func() { ... }()`) under burst traffic (e.g. 100k events/sec) causes severe heap allocation spikes, GC stop-the-world latency, and eventual OOM crashes.

##### 1. High-Performance Bounded Worker Pool with `panjf2000/ants/v2`
```go
package workerpool

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/panjf2000/ants/v2"
)

type TaskPayload struct {
	ID        string
	Data      []byte
	CreatedAt time.Time
	Ctx       context.Context
}

type PoolManager struct {
	pool *ants.PoolWithFunc
	wg   sync.WaitGroup
	mu   sync.RWMutex
}

func NewPoolManager(capacity int) (*PoolManager, error) {
	mgr := &PoolManager{}

	// Initialize ants pool with panic handler and pre-allocated worker ring
	pool, err := ants.NewPoolWithFunc(capacity, func(payload any) {
		defer mgr.wg.Done()
		task, ok := payload.(*TaskPayload)
		if !ok {
			return
		}
		processTask(task)
	}, ants.WithPanicHandler(func(p any) {
		fmt.Printf("Recovered from panic in worker pool task: %v\n", p)
	}), ants.WithPreAlloc(true))

	if err != nil {
		return nil, fmt.Errorf("failed creating ants pool: %w", err)
	}

	mgr.pool = pool
	return mgr, nil
}

func processTask(task *TaskPayload) {
	// Respect cancellation and timeout deadlines passed from caller
	if task.Ctx != nil && task.Ctx.Err() != nil {
		return
	}
	// Perform CPU or I/O bound processing within controlled pool boundary
	_ = task.ID
}

func (m *PoolManager) Submit(ctx context.Context, payload TaskPayload) error {
	if err := ctx.Err(); err != nil {
		return fmt.Errorf("context canceled before submitting task: %w", err)
	}

	m.mu.RLock()
	defer m.mu.RUnlock()

	payload.Ctx = ctx
	m.wg.Add(1)
	if err := m.pool.Invoke(&payload); err != nil {
		m.wg.Done()
		return fmt.Errorf("failed invoking worker pool: %w", err)
	}
	return nil
}

func (m *PoolManager) Close() {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.wg.Wait()
	m.pool.Release()
}
```

##### 2. Serialization Benchmark: `encoding/json` vs `mailru/easyjson` vs `bytedance/sonic`
- **Standard `encoding/json`**: Uses runtime reflection (`reflect.Value`), allocating heavily on the heap and incurring ~1,200 ns/op with 15 heap allocations per struct.
- **`mailru/easyjson`**: Generates static marshalers at build time. Achieves ~350 ns/op with **0 heap allocations** during serialization.
- **`bytedance/sonic`**: Leverages runtime JIT compilation and AVX2/NEON SIMD vector instructions. Achieves ~180 ns/op for large payloads.
```go
package serialization

import (
	"github.com/bytedance/sonic"
)

type EventEnvelope struct {
	ID        string            `json:"id"`
	Type      string            `json:"type"`
	Payload   map[string]string `json:"payload"`
	Timestamp int64             `json:"timestamp"`
}

// FastSerializeSonic demonstrates SIMD zero-allocation JSON serialization
func FastSerializeSonic(env *EventEnvelope) ([]byte, error) {
	return sonic.Marshal(env)
}
```

---

#### 3.5.2 PHP 8.3/8.4+: FrankenPHP Caddy Worker Mode, 103 Early Hints & State-Bleed Elimination

##### 1. Production `Caddyfile` for FrankenPHP Worker Mode
```caddyfile
{
    frankenphp {
        num_threads 8
        worker {
            file /app/public/frankenphp-worker.php
            num 4
            env MAX_REQUESTS 1000
        }
    }
}

:80 {
    root * /app/public
    encode zstd gzip
    
    # 103 Early Hints enabled natively
    early_hints

    php_server
}
```

##### 2. Worker Loop with 103 Early Hints: `public/frankenphp-worker.php`
```php
<?php

declare(strict_types=1);

use Illuminate\Contracts\Http\Kernel;
use Illuminate\Http\Request;

require __DIR__ . '/../vendor/autoload.php';
$app = require_once __DIR__ . '/../bootstrap/app.php';
$kernel = $app->make(Kernel::class);

$handler = function () use ($app, $kernel): void {
    // Send RFC 8297 Early Hints before processing heavy backend business logic
    if (function_exists('frankenphp_send_early_hints')) {
        frankenphp_send_early_hints([
            '</build/assets/app.css>; rel=preload; as=style',
            '</build/assets/app.js>; rel=preload; as=script',
        ]);
    }

    $request = Request::capture();
    $response = $kernel->handle($request);
    $response->send();
    $kernel->terminate($request, $response);

    // Flush stateful singletons configured in config/octane.php to eliminate cross-request state bleed
    $flushable = (array) config('octane.flush', [
        \App\Domain\Billing\Services\PaymentContext::class,
        \App\Infrastructure\Telemetry\SpanContext::class,
    ]);
    foreach ($flushable as $service) {
        $app->forgetInstance($service);
    }
};

// Explicitly bound worker lifecycle to prevent memory fragmentation and leaks
$maxRequests = (int) ($_SERVER['MAX_REQUESTS'] ?? 500);

// FrankenPHP in-memory event loop
for ($nbRequests = 0; !$maxRequests || $nbRequests < $maxRequests; ++$nbRequests) {
    if (!frankenphp_handle_request($handler)) {
        break;
    }

    // Force garbage collection cycle after each request to prevent fragmentation
    gc_collect_cycles();
}
```

##### 3. Container State-Bleed Elimination in `config/octane.php`
```php
<?php

return [
    'flush' => [
        \App\Domain\Billing\Services\PaymentContext::class,
        \App\Infrastructure\Telemetry\SpanContext::class,
        \Illuminate\Support\Facades\Auth::class,
    ],
    'warm' => [
        ...Laravel\Octane\Octane::defaultServicesToWarm(),
    ],
];
```

---

#### 3.5.3 Python 3.13+: AI-Native Architecture: LiteLLM Gateway, Langfuse `@observe`, Instructor Extraction & OpenTelemetry GenAI

In production AI-native systems, LLM inferences must satisfy four non-negotiable architectural requirements:
1. **Gateway Reverse Proxy (LiteLLM)**: Abstracts upstream providers (OpenAI, Anthropic, Bedrock), handles load balancing, and executes automated failover on rate limits (HTTP 429) or server outages (HTTP 503).
2. **Deterministic Schema Extraction (Instructor + Pydantic v2)**: Replaces regex parsing with tool-calling and self-correcting validation loops (`max_retries=3`).
3. **Multi-Agent Observability (Langfuse)**: Decorator-based tracing capturing session IDs, prompt template versions, and generation histories.
4. **OpenTelemetry GenAI Semantic Conventions**: Standardized spans capturing `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, and `gen_ai.usage.output_tokens` for centralized billing and governance.

##### Complete Compiling Blueprint
```python
import os
from typing import Any
import httpx
import instructor
from langfuse.decorators import langfuse_context, observe
from openai import AsyncOpenAI
from opentelemetry import trace
from pydantic import BaseModel, Field, field_validator

tracer = trace.get_tracer("ai_service", "1.0.0")

class ExtractedFinancialInsight(BaseModel):
    company_name: str = Field(description="Full legal company name")
    ticker: str = Field(description="Stock exchange ticker symbol in uppercase")
    revenue_growth_pct: float = Field(description="YoY revenue growth percentage")
    risk_factors: list[str] = Field(min_length=1, description="Identified risk factors")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence score between 0 and 1")

    @field_validator("ticker", mode="after")
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        if not v.isalnum() or len(v) > 5:
            raise ValueError("Ticker must be 1-5 alphanumeric characters")
        return v.upper()

class FinancialAnalysisAIService:
    def __init__(self, litellm_proxy_url: str, api_key: str) -> None:
        # Route through LiteLLM Proxy Gateway for multi-model failover and rate-limiting
        self._raw_client = AsyncOpenAI(base_url=litellm_proxy_url, api_key=api_key)
        # Wrap client with Instructor for Pydantic v2 structured output extraction
        self._instructor_client = instructor.from_openai(self._raw_client)

    @observe(name="extract_financial_insights")
    async def analyze_report(
        self,
        report_text: str,
        correlation_id: str,
    ) -> ExtractedFinancialInsight:
        # Langfuse prompt and session context injection
        langfuse_context.update_current_trace(
            user_id="analyst_system",
            session_id=correlation_id,
            tags=["finance", "automated_extraction"],
            metadata={"text_length": len(report_text)},
        )

        # OpenTelemetry GenAI Semantic Convention Span
        with tracer.start_as_current_span("gen_ai.client.chat") as span:
            span.set_attribute("gen_ai.system", "openai")
            span.set_attribute("gen_ai.request.model", "gpt-4o")
            span.set_attribute("gen_ai.request.temperature", 0.0)
            span.set_attribute("workflow.correlation_id", correlation_id)

            try:
                insight: ExtractedFinancialInsight = (
                    await self._instructor_client.chat.completions.create(
                        model="gpt-4o",
                        response_model=ExtractedFinancialInsight,
                        max_retries=3,  # Self-correction loop feeding Pydantic errors back to LLM
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a financial analyst. Extract structured insight from financial text.",
                            },
                            {"role": "user", "content": report_text},
                        ],
                        temperature=0.0,
                    )
                )

                span.set_attribute("gen_ai.response.finish_reasons", ["stop"])
                span.set_attribute("financial.ticker", insight.ticker)
                span.set_attribute("financial.confidence", insight.confidence_score)
                return insight
            except Exception as exc:
                span.record_exception(exc)
                span.set_status(trace.StatusCode.ERROR, str(exc))
                raise
```


---

## 4. Comprehensive 6-Dimension Cross-Language Comparative Matrix

To guide technology selection, architecture reviews, and cross-language engineering migrations, this section evaluates Go 1.25+, Modern PHP 8.3/8.4+ (Laravel 11/12+ & FrankenPHP), and Python 3.13+ (FastAPI, Dishka & AI-Native stack) across six critical backend engineering dimensions.

---

### 4.1 Dimension 1: Layer Separation & Dependency Injection

| Dimension Criteria | Go 1.25+ (Kratos + Wire) | PHP 8.3/8.4+ (Laravel 11/12 + Spatie) | Python 3.13+ (FastAPI + Dishka) |
| :--- | :--- | :--- | :--- |
| **Primary Architecture Style** | Clean / Hexagonal (Protobuf-First 4-Layer Layout) | Domain-Driven Design (DDD Bounded Context Monolith) | Clean Architecture (Port & Adapter / UoW) |
| **DI Paradigm & Tooling** | Compile-Time Static AST Generation (`google/wire`) | Runtime Container Reflection + Service Providers | Scoped Runtime IoC Container (`reagento/dishka`) |
| **Lifecycle Hook Management** | Manual / `kratos.App` lifecycle (`app.Run()`, `app.Stop()`) | Container singletons, `boot()` and `register()` methods | Explicit scopes: `Scope.APP`, `Scope.REQUEST`, `Scope.ACTION` |
| **Failure Detection Phase** | **100% Compile-Time** (`wire gen ./...` fails on graph cycles) | **Runtime / Test Phase** (fails on container resolution) | **Container Initialization Phase** (verified on startup) |
| **Runtime Memory Overhead** | **Absolute Zero** (direct static struct initializations) | Low-to-moderate (reflected bindings cached in RAM) | Low (cached dependency instances per scope) |
| **Domain Isolation Guarantee** | Absolute: `internal/biz` bans all DB/SQL driver packages | High: Domain actions decouple Eloquent from Controllers | High: Domain entities use pure Python dataclasses / Pydantic |
| **Non-Web Context Reusability** | Native: Wires plain Go structs usable in CLI and daemons | High: Artisan commands resolve container dependencies | **Absolute**: Dishka runs identically in FastAPI, Celery, CLI |

#### Architectural Analysis
- **Go** sets the gold standard for compile-time safety and runtime performance. By enforcing dependency resolution via `google/wire` at build time, Go eliminates runtime container overhead and prevents boot-time panics. The physical package separation of `internal/biz` from `internal/data` structurally prevents ORM and database leakage.
- **PHP** has achieved high domain rigor through Laravel 11/12's streamlined foundation and Spatie's typed DTOs. While Laravel's service container relies on runtime reflection, the elimination of legacy kernels (`bootstrap/app.php`) combined with Pest `arch()` tests enables automated CI enforcement of architectural layer boundaries.
- **Python** historically suffered from leaky abstractions due to FastAPI's request-coupled `Depends`. The emergence of **Dishka** elevates Python backends to true Clean Architecture parity, providing explicit scopes (`Scope.APP`, `Scope.REQUEST`) that cleanly isolate use cases from web transports.

---

### 4.2 Dimension 2: Concurrency & Worker Runtimes

| Dimension Criteria | Go 1.25+ (Goroutines & Ants) | PHP 8.3/8.4+ (FrankenPHP & Octane) | Python 3.13+ (AsyncIO & AnyIO) |
| :--- | :--- | :--- | :--- |
| **Concurrency Primitive** | Lightweight CSP Goroutines (~2KB initial stack) | Long-Running Worker Processes + libphp threads | Single-Threaded Cooperative Event Loop (`asyncio`) |
| **Memory Isolation Model** | Shared Memory with Pointer Protection (`sync.Mutex`) | Shared Caddy Memory + Isolated Per-Worker Contexts | Single-Process Heap with Greenlet Task Frames |
| **Baseline HTTP Latency** | **Sub-millisecond (0.2ms – 0.8ms)** | **Ultra-low (1.2ms – 3.5ms in worker mode)** | **Low (2.0ms – 6.0ms in ASGI)** |
| **Concurrent Throughput** | Extreme (100k+ concurrent requests per node) | High (5k – 15k concurrent requests per node) | High (8k – 25k concurrent requests per node) |
| **State Bleeding Risk** | Zero across requests unless using shared global state | **High**: Static properties survive request cycles | Low: Request context variables (`contextvars`) isolated |
| **Blocking I/O Vulnerability** | Low: Go runtime M:N scheduler switches OS threads | Low: Handled across worker process pool | **Critical**: Synchronous call blocks entire event loop |
| **Memory Fragmentation** | Negligible: Go GC tuned for concurrent heap tracing | Moderate: Long-running workers require recycling | Low: Controlled via generational garbage collection |

#### Architectural Analysis
- **Go** remains unmatched for raw concurrency and network throughput. The Go M:N scheduler multiplexes hundreds of thousands of goroutines over OS threads seamlessly. When burst traffic occurs, bounded worker pools like `panjf2000/ants` prevent unbounded heap growth and maintain sub-millisecond p99 latencies.
- **PHP** via FrankenPHP and Octane represents an astounding leap, eliminating the 30ms bootstrap overhead of traditional PHP-FPM. However, long-running in-memory workers invert PHP's traditional memory safety model: engineers must actively configure state-reset flush listeners to avoid multi-tenant session bleed and static registry leaks.
- **Python's** asynchronous ASGI model (`FastAPI` on `uvicorn`/`granian`) provides excellent concurrency for I/O-bound workloads. However, the single-threaded cooperative event loop introduces a fatal vulnerability: any unmanaged synchronous I/O or CPU-heavy operation immediately freezes the entire worker process for all concurrent clients.

---

### 4.3 Dimension 3: Persistence, Transactions & ORM Ergonomics

| Dimension Criteria | Go 1.25+ (GORM / sqlc / pgx) | PHP 8.3/8.4+ (Eloquent / Doctrine) | Python 3.13+ (SQLAlchemy 2.0 Async) |
| :--- | :--- | :--- | :--- |
| **Paradigm** | Data Mapper (sqlc) / Hybrid Active Record (GORM) | Active Record (Eloquent) / Data Mapper (Doctrine) | Data Mapper (SQLAlchemy 2.0 Async Unit of Work) |
| **Compile-Time Safety** | **100% (sqlc)** / Moderate (GORM struct tags) | Low (Runtime magic methods, improved by Larastan) | High (Mypy / Pyright typed DeclarativeBase) |
| **Transaction Propagation** | Explicit `context.Context` encapsulation (`InTx`) | Closures via `DB::transaction(fn)` / manual begin | Context managers: `async with uow:` / `session.begin()` |
| **N+1 Prevention Strategy** | Explicit `Preload()` or compile-time SQL joins | `Model::shouldBeStrict(!app()->isProduction())` | Explicit `selectinload()` / `joinedload()` |
| **Concurrency Locking** | Native `clause.Locking{Options: "SKIP LOCKED"}` | Native `$query->lockForUpdate()->skipLocked()` | Native `.with_for_update(skip_locked=True)` |
| **Performance Overhead** | Minimal (sqlc has zero reflection; GORM is fast) | Moderate (Eloquent hydrates rich model instances) | Moderate (SQLAlchemy maintains Identity Map in session) |
| **Schema Migration Tooling** | External (Goose, golang-migrate, Atlas) | **Native & Superior** (Laravel Migrations CLI) | External / Native standard (Alembic) |

#### Architectural Analysis
- **Go** offers a dual choice: `sqlc` delivers compile-time SQL verification and zero reflection, making it ideal for high-throughput OLTP; while `GORM` provides rapid enterprise development. Encapsulating transactions via the `InTx` interface passing `*gorm.DB` in `context.Context` guarantees absolute persistence isolation from business logic.
- **PHP's** Eloquent remains the most ergonomic and developer-friendly ORM in the industry. In Laravel 11/12, strict mode (`Model::shouldBeStrict()`) prevents accidental N+1 queries during test runs, and built-in support for `SKIP LOCKED` makes transactional outbox implementations remarkably clean.
- **Python's** SQLAlchemy 2.0 has completed its transition to explicit 2.0 syntax, deprecating legacy magic. Its Unit of Work pattern and Identity Map ensure atomic consistency across multi-entity mutations, while `selectinload` prevents the notorious `MissingGreenlet` async lazy-loading exception.

---

### 4.4 Dimension 4: Distributed Messaging & Workflow Orchestration

| Dimension Criteria | Go 1.25+ (Watermill & Temporal Go) | PHP 8.3/8.4+ (Laravel Queues & Spatie) | Python 3.13+ (Temporal Python & Arq) |
| :--- | :--- | :--- | :--- |
| **Event Routing Engine** | Universal Event Router (`ThreeDotsLabs/watermill`) | Artisan Queue Workers (Redis, SQS, DB) | Async Task Queues (`arq`) & Celery |
| **Durable Execution Model** | **Native Virtual State Machine (`temporalio/sdk-go`)**| Limited (Requires external orchestrators or state DB) | **Native Virtual State Machine (`temporalio/sdk-python`)** |
| **Long-Running Workflows** | Indestructible (Workflows sleep for months in RAM) | Fragile (Relies on queue polling and persistent DB flags) | Indestructible (Replay-based deterministic event log) |
| **Saga & Compensation** | Automated reverse compensation activity triggers | Manual event listeners or custom workflow tables | Automated reverse compensation activity triggers |
| **Cloud-Native Abstraction**| Dapr Go SDK (PubSub, State, Distributed Locks) | Dapr HTTP/gRPC SDK or custom integrations | Dapr Python SDK / Async IO gRPC |
| **Versioning Discipline** | `workflow.GetVersion()` / Determinism linting | Queue payload serialization versioning | `workflow.patched()` for non-breaking execution |

#### Architectural Analysis
- **Go** and **Python** are first-class citizens in the durable execution landscape via the **Temporal SDK**. Workflows in these languages act as fault-tolerant virtual state machines where state transitions are recorded into an append-only event log. If a host node crashes mid-execution, another worker replays history and resumes immediately.
- **PHP** excels at asynchronous background jobs via Laravel Queues (Horizon, Redis, SQS) and event sourcing via `spatie/laravel-event-sourcing`. However, for multi-day, human-in-the-loop, or multi-step saga workflows exceeding several minutes, PHP applications typically delegate orchestration to Temporal or external state machines.

---

### 4.5 Dimension 5: Resilience & Fault Tolerance

| Dimension Criteria | Go 1.25+ (Gobreaker & Time/Rate) | PHP 8.3/8.4+ (Saloon v3 & Cache Breakers) | Python 3.13+ (Tenacity & Redis Lua) |
| :--- | :--- | :--- | :--- |
| **Rate Limiter Topology** | In-memory token bucket (`golang.org/x/time/rate`) | Redis cache throttlers (`RateLimiter` facade) | Distributed atomic Redis token bucket via Lua script |
| **Circuit Breaker Engine** | High-performance in-memory state machine (`sony/gobreaker`) | Cache/Redis distributed state machine in Saloon | Thread-safe / async in-memory or Redis circuit breaker |
| **Retry Backoff Algorithm** | AWS Full Jitter: $\text{Uniform}(0, \min(\text{cap}, b \cdot 2^a))$ | Full Jitter via `rand()` + exponential sleep | Tenacity `wait_random_exponential` |
| **Idempotency Strategy** | In-memory sharded lock / Redis key middleware | DB unique constraints / Saloon Idempotency headers | FastAPI `IdempotencyMiddleware` with Redis locks |
| **Downstream Timeouts** | Context deadlines (`context.WithTimeout`) | Saloon `HasTimeout` plugin / Guzzle timeouts | HTTPX explicit timeouts (`timeout=5.0`) |
| **Failure Fast Behavior** | Instant error return when breaker is `OPEN` | Fast-fail exception before network dispatch | `CircuitBreakerOpenException` fast-fail |

#### Architectural Analysis
- All three ecosystems share identical mathematical resilience requirements: **AWS Full Jitter** must be used instead of uniform backoff to eliminate retry synchronization, and **Circuit Breakers** must guard downstream network integrations.
- **Go** implements these primitives with extreme efficiency: context deadlines propagate cancellations down the network stack automatically, and `gobreaker` incurs zero GC overhead.
- **PHP** achieves declarative elegance via Saloon v3, which embeds timeouts, circuit checking, and idempotency headers directly into reusable Connector classes.
- **Python** leverages Tenacity's battle-tested retry decorators and Redis Lua scripts to execute atomic token-bucket rate limiting without distributed race conditions.

---

### 4.6 Dimension 6: Telemetry, Observability & AI-Native Integration

| Dimension Criteria | Go 1.25+ (OpenTelemetry Go) | PHP 8.3/8.4+ (Laravel Pulse & OTel PHP) | Python 3.13+ (LiteLLM, Langfuse, Instructor, OTel) |
| :--- | :--- | :--- | :--- |
| **OTel SDK Performance** | Zero-alloc tracing pipelines, compiled OTel Go SDK | Ext-OTel C-extension or userland composer SDK | Native OpenTelemetry Python SDK with auto-instrumentation |
| **Application Telemetry** | Prometheus metrics, OpenTelemetry TracerProvider | Laravel Pulse real-time dashboard, Sentry, OpenTelemetry | Langfuse, OpenTelemetry GenAI Semantic Conventions |
| **AI Gateway & Routing** | Custom proxy / HTTP client wrappers | Saloon AI connectors / custom LLM clients | **LiteLLM Gateway** (Unified 100+ provider routing) |
| **Structured LLM Output** | JSON Schema unmarshaling with Protobuf stubs | Spatie Laravel Data mapping from JSON | **Instructor** (Pydantic v2 + self-correction retry) |
| **GenAI Trace Attributes** | Custom spans with `gen_ai.*` attributes | Custom spans with `gen_ai.*` attributes | **Native Langfuse `@observe` + OTel GenAI attributes** |
| **Cost Attribution & TPM** | External gateway / custom Redis meters | Redis token tracking | Native LiteLLM real-time USD budgeting & TPM quotas |

#### Architectural Analysis
- **Python** is the undisputed center of gravity for AI-Native backend engineering. The combination of **LiteLLM** (gateway proxy and failover), **Instructor** (Pydantic v2 structured output extraction with self-correcting retry loops), **Langfuse** (multi-agent tracing and prompt versioning), and **OpenTelemetry GenAI Semantic Conventions** forms a cohesive, production-grade AI stack.
- **Go** and **PHP** backends interface seamlessly with these AI architectures either by calling LiteLLM proxy gateways as downstream services or by consuming events emitted from Python-based AI workers. Both Go and PHP propagate OpenTelemetry `traceparent` W3C headers across service boundaries, ensuring end-to-end distributed trace visibility.


---

## 5. Production Failure Modes & Post-Mortem Autopsies ("Vibe-Slop" Traps)

In modern software development, code that "looks clean" and passes a superficial happy-path test often conceals catastrophic architectural flaws—colloquially termed **"Vibe-Slop" Engineering**. Under production load, these anti-patterns trigger cascading outages, data corruption, and security breaches.

This section presents real-world production incident autopsies across Go, PHP, and Python, dissecting their root causes, system impacts, and concrete remediation protocols.

---

### 5.1 Go Post-Mortems: Concurrency, Context, and Resource Leaks

#### Autopsy 1: Unmanaged Goroutine Spawning (Pod OOM Killer Exit Code 137)
- **The Vibe-Slop Pattern**: Spawning unmanaged background goroutines inside an HTTP handler to "improve API responsiveness":
```go
func (s *Handler) HandleWebhook(w http.ResponseWriter, r *http.Request) {
    go processWebhookAsync(r.Body) // 🚨 FATAL: Unbounded goroutine allocation!
    w.WriteHeader(http.StatusAccepted)
}
```
- **Root Cause & Autopsy**: Under a sustained burst of 50,000 requests per minute, if `processWebhookAsync` encounters downstream network latency (e.g. slow database writes or third-party rate limits), goroutines accumulate indefinitely. Each goroutine retains stack memory (2KB–8KB) and open heap pointers.
- **Production Impact**: Pod memory steadily escalates until the Linux kernel OOM-Killer kills the pod with `SIGKILL` (`Exit Code 137`). Kubernetes restarts the pod, but the restart triggers a thundering herd on neighboring replicas, causing a rolling cluster failure.
- **Remediation**: Banish bare `go func()`. Route asynchronous background tasks through a bounded pool (`panjf2000/ants/v2`) or coordinate concurrent sub-tasks via `errgroup.Group` with strict context cancellation and concurrency limits (`g.SetLimit(100)`).

#### Autopsy 2: Context Discarding & Database Connection Pool Starvation
- **The Vibe-Slop Pattern**: Replacing the incoming HTTP request context with `context.Background()` when calling downstream databases:
```go
func (r *Repo) FindUserData(ctx context.Context, id int64) (*User, error) {
    return r.db.WithContext(context.Background()).First(&user, id).Error // 🚨 FATAL!
}
```
- **Root Cause & Autopsy**: When an HTTP client cancels a request or experiences a timeout, the backend remains unaware. The database continues executing expensive 5-second queries to completion.
- **Production Impact**: The PostgreSQL connection pool reaches `MaxOpenConns` within minutes. Legitimate incoming requests block waiting for available database connections, causing cascading 504 Gateway Timeouts across the entire service fleet.
- **Remediation**: Always pass the incoming `ctx` downwards. If a background operation MUST outlive the client request (e.g. audit logging), explicitly use Go 1.21+ `context.WithoutCancel(ctx)` with an explicit secondary timeout (`context.WithTimeout`).

#### Autopsy 3: GORM Silent Error Suppression & Corrupt Zero-Value Mutations
- **The Vibe-Slop Pattern**: Ignoring `db.Error` return values when querying records:
```go
var user User
db.Where("id = ?", requestedID).First(&user) // db.Error ignored!
if user.Role == "ADMIN" {
	user.IsAdmin = true
	logger.Info("admin access granted to unauthenticated zero user")
}
```
- **Root Cause & Autopsy**: When no record matches, GORM returns `gorm.ErrRecordNotFound`. Suppressing this error leaves `user` initialized to zero-values (`ID = 0`, `Email = ""`). Subsequent business logic executes against an unauthenticated zero-user.
- **Production Impact**: Severe security bypasses (authorizing unauthenticated operations on user ID 0) or database corruption when zero-value structs are updated back to persistence.
- **Remediation**: Never ignore `db.Error`. Explicitly check for `errors.Is(err, gorm.ErrRecordNotFound)` and translate it into a domain-level `ErrNotFound`.

#### Autopsy 4: TCP Socket Leaks from Missing `defer rows.Close()`
- **The Vibe-Slop Pattern**:
```go
rows, err := db.QueryContext(ctx, "SELECT id, email FROM users")
if err != nil { return err }
// Missing defer rows.Close()!
for rows.Next() {
	var u User
	if err := rows.Scan(&u.ID, &u.Email); err != nil {
		return err
	}
	users = append(users, u)
}
```
- **Root Cause & Autopsy**: If the loop exits early due to an error, break statement, or return, the underlying TCP connection is never returned to the driver pool.
- **Production Impact**: File descriptors and connection pools are completely exhausted within hours under normal traffic.
- **Remediation**: Immediately follow every successful `db.QueryContext` with `defer rows.Close()`, and verify `rows.Err()` after iteration.

---

### 5.2 PHP Post-Mortems: In-Memory Workers, State Bleed, and Queue Retries

#### Autopsy 1: Multi-Tenant State Bleeding Across Octane/FrankenPHP Requests
- **The Vibe-Slop Pattern**: Registering tenant-specific context as a singleton in a Laravel Service Provider:
```php
// AppServiceProvider.php
$this->app->singleton(CurrentTenantContext::class, function () {
    return new CurrentTenantContext(request()->header('X-Tenant-ID'));
}); // 🚨 FATAL: Singleton survives across sequential HTTP requests in worker mode!
```
- **Root Cause & Autopsy**: In traditional PHP-FPM, memory is wiped at the end of every request. In FrankenPHP and Octane, the application stays booted in RAM. When Tenant A submits a request, `CurrentTenantContext` is instantiated. When Tenant B submits a subsequent request handled by the same worker thread, the container returns Tenant A's cached singleton!
- **Production Impact**: Cross-tenant data leakage: Tenant B views Tenant A's private financial records and customer data, violating GDPR and SOC2 compliance.
- **Remediation**: Never bind request-scoped or user-scoped state into container singletons. Configure flush listeners in `config/octane.php` under `'flush'` and call `App::forgetInstance()`. Use Pest `arch()` tests to forbid stateful singletons.

#### Autopsy 2: Unbounded Static Registry Memory Leaks (Worker OOM)
- **The Vibe-Slop Pattern**: Appending debugging metrics or spans to a static array:
```php
class TelemetryRegistry {
    public static array $spans = []; // 🚨 FATAL: Accumulates in RAM across thousands of requests!
}
```
- **Root Cause & Autopsy**: In worker mode, static class properties persist across the entire lifespan of the process. Appending data without bounds causes steady memory growth (100MB → 500MB → 2GB).
- **Production Impact**: The worker process crashes abruptly when reaching the container memory ceiling, terminating in-flight requests with HTTP 502 Bad Gateway.
- **Remediation**: Set `--max-requests=1000` on worker instances to automatically recycle processes. Eliminate unbound static arrays; use scoped services with deterministic resets.

#### Autopsy 3: Duplicate Billing from Non-Idempotent Queue Retries
- **The Vibe-Slop Pattern**: Retrying an external payment job without an idempotency key:
```php
class ProcessPaymentJob implements ShouldQueue {
    public int $tries = 3;
    public function handle(PaymentGateway $gateway): void {
        $gateway->charge($this->order->total_cents); // 🚨 FATAL: Duplicate charges on retry!
    }
}
```
- **Root Cause & Autopsy**: The payment gateway successfully charges the customer's credit card, but the HTTP response times out after 10 seconds. The queue worker marks the job failed and retries it, triggering a second charge.
- **Production Impact**: Widespread double-billing, customer disputes, bank chargeback fees, and payment gateway account suspension.
- **Remediation**: Generate a deterministic UUID v4 `idempotency_key` stored on the `Order` entity *before* dispatching the job, and send it in the `Idempotency-Key` HTTP header. The gateway recognizes the duplicate key and returns the original transaction status.

---

### 5.3 Python Post-Mortems: Event Loop Blocking, Async Detachment, and Task GC

#### Autopsy 1: Event Loop Starvation via Synchronous I/O in `async def`
- **The Vibe-Slop Pattern**: Invoking synchronous blocking libraries inside FastAPI async route handlers:
```python
@app.post("/api/v1/process")
async def handle_process(payload: ProcessRequest):
    response = requests.post("https://legacy-crm.internal/api", json=payload.dict()) # 🚨 FATAL!
    time.sleep(1.0) # Synchronous sleep freezes event loop!
    return response.json()
```
- **Root Cause & Autopsy**: Python's `asyncio` runs on a single OS thread using cooperative multitasking. When `requests.post()` or `time.sleep()` executes, the OS thread blocks. No other concurrent coroutine can yield or run.
- **Production Impact**: Under 50 concurrent requests, p99 latency spikes from 30ms to 45 seconds. Kubernetes liveness probes fail, triggering pod restarts and catastrophic cascading downtime.
- **Remediation**: Never perform synchronous I/O in `async def`. Use `httpx.AsyncClient` and `asyncio.sleep()`. If synchronous code cannot be avoided, offload it to a worker thread: `await anyio.to_thread.run_sync(blocking_call, arg)`.

#### Autopsy 2: SQLAlchemy Async `MissingGreenlet` Exception
- **The Vibe-Slop Pattern**: Accessing unloaded relationships on an ORM entity outside the active session or after commit:
```python
async def get_order(order_id: UUID) -> OrderDTO:
    async with sessionmaker() as session:
        stmt = select(OrderORM).where(OrderORM.id == order_id)
        order = (await session.execute(stmt)).scalar_one()
    return OrderDTO(id=order.id, items=[i.name for i in order.items]) # 🚨 FATAL!
```
- **Root Cause & Autopsy**: In async SQLAlchemy, implicit I/O is disabled because attribute access cannot be awaited. Accessing `order.items` after the session closes raises `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called`.
- **Production Impact**: 100% failure rate for all endpoints touching relational models; crashes only appear during integration or production traffic.
- **Remediation**: Enforce explicit eager loading via `options(selectinload(OrderORM.items))`. In the Repository layer, map ORM models to pure domain dataclasses before returning them to Use Cases.

#### Autopsy 3: The `asyncio.create_task()` Garbage Collection Silent Drop
- **The Vibe-Slop Pattern**: Spawning fire-and-forget background tasks without retaining a strong reference:
```python
@app.post("/api/v1/orders")
async def create_order(req: OrderCreate):
    order = await save_order(req)
    asyncio.create_task(send_confirmation_email(order.id)) # 🚨 FATAL: Silent loss!
    return order
```
- **Root Cause & Autopsy**: Python's garbage collector destroys coroutines created by `asyncio.create_task()` if no strong in-memory reference to the `Task` object is retained. When GC runs, the task is finalized and silently destroyed mid-execution without raising errors.
- **Production Impact**: Critical emails, audit logs, and analytics events randomly disappear in production without a trace.
- **Remediation**: Maintain a global strong-reference set (`background_tasks.add(task)` with `task.add_done_callback(background_tasks.discard)`), or delegate to a durable task queue (**Arq** or **Temporal**).

---

### 5.4 Cross-Ecosystem Anti-Vibe-Slop Verification Checklist

| Vulnerability Category | Go Verification Check | PHP Verification Check | Python Verification Check |
| :--- | :--- | :--- | :--- |
| **Concurrency & Workers** | Run `go test -race ./...`; verify zero unmanaged `go func()` | Verify `MAX_REQUESTS` in FrankenPHP; run 10k load test checking memory stability | Audit AST for blocking calls in `async def`; enable `PYTHONASYNCIODEBUG=1` |
| **Layer Boundaries** | Confirm `internal/biz` has zero database/SQL imports | Run Pest `arch()` test verifying controllers do not access Eloquent models | Verify Use Cases take abstract `Protocol` interfaces without importing FastAPI |
| **Transaction Integrity** | Verify all multi-write operations run via `tx.InTx` | Verify domain writes execute inside `DB::transaction()` closures | Verify domain writes execute inside `async with uow:` context manager |
| **Event Consistency** | Verify outbox table uses `SELECT ... FOR UPDATE SKIP LOCKED` | Verify outbox worker command calls `$query->lockForUpdate()->skipLocked()` | Verify outbox polling worker executes `.with_for_update(skip_locked=True)` |
| **Error Exposure** | Verify custom HTTP error encoder outputs RFC 9457 without DB strings | Confirm `withExceptions()` in `bootstrap/app.php` masks `QueryException` | Verify global FastAPI exception handler intercepts raw `Exception` and logs trace ID |
| **AI Output Parsing** | Ban regex on JSON outputs; enforce Protobuf/JSON schema validation | Enforce Spatie Data DTO validation on LLM JSON payloads | Ban regex parsing on LLM strings; enforce `instructor` with Pydantic v2 schemas |


---

## 6. Actionable Skills Taxonomy for `agent-skills`

To operationalize the findings of this research within the `agent-skills` engineering pack, this section specifies **11 new modular skills** adhering strictly to the standardized `SKILL.md` format, followed by concrete upgrade recommendations for `core/roles/backend-developer.md`.

---

### 6.1 Overview of Proposed Modular Backend Skills

```
core/skills/backend/
├── implement-kratos-service/          # [Go] Kratos Clean Architecture + Wire DI
├── implement-transactional-outbox-go/ # [Go] GORM + SKIP LOCKED Outbox Relay
├── implement-resilient-client-go/     # [Go] Gobreaker + Token Bucket + Full Jitter
├── optimize-go-concurrency/           # [Go] Ants worker pool + Sonic zero-alloc
├── implement-laravel-ddd-action/      # [PHP] Laravel 11/12+ DDD + Spatie Data
├── implement-transactional-outbox-php/# [PHP] Eloquent Outbox + SKIP LOCKED Daemon
├── configure-frankenphp-octane/       # [PHP] Caddy Worker Mode + State Bleed Reset
├── implement-saloon-client/           # [PHP] Saloon v3 Connector + Circuit Breaker
├── python-async-clean-architecture/   # [Python] FastAPI + Dishka IoC + SQLAlchemy UoW
├── python-temporal-workflow/          # [Python] Temporal SDK Durable Workflow
└── python-ai-native-service/          # [Python] LiteLLM + Instructor + Langfuse OTel
```

---

### 6.2 Go Ecosystem Modular Skills

#### 1. Skill Specification: `implement-kratos-service`
```markdown
---
name: implement-kratos-service
description: Implement or evolve a Go microservice endpoint using the Kratos v2.9.1 Clean Architecture layout (api, service, biz, data) with compile-time Wire dependency injection and strict Biz layer isolation.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Kratos Service

Use this skill to implement microservice endpoints in Go adhering to Kratos Clean Architecture principles.

## Inputs Schema
- `service_name` (string, required): Name of the microservice.
- `proto_contract_path` (string, required): Path to the `api/v1/*.proto` file.
- `usecase_name` (string, required): Business use case name in `internal/biz`.
- `persistence_backend` (enum: `["gorm", "sqlc", "pgx"]`, default: `"gorm"`).

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Generated stubs: `api/v1/*_grpc.pb.go`, `api/v1/*.pb.go`
- Domain use case: `internal/biz/<domain>.go`
- Repository adapter: `internal/data/<domain>.go`
- Inbound service adapter: `internal/service/<domain>.go`
- Wire injector: `cmd/server/wire_gen.go`

## Definition of Done (DoD)
- [ ] Protobuf contract updated and stubs generated via `kratos proto client api/...`.
- [ ] Domain entity and repository interface defined in `internal/biz` with zero database driver imports.
- [ ] Repository implemented in `internal/data` implementing Biz port interface.
- [ ] Inbound handler implemented in `internal/service` mapping domain errors to Kratos Status/HTTP codes.
- [ ] Dependencies registered in `ProviderSet` and compiled successfully via `wire gen ./...`.
- [ ] Table-driven unit tests pass with 100% path coverage.
```

#### 2. Skill Specification: `implement-transactional-outbox-go`
```markdown
---
name: implement-transactional-outbox-go
description: Implement atomic transactional outbox persistence and a background relay forwarder using GORM and PostgreSQL (with SELECT FOR UPDATE SKIP LOCKED) to achieve zero-loss distributed event delivery.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Transactional Outbox (Go)

Use this skill to implement the Transactional Outbox pattern for reliable, at-least-once distributed messaging in Go services.

## Inputs Schema
- `aggregate_type` (string, required): Domain aggregate name (e.g. `"order"`).
- `event_types` (array of strings, required): List of event types emitted.
- `batch_size` (integer, default: 50): Number of records fetched per polling cycle.
- `max_retries` (integer, default: 5): Maximum retry threshold before marking `FAILED`.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- GORM outbox model: `internal/data/models/outbox.go`
- Atomic InTx writer: `internal/biz/` & `internal/data/`
- Outbox relay worker: `internal/data/outbox_relay.go`

## Definition of Done (DoD)
- [ ] `outbox_records` schema created with composite index on `(status, created_at)`.
- [ ] Domain use case creates domain entity and outbox message in a single atomic `InTx` transaction.
- [ ] Relay worker query uses `clause.Locking{Strength: "UPDATE", Options: "SKIP LOCKED"}`.
- [ ] Exponential backoff and maximum retry threshold implemented to prevent poison loops.
- [ ] Integration test verifies message is written and marked `PUBLISHED` upon broker acknowledgment.
```

#### 3. Skill Specification: `implement-resilient-client-go`
```markdown
---
name: implement-resilient-client-go
description: Wrap external HTTP/gRPC downstream service clients with token-bucket rate limiting (x/time/rate), circuit breaking (sony/gobreaker), and exponential backoff retries with full jitter.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Resilient Client (Go)

Use this skill to harden service-to-service communications against cascading network failures in Go.

## Inputs Schema
- `client_name` (string, required): Downstream client identifier.
- `qps_limit` (integer, required): Token bucket queries per second.
- `burst_limit` (integer, required): Maximum token bucket burst capacity.
- `circuit_breaker_settings` (object, required): Failure ratio and recovery timeout.
- `max_retries` (integer, default: 3): Maximum retry attempts.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Resilient client wrapper: `internal/data/clients/<client>_resilient.go`
- Unit tests with mock server: `internal/data/clients/<client>_resilient_test.go`

## Definition of Done (DoD)
- [ ] Client wrapped with `rate.NewLimiter` and `gobreaker.NewCircuitBreaker`.
- [ ] Exponential backoff with AWS full jitter implemented (`FullJitterSleep`).
- [ ] 5xx errors trip circuit breaker; 4xx client errors pass through without tripping.
- [ ] Context cancellation and timeout deadlines strictly respected.
```

#### 4. Skill Specification: `optimize-go-concurrency`
```markdown
---
name: optimize-go-concurrency
description: Audit and optimize high-concurrency Go code by replacing unmanaged goroutines with bounded worker pools (ants) or errgroup, eliminating data races, and enforcing zero-allocation serialization.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Optimize Go Concurrency

Use this skill to eliminate goroutine leaks, data races, and memory thrashing in high-throughput Go services.

## Inputs Schema
- `target_package` (string, required): Path to package requiring concurrency audit.
- `max_workers` (integer, default: 1000): Capacity for bounded worker pool.
- `enable_simd_serialization` (boolean, default: true): Whether to integrate `bytedance/sonic`.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Worker pool manager: `internal/pkg/workerpool/pool.go`
- Benchmark report: `benchmark_results.txt`

## Definition of Done (DoD)
- [ ] Zero unmanaged `go func()` in request execution paths.
- [ ] All shared in-memory state guarded by `sync.Mutex`, `sync.RWMutex`, or `sync.Map`.
- [ ] `go test -race ./...` executes with zero data race warnings.
- [ ] Memory allocation benchmarks confirm reduced heap allocation overhead.
```

---

### 6.3 PHP Ecosystem Modular Skills

#### 5. Skill Specification: `implement-laravel-ddd-action`
```markdown
---
name: implement-laravel-ddd-action
description: Implement an enterprise-grade Domain Action adhering to Clean Architecture and DDD in Laravel 11/12+ using Spatie Laravel Data DTOs, custom repositories, Form Requests, and Pest unit/feature tests.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Laravel DDD Action

Use this skill to implement single-responsibility command actions in Laravel following DDD principles.

## Inputs Schema
- `domain_name` (string, required): Bounded context domain name.
- `action_name` (string, required): Name of the action class.
- `input_schema` (object, required): Attributes and validation rules.
- `output_schema` (object, required): Return entity attributes.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Strongly typed DTO: `app/Domain/<Domain>/Data/<Action>Data.php`
- Invokable Action: `app/Domain/<Domain>/Actions/<Action>Action.php`
- Repository Interface: `app/Domain/<Domain>/Repositories/<Domain>RepositoryInterface.php`
- Pest Test: `tests/Feature/Domain/<Domain>/<Action>Test.php`

## Definition of Done (DoD)
- [ ] Action implemented with invokable `__invoke()` signature.
- [ ] Input parameters strictly validated via Spatie Data DTO.
- [ ] Database mutations executed inside atomic `DB::transaction()`.
- [ ] Pest `arch()` test confirms no Eloquent leakage into presentation layer.
- [ ] 100% test pass under Pest testing framework.
```

#### 6. Skill Specification: `implement-transactional-outbox-php`
```markdown
---
name: implement-transactional-outbox-php
description: Implement an atomic Transactional Outbox pattern in Laravel with PostgreSQL FOR UPDATE SKIP LOCKED for lockless concurrent event publishing to Kafka/RabbitMQ/Dapr.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Transactional Outbox (PHP)

Use this skill to implement reliable transactional outbox event publishing in Laravel applications.

## Inputs Schema
- `event_types` (array of strings, required): Event names emitted.
- `batch_size` (integer, default: 100): Batch size per polling command.
- `max_retries` (integer, default: 5): Maximum retry threshold.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Database migration: `database/migrations/*_create_outbox_messages_table.php`
- Eloquent model: `app/Infrastructure/Outbox/Models/OutboxMessage.php`
- Artisan daemon command: `app/Console/Commands/ProcessOutboxMessagesCommand.php`

## Definition of Done (DoD)
- [ ] Outbox message recorded atomically with domain entity in single `DB::transaction()`.
- [ ] Polling query utilizes `$query->lockForUpdate()->skipLocked()`.
- [ ] Failed dispatches retry with exponential backoff and random jitter.
- [ ] Zero race conditions under concurrent worker executions.
```

#### 7. Skill Specification: `configure-frankenphp-octane`
```markdown
---
name: configure-frankenphp-octane
description: Configure, benchmark, and harden high-concurrency Laravel Octane and FrankenPHP worker runtimes with Caddy, state-bleed auditing, and memory leak prevention.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Configure FrankenPHP & Octane

Use this skill to configure and harden in-memory PHP worker runtimes.

## Inputs Schema
- `worker_count` (integer, default: 4): Number of worker threads.
- `max_requests_limit` (integer, default: 1000): Maximum requests before worker recycle.
- `enable_early_hints` (boolean, default: true): Enable RFC 8297 Early Hints.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Caddyfile configuration: `Caddyfile`
- Worker script: `public/frankenphp-worker.php`
- Octane config: `config/octane.php`

## Definition of Done (DoD)
- [ ] Zero state bleed between sequential requests (verified via multi-user session audit).
- [ ] Worker recycling configured at 1,000 requests to eliminate memory fragmentation.
- [ ] 103 Early Hints validated in HTTP response headers.
- [ ] Memory footprint remains stable under sustained 10,000-request load test.
```

#### 8. Skill Specification: `implement-saloon-client`
```markdown
---
name: implement-saloon-client
description: Create a resilient, production-ready third-party API integration using Saloon v3 with circuit breaker middleware, exponential backoff, rate limiting, and MockClient fixtures.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Saloon Client

Use this skill to implement resilient third-party API connectors in PHP.

## Inputs Schema
- `api_name` (string, required): Identifier of downstream service.
- `base_url` (string, required): Downstream endpoint base URL.
- `timeout_seconds` (integer, default: 10): Maximum request timeout.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Saloon Connector: `app/Infrastructure/<Api>/<Api>Connector.php`
- Saloon Request: `app/Infrastructure/<Api>/Requests/<Action>Request.php`
- MockClient test: `tests/Unit/<Api>ConnectorTest.php`

## Definition of Done (DoD)
- [ ] Connector implements `AlwaysThrowOnErrors` and `HasTimeout` plugins.
- [ ] Circuit breaker trips after repeated 5xx errors; 4xx client errors do not trip breaker.
- [ ] Retries include exponential backoff with full jitter.
- [ ] MockClient test suite covers 100% of execution paths without external network egress.
```

---

### 6.4 Python Ecosystem Modular Skills

#### 9. Skill Specification: `python-async-clean-architecture`
```markdown
---
name: python-async-clean-architecture
description: Scaffold, implement, or refactor modern Python async backend services adhering to Clean Architecture principles using FastAPI or Litestar, Dishka scoped dependency injection, and SQLAlchemy 2.0 Async Session with Unit of Work and Repository patterns.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Python Async Clean Architecture

Use this skill to implement Clean Architecture services in Python with scoped IoC dependency injection.

## Inputs Schema
- `domain_name` (string, required): Bounded context domain name.
- `use_case_name` (string, required): Business use case identifier.
- `framework` (enum: `["fastapi", "litestar"]`, default: `"fastapi"`).

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Domain Entity: `app/domain/<domain>/models.py`
- Protocol Interfaces: `app/domain/<domain>/interfaces.py`
- Application Use Case: `app/application/<domain>/use_cases.py`
- SQLAlchemy UoW & Repo: `app/infrastructure/persistence/<domain>_repo.py`
- Dishka Provider: `app/infrastructure/di/providers.py`

## Definition of Done (DoD)
- [ ] Domain entities defined as pure dataclasses/Pydantic models with zero framework imports.
- [ ] Repositories and Unit of Work declared as abstract `Protocol` classes in domain layer.
- [ ] SQLAlchemy 2.0 async implementations use `selectinload` for relational traversal.
- [ ] Dishka IoC configured with explicit `Scope.APP` and `Scope.REQUEST`.
- [ ] Unit tests for Use Cases achieve 100% path coverage with mocked UoW in air-gapped test sandbox.
```

#### 10. Skill Specification: `python-temporal-workflow`
```markdown
---
name: python-temporal-workflow
description: Author, test, and version durable distributed workflows and activities using the Temporal Python SDK. Enforces strict workflow determinism, exponential retry policies, signal/query handlers, and non-breaking versioning with workflow.patched().
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, execute_command]
---

# Python Temporal Workflow

Use this skill to implement indestructible, long-running distributed workflows in Python.

## Inputs Schema
- `workflow_name` (string, required): Workflow class identifier.
- `activities` (array of strings, required): List of activities invoked.
- `timeout_duration` (string, required): ISO-8601 or seconds duration.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- Workflow definition: `app/workflows/<name>_workflow.py`
- Activity definitions: `app/workflows/activities/<name>_activities.py`
- Temporal worker runner: `app/workers/temporal_worker.py`

## Definition of Done (DoD)
- [ ] Workflow code adheres 100% to Temporal determinism invariants (no direct I/O, no unmanaged system clocks).
- [ ] Side effects strictly encapsulated in `@activity.defn` functions with explicit timeouts and `RetryPolicy`.
- [ ] Breaking changes guarded by `workflow.patched()`.
- [ ] Temporal test suite passes using `WorkflowEnvironment.start_time_skipping()`.
```

#### 11. Skill Specification: `python-ai-native-service`
```markdown
---
name: python-ai-native-service
description: Build resilient, observable AI-native backend services integrating LiteLLM proxy routing, Langfuse prompt management and tracing, Instructor structured output validation, and OpenTelemetry GenAI semantic conventions.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, execute_command]
---

# Python AI-Native Service

Use this skill to author production-grade, observable AI-native backend services.

## Inputs Schema
- `service_name` (string, required): Name of AI service component.
- `pydantic_schema` (object, required): Expected structured output model definition.
- `litellm_proxy_url` (string, required): Gateway proxy URL.

## Outputs Schema
- `contracts/schemas/implementation-result.json`
- AI Service Class: `app/services/ai/<service>.py`
- Pydantic Response Model: `app/domain/ai/schemas.py`
- OTel Instrumentation: `app/infrastructure/telemetry/genai_spans.py`

## Definition of Done (DoD)
- [ ] Inferences routed through LiteLLM proxy gateway with automatic model failover.
- [ ] Response schemas extracted via Instructor with Pydantic v2 and `max_retries >= 3` (zero regex parsing).
- [ ] Invocations traced via Langfuse `@observe` and OpenTelemetry GenAI Semantic Convention spans (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.*`).
- [ ] Prompt injection boundaries strictly enforced: user content structurally separated from system instructions.
```

---

### 6.5 Concrete Enhancement Roadmap for `core/roles/backend-developer.md`

To modernize `core/roles/backend-developer.md` from its generic baseline to an authoritative, master-level engineering standard, the following four enhancements must be integrated:

#### 1. Language-Specific Architecture Standards
Add dedicated clauses under `## Principal Expectations`:
- **Go Clean Architecture Standard**: Enforce **Go 1.25+**, **Kratos v2.9.1**, **Wire compile-time DI**, **PostgreSQL with pgx/GORM**, and **Dapr for pub/sub/state**. Prohibit database imports in `internal/biz`.
- **PHP Worker-Mode Standard**: For high-throughput PHP services, mandate **PHP 8.4+**, **Laravel 11/12+ DDD**, and **FrankenPHP/Octane worker mode**. Mandate container flush listeners to prevent multi-tenant state bleed.
- **Python Async IoC Standard**: Enforce **Python 3.13+**, **FastAPI/Litestar**, **Dishka scoped IoC**, and **SQLAlchemy 2.0 Async Unit of Work**. Prohibit leaking web framework `Depends` into business use cases.

#### 2. Skill Toolbox Expansion
Expand the `### Primary Skills` toolbox in `core/roles/backend-developer.md`:
```markdown
### Primary Skills (Updated 2026/2027 Standards)
- `add-api-endpoint`
- `add-event-handler`
- `add-service-client`
- `create-migration`
- `write-tests`
- `commit-code`
- `scaffold-new-service`
- `navigate-service`
- `build-mcp-server`
- `implement-structured-outputs`
- `implement-kratos-service`              # NEW: Go Kratos Clean Architecture
- `implement-transactional-outbox-go`      # NEW: Go Transactional Outbox
- `implement-resilient-client-go`          # NEW: Go Resilience & Full Jitter
- `optimize-go-concurrency`                # NEW: Go Concurrency & Ants Pools
- `implement-laravel-ddd-action`           # NEW: PHP Laravel 11/12 DDD
- `implement-transactional-outbox-php`     # NEW: PHP Eloquent Outbox
- `configure-frankenphp-octane`            # NEW: PHP FrankenPHP Worker Mode
- `implement-saloon-client`                # NEW: PHP Saloon v3 Resilient API
- `python-async-clean-architecture`        # NEW: Python FastAPI + Dishka
- `python-temporal-workflow`               # NEW: Python Temporal Durable Workflows
- `python-ai-native-service`               # NEW: Python LiteLLM + Instructor + OTel
```

#### 3. New Mandatory Guardrail Locks
Add to `## Guardrails`:
- **ANTI-VIBE-SLOP LOCK (EXPANDED)**: Reject implementations that return dummy success responses, ignore database errors, spawn unmanaged background goroutines, or perform regex parsing on LLM strings.
- **TRANSACTIONAL-OUTBOX LOCK**: Dual-writes across a database and an external message broker must use the Transactional Outbox pattern with `SELECT ... FOR UPDATE SKIP LOCKED`.
- **ASYNC-EVENT-LOOP LOCK**: Forbids synchronous blocking calls (`requests`, `time.sleep`, synchronous DB drivers) inside Python `async def` routes.
- **WORKER-STATE-ISOLATION LOCK**: Forbids binding request-scoped or user-scoped data into application singletons in PHP worker runtimes (FrankenPHP/Octane).
- **DURABLE-WORKFLOW LOCK**: Multi-step business processes or agent executions exceeding 30 seconds must use Temporal SDK deterministic state machines.

#### 4. Automated Architecture Governance Mandates
- In Go: Enforce `go test -race ./...` as a mandatory pre-merge gate.
- In PHP: Enforce Pest `arch()` tests verifying that HTTP controllers do not call database models directly and that no debugging remnants (`dd`, `dump`) exist in code.
- In Python: Enforce AST linting verifying zero synchronous I/O in async route handlers and zero regex parsing on LLM response payloads.


---

## 7. Mermaid Architecture & Lifecycle Diagrams

This section provides visual architectural models illustrating layer boundaries, the outbox lifecycle, the circuit breaker finite state machine, and AI-native observability topologies.

---

### 7.1 Clean Architecture Hexagonal Topology Across Languages

The following diagram illustrates how the three language ecosystems map onto Clean Architecture's concentric layer boundaries, preserving the Dependency Inversion Principle (DIP):

```mermaid
graph TD
    subgraph External["External Actors & Infrastructure"]
        Client([HTTP / gRPC Client])
        DB[(PostgreSQL Database)]
        Broker([Kafka / RabbitMQ / Dapr])
        LLM([LLM Gateway / OpenAI])
    end

    subgraph Presentation["Presentation Layer (Transport Adapters)"]
        GoProto["Go: internal/service (Protobuf stubs, gRPC/HTTP handlers)"]
        PHPController["PHP: app/Http/Controllers (Form Requests, Route definitions)"]
        PyRouter["Python: app/presentation (FastAPI APIRouter / Litestar)"]
    end

    subgraph Application["Application Layer (Use Cases & Orchestrators)"]
        GoUsecase["Go: internal/biz (UserUsecase, AccountUsecase)"]
        PHPAction["PHP: app/Domain/*/Actions (CreateOrderAction, Invokable)"]
        PyUseCase["Python: app/application (CancelOrderUseCase)"]
    end

    subgraph Domain["Domain Layer (Pure Invariants & Ports)"]
        GoDomain["Go: internal/biz (User entity, UserRepo port, Transaction port)"]
        PHPDTO["PHP: app/Domain/*/Data (Spatie DTOs, Repository Interfaces)"]
        PyDomain["Python: app/domain (Dataclasses, Protocol Interfaces)"]
    end

    subgraph Infrastructure["Infrastructure Layer (Persistence & Integration Adapters)"]
        GoData["Go: internal/data (GORM / sqlc repo, DB connection pool)"]
        PHPEloquent["PHP: app/Infrastructure (Eloquent repo, OutboxPublisher)"]
        PyUoW["Python: app/infrastructure (SQLAlchemy 2.0 Async UoW)"]
    end

    %% Inbound Request Flow
    Client -->|HTTP / gRPC| Presentation
    Presentation -->|Dispatches DTOs| Application
    Application -->|Coordinates| Domain
    
    %% Outbound Dependency Inversion (Ports & Adapters)
    Application -->|Depends on Port| Domain
    Infrastructure -.->|Implements Port (DIP)| Domain
    Infrastructure -->|Executes Queries| DB
    Infrastructure -->|Publishes Events| Broker
    Infrastructure -->|Inference Calls| LLM
```

---

### 7.2 The Transactional Outbox Pattern & SKIP LOCKED Relay Lifecycle

The sequence below illustrates atomic dual-write persistence and non-blocking background event dispatch using PostgreSQL `SELECT ... FOR UPDATE SKIP LOCKED`:

```mermaid
sequenceDiagram
    autonumber
    actor Client as HTTP Client
    participant App as API Service Handler
    participant DB as PostgreSQL (ACID Boundary)
    participant Relay as Outbox Daemon Worker (Replica 1..N)
    participant Broker as Message Broker (Kafka / Dapr)

    Note over Client, DB: Step 1: Atomic InTx Local Dual-Write
    Client->>App: POST /api/v1/orders (Create Order)
    activate App
    App->>DB: BEGIN TRANSACTION
    App->>DB: INSERT INTO orders (id, user_id, amount, status='PENDING')
    App->>DB: INSERT INTO outbox_records (id, event_type, payload, status='PENDING')
    App->>DB: COMMIT TRANSACTION
    App-->>Client: 201 Created (Order confirmed atomically)
    deactivate App

    Note over Relay, Broker: Step 2: Asynchronous Non-Blocking Relay Dispatch
    loop Every Polling Interval (e.g. 500ms)
        Relay->>DB: BEGIN TRANSACTION
        Relay->>DB: SELECT * FROM outbox_records WHERE status='PENDING'<br/>ORDER BY created_at ASC LIMIT 50<br/>FOR UPDATE SKIP LOCKED
        Note right of DB: Rows locked exclusively for this worker.<br/>Other worker replicas SKIP these rows!
        DB-->>Relay: Return 50 Locked Outbox Records
        
        alt Broker Dispatch Succeeded
            Relay->>Broker: Publish(topic, key, payload)
            Broker-->>Relay: ACK (Delivered)
            Relay->>DB: UPDATE outbox_records SET status='PUBLISHED', processed_at=NOW() WHERE id IN (...)
            Relay->>DB: COMMIT TRANSACTION
        else Broker Dispatch Failed (Network Timeout)
            Relay->>DB: UPDATE outbox_records SET retry_count = retry_count + 1,<br/>scheduled_at = NOW() + BackoffWithJitter()<br/>WHERE id = ...
            Relay->>DB: COMMIT TRANSACTION
            Note over Relay: Record will be re-attempted after backoff.<br/>Transitions to 'FAILED' after 5 retries.
        end
    end
```

---

### 7.3 Circuit Breaker Finite State Machine with Half-Open Recovery

The following state machine details how failure counters, recovery timeouts, and probe requests govern circuit state transitions:

```mermaid
stateDiagram-v2
    [*] --> CLOSED : Service Boot

    state CLOSED {
        [*] --> NormalOperation
        NormalOperation --> Success : Execute Request
        Success --> NormalOperation : Reset Failure Counter
        NormalOperation --> Failure : 5xx / Timeout Error
        Failure --> EvaluateThreshold : Increment Failure Counter
        EvaluateThreshold --> NormalOperation : Failures < Threshold (e.g. 5)
    }

    CLOSED --> OPEN : Failure Threshold Exceeded\n(e.g. 5 consecutive 5xx or >50% error rate)

    state OPEN {
        [*] --> FastFail
        FastFail --> FastFail : Incoming Requests Rejected\nImmediately (CircuitBreakerOpenException)
    }

    OPEN --> HALF_OPEN : Cooldown Timeout Expires\n(e.g. after 30 seconds)

    state HALF_OPEN {
        [*] --> AllowProbeRequest
        AllowProbeRequest --> ProbeExecuting : Allow Single Request Through
    }

    HALF_OPEN --> CLOSED : Probe Request Succeeds\n(Reset All Error Counters)
    HALF_OPEN --> OPEN : Probe Request Fails\n(Re-trip Breaker for another 30s)
```

---

### 7.4 AI-Native Agentic Observability & Distributed Tracing Topology

The following diagram illustrates the lifecycle of a request through an AI-Native backend, showcasing how LiteLLM, Instructor, Langfuse, and OpenTelemetry correlate execution traces:

```mermaid
graph LR
    subgraph ClientLayer["Client & Ingress Layer"]
        User([End User / Client App])
        Gateway[FastAPI / ASGI Gateway]
    end

    subgraph ServiceLayer["Application & IoC Service Layer"]
        Dishka[Dishka Scoped IoC]
        AIService[FinancialAnalysisAIService]
        InstructorEngine[Instructor + Pydantic v2 Engine]
    end

    subgraph GatewayLayer["AI Gateway & Fallback Layer"]
        LiteLLMProxy[LiteLLM Gateway Proxy]
    end

    subgraph ModelProviders["Upstream LLM Providers"]
        OpenAI[Primary: OpenAI GPT-4o]
        Anthropic[Fallback: Claude 3.5 Sonnet]
    end

    subgraph TelemetryCluster["Observability & Governance"]
        Langfuse[(Langfuse Platform<br/>Prompt Versions & Generations)]
        OTelCollector[(OpenTelemetry Collector<br/>GenAI Semantic Convention Spans)]
    end

    User -->|1. HTTP Request with Traceparent| Gateway
    Gateway -->|2. Injects Dependencies| Dishka
    Dishka -->|3. Resolves Service| AIService
    
    AIService -->|4. @observe decorator| Langfuse
    AIService -->|5. gen_ai.* spans| OTelCollector
    
    AIService -->|6. chat.completions.create| InstructorEngine
    InstructorEngine -->|7. Tool-call JSON Schema| LiteLLMProxy
    
    LiteLLMProxy -->|8a. Primary Route| OpenAI
    LiteLLMProxy -.->|8b. Failover on 429/503| Anthropic
    
    OpenAI -->|9. Returns Tool Arguments| InstructorEngine
    
    InstructorEngine -->|10. Strict Pydantic Validation| InstructorEngine
    Note over InstructorEngine: If validation fails, Instructor<br/>re-prompts LLM with error trace<br/>(Self-Correction Loop)
    
    InstructorEngine -->|11. Validated DTO| AIService
    AIService -->|12. Records Final Tokens & Cost| OTelCollector
    AIService -->|13. Typed Response| Gateway
    Gateway -->|14. RFC 9457 / JSON Response| User
```

---

### 7.5 Architectural Summary & Engineering Synthesis

Modern backend engineering across Go, PHP, and Python has reached an unprecedented level of **architectural convergence**. Regardless of the runtime language:
- Clean Architecture isolates business domain models from volatile infrastructure adapters.
- Atomic InTx persistence combined with the Transactional Outbox pattern eliminates distributed dual-write inconsistencies.
- Mathematical resilience (AWS Full Jitter and Circuit Breakers) shields services from cascading network degradation.
- RFC 9457 Problem Details envelopes enforce deterministic error communication without leaking internal database secrets.
- AI-Native systems treat LLM invocations as untrusted, stochastic downstream APIs, enforcing schema validation via Instructor and deep observability via OpenTelemetry GenAI standards.

By integrating the **11 modular skill definitions** and adopting the proposed **`backend-developer` role upgrades**, the `agent-skills` engineering pack provides an authoritative, enterprise-ready standard for modern backend software delivery.

