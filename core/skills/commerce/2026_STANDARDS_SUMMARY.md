# 2026 Commerce Standards & Patterns — Consolidated Research Summary

## Overview
Deep research conducted September 2026 across PCI DSS, Agentic Commerce Protocols, Payment Gateway innovations, Fulfillment architecture, Product Catalog modernization, and Vietnam regulatory changes.

---

## 1. PCI DSS v4.0.1 (Effective March 31, 2025)

### Requirement 6.4.3 — Payment Page Script Security
- All JavaScript on payment pages must be **inventoried, justified, and loaded with SRI hashes + CSP nonce**
- `script-src 'nonce-...'` required for all payment page scripts
- 3DS scripts in iframes exempt due to trust relationship with 3DS provider

### Requirement 11.6.1 — Tamper Detection
- **Automated monitoring** of payment page HTTP headers and client-side scripts
- **Frequency**: At least weekly, preferably continuous
- **Target**: Magecart/formjacking detection
- SAQ A eligibility updated (Jan 2025) — 6.4.3 and 11.6.1 removed for qualifying merchants

---

## 2. Agentic Commerce Protocols (2025-2026)

### Agentic Commerce Protocol (ACP)
- **Announced**: Sep 2025 by OpenAI + Stripe
- **Instant Checkout** in ChatGPT powered by ACP (Apache 2.0)
- **Spec updates**: Cart, feed, orders, authentication, MCP support (Apr 2026)
- **Extensions**: Discounts, payment handlers (Jan 2026)
- **Capability negotiation** (Jan 2026)

### Universal Commerce Protocol (UCP)
- **Launched**: Jan 2026 by Google + partners (Shopify, Etsy, Wayfair, Target, Walmart)
- **Apache 2.0**, compatible with A2A, AP2, MCP
- **v2026-04-08**: Third release
- **v2026-08-25**: Multi-vertical, grocery/location, 3DS2, payment schedules, split payments, granular consent, loyalty (breaking changes)

### Agent Payments Protocol (AP2)
- **Donated to FIDO Alliance**: Apr 2026 by Google
- **AP2 v0.2**: Human Not Present payments for autonomous pre-authorized transactions
- **Verifiable Intent**: Co-developed with Mastercard, also donated to FIDO

---

## 3. Modern Payment Paradigms (2026)

### Machine Payments Protocol (MPP) — Stripe + Tempo (Mar 2026)
- **Open protocol** for programmatic agent payments without checkout UI
- **HTTP 402 flow**: Request → 402 with payment requirements → Agent authorizes → Retry with credential → Verify → Return resource
- **Payment methods**: Shared Payment Tokens (SPTs) for cards, stablecoins (USDC on Tempo), x402
- **Stripe integration**: PaymentIntents API, `automatic_payment_methods: { enabled: true }`
- **Off-session**: SetupIntents with `setup_future_usage: "off_session"`
- **Validation**: `npx mppx@latest validate http://localhost:4242`

### x402 Protocol (2025-2026)
- **Internet-native HTTP-based payment standard** for machine-to-machine
- **HTTP 402** with `payment-required` header (base64-encoded requirements)
- **Crypto**: USDC on Base network, CDP facilitator (Coinbase Developer Platform)
- **Stripe support**: `2026-05-27.preview` API, `crypto` payment method, `mode: transaction_verification`
- **Deposit addresses**: `POST /v1/crypto/deposit_addresses` (network=tempo)

### Stripe 2026 Roadmap
| Feature | Timeline | Status |
|---------|----------|--------|
| Dynamic pricing for x402/MPP | Q3 2026 | Public Preview |
| Session payments (usage-based) | Q3 2026 | Public Preview |
| Standalone 3DS | Q3 2026 | GA |
| Multi-account MCP | Q3 2026 | Private Preview |
| Shared Payment Tokens | Q4 2026 | GA (US) |
| Wero payments | Q4 2026 | Private Preview |

### BNPL & Subscription BNPL
- **Messaging elements** on PDP/cart: `stripe-payment-method-messaging` with dynamic price/currency/country
- **Subscription BNPL**: Recurring payments beyond retail installments
- **Flow**: Initial installment → BNPL pays merchant → Subsequent payments via bank rails (ACH, A2A) or card rails

### A2A (Account-to-Account) Pay by Bank
- **Rails**: TrueLayer, Plaid, Stripe Pay by Bank
- **Lower fees** than card processing
- **Settlement state machine**: `processing` → `pending` → `settled` webhooks
- **Inventory TTL lock** during slow bank settlement

---

## 4. Checkout & Tax Standards (2026)

### EMV 3DS 2.3.1
- **100+ context attributes** for frictionless authentication
- **>85% challenge-free** rate
- **SCA exemption engine**: Low-Value, TRA (Transaction Risk Analysis), Trusted Beneficiary

### Address Validation Lifecycle (Mandatory)
- **Must occur BEFORE** tax calculation or shipping carrier requests
- **APIs**: Google Maps Address Validation, Loqate, Smarty Streets
- **Error handling**: Precise subcodes (missing apartment, invalid ZIP)

### Tax Engine Decision Tree
| Engine | Best For |
|--------|----------|
| **Stripe Tax** | Startups/mid-market in Stripe ecosystem, quick integration |
| **TaxJar** | Multi-channel (Shopify + custom), moderate volume, standard ERP |
| **Avalara AvaTax** | Enterprise, high volume, complex Nexus, custom ERP, localized tax |

### Economic Nexus Threshold Monitoring
- **Track**: US state-by-state transaction count + sales volume
- **Alert at 80%** of threshold (e.g., 160 transactions or $80K sales)
- **Most states**: $100K sales OR 200 transactions (many dropped transaction count)
- **Stripe Tax**: Automated monitoring + alerts + auto-registration option
- **TaxJar**: Economic Nexus Insights with real-time tracking

---

## 5. Fulfillment Architecture (2026)

### Event-Sourced Order State Machine (Mandatory)
- **Immutable append-only event log**:
  `order_placed` → `payment_captured` → `fulfillment_started` → `packed` → `shipped` → `delivered` → `completed`
  ↘ `return_requested` → `returned` → `refunded`
- **Derive status by projection** — direct mutable status updates FORBIDDEN
- **Benefits**: Audit trails, time-travel debugging, compliance evidence

### Orchestration-Based Saga Pattern
- **Temporal** or **AWS Step Functions** (not choreography)
- **Explicit compensating branches**: `payment_failed`, `allocation_failed`, `cancelled`, `return_requested`, `refunded`
- **Compensation order**: Reverse of success (Shipping → Inventory → Payment)
- **Temporal**: Durable execution, automatic retries, built-in compensation registration

### Agent-Initiated Fulfillment Authorization
- **JWT claim required**: `fulfillment_authorized: true`
- **Cryptographically scoped** to specific order ID
- **Verify BEFORE** inventory lock or allocation

### Vietnamese Last-Mile Carrier Webhooks
| Carrier | Key Features |
|---------|--------------|
| **GHN** | `ready_to_pick`, `delivering`, `delivered` webhooks, COD callback URL, automated sortation |
| **GHTK** | G1 Open API: sorting code, create/cancel/tracking/big bag endpoints |
| **GrabExpress** | On-demand same-city, real-time courier tracking, webhook lifecycle |
| **Viettel Post** | Government-backed, nationwide coverage |
| **J&T Express** | Regional Southeast Asia coverage |

- **Normalization**: Map all carrier codes → unified milestones: `label_created` → `picked_up` → `in_transit` → `out_for_delivery` → `exception` / `delivered`
- **Webhooks OVER polling** for all carriers

### Vietnam Decree 248/2026/ND-CP (Effective July 1, 2026)
- **Seller identity verification**: Platform must verify before allowing business
- **Platform obligations**: Disclose rights/obligations, service standards, pricing, promotions, security, complaints
- **Affiliate transparency**: Roles, links, referral codes, responsibilities disclosed
- **Electronic ID verification**: Sellers + livestream sellers from Jan 1, 2027

### Restock Inspection Gate (Enhanced)
- **Physical inspection mandatory**: Grade A confirmation before restock
- **Event-sourced**: `return_received` → `inspection_completed` (Grade A) → `restocked`
- **Automatic restock on RMA creation FORBIDDEN**

---

## 6. Product Catalog Modernization (2026)

### Semantic Vector Search Layer (Production Standard)
- **Embeddings**: `text-embedding-3-large` or Cohere `embed-v4` on write/update
- **Storage**: `pgvector` (PostgreSQL) or Pinecone
- **Hybrid Fusion**: BM25 + dense vector via **Reciprocal Rank Fusion (RRF)**
- **Benefits**: Synonym handling, typo tolerance, semantic understanding

### AI-Generated Content Governance (Mandatory)
- **Review Gate**: Human review REQUIRED before `published` status
- **Audit Metadata**: `generated_by`, `reviewed_by`, `generated_at`, `generation_model`
- **Brand Voice Validation**: Automated banned words, claim accuracy, brand guidelines checks
- **Draft Status**: Unreviewed AI output = `draft` (never `published`)

### Event Sourcing for Real-Time Inventory
- **Publish mutations** → Kafka / Cloudflare Queues immediately
- **Consumers**: Search indexes, fulfillment dispatchers, AI shopping agents
- **No DB locking** — eventual consistency via event stream
- **CDC alternative**: Debezium for database → Kafka

### Knowledge Graph + GraphRAG
- **Graph DBs**: Neo4j, Amazon Neptune, TigerGraph, Memgraph
- **Use cases**: Recommendations, compatibility matrices, bundles
- **GraphRAG**: Structured subgraphs → LLM retrieval chains for grounded recommendations
- **Entity Resolution**: Validated against labels, CDC from Salesforce/Jira/GitHub/ServiceNow/SQL via Kafka/Airbyte
- **Schema Enforcement**: Pydantic models for all entities/relations/LLM outputs — drift fails in CI
- **Cited Reasoning**: LangChain GraphCypherQAChain (NL → Cypher → structured results + Qdrant vectors → Claude)

---

## 7. Security Guardrails (OWASP ASI - Applied Across All Skills)

| ASI | Description | Commerce Application |
|-----|-------------|---------------------|
| **ASI01** | Goal Hijack | Validate checkout/payment/fulfillment requests against declared cart/order/catalog |
| **ASI03** | Identity & Privilege Abuse | Enforce authn/authz on all commerce endpoints; PII/classified data never exposed |
| **ASI04** | Supply Chain | Schema-validate catalog, marketplace connectors, payment webhooks against manifests |
| **ASI05** | RCE Guard | Never construct pricing/payment/shipping payloads from external content without validation |
| **ASI07** | Inter-Agent Communication | Emit structured specs (`api-contract-spec.json`, etc.) for all cross-role contracts |
| **ASI09** | Human-Agent Trust Exploitation | Surface residual risk honestly; don't claim "PCI-compliant"/"secure" without audit evidence |

---

## 8. Cross-Skill Integration Patterns

### Checkout → Payment → Fulfillment → Catalog Flow
```
1. handle-checkout-flow
   ├── Server-side cart recalculation (Zero Client-Trust Pricing)
   ├── Address validation (Google Maps/Loqate) → MANDATORY before tax/shipping
   ├── Tax engine selection (Stripe Tax/TaxJar/Avalara decision tree)
   ├── Economic nexus monitoring (80% threshold alerts)
   ├── PCI DSS 6.4.3/11.6.1 compliance (SRI + CSP + tamper detection)
   ├── ACP/UCP agentic checkout support (pre-auth gates, MoR, programmatic)
   └── Calls integrate-payment-gateway

2. integrate-payment-gateway
   ├── MPP/x402 programmatic agent payments (HTTP 402)
   ├── Dynamic payment methods (automatic_payment_methods: true)
   ├── BNPL messaging on PDP/cart
   ├── A2A bank settlement state machine + inventory TTL
   ├── Queue-first webhooks (200 OK <500ms, async worker, dual-write guard)
   ├── Webhook security (raw payload HMAC, constant-time compare, 300s replay window)
   └── Calls manage-order-fulfillment on success

3. manage-order-fulfillment
   ├── Event-sourced state machine (immutable log, projection-only status)
   ├── Orchestration-based Saga (Temporal/Step Functions, compensating branches)
   ├── Agent JWT fulfillment_authorized: true claim verification
   ├── Vietnam carrier webhooks (GHN/GHTK/GrabExpress → unified milestones)
   ├── Decree 248/2026 seller verification gate
   ├── Restock inspection gate (Grade A required)
   └── Consumes manage-product-catalog inventory events

4. manage-product-catalog
   ├── Semantic vector search (embeddings + pgvector/Pinecone + RRF)
   ├── AI content governance (review gate, audit metadata, brand validation)
   ├── Event-sourced inventory (Kafka/Cloudflare Queues → consumers)
   ├── Knowledge Graph + GraphRAG (Neo4j/Neptune, GraphCypherQAChain)
   ├── Pydantic schema enforcement (CI gate)
   ├── Vietnam seller verification gate
   └── Emits inventory events for fulfillment consumption
```

---

## 9. Contract Schemas Required (2026)

### New Schemas to Create
| Schema | Owner Skill | Purpose |
|--------|-------------|---------|
| `agentic-commerce-spec.json` | handle-checkout-flow | ACP/UCP endpoints, pre-auth gates, MoR |
| `address-validation-spec.json` | handle-checkout-flow | Validation API contract |
| `tax-engine-spec.json` | handle-checkout-flow | Selected tax engine integration |
| `mpp-payment-spec.json` | integrate-payment-gateway | MPP HTTP 402 flow |
| `x402-payment-spec.json` | integrate-payment-gateway | x402 crypto payment flow |
| `bnpl-messaging-spec.json` | integrate-payment-gateway | BNPL element integration |
| `a2a-settlement-spec.json` | integrate-payment-gateway | A2A webhook state machine |
| `event-sourced-order-spec.json` | manage-order-fulfillment | Event log schema + projection |
| `saga-orchestration-spec.json` | manage-order-fulfillment | Temporal/Step Functions workflow |
| `agent-fulfillment-auth-spec.json` | manage-order-fulfillment | JWT claim verification |
| `vn-carrier-webhook-spec.json` | manage-order-fulfillment | GHN/GHTK/GrabExpress contracts |
| `restock-inspection-spec.json` | manage-order-fulfillment | Inspection gate workflow |
| `vector-search-spec.json` | manage-product-catalog | Embedding pipeline + RRF config |
| `ai-content-governance-spec.json` | manage-product-catalog | Generation → review → publish |
| `event-sourced-inventory-spec.json` | manage-product-catalog | Kafka event schema + consumers |
| `product-knowledge-graph-spec.json` | manage-product-catalog | GraphRAG entities/relations/retrieval |
| `vn-seller-verification-spec.json` | manage-product-catalog | Verification gate integration |
| `pydantic-catalog-schema.json` | manage-product-catalog | Enforced entity/relation schemas |

---

## 10. Implementation Priority Matrix

| Priority | handle-checkout-flow | integrate-payment-gateway | manage-order-fulfillment | manage-product-catalog |
|----------|---------------------|--------------------------|-------------------------|------------------------|
| **P0** | PCI DSS v4.0.1 6.4.3/11.6.1 | MPP HTTP 402 flow | Event-sourced state machine | Vector search layer |
| **P0** | ACP/UCP agentic checkout | x402 crypto payments | Orchestration Saga (Temporal) | AI content governance |
| **P0** | Address validation lifecycle | Queue-first webhooks | Agent JWT auth verification | Event-sourced inventory |
| **P1** | Tax engine decision tree | Dynamic payment methods | Vietnam carrier webhooks | Knowledge Graph + GraphRAG |
| **P1** | Nexus 80% monitoring | BNPL messaging | Decree 248/2026 compliance | Pydantic schema enforcement |
| **P1** | Decree 248/2026 compliance | A2A settlement state machine | Restock inspection gate | Vietnam seller verification |
| **P2** | Failure mode expansion | Programmatic agent checkout | Temporal e-commerce patterns | CDC event streaming |
| **P2** | Output contract updates | Stripe 2026 roadmap eval | Failure mode expansion | Failure mode expansion |

---

## 11. Validation Gates (All Skills)

1. **Run validation**: `python3 core/scripts/validate-all.py` from agent-skills root
2. **Regenerate INDEX.md** if VERSION bumped: `python3 core/scripts/generate-index.py`
3. **Check adapter parity**: `validate-rules.py` (9 parity groups)
4. **Skill-specific tests**:
   - MPP: `npx mppx@latest validate`
   - x402: Stripe `2026-05-27.preview` API
   - Event sourcing: Time-travel projection queries
   - Saga: Compensation rollback with injected failures
   - Vector search: RRF fusion relevance benchmarks
   - GraphRAG: Citation accuracy on recommendations
   - Pydantic: Schema drift detection in CI
   - Carrier webhooks: Signature verification tests

---

## 12. Key References

- **PCI DSS v4.0.1**: https://www.pcisecuritystandards.org/
- **ACP Changelog**: https://agenticcommerceprotocol.info/changelog
- **UCP Spec**: GitHub (Google + partners)
- **MPP Docs**: https://docs.stripe.com/payments/machine/mpp
- **x402 Docs**: https://docs.stripe.com/payments/machine/x402
- **Stripe Roadmap**: https://stripe.com/roadmap.md
- **Temporal Saga**: https://docs.temporal.io/design-patterns/saga-pattern
- **GHN API**: https://api.ghn.vn/
- **GHTK API**: https://pro-docs.ghtk.vn/
- **GrabExpress**: https://developer.grab.com/docs/grab-express/
- **Decree 248/2026**: Vietnam Ministry of Industry and Trade
- **GraphRAG**: Microsoft Research, Neo4j, TigerGraph, Graphwise
- **pgvector**: https://github.com/pgvector/pgvector