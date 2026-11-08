# Event-Sourced Order Fulfillment & Carrier Webhook Specifications (2026)

## 1. Event-Sourced Order State Machine

### 1.1 Append-Only Event Log Architecture
Direct mutable updates to order status (e.g., `UPDATE orders SET status = 'shipped'`) are strictly prohibited. Order state is modeled as an append-only stream of immutable events:
1. `order_placed`: Cart confirmed, preliminary reservation recorded.
2. `payment_captured`: Payment processor confirmed settlement.
3. `inventory_allocated`: Hard decrement on warehouse bins.
4. `fulfillment_started`: Picking list generated and dispatched.
5. `packed`: Box sealed, dimensions and weight verified.
6. `carrier_dispatched`: Handed off to carrier courier with tracking ID.
7. `in_transit`: Scanned at regional carrier sorting hub.
8. `out_for_delivery`: Loaded onto last-mile vehicle.
9. `delivery_confirmed`: Signed proof of delivery (POD) recorded.
10. `return_initiated` / `inspection_completed` / `restocked`: Controlled return lifecycle.

Current status is computed by applying a deterministic projection function over the event history:
$$\text{State}_N = \text{Fold}(\text{InitialState}, [E_1, E_2, \dots, E_N])$$

### 1.2 Warehouse Restock Inspection Gate
Returned merchandise must never be automatically restored to sellable inventory upon Return Merchandise Authorization (RMA) generation. The event stream requires:
$$\text{return\_received} \longrightarrow \text{inspection\_completed (Grade A confirmed)} \longrightarrow \text{restocked}$$
Merchandise graded below Grade A is routed to liquidation or refurbishment streams.

---

## 2. Orchestration-Based Saga Architecture (Temporal)

### 2.1 Forward Actions & Compensations
Distributed e-commerce fulfillment requires an orchestrator managing compensating transactions in strict reverse order:
- **Activity 1**: `AllocateInventory` $\longleftrightarrow$ **Compensating Activity**: `ReleaseInventoryAllocation`
- **Activity 2**: `GenerateCarrierLabel` $\longleftrightarrow$ **Compensating Activity**: `VoidCarrierLabel`
- **Activity 3**: `CapturePayment` $\longleftrightarrow$ **Compensating Activity**: `IssueStripeRefund`

If `GenerateCarrierLabel` encounters an unrecoverable routing error (e.g., remote province embargo), the Saga triggers compensations in reverse:
1. `VoidCarrierLabel` (if partially allocated).
2. `ReleaseInventoryAllocation` (restores stock immediately).
3. `IssueStripeRefund` (credits customer card).

---

## 3. Vietnamese Last-Mile Carrier Webhook Normalization

Carrier webhooks must be verified via HMAC signatures and mapped to normalized internal status milestones:

| Carrier | Raw Status Code | Normalized Milestone |
|---|---|---|
| **GHN** | `ready_to_pick` | `label_created` |
| **GHN** | `delivering` | `in_transit` |
| **GHN** | `delivered` | `delivery_confirmed` |
| **GHTK (G1)** | `1` (Chưa tiếp nhận) | `label_created` |
| **GHTK (G1)** | `3` (Đang lấy hàng) | `picked_up` |
| **GHTK (G1)** | `5` (Đang giao hàng) | `out_for_delivery` |
| **GHTK (G1)** | `6` (Đã giao hàng) | `delivery_confirmed` |
| **GrabExpress** | `ALLOCATING` | `label_created` |
| **GrabExpress** | `PICKED_UP` | `picked_up` |
| **GrabExpress** | `COMPLETED` | `delivery_confirmed` |
