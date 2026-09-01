---
name: handle-checkout-flow
description: Design and implement the end-to-end checkout flow including cart management, tax and shipping calculation, discount/coupon application, and order confirmation. Use when building or fixing any step in the purchase funnel from cart to payment confirmation.
---

# Handle Checkout Flow

Use this skill when the task involves building, extending, or debugging the steps a customer takes from adding an item to cart through to receiving an order confirmation.

## When to Use

- building/fixing the purchase funnel
- cart, tax/shipping, discount/coupon logic
- order confirmation step
- end-to-end checkout from cart to payment

## Core Rules

- **Zero Client-Trust Pricing**: recalculate all line items, discounts, taxes, and shipping server-side immediately before creating the payment intent — discard any client-submitted monetary amounts
- **PCI DSS v4.0.1 Script Integrity** (req 6.4.3): all JavaScript executing on payment pages must be inventoried, justified, and loaded with **Subresource Integrity (SRI) hashes** and a strict **CSP nonce** (`script-src 'nonce-...'`)
- **Tamper Detection** (req 11.6.1): an automated mechanism must monitor payment page HTTP headers and client-side scripts at least weekly (or continuously) to detect unauthorized modifications (Magecart/formjacking)
- validate inventory availability at checkout submission time, not only at add-to-cart time; use **two-phase atomic hold** (soft reserve with TTL → hard commit on payment success / release on failure)
- apply discounts and promotions server-side only; wrap coupon validation and usage increment in an **atomic transaction with row-level lock** (`SELECT ... FOR UPDATE`) to prevent TOCTOU race conditions under concurrent requests
- ensure checkout submission is idempotent: use idempotency keys on payment intent creation; submitting an order twice must not produce two charges
- protect guest checkout with **cryptographically signed HMAC tokens** — not plain session IDs; enforce strict BOLA checks so each cart/order is accessible only to its owning session or user
- support **EMV 3DS 2.3.1** with 100+ context attributes for frictionless risk-based authentication (\> 85% challenge-free); integrate SCA exemption engine (Low-Value, TRA, Trusted Beneficiary)

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

## 2026 Agentic Checkout Patterns

### 2026: Agentic Checkout Architecture

Agentic Checkout enables AI agents to autonomously execute purchase transactions under the Agentic Commerce Protocol (ACP) and User Context Protocol (UCP):
- **Authorization & Limits**: Implement pre-authorization gates and spending limits per agent session or customer ID to control transactional risk.
- **Merchant of Record (MoR)**: Define clear MoR assignments to handle fraud liability, chargeback handling, and regional taxes for agentic transactions.
- **Programmatic Checkout**: Ensure the end-to-end checkout pipeline supports headless execution without interactive browser sessions, relying on standardized structured responses.

### 2026: Address Validation Lifecycle

Validating the shipping address is a mandatory, isolated step that must occur before tax calculation or shipping carrier requests:
- **API Standards**: Integrate Google Maps Address Validation, Loqate, or Smarty Streets APIs to standardize raw user inputs into verified, carrier-compliant address structures.
- **Error Handling**: Promptly catch validation errors (e.g., missing apartment number, invalid zip codes) and resolve them programmatically or reject with precise error subcodes.

### 2026: Stripe Tax Integration and Decision Tree

Selecting the correct tax calculation service depends on the merchant's scale, transaction volume, and operational context:
- **Stripe Tax**: Recommended for startups and mid-market merchants operating within the Stripe payment ecosystem who require quick integration.
- **TaxJar**: Ideal for multi-channel merchants (e.g., Shopify + Custom Web App) with moderate transaction volumes and standard ERP requirements.
- **Avalara AvaTax**: Designed for enterprise organizations with high transaction volumes, complex Nexus rules, custom ERP systems, and localized tax needs.

### 2026: Economic Nexus Threshold Monitoring

Merchants must actively track regional sales thresholds to ensure compliance with local tax registration laws:
- **Nexus Monitoring**: Track US state-by-state transaction count and sales volume thresholds programmatically.
- **Alerting**: Alert internal operations teams when approaching 80% of any state's economic nexus threshold (e.g., 200 transactions or $100,000 in sales) to trigger timely registration.

## Checklist

- [ ] cart totals recalculated server-side before every charge
- [ ] inventory availability re-validated at checkout submission
- [ ] coupon validation is server-side with usage limit enforcement
- [ ] tax and shipping calculated from confirmed shipping address
- [ ] checkout submission is idempotent (double-submit safe)
- [ ] inventory locked before charge, released on failure
- [ ] order confirmation and email sent after successful payment
- [ ] guest and authenticated paths tested independently
- [ ] agentic checkout spending limits and pre-authorization gates enforced
- [ ] address validation performed via verified API before tax/shipping calculations
- [ ] Stripe Tax, TaxJar, or Avalara chosen based on transaction volume and ERP needs
- [ ] economic nexus threshold monitoring and low-nexus alerts configured

## Output Contracts

When the checkout flow is consumed by storefront, payment, or fulfillment
agents, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the checkout endpoints, the request/response shapes, and the auth requirements.
- For human-readable reports, a markdown summary of the flow, the failure modes, and the rollback path.

Skip emission for single-checkout experiments that do not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a checkout request body may try to reframe the order's intent. Validate against the declared cart and pricing.
- **ASI03 Identity & Privilege Abuse**: checkout endpoints must enforce authn/authz; reject anonymous high-value actions.
- **ASI05 RCE Guard**: never construct pricing, tax, or payment payloads from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the checkout contract is consumed by storefront, payment, and fulfillment agents; emit a structured spec so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the flow as "secure" without the inventory hold and PCI scope review; surface the residual risk honestly.

## Related Skills

- **integrate-payment-gateway**: Process the final payment step in the checkout flow
- **manage-product-catalog**: Source product details, pricing, and inventory levels
- **manage-order-fulfillment**: Hand off the confirmed order for packing and shipping
- **add-ui-component**: Build the cart and checkout UI components
- **write-tests**: Write integration tests for the purchase funnel
