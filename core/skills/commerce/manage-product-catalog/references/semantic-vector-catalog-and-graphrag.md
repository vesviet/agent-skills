# Semantic Vector Catalog & GraphRAG Governance Specifications (2026)

## 1. Hybrid Search Architecture & Reciprocal Rank Fusion (RRF)

### 1.1 Dense Vector Layer with pgvector HNSW
E-commerce catalogs in 2026 deploy hybrid retrieval combining sparse BM25 text search with dense semantic embeddings:
- **Embedding Generation**: Compute dense embeddings on product write/update using `text-embedding-3-large` (1536/3072 dimensions) or Cohere `embed-v4`.
- **pgvector Indexing**: Index dense vectors using Hierarchical Navigable Small World (HNSW) with production-calibrated hyperparameters:
  ```sql
  CREATE INDEX idx_products_embedding ON products 
  USING hnsw (embedding vector_cosine_ops) 
  WITH (m = 16, ef_construction = 64);
  ```
- **Reciprocal Rank Fusion (RRF)**:
  Merge sparse keyword ranks ($R_{\text{BM25}}$) and vector similarity ranks ($R_{\text{dense}}$) using constant $k = 60$:
  $$\text{RRF Score}(d) = \frac{1}{60 + R_{\text{BM25}}(d)} + \frac{1}{60 + R_{\text{dense}}(d)}$$

---

## 2. AI Content Governance Pipeline (Human-in-the-Loop)

### 2.1 State Transition Enforcement
Autonomous LLM-generated product descriptions, titles, and variant attributes must never be set directly to `published`:
$$\text{Draft (AI Generated)} \xrightarrow{\text{Brand Voice Linter}} \text{Pending Review} \xrightarrow{\text{Human Gate Approved}} \text{Published}$$

### 2.2 Mandatory Provenance Metadata
Every catalog entity carries immutable provenance audit attributes:
```json
{
  "generation_metadata": {
    "generated_by_model": "gpt-4o-2026-08-06",
    "prompt_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "generated_at": "2026-11-08T09:00:00Z",
    "banned_claims_check_passed": true,
    "reviewed_by_user_id": "usr_compliance_lead_08",
    "reviewed_at": "2026-11-08T09:30:00Z",
    "approval_status": "APPROVED"
  }
}
```

---

## 3. Real-Time Inventory CDC & Event Sourcing

- **Debezium CDC**: Stream database inventory adjustments to Kafka / Cloudflare Queues with sub-second latency.
- **Safety Stock Deduction**: Deduct a virtual safety stock buffer (5% or minimum 3 units) before publishing available inventory to external channels (Shopee, Lazada, TikTok Shop, Amazon).

---

## 4. Knowledge Graph & GraphRAG Grounding

- **Graph Topology**: Model cross-sell relationships, bundles, compatibility constraints, and replacement components in Neo4j or Amazon Neptune.
- **Cited Recommendations**: Use LangChain `GraphCypherQAChain` to execute natural language queries against graph topology, enforcing explicit source node citations on all LLM recommendations.
