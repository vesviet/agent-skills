## Cloudflare Engineer Review Checklist

This reference checklist provides operational architecture, edge computing, serverless data fabric, and security verification criteria for Cloudflare engineering to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across Compatibility Date pinning, Durable Objects SQLite state machines, Workers AI LLM Gateway integration, stateless edge MCP servers, Hyperdrive connection pooling, Vectorize semantic search, R2 zero-egress storage, Turnstile bot defense, and canary deployment rollouts.

### 1. Compatibility Date Pinning & Wrangler Configuration
- **Deterministic Runtime Compatibility Pinning**:
  - `wrangler.toml` or `wrangler.jsonc` mandates explicit `compatibility_date` pinned to an immutable date ($\ge \text{2026-05-01}$); unpinned or future compatibility dates prohibited
  - compatibility flags declared explicitly (e.g. `nodejs_compat_v2`, `transformstream_enable_standard_constructor`)
  - staging and production environments define separate binding declarations, route patterns, and secret configurations
- **Hermetic Secret Injection & Zero Client Leakage**:
  - production secrets injected via `wrangler secret put` or Cloudflare Dashboard; `.dev.vars` excluded via `.gitignore`
  - bundles scanned before release to ensure no R2/KV access keys, database passwords, or Turnstile secret keys are bundled into client-side assets

### 2. Durable Objects SQLite & Distributed State Consistency
- **Durable Objects with Embedded SQLite Engine**:
  - transactional state models utilize Durable Objects backed by the embedded SQLite storage engine (`ctx.storage.sql.exec(...)`) rather than legacy unstructured KV storage
  - atomic SQL transactions wrap multi-entity state mutations to prevent partial write corruption
  - alarm handlers (`alarm()`) implement automated TTL garbage collection and delayed reconciliation loops
- **Single-Writer Concurrency & Partitioning**:
  - DO IDs mapped deterministically by tenant, user, or room ID (`idFromName`) to isolate fault domains
  - cross-DO messaging utilizes typed RPC methods; circular invocation loops between Durable Objects prevented via hop-count headers

### 3. Workers AI & Centralized LLM Gateway Integration (`LLM-GATEWAY LOCK` / `TOKEN-BUDGET LOCK`)
- **Centralized LLM Gateway Routing**:
  - all Workers AI calls route through Cloudflare AI Gateway (`cf.ai.gateway`); direct raw calls to external LLM provider endpoints from Worker handlers strictly prohibited
  - AI Gateway caching rules enabled for deterministic inference queries, reducing redundant inference costs by $\ge 40\%$
  - automated fallback and multi-model routing configured across primary (e.g. Workers AI Llama-3.3-70B) and secondary backup providers
- **Per-Tenant Token Budgets & Rate Throttling**:
  - per-request, per-user, and per-tenant token consumption ceilings enforced at the edge
  - rate limiting rules return HTTP 429 Too Many Requests with compliant `Retry-After` headers when quotas are approached (alerting at 70% of cap)

### 4. Stateless Edge MCP 2026-07-28 Protocol (`MCP-STATELESS LOCK` / `MCP-REGISTRY LOCK`)
- **Stateless HTTP Architecture**:
  - edge MCP servers strictly implement stateless HTTP transport complying with the MCP 2026-07-28 specification
  - long-lived stateful WebSockets or stdio session dependencies eliminated; session continuity externalized to Durable Objects, D1, or KV
  - protocol headers verified on every request (`_meta.protocol_version`, `MCP-Protocol-Version: 2026-07-28`)
- **Tool Registry Allowlist & Provenance Check**:
  - all edge MCP tools verified against the organization tool map; tools advertising unmapped mutations or dangerous shells rejected fail-closed

### 5. Edge Data Fabric (Hyperdrive, Vectorize, D1 & R2)
- **Hyperdrive Accelerated Database Pooling**:
  - backend PostgreSQL / MySQL database queries route via Cloudflare Hyperdrive bindings, pooling connections and caching prepared statements at edge PoPs
  - P95 database connection latency reduced from $>150\text{ms}$ cross-region to $<15\text{ms}$ at edge cache hit
- **Vectorize Semantic Search & Embeddings**:
  - vector index dimensions match embedding model output exactly (e.g. 768-dim for `bge-base-en-v1.5`)
  - cosine or dot-product distance metrics verified; search queries filter metadata before top-K ranking
- **R2 Zero-Egress Storage & Asset Caching**:
  - binary assets, model weights, and media served from R2 buckets via custom domain routing with Cache-Control headers (`public, max-age=31536000, immutable`)

### 6. Edge Security, Turnstile & WAF Architecture
- **Turnstile Managed Challenge Integration (`turnstile-spin`)**:
  - interactive forms, checkout endpoints, and login gates protected by Cloudflare Turnstile
  - server-side token validation executed against `https://challenges.cloudflare.com/turnstile/v0/siteverify` using idempotent verification calls; client responses never trusted without server-side validation
- **WAF Custom Rules & Rate Limiting**:
  - edge WAF rules inspect bot score, JA4 TLS fingerprints, and country codes before passing traffic to origin
  - API endpoints enforce sliding-window rate limits to prevent brute-force and credential-stuffing abuse

### 7. Zero-Downtime Canary Rollouts & Rollback Automation
- **Gradual Version Deployments**:
  - production deployments utilize Cloudflare Deployments gradual rollout (e.g. 10% $\rightarrow$ 25% $\rightarrow$ 50% $\rightarrow$ 100%) to canary new versions
  - automated rollback triggered if edge error rates (HTTP 5xx) exceed 0.5% during canary evaluation
- **Smoke Testing & Pre-Flight Verification**:
  - staging preview environments (`*.<project>.workers.dev` or preview branch domains) verified with hermetic smoke tests before promoting versions to production custom domains

### 8. Performance SLAs & V8 Isolate Optimization (`web-perf`)
- **Cold Start Elimination & CPU Limits**:
  - worker bundle size optimized via Tree-shaking and minification; uncompressed bundle size strictly capped ($\le 1\text{MB}$ for standard Workers, $\le 5\text{MB}$ for Workers with WASM)
  - V8 isolate initialization time verified at $\le 5\text{ms}$
- **Streaming Responses & Smart Placement**:
  - large HTML or JSON payloads streamed via `TransformStream` to minimize Time-to-First-Byte (TTFB)
  - Smart Placement enabled for database-heavy Workers to execute workloads geographically adjacent to backend database instances
