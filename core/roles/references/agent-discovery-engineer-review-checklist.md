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

### 2. RFC 8414 & RFC 8707 OAuth Discovery Endpoints (`SCHEMA-EXACT LOCK`)
- **Protected Resource & Authorization Server Metadata**:
  - `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server` return valid JSON conforming to RFC 8414 and RFC 8707 schemas
  - authorization metadata mandates PKCE support (`code_challenge_methods_supported` includes `S256`)
  - token endpoint auth methods (`token_endpoint_auth_methods_supported`) specify supported client authentication types explicitly (`private_key_jwt`, `tls_client_auth`)
  - rotating JWKS endpoints (`jwks_uri`) enforce cache TTL $\le 1\text{h}$ with automated zero-downtime key rotation
- **Resource Indicators (RFC 8707) Enforcement**:
  - authorization requests must specify the exact `resource` URI parameter matching the intended target API
  - wildcards or omitted resource parameters in cross-domain agent delegations rejected fail-closed

### 3. Model Context Protocol (MCP) Server Card Specification (`MCP-SERVER-INTEGRITY LOCK`)
- **Standardized Server Card Manifest**:
  - `/.well-known/mcp/server-card.json` validates against the official MCP server-card schema specification
  - card accurately advertises supported transport types (stateless HTTP SSE), tool registry endpoints, and authentication requirements
  - advertised capabilities match deployed MCP server endpoints with zero schema drift; unmapped tools rejected fail-closed
- **Tool Schema Sandboxing**:
  - tool input parameters must provide strict JSON Schema Draft 2020-12 definitions with complete descriptions
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

### 7. Agentic Commerce Protocols (x402, UCP, MPP, ACP) Verification
- **Machine-to-Machine Payment Standards**:
  - payment endpoints implement x402 payment headers (`X-402-Payment-Required`) or Merchant Payment Protocol (MPP) schemas
  - User Context Protocol (UCP) and Agentic Commerce Protocol (ACP) manifests return valid schemas or are explicitly marked `not_implemented` rather than returning broken payloads

### 8. Public Metadata Sanitization & Live Domain Integrity (`NO-SECRETS LOCK` / `NO-DUMMY-DOMAIN LOCK`)
- **Zero Secrets in Public Discovery Files**:
  - discovery files (`auth.md`, well-known JSON, server cards) thoroughly audited to ensure zero private keys, API secrets, or OAuth client secrets are exposed
- **Live Resolvable Domains Only**:
  - placeholder domains (`example.com`, `dummy.local`) strictly prohibited; all URLs in discovery files must be live, resolvable HTTPS endpoints owned by the deployment

### 9. Registry Synchronization & Dual-Index SHA-256 Invariant (`ZERO-DRIFT-REGISTRY-LOCK`)
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

### 10. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Auth.md Syntax** | RFC-compliant headers | `curl -sS https://domain.internal/auth.md` | H1 `# Auth.md` present; endpoints valid |
| **Scanner Check** | 19/19 checks passing | `agent-readiness-scanner --target domain.internal` | Score == 19/19 |
| **Dual-Index Parity** | $H_{\text{core}} = H_{\text{adapter}}$ | `python3 core/scripts/generate-index.py --check` | 0 bitwise drift detected |
| **A2A Schema Parity** | Structural Part validation | `python3 core/scripts/validate-contracts.py` | 100% schema compliant |
| **Zero Secrets Gate** | Entropy $< 4.5$, 0 keys | `trufflehog filesystem core/a2a/` | 0 secret findings |
| **DNSSEC Integrity** | RRSIG authenticated | `dig +dnssec domain.internal TXT` | `ad` flag set in DNS response |
