# Agent Knowledge Base & Reports Operating Rules (2027 SOTA Standard)

This rule defines mandatory invariants for all AI Agents operating within the Vesviet (`tanhdev.com`) and Learn (`learn.tanhdev.com`) twin repository ecosystem.

---

## 1. Mandatory Knowledge Base Consultation (Pre-Execution Retrieval)

Before designing system architectures, generating code snippets, drafting technical articles, or producing radar briefings, Agents **MUST** consult the centralized Agent Knowledge Base:

1. **Master Index**: Read `reports/KNOWLEDGE_INDEX.md` (located in both `vesviet/reports/` and `learn/reports/`).
2. **Domain Knowledge Cards**: Read the targeted topic card in `reports/knowledge/<domain>/<topic>.md` across the 6 core domains:
   - `reports/knowledge/ecommerce/`: Alipay 610k TPS, Shopee Traffic Shield, Composable 21 Services, WMS Order Allocation, Cart Redis Lua.
   - `reports/knowledge/banking-fintech/`: Core Banking Double-Entry Ledger, Microfinance Event Sourcing, Distributed Financial Sagas.
   - `reports/knowledge/ai-slm-agentic/`: vLLM v1 PagedAttention, SLM Distillation DeepSeek-R1, Generative UI Edge, Agent Swarms LiteLLM, HNSW Vector DB.
   - `reports/knowledge/distributed-systems/`: gRPC vs REST, Kafka vs NATS JetStream, TiDB vs Sharding, Dapr Actors, Modular Monolith, UUIDv7 vs Snowflake.
   - `reports/knowledge/ride-hailing-geospatial/`: H3 Spatial Indexing, Dispatch Matching & Surge, Urban Canyon GPS EKF, Ramen WebSocket.
   - `reports/knowledge/cloud-infrastructure/`: AWS MySQL 8.4 EOL Migration, AWS EKS vs ECS Fargate, Cilium eBPF Mesh, Zero-Trust SPIRE.
3. **Context Efficiency Rule**: NEVER ingest or search raw, verbose 100-round JSON dossiers in `reports/archive/` unless explicitly instructed to perform historical debugging. The `knowledge/` cards are distilled for minimal token overhead (< 15 KB).
4. **Invariant Compliance**: Architectural invariants, mathematical formulas, and concurrency fences defined in the Knowledge Cards (e.g. Balanced Debit/Credit, single aggregate boundaries, Redis Lua fencing tokens, monotonic UUIDv7, H3 resolution levels) MUST be strictly preserved in any generated code or architecture.

---

## 2. Reports Directory Cleanliness & Hygiene

The `reports/` directory in both repositories must remain clean, uncluttered, and strictly structured:

1. **Root Directory Limit ($\le 5$ files)**: The root of `reports/` must only contain active, authoritative platform files:
   - `KNOWLEDGE_INDEX.md`
   - `CONTENT_INDEX.md`
   - `posts-corpus-audit-*.md`
   - `legacy-posts-upgrade-plan-*.md`
2. **Zero Scratch Files**: NEVER dump loose scratch scripts (`*.py`, `*.sh`), temporary test dumps, or raw research JSON files into `reports/` root.
3. **Archival Standard**: All raw 100-round research dossiers and legacy audit snapshots must reside in `reports/archive/research-dossiers/` and `reports/archive/historical-audits/`.
4. **Synthesis Standard**: Any new architectural findings must be synthesized as a concise Knowledge Card in `reports/knowledge/<domain>/` and indexed in `KNOWLEDGE_INDEX.md`.

---

## 3. Twin Repository Parity & One-Way Authority

1. **Bitwise Twin Parity**: Any modification to `reports/KNOWLEDGE_INDEX.md` or `reports/knowledge/` MUST maintain **100% SHA-256 bitwise parity** between `vesviet/reports` and `learn/reports`.
2. **One-Way Authority Rule**:
   - Vietnamese content in `learn/` links UP to English flagship articles in `vesviet/` via badges.
   - English content in `vesviet/` must have **ZERO** outbound leaks to `learn.tanhdev.com`.

---

## 4. Article 2027 SOTA 7-Gate Compliance

All standalone articles, series chapters, and radar briefings must satisfy all 7 Quality Gates:
- **Gate 1 (Depth)**: Size > 20.5 KB & Body words $\ge 2,500$.
- **Gate 2 (Answer-First)**: Single-line blockquote `> **Answer-first:**` (48–62 words).
- **Gate 3 (Prerequisite)**: Explicit prerequisite callout block.
- **Gate 4 (Visuals)**: $\ge 2$ valid Mermaid diagrams (`mermaid: true` in frontmatter).
- **Gate 5 (Structured FAQ)**: $\ge 3\text{--}4$ `{{< faq >}}` shortcodes generating valid Schema.org FAQPage JSON-LD.
- **Gate 6 (Code Realism)**: Production-grade Go 1.25+, Redis 7.4, MySQL 8.4, zero pseudo-code.
- **Gate 7 (Authority)**: Inbound links to Anchor Pillar Hubs and reciprocal badges.

---

## 5. Mandatory Verification Before Done

Before declaring any task complete or proposing `git commit` / `git push`:
1. `python learn/tests/verify_knowledge_base_sota.py` (6/6 PASS).
2. `python vesviet/tests/test_redirects_oracle.py` (23/23 PASS).
3. `python learn/tests/verify_gsc_remediation.py --skip-build` (38/38 PASS).
4. `python learn/tests/verify_sprint1_master.py` & `verify_sprint2_master.py` (100% PASS).
5. `python learn/tests/verify_radar_2027_sota.py` & `verify_target_posts_sota.py` (100% PASS).
6. Dual Hugo minified builds (`hugo --minify --source vesviet` & `learn`) exit code 0.
