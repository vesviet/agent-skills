# Contract Testing, Chaos Injection & Concurrency Verification — Reference

This reference documents 2027 testing standards for resilient distributed systems: Consumer-Driven Contract Testing (PactV3), in-test network chaos injection (Toxiproxy), Circuit Breaker state verification, and strict goroutine leak detection (`goleak`).

---

## 1. Consumer-Driven Contract Testing (PactV3)

Consumer-Driven Contract Testing eliminates breaking API changes between microservices without requiring brittle end-to-end multi-service test environments.

### 1.1 Core Principles
1. **Consumer-Driven**: The client (consumer) defines expectations for endpoints, query params, headers, and payload structures.
2. **Flexible Structural Matching**: Contracts assert data types and shape using PactV3 matchers (`like`, `eachLike`, `regex`) rather than hardcoded mock values.
3. **Provider State Isolation**: Providers set up isolated test fixtures based on a declared `providerState` before verifying interactions.

### 1.2 TypeScript PactV3 Consumer Contract Specification

```typescript
import { PactV3, MatchersV3 } from "@pact-foundation/pact";
import { PaymentClient } from "../clients/payment";

const { like, eachLike, regex } = MatchersV3;

const provider = new PactV3({
  consumer: "order-service",
  provider: "payment-service",
  dir: "./pacts"
});

test("fetches payment transaction details by transaction ID", async () => {
  await provider
    .given("payment txn_12345 exists and is settled")
    .uponReceiving("a request for payment txn_12345")
    .withRequest({
      method: "GET",
      path: "/v1/payments/txn_12345",
      headers: { Accept: "application/json" }
    })
    .willRespondWith({
      status: 200,
      headers: { "Content-Type": "application/json" },
      body: {
        paymentId: like("txn_12345"),
        status: regex("SETTLED|AUTHORIZED", "SETTLED"),
        amountCents: like(10000),
        currency: regex("^[A-Z]{3}$", "USD"),
        lineItems: eachLike({
          itemId: like("item_abc"),
          quantity: like(1)
        })
      }
    })
    .executeTest(async (mockServer) => {
      const client = new PaymentClient(mockServer.url);
      const res = await client.getPayment("txn_12345");
      expect(res.paymentId).toBe("txn_12345");
      expect(res.status).toBe("SETTLED");
    });
});
```

---

## 2. In-Test Chaos Injection via Toxiproxy

Unit tests with in-memory mocks fail to verify real-world transport failure handling. Toxiproxy simulates production network faults deterministically in local integration tests.

### 2.1 Toxic Types & Failure Modes
- **`latency`**: Adds simulated latency and jitter (e.g., 2000ms ± 500ms) to trigger timeouts and race conditions.
- **`reset_peer`**: Simulates TCP RST packets or abrupt network disconnects mid-stream.
- **`bandwidth`**: Limits downstream or upstream throughput (e.g., 10 KB/s) to simulate mobile packet loss or network degradation.
- **`slicer`**: Slices TCP packets into small chunks with delays to test socket streaming parsers.

### 2.2 Go In-Test Toxiproxy Walkthrough

```go
package chaos_test

import (
	"context"
	"testing"
	"time"

	toxiproxy "github.com/Shopify/toxiproxy/v2/client"
	"github.com/stretchr/testify/assert"
)

func TestClientCircuitBreakerUnderNetworkChaos(t *testing.T) {
	toxiClient := toxiproxy.NewClient("localhost:8474")

	// Create proxy between payment client and downstream mock server
	proxy, err := toxiClient.CreateProxy("payment_proxy", "localhost:28080", "localhost:18080")
	assert.NoError(t, err)
	defer proxy.Delete()

	// 1. Inject high latency toxic (simulate 3000ms delay)
	toxic, err := proxy.AddToxic("slow_network", "latency", "downstream", 1.0, toxiproxy.Attributes{
		"latency": 3000,
		"jitter":  200,
	})
	assert.NoError(t, err)

	client := NewResilientClient("http://localhost:28080", 500*time.Millisecond)

	// 2. Client timeout triggers
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	_, err = client.ExecuteRequest(ctx)
	assert.ErrorIs(t, err, context.DeadlineExceeded)

	// 3. Remove toxic and verify automatic recovery
	assert.NoError(t, proxy.RemoveToxic(toxic.Name))
	resp, err := client.ExecuteRequest(context.Background())
	assert.NoError(t, err)
	assert.Equal(t, 200, resp.StatusCode)
}
```

---

## 3. Circuit Breaker State Transition Testing

A circuit breaker prevents cascading microservice failures by failing fast when a dependency degrades.

### 3.1 State Machine Specification
```
        ┌──────────────────────────────────────┐
        │                                      │ Success count >= threshold
        ▼                                      │
  ┌───────────┐      Failure threshold reached ┌───────────┐
  │  CLOSED   ├───────────────────────────────►│   OPEN    │
  │ (Normal)  │                                │(Fast-Fail)│
  └─────▲─────┘                                └─────┬─────┘
        │                                            │
        │ Success                      Timeout expires│
        │                                            │
        │              ┌───────────┐                 │
        └──────────────┤ HALF-OPEN │◄────────────────┘
                       │ (Probing) │
                       └─────┬─────┘
                             │ Failure
                             ▼
                        (Back to OPEN)
```

### 3.2 Verification Protocol
1. **Transition to OPEN**: Fire $N$ consecutive simulated failure requests (e.g. 5 failures within 10 seconds). Assert that subsequent requests fail immediately without invoking the network (`ErrCircuitOpen`).
2. **Transition to HALF-OPEN**: Advance virtual or real clock past the sleep window (e.g. 5 seconds). Assert the breaker permits a single probe request.
3. **Transition to CLOSED**: Assert that successful probe resets failure counters and restores normal traffic.

---

## 4. Concurrency & Goroutine Leak Assertions

Data races and goroutine leaks in asynchronous services cause memory starvation and mysterious production deadlocks.

### 4.1 Race Detection
Run all test suites with the race detector enabled:
```bash
go test -v -race -count=1 ./...
```

### 4.2 Leak Detection with `uber-go/goleak`
Enforce that no background goroutines linger after test teardown:

```go
package integration_test

import (
	"testing"
	"go.uber.org/goleak"
)

func TestMain(m *testing.M) {
	// Verify zero leaked goroutines across all package tests
	goleak.VerifyTestMain(m)
}

func TestWorkerPoolShutdown(t *testing.T) {
	defer goleak.VerifyNone(t)

	pool := NewWorkerPool(4)
	pool.Submit(func() { /* task */ })
	pool.Shutdown() // Must cancel all internal worker loops
}
```
