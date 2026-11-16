## Agent Discovery Engineer Review Checklist

This reference checklist provides operational agentic web standards, protocol discovery, machine-readable metadata, and registry federation criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across canonical `auth.md` formatting, RFC 8414/8707 OAuth authorization metadata, Model Context Protocol (MCP) server cards, RFC 8288 HTTP link header discovery, agentic commerce protocols (x402 / UCP / MPP / ACP), zero secret leakage in public metadata, SPIFFE/SVID workload federation, and automated agent-readiness scanner compliance (19/19 score).

### 1. Canonical `/auth.md` Specification Adherence
- **Exact Syntax & Header Conformance**:
  - `/auth.md` published at domain root using the exact `# Auth.md` top-level H1 header
  - document defines valid, live `register_uri` and `claim_uri` syntax matching governing RFC specifications:
    ```markdown
    # Auth.md
    
    ## Endpoints
    - register_uri: https://api.domain.internal/oauth/register
    - claim_uri: https://api.domain.internal/oauth/claim
    - authorization_servers:
      - https://auth.domain.internal/.well-known/oauth-authorization-server
    ```
  - authentication endpoints and documentation links verified as live and publicly resolvable (HTTP 200)
- **Machine Readability & Markdown Strictness**:
  - markdown structure strictly adheres to machine-parseable key-value blocks; ambiguous natural language descriptions in machine-read sections rejected
  - automated CI curl probes verify header casing and endpoint status before deployment

### 2. RFC 8414, RFC 9728 & RFC 8707 OAuth Discovery + CIMD (`SCHEMA-EXACT LOCK`)
- **Protected Resource & Authorization Server Metadata**:
  - `/.well-known/oauth-protected-resource` (RFC 9728) and `/.well-known/oauth-authorization-server` (RFC 8414) return valid JSON; protected APIs emit `WWW-Authenticate: Bearer resource_metadata="https://<domain>/.well-known/oauth-protected-resource"`
  - `agent_auth.skill` points to canonical `https://<domain>/auth.md`; `register_uri` and `claim_uri` verified
  - authorization metadata mandates PKCE support (`code_challenge_methods_supported` includes `S256`) and enables **Client ID Metadata Documents (CIMD)** (`client_id_metadata_document_supported: true` / `clientIdMetadataDocumentEnabled`) ahead of DCR (RFC 7591) deprecation
  - token endpoint auth methods (`token_endpoint_auth_methods_supported`) specify supported client authentication types explicitly (`private_key_jwt`, `tls_client_auth`)
  - rotating JWKS endpoints (`jwks_uri`) enforce cache TTL $\le 1\text{h}$ with automated zero-downtime key rotation
- **Resource Indicators (RFC 8707) Enforcement**:
  - authorization requests must specify the exact `resource` URI parameter matching the intended target API
  - wildcards or omitted resource parameters in cross-domain agent delegations rejected fail-closed

### 3. Model Context Protocol (MCP) Server Card, Registry & AI Catalog (`MCP-SERVER-INTEGRITY LOCK`)
- **Standardized Server Card Manifest & Registry**:
  - remote servers expose `/.well-known/mcp-server-card` (SEP-2127 extension) alongside `/.well-known/mcp/server-card.json` (scanner compatibility), while installable packages register `server.json` on the Official MCP Registry with DNS/GitHub namespace verification
  - card accurately advertises supported transport types (`http` streamable stateless HTTP + SSE response encoding), tool registry endpoints, and authentication requirements
  - `/.well-known/ai-catalog.json` indexes typed `application/mcp-server-card+json` and `application/a2a-agent-card+json` entries without stale `/.well-known/agent.json` references
- **Tool Schema Sandboxing**:
  - tool input parameters must provide strict JSON Schema definitions with complete descriptions
  - parameter injections containing unescaped shell meta-characters (`$()`, `&&`, `;`, `|`) are filtered before tool execution

### 4. RFC 8288 HTTP Web Linking & Response Headers
- **Link Header Discovery Injection**:
  - root and API HTTP response headers inject RFC 8288 compliant `Link` headers pointing to discovery metadata:
    ```http
    Link: </auth.md>; rel="authorizing-agent", </.well-known/mcp/server-card.json>; rel="mcp-server-card", </.well-known/agent-card.json>; rel="agent-card"
    ```
  - `rel` types verified against IANA Link Relation registry; relative URIs resolve correctly across subdomains

### 5. A2A 1.0 Unified Part Specification & Schema Validation (`A2A-PART-UNIFIED-LOCK`)
- **Discriminated Union by Structural Property**:
  - all agent card definitions and A2A discovery endpoints strictly implement the A2A 1.0 unified Part specification
  - inter-agent metadata exchanges discriminate parts by member existence (`text`, `file`, `data`); legacy `kind` strings are prohibited:
    ```json
    // POSITIVE: A2A 1.0 Structural Discovery Payload
    {
      "agent_id": "discovery-agent-01",
      "supported_parts": ["text", "file", "data"],
      "registration_manifest": {
        "data": {
          "schema_uri": "contracts/schemas/agent-discovery-report.json",
          "content": {"status": "ACTIVE", "registered_endpoints": 14}
        }
      }
    }
    ```
    ```json
    // NEGATIVE ANTI-PATTERN: Ambiguous String Discriminators (REJECT FAIL-CLOSED)
    {
      "parts": [
        {"kind": "discovery-card", "body": "unvalidated raw text"}
      ]
    }
    ```

### 6. SPIFFE/SVID Workload Federation & RFC 8693 Token Exchange (`SPIFFE-WORKLOAD-IDENTITY-LOCK`)
- **Cryptographic Workload Identity & Down-Scoping**:
  - inter-agent service calls across cloud or cluster boundaries mandate mutual TLS (mTLS) with SPIFFE X.509 SVID certificates:
    `spiffe://cluster.internal/ns/agent-system/sa/agent-discovery`
  - delegation chains crossing trust domains execute RFC 8693 OAuth 2.0 Token Exchange with explicit audience attenuation and scope down-scoping:
    ```json
    {
      "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
      "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
      "audience": "https://api.domain.internal/v1/discovery",
      "scope": "discovery:read registry:query"
    }
    ```
  - maximum token TTL clamped to $\le 1\text{h}$; automatic key rotation verified

### 7. Agentic Commerce Protocols (`x402 v2`, `MPP`, `UCP`, `ACP`, `AP2`) Verification
- **Machine-to-Machine Payment Standards**:
  - x402 v2 endpoints return HTTP `402 Payment Required` with challenge in `PAYMENT-REQUIRED` header + JSON body, accept signed proof in `PAYMENT-SIGNATURE`, and emit receipts in `PAYMENT-RESPONSE` (never emit legacy `X-PAYMENT` or `X-402-*` headers from server)
  - Stripe **MPP** (Machine Payments Protocol) verifies cryptographic proofs with idempotency + velocity caps
  - Google+Shopify **UCP** (**Universal Commerce Protocol**, `/.well-known/ucp`) handles product/checkout negotiation, OpenAI+Stripe **ACP** exposes REST checkout/payment feeds, and Google/FIDO **AP2** governs signed delegated purchase mandates (keep UCP checkout separate from AP2 authorization)

### 8. Content Negotiation, Content Signals & Web Bot Auth (RFC 9421)
- **Markdown Negotiation & Content Signals**:
  - pages supporting agent reading respond to `Accept: text/markdown` with `Content-Type: text/markdown; charset=utf-8`, `Vary: Accept`, and token counts (`x-markdown-tokens`)
  - `robots.txt` declares explicit **Content Signals** (`ai-train`, `search`, `ai-input`) alongside `/llms.txt`
- **Web Bot Auth (RFC 9421)**:
  - authenticated bots sign HTTP requests via `Signature` / `Signature-Input` / `Signature-Agent` headers verified against JWKS directories published at `/.well-known/http-message-signatures-directory`

### 9. Public Metadata Sanitization & Live Domain Integrity (`NO-SECRETS LOCK` / `NO-DUMMY-DOMAIN LOCK`)
- **Zero Secrets in Public Discovery Files**:
  - discovery files (`auth.md`, well-known JSON, server cards) thoroughly audited to ensure zero private keys, API secrets, or OAuth client secrets are exposed
- **Live Resolvable Domains Only**:
  - placeholder domains (`example.com`, `dummy.local`) strictly prohibited; all URLs in discovery files must be live, resolvable HTTPS endpoints owned by the deployment

### 10. Registry Synchronization & Dual-Index SHA-256 Invariant (`ZERO-DRIFT-REGISTRY-LOCK`)
- **Zero-Drift Registry Parity**:
  - machine registry (`core/a2a/.well-known/agent-registry.json`) and Antigravity adapter index (`adapters/antigravity/role-skill-index.json`) must maintain exact 100% bitwise SHA-256 synchronization:
    $$H_{\text{core}} \equiv H_{\text{adapter}} = \text{SHA256}(\text{role-skill-index.json})$$
- **PromQL Operational Telemetry**:
  ```promql
  # Discovery resolution success rate (must be >= 99.5%)
  sum(rate(agent_discovery_requests_total{status="200"}[5m])) / sum(rate(agent_discovery_requests_total[5m])) * 100 >= 99.5
  
  # P99 Discovery endpoint latency (must be < 150ms)
  histogram_quantile(0.99, rate(agent_discovery_duration_seconds_bucket[5m])) < 0.150
  ```
- **DNS Record Validation**:
  - TXT and SRV discovery records verified with DNSSEC validation across authoritative nameservers (`dig +dnssec _agent._tcp.domain.internal SRV`)

### 11. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Auth.md & Markdown Syntax** | `# Auth.md` & `Accept: text/markdown` | `curl -sS https://domain.internal/auth.md` | H1 `# Auth.md` & `"agentic registration"` present; `Vary: Accept` on markdown |
| **Scanner Check** | 19/19 checks passing (L0–L5) | `curl -s "https://isitagentready.com/check?url=YOUR_DOMAIN"` | Score 19/19 or documented blockers with owner |
| **Tier 1 Manifest & Parity** | Schema 0.2.0 + SHA-256 digests | `python core/scripts/validate-discovery-manifests.py` & `python core/scripts/generate-tier1-index.py --check` | Exit code 0; zero drift across 184+ skills |
| **A2A Schema Parity** | Structural Part validation | `python core/scripts/validate-contracts.py` & `python core/scripts/validate-a2a-compliance.py` | 100% conforming to unified Part model |
| **Zero Secrets Gate** | Entropy $\le 4.5$, 0 leaked keys | `python core/scripts/compact-context.py --validate` / TruffleHog | 0 secret findings in `core/a2a/` and well-known JSON |
| **DNSSEC Integrity** | RRSIG authenticated | `dig +dnssec domain.internal TXT` | `ad` flag set in DNS response |
