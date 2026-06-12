---
name: manage-product-catalog
description: Build or maintain a product catalog including product creation, variant management (size, color, SKU), pricing, and inventory synchronization across channels. Use when adding, updating, or structuring product data in an e-commerce system.
---

# Manage Product Catalog

Use this skill when the task involves designing the data model or implementing the CRUD operations for products, product variants, categories, pricing, and stock levels in an e-commerce context.

## Core Rules

- every sellable unit must have a unique SKU; never allow duplicate SKUs within the same catalog
- pricing changes must be versioned or timestamped — do not silently overwrite historical prices
- inventory counts are `confidential` data; do not expose raw warehouse stock levels to unauthenticated clients
- stock level decrements must be atomic operations to prevent overselling under concurrent load
- product data changes that affect live checkout (price, availability) must go through an approval or review step before publishing

## Suggested Process

### 1. Define the Product Data Model

Clarify before building:

- what are the product types (simple, configurable/variant, bundle, digital)?
- which attributes are shared across variants (description, images) vs variant-specific (price, SKU, weight, stock)?
- what category taxonomy structure is required (flat list, nested tree)?
- what pricing model applies (fixed, tiered, time-limited sale)?

### 2. Implement Product and Variant Structure

- create a `Product` entity with shared fields: name, description, slug, images, category, status
- create a `ProductVariant` entity with: SKU, price, compare-at price, weight, stock quantity, and attribute options (e.g., `size: M`, `color: blue`)
- enforce uniqueness constraint on SKU at the database level
- generate URL-friendly slugs from product names; ensure uniqueness

### 3. Implement Inventory Management

- store `quantity_on_hand` per variant — never per product
- implement `reserve_stock(variant_id, qty)` and `release_stock(variant_id, qty)` as atomic transactions
- expose `is_in_stock` as a computed property: `quantity_on_hand - reserved_quantity > 0`
- implement a low-stock threshold alert mechanism for operations teams

### 4. Implement Pricing and Promotions Support

- store `price` and `compare_at_price` (strike-through) separately to support sale display
- support scheduled price changes with `effective_from` and `effective_until` timestamps
- never compute price purely on the client side; always resolve from the server

### 5. Implement Multi-channel Sync (when applicable)

- if syncing from an external source (POS, ERP, supplier feed), treat the external system as source of truth
- implement idempotent upsert by SKU to safely re-run sync without duplicating products
- log sync runs with counts of created, updated, and failed records

## Checklist

- [ ] SKU uniqueness enforced at database level
- [ ] variant-level inventory tracked separately from product level
- [ ] stock decrement operations are atomic (transaction-safe)
- [ ] pricing stored with version or effective timestamp
- [ ] `is_in_stock` computed server-side, not client-side
- [ ] product publish/unpublish guarded by review or approval step
- [ ] catalog sync is idempotent by SKU if external source is used
- [ ] low-stock alerting threshold configured for ops team

## Related Skills

- **handle-checkout-flow**: Consumes product and stock data during checkout
- **manage-order-fulfillment**: Decrements inventory when an order ships
- **build-data-pipeline**: Synchronize product data from ERP, supplier feeds, or PIM systems
- **add-api-endpoint**: Expose catalog CRUD endpoints for admin and storefront consumers
- **database-maintenance**: Maintain catalog indexes and handle bulk data operations
