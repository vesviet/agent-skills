# manage-order-fulfillment — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Event-Sourced Order State Machine (Mandatory 2026)
- **Immutable append-only event log**: `order_placed`, `payment_captured`, `fulfillment_started`, `packed`, `shipped`, `delivered`, `returned`
- **Derive current status** by projecting event stream — direct mutable status field updates FORBIDDEN
- **Enables**: reliable audit trails, time-travel debugging, compliance evidence

### Orchestration-Based Saga Pattern (Temporal / AWS Step Functions)
- **Replace choreography with orchestration**: explicit compensating branches (`payment_failed`, `allocation_failed`, `cancelled`, `return_requested`, `refunded`)
- **Temporal Workflow**: durable execution, automatic retries, built-in saga compensation registration
- **AWS Step Functions**: state machine with Lambda compensations for rollback
- **Compensation order**: reverse of success order (Shipping → Inventory → Payment)

### Agent-Initiated Fulfillment Authorization
- **JWT claim required**: `fulfillment_authorized: true` cryptographically scoped to specific order ID
- **Verify before**: locking inventory or executing allocation routines
- **Scope**: agent-specific, order-specific, time-limited

### Vietnamese Last-Mile Carrier Webhook Integrations
- **Primary carriers**: GHN (Giao Hang Nhanh), GHTK, Grab Express, Viettel Post, J&T Express
- **Webhook callbacks OVER polling**: secure callbacks for tracking events
- **Carrier status code normalization**: Map to unified internal milestones:
  - `label_created` → `picked_up` → `in_transit` → `out_for_delivery` → `exception` / `delivered`
- **GHN specifics**: `ready_to_pick`, `delivering`, `delivered` webhooks, COD callback URL for real-time COD status
- **GHTK specifics**: G1 Open API with sorting code, create order, cancel, tracking, big bag order endpoints
- **GrabExpress**: on-demand same-city courier, real-time courier tracking, webhook updates over delivery lifecycle

### Vietnam Decree 248/2026/ND-CP (Effective July 1, 2026)
- **Seller identity verification**: Platform operators must verify sellers before allowing business
- **Platform obligations**: Disclose rights/obligations, service standards, pricing, promotions, security, complaint handling
- **Affiliate marketing transparency**: All parties must disclose roles, links, referral codes, responsibilities
- **Electronic identity verification**: Required for sellers and livestream sellers from Jan 1, 2027

### Restock Inspection Gate (Enhanced)
- **Physical warehouse inspection mandatory**: Grade A confirmation before restock
- **Automatic restock on RMA creation FORBIDDEN**
- **Event-sourced**: `return_received` → `inspection_completed` (Grade A) → `restocked`

### Temporal E-Commerce Demo Patterns (2026)
- **No saga orchestrator**: checkout workflow IS the saga
- **No distributed transaction coordinator**: `updateWithStart` for atomic create-or-update
- **Declarative states**: transitions and guards in config, pure decider owns decisions
- **Derived UI steps**: `deriveStep()` maps prerequisites to wire-visible step
- **Price integrity**: stale `reviewedCartVersion` aborts with `CART_CHANGED`
- **Reservation management**: inventory reservations renewed at checkout start, released on timeout/cancellation, confirmed on success
- **Timeout**: `condition(() => complete, '1 hour')` auto-cancels stale checkouts, releases inventory

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Event-sourced state machine mentioned | **MANDATORY** immutable append-only event log, derive status by projection only |
| Saga pattern generic | **Orchestration-based Saga** with Temporal/AWS Step Functions, explicit compensating branches |
| Agent authorization mention | **JWT `fulfillment_authorized: true` claim** cryptographically scoped to order ID |
| Vietnamese carriers generic | **Specific carrier webhook integrations**: GHN, GHTK, GrabExpress with status code normalization |
| Restock inspection | **Enhanced**: physical inspection event required, Grade A confirmation, event-sourced |
| Vietnam compliance | **Decree 248/2026/ND-CP**: seller verification, platform obligations, affiliate transparency |

### 2. New 2026 Patterns to Add
- **Event-Sourced Fulfillment Architecture** with complete event list and projection logic
- **Temporal/AWS Step Functions Saga Orchestration** with compensation registration
- **Agent-Initiated Authorization** verification flow with JWT claim validation
- **Vietnamese Carrier Webhook Integration** with status code mapping table
- **Vietnam Decree 248/2026 Compliance** checklist for fulfillment operations
- **Restock Inspection Gate** as event-sourced workflow
- **Temporal E-Commerce Patterns** (declarative states, derived UI, price integrity, reservation management)

### 3. Checklist Additions
- [ ] Order state machine modeled as immutable append-only event log
- [ ] Current status derived by projecting event stream (no mutable status field)
- [ ] Orchestration-based Saga with Temporal or AWS Step Functions
- [ ] Explicit compensating branches for all failure modes
- [ ] Agent JWT contains `fulfillment_authorized: true` claim scoped to order ID
- [ ] Cryptographic verification of agent authorization before inventory allocation
- [ ] GHN webhook integration: `ready_to_pick`, `delivering`, `delivered`, COD callback
- [ ] GHTK webhook integration: G1 Open API endpoints, status normalization
- [ ] GrabExpress webhook integration: real-time courier tracking, delivery lifecycle
- [ ] Carrier status codes mapped to unified milestones (`label_created` → `delivered`)
- [ ] Vietnam Decree 248/2026: seller verification workflow in fulfillment
- [ ] Affiliate marketing transparency: roles, links, codes disclosed
- [ ] Restock inspection gate: `return_received` → `inspection_completed` (Grade A) → `restocked`
- [ ] Automatic restock on RMA creation forbidden
- [ ] Declarative state transitions with guards in configuration
- [ ] Price integrity: stale cart version aborts with `CART_CHANGED`
- [ ] Inventory reservation renewal at fulfillment start, TTL release on timeout
- [ ] Customer PII not in logs or non-admin API responses
- [ ] State change events emitted for downstream systems (warehouse, email, analytics)

### 4. Failure Mode Additions
- **Agent fulfillment spoofing**: Unauthorized agent triggers fulfillment → Mitigation: JWT `fulfillment_authorized: true` claim verification scoped to order ID
- **Event log corruption**: Direct status field update bypasses event sourcing → Mitigation: Database constraint forbidding direct status updates, audit trigger
- **Saga compensation failure**: Compensation action itself fails → Mitigation: Temporal durable retries, dead letter queue for manual intervention
- **Carrier webhook spoofing**: Fake delivery confirmation → Mitigation: Webhook signature verification (HMAC), carrier allowlist
- **Vietnam compliance gap**: Unverified seller ships order → Mitigation: Decree 248/2026 verification gate before fulfillment_started event
- **Restock without inspection**: Returned items added to sellable stock → Mitigation: Mandatory `inspection_completed` event with Grade A before `restocked`
- **Inventory double-allocation**: Two fulfillments for same order → Mitigation: Idempotency key on fulfillment call, event-sourced deduplication

### 5. Output Contract Updates
- Add `contracts/schemas/event-sourced-order-spec.json` for event log schema and projection
- Add `contracts/schemas/saga-orchestration-spec.json` for Temporal/Step Functions workflow definition
- Add `contracts/schemas/agent-fulfillment-auth-spec.json` for JWT claim verification
- Add `contracts/schemas/vn-carrier-webhook-spec.json` for GHN/GHTK/GrabExpress webhook contracts
- Add `contracts/schemas/restock-inspection-spec.json` for inspection gate workflow
- Update `contracts/schemas/api-contract-spec.json` with new fulfillment endpoints

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Convert to mandatory event-sourced state machine (immutable log, projection) | High |
| P0 | Add orchestration-based Saga with Temporal/AWS Step Functions | High |
| P0 | Add agent JWT `fulfillment_authorized: true` claim verification | High |
| P1 | Add Vietnamese carrier webhook integrations (GHN, GHTK, GrabExpress) | High |
| P1 | Add Vietnam Decree 248/2026 compliance gates | Medium |
| P1 | Enhance restock inspection gate with event-sourced workflow | Medium |
| P1 | Add Temporal e-commerce patterns (declarative states, price integrity) | Medium |
| P2 | Expand failure modes with 2026-specific scenarios | Low |
| P2 | Update output contracts for new specs | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root after edits
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test event sourcing projection logic with time-travel queries
- Test Saga compensation rollback with injected failures
- Test agent JWT claim verification with invalid/expired tokens
- Test carrier webhook signature verification