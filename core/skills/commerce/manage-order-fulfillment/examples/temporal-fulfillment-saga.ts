/**
 * Production Temporal Fulfillment Saga Workflow
 *
 * Implements:
 * - Orchestration-based Saga with explicit compensating activities
 * - Reverse compensation order (Shipping -> Inventory -> Payment)
 * - Deterministic event generation for event-sourced projections
 * - Vietnamese carrier label generation (GHN integration)
 */

export interface FulfillmentSagaInput {
  orderId: string;
  customerId: string;
  items: Array<{ sku: string; quantity: number }>;
  shippingAddress: {
    name: string;
    phone: string;
    address: string;
    wardCode: string;
    districtId: number;
  };
  totalAmountCents: number;
}

export interface InventoryAllocation {
  allocationId: string;
  orderId: string;
}

export interface ShippingLabel {
  trackingCode: string;
  carrierOrderCode: string;
  labelUrl: string;
}

// Workflow Activities Contract
export interface FulfillmentActivities {
  allocateInventory(orderId: string, items: Array<{ sku: string; quantity: number }>): Promise<InventoryAllocation>;
  releaseInventory(allocationId: string): Promise<void>;
  createGhnShippingOrder(input: FulfillmentSagaInput): Promise<ShippingLabel>;
  cancelGhnShippingOrder(carrierOrderCode: string): Promise<void>;
  capturePayment(orderId: string, amountCents: number): Promise<{ paymentId: string }>;
  refundPayment(paymentId: string, reason: string): Promise<void>;
  recordOrderEvent(orderId: string, eventType: string, payload: Record<string, unknown>): Promise<void>;
}

export async function fulfillmentSagaWorkflow(
  input: FulfillmentSagaInput,
  activities: FulfillmentActivities
): Promise<{ status: 'fulfilled' | 'compensated'; trackingCode?: string; error?: string }> {
  const compensations: Array<() => Promise<void>> = [];

  try {
    // Step 1: Capture Payment (or verify prior capture)
    await activities.recordOrderEvent(input.orderId, 'order_placed', { total: input.totalAmountCents });
    const payment = await activities.capturePayment(input.orderId, input.totalAmountCents);
    compensations.push(async () => {
      await activities.refundPayment(payment.paymentId, 'Fulfillment saga failure compensation');
      await activities.recordOrderEvent(input.orderId, 'payment_refunded', { paymentId: payment.paymentId });
    });

    // Step 2: Allocate Inventory
    const allocation = await activities.allocateInventory(input.orderId, input.items);
    compensations.push(async () => {
      await activities.releaseInventory(allocation.allocationId);
      await activities.recordOrderEvent(input.orderId, 'inventory_released', { allocationId: allocation.allocationId });
    });
    await activities.recordOrderEvent(input.orderId, 'inventory_allocated', { allocationId: allocation.allocationId });

    // Step 3: Generate Vietnamese Carrier Label (GHN)
    const shippingLabel = await activities.createGhnShippingOrder(input);
    compensations.push(async () => {
      await activities.cancelGhnShippingOrder(shippingLabel.carrierOrderCode);
      await activities.recordOrderEvent(input.orderId, 'shipping_cancelled', { code: shippingLabel.carrierOrderCode });
    });
    await activities.recordOrderEvent(input.orderId, 'carrier_dispatched', {
      carrier: 'GHN',
      trackingCode: shippingLabel.trackingCode,
    });

    return {
      status: 'fulfilled',
      trackingCode: shippingLabel.trackingCode,
    };
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : 'Unknown fulfillment failure';
    await activities.recordOrderEvent(input.orderId, 'fulfillment_failed', { error: errorMsg });

    // Execute compensations in strict reverse order
    while (compensations.length > 0) {
      const compensate = compensations.pop()!;
      try {
        await compensate();
      } catch (compErr) {
        console.error(`[CRITICAL] Compensation failed during rollback for ${input.orderId}:`, compErr);
      }
    }

    return {
      status: 'compensated',
      error: errorMsg,
    };
  }
}
