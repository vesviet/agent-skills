# Worked Example: Go Kratos Clean Architecture Endpoint

This worked example demonstrates an enterprise-grade endpoint in Go 1.25+ using the Kratos v2.9.1 microservices framework, strictly adhering to Clean Architecture across `api`, `service`, `biz`, and `data` layers with GORM transaction safety (`InTx`) and table-driven unit tests.

---

## 1. Protobuf Contract (`api/payment/v1/payment.proto`)

```protobuf
syntax = "proto3";

package payment.v1;

option go_package = "payment/api/payment/v1;v1";

import "google/api/annotations.proto";
import "validate/validate.proto";

service PaymentService {
  rpc ProcessPayment (ProcessPaymentRequest) returns (ProcessPaymentReply) {
    option (google.api.http) = {
      post: "/v1/payments"
      body: "*"
    };
  }
}

message ProcessPaymentRequest {
  string idempotency_key = 1 [(validate.rules).string = {min_len: 16, max_len: 128}];
  int64 amount_cents = 2 [(validate.rules).int64 = {gt: 0}];
  string currency = 3 [(validate.rules).string = {len: 3}];
  string recipient_id = 4 [(validate.rules).string = {uuid: true}];
}

message ProcessPaymentReply {
  string payment_id = 1;
  string status = 2;
  int64 amount_cents = 3;
  string currency = 4;
  string recipient_id = 5;
  int64 created_at = 6;
}
```

---

## 2. Biz Layer — Pure Business Logic (`internal/biz/payment.go`)

The biz layer contains domain models and usecases. It has **zero knowledge of GORM, SQL, or transport protocols**:

```go
package biz

import (
	"context"
	"errors"
	"time"

	"github.com/go-kratos/kratos/v2/log"
)

var (
	ErrInvalidAmount    = errors.New("payment amount must be greater than zero")
	ErrDuplicatePayment = errors.New("duplicate payment transaction detected")
)

type Payment struct {
	ID             string
	IdempotencyKey string
	AmountCents    int64
	Currency       string
	RecipientID    string
	Status         string
	CreatedAt      time.Time
}

type PaymentRepo interface {
	Save(ctx context.Context, p *Payment) (*Payment, error)
	GetByIdempotencyKey(ctx context.Context, key string) (*Payment, error)
}

type Transaction interface {
	InTx(ctx context.Context, fn func(ctx context.Context) error) error
}

type PaymentUsecase struct {
	repo PaymentRepo
	tx   Transaction
	log  *log.Helper
}

func NewPaymentUsecase(repo PaymentRepo, tx Transaction, logger log.Logger) *PaymentUsecase {
	return &PaymentUsecase{
		repo: repo,
		tx:   tx,
		log:  log.NewHelper(logger),
	}
}

func (uc *PaymentUsecase) ProcessPayment(ctx context.Context, p *Payment) (*Payment, error) {
	if p.AmountCents <= 0 {
		return nil, ErrInvalidAmount
	}

	// Verify idempotency
	existing, err := uc.repo.GetByIdempotencyKey(ctx, p.IdempotencyKey)
	if err == nil && existing != nil {
		uc.log.WithContext(ctx).Infof("Idempotent replay for key: %s", p.IdempotencyKey)
		return existing, nil
	}

	p.Status = "SETTLED"
	p.CreatedAt = time.Now().UTC()

	var created *Payment
	err = uc.tx.InTx(ctx, func(ctx context.Context) error {
		var saveErr error
		created, saveErr = uc.repo.Save(ctx, p)
		return saveErr
	})

	if err != nil {
		return nil, err
	}
	return created, nil
}
```

---

## 3. Data Layer — Persistence (`internal/data/payment.go`)

The data layer implements `biz.PaymentRepo` and `biz.Transaction` using GORM:

```go
package data

import (
	"context"
	"errors"
	"time"

	"payment/internal/biz"

	"github.com/go-kratos/kratos/v2/log"
	"gorm.io/gorm"
)

type PaymentPO struct {
	ID             string    `gorm:"primaryKey;type:varchar(64)"`
	IdempotencyKey string    `gorm:"uniqueIndex;type:varchar(128);not null"`
	AmountCents    int64     `gorm:"not null"`
	Currency       string    `gorm:"type:varchar(3);not null"`
	RecipientID    string    `gorm:"type:varchar(64);not null"`
	Status         string    `gorm:"type:varchar(32);not null"`
	CreatedAt      time.Time `gorm:"not null"`
}

func (PaymentPO) TableName() string {
	return "payments"
}

type paymentRepo struct {
	data *Data
	log  *log.Helper
}

func NewPaymentRepo(data *Data, logger log.Logger) biz.PaymentRepo {
	return &paymentRepo{
		data: data,
		log:  log.NewHelper(logger),
	}
}

func (r *paymentRepo) Save(ctx context.Context, p *biz.Payment) (*biz.Payment, error) {
	po := &PaymentPO{
		ID:             p.ID,
		IdempotencyKey: p.IdempotencyKey,
		AmountCents:    p.AmountCents,
		Currency:       p.Currency,
		RecipientID:    p.RecipientID,
		Status:         p.Status,
		CreatedAt:      p.CreatedAt,
	}

	db := r.data.DB(ctx)
	if err := db.WithContext(ctx).Create(po).Error; err != nil {
		return nil, err
	}
	return p, nil
}

func (r *paymentRepo) GetByIdempotencyKey(ctx context.Context, key string) (*biz.Payment, error) {
	var po PaymentPO
	db := r.data.DB(ctx)
	err := db.WithContext(ctx).Where("idempotency_key = ?", key).First(&po).Error
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil
		}
		return nil, err
	}

	return &biz.Payment{
		ID:             po.ID,
		IdempotencyKey: po.IdempotencyKey,
		AmountCents:    po.AmountCents,
		Currency:       po.Currency,
		RecipientID:    po.RecipientID,
		Status:         po.Status,
		CreatedAt:      po.CreatedAt,
	}, nil
}
```

---

## 4. Service Layer — Adapter (`internal/service/payment.go`)

Adapts incoming Protobuf DTOs to Biz entities and maps domain errors to gRPC/HTTP status codes:

```go
package service

import (
	"context"

	v1 "payment/api/payment/v1"
	"payment/internal/biz"

	"github.com/go-kratos/kratos/v2/errors"
	"github.com/go-kratos/kratos/v2/log"
	"github.com/google/uuid"
)

type PaymentService struct {
	v1.UnimplementedPaymentServiceServer
	uc  *biz.PaymentUsecase
	log *log.Helper
}

func NewPaymentService(uc *biz.PaymentUsecase, logger log.Logger) *PaymentService {
	return &PaymentService{
		uc:  uc,
		log: log.NewHelper(logger),
	}
}

func (s *PaymentService) ProcessPayment(ctx context.Context, req *v1.ProcessPaymentRequest) (*v1.ProcessPaymentReply, error) {
	entity := &biz.Payment{
		ID:             uuid.New().String(),
		IdempotencyKey: req.IdempotencyKey,
		AmountCents:    req.AmountCents,
		Currency:       req.Currency,
		RecipientID:    req.RecipientId,
	}

	res, err := s.uc.ProcessPayment(ctx, entity)
	if err != nil {
		if errors.Is(err, biz.ErrInvalidAmount) {
			return nil, errors.BadRequest("INVALID_AMOUNT", err.Error())
		}
		s.log.WithContext(ctx).Errorf("Internal payment error: %v", err)
		return nil, errors.InternalServer("PAYMENT_FAILED", "Unable to complete transaction")
	}

	return &v1.ProcessPaymentReply{
		PaymentId:   res.ID,
		Status:      res.Status,
		AmountCents: res.AmountCents,
		Currency:    res.Currency,
		RecipientId: res.RecipientID,
		CreatedAt:   res.CreatedAt.Unix(),
	}, nil
}
```

---

## 5. Table-Driven Unit Tests (`internal/biz/payment_test.go`)

```go
package biz_test

import (
	"context"
	"testing"
	"time"

	"payment/internal/biz"

	"github.com/go-kratos/kratos/v2/log"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type MockRepo struct {
	mock.Mock
}

func (m *MockRepo) Save(ctx context.Context, p *biz.Payment) (*biz.Payment, error) {
	args := m.Called(ctx, p)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*biz.Payment), args.Error(1)
}

func (m *MockRepo) GetByIdempotencyKey(ctx context.Context, key string) (*biz.Payment, error) {
	args := m.Called(ctx, key)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*biz.Payment), args.Error(1)
}

type MockTx struct{}

func (m *MockTx) InTx(ctx context.Context, fn func(ctx context.Context) error) error {
	return fn(ctx)
}

func TestProcessPayment(t *testing.T) {
	tests := []struct {
		name        string
		input       *biz.Payment
		setupMock   func(r *MockRepo)
		expectError error
		checkResult func(t *testing.T, res *biz.Payment)
	}{
		{
			name: "Success - New Payment Settled",
			input: &biz.Payment{
				IdempotencyKey: "test-key-1234567890",
				AmountCents:    5000,
				Currency:       "USD",
				RecipientID:    "rec-123",
			},
			setupMock: func(r *MockRepo) {
				r.On("GetByIdempotencyKey", mock.Anything, "test-key-1234567890").Return(nil, nil)
				r.On("Save", mock.Anything, mock.MatchedBy(func(p *biz.Payment) bool {
					return p.AmountCents == 5000 && p.Status == "SETTLED"
				})).Return(&biz.Payment{
					ID:          "pay-uuid-001",
					Status:      "SETTLED",
					AmountCents: 5000,
					CreatedAt:   time.Now(),
				}, nil)
			},
			expectError: nil,
			checkResult: func(t *testing.T, res *biz.Payment) {
				assert.Equal(t, "SETTLED", res.Status)
				assert.Equal(t, int64(5000), res.AmountCents)
			},
		},
		{
			name: "Error - Invalid Amount Rejected",
			input: &biz.Payment{
				AmountCents: -100,
			},
			setupMock:   func(r *MockRepo) {},
			expectError: biz.ErrInvalidAmount,
			checkResult: func(t *testing.T, res *biz.Payment) {
				assert.Nil(t, res)
			},
		},
		{
			name: "Success - Idempotent Replay Cached Record",
			input: &biz.Payment{
				IdempotencyKey: "replayed-key-9999",
				AmountCents:    1000,
			},
			setupMock: func(r *MockRepo) {
				r.On("GetByIdempotencyKey", mock.Anything, "replayed-key-9999").Return(&biz.Payment{
					ID:          "cached-pay-id",
					Status:      "SETTLED",
					AmountCents: 1000,
				}, nil)
			},
			expectError: nil,
			checkResult: func(t *testing.T, res *biz.Payment) {
				assert.Equal(t, "cached-pay-id", res.ID)
			},
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			repo := new(MockRepo)
			tc.setupMock(repo)
			uc := biz.NewPaymentUsecase(repo, &MockTx{}, log.DefaultLogger)

			res, err := uc.ProcessPayment(context.Background(), tc.input)

			if tc.expectError != nil {
				assert.ErrorIs(t, err, tc.expectError)
			} else {
				assert.NoError(t, err)
			}
			tc.checkResult(t, res)
			repo.AssertExpectations(t)
		})
	}
}
```
