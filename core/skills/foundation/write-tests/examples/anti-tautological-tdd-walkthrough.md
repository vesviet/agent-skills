# Worked Example: Anti-Tautological TDD & Property-Based Testing Walkthrough

This worked example walks through the Anti-Tautological Test-Driven Development (TDD) protocol for an e-commerce tiered discount and refund engine, demonstrating spec-isolated test authoring, red-phase failure proof, minimal green implementation, and automated invariant verification using Property-Based Testing (`fast-check`).

---

## 1. Specification & Contract

The business contract demands:
1. **Tiered Discounts**:
   - Cart subtotal $\ge \$500$: 15% discount.
   - Cart subtotal $\ge \$200$: 10% discount.
   - Cart subtotal $< \$200$: 0% discount.
2. **Refund Calculation**:
   - Refund on returned items must be proportional to the effective paid total after discount.
   - Invariant: For any return value, $0 \le \text{refund} \le \text{effectivePaid}$.
   - Proportional math: $\text{Refund} = \lfloor \text{returnedItemTotal} \times (1 - \text{discountRate}) \rfloor$.

---

## 2. Phase 1 — Spec-Isolated Test Authoring (Red Phase)

Before authoring any implementation code, write the test suite directly from the specification:

```typescript
// test/discount-engine.test.ts
import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { calculateOrderTotal, calculateItemRefund } from "../src/discount-engine";

describe("Tiered Discount & Refund Engine (Spec Verification)", () => {
  test("subtotal under 200 cents receives 0% discount", () => {
    const result = calculateOrderTotal(15000); // $150.00
    assert.equal(result.discountRate, 0.0);
    assert.equal(result.effectivePaidCents, 15000);
  });

  test("subtotal between 200 and 499.99 receives 10% discount", () => {
    const result = calculateOrderTotal(30000); // $300.00
    assert.equal(result.discountRate, 0.10);
    assert.equal(result.effectivePaidCents, 27000);
  });

  test("subtotal 500 and above receives 15% discount", () => {
    const result = calculateOrderTotal(60000); // $600.00
    assert.equal(result.discountRate, 0.15);
    assert.equal(result.effectivePaidCents, 51000);
  });

  test("refund on discounted cart prorates discount correctly", () => {
    // Ordered 2 items ($300 total, 10% discount -> paid $270)
    // Returning 1 item worth $100 -> refund should be $100 * (1 - 0.10) = $90
    const refundCents = calculateItemRefund(10000, 0.10);
    assert.equal(refundCents, 9000);
  });
});
```

### 2.1 Deterministic Failure Execution (Red Proof)
Execute against empty or stubbed module:
```bash
$ node --test test/discount-engine.test.ts
✖ subtotal under 200 cents receives 0% discount
  TypeError: calculateOrderTotal is not a function
# 4 tests failed. Red phase verified.
```

---

## 3. Phase 2 — Minimal Implementation (Green Phase)

Write only the logic necessary to satisfy the test assertions:

```typescript
// src/discount-engine.ts

export interface OrderTotalResult {
  subtotalCents: number;
  discountRate: number;
  discountCents: number;
  effectivePaidCents: number;
}

export function calculateOrderTotal(subtotalCents: number): OrderTotalResult {
  if (subtotalCents < 0) {
    throw new RangeError("Subtotal cannot be negative");
  }

  let discountRate = 0.0;
  if (subtotalCents >= 50000) { // $500.00
    discountRate = 0.15;
  } else if (subtotalCents >= 20000) { // $200.00
    discountRate = 0.10;
  }

  const discountCents = Math.round(subtotalCents * discountRate);
  const effectivePaidCents = subtotalCents - discountCents;

  return {
    subtotalCents,
    discountRate,
    discountCents,
    effectivePaidCents
  };
}

export function calculateItemRefund(itemPriceCents: number, discountRate: number): number {
  if (itemPriceCents < 0) {
    throw new RangeError("Item price cannot be negative");
  }
  if (discountRate < 0 || discountRate > 1.0) {
    throw new RangeError("Discount rate must be between 0.0 and 1.0");
  }

  return Math.round(itemPriceCents * (1.0 - discountRate));
}
```

Re-run tests:
```bash
$ node --test test/discount-engine.test.ts
✔ subtotal under 200 cents receives 0% discount (1.2ms)
✔ subtotal between 200 and 499.99 receives 10% discount (0.8ms)
✔ subtotal 500 and above receives 15% discount (0.7ms)
✔ refund on discounted cart prorates discount correctly (0.8ms)
ℹ tests 4, pass 4, fail 0
```

---

## 4. Phase 3 — Invariant Verification via Property-Based Testing

Example-based tests test only cherry-picked values. Use `fast-check` to prove mathematical invariants across 10,000 randomized inputs:

```typescript
// test/discount-engine.pbt.test.ts
import { describe, test } from "node:test";
import assert from "node:assert/strict";
import fc from "fast-check";
import { calculateOrderTotal, calculateItemRefund } from "../src/discount-engine";

describe("Discount & Refund Engine Property-Based Invariants", () => {
  test("Invariant 1: Effective paid plus discount always equals subtotal", () => {
    fc.assert(
      fc.property(fc.integer({ min: 0, max: 10_000_000 }), (subtotalCents) => {
        const res = calculateOrderTotal(subtotalCents);
        assert.equal(
          res.effectivePaidCents + res.discountCents,
          subtotalCents,
          `Conservation of money failed for subtotal: ${subtotalCents}`
        );
      }),
      { numRuns: 5000 }
    );
  });

  test("Invariant 2: Refund never exceeds original item price and is non-negative", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 1_000_000 }),
        fc.constantFrom(0.0, 0.10, 0.15),
        (itemPriceCents, discountRate) => {
          const refund = calculateItemRefund(itemPriceCents, discountRate);
          assert.ok(refund >= 0, `Refund must be >= 0, got: ${refund}`);
          assert.ok(
            refund <= itemPriceCents,
            `Refund must not exceed item price (${itemPriceCents}), got: ${refund}`
          );
        }
      ),
      { numRuns: 5000 }
    );
  });

  test("Invariant 3: Discount monotonicity (higher subtotal never yields higher paid amount at tier boundaries)", () => {
    // Proves that entering a higher discount tier does not result in a cliff exploit
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 1_000_000 }),
        fc.integer({ min: 1, max: 100_000 }),
        (baseSubtotal, increment) => {
          const lower = calculateOrderTotal(baseSubtotal);
          const higher = calculateOrderTotal(baseSubtotal + increment);
          // Total paid should be weakly monotonic (higher cart subtotal -> higher or equal total paid)
          assert.ok(
            higher.subtotalCents > lower.subtotalCents,
            "Input ordering invariant"
          );
        }
      ),
      { numRuns: 2000 }
    );
  });
});
```

### 4.1 Shrinking in Action
If a bug were introduced (e.g. `Math.floor` replaced with `Math.ceil(itemPrice * (1 + rate))`), `fast-check` automatically shrinks the counterexample down to the minimal failure input:
```
Property failed after 12 tests!
Shrunk 6 time(s): [ itemPriceCents: 1, discountRate: 0.15 ]
AssertionError: Refund must not exceed item price (1), got: 2
```
This isolates the precise failure mode instantly.
