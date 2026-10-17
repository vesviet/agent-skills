## Cloudflare Engineer Review Checklist

This reference checklist provides operational architecture, edge computing, serverless data fabric, and security verification criteria for Cloudflare engineering to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across Compatibility Date pinning, Durable Objects SQLite state machines, Workers AI LLM Gateway integration, stateless edge MCP servers, Hyperdrive connection pooling, Vectorize semantic search, R2 zero-egress storage, Turnstile bot defense, and canary deployment rollouts.

### 1. Compatibility Date Pinning & Wrangler Configuration (`COMPAT-DATE LOCK`)
- **Deterministic Runtime Compatibility Pinning**:
  - `wrangler.toml` or `wrangler.jsonc` mandates explicit `compatibility_date` pinned to an immutable date ($\ge \text{2026-09-23}$); unpinned or future compatibility dates prohibited
  - compatibility flags declared explicitly (e.g. `nodejs_compat_v2`, `transformstream_enable_standard_constructor`)
  - staging and production environments define separate binding declarations, route patterns, and secret configurations:
    ```toml
    name = "edge-api-gateway"
    main = "src/index.ts"
    compatibility_date = "2026-09-23"
    compatibility_flags = ["nodejs_compat_v2"]
    
    [placement]
    mode = "smart"
    ```
- **Hermetic Secret Injection & Zero Client Leakage**:
  - production secrets injected via `wrangler secret put` or Cloudflare Dashboard; `.dev.vars` excluded via `.gitignore`
  - bundles scanned before release to ensure no R2/KV access keys, database passwords, or Turnstile secret keys are bundled into client-side assets

### 2. Durable Objects SQLite & Distributed State Consistency (`DO-SQLITE LOCK`)
- **Durable Objects with Embedded SQLite Engine**:
  - transactional state models utilize Durable Objects backed by the embedded SQLite storage engine (`ctx.storage.sql.exec(...)`) rather than legacy unstructured KV storage:
    ```typescript
    export class InventoryDurableObject implements DurableObject {
      constructor(private ctx: DurableObjectState, private env: Env) {
        ctx.storage.sql.exec(`
          CREATE TABLE IF NOT EXISTS stock (
            sku TEXT PRIMARY KEY,
            available INTEGER NOT NULL,
            reserved INTEGER NOT NULL DEFAULT 0
          );
        `);
      }
      async reserveStock(sku: string, qty: number): Promise<boolean> {
        return this.ctx.storage.transactionSync(() => {
          const row = this.ctx.storage.sql.exec('SELECT available FROM stock WHERE sku = ?', sku).one();
          if (row && (row.available as number) >= qty) {
            this.ctx.storage.sql.exec('UPDATE stock SET available = available - ?, reserved = reserved + ? WHERE sku = ?', qty, qty, sku);
            return true;
          }
          return false;
        });
      }
    }
    ```
  - single-writer concurrency guaranteed per entity ID (`idFromName`); circular RPC calls between Durable Objects prevented via hop-count headers
  - alarm handlers (`alarm()`) implement automated TTL garbage collection and delayed reconciliation loops

### 3. Workers AI & Centralized LLM Gateway Integration (`LLM-GATEWAY LOCK` / `TOKEN-BUDGET LOCK`)
- **Centralized LLM Gateway Routing & Caching**:
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
  - effective database latency modeled via:
    $$\text{Latency}_{\text{effective}} = \text{CHR} \cdot L_{\text{edge}} + (1 - \text{CHR}) \cdot L_{\text{origin}}$$
    where $\text{CHR} \ge 0.85$ (Cache Hit Ratio), $L_{\text{edge}} \le 12\text{ms}$, and $L_{\text{origin}} \approx 180\text{ms}$
- **Vectorize Semantic Search & Embeddings**:
  - vector index dimensions match embedding model output exactly (768-dim for `bge-base-en-v1.5`)
  - cosine or dot-product distance metrics verified; search queries filter metadata before top-K ranking
  - maximum index size capped at $\le 5,000,000$ vectors per index; queries benchmarked at P95 $< 25\text{ms}$
- **R2 Zero-Egress Storage & Asset Caching**:
  - binary assets, model weights, and media served from R2 buckets via custom domain routing with Cache-Control headers (`public, max-age=31536000, immutable`)
  - direct S3 egress fees eliminated; presigned upload URLs generated with strict $\le 15\text{min}$ TTL

### 6. Edge Security, Turnstile & WAF Architecture
- **Turnstile Managed Challenge Integration (`turnstile-spin`)**:
  - interactive forms, checkout endpoints, and login gates protected by Cloudflare Turnstile
  - server-side token validation executed against `https://challenges.cloudflare.com/turnstile/v0/siteverify` using idempotent verification calls; client responses never trusted without server-side validation
- **WAF Custom Rules & Rate Limiting**:
  - edge WAF rules inspect bot score, JA4 TLS fingerprints, and country codes before passing traffic to origin
  - API endpoints enforce sliding-window rate limits to prevent brute-force and credential-stuffing abuse

### 7. Zero-Downtime Canary Rollouts & Rollback Automation
- **Gradual Version Deployments**:
  - production deployments utilize Cloudflare Deployments gradual rollout (10% $\rightarrow$ 25% $\rightarrow$ 50% $\rightarrow$ 100%) to canary new versions
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

### 9. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Compatibility Date** | Date $\ge \text{2026-09-23}$ | `wrangler deploy --dry-run` | Valid compatibility date pinned |
| **Durable Objects SQL** | Atomic transaction lock | `wrangler tail \| grep "transactionSync"` | Zero unhandled SQL errors |
| **Hyperdrive Latency** | P95 latency $< 15\text{ms}$ | Cloudflare GraphQL Analytics API | P95 $< 15\text{ms}$ on cache hit |
| **Canary Error Gate** | Error rate $< 0.5\%$ | Cloudflare Dashboard Deployments | Automatic rollback on breach |
| **Turnstile Validation** | Server-side verification | `curl -X POST .../siteverify` | Success true, hostname match |
| **Bundle Size Cap** | Bundle size $\le 1\text{MB}$ | `wrangler deploy --dry-run --outdir dist` | Output file $\le 1048576$ bytes |
| **Vectorize Index** | Dimensions == 768 | `wrangler vectorize get my-index` | Metric: cosine, dim: 768 |
