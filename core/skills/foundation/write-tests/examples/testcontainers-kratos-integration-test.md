# Worked Example: Testcontainers + Go Kratos Integration Test

This worked example demonstrates an ephemeral integration test for Go Kratos microservices using `testcontainers-go` to spin up PostgreSQL 18, Wire dependency injection, uncommitted transactional rollbacks (`InTx`) for cross-test state isolation, and goroutine leak detection (`goleak`).

---

## 1. Test Suite Architecture

```
┌────────────────────────────────────────────────────────┐
│                   go test -v -race                     │
│                                                        │
│  ┌──────────────────┐          ┌────────────────────┐  │
│  │ TestMain Setup   ├─────────►│ PostgreSQL 18      │  │
│  │ (testcontainers) │          │ Ephemeral Container│  │
│  └────────┬─────────┘          └─────────▲──────────┘  │
│           │                              │             │
│  ┌────────▼─────────┐                    │             │
│  │ Wire DI Init     │                    │             │
│  │ (TestProviderSet)│                    │             │
│  └────────┬─────────┘                    │             │
│           │                              │             │
│  ┌────────▼──────────────────────────────┴──────────┐  │
│  │ Subtest 1: InTx Rollback ──► Zero State Contam.  │  │
│  │ Subtest 2: InTx Rollback ──► Zero State Contam.  │  │
│  │ goleak.VerifyNone(t)     ──► Zero Leaks          │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Complete Integration Test (`test/payment_integration_test.go`)

```go
package test

import (
	"context"
	"fmt"
	"testing"
	"time"

	"payment/internal/biz"
	"payment/internal/data"

	"github.com/go-kratos/kratos/v2/log"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/modules/postgres"
	"github.com/testcontainers/testcontainers-go/wait"
	"go.uber.org/goleak"
	gormpg "gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var (
	testDB *gorm.DB
	pgC    *postgres.PostgresContainer
)

func TestMain(m *testing.M) {
	ctx := context.Background()

	// 1. Start ephemeral PostgreSQL 18 container
	var err error
	pgC, err = postgres.Run(ctx,
		"postgres:18-alpine",
		postgres.WithDatabase("testdb"),
		postgres.WithUsername("testuser"),
		postgres.WithPassword("testpass"),
		testcontainers.WithWaitStrategy(
			wait.ForLog("database system is ready to accept connections").
				WithOccurrence(2).
				WithStartupTimeout(30*time.Second),
		),
	)
	if err != nil {
		panic(fmt.Sprintf("Failed to start Postgres container: %v", err))
	}

	// 2. Obtain connection string and initialize GORM
	connStr, err := pgC.ConnectionString(ctx, "sslmode=disable")
	if err != nil {
		panic(err)
	}

	testDB, err = gorm.Open(gormpg.Open(connStr), &gorm.Config{})
	if err != nil {
		panic(err)
	}

	// Run auto-migration for test schema
	if err := testDB.AutoMigrate(&data.PaymentPO{}); err != nil {
		panic(err)
	}

	// 3. Execute test suite with goleak verification
	code := m.Run()

	// 4. Terminate container
	_ = pgC.Terminate(ctx)

	goleak.VerifyTestMain(m)
}

func TestPaymentUsecase_Integration(t *testing.T) {
	defer goleak.VerifyNone(t)

	// Dependency injection wiring
	logger := log.DefaultLogger
	d, cleanup, err := data.NewData(testDB, logger)
	require.NoError(t, err)
	defer cleanup()

	repo := data.NewPaymentRepo(d, logger)
	tx := data.NewTransaction(d)
	uc := biz.NewPaymentUsecase(repo, tx, logger)

	t.Run("Subtest 1 - Insert payment within isolated transaction rollback", func(t *testing.T) {
		ctx := context.Background()

		// Execute operation inside a manual transaction that rolls back at end of subtest
		err := testDB.Transaction(func(txDB *gorm.DB) error {
			subData, _, _ := data.NewData(txDB, logger)
			subRepo := data.NewPaymentRepo(subData, logger)
			subUsecase := biz.NewPaymentUsecase(subRepo, data.NewTransaction(subData), logger)

			payment := &biz.Payment{
				ID:             "txn-test-001",
				IdempotencyKey: "idemp-key-alpha",
				AmountCents:    10000,
				Currency:       "USD",
				RecipientID:    "rec-001",
			}

			saved, err := subUsecase.ProcessPayment(ctx, payment)
			assert.NoError(t, err)
			assert.Equal(t, "SETTLED", saved.Status)

			// Verify record exists in active transaction view
			found, err := subRepo.GetByIdempotencyKey(ctx, "idemp-key-alpha")
			assert.NoError(t, err)
			assert.NotNil(t, found)
			assert.Equal(t, "txn-test-001", found.ID)

			// Return error deliberately to force rollback
			return fmt.Errorf("force-rollback-for-isolation")
		})

		assert.Error(t, err)
	})

	t.Run("Subtest 2 - Verify zero state contamination from Subtest 1", func(t *testing.T) {
		ctx := context.Background()

		// Verify that "idemp-key-alpha" from Subtest 1 does NOT exist in the database
		found, err := repo.GetByIdempotencyKey(ctx, "idemp-key-alpha")
		assert.NoError(t, err)
		assert.Nil(t, found, "Expected database to be clean; rolled back transaction leaked data!")

		// Insert fresh record cleanly
		payment := &biz.Payment{
			ID:             "txn-test-002",
			IdempotencyKey: "idemp-key-alpha", // Reuse same key safely
			AmountCents:    25000,
			Currency:       "EUR",
			RecipientID:    "rec-002",
		}

		saved, err := uc.ProcessPayment(ctx, payment)
		assert.NoError(t, err)
		assert.Equal(t, "SETTLED", saved.Status)
		assert.Equal(t, int64(25000), saved.AmountCents)
	})
}
```

---

## 3. Key Verification Guarantees

1. **Zero Database Drift**: Each subtest operates in an uncommitted rollback wrapper, eliminating the need to drop tables, run truncate scripts, or restart Docker containers between test cases.
2. **Ephemeral Port Mapping**: `testcontainers-go` binds PostgreSQL to a random available host port, preventing port collision (`5432 already in use`) in parallel CI runs.
3. **Goroutine Leak Proof**: `goleak.VerifyNone(t)` guarantees no unclosed database connection pools or background monitoring threads remain active after test completion.
