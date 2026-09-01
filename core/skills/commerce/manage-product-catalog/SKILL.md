---
name: manage-product-catalog
description: Build or maintain a product catalog including product creation, variant management (size, color, SKU), pricing, and inventory synchronization across channels. Use when adding, updating, or structuring product data in an e-commerce system.
---

# Manage Product Catalog

Use this skill when the task involves designing the data model or implementing the CRUD operations for products, product variants, categories, pricing, and stock levels in an e-commerce context.

## When to Use

- adding or updating product data
- variant management (size, color, SKU)
- pricing or inventory sync across channels
- structuring catalog data

## Core Rules

- every sellable unit must have a unique SKU enforced at the **database constraint level**; never allow duplicate SKUs within the same catalog
- pricing changes must be versioned or timestamped — store `price`, `compare_at_price`, `effective_from`, and `effective_until`; never silently overwrite historical prices
- inventory counts are `confidential` data; do not expose raw warehouse stock levels to unauthenticated clients
- **Two-Phase Atomic Inventory Hold**: use atomic conditional SQL (`UPDATE inventory SET available = available - X, reserved = reserved + X WHERE available >= X`) or Redis Lua scripts with a TTL; convert reserved hold to hard commit on payment success; release via background sweeper on TTL expiry or payment failure — never naive read-then-write sequences
- **Optimistic Concurrency Control (OCC)**: reject stale out-of-order inventory updates using version stamps (`version`, `ETag`, or vector clocks) to prevent overselling under concurrent channel sync
- **Channel Safety Buffers**: when syncing to external marketplaces (Shopee, Lazada, TikTok Shop, Amazon), deduct dynamic virtual safety stock buffers (e.g., 5% or minimum 3 units) before publishing available quantities — never broadcast 100% of available stock
- use **CDC event streaming** (Debezium / Kafka) to broadcast real-time stock changes to downstream channels; prefer push events over polling for inventory sync
- product data changes that affect live checkout (price, availability) must go through an approval or review step before publishing; **AI-generated product content** requires a mandatory human-review gate before status is set to published
- treat inventory counts as confidential data; never expose raw warehouse stock levels to unauthenticated clients; classify with `data-classification.yaml` (OWASP ASI03)
- every catalog write must be schema-validated against the active product schema; reject schema-drifted entries to prevent downstream agent desync (OWASP ASI04)
- when AI tools generate product descriptions, track `generated_by`, `reviewed_by`, `generated_at`, and `generation_model`; treat unreviewed AI output as drafts (OWASP ASI09)

## Output Contracts

When the catalog change is consumed by a storefront, a marketplace sync, or a
downstream analytics system, emit:

- **`contracts/schemas/api-contract-spec.json`** describing the catalog entity shape, the variant structure, and the inventory model. The consuming agent can then validate before publishing.
- **`contracts/schemas/deployment-plan.json`** when the catalog change is part of a coordinated multi-role rollout (e.g., a price update tied to a checkout flow change).
- For human-readable reports, a markdown diff of the affected SKUs and the rationale.

Skip emission for read-only catalog queries that do not cross a role boundary.

## Failure Modes

- **Duplicate SKU**: a SKU collision is created at the application layer. Mitigation: enforce SKU uniqueness at the database constraint level; reject duplicate inserts.
- **Silent price overwrite**: a price change overwrites historical prices without a version or timestamp. Mitigation: store `price`, `compare_at_price`, `effective_from`, and `effective_until`; never silently overwrite.
- **Inventory oversell under concurrency**: two channels decrement the same stock in parallel and oversell. Mitigation: use Two-Phase Atomic Inventory Hold (atomic SQL or Redis Lua) with TTL; reject naive read-then-write sequences.
- **OCC version drift**: a stale inventory update overwrites a newer one. Mitigation: enforce Optimistic Concurrency Control via `version`/`ETag`; reject stale updates.
- **Channel over-broadcast**: 100% of available stock is published to external marketplaces, allowing oversell from marketplace surges. Mitigation: apply dynamic virtual safety stock buffers (5% or minimum 3 units) before publishing.
- **AI content published unreviewed**: an AI-generated product description is set to `published` without a human review gate. Mitigation: enforce the review gate; track `reviewed_by` and `reviewed_at`; treat unreviewed AI output as drafts.
- **Inventory leaked**: raw warehouse stock levels are exposed to unauthenticated clients. Mitigation: classify inventory as confidential; expose `is_in_stock` (a computed boolean) rather than raw counts.
- **Sync duplicate**: an idempotent upsert is missing, causing duplicates on re-run. Mitigation: implement upsert by SKU; log sync run counts (created, updated, failed).

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a catalog update may try to reframe a product's category or compliance status. Cross-check the update against the source-of-truth catalog; reject off-spec edits.
- **ASI03 Identity & Privilege Abuse**: inventory counts and pricing are confidential; never expose raw values to unauthenticated clients; expose computed booleans only.
- **ASI04 Supply Chain**: the catalog schema and any external marketplace connector must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI07 Inter-Agent Communication**: the catalog contract is consumed by storefront, marketplace, and analytics agents; emit a structured spec so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present AI-generated product copy as "ready to publish" without a human review gate; surface the AI provenance and the reviewer.

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

## 2026 Catalog Architecture Patterns

### 2026: Semantic Vector Search Layer

Modern catalogs utilize a semantic vector search layer alongside traditional keyword search to improve product discovery:
- **Embedding Generation**: Generate high-dimensional vector embeddings for product titles and descriptions on write/update operations using models like `text-embedding-3-large` or Cohere `embed-v4`.
- **Vector Storage**: Store and index these embeddings in vector databases or extensions such as `pgvector` or Pinecone.
- **Hybrid Search Fusion**: Combine keyword-based search (BM25) and dense vector search results using Reciprocal Rank Fusion (RRF) to provide highly accurate, contextual search results.

### 2026: AI-Generated Product Content Governance

Automated generation of product copy and metadata requires strict quality gates to preserve brand integrity and accuracy:
- **Review Gate**: Impose a mandatory human-review gate before setting the status of any AI-generated product description to published.
- **Audit Metadata**: Track content generation lineage by saving audit fields: `generated_by`, `reviewed_by`, `generated_at`, and `generation_model`.
- **Brand Voice Validation**: Run automated checks for compliance with brand guidelines, banned words, and product claim accuracy prior to review.

### 2026: Event Sourcing for Real-Time Inventory

Decouple inventory updates from catalog writes using asynchronous event-driven state mutation:
- **Publish Mutations**: Publish all inventory adjustments and reservations immediately to messaging systems like Apache Kafka or Cloudflare Queues.
- **Consumer Processing**: Let downstream catalog search indexes, fulfillment dispatchers, and external AI shopping agents consume these updates to ensure eventual consistency without database locking.

### 2026: Knowledge Graph for Product Relationships

Utilize graphical data models to capture and traverse complex product relationships and user behaviors:
- **Graph Databases**: Model recommendations, compatibility matrices, and bundles using graph databases such as Neo4j or Amazon Neptune.
- **GraphRAG Pattern**: Feed structured subgraphs into LLM retrieval chains (GraphRAG) to ground automated customer recommendations in verifiable catalog relationships.

## Checklist

- [ ] SKU uniqueness enforced at database level
- [ ] variant-level inventory tracked separately from product level
- [ ] stock decrement operations are atomic (transaction-safe)
- [ ] pricing stored with version or effective timestamp
- [ ] `is_in_stock` computed server-side, not client-side
- [ ] product publish/unpublish guarded by review or approval step
- [ ] catalog sync is idempotent by SKU if external source is used
- [ ] low-stock alerting threshold configured for ops team
- [ ] semantic vector embeddings generated and stored on product write
- [ ] hybrid search (BM25 and dense vectors) combined using RRF fusion
- [ ] AI-generated product content audited and verified by human-review gate
- [ ] inventory updates published via Kafka or Cloudflare Queues
- [ ] product knowledge graph structured to drive Recommendations/GraphRAG

## Related Skills

- **handle-checkout-flow**: Consumes product and stock data during checkout
- **manage-order-fulfillment**: Decrements inventory when an order ships
- **build-data-pipeline**: Synchronize product data from ERP, supplier feeds, or PIM systems
- **add-api-endpoint**: Expose catalog CRUD endpoints for admin and storefront consumers
- **database-maintenance**: Maintain catalog indexes and handle bulk data operations
