---
name: integrate-payment-gateway
description: Integrate or extend a payment gateway (Stripe, VNPay, PayPal, Momo, etc.) into an e-commerce application. Use when adding, replacing, or auditing a payment provider's checkout, refund, or webhook flow.
---

# Integrate Payment Gateway

Use this skill when a task requires connecting an application to a payment provider's API, including initial setup, webhook handling, refund flows, and PCI-DSS-compliant implementation.

## When to Use

- adding/replacing a payment provider
- auditing checkout, refund, or webhook flow
- Stripe, VNPay, PayPal, Momo, etc.
- payment integration in e-commerce

## Core Rules

- never log, store, or return raw card numbers, CVV, or full PAN data — treat all card data as `restricted` per `core/policies/data-classification.yaml`; prefer **EMVCo Network Tokens** (Visa VTS, Mastercard MDES) with dynamic transaction cryptograms over raw PAN or gateway-specific tokens
- always use the provider's official SDK or API client; do not hand-roll raw HTTP calls to payment endpoints
- handle idempotency keys (UUID per transaction attempt) for all charge/capture operations to prevent double-billing
- **Webhook Signature Verification** (PCI DSS v4.1.0): compute HMAC over the **raw, unparsed request payload** before JSON parsing; use **constant-time comparison** (`crypto.timingSafeEqual` / `hmac.compare_digest`) to prevent timing side-channel attacks; reject any event with a timestamp older than 300 seconds to block replay attacks
- **Queue-First Webhook Ingestion**: return HTTP `200 OK` within **500 ms** after persisting the raw event — offload all state mutations to an async worker queue (Kafka, Cloudflare Queues, RabbitMQ); never perform heavy processing in the webhook handler synchronously
- enforce a **dual-write idempotency guard**: unique database index on `(provider, event_id, event_type)` combined with a distributed lock (Redis Redlock or Postgres Advisory Lock) during event processing to prevent duplicate state transitions
- store only tokenized references (e.g., `customer_id`, `payment_method_id`) — never raw payment credentials
- prefer dynamic payment methods (`automatic_payment_methods: { enabled: true }` in Stripe) over static backend payment method arrays
- support **HTTP 402 / MPP** programmatic machine payment challenges and off-session `SetupIntents` for autonomous agent checkout flows
- handle asynchronous clearing states (A2A bank transfers) via webhook state machine with inventory TTL lock during settlement pending

## Suggested Process

### 1. Clarify Integration Scope

Answer before building:

- which payment provider(s) are required?
- which flows: checkout, subscription, manual capture, refund, or dispute handling?
- what currency and locale requirements apply?
- is 3DS / SCA (Strong Customer Authentication) required?
- what is the test/live key management strategy?

### 2. Set Up Provider Configuration

- install the official SDK and pin the version
- configure environment-based keys (`STRIPE_SECRET_KEY`, `VNPAY_HASH_SECRET`, etc.) via `.env` — never hardcode
- configure webhook endpoints and register them with the provider dashboard
- set up idempotency key generation (UUID per transaction attempt)

### 3. Implement the Payment Flow

- **create payment intent / order**: call the provider to initialize a transaction with amount, currency, and metadata
- **confirm / capture**: handle redirect or SDK confirmation; capture only after authorization succeeds
- **webhook handler**: verify signature → parse event → update order status atomically → return `200` quickly (offload side effects)
- **refund path**: expose a refund endpoint; pass original charge/transaction ID; log refund ID for audit trail

### 4. Implement Error and Edge Case Handling

- map provider error codes to user-facing messages (do not expose raw gateway errors)
- handle card decline, insufficient funds, authentication required, and network timeout distinctly
- implement retry logic with exponential backoff for transient network errors only — never retry a charge without user intent
- log payment events with metadata only (order_id, status, provider_event_id) — zero card data

### 2026: Modern Payment Paradigms

#### Stripe Dynamic Payment Methods
- Configure "automatic_payment_methods" with enabled set to true when creating the payment intent. Avoid passing hardcoded lists of payment method types in the backend request.
- This allows the payment elements UI to render and prioritize available payment methods (cards, BNPL, bank transfers) dynamically based on client location, currency, and dashboard settings.

#### Buy Now Pay Later (BNPL) messaging
- Integrate BNPL messaging elements (e.g., "stripe-payment-method-messaging" or equivalent provider widget) early in the purchase funnel, such as on the product detail and cart pages.
- Pass the item price, currency, and consumer country dynamically to the element to display accurate Klarna/Affirm payment split calculations (e.g., "4 payments of $25").

#### Account-to-Account (A2A) Pay by Bank
- Use bank-to-bank direct rails (such as TrueLayer, Plaid, or Stripe Pay by Bank) to lower card processing fees.
- Account for slow-settling transactions by managing intermediate status webhooks (e.g., "processing", "pending", and "settled") in the database state machine. Keep order state as payment pending and lock inventory with a TTL while waiting for bank settlement.

#### Programmatic Agent Payments (x402 / MPP)
- For machine-to-machine or autonomous AI agent checkouts, avoid interactive frontend redirects.
- Respond to unauthorized agent requests with an HTTP 402 Payment Required status code, accompanied by payment headers containing the payment link, provider details, or link headers.
- Support programmatic card and A2A billing via Stripe Machine Payments Protocol (MPP) or SetupIntents configured with "setup_future_usage" set to "off_session" to charge stored methods programmatically.

### 5. Test and Validate

- run against provider sandbox with documented test card numbers
- verify webhook delivery end-to-end (use provider dashboard or a tool like Stripe CLI)
- confirm idempotency: replay a webhook event; verify the order is not double-updated
- confirm no sensitive data appears in logs or error responses

## Checklist

- [ ] provider SDK installed and version pinned
- [ ] all credentials in env vars — not in source code
- [ ] idempotency keys used for charge and capture calls
- [ ] webhook signature validation implemented before processing events
- [ ] error codes mapped to safe user-facing messages
- [ ] refund flow implemented with audit trail
- [ ] no card numbers, CVV, or PAN in logs or API responses
- [ ] sandbox tested end-to-end including failure cases
- [ ] webhook replay tested for idempotency
- [ ] dynamic payment methods enabled ("automatic_payment_methods" set to true)
- [ ] BNPL promotional messaging elements integrated on product detail and cart pages
- [ ] A2A bank settlement flow webhook states handled dynamically with inventory TTL locks
- [ ] HTTP 402/MPP programmatic checkout path supported and tested for non-interactive agent payments

## Output Contracts

When the payment integration is consumed by storefront, checkout, or
fulfillment agents, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the gateway endpoints, the request/response shapes, and the auth requirements.
- **`contracts/schemas/edge-deployment-spec.json`** when the integration is part of a coordinated deploy handoff.

Skip emission for local sandbox experiments that do not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a payment payload may try to reframe the order's amount or merchant. Validate against the declared cart and the merchant allowlist.
- **ASI03 Identity & Privilege Abuse**: payment endpoints must enforce authn/authz; reject anonymous or unscoped payment calls.
- **ASI05 RCE Guard**: never construct payment payloads, webhooks, or signing inputs from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the gateway contract is consumed by storefront and checkout agents; emit a structured spec so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the integration as "PCI-compliant" without a real audit; surface the actual scope and the residual risk.

## Related Skills

- **handle-checkout-flow**: Orchestrate the full cart-to-confirmation flow that calls this skill
- **manage-order-fulfillment**: Update order status after payment confirmation
- **manage-secrets**: Rotate or audit gateway API keys
- **security-audit**: Review payment integration for PCI exposure
- **add-api-endpoint**: Scaffold the payment and webhook controller endpoints
- **configure-agent-commerce**: Implement x402 HTTP billing, MPP endpoints, and agent commerce registration
