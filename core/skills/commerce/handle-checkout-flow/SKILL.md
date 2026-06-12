---
name: handle-checkout-flow
description: Design and implement the end-to-end checkout flow including cart management, tax and shipping calculation, discount/coupon application, and order confirmation. Use when building or fixing any step in the purchase funnel from cart to payment confirmation.
---

# Handle Checkout Flow

Use this skill when the task involves building, extending, or debugging the steps a customer takes from adding an item to cart through to receiving an order confirmation.

## Core Rules

- treat cart state as eventually consistent — never trust client-side totals for final billing; always recalculate server-side before charge
- validate inventory availability at checkout time, not only at add-to-cart time
- apply discounts and promotions server-side only; never trust coupon validation from the client
- ensure the checkout flow is idempotent: submitting an order twice must not produce two charges
- protect guest checkout and authenticated checkout paths equally — no security shortcuts for guest sessions

## Suggested Process

### 1. Map the Checkout Steps

Define the full funnel before building:

- cart review → shipping address → shipping method selection → discount/coupon → payment → order confirmation
- identify which steps are required vs skippable (e.g., digital goods skip shipping)
- confirm whether guest checkout is supported alongside authenticated checkout

### 2. Implement Cart State Management

- store cart in session (guest) or database (authenticated), syncing on authentication
- calculate line-item totals, subtotal, and item weight server-side
- handle out-of-stock and quantity changes gracefully with clear user messaging

### 3. Implement Tax and Shipping Calculation

- integrate a tax engine (TaxJar, Avalara, or manual rules) to calculate jurisdiction-based tax on the final shipping address
- call shipping carrier APIs (or flat-rate rules) to present shipping options and costs
- recalculate totals whenever address or shipping method changes

### 4. Implement Discount and Coupon Logic

- validate coupons server-side: check code existence, validity window, usage limits, minimum order value, and applicable SKUs
- apply discounts in a defined precedence order (e.g., item discount → coupon → loyalty points)
- display applied discount breakdown clearly before final payment

### 5. Finalize Order and Confirm Payment

- lock inventory at order-creation time (before charging)
- call `integrate-payment-gateway` to process payment
- on success: persist the confirmed order, release inventory lock, send confirmation email, and redirect to confirmation page
- on failure: release inventory lock, surface payment error, allow retry without re-entering non-payment data

## Checklist

- [ ] cart totals recalculated server-side before every charge
- [ ] inventory availability re-validated at checkout submission
- [ ] coupon validation is server-side with usage limit enforcement
- [ ] tax and shipping calculated from confirmed shipping address
- [ ] checkout submission is idempotent (double-submit safe)
- [ ] inventory locked before charge, released on failure
- [ ] order confirmation and email sent after successful payment
- [ ] guest and authenticated paths tested independently

## Related Skills

- **integrate-payment-gateway**: Process the final payment step in the checkout flow
- **manage-product-catalog**: Source product details, pricing, and inventory levels
- **manage-order-fulfillment**: Hand off the confirmed order for packing and shipping
- **add-ui-component**: Build the cart and checkout UI components
- **write-tests**: Write integration tests for the purchase funnel
