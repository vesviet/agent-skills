# ACP & UCP Agentic Commerce Protocol Specifications (2026)

## 1. Protocol Architecture & Layering

Agentic commerce decouples tool orchestration, capability negotiation, payment settlement, and user delegation into four distinct architectural tiers:

```
┌────────────────────────────────────────────────────────┐
│   Tier 4: Delegation & Mandate (AP2 / FIDO Alliance)   │
│   - Cryptographic purchase authorization & user intent │
├────────────────────────────────────────────────────────┤
│   Tier 3: Discovery & Negotiation (UCP / ACP)          │
│   - Capability negotiation, product feed, cart saga    │
├────────────────────────────────────────────────────────┤
│   Tier 2: Machine Payment Settlement (x402 / MPP)      │
│   - HTTP 402, stablecoins (USDC/SOL) & card rails      │
├────────────────────────────────────────────────────────┤
│   Tier 1: Tool Execution & Discovery (MCP / AAIF)      │
│   - Model Context Protocol underlying transport        │
└────────────────────────────────────────────────────────┘
```

## 2. Universal Commerce Protocol (UCP v2026-08-25)

The Universal Commerce Protocol defines how AI agents discover merchant capabilities and execute programmatic checkout sessions without DOM scraping.

### 2.1 Capability Discovery (`/.well-known/ucp`)

Merchants host a signed JSON manifest at `/.well-known/ucp`:
- `spec_version`: Identifies supported UCP revisions (`"2026-08-25"`).
- `capabilities`: Explicit array of supported features (`cart_management`, `atomic_checkout`, `dynamic_pricing`, `delegated_authorization`).
- `endpoints`: Canonical URL endpoints for cart mutation, payment intent, and order status verification.
- `signing_keys`: JWKS endpoint or embedded public keys for validating merchant order receipts.

### 2.2 UCP Cart & Checkout Lifecycle

1. **Session Negotiation (`POST /ucp/v1/sessions`)**:
   Agent presents buyer credentials (agent DID and optional AP2 delegation token). Server issues `session_id` and ephemeral cart state.
2. **Item Synchronization (`PUT /ucp/v1/sessions/{id}/items`)**:
   Strict JSON Schema validation: `sku`, `quantity`, `unit_price_cents`, and buyer constraint bounds.
3. **Fulfillment Resolution (`POST /ucp/v1/sessions/{id}/shipping-methods`)**:
   Returns tax and shipping rate matrix computed deterministically based on shipping destination.
4. **Execution-Finality Check (`POST /ucp/v1/sessions/{id}/commit`)**:
   Validates total transaction value against the buyer's mandate spend cap before triggering settlement.

## 3. Agentic Commerce Protocol (ACP) Specification

The Agentic Commerce Protocol standardizes card-rail checkout via RESTful contracts:
- `POST /v1/checkout_sessions`: Creates an agent-driven checkout instance with structured line items and payment allowances.
- `POST /v1/agentic_commerce/delegate_payment`: Binds a Stripe Shared Payment Token (SPT) to the active session.
- **Strict Headers**:
  - `Idempotency-Key`: UUIDv4 ensuring zero double-charging on network retry.
  - `X-Agent-DID`: Cryptographic Decentralized Identifier of the calling autonomous system.

## 4. Machine Payments Protocol (MPP) & x402 V2 Header Invariants

For micro-transactions and machine-to-machine settlements:
- `402 Payment Required` challenge must supply:
  - Header: `PAYMENT-REQUIRED: scheme=x402; asset=USDC; network=base; amount=10000; pay_to=0x...; nonce=...`
  - Response Body: Complete JSON schema detailing settlement networks, decimals, and expiry timestamp.
- Client retry must provide:
  - Header: `PAYMENT-SIGNATURE: version=2; proof=...; nonce=...`
- Server verification:
  - Replay cache lookup (Redis NX TTL 3600s).
  - Signature validation against on-chain transaction or Stripe MPP verification API.
  - Emission of `PAYMENT-RESPONSE: status=settled; tx_hash=0x...; receipt_id=rcpt_...`
