# Machine Payments Protocol (MPP), x402, and Webhook Security Specifications (2026)

## 1. Webhook Ingestion & Cryptographic Verification

### 1.1 HMAC SHA-256 Signature Hardening
Payment webhook endpoints are the primary target for unauthorized state transition tampering. The following invariants are non-negotiable:
- **Raw Payload Preservation**: The HMAC signature must be calculated exclusively over the raw, unparsed byte buffer of the HTTP request body (`req.rawBody`). Any JSON re-serialization before verification introduces whitespace/key-ordering mutations that break cryptographic integrity.
- **Constant-Time Comparison**: Comparison between computed and transmitted HMAC digests must use constant-time operations (`crypto.timingSafeEqual` in Node.js or `hmac.compare_digest` in Python) to prevent statistical timing side-channel attacks.
- **Replay Window Enforcement**: Reject any webhook where the payload timestamp drifts by more than 300 seconds ($T_{drift} > 300\text{s}$) relative to server time ($T_{now}$).

### 1.2 Queue-First Architecture (<500ms SLA)
To guarantee high availability and prevent gateway timeouts:
1. Verify signature over raw bytes.
2. Persist the raw event to an asynchronous durable message queue (Kafka, Cloudflare Queues, AWS SQS, or RabbitMQ).
3. Immediately return HTTP `200 OK` within 500ms.
4. Downstream consumer workers execute business logic (ledger booking, fulfillment dispatch).

### 1.3 Dual-Write Idempotency Guards
Webhook delivery semantics are strictly at-least-once. To ensure exactly-once execution:
- **Database Composite Constraint**: Enforce a unique database constraint on `(provider, event_id, event_type)`.
- **Distributed Lock**: Acquire a distributed lock (Redis Redlock or PostgreSQL Advisory Lock) keyed by `lock:payment:event:<event_id>` with a 30-second TTL before initiating order state transitions.

---

## 2. Machine Payments Protocol (MPP) & HTTP 402 / x402

### 2.1 Autonomous Agent Payment Flow
Autonomous AI agents interact with paywalled APIs via the Machine Payments Protocol (MPP) and the open x402 specification:

1. **Challenge Stage**: Client agent requests a restricted resource; server responds with HTTP `402 Payment Required` accompanied by the `Payment-Required` challenge header containing base64-encoded payment schemes, pricing, and deposit addresses.
2. **Credential Negotiation**:
   - *Fiat / Cards*: Shared Payment Tokens (SPTs) or off-session `SetupIntents` with `setup_future_usage: "off_session"`.
   - *Stablecoins*: USDC on Base or Tempo network via Coinbase Developer Platform (CDP) facilitators.
3. **Settlement Verification**:
   - Merchant validates the on-chain transaction receipt or Stripe `crypto` transaction verification object (`POST /v1/crypto/deposit_addresses`).
4. **Fulfillment**: Once verified, the server yields the requested resource payload with payment confirmation headers.

---

## 3. Account-to-Account (A2A) Pay by Bank Settlement

### 3.1 Asynchronous Settlement State Machine
Bank-to-bank direct payment rails (Plaid, TrueLayer, Stripe Pay by Bank) execute across asynchronous settlement phases:
- `processing`: Initial customer bank consent and payment initiation.
- `pending`: ACH/SEPA clearance in flight. Inventory must be protected with a soft TTL lock (typically 48–72 hours).
- `settled`: Final funds settlement confirmed via signed webhook. Order transitions to `paid`, locking inventory hard.
- `failed` / `cancelled`: Settlement rejected or NSF. Soft inventory lock automatically releases via sweeper.
