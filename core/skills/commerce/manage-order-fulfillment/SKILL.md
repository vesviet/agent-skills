---
name: manage-order-fulfillment
description: Implement and manage the post-purchase order lifecycle including order status management, packing, shipping label generation, carrier tracking, and refund or return processing. Use when building or maintaining fulfillment workflows after a successful payment.
---

# Manage Order Fulfillment

Use this skill when the task involves the operations and engineering required to move a confirmed order through packing, shipping, delivery tracking, and post-delivery actions (returns, refunds, exchanges).

## When to Use

- building post-purchase order lifecycle
- packing, shipping labels, carrier tracking
- refund or return processing
- fulfillment after successful payment

## Core Rules

- treat order data as `confidential` — customer PII (address, phone) must never appear in logs or public API responses
- order status transitions must follow a defined state machine; do not allow arbitrary status jumps (e.g., jumping from `pending` directly to `delivered` without `shipped`)
- refunds must always reference the original payment transaction ID — never issue a refund without a verified charge to reverse
- shipping label generation is an irreversible, billable action — confirm carrier and address before requesting a label
- inventory must be decremented only when an order is confirmed paid, not at cart reservation time (unless the business requires strict reservation)
- Ensure that agent-initiated fulfillment requests validate the agent JWT for a `fulfillment_authorized: true` claim scoped to the specific order ID.
- Avoid updating status fields directly; model state transitions as an immutable event log including `order_placed`, `payment_captured`, `fulfillment_started`, `shipped`, `delivered`, and `returned`.
- Prefer webhook callbacks over polling for last-mile Vietnamese carriers (Grab Express, GHN, GHTK) and map their status codes to internal event-sourced events.

## Suggested Process

### 1. Define the Order State Machine

Map the full lifecycle before implementing:

```
pending → processing → packed → shipped → delivered → completed
                                                    ↘ return_requested → refunded
pending → cancelled (only before shipped)
```

- enforce state transitions in code — reject invalid transitions with a clear error
- emit an event or webhook on each state change for downstream systems (warehouse, email, analytics)

### 2. Implement Order Processing

- on payment confirmation: create the order record, decrement inventory, send confirmation email
- assign the order to a fulfillment queue (warehouse team, 3PL, or automated picker)
- allow operations team to view and manage orders through an admin interface

### 3. Implement Shipping Label Generation

- integrate with a carrier API (e.g., EasyPost, Shippo, DHL API, GHTK for Vietnam) to generate shipping labels
- validate the shipping address before requesting a label (reduce carrier correction fees)
- store the label URL and tracking number against the order record
- mark order as `shipped` after label is generated and send tracking info to customer

### 4. Implement Carrier Tracking

- poll or subscribe to carrier tracking webhooks to receive delivery status updates
- map carrier status codes to internal order statuses (`in_transit`, `out_for_delivery`, `delivered`, `delivery_failed`)
- notify the customer at key tracking milestones (shipped, out for delivery, delivered)
- handle delivery failures: attempt re-delivery or route to returns flow

### 5. Implement Refund and Returns

- create a `ReturnRequest` with reason, items, and quantity
- validate the return eligibility: within return window, original order in `completed` or `delivered` state
- on approval: initiate refund via `integrate-payment-gateway` using original transaction ID
- update inventory when returned items are received and pass quality check
- emit a `refund_issued` event for accounting systems

### 2026: Agent Security, Event Sourcing, and Vietnamese Logistics

- **Agent-Initiated Authorization**: When fulfillment is triggered by an autonomous agent, verify that the agent's JWT contains the `fulfillment_authorized: true` claim. This claim must be cryptographically verified and scoped to the target order ID prior to locking inventory or executing allocation routines.
- **Event-Sourced State Transitions**: Transition away from mutable status-field updates. Maintain an immutable, append-only event-sourced log of order states:
  - `order_placed`
  - `payment_captured`
  - `fulfillment_started`
  - `shipped`
  - `delivered`
  - `returned`
  Compute the current status of any order dynamically by projecting the event stream.
- **Vietnamese Carrier Webhook Integrations**: When integrating with local last-mile carriers (such as Grab Express, GHN, or GHTK), use secure webhook callbacks instead of frequent polling. Map carrier-specific status codes (e.g., GHN's `ready_to_pick`, `delivering`, `delivered`) directly to the corresponding internal event-sourced events.

## Checklist

- [ ] order state machine defined and enforced in code
- [ ] invalid state transitions rejected with clear error messages
- [ ] inventory decremented atomically on payment confirmation
- [ ] shipping address validated before label generation
- [ ] tracking number stored per order and sent to customer
- [ ] refund always references original transaction ID
- [ ] return window eligibility checked before processing return
- [ ] customer PII not present in logs or non-admin API responses
- [ ] state change events emitted for downstream systems
- [ ] Agent JWT contains the `fulfillment_authorized: true` claim scoped to the specific order ID.
- [ ] Order status is modeled as an immutable, append-only event-sourced log.
- [ ] Vietnamese carrier (Grab Express, GHN, GHTK) tracking is driven by webhook callbacks.
- [ ] Carrier status codes are mapped to internal event-sourced order events.

## Related Skills

- **integrate-payment-gateway**: Issue refunds against original payment transactions
- **handle-checkout-flow**: Creates the order that this skill fulfills
- **manage-product-catalog**: Decrements inventory and restocks on returns
- **add-event-handler**: Handle carrier tracking webhooks and order state events
- **add-api-endpoint**: Expose fulfillment status and return endpoints
- **incident-report**: Escalate lost packages, carrier failures, and refund disputes
\n### 2026: Event-Sourced Fulfillment

- **Agent-initiated fulfillment:** When an AI agent places an order on behalf of a user (via ACP/UCP checkout), the fulfillment pipeline must validate the agent's authorization scope before allocating inventory. The agent's JWT must include a `fulfillment_authorized: true` claim scoped to the specific order ID.
- **Event-sourced order state:** Model order state transitions as an immutable event log (e.g., `order_placed`, `payment_captured`, `fulfillment_started`, `shipped`, `delivered`, `returned`). Derive current status from the event stream, never update a status field directly. This enables reliable audit trails and time-travel debugging.
- **Vietnamese carrier integration:** Grab Express, GHN (Giao Hang Nhanh), and GHTK are the primary last-mile carriers for Vietnam. Use their webhook callbacks for tracking events rather than polling. Map carrier status codes to your internal event-sourced order events.\n
