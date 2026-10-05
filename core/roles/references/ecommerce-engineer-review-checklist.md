## E-Commerce Engineer Review Checklist

This reference checklist provides operational architecture, transactional integrity, payment security, and fulfillment engineering criteria for e-commerce systems to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across extreme-throughput checkout architectures (Alipay 610k TPS scale), server-side pricing authority, Redis Lua inventory fencing tokens, database idempotency ledgers, PCI-DSS v4.1.0 compliance, autonomous agentic commerce (AP2 / UCP mandates), double-entry financial ledgering, and anti-scalping traffic shields.

### 1. High-Throughput Checkout Architecture & Redis Lua Fencing (`TTL-RESERVATION LOCK`)
- **Atomic Inventory Fencing via Redis Lua**:
  - inventory stock decrements executed atomically using evaluated Redis Lua scripts with fencing tokens, eliminating read-then-write race conditions and overselling under concurrent flash-sale bursts
  - inventory reservations backed by a Time-To-Live (TTL) reservation state machine (e.g. 15-minute hold window); expired reservations returned to Available-to-Promise (ATP) stock automatically via scheduled reconciliation
  - physical stock decrements committed to persistent database only upon successful payment confirmation
- **Partitioned Stock Sharding & Hotspot Protection**:
  - high-velocity SKUs partitioned across virtual stock buckets (e.g. SKU_1001_bucket_0..N) to distribute write lock contention across database rows and Redis keys
  - stock reservation operations guarantee bounded latency (P99 $\le 10\text{ms}$) under high-volume concurrency

### 2. Server-Side Pricing Authority & Cart Tampering Defense (`SERVER-PRICING-AUTHORITY LOCK`)
- **Zero Client Price Trust**:
  - all unit prices, tier discounts, coupon codes, shipping costs, and localized sales tax (VAT / GST) computed authoritatively server-side at the moment of charge creation
  - client-submitted price totals, discounts, or modified item amounts strictly ignored or rejected
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
- **Zero Raw Cardholder Data on Backend**:
  - backend systems strictly out of PCI scope (SAQ-A compliant); credit card numbers (PAN), CVV/CVC, and expiration dates tokenized directly in client browser via payment gateway SDK iframe / Elements
  - logs, traces, APM spans, and database dumps audited to ensure 100% absence of raw card data
- **Subresource Integrity (SRI) & Script Tamper Detection (Req 6.4.3 / 11.6.1)**:
  - all external JavaScript libraries loaded on checkout pages mandate cryptographic Subresource Integrity (`integrity="sha384-..."`) and strict Content Security Policy (CSP)
  - automated script change monitoring alerts on unauthorized DOM modifications or unapproved script injections within payment flows

### 5. Autonomous Agent Commerce & Cryptographic User Mandates (`MANDATE-AUTHORIZATION LOCK` / `NHI-COMMERCE LOCK`)
- **Cryptographic User Mandate Verification (AP2 / Verifiable Credentials)**:
  - autonomous AI purchasing agents must present a cryptographically signed User Mandate (e.g. W3C Verifiable Credential or signed AP2 token) authorizing transaction parameters
  - mandate verified against: allowed merchant domain, explicit item category, per-transaction spending limit, and expiration timestamp
- **AI Agent Identity & Velocity Rate Limiting**:
  - agent checkout sessions authenticated as distinct Non-Human Identities (NHI); rate limiting fences prevent algorithmic high-frequency order flooding
  - transactions exceeding autonomous thresholds pause execution for Human-in-the-Loop (HITL) step-up approval

### 6. Double-Entry Accounting Ledger & Distributed Financial Sagas
- **Balanced Debit/Credit Ledger Invariant**:
  - every monetary movement recorded as an immutable double-entry ledger entry satisfying the mathematical invariant:
    $$\sum \text{Debits} \equiv \sum \text{Credits}$$
  - money cannot be created or destroyed across accounts (Customer Accounts, Merchant Receivables, Platform Fee Escrow, Gateway Clearing)
- **Compensating Sagas for Distributed Failures**:
  - multi-stage checkout workflows (Auth $\rightarrow$ Inventory Deduct $\rightarrow$ Shipping Label Creation $\rightarrow$ Capture) orchestrated via distributed Sagas (Temporal or Dapr)
  - failures at any step trigger automated compensating actions (e.g. authorization void, stock release) ensuring zero inconsistent state

### 7. Shopee Traffic Shield & Anti-Scalping Protection
- **Bot Mitigation & Virtual Waiting Rooms**:
  - flash-sale traffic routed through edge waiting-room queues (Queue-it / Cloudflare Waiting Room) during traffic surges
  - device fingerprinting, TLS JA4 inspection, and behavioral analysis identify and reject automated scalper bots before reaching cart APIs
- **Account Farm & Multi-Accounting Defense**:
  - address normalization and fuzzy matching detect scalper rings attempting bulk checkout across coordinated dummy accounts

### 8. Fulfillment, Return Merchandise & Tracking Integration
- **Deterministic Order State Machine (`STATE-MACHINE LOCK`)**:
  - order status transitions follow a rigid, documented state machine: `PENDING` $\rightarrow$ `CONFIRMED` $\rightarrow$ `ALLOCATED` $\rightarrow$ `SHIPPED` $\rightarrow$ `DELIVERED`
  - invalid transitions (e.g. `REFUNDED` $\rightarrow$ `SHIPPED`) blocked fail-closed in business logic
- **Return & Refund Verification**:
  - refunds tied immutably to original payment charge IDs; partial refunds track remaining refundable balance to prevent over-refund exploits
