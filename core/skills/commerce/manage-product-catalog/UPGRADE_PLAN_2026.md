# manage-product-catalog — 2026 Upgrade Plan

## Summary of 2026 Standards Changes

### Semantic Vector Search Layer (Production Standard 2026)
- **Embedding Generation**: High-dimensional vector embeddings for product titles/descriptions on write/update using `text-embedding-3-large` or Cohere `embed-v4`
- **Vector Storage**: `pgvector` (PostgreSQL extension) or Pinecone for storage and indexing
- **Hybrid Search Fusion**: BM25 (keyword) + dense vector search combined via **Reciprocal Rank Fusion (RRF)**
- **Benefits**: Contextual search, handles synonyms, typo tolerance, semantic understanding beyond keywords

### AI-Generated Product Content Governance (Mandatory 2026)
- **Review Gate**: Human review REQUIRED before AI-generated content status = `published`
- **Audit Metadata**: Track `generated_by`, `reviewed_by`, `generated_at`, `generation_model` on every AI-generated field
- **Brand Voice Validation**: Automated checks for banned words, claim accuracy, brand guidelines compliance BEFORE human review
- **Draft Status**: Unreviewed AI output = `draft` status, never `published`

### Event Sourcing for Real-Time Inventory (2026)
- **Publish Mutations**: All inventory adjustments/reservations → messaging systems (Apache Kafka, Cloudflare Queues) immediately
- **Consumer Processing**: Downstream consumers (search indexes, fulfillment dispatchers, AI shopping agents) consume for eventual consistency
- **No Database Locking**: Decouples inventory updates from catalog writes
- **CDC Alternative**: Debezium for change-data-capture from database to Kafka

### Knowledge Graph for Product Relationships (GraphRAG Pattern)
- **Graph Databases**: Neo4j, Amazon Neptune, TigerGraph, Memgraph for recommendations, compatibility matrices, bundles
- **GraphRAG Pattern**: Structured subgraphs fed into LLM retrieval chains for grounded customer recommendations
- **Entity Resolution**: Validated against labels, change-data-capture from Salesforce, Jira, GitHub, ServiceNow, SQL via Kafka/Airbyte
- **Pydantic-Enforced Schema**: Every entity type, relation, LLM output validated against Pydantic models — schema drift fails in CI
- **Cited Reasoning**: LangChain GraphCypherQAChain translates NL → Cypher → executes → feeds structured results + hybrid Qdrant vector hits → Anthropic Claude for cited reasoning

### Vietnam E-Commerce Compliance (Decree 248/2026/ND-CP)
- **Seller verification**: Platform must verify seller identity before allowing product listing
- **Product information accuracy**: Sellers must provide accurate, complete product info
- **Platform obligations**: Disclose service standards, pricing, promotions, handle complaints

---

## Required Skill Upgrades

### 1. Core Rules Updates
| Current Rule | 2026 Upgrade |
|--------------|--------------|
| Vector search mention | **Mandatory semantic vector layer**: embeddings on write, pgvector/Pinecone, RRF hybrid fusion |
| AI content governance mention | **Mandatory human review gate**, audit metadata tracking, brand voice validation, draft status for unreviewed |
| Event sourcing mention | **Full event sourcing for inventory**: Kafka/Cloudflare Queues, consumer processing, no DB locking |
| Knowledge graph mention | **GraphRAG pattern**: Neo4j/Neptune/TigerGraph, entity resolution, Pydantic schema enforcement, cited reasoning |
| Vietnam compliance | **Decree 248/2026/ND-CP**: seller verification gate before publish, platform obligations |
| CDC event streaming | **Debezium/Kafka** for real-time stock changes to downstream channels |

### 2. New 2026 Patterns to Add
- **Semantic Vector Search Architecture** with embedding pipeline, vector storage, RRF fusion
- **AI Content Governance Pipeline** with generation → validation → review → publish workflow
- **Event-Sourced Inventory** with Kafka/Cloudflare Queues, consumer patterns
- **Product Knowledge Graph** with GraphRAG retrieval for recommendations/compatibility
- **Vietnam Seller Verification Gate** integrated into product publish workflow
- **Pydantic Schema Enforcement** for all catalog entities and AI outputs

### 3. Checklist Additions
- [ ] Semantic vector embeddings generated on product write/update (`text-embedding-3-large` or Cohere `embed-v4`)
- [ ] Vector embeddings stored in pgvector or Pinecone with proper indexing
- [ ] Hybrid search: BM25 + dense vector combined via Reciprocal Rank Fusion (RRF)
- [ ] AI-generated product content: mandatory human review gate before `published` status
- [ ] AI content audit metadata: `generated_by`, `reviewed_by`, `generated_at`, `generation_model` tracked
- [ ] Brand voice validation: automated banned words, claim accuracy, brand guidelines checks
- [ ] Unreviewed AI output status = `draft` (never `published`)
- [ ] Inventory adjustments published to Kafka/Cloudflare Queues immediately
- [ ] Downstream consumers: search indexes, fulfillment, AI agents consume inventory events
- [ ] Product knowledge graph in Neo4j/Neptune/TigerGraph for relationships
- [ ] GraphRAG retrieval: structured subgraphs → LLM chains for grounded recommendations
- [ ] Entity resolution with CDC from Salesforce/Jira/GitHub/ServiceNow/SQL via Kafka/Airbyte
- [ ] Pydantic models for all entity types, relations, LLM outputs — schema drift fails in CI
- [ ] LangChain GraphCypherQAChain for NL → Cypher → cited reasoning
- [ ] Vietnam seller verification gate before product publish
- [ ] Platform obligations: service standards, pricing, promotions disclosed
- [ ] SKU uniqueness enforced at database constraint level
- [ ] Variant-level inventory tracked separately from product level
- [ ] Stock decrement operations atomic (transaction-safe)
- [ ] Pricing stored with version or effective timestamp
- [ ] `is_in_stock` computed server-side, not client-side
- [ ] Product publish/unpublish guarded by review/approval step
- [ ] Catalog sync idempotent by SKU if external source used
- [ ] Low-stock alerting threshold configured for ops team
- [ ] Channel safety buffers: dynamic virtual safety stock (5% or min 3 units) before marketplace publish

### 4. Failure Mode Additions
- **Vector search hallucination**: Semantic search returns irrelevant products → Mitigation: RRF fusion with BM25, relevance threshold tuning, human-in-the-loop evaluation
- **AI content published unreviewed**: Brand-damaging content goes live → Mitigation: Mandatory review gate, draft status enforcement, audit trail
- **Brand voice violation**: AI generates off-brand or inaccurate claims → Mitigation: Automated pre-review validation, banned words list, claim accuracy checks
- **Inventory event loss**: Kafka message lost, search index stale → Mitigation: Idempotent consumers, event replay capability, CDC backup (Debezium)
- **Knowledge graph entity resolution error**: Wrong product relationships → Mitigation: Validated against labels, human review of graph changes, Pydantic schema enforcement
- **GraphRAG citation failure**: LLM generates uncited recommendations → Mitigation: GraphCypherQAChain with mandatory citation, structured output validation
- **Vietnam compliance gap**: Unverified seller lists products → Mitigation: Verification gate in publish workflow, platform audit trail
- **Schema drift**: Catalog write with new/changed fields breaks downstream → Mitigation: Pydantic validation in CI, schema registry, contract testing

### 5. Output Contract Updates
- Add `contracts/schemas/vector-search-spec.json` for embedding pipeline and RRF fusion config
- Add `contracts/schemas/ai-content-governance-spec.json` for generation → review → publish workflow
- Add `contracts/schemas/event-sourced-inventory-spec.json` for Kafka event schema and consumer contracts
- Add `contracts/schemas/product-knowledge-graph-spec.json` for GraphRAG entities, relations, retrieval
- Add `contracts/schemas/vn-seller-verification-spec.json` for verification gate integration
- Add `contracts/schemas/pydantic-catalog-schema.json` for enforced entity/relation schemas
- Update `contracts/schemas/api-contract-spec.json` with new catalog endpoints

---

## Implementation Priority

| Priority | Task | Effort |
|----------|------|--------|
| P0 | Add semantic vector search layer (embeddings, pgvector/Pinecone, RRF) | High |
| P0 | Add mandatory AI content governance pipeline (review gate, audit metadata, brand validation) | High |
| P0 | Add event-sourced inventory with Kafka/Cloudflare Queues | High |
| P1 | Add product knowledge graph with GraphRAG (Neo4j/Neptune, GraphCypherQAChain) | High |
| P1 | Add Pydantic schema enforcement for all catalog entities | Medium |
| P1 | Add Vietnam seller verification gate in publish workflow | Medium |
| P1 | Add CDC event streaming (Debezium) for real-time sync | Medium |
| P2 | Expand failure modes with 2026-specific scenarios | Low |
| P2 | Update output contracts for new specs | Low |

---

## Validation Gates
- Run `python3 core/scripts/validate-all.py` from agent-skills root after edits
- Verify INDEX.md regeneration if VERSION bumped
- Check adapter parity with `validate-rules.py` (9 parity groups)
- Test vector search RRF fusion relevance with benchmark queries
- Test AI content review gate blocks unreviewed publish
- Test event-sourced inventory eventual consistency under load
- Test GraphRAG citation accuracy on product recommendation queries
- Test Pydantic schema validation catches drift in CI
- Test Vietnam seller verification gate integration