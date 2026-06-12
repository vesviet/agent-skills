---
name: integrate-payment-gateway
description: Integrate or extend a payment gateway (Stripe, VNPay, PayPal, Momo, etc.) into an e-commerce application. Use when adding, replacing, or auditing a payment provider's checkout, refund, or webhook flow.
---

# Integrate Payment Gateway

Use this skill when a task requires connecting an application to a payment provider's API, including initial setup, webhook handling, refund flows, and PCI-DSS-compliant implementation.

## Core Rules

- never log, store, or return raw card numbers, CVV, or full PAN data — treat all card data as `restricted` per `core/policies/data-classification.yaml`
- always use the provider's official SDK or API client; do not hand-roll raw HTTP calls to payment endpoints
- handle idempotency keys for all charge/capture operations to prevent double-billing
- validate webhook signatures before processing any inbound event
- store only tokenized references (e.g., `customer_id`, `payment_method_id`) — never raw payment credentials

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

## Related Skills

- **handle-checkout-flow**: Orchestrate the full cart-to-confirmation flow that calls this skill
- **manage-order-fulfillment**: Update order status after payment confirmation
- **manage-secrets**: Rotate or audit gateway API keys
- **security-audit**: Review payment integration for PCI exposure
- **add-api-endpoint**: Scaffold the payment and webhook controller endpoints
