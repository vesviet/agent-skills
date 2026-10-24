## E-Commerce Engineer Review Checklist

This reference checklist provides operational architecture, transactional integrity, payment security, and fulfillment engineering criteria for e-commerce systems to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across extreme-throughput checkout architectures (Alipay 610k TPS scale), server-side pricing authority, Redis Lua inventory fencing tokens, database idempotency ledgers, PCI-DSS v4.1.0 compliance, autonomous agentic commerce (AP2 / UCP mandates), double-entry financial ledgering, and anti-scalping traffic shields.

### 1. High-Throughput Checkout Architecture & Redis Lua Fencing (`TTL-RESERVATION LOCK`)
- **Atomic Inventory Fencing via Redis Lua**:
  - inventory stock decrements executed atomically using evaluated Redis Lua scripts with monotonic fencing tokens, eliminating read-then-write race conditions and overselling under concurrent flash-sale bursts:
    ```lua
    -- Atomic Available-to-Promise (ATP) Decrement with Monotonic Fencing Token
    local stock = tonumber(redis.call('get', KEYS[1]) or 0)
    local requested = tonumber(ARGV[1])
    if stock >= requested then
      redis.call('decrby', KEYS[1], requested)
      local fencing_token = redis.call('incr', KEYS[2])
      return {1, fencing_token}
    end
    return {0, 0}
    ```
  - inventory reservations backed by a Time-To-Live (TTL) reservation state machine (e.g. 15-minute hold window); expired reservations returned to Available-to-Promise (ATP) stock automatically via scheduled reconciliation
- **Partitioned Stock Sharding & OceanBase 610k TPS Hotspot Protection**:
  - high-velocity SKUs partitioned across virtual stock buckets (e.g. `SKU_1001_bucket_0..N`) to distribute write lock contention across database rows and Redis keys
  - stock reservation operations guarantee bounded latency (P99 $\le 10\text{ms}$) under high-volume concurrency
  - OceanBase / distributed relational databases configure row-level hotspot bypass and batch commit merging during flash-sale events

### 2. Server-Side Pricing Authority & Cart Tampering Defense (`SERVER-PRICING-AUTHORITY LOCK`)
- **Zero Client Price Trust & Fixed-Point Math**:
  - all unit prices, tier discounts, coupon codes, shipping costs, and localized sales tax (VAT / GST) computed authoritatively server-side at the moment of charge creation:
    ```go
    // POSITIVE: Server-Side Authoritative Pricing with Integer Cents
    func CalculateOrderTotal(ctx context.Context, cart *Cart, promoCode string) (*OrderSummary, error) {
        var subtotalCents int64 = 0
        for _, item := range cart.Items {
            unitPrice := catalogRepo.GetAuthoritativePrice(ctx, item.SKU) // Never trust cart.ItemPrice
            subtotalCents += unitPrice * item.Quantity
        }
        discountCents := promoEngine.ApplyValidatedCoupon(ctx, promoCode, subtotalCents)
        taxCents := taxService.ComputeStatutoryVAT(ctx, subtotalCents - discountCents)
        return &OrderSummary{
            SubtotalCents: subtotalCents,
            DiscountCents: discountCents,
            TaxCents:      taxCents,
            TotalCents:    subtotalCents - discountCents + taxCents,
        }, nil
    }
    ```
  - client-submitted price totals, discounts, or modified item amounts strictly ignored or rejected fail-closed
- **Coupon & Promotion State Machine**:
  - promo codes validated against strict usage limit constraints (per-user limit, global budget ceiling, category exclusions, minimum spend) inside atomic database transactions
  - expired, disabled, or non-stackable promotion combinations rejected fail-closed

### 3. Payment Gateway Integration & Idempotency Ledger (`IDEMPOTENCY-LEDGER LOCK`)
- **Deterministic Idempotency Keys**:
  - every payment mutation, capture, authorization, and refund request requires a deterministic idempotency key (UUIDv7 or SHA-256 hash of order ID + attempt number)
  - database unique constraint on `(idempotency_key)` guarantees zero duplicate charge executions on network retries or client double-clicks
- **Secure Webhook Ingestion & Signature Verification**:
  - payment provider webhooks (Stripe, Adyen, MoMo, VNPay) must verify HMAC-SHA256 signatures before reading payload data
  - webhook events recorded to an incoming event ledger table before processing; asynchronous workers handle event side effects to return HTTP 200 within $<2\text{s}$

### 4. PCI-DSS v4.1.0 Compliance & Cardholder Data Isolation (`PCI-DSS-401 LOCK` / `PAYMENT-LOCK`)
- **Zero Raw Cardholder Data on Backend (SAQ-A)**:
  - backend systems strictly out of PCI scope (SAQ-A compliant); credit card numbers (PAN), CVV/CVC, and expiration dates tokenized directly in client browser via payment gateway SDK iframe / Elements
  - logs, traces, APM spans, and database dumps audited to ensure 100% absence of raw card data
- **Subresource Integrity (SRI) & Script Tamper Detection (Req 6.4.3 / 11.6.1)**:
  - all external JavaScript libraries loaded on checkout pages mandate cryptographic Subresource Integrity (`integrity="sha384-..."`) and strict Content Security Policy (CSP):
    ```http
    Content-Security-Policy: default-src 'self'; script-src 'self' https://js.stripe.com 'sha384-...'; frame-src https://js.stripe.com; object-src 'none'
    ```
  - automated script change monitoring alerts on unauthorized DOM modifications or unapproved script injections within payment flows

### 5. Autonomous Agent Commerce & Cryptographic User Mandates (`MANDATE-AUTHORIZATION LOCK` / `NHI-COMMERCE LOCK`)
- **Cryptographic User Mandate Verification (AP2 / Verifiable Credentials)**:
  - autonomous AI purchasing agents must present a cryptographically signed User Mandate (e.g. W3C Verifiable Credential or signed AP2 token) authorizing transaction parameters:
    ```json
    {
      "mandate_id": "urn:ap2:mandate:7f8e4a88-8254-8e1f592e3894",
      "type": ["VerifiableCredential", "AgentCommerceMandate"],
      "issuer": "did:key:z6Mku...user",
      "credentialSubject": {
        "merchant_domain": "store.domain.internal",
        "max_amount_cents": 50000,
        "currency": "USD",
        "valid_until": "2026-10-31T23:59:59Z"
      }
    }
    ```
  - mandate verified against: allowed merchant domain, explicit item category, per-transaction spending limit, and expiration timestamp
- **AI Agent Identity & Velocity Rate Limiting**:
  - agent checkout sessions authenticated as distinct Non-Human Identities (NHI); rate limiting fences prevent algorithmic high-frequency order flooding
  - transactions exceeding autonomous thresholds pause execution for Human-in-the-Loop (HITL) step-up approval

### 6. Double-Entry Accounting Ledger & Distributed Financial Sagas
- **Balanced Debit/Credit Ledger Invariant**:
  - every monetary movement recorded as an immutable double-entry ledger entry satisfying the mathematical invariant:
    $$\sum_{i=1}^N \text{Debits}_i \equiv \sum_{j=1}^M \text{Credits}_j$$
  - monetary calculations strictly utilize integer cents or fixed-point decimal arithmetic (64-bit integer); IEEE 754 floating-point operations on currency are strictly prohibited
- **Compensating Sagas for Distributed Failures**:
  - multi-stage checkout workflows (Auth $\rightarrow$ Inventory Deduct $\rightarrow$ Shipping Label Creation $\rightarrow$ Capture) orchestrated via distributed Sagas (Temporal or Dapr)
  - failures at any step trigger automated compensating actions (e.g. authorization void, stock release) ensuring zero inconsistent state

### 7. Shopee Traffic Shield & Anti-Scalping Protection
- **Bot Mitigation & Virtual Waiting Rooms**:
  - flash-sale traffic routed through edge waiting-room queues (Queue-it / Cloudflare Waiting Room) during traffic surges
  - device fingerprinting, TLS JA4 inspection, and behavioral analysis identify and reject automated scalper bots before reaching cart APIs
  - address normalization and fuzzy matching detect scalper rings attempting bulk checkout across coordinated dummy accounts

### 8. Vietnamese Statutory Accounting & AMIS Revenue Sync (`AMIS-REVENUE-SYNC-LOCK`)
- **Dual-Header Sales & Tax Record Synchronization**:
  - checkout tax and revenue calculations in Vietnamese commerce operations must generate data compatible with Circular 200/133/99 and MISA AMIS 63-column dual-header sales records
  - return merchandise authorizations (RMA) synchronized with AMIS 44-column return manifests

### 9. Operational Telemetry & Checkout SLOs
- **PromQL Operational Invariants**:
  ```promql
  # Flash-sale checkout success rate (must be >= 99.0%)
  sum(rate(checkout_success_total[5m])) / (sum(rate(checkout_success_total[5m])) + sum(rate(checkout_failed_total[5m]))) * 100 >= 99.0
  
  # P99 Inventory reservation latency (must be < 10ms)
  histogram_quantile(0.99, rate(inventory_reservation_duration_seconds_bucket[5m])) < 0.010
  ```

### 10. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Lua Inventory Atomicity** | 0 oversell anomalies | `redis-benchmark -s redis.sock evalsha ...` | Monotonic fencing token returned |
| **Double-Entry Balance** | $\sum \text{Debits} = \sum \text{Credits}$ | Automated SQL ledger audit test | Balanced to the exact cent |
| **Idempotency Constraint** | 0 duplicate charges | `curl -X POST ... -H "Idempotency-Key: ..."` | Second call returns original result |
| **PCI SAQ-A Compliance** | 0 raw PAN in logs | `rg -E "[0-9]{13,16}" /var/log/app/` | 0 raw credit card matches |
| **AMIS Sync Alignment** | 63-col schema match | `python3 core/scripts/validate-contracts.py` | Valid revenue manifest schema |
| **AP2 Mandate Crypto** | ECDSA / Ed25519 valid | `verify-vc-mandate --input mandate.json` | Signature valid, unexpired |
