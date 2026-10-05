## Agent Discovery Engineer Review Checklist

This reference checklist provides operational agentic web standards, protocol discovery, machine-readable metadata, and registry federation criteria to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across canonical `auth.md` formatting, RFC 8414/8707 OAuth authorization metadata, Model Context Protocol (MCP) server cards, RFC 8288 HTTP link header discovery, agentic commerce protocols (x402 / UCP / MPP / ACP), zero secret leakage in public metadata, and automated agent-readiness scanner compliance (19/19 score).

### 1. Canonical `/auth.md` Specification Adherence
- **Exact Syntax & Header Conformance**:
  - `/auth.md` published at domain root using the exact `# Auth.md` top-level H1 header
  - document defines valid, live `register_uri` and `claim_uri` syntax matching governing RFC specifications
  - authentication endpoints and documentation links verified as live and publicly resolvable
- **Machine Readability**:
  - markdown structure strictly adheres to machine-parseable key-value blocks; ambiguous natural language descriptions in machine-read sections rejected

### 2. RFC 8414 & RFC 8707 OAuth Discovery Endpoints (`SCHEMA-EXACT LOCK`)
- **Protected Resource & Authorization Server Metadata**:
  - `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server` return valid JSON conforming to RFC 8414 and RFC 8707 schemas
  - authorization metadata mandates PKCE support (`code_challenge_methods_supported` includes `S256`)
  - token endpoint auth methods (`token_endpoint_auth_methods_supported`) specify supported client authentication types explicitly

### 3. Model Context Protocol (MCP) Server Card Specification
- **Standardized Server Card Manifest**:
  - `/.well-known/mcp/server-card.json` validates against the official MCP server-card schema specification
  - card accurately advertises supported transport types (stateless HTTP), tool registry endpoints, and authentication requirements
  - advertised capabilities match deployed MCP server endpoints with zero schema drift

### 4. RFC 8288 HTTP Web Linking & Response Headers
- **Link Header Discovery Injection**:
  - root and API HTTP response headers inject RFC 8288 compliant `Link` headers pointing to discovery metadata:
    ```http
    Link: </auth.md>; rel="authorizing-agent", </.well-known/api-catalog>; rel="api-catalog"
    ```
  - `rel` types verified against IANA Link Relation registry

### 5. Agentic Commerce Protocols (x402, UCP, MPP, ACP) Verification
- **Payment & Machine Interaction Standards**:
  - payment endpoints implement x402 payment headers (`X-402-Payment-Required`) or Merchant Payment Protocol (MPP) schemas
  - User Context Protocol (UCP) and Agentic Commerce Protocol (ACP) manifests return valid schemas or are explicitly marked `not_implemented` rather than returning broken payloads

### 6. Public Metadata Sanitization & Live Domain Integrity (`NO-SECRETS LOCK` / `NO-DUMMY-DOMAIN LOCK`)
- **Zero Secrets in Public Discovery Files**:
  - discovery files (`auth.md`, well-known JSON, server cards) thoroughly audited to ensure zero private keys, API secrets, or OAuth client secrets are exposed
- **Live Resolvable Domains Only**:
  - placeholder domains (`example.com`, `dummy.local`) strictly prohibited; all URLs in discovery files must be live, resolvable HTTPS endpoints owned by the deployment

### 7. Cryptographic Peer Attestation & Signature Verification (`SIGNATURE-VERIFY LOCK`)
- **Peer Metadata Validation**:
  - external agent cards, skills manifests, and discovery documents consumed from peer networks must verify cryptographic signatures before metadata content is trusted
  - unsigned or schema-drifted peer cards rejected as untrusted input

### 8. Automated Scanner Scoring (19/19 Checks)
- **Comprehensive Agent-Readiness Scan**:
  - domain evaluated against automated agent-readiness scanners (isitagentready.com or equivalent) achieving a 19/19 score
  - any failing scanner check must be documented with an assigned owner, root-cause analysis, and tracked remediation ticket

### 9. Registry Synchronization & Federation Standards (`REGISTRY-FEDERATION LOCK`)
- **Automated Registry Ingestion**:
  - discovery endpoints synchronize with local A2A registry (`core/a2a/.well-known/agent-registry.json`) with zero orphaned or unresolvable agent IDs
  - federated discovery manifests produce schema-compliant `contracts/schemas/agent-discovery-report.json`
- **DNS Record Validation**:
  - TXT and SRV discovery records verified with DNSSEC validation across authoritative nameservers

### 10. Operational Failure Modes & Escalation Protocols
- **Stale Discovery Metadata Invalidation**:
  - CDN edge caching headers for discovery endpoints enforce strict `max-age` ($\le 300\text{s}$) with `must-revalidate` to prevent stale agent capability routing
- **Escalation Triggers**:
  - unresolvable endpoints or invalid RFC JSON schemas trigger immediate P1 alerts to platform and security engineers
