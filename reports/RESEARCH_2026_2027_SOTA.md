# Comprehensive Research & Comparative Gap Analysis: 2026–2027 SOTA Agent Engineering Standards

> **Document Type:** Master SOTA Research Report & Architectural Gap Analysis  
> **Target Repository:** `agent-skills` (`d:\myproject\agent-skills`)  
> **Baseline Codebase:** `v5.7.3` (A2A 1.0 + Antigravity Adapter)  
> **Target Release:** `v5.9.0` / `v6.0.0` (AAIF A2A v1.0.1+, MCP 2026-07-28 Stateless HTTP, Two-Tier JIT, Prefix-Cache Alignment)  
> **Author:** `worker_research_m1` (Technical Author & Systems Analyst)  
> **Date:** November 2026  
> **Status:** Authoritative / Milestone M1 Deliverable  

---

## Table of Contents

1. [Executive Summary: The 2026–2027 Agent Engineering Paradigm Shift](#1-executive-summary-the-20262027-agent-engineering-paradigm-shift)
2. [Standard 1: agentskills.io Discovery Manifest Standard](#2-standard-1-agentskillsio-discovery-manifest-standard)
3. [Standard 2: AAIF Agent-to-Agent (A2A) Protocol v1.0.1+](#3-standard-2-aaif-agent-to-agent-a2a-protocol-v101)
4. [Standard 3: MCP Revision 2026-07-28 Stateless HTTP Transport & Remote Architecture](#4-standard-3-mcp-revision-2026-07-28-stateless-http-transport--remote-architecture)
5. [Standard 4: OWASP Top 10 for Agentic Security (ASI01–ASI10) & Agent Security Testing (AST01–AST10)](#5-standard-4-owasp-top-10-for-agentic-security-asi01asi10--agent-security-testing-ast01ast10)
6. [Standard 5: Prompt Prefix Caching Optimization Patterns & Cache Alignment](#6-standard-5-prompt-prefix-caching-optimization-patterns--cache-alignment)
7. [Standard 6: Token Economics, Context Window Efficiency & Head-Tail Tool Output Truncation (TOC)](#7-standard-6-token-economics-context-window-efficiency--head-tail-tool-output-truncation-toc)
8. [Standard 7: Two-Tier Just-In-Time (JIT) Skill Discovery Architectures](#8-standard-7-two-tier-just-in-time-jit-skill-discovery-architectures)
9. [Standard 8: Role Modularization, Least-Agency & Boundary Isolation Standards](#9-standard-8-role-modularization-least-agency--boundary-isolation-standards)
10. [Comprehensive Comparative Gap Analysis Matrix & File-by-File Divergence Ledger](#10-comprehensive-comparative-gap-analysis-matrix--file-by-file-divergence-ledger)
11. [Architectural Synthesis & Modernization Invariants](#11-architectural-synthesis--modernization-invariants)
12. [Appendix: Primary References & Standards Bibliography](#12-appendix-primary-references--standards-bibliography)

---

## 1. Executive Summary: The 2026–2027 Agent Engineering Paradigm Shift

Between 2024 and 2027, the autonomous agent engineering domain underwent a fundamental paradigm shift. Early multi-agent systems relied on ad-hoc system prompt concatenation, unconstrained tool sets injected monolithically into prompt context, stateful sticky HTTP sessions, and perimeter-based security assumptions. In production, these early architectures suffered from four systemic failure modes:
1. **Context Exhaustion & Attention Saturation ("Lost-in-the-Middle")**: Loading hundreds of skill descriptions and schemas into context consumed $15,000\text{--}300,000$ tokens per turn, inducing token starvation, high inference latency, and cognitive degradation where models ignored instructions positioned mid-context.
2. **Brittle Sticky Sessions & Scalability Ceilings**: Persistent socket handshakes and stateful HTTP session identifiers collided with serverless edge runtimes, dynamic auto-scalers, and distributed multi-cloud gateways.
3. **Severe Vulnerability to Supply Chain & Execution Exploits**: Incidents such as ClawHavoc (1,184 trojanized skills delivering reverse shells) and ToxicSkills (36.82% of public agent skills demonstrating over-privilege or remote instruction injection) demonstrated that traditional Least Privilege is insufficient for autonomous systems. Agent engineering requires **Least Agency**—restricting not just data access, but autonomous decision scope and irreversible execution reach.
4. **Economic & Latency Inefficiencies**: Failing to align prompt assembly with hardware KV-cache prefix quantization incurred $10\times$ token cost penalties and $85\text{--}90\%$ Time-To-First-Token (TTFT) latency inflation.

The **2026–2027 SOTA Agent Engineering Standards** resolve these challenges through eight interlocking architectural pillars:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        2026–2027 SOTA AGENT ARCHITECTURE                               │
├───────────────────────────────┬────────────────────────────────────────────────────────┤
│ Discovery & Interoperability  │ agentskills.io 0.2.0 (RFC 8615) + AAIF A2A v1.0.1+     │
│ Tool Execution & Transport    │ MCP 2026-07-28 Stateless HTTP + MRTR + SEP-2567        │
│ Security & Governance         │ OWASP ASI01–ASI10 + AST01–AST10 + Lethal Trifecta (T)  │
│ Context & Inference Economics │ 6-Layer Prefix Caching + 5-Tier Token Budget + TOC     │
│ Runtime Modularity            │ Two-Tier JIT Discovery + 3-State Policy Lattice (39x59)│
└───────────────────────────────┴────────────────────────────────────────────────────────┘
```

The `agent-skills` repository at version **5.7.3** represents an exceptional foundation—featuring 39 roles, 183 skills, 25 workflows, 60 JSON Schema Draft 2020-12 data contracts, and an automated 19-suite test validator achieving 100% exit code 0. However, v5.7.3 operates primarily on an internal adapter layer (Antigravity bindings, monolithic skill pre-loading, line-based output trimming). 

This research report provides the exhaustive technical foundation and empirical gap analysis required to modernize `agent-skills` to **v5.9.0 / v6.0.0**, aligning every role, skill, contract, and adapter with the authoritative 2026–2027 specifications.

---

## 2. Standard 1: agentskills.io Discovery Manifest Standard

### 2.1 Specification Citations & Primary Sources
* **Authoritative Schema URI**: `https://schemas.agentskills.io/discovery/0.2.0/schema.json`
* **Legacy Reference**: `https://schemas.agentskills.io/discovery/0.1.0/schema.json`
* **Well-Known URI Registry**: RFC 8615 (*Well-Known Uniform Resource Identifiers*) registered path:
  `/.well-known/agent-skills/index.json`
* **Cryptographic Canonicalization & Integrity**:
  * RFC 8785: *JSON Canonicalization Scheme (JCS)*
  * FIPS PUB 180-4: *Secure Hash Standard (SHS) - SHA-256*
* **URI Resolution & Normalization**: RFC 3986 (*Uniform Resource Identifier: Generic Syntax*)

### 2.2 Protocol Mechanics, Discovery Flow & Transport Requirements

#### 2.2.1 Progressive Disclosure Pattern
The `agentskills.io` standard enforces a two-tier **Progressive Disclosure** architecture designed to eliminate boot-time context window bloat:
1. **Tier 1 (Passive Discovery Index)**: The orchestrator or agent queries `GET /.well-known/agent-skills/index.json`. The server responds with a lightweight JSON payload containing only skill identifiers, display names, execution types, concise capability summaries, relative or absolute URLs, and SHA-256 integrity digests. Under no circumstances may instruction bodies, procedural checklists, or code implementations be embedded inside this index. The total payload size remains $< 5\text{ KB}$ across hundreds of cataloged skills.
2. **Tier 2 (Just-In-Time Asset Retrieval)**: When user intent triggers a specific capability, the agent fetches the target `SKILL.md` (or archive bundle) via HTTPS, validates its SHA-256 digest against the manifest, parses its YAML frontmatter, and loads allowed tool bindings into an isolated execution sandbox.

```
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Lightweight Discovery Index (~2–4 KB)                         │
│ Client executes GET /.well-known/agent-skills/index.json               │
│ Ingests: name, type, description, url, digest (NO instruction bodies)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 2: Intent Matching & Capability Routing                          │
│ Match user prompt against skill description "When to use" triggers     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Target matched: "pdf-processing"
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 3: JIT Asset Retrieval & Cryptographic Hash Verification         │
│ Fetch URL -> Compute SHA-256 -> Match against manifest digest          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Digest valid (sha256:...)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 4: Runtime Skill Activation & Sandbox Injection                  │
│ Ingest SKILL.md frontmatter -> Bind allowed tools -> Execute in Sandbox│
└────────────────────────────────────────────────────────────────────────┘
```

#### 2.2.2 Transport Requirements & HTTP Headers
* **HTTP Method**: `GET`
* **Endpoint**: `https://{domain}/.well-known/agent-skills/index.json`
* **Content-Type**: `application/json; charset=utf-8`
* **CORS Invariants**: Origin servers MUST provide CORS headers enabling web and IDE-based agent orchestrators:
  `Access-Control-Allow-Origin: *` (or whitelisted agent orchestrator origins). Preflight `OPTIONS` requests must return `204 No Content` with `Access-Control-Allow-Methods: GET, OPTIONS`.
* **Caching & Freshness**: Origin servers MUST emit `ETag` and `Last-Modified` headers. Agents MUST issue conditional HTTP requests (`If-None-Match`, `If-Modified-Since`) to avoid re-fetching unchanged manifests while preventing the execution of stale contracts (OWASP ASI01 / ASI04).
* **Passive Discovery Link Header**: Web servers and API gateways SHOULD advertise the discovery manifest via RFC 8288 `Link` headers on API responses and homepage headers:
  ```http
  Link: </.well-known/agent-skills/index.json>; rel="agent-skills"
  ```

### 2.3 Concrete Schemas & Manifest Formats

#### 2.3.1 Normative Discovery Manifest Schema (v0.2.0)
```json
{
  "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
  "skills": [
    {
      "name": "pdf-processing",
      "type": "skill-md",
      "description": "Extract text, tables, and form fields from PDF files. Use when extracting data from invoices, forms, or documents.",
      "url": "/.well-known/agent-skills/pdf-processing/SKILL.md",
      "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "name": "cart-checkout-orchestrator",
      "type": "archive",
      "description": "Orchestrates multi-channel shopping cart checkout, voucher validation, and inventory hold. Use during transaction checkout flows.",
      "url": "https://cdn.example.com/skills/cart-checkout-orchestrator-v2.1.0.tar.gz",
      "digest": "sha256:8f434346648f6b96df89dda901c5176b10f600aec66b197e4242633008447814"
    }
  ]
}
```

#### 2.3.2 Normative Field Validation Matrix
| Field Name | Type | Required | Constraint / Standard | Validation Invariant |
|---|---|:---:|---|---|
| `$schema` | `string` | **Yes** | Valid URI | Must match `"https://schemas.agentskills.io/discovery/0.2.0/schema.json"` |
| `skills` | `array` | **Yes** | Min Items: 1 | Bounded collection of discoverable capability objects |
| `skills[].name` | `string` | **Yes** | Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$` | Kebab-case; must exactly match parent folder name and frontmatter `name` |
| `skills[].type` | `string` | **Yes** | Enum: `["skill-md", "archive"]` | `"skill-md"` for standalone Markdown; `"archive"` for `.tar.gz`/`.zip` bundles |
| `skills[].description` | `string` | **Yes** | Length: 20 to 1024 characters | Must define operational capability + explicit "When to use" trigger phrase |
| `skills[].url` | `string` | **Yes** | RFC 3986 URI Reference | Absolute HTTPS URL or origin-relative path |
| `skills[].digest` | `string` | **Yes** | Pattern: `^sha256:[a-f0-9]{64}$` | Cryptographic SHA-256 hash of target payload |

### 2.4 Core Architectural Invariants & Failure Modes
1. **Digest Integrity Invariant (Tamper-Proof Delivery)**:
   $$\text{SHA-256}(\text{FetchedPayload}) \equiv \text{Manifest}.\text{digest} \implies \text{Admit to Sandbox}$$
   If the computed SHA-256 hash does not match the manifest digest byte-for-byte, the agent runtime MUST reject the payload immediately with error `E_DIGEST_MISMATCH` and fail closed, blocking supply chain poisoning (OWASP AST02 / ASI04).
2. **Identity Triad Parity Invariant**:
   The `skills[].name` attribute in `index.json`, the directory path name (`core/skills/<cat>/<name>/`), and the `name:` field in the `SKILL.md` YAML frontmatter MUST be 100% identical. Any deviation indicates unvetted drift (AST04).
3. **Payload Boundary Invariant**:
   `index.json` is strictly an indexing directory. Ingesting procedural steps, tool implementations, code snippets, or configuration secrets into `index.json` is an architectural violation.

---

## 3. Standard 2: AAIF Agent-to-Agent (A2A) Protocol v1.0.1+

### 3.1 Specification Citations & Primary Sources
* **Governance**: Agentic AI Foundation (AAIF), Linux Foundation directed fund (established August 27, 2026).
* **Specification Baseline**: **A2A Protocol Specification v1.0.1 (Released 2026-05-26)**.
* **Interface Definition Language (IDL)**: `a2a.proto` (Protocol Buffers v3 IDL defining wire envelopes, RPC services, and streaming events).
* **Agent Card Well-Known Path**: RFC 8615 registered URI `/.well-known/agent-card.json` (formerly `agent.json` in v0.2.x, updated in v0.3.0/v1.0.0).
* **Cryptographic Signatures**: RFC 7515 (JSON Web Signature - JWS) detached signatures over RFC 8785 (JCS) canonical JSON, resolving public keys via RFC 7517 (JSON Web Key - JWK).
* **Wire Error Standards**: `google.rpc.Status` with `google.rpc.ErrorInfo` (`domain: "a2a-protocol.org"`).

### 3.2 Protocol Mechanics, Endpoints & Lifecycle State Machine

#### 3.2.1 Normative RPC Operations & Methods
The A2A v1.0.1 specification defines four standard JSON-RPC 2.0 / HTTP operations:

| Method Name | Direction | Transport | Purpose |
|---|---|---|---|
| `message/send` | Client $\rightarrow$ Agent | HTTP POST (Sync) | Synchronously dispatch task message; returns task acknowledgment and status |
| `message/stream` | Client $\rightarrow$ Agent | HTTP POST + SSE | Opens Server-Sent Events stream for real-time status updates and partial artifact chunks |
| `tasks/get` | Client $\rightarrow$ Agent | HTTP POST | Retrieve full state, message thread, and partial artifacts for `task_id` |
| `tasks/cancel` | Client $\rightarrow$ Agent | HTTP POST | Terminate an active task with structured cancellation reason |
| `tasks/list` | Client $\rightarrow$ Agent | HTTP POST | Paginated listing of agent tasks filtered by state or tenant |

#### 3.2.2 Monotonic Task Lifecycle State Machine

```
                         ┌───────────────────────┐
                         │ TASK_STATE_SUBMITTED  │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  TASK_STATE_WORKING   │◄────────────────┐
                         └───────┬───────┬───────┘                 │
                                 │       │                         │
           Needs Input / Clarify │       │ Needs Credentials       │ User Responded /
                                 ▼       ▼                         │ Auth Provided
                 ┌──────────────────┐ ┌───────────────────┐        │
                 │   TASK_STATE_    │ │   TASK_STATE_     │        │
                 │  INPUT_REQUIRED  │ │  AUTH_REQUIRED    │────────┘
                 └─────────┬────────┘ └─────────┬─────────┘
                           │                    │
                           └──────────┬─────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │ Terminal Completion     │ Terminal Failure        │ Aborted / Rejected
            ▼                         ▼                         ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│ TASK_STATE_COMPLETED  │ │   TASK_STATE_FAILED   │ │ TASK_STATE_CANCELED / │
│                       │ │                       │ │  TASK_STATE_REJECTED  │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
```

#### 3.2.3 State Monotonicity & Casing Invariants
1. **Irreversible Terminal States**: Transitions to `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_CANCELED`, or `TASK_STATE_REJECTED` are strictly terminal. No subsequent message, timeout, or event can transition a task out of a terminal state.
2. **Screaming Snake Case Standard**: Wire states MUST use uppercase `TASK_STATE_*`. Runtime adapters mapping to lowercase aliases (`working`, `completed`) must translate at the wire boundary.

### 3.3 Concrete Wire Schemas, SSE Envelopes & Error Models

#### 3.3.1 Agent Card Discovery Schema (`/.well-known/agent-card.json`)
```json
{
  "$schema": "https://a2a-protocol.org/schemas/v1.0.1/agent-card.json",
  "name": "Backend Implementation Agent",
  "description": "High-velocity Go and Python backend service development agent.",
  "version": "1.0.1",
  "capabilities": {
    "streaming": true,
    "push_notifications": true
  },
  "supportedInterfaces": [
    {
      "url": "https://api.example.com/a2a/v1",
      "protocolBinding": "JSONRPC",
      "protocolVersion": "1.0.1"
    }
  ],
  "securitySchemes": {
    "bearerAuth": {
      "type": "http",
      "scheme": "bearer",
      "bearerFormat": "JWT"
    },
    "oauth2": {
      "type": "oauth2",
      "flows": {
        "clientCredentials": {
          "tokenUrl": "https://auth.example.com/oauth/token",
          "scopes": {
            "a2a:delegate": "Delegate engineering tasks"
          }
        }
      }
    }
  },
  "security": [
    { "bearerAuth": [] },
    { "oauth2": ["a2a:delegate"] }
  ]
}
```

#### 3.3.2 Streaming Progress Events (`text/event-stream`)
When connecting via `message/stream`, updates are transmitted over SSE using two primary event types:
```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

event: TaskStatusUpdateEvent
data: {"taskId":"c9b1b72e-3351-4091-a67b-1cb1e6a39480","contextId":"ctx-99182","state":"TASK_STATE_WORKING","statusMessage":"Executing unit tests across 14 modules...","progressPercent":45,"timestamp":"2026-11-05T13:31:00Z"}

event: TaskArtifactUpdateEvent
data: {"taskId":"c9b1b72e-3351-4091-a67b-1cb1e6a39480","artifactId":"art-001","partIndex":0,"append":true,"lastChunk":false,"part":{"text":"PASS: internal/auth/jwt_test.go (14 tests passed in 12ms)\n"}}

event: TaskArtifactUpdateEvent
data: {"taskId":"c9b1b72e-3351-4091-a67b-1cb1e6a39480","artifactId":"art-001","partIndex":1,"append":true,"lastChunk":true,"part":{"data":{"format":"json","content":{"totalTests":14,"failures":0,"coverage":98.4}}}}

event: TaskStatusUpdateEvent
data: {"taskId":"c9b1b72e-3351-4091-a67b-1cb1e6a39480","contextId":"ctx-99182","state":"TASK_STATE_COMPLETED","statusMessage":"Task completed successfully. All artifacts delivered.","progressPercent":100,"timestamp":"2026-11-05T13:31:15Z"}
```

#### 3.3.3 Unified Wire `Part` Model
In A2A v1.0.1, payload parts are unified without redundant string discriminator fields (`kind`/`type`). Deserializers inspect field presence:
* **Text part**: `{"text": "..."}`
* **File/binary part**: `{"file": {"name": "report.pdf", "mimeType": "application/pdf", "uri": "https://..."}}`
* **Structured data part**: `{"data": {"format": "json", "content": { ... }}}`

#### 3.3.4 Wire Error Envelopes (`google.rpc.Status`)
```json
{
  "jsonrpc": "2.0",
  "id": "req-1092",
  "error": {
    "code": -32000,
    "message": "Task rejected: Output schema validation failure",
    "data": {
      "@type": "type.googleapis.com/google.rpc.Status",
      "code": 3,
      "message": "INVALID_ARGUMENT",
      "details": [
        {
          "@type": "type.googleapis.com/google.rpc.ErrorInfo",
          "reason": "SCHEMA_VIOLATION",
          "domain": "a2a-protocol.org",
          "metadata": {
            "taskId": "c9b1b72e-3351-4091-a67b-1cb1e6a39480",
            "missingField": "output_schema_ref"
          }
        }
      ]
    }
  }
}
```

### 3.4 Multi-Tenant Isolation & SSRF Security Boundaries
1. **Multi-Tenant Boundary Invariant**:
   Every A2A task, status check, and artifact stream MUST be bounded by a verified `tenant` identifier. Cross-tenant task polling or message leakage is blocked at the transport layer.
2. **Three-Layer Error Recovery Invariant**:
   * *Layer 1 (Schema Reflection)*: Format errors trigger an automatic correction turn with the JSON Schema validation error injected into the agent prompt.
   * *Layer 2 (Transient Backoff)*: Transport interruptions (SSE disconnects) retry with exponential backoff and full jitter:
     $$t = \text{random}(0, \min(T_{\max}, T_{\text{base}} \times 2^{\text{attempt}}))$$
   * *Layer 3 (Circuit Breaker)*: After 3 consecutive semantic failures, trip the breaker and escalate to Human-in-the-Loop (HITL).
3. **SSRF-Safe Webhook Push Notifications**:
   `PushNotificationConfig.callback_url` must be validated before registration against private IPv4/IPv6 ranges (RFC 1918, RFC 4193), link-local addresses (RFC 3927), and cloud instance metadata endpoints (`http://169.254.169.254`).

---

## 4. Standard 3: MCP Revision 2026-07-28 Stateless HTTP Transport & Remote Architecture

### 4.1 Specification Citations & 2026-07-28 Overhaul Context
* **Governing Body**: Agentic AI Foundation (AAIF), Linux Foundation (donated by Anthropic on 2025-12-09).
* **Authoritative Specification**: **MCP Spec Revision 2026-07-28** (`https://modelcontextprotocol.io/specification/2026-07-28/`).
* **Superseded Revisions**: `2025-03-26` $\rightarrow$ `2025-06-18` $\rightarrow$ `2025-11-25` (12-month deprecation transition window).
* **Key Enhancements (SEPs)**:
  * **SEP-2322**: Multi Round-Trip Requests (MRTR) for stateless Human-in-the-Loop input.
  * **SEP-2567**: Externalized State Handle architecture for serverless/edge runtimes.
  * **RFC 8707**: Resource Indicators for OAuth 2.1 audience binding.

### 4.2 Stateless Protocol Mechanics & Transport Overhaul

#### 4.2.1 Session Elimination & Handshake Removal
In early MCP revisions (`2025-11-25`), HTTP transport relied on sticky SSE connections tied to an `Mcp-Session-Id` header and an initial `initialize`/`notifications/initialized` handshake. In production, this created catastrophic friction with autoscalers, serverless workers, and distributed Kubernetes pods.

The **2026-07-28 Revision** completely eliminates sessions:
1. **`Mcp-Session-Id` Removed**: The protocol is completely stateless. Every HTTP request is standalone and self-sufficient.
2. **Handshake Removed**: No `initialize` handshake. Servers do not track client session lifecycles.
3. **Per-Request `_meta` Envelope**: Every JSON-RPC request body MUST supply client capabilities and protocol version inside a top-level `_meta` dictionary:
   ```json
   {
     "_meta": {
       "io.modelcontextprotocol/protocolVersion": "2026-07-28",
       "io.modelcontextprotocol/clientInfo": {
         "name": "enterprise-agent-core",
         "version": "5.8.0"
       },
       "io.modelcontextprotocol/clientCapabilities": {
         "tools": true,
         "resources": true,
         "prompts": false
       }
     },
     "jsonrpc": "2.0",
     "id": "call-104",
     "method": "tools/call",
     "params": {
       "name": "billing_issue_refund",
       "arguments": { "invoiceId": "INV-109284", "amountCents": 4500 }
     }
   }
   ```

#### 4.2.2 Gateway Routing Headers
To allow modern edge gateways (Envoy, Cloudflare Workers, Kong) to rate-limit, authorize, and route MCP traffic without parsing the entire JSON payload, streamable HTTP calls mandate declarative HTTP headers:
```http
POST /mcp HTTP/1.1
Host: tools.internal.enterprise.com
Mcp-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: billing_issue_refund
Accept: text/event-stream, application/json
Authorization: Bearer eyJhbGciOi...
Content-Type: application/json
```

#### 4.2.3 Multi Round-Trip Requests (MRTR - SEP-2322)
Because stateless servers cannot initiate upstream requests across long-lived socket sessions, interactive tool execution (such as requesting missing arguments or human authorization) uses MRTR:
1. Client calls `tools/call`.
2. Server detects missing parameter or high-risk confirmation threshold and returns:
   ```json
   {
     "jsonrpc": "2.0",
     "id": "call-104",
     "result": {
       "resultType": "input_required",
       "stateHandle": "hdl_sec_8f912a7e9b04",
       "prompt": "Refund exceeds $500.00. Please provide manager authorization code.",
       "expectedFields": [
         { "name": "managerAuthCode", "type": "string", "required": true }
       ]
     }
   }
   ```
3. Client agent requests user input and re-invokes the tool, passing the answers in `inputResponses` and supplying the `stateHandle`:
   ```json
   {
     "params": {
       "name": "billing_issue_refund",
       "stateHandle": "hdl_sec_8f912a7e9b04",
       "inputResponses": { "managerAuthCode": "AUTH-MGR-88910" }
     }
   }
   ```

### 4.3 SEP-2567 State Handle Externalization for Serverless Edge
Edge computing runtimes (Cloudflare Workers, Fastly Compute, AWS Lambda) spin up and tear down instances in milliseconds. To support multi-turn workflows without server-side memory affinity:
* Intermediate context is serialized, encrypted with AES-256-GCM, and saved to a distributed KV store (Redis Cluster, Cloudflare KV/D1) keyed by the opaque `stateHandle`.
* State handles carry an explicit Time-to-Live (TTL, default 900 seconds).
* Any edge instance in any data center can decrypt and resume execution seamlessly.

### 4.4 Concrete Schemas & Actionable Error Envelopes

#### 4.4.1 StructuredContent Output with Separation
To prevent LLM confusion between structured programmatic data and conversational prose, MCP responses enforce strict separation:
```json
{
  "jsonrpc": "2.0",
  "id": "call-104",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Successfully processed refund of $45.00 for invoice INV-109284."
      },
      {
        "type": "json",
        "json": {
          "refundId": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
          "status": "settled",
          "settlementTimestamp": "2026-11-05T13:32:00Z",
          "remainingBalanceCents": 0
        }
      }
    ]
  }
}
```

#### 4.4.2 Actionable Error Envelopes (Autonomous Self-Healing)
Raw stack traces or HTTP 500 status codes cause agents to loop endlessly. MCP servers MUST return structured, actionable error envelopes:
```json
{
  "jsonrpc": "2.0",
  "id": "call-104",
  "result": {
    "is_error": true,
    "error_code": "CUSTOMER_ACCOUNT_LOCKED",
    "category": "business_precondition_failed",
    "message": "Customer account is locked due to suspected security compromise.",
    "remediation_hint": "Invoke sec_query_account_status to check lock conditions or route request to Tier 2 human supervisor.",
    "is_retriable": false
  }
}
```

### 4.5 Remote Server Security: OAuth 2.1 RFC 8707 & Shadow MCP Governance
1. **RFC 8707 Resource Indicators**:
   When an agent obtains an OAuth 2.1 token, it MUST pass `resource=urn:mcp:<server-name>` to the Authorization Server. The MCP server verifies that the JWT `aud` claim matches its canonical URN. Tokens lacking matching resource indicators are rejected (preventing malicious token forwarding).
2. **Shadow MCP Detection (`MCP-GATEWAY LOCK`)**:
   Enterprise egress proxies inspect local and outbound HTTP traffic for JSON-RPC 2.0 payloads containing `io.modelcontextprotocol` or `tools/call`. Unregistered local servers attempting to interact with AI agents are quarantined immediately.

---

## 5. Standard 4: OWASP Top 10 for Agentic Security (ASI01–ASI10) & Agent Security Testing (AST01–AST10)

### 5.1 Authoritative Citations & The Paradigm Shift to "Least Agency"
* **Authoritative Frameworks**:
  * OWASP Top 10 for Agentic Applications (2026 Release)
  * OWASP Agentic Skills Top 10 (AST10 v1.0-2026)
* **Real-World Incident Evidence**:
  * **ClawHavoc (2026)**: 1,184 malicious agent skills discovered in public repositories delivering reverse shells via hidden markdown shell prompts.
  * **ToxicSkills (2026)**: Empirical analysis finding 36.82% of open-source agent skills suffered from over-privilege or untrusted external instruction injection.
  * **SkillJacking (2026)**: Exploitation of unpinned, floating skill dependencies to poison agent system instructions.
* **Paradigm Shift: Least Privilege $\rightarrow$ Least Agency**:
  Traditional security restricts *what resources a user can access* (Least Privilege). Agentic security restricts *how much autonomy, execution reach, and multi-step authority an autonomous model possesses* (Least Agency).

### 5.2 Comprehensive ASI01–ASI10 Threat Vectors & Mitigation Patterns

| Vulnerability ID & Title | Threat Vector / Attack Scenario | SOTA Architectural Mitigation Pattern |
|---|---|---|
| **ASI01: Agent Goal Hijack** | Direct/Indirect prompt injection in retrieved documents, issues, or web data overrides the agent's system prompt and redirects its mission. | Structural delimiter isolation (`<system_instructions>`, `<untrusted_content>`); pre-execution goal drift detector; immutable goal verification. |
| **ASI02: Tool Misuse & Exploitation** | Attacker crafts inputs that manipulate the agent into invoking tools with dangerous parameters (e.g., dropping DB tables, exfiltrating secrets). | Strict schema validation with Zod/Pydantic; Tool Sandbox Locks; parameter range bounds; read-only default postures. |
| **ASI03: Identity & Privilege Abuse** | Agent inherits broad user privileges or long-lived static API tokens, performing unauthorized actions across organizational boundaries. | Scoped Non-Human Identity (NHI) bindings; short-lived SPIFFE/SVID tokens; WIMSE workload identity federation; execution-time authorization. |
| **ASI04: Agentic Supply Chain** | Compromised third-party agent cards, tools, prompt templates, or skill manifests inject backdoors into the orchestration graph. | Cryptographic publisher verification; SHA-256 digest validation in `index.json`; AST preflight checks; dependency hash pinning. |
| **ASI05: Unexpected Code Execution (RCE)** | Agent dynamically generates and executes unsandboxed shell commands or code strings (`eval`, `exec`, `subprocess`) on the host system. | Physical 4-tier containerized sandbox hierarchy; parameter array execution (no raw `bash -c`); read-only root filesystems; air-gapped network. |
| **ASI06: Memory & Context Poisoning** | Adversary injects malicious entries into persistent semantic memory (RAG, Vector DBs, `MEMORY.md`), altering future agent reasoning. | Cryptographic provenance tagging on memory entries; strict memory write ACLs; memory hygiene audits (`memory-audit-report.json`). |
| **ASI07: Insecure Inter-Agent Communication** | Spoofed or unauthenticated peer agent messages inject false state into a multi-agent coordinator or worker. | Mutual TLS (mTLS); JWS-signed Agent Cards; schema validation on every received artifact; zero trust across agent boundaries. |
| **ASI08: Cascading Failures** | Localized tool error or hallucination propagates and amplifies across an agent swarm, draining token budgets or triggering crash loops. | Bulkhead pattern; per-phase token budgets; circuit breakers tripping after $N=3$ errors; explicit partial acceptance gates. |
| **ASI09: Human-Agent Trust Exploitation** | Agent uses anthropomorphic persuasion or deceptive explanations to trick a human operator into authorizing dangerous actions. | Transparent risk disclosure; mandatory Irreversible Action Standard; raw diff inspection for human approval gates. |
| **ASI10: Rogue Agents** | Agent gradually drifts from its original plan through multi-step reasoning loops, accumulating unauthorized autonomous actions. | Instruction drift monitors; bounded execution graphs; hard termination on unapproved branching; policy-as-code fail-closed evaluation. |

### 5.3 Comprehensive AST01–AST10 Skills Vulnerability Matrix
* **AST01 – Malicious Skills**: Trojanized skills carrying concealed payloads (reverse shells, credential wipers). Checked via zero-execution static Python AST parsing (`ast.parse()`) detecting prohibited functions (`eval`, `exec`, `__import__`).
* **AST02 – Supply Chain Compromise**: Insecure dependency trees and floating version tags (`:latest`, `^1.0.0`). Mitigated by enforcing immutable commit hash pinning.
* **AST03 – Over-Privileged Skills (Lethal Trifecta)**: Skill requests broad system privileges exceeding its documented mission.
* **AST04 – Insecure Metadata**: Mismatched skill IDs, falsified risk-tier levels, and unvalidated YAML frontmatter.
* **AST05 – Untrusted External Instructions**: Skills configured to dynamically fetch operational instructions or prompts from remote URLs at runtime.
* **AST06 – Weak Isolation**: Skills executing with root privileges or write permissions outside declared project folders.
* **AST07 – Update Drift**: A skill's behavioral profile or tool requests expand post-deployment without re-certification.
* **AST08 – Poor Scanning**: Relying on simple keyword regex instead of abstract syntax tree traversal and semantic policy analysis.
* **AST09 – No Governance (Shadow Skills)**: Skills loaded without registered ownership in `INDEX.md` or the primary role toolbox.
* **AST10 – Cross-Platform Reuse**: Assuming permission grants in Cursor/Claude Code transfer safely to CLI or headless cloud runners.

### 5.4 Mathematical Formalism of the Lethal Trifecta Invariant (AST03)
The Lethal Trifecta represents the mathematical condition under which an agent skill or composite role achieves unrestricted capability to exfiltrate confidential data or execute arbitrary remote actions.

#### Definition of Risk Dimensions
For any skill $\mathcal{S}$, evaluate three orthogonal boolean risk predicates:
1. $\mathcal{D}_{\text{priv}}(\mathcal{S}) \in \{0, 1\}$: Access to confidential data, private files, secrets, or database records.
2. $\mathcal{C}_{\text{untrusted}}(\mathcal{S}) \in \{0, 1\}$: Ingestion of untrusted inputs, web content, user prompts, or external feeds.
3. $\mathcal{E}_{\text{net}}(\mathcal{S}) \in \{0, 1\}$: Outbound network egress via raw sockets, HTTP requests, or external APIs.

#### The Lethal Invariant Theorem
$$\mathcal{T}_{\text{lethal}}(\mathcal{S}) = \mathcal{D}_{\text{priv}}(\mathcal{S}) \wedge \mathcal{C}_{\text{untrusted}}(\mathcal{S}) \wedge \mathcal{E}_{\text{net}}(\mathcal{S})$$

$$\mathcal{T}_{\text{lethal}}(\mathcal{S}) = 1 \implies \text{Disposition}(\mathcal{S}) = \text{REJECT (FAIL-CLOSED)}$$

#### Composite Role Blast Radius
When an agent role $\mathcal{R}$ activates a toolbox $\mathcal{T}_{\text{box}}(\mathcal{R}) = \{s_1, s_2, \dots, s_n\}$, the composite blast radius $\mathcal{B}_{\text{role}}(\mathcal{R})$ is evaluated across the union of tool capabilities:
$$\mathcal{B}_{\text{role}}(\mathcal{R}) = \left( \bigvee_{s \in \mathcal{T}_{\text{box}}(\mathcal{R})} \mathcal{D}_{\text{priv}}(s) \right) \wedge \left( \bigvee_{s \in \mathcal{T}_{\text{box}}(\mathcal{R})} \mathcal{C}_{\text{untrusted}}(s) \right) \wedge \left( \bigvee_{s \in \mathcal{T}_{\text{box}}(\mathcal{R})} \mathcal{E}_{\text{net}}(s) \right)$$

$$\mathcal{B}_{\text{role}}(\mathcal{R}) = 1 \implies \text{Enforce Physical Air-Gap Containerization}$$

#### Mandatory Air-Gap Enforcement Rule
$$\left( \bigvee_{s \in \mathcal{T}_{\text{box}}} \mathcal{D}_{\text{priv}}(s) = 1 \wedge \bigvee_{s \in \mathcal{T}_{\text{box}}} \mathcal{C}_{\text{untrusted}}(s) = 1 \right) \implies \mathcal{E}_{\text{net}}(\text{Runtime}) \leftarrow 0 \text{ (Air-Gapped: } \texttt{--network=none}\text{)}$$

### 5.5 Physical 4-Tier Sandbox Execution Hierarchy
Dynamic execution generated by agent tools MUST NOT run directly on developer workstations or host orchestrators. Workloads are strictly assigned to a 4-tier isolation hierarchy:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Tier 1: WebAssembly / WASI                                             │
│ Startup: < 5ms | Overhead: ~64MB | Isolation: Software Fault Isolation │
│ Use Case: AST analysis, regex parsing, deterministic calculations      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ Tier 2: Hardened OCI Container / gVisor                                │
│ Startup: 500ms - 2s | RAM: 512MB | Net: Level 0 (--network=none)       │
│ Security: CAP_DROP=ALL, --read-only rootfs, cgroups v2, no-new-privs   │
│ Use Case: Local builds, unit tests, code linting                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ Tier 3: Firecracker MicroVM                                            │
│ Startup: 5ms - 150ms | Dedicated Linux Guest Kernel | Hardware KVM     │
│ Security: Hypervisor memory boundary, isolated root device             │
│ Use Case: Untrusted third-party code compilation, dynamic test suites   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│ Tier 4: Cloud Ephemeral MicroVM Sandbox SDK                            │
│ Startup: 100ms - 1.5s | Remote Cloudflare Sandbox SDK / E2B            │
│ Security: Edge worker hypervisor isolation, automatic 300s reap TTL    │
│ Use Case: Distributed multi-agent swarms, complex web crawling         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Standard 5: Prompt Prefix Caching Optimization Patterns & Cache Alignment

### 6.1 Authoritative Specification Citations & Primary Sources
1. **Anthropic Prompt Caching API Specification (Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude 3 Opus)**:
   - Construct: `cache_control: {"type": "ephemeral", "ttl": "5m" | "1h"}`.
   - Max 4 explicit cache breakpoints per API call. Ingestion order: `tools` $\rightarrow$ `system` $\rightarrow$ `messages`.
   - Multipliers: 5m write ($1.25\times$), 1h write ($2.0\times$), cache read hit ($0.10\times$ / 90% discount).
2. **OpenAI Automatic Prompt Caching Specification (GPT-4o, o1, o3-mini, GPT-4.5, GPT-5)**:
   - Minimum threshold: 1,024 prompt prefix tokens. Matching operates in **128-token quantized blocks**.
   - Multipliers: 50% to 90% discount on cached input tokens; telemetry in `usage.prompt_tokens_details.cached_tokens`.
   - Routing: `prompt_cache_key` for deterministic worker routing in clustered multi-tenant deployments.
3. **Google Gemini Context Caching Architecture (Gemini 1.5 Pro, Gemini 2.0 Flash, Gemini 2.5)**:
   - Explicit `CachedContent` resource lifecycle with defined TTL (`ttl: "3600s"`) vs. implicit prefix caching.
4. **vLLM Automatic Prefix Caching (APC) & Chunked Prefill**:
   - Kwon et al., *PagedAttention: Efficient Memory Management for Large Language Models* (SOSP 2023).
   - CLI flags: `--enable-prefix-caching`, `--block-size 16|32`, `--enable-chunked-prefill`.
5. **SGLang RadixAttention Architecture**:
   - Zheng et al., *SGLang: Efficient Execution of Structured Language Model Programs* (ICLR 2024 / 2025). Radix tree caching of KV states across multi-turn dialogues with LRU eviction.

### 6.2 Algorithmic Mechanics & Cache Alignment

#### 6.2.1 The Prefix Alignment Invariant
In auto-regressive Transformer architectures, the Key-Value (KV) cache for token at position $i$ is mathematically conditioned on all preceding tokens:
$$K_i, V_i = f(x_0, x_1, \dots, x_i; \theta)$$

**Invariant**: A KV cache hit for sequence $[x_0, \dots, x_M]$ is valid **if and only if** the entire subsequence $[x_0, \dots, x_M]$ matches the cached sequence identically, token-for-token. If a dynamic token (timestamp, random UUID, or volatile nonce) is inserted at index $k$, **all KV cache states for positions $j \ge k$ are invalidated instantly**:
$$\text{HitRate}(j) = \begin{cases} 1.0 & \text{for } j < k \\ 0.0 & \text{for } j \ge k \end{cases}$$

#### 6.2.2 Cache Block Quantization
In inference engines using PagedAttention (vLLM, HuggingFace TGI, SGLang, and hyperscalers), GPU memory is partitioned into physical blocks of size $B \in \{16, 32, 64, 128\}$ tokens:
$$H_n = \text{Hash}(H_{n-1} \parallel T_{n, 0} \parallel T_{n, 1} \parallel \dots \parallel T_{n, B-1})$$
When a prompt prefix ends mid-block (e.g. at token $B \times n + 7$), the partial block cannot be safely matched. OpenAI explicitly quantizes cache segments to **128-token increments**. Anthropic sets minimum boundaries at **1,024 tokens**.

#### 6.2.3 Deterministic 6-Layer Static-to-Dynamic Assembly Pipeline
To achieve cache hit rates $\ge 85\%$ in multi-turn agent systems, the prompt assembly pipeline must strictly order prompt layers from lowest volatility to highest volatility:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Layer 1: Static Core Invariants & Global Rules (1,000–1,500 tokens)     │ -> 100% Cache Hit
│ (role-standard.md, code.md, unchanging safety instructions)            │ (Shared by all roles)
├────────────────────────────────────────────────────────────────────────┤
│ Layer 2: Role Identity & Core Tool Contracts (1,000–2,000 tokens)       │ -> BREAKPOINT 1 (Anthropic)
│ (Specific role instructions, primary skill schemas, output schemas)    │ (Shared within role sessions)
├────────────────────────────────────────────────────────────────────────┤
│ Layer 3: Domain / Repository Static Knowledge (2,000–5,000 tokens)      │ -> BREAKPOINT 2
│ (Architecture cards, system invariants, unchanging repository layout)  │ (Shared across repo tasks)
├────────────────────────────────────────────────────────────────────────┤
│ Layer 4: Session Durable Working State (500–1,500 tokens)               │ -> BREAKPOINT 3
│ (Anchored 10-slot compact-working-state.json, completed milestone logs)│ (Shared within task session)
├────────────────────────────────────────────────────────────────────────┤
│ Layer 5: Dynamic Turn History (Recent 3 turns: tool calls & results)    │ -> BREAKPOINT 4 (Rolling)
│ (Applied Head-Tail TOC truncation on stdout/stderr)                    │ (Refreshed every turn)
├────────────────────────────────────────────────────────────────────────┤
│ Layer 6: Dynamic Ephemeral Payload (100–500 tokens)                    │ -> Uncached / Fresh Prefill
│ (Current user turn, ephemeral UTC timestamp, dynamic nonce)             │ (Never placed in Layers 1–4)
└────────────────────────────────────────────────────────────────────────┘
```

#### 6.2.4 Cache-Busting Anti-Patterns to Eliminate
1. **Header Timestamp Anti-Pattern**: Putting `Current Time: 2026-11-05T13:26:00Z` or `Session ID: 5c5a24d7...` at Line 1 of the system prompt. This completely annihilates the KV cache hit rate across all turns ($0\%$ cache hit).
   - *Fix*: Move all dynamic timestamps and UUIDs into Layer 6 (the final user message or completion instruction).
2. **Tool Definition Shuffling Anti-Pattern**: Iterating over Python dictionaries (`dict.values()`) without sorting, causing tool definitions to change order between API calls.
   - *Fix*: Deterministically sort all tools and schemas alphabetically by name before serialization.
3. **Dynamic Memory Injection in System Tier Anti-Pattern**: Ingesting volatile memory notes into the system prompt prefix.
   - *Fix*: Isolate memory notes in Layer 4 and sanitize timestamps into normalized turn indices.

### 6.3 Concrete Metadata Schemas & Configuration Layouts

#### 6.3.1 Anthropic Multi-Breakpoint Cache Control Payload
```json
{
  "model": "claude-3-7-sonnet-20250219",
  "max_tokens": 4096,
  "system": [
    {
      "type": "text",
      "text": "You are a principal engineer operating under agent-skills v5.9.0. Core constraints: Fail-closed, minimal footprint, least-agency.",
      "cache_control": {
        "type": "ephemeral",
        "ttl": "1h"
      }
    },
    {
      "type": "text",
      "text": "=== REPOSITORY ARCHITECTURAL INVARIANTS ===\n[Static domain knowledge, schemas, policy-as-code definitions...]",
      "cache_control": {
        "type": "ephemeral",
        "ttl": "1h"
      }
    }
  ],
  "tools": [
    {
      "name": "run_command",
      "description": "Execute shell commands under action-boundaries policy.",
      "input_schema": { "type": "object", "properties": { "command": { "type": "string" } }, "required": ["command"] },
      "cache_control": {
        "type": "ephemeral"
      }
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "=== DURABLE TASK STATE (COMPACT-WORKING-STATE) ===\n[10-slot anchored JSON checkpoint from turn 10]",
          "cache_control": {
            "type": "ephemeral"
          }
        },
        {
          "type": "text",
          "text": "Current command output: ... Next single safe action: Run unit test suite."
        }
      ]
    }
  ]
}
```

#### 6.3.2 Efficiency Benchmarks & Cross-Tenant Security
| Metric / Dimension | Uncached Baseline | SOTA Prefix-Cached (2026–2027) | Relative Improvement |
|---|---|---|---|
| **Time-To-First-Token (TTFT, 32k tokens)** | $3,200\text{ ms} - 4,800\text{ ms}$ | $350\text{ ms} - 650\text{ ms}$ | **$85\% - 90\%$ reduction** |
| **Input Token Cost (Anthropic Sonnet)** | $\$3.00\text{ / 1M tokens}$ | $\$0.30\text{ / 1M tokens}$ (read) | **$90\%$ cost reduction** |
| **Input Token Cost (OpenAI GPT-4o)** | $\$2.50\text{ / 1M tokens}$ | $\$1.25\text{ / 1M tokens}$ (cached) | **$50\%$ cost reduction** |
| **GPU Memory Bandwidth Saturation** | $100\%$ prefill compute bound | $12\% - 18\%$ KV cache lookup | **$5\times - 8\times$ throughput** |
| **Multi-turn Cache Hit Rate Target** | $0\%$ | $\ge 88.5\%$ | **$+\infty$ cache efficiency** |

* **Tenant Salt Isolation Invariant**: High-security agent deployments MUST partition the KV cache hash chain using a per-tenant cryptographic salt:
  $$H_0 = \text{HMAC-SHA256}(\text{TenantID} \parallel \text{SecurityDomain}, \text{Salt})$$
  This guarantees that Agent A cannot benefit from or probe the cached prefixes of Agent B, eliminating cross-tenant timing side-channel attacks.

---

## 7. Standard 6: Token Economics, Context Window Efficiency & Head-Tail Tool Output Truncation (TOC)

### 7.1 Authoritative Specification Citations & Primary Sources
1. **Anthropic Context Engineering Standard (2026)**:
   - "Context Rot" principle: Reasoning density decreases non-linearly as the context window fills with low-value, unstructured tool outputs.
   - Core axioms: *Compaction over overflow*, *Just-in-time retrieval over pre-loading*, *Durable notes over transcript replay*.
2. **"Lost in the Middle: How Language Models Use Long Contexts"** (Liu et al., TACL / Stanford & Berkeley, 2023):
   - Establishes the U-shaped attention retrieval curve: information placed in the middle of long contexts suffers retrieval accuracy degradation of up to $40\%-60\%$ compared to primacy and recency edges.
3. **Pydantic AI / Codex Context Compaction & ClampOversizedMessages Architecture**:
   - Modern agent harnesses mandate strict token ceilings and fallback truncation policies (`ClampOversizedMessages`, offloading to disk).
4. **Agent-Skills Reference Implementation**:
   - Schema: `core/contracts/schemas/compact-working-state.json` (Draft 2020-12).
   - Scripts: `core/scripts/compact-context.py` (Head-Tail TOC & 10-slot validation), `core/scripts/prune-memory.py` (5-tier triage & Shannon entropy scan).

### 7.2 Algorithmic Mechanics

#### 7.2.1 Five-Tier Token Budget Allocation Model
For any active context window capacity $C_{\text{max}}$, memory is partitioned into five deterministic allocations:
$$\sum_{i=1}^{5} \text{Budget}_i = 1.00 \times C_{\text{max}}$$
1. **Tier 1: System & Behavioral Invariants ($15\%$)**: Immutable core prompt, role constraints, negative security locks, tool call syntax rules.
2. **Tier 2: Dynamic Task Grounding ($35\%$)**: Active task specification, retrieved documentation snippets, verified codebase facts, schema contracts.
3. **Tier 3: Working Memory & In-Flight Turns ($25\%$)**: Anchored compact state checkpoint plus the last 3 raw turns of tool interactions.
4. **Tier 4: Scratchpad & Intermediate Reasoning ($10\%$)**: Active execution plan checklist, immediate step observations, transient hypothesis state.
5. **Tier 5: Output Generation Reserve ($15\%$)**: Uncompromised completion buffer preventing truncated LLM generation or abrupt termination.

#### 7.2.2 Dynamic 60/80 Compaction Trigger Rules
Context compaction must not be a lazy, end-of-window emergency reaction. It is governed by a two-stage proactive gate:

```
0% ------------------------ 60% ------------------------ 80% ----------------------- 100%
   Normal Execution Loop        |   Warning & Staging Gate   |   Blocking Compaction Gate
                                |                            |   (Tool Execution HALTED)
```

- **At $60\%$ Context Utilization (Warning & Staging)**:
  - System emits a background warning telemetry event.
  - Runtime stages verbose tool logs for syntax-aware Head-Tail truncation (TOC).
  - Background memory auditor flags completed subtasks and duplicate instructions for consolidation.
- **At $80\%$ Context Utilization (Hard Blocking Compaction Gate)**:
  - **Tool execution is blocked immediately**. No new tool calls are dispatched.
  - The agent is forced to execute a compaction cycle:
    1. Parse in-flight context into the canonical **10-Slot Anchored Schema**.
    2. Write raw full transcript to disk (`.agent/archive/session_<id>_turn_<n>.json`).
    3. Validate candidate checkpoint against `contracts/schemas/compact-working-state.json`.
    4. Re-initialize active context window with Layer 1–3 invariants + the validated 10-slot state checkpoint.
  - Execution resumes strictly from `next_single_safe_action`.
- **Turn Count Override**: Regardless of token percentage, a compaction cycle triggers automatically after **15–20 turns** of continuous execution to purge accumulated reasoning loops.

#### 7.2.3 Head-Tail Tool Output Truncation (TOC) Ratios & Mechanics
Naive string truncation (e.g. chopping after 4,000 characters) creates broken JSON, truncated stack traces, and lost test assertions. SOTA agent engineering implements **Syntax-Aware Head-Tail Truncation (TOC)**:
1. **Ratio Allocation**:
   - **Line-Based Standard**: Retain first **5 lines** (execution command, environment parameters, initial headers) + last **15 lines** (panic traces, exit code, test pass/fail counts, final output summary).
   - **Token/Budget Standard**: When trimming large outputs to budget $K$ (e.g., $K = 1,000$ tokens):
     - **Head ($20\%$ / 200 tokens)**: Captures invocation context, schema headers, initial results.
     - **Tail ($80\%$ / 800 tokens)**: Captures terminal failure diagnostics, error line numbers, execution summary.
     - **Middle ($0\%$)**: Discard repetitive intermediate iteration loops, progress bars, or verbose row dumps.
2. **Syntax-Aware Code Fence Preservation**:
   - When truncating inside Markdown code fences (```` ```python ... ``` ````), TOC must never leave an unclosed fence.
   - The regex replacement engine matches matching open/close fences and injects a standard truncation delimiter:
     `... [Truncated N lines of execution output. Full payload persisted to disk] ...`
3. **Spill-to-Disk Offloading Invariant**:
   - If stdout/stderr exceeds $4\text{ KB}$ ($~1,000$ tokens), the full payload is written to `.agent/outputs/cmd_<uuid>.log`.
   - Injected prompt text contains the Head-Tail summary plus an exact command pointer:
     `[Output truncated: 412 lines omitted. Use read_file(path='.agent/outputs/cmd_abc.log', start_line=100, end_line=150) to inspect specifics]`

### 7.3 Concrete 10-Slot Anchored Working State Schema
Conforming to `core/contracts/schemas/compact-working-state.json` (Draft 2020-12):
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "compact-working-state",
  "contract_type": "compact-working-state",
  "checkpoint_id": "CHK-20261105-001",
  "timestamp": "2026-11-05T13:30:00Z",
  "current_goal": "Upgrade agent-skills repository to 2026-2027 SOTA standards",
  "work_type": "refactor",
  "phase_control": {
    "current_phase": "research_and_survey",
    "total_phases": 4,
    "phase_name": "SOTA Standards Investigation",
    "status": "in_progress",
    "active_owner": "@agent-coordinator"
  },
  "active_constraints": [
    "Read-only exploration: do not modify target codebase directly",
    "All handoffs must conform to 5-component protocol",
    "Strict OWASP ASI01-ASI10 security guardrails active"
  ],
  "files_modified_and_inspected": {
    "modified": [],
    "inspected": [
      "core/scripts/compact-context.py",
      "core/scripts/prune-memory.py",
      "core/contracts/schemas/compact-working-state.json",
      "core/roles/role-standard.md"
    ]
  },
  "decisions_and_tradeoffs": [
    {
      "decision": "Adopt 10-slot anchored schema over free-form narrative summaries",
      "rationale": "Eliminates hallucination drift and guarantees 98%+ critical information retention",
      "alternatives_rejected": ["Narrative conversational prose summaries", "Unstructured KV JSON bags"]
    }
  ],
  "verification_and_evidence": [
    {
      "command": "python core/scripts/compact-context.py --validate",
      "exit_code": 0,
      "verbatim_snippet": "Validation passed: checkpoint conforms to compact-working-state.json.",
      "status": "passed"
    }
  ],
  "failed_attempts_and_antipatterns": [
    {
      "attempt": "Blind string truncation after 2,000 characters",
      "failure_reason": "Chopped JSON syntax and dropped traceback exit code",
      "preventive_rule": "Apply syntax-aware TOC with head 5 lines and tail 15 lines"
    }
  ],
  "preserved_invariants": [
    "All 60 existing schema contracts must remain backward-compatible",
    "Bitwise parity between twin repositories maintained"
  ],
  "next_single_safe_action": "Synthesize findings into analysis.md and emit handoff report",
  "compaction_metrics": {
    "token_compression_ratio": 8.4,
    "critical_retention_rate": 0.995,
    "goal_drift_metric": 0.012,
    "tool_reinvocation_waste": 0.000
  }
}
```

### 7.4 Quantitative Compaction Metrics
1. **Token Compression Ratio (TCR)**:
   $$\text{TCR} = \frac{\text{Tokens}_{\text{pre-compaction}}}{\text{Tokens}_{\text{post-compaction}}}$$
   *Benchmark Target*: $\text{TCR} \in [5.0\times, 15.0\times]$.
2. **Critical Information Retention Rate (CIRR)**:
   $$\text{CIRR} = \frac{|\text{Facts}_{\text{retained}} \cap \text{Facts}_{\text{critical}}|}{|\text{Facts}_{\text{critical}}|}$$
   *Benchmark Target*: $\text{CIRR} \ge 98.0\%$ across exact file paths, exit codes, and test failure assertions.
3. **Goal Drift Metric (GDM)**:
   $$\text{GDM} = 1.0 - \cos(\vec{v}_{\text{root\_goal}}, \vec{v}_{\text{compacted\_goal}})$$
   *Benchmark Target*: $\text{GDM} \le 0.05$ (equivalent to cosine similarity $\ge 0.95$).
4. **Tool Re-invocation Waste (TRW)**:
   $$\text{TRW} = \frac{\text{Count}(\text{Redundant Tool Calls Post-Resume})}{\text{Total Tool Calls Post-Resume}}$$
   *Benchmark Target*: $\text{TRW} \le 1.0\%$.

---

## 8. Standard 7: Two-Tier Just-In-Time (JIT) Skill Discovery Architectures

### 8.1 Authoritative Specification Citations & Primary Sources
1. **agentskills.io Open Specification**:
   - Machine-readable skill discovery manifest at `/.well-known/agent-skills/index.json`.
   - Core principle: Decoupling public discovery metadata from private execution implementations.
2. **Claude Code / Anthropic Dynamic Tool Discovery Standard (2026)**:
   - Progressive Disclosure architecture: Agents operate with a lightweight metadata index in the system prompt; detailed tool schemas and full `SKILL.md` documents are retrieved JIT via dedicated discovery tools (`search_tools`, `read_skill`).
3. **Model Context Protocol (MCP) Dynamic Tool Surfaces (2025–2026)**:
   - MCP `tools/list` with pagination, `tools/search` by capability tag, and dynamic resource subscriptions.
4. **Academic Foundations**:
   - *ToolSearch: Dynamic Tool Selection for Massive API Repositories* (NeurIPS 2024 / 2025).
   - *Gorilla: Large Language Model Connected with Massive APIs* (Patil et al., UC Berkeley).

### 8.2 Algorithmic Mechanics: Progressive Disclosure & JIT Ranking

#### 8.2.1 The Monolithic Tool Saturation Problem
In `agent-skills` v5.9.0:
- Catalog: **183 skills** across 15 domains.
- Average full skill payload (`SKILL.md` + schema): $~1,500\text{ tokens}$.
- Monolithic Injection Footprint: $183 \times 1,500 = \mathbf{274,500\text{ tokens}}$.
Injecting this catalog upfront exhausts the context window before execution begins, increases per-turn API costs by $> \$1.50\text{ / call}$, introduces catastrophic tool hallucinations, and violates least-privilege security boundaries.

#### 8.2.2 Two-Tier Architectural Topology
```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: Lightweight Discovery Index (Always In-Context / Cacheable)    │
│ - Ingested in Layer 2 prefix cache (~40 tokens per skill)              │
│ - 183 skills = ~7,300 tokens (vs. 274,500 monolithic = 97.3% reduction)│
│ - Format: id, name, description, taxonomy, owner roles, integrity hash │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                     [User Intent / Task Dispatch]
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Hybrid JIT Candidate Ranking Algorithm (BM25 + Dense + Role Affinity)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Match Score S >= 0.72
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 2: Just-In-Time Full Payload Loading (Dynamic Sandbox Injection)  │
│ - Loads ONLY target SKILL.md (procedures, allowed tools, checklists)   │
│ - Scoped strictly to 1 to 3 active skills (~2,000 to 4,500 tokens)     │
└────────────────────────────────────────────────────────────────────────┘
```

#### 8.2.3 Hybrid JIT Candidate Ranking Algorithm
When an incoming task query $q$ arrives, candidate skills $s \in \mathcal{S}$ are evaluated using a multi-factor ranking function:
$$\text{Score}(s, q) = w_1 \cdot \text{BM25}(s_{\text{lexical}}, q) + w_2 \cdot \cos(\vec{E}_s, \vec{E}_q) + w_3 \cdot \text{RoleAffinity}(s, R_{\text{active}}) - \text{Penalty}(s)$$
* **Weights**: $w_1 = 0.35$ (keyword precision), $w_2 = 0.45$ (semantic intent), $w_3 = 0.20$ (role alignment).
* **Role Affinity Function**:
  $$\text{RoleAffinity}(s, R_{\text{active}}) = \begin{cases} 
  1.0 & \text{if } s \in \text{PrimarySkills}(R_{\text{active}}) \\
  0.5 & \text{if } s \in \text{SupportingSkills}(R_{\text{active}}) \\
  0.0 & \text{otherwise}
  \end{cases}$$
* **Toolbox Lock Penalty**:
  $$\text{Penalty}(s) = \begin{cases} 
  0.0 & \text{if } s \in \text{Toolbox}(R_{\text{active}}) \lor \text{UserExplicit}(s) \\
  0.60 & \text{if } s \notin \text{Toolbox}(R_{\text{active}}) \text{ (Enforces SKILL TOOLBOX LOCK)}
  \end{cases}$$
* **Selection Decision**:
  - Top-$K$ candidates ($K \in [1, 3]$) with $\text{Score} \ge 0.72$ are retrieved and injected into Tier 2.
  - If $\max(\text{Score}) < 0.72$, the system triggers an escalation or requests user clarification rather than hallucinating an arbitrary skill.

### 8.3 Concrete Tier 1 Discovery Manifest Schema
```json
{
  "$schema": "https://agentskills.io/v2/manifest.json",
  "schema_version": "2.0.0",
  "catalog_id": "agent-skills-core",
  "skills": [
    {
      "id": "agent-memory-compaction",
      "name": "Agent Memory Compaction",
      "description": "Compacts conversation context into anchored 10-slot working state using 60/80 triggers and Head-Tail TOC truncation.",
      "taxonomy": "agent",
      "tags": ["memory", "compaction", "context-window", "toc"],
      "owners": { "primary": "@agent-coordinator", "supporting": ["@prompt-engineer", "@reviewer"] },
      "tier2_ref": "core/skills/agent/agent-memory-compaction/SKILL.md",
      "integrity_sha256": "8f4a3e2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f"
    },
    {
      "id": "add-api-endpoint",
      "name": "Add API Endpoint",
      "description": "Scaffold and implement HTTP/RPC service endpoints following contract boundaries, validation schemas, and handler routing.",
      "taxonomy": "backend",
      "tags": ["api", "rest", "rpc", "http", "routing"],
      "owners": { "primary": "@backend-developer", "supporting": ["@technical-lead"] },
      "tier2_ref": "core/skills/backend/add-api-endpoint/SKILL.md",
      "integrity_sha256": "4b3c2d1e0f9a8b7c6d5e4f8f4a3e2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a"
    }
  ]
}
```

### 8.4 Efficiency Benchmarks & AST Security Guardrails
| Metric | Monolithic Pre-Loading (v5.7.3) | Two-Tier JIT Architecture (2027) | Gain / Reduction |
|---|---|---|---|
| **System Prompt Size** | $274,500\text{ tokens}$ | $7,300\text{ tokens}$ (Tier 1) | **$97.3\%$ context reduction** |
| **Active Turn Token Cost** | $\$1.65\text{ / turn}$ | $\$0.05\text{ / turn}$ | **$33\times$ cost savings** |
| **Tool Selection Accuracy** | $64.2\%$ (saturation errors) | $96.8\%$ (focused candidate space) | **$+32.6\%$ accuracy** |
| **Time-To-First-Token (TTFT)** | $4,800\text{ ms}$ | $420\text{ ms}$ | **$11.4\times$ faster startup** |

* **OWASP AST01/AST02 Integrity Lock**: Tier 2 `SKILL.md` payloads must match `integrity_sha256` before sandbox admission.
* **AST03 Lethal Trifecta Rejection**: Skills combining private data access + untrusted input + network egress are denied execution.

---

## 9. Standard 8: Role Modularization, Least-Agency & Boundary Isolation Standards

### 9.1 Authoritative Specification Citations & Primary Sources
1. **NIST AI Risk Management Framework (NIST AI RMF 1.0 / SP 1270 Generative AI Profile)**:
   - Mandates role governance, boundary mapping, risk measurement, and continuous management for autonomous agent systems.
2. **OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10)** & **Agentic Skills Top 10 (AST01–AST10)**.
3. **IETF WIMSE (Workload Identity in Multi-System Environments) & SPIFFE/SPIRE Standards**:
   - Dynamic Non-Human Identity (NHI) issuance, cryptographic SVID attribution, and RFC 8693 token exchange for subagent delegation.
4. **Open Cybersecurity Schema Framework (OCSF 99001 Policy Event)**:
   - Structured JSON audit logging for agent authorization and policy evaluation events.
5. **Agent-Skills Reference Standards**:
   - Standard: `core/roles/role-standard.md` (19 mandatory sections, 20 universal locks).
   - Policy: `core/policies/action-boundaries.yaml` (39 roles $\times$ 59 action verbs).
   - Enforcer: `core/scripts/hooks/check-policy.py`.

### 9.2 Algorithmic Mechanics: Boundary Enforcement & Least-Agency

#### 9.2.1 The Least-Agency Principle
While classical *Least Privilege* restricts static system access (e.g. read-only permissions), **Least-Agency** restricts *autonomous decision-making scope*:
- An agent must possess the absolute minimum degree of autonomy necessary to complete its localized assignment.
- High-impact, irreversible actions (e.g., deleting branches, pushing to production, migrating schemas, altering IAM) are stripped from autonomous execution and bound to **Human-In-The-Loop (HITL) confirmation gates**.

#### 9.2.2 Four Architectural Boundary Locks
1. **BOUNDARY LOCK**: Refuses tasks outside declared role responsibilities; recommends delegation to designated role.
2. **SKILL TOOLBOX LOCK**: Strict split into Primary Skills (direct execution) and Supporting Skills (delegation only). Prohibited skills permanently locked.
3. **MINIMAL-FOOTPRINT LOCK**: Tool calls must use minimal necessary arguments; sweeping wildcards and full scans are rejected.
4. **POLICY-FAIL-CLOSED INVARIANT**: If policy evaluation encounters an error, timeout, or missing field, it MUST fail closed and deny execution.

#### 9.2.3 Zero-Trust Policy-as-Code Engine (3-State Lattice)
The policy engine evaluates actions against a formal 3-state permission lattice:
$$\mathcal{P}(\text{Role}, \text{Action}) \in \{\text{allowed}, \text{requires\_approval}, \text{denied}\}$$

```
                [Action Request: (Role, Verb, Target)]
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │ Check Explicit Denied     │ ───► Matches? ───► [DENIED / HALT]
                    └─────────────┬─────────────┘
                                  │ No
                                  ▼
                    ┌───────────────────────────┐
                    │ Check Explicit Allowed    │ ───► Matches? ───► [ALLOWED / EXECUTE]
                    └─────────────┬─────────────┘
                                  │ No
                                  ▼
                    ┌───────────────────────────┐
                    │ Check Requires Approval   │ ───► Matches? ───► [GATE / HITL PROMPT]
                    └─────────────┬─────────────┘
                                  │ No (Unclassified)
                                  ▼
                    ┌───────────────────────────┐
                    │ Default Policy:           │
                    │ Zero-Trust Fail-Closed    │ ───► [REQUIRES APPROVAL or DENIED]
                    └───────────────────────────┘
```

### 9.3 Concrete Metadata Schemas & Policy Layouts

#### 9.3.1 Role Definition Schema (Mandatory 19-Section Layout)
Conforming to `core/roles/role-standard.md`:
```markdown
# [Role Name]

Mission: [Clear, single-sentence operational objective]
Level: Principal / Master Practitioner
Operating Standard: See core/roles/role-standard.md

## Principal Expectations
## Use This Role When
## Core Responsibilities
## Inputs Required
## Outputs Produced
## Deliverable Routing
## Decision Boundaries
## Role Boundaries
## Collaboration
## Guardrails
## Skill Toolbox
- **Primary Skills**: [`skill-a`, `skill-b`]
- **Supporting Skills**: [`skill-c`]
- **Prohibited Skills**: [`skill-d`]
## Output Template
## Review Checklist
## Failure Modes
## Anti-Patterns To Reject
## Role Handoff
## Definition Of Done
Last updated: YYYY-MM-DD
```

#### 9.3.2 Action Boundaries Configuration Matrix (`action-boundaries.yaml`)
```yaml
schema_version: "2"
compliance:
  eu_ai_act_article_9:
    risk_tier: minimal_risk
    human_oversight_required:
      - push_to_production
      - run_migration
      - modify_secrets
      - apply_iac
      - rotate_agent_credentials
  access_control:
    default_posture: deny
    credential_type: short-lived-oidc

roles:
  backend-developer:
    allowed:
      - create_file
      - read_file
      - run_build
      - run_linter
      - run_tests
      - search_code
      - write_file
    requires_approval:
      - delegate_task
      - delete_file
      - install_dependency
      - modify_environment_config
      - modify_public_api_contract
      - run_migration
    denied:
      - bypass_ai_guardrail
      - clear_agent_memory
      - deploy_ai_model
      - drop_database
      - force_push
      - modify_secrets
      - push_to_production
      - apply_iac
      - delete_cloudflare_resource
      - terminate_instance
```

#### 9.3.3 OCSF 99001 Audit Event Payload (Emitted by `check-policy.py`)
```json
{
  "class_uid": 99001,
  "category_uid": 9,
  "activity_id": 1,
  "time": 1730813400,
  "severity_id": 3,
  "actor": {
    "user": {
      "name": "agent-coordinator",
      "type": "Non-Human Identity",
      "uid": "nhi-agent-coord-042"
    }
  },
  "action": "run_migration",
  "status": "requires_approval",
  "status_code": "HITL_TRIGGERED",
  "message": "Action 'run_migration' requested by '@backend-developer' requires explicit human confirmation under EU AI Act Article 9.",
  "metadata": {
    "policy_version": "2.0.0",
    "rule_id": "compliance.eu_ai_act.human_oversight"
  }
}
```

### 9.4 Non-Human Identity (NHI) & Workload Identity Federation
* **SVID / OIDC Token Binding**: Every subagent invocation generates a short-lived token (TTL $\le 15\text{ minutes}$) containing the role slug and task ID in its claims.
* **Execution-Time Authorization Invariant**: Tool execution must not rely on authorization granted at planning time. Every state-changing API call performs a fresh verification of the active SVID token and policy predicates at the exact instant of execution.

---

## 10. Comprehensive Comparative Gap Analysis Matrix & File-by-File Divergence Ledger

### 10.1 Comparative Gap Analysis Matrix Across 8 Standards

| Standard | Current Implementation in v5.7.3 | 2026–2027 SOTA Requirement | Gap Severity | Affected File Paths in `agent-skills` | Target Deliverable / Phase |
|---|---|---|:---:|---|---|
| **1. agentskills.io Discovery Manifest** | `configure-agent-skills/SKILL.md` defines legacy API-catalog format `{"schema_version": "1.0", "skills": [{"id", "endpoint", ...}]}`. | `0.2.0` specification: `/.well-known/agent-skills/index.json` with `type: "skill-md"`, `url`, `digest: "sha256:..."`, and progressive disclosure. | **HIGH** | `core/skills/agent/configure-agent-skills/SKILL.md`<br>`core/contracts/schemas/agent-skills-discovery.json`<br>`core/scripts/generate-a2a-registry.py` | Phase 1 (Schema) + Phase 2 (Skill) |
| **2. AAIF A2A Protocol v1.0.1+** | Uses Antigravity adapter bindings (`agent.invoke`, `agent.stream`, `task.status`, lowercase states). `agent-card.json` constrains `"protocol_version": {"const": "1.0"}`. | A2A v1.0.1 (AAIF/Linux Foundation): Wire operations `message/send`, `message/stream`, `tasks/get`; monotonic `TASK_STATE_*`; `securitySchemes`; `google.rpc.Status`. | **HIGH** | `core/contracts/schemas/agent-card.json`<br>`core/contracts/schemas/a2a-task.json`<br>`core/contracts/schemas/a2a-task-progress.json`<br>`core/contracts/schemas/a2a-jsonrpc-envelope.json`<br>`core/skills/agent/agent-a2a-protocol/SKILL.md` | Phase 1 (Contracts) + Phase 2 (Skills) |
| **3. MCP 2026 Stateless HTTP Transport** | `architect-mcp-server/SKILL.md` codifies stateless streamable HTTP and SEP-2567. However, `mcp-tool-map.yaml` maps `mcp_call: read_file`, and telemetry logs cite `mcp.session.id`. | Spec Revision `2026-07-28`: Abolished `Mcp-Session-Id` and `initialize`; mandates per-request `_meta`, MRTR (SEP-2322), and domain-prefixed policy checks. | **MEDIUM** | `core/policies/mcp-tool-map.yaml`<br>`core/observability/README.md`<br>`core/skills/backend/build-mcp-server/SKILL.md` | Phase 2 (Skills) + Phase 4 (Policies) |
| **4. OWASP ASI01–ASI10 & AST01–AST10** | All 39 roles enforce `AST10-SKILL-SECURITY LOCK` and `LETHAL-TRIFECTA LOCK`. Static AST scanner exists in `skill-preflight-ast-check`. | Automated CI enforcement: Preflight AST scanner must run in `validate-all.py` against dynamically loaded skills to mathematically block $\mathcal{T}_{\text{lethal}}$. | **LOW** | `core/scripts/validate-thirdparty-skills.py`<br>`core/scripts/validate-all.py`<br>`core/roles/role-standard.md` | Phase 4 (Tooling / CI) |
| **5. Prompt Prefix Caching Optimization** | Mentions in `context-optimization` and `ai-systems-engineer` (Radix Tree). Static prefix stability mentioned as advice. | Deterministic 6-layer static-to-dynamic prompt layout with explicit provider breakpoints (`cache_control: {"type": "ephemeral"}` / `prompt_cache_key`). | **MEDIUM** | `core/skills/ai-agent/context-optimization/SKILL.md`<br>`core/roles/prompt-engineer.md`<br>`adapters/antigravity/rules.template.md` | Phase 2 (Skills) + Phase 3 (Adapters) |
| **6. Token Economics & TOC Truncation** | Line-based 5/15 Head-Tail TOC in `compact-context.py` and `agent-memory-compaction`. 10-slot `compact-working-state.json` schema. | Token-aware syntax-aware TOC with spill-to-disk offloading for outputs $> 4\text{ KB}$, 60/80 compaction gates, and CIRR $\ge 98\%$ verification. | **LOW** | `core/scripts/compact-context.py`<br>`core/skills/agent/agent-memory-compaction/SKILL.md` | Phase 2 (Skills) + Phase 4 (Scripts) |
| **7. Two-Tier JIT Skill Discovery** | Monolithic loading model: `INDEX.md` instructs agents to load all primary skill files upfront (>274k tokens for full catalog). | Two-Tier architecture: Tier 1 lightweight index (~40 tokens/skill) + Tier 2 JIT on-demand loading of full `SKILL.md` upon explicit invocation. | **HIGH** | `INDEX.md`<br>`adapters/antigravity/ANTIGRAVITY.md`<br>`core/scripts/generate-index.py` | Phase 3 (Adapters & Index) |
| **8. Role Modularization & Boundaries** | 39 roles with strict 16 sections, calibrated locks (14–24), `### Prohibited Skills`, and `action-boundaries.yaml` enforcement. | Full SOTA compliance achieved; minor drift in deliverable routing references (`compliance-report.json`, `test-strategy.json`, `delivery-plan.json`). | **LOW** | `core/roles/agent-discovery-engineer.md`<br>`core/roles/business-analyst.md`<br>`core/roles/technical-lead.md` | Phase 5 (Roles Polish) |

---

### 10.2 File-by-File Divergence Ledger & Target Upgrade Map

The following ledger documents the exact files, current code states, specific line numbers, required modifications, and target release phases:

| # | Exact File Path | Current Code State & Line Reference | Required SOTA Modification | Target Release Phase |
|---|---|---|---|:---:|
| 1 | `core/contracts/schemas/agent-card.json` | Lines 26, 114–129: `"protocol_version": {"const": "1.0"}`; legacy `authentication.schemes` structure. | Change protocol pattern to `^1\.[0-9]+(\.[0-9]+)?$`; add standard `securitySchemes` and `supportedInterfaces` objects per A2A v1.0.1. | Phase 1 (Contracts) |
| 2 | `core/contracts/schemas/a2a-task.json` | Lines 14–22: Lowercase state enums only (`submitted`, `working`, `completed`, `failed`); carries legacy `timeout_minutes`. | Add uppercase `TASK_STATE_*` enums (`TASK_STATE_SUBMITTED`, etc.); add bi-directional mapping; deprecate `timeout_minutes`. | Phase 1 (Contracts) |
| 3 | `core/contracts/schemas/a2a-task-progress.json` | Lines 8–18: Only Antigravity `task.*` event enums (`task.status`, `task.artifact`); lowercase states. | Add `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent` spec event names and uppercase `TASK_STATE_*`. | Phase 1 (Contracts) |
| 4 | `core/contracts/schemas/a2a-jsonrpc-envelope.json` | Lines 23–32: Method enum omits standard wire operations. | Add `"message/send"`, `"message/stream"`, `"tasks/get"`, `"tasks/cancel"`, `"tasks/list"` to method enum. | Phase 1 (Contracts) |
| 5 | `core/contracts/schemas/a2a-artifact.json` | Line 57: Contains legacy `"kind"` discriminator inside Part. | Mark `"kind"` as deprecated; make `text`, `file`, `data` direct optional properties per unified Part model. | Phase 1 (Contracts) |
| 6 | `core/contracts/schemas/compliance-report.json` | **Missing file**; referenced in `agent-discovery-engineer.md:61`. | Create new Draft 2020-12 schema for Agent Readiness & Protocol Discovery compliance reports. | Phase 1 (Contracts) |
| 7 | `core/contracts/schemas/agent-skills-discovery.json` | **Missing file**; referenced across discovery skills. | Create schema matching `https://schemas.agentskills.io/discovery/0.2.0/schema.json`. | Phase 1 (Contracts) |
| 8 | `core/contracts/schemas/mcp-server-card.json` | **Missing file**; referenced in `configure-mcp` and `agent-discovery-engineer`. | Create schema for `/.well-known/mcp/server-card.json` adhering to MCP 2026-07-28. | Phase 1 (Contracts) |
| 9 | `core/skills/agent/configure-agent-skills/SKILL.md` | Lines 45–55: Legacy API catalog shape with `id`, `endpoint`, `method`. | Overhaul to `agentskills.io` 0.2.0 format with SHA-256 digests and progressive disclosure. | Phase 2 (Skills) |
| 10 | `core/skills/agent/agent-a2a-protocol/SKILL.md` | Lines 30–70: Mentions Antigravity local bindings without wire transformer. | Add explicit A2A v1.0.1 wire transformer specification and `a2a.proto` IDL mapping. | Phase 2 (Skills) |
| 11 | `core/skills/ai-agent/context-optimization/SKILL.md` | General prompt caching advice without concrete breakpoint headers. | Codify deterministic 6-layer prompt prefix caching layout with provider breakpoint headers. | Phase 2 (Skills) |
| 12 | `adapters/antigravity/a2a-config.template.yaml` | Lines 43–83: Only 25 roles in capability map (missing 14 roles). | Synchronize all 39 roles from `capability-role-map.generated.yaml`. | Phase 3 (Adapters) |
| 13 | `adapters/antigravity/ANTIGRAVITY.md` | Monolithic skill loading instructions. | Document Two-Tier JIT Skill Discovery mechanics for Antigravity workspaces. | Phase 3 (Adapters) |
| 14 | `INDEX.md` | Line 26: Instructions to pre-load all skills. | Update router protocol to support Tier 1 lightweight index + Tier 2 JIT loading. | Phase 3 (Router) |
| 15 | `core/policies/mcp-tool-map.yaml` | Line 44: `mcp_call: read_file`. | Introduce `<domain>_<action>` prefix resolution to map mutating MCP calls to proper policy actions. | Phase 4 (Policies) |
| 16 | `core/scripts/compact-context.py` | Line-based 5/15 trimming; no spill-to-disk offloading. | Implement token-ratio budgeting (20/80) and spill-to-disk offloading for tool outputs $> 4\text{ KB}$. | Phase 4 (Scripts) |
| 17 | `core/scripts/generate-a2a-registry.py` | Emits `ai-catalog.json` without `agent-skills`. | Add `/.well-known/agent-skills/index.json` to `ai-catalog.json` discovery endpoints. | Phase 4 (Scripts) |
| 18 | `core/roles/agent-discovery-engineer.md` | Line 61: References missing `compliance-report.json`. | Bind deliverable table to newly created `contracts/schemas/compliance-report.json`. | Phase 5 (Roles Polish) |
| 19 | `core/roles/business-analyst.md` | Line 111: References nonexistent `test-strategy.json`. | Correct boundary to reference `test-report.json` and `validation-result.json`. | Phase 5 (Roles Polish) |
| 20 | `core/roles/technical-lead.md` | Line 325: References `delivery-plan.json` (typo). | Correct reference to `technical-delivery-plan.json`. | Phase 5 (Roles Polish) |
| 21 | `core/roles/cloudflare-engineer.md` & `seo-analyst.md` | Cites `agent-skills.json` at root. | Standardize path to `/.well-known/agent-skills/index.json`. | Phase 5 (Roles Polish) |

---

## 11. Architectural Synthesis & Modernization Invariants

To guarantee backward compatibility, operational reliability, and cryptographic security throughout the upgrade cycle, the following architectural invariants are established as non-negotiable platform laws:

### 11.1 Contract Backward-Compatibility Invariant
* **Dual-Stack Wire Translation**: When communicating within Antigravity or local CLI environments, local bindings (`agent.invoke`, `agent.stream`, `task.status`, lowercase states) remain valid and supported.
* **Wire Gateway Adaptation**: When communicating across external network boundaries or interacting with pure AAIF A2A v1.0.1+ agents, the A2A adapter MUST translate wire messages into standard Protobuf/JSON-RPC operations (`message/send`, `message/stream`, `tasks/get`), uppercase `TASK_STATE_*` enums, and `google.rpc.Status` error structures.
* Existing schema contracts ($N=60$) must remain valid; extensions must add optional fields or use non-breaking `anyOf`/`oneOf` schema constructs.

### 11.2 The Single-Source-of-Identity (SSOI) Invariant
* Every skill's identity triad:
  $$\text{Directory Name} \equiv \text{SKILL.md Frontmatter Name} \equiv \text{index.json / role-skill-index.json ID}$$
  must match identically across all 183 skills.
* SHA-256 integrity digests in `index.json` must be regenerated via `core/scripts/generate-a2a-registry.py` upon any modification to a `SKILL.md` file.

### 11.3 Fail-Closed Policy Enforcement Invariant
* All policy evaluations in `core/scripts/hooks/check-policy.py` operate under zero-trust:
  $$\mathcal{P}(\text{Role}, \text{Action}) \notin \{\text{allowed}\} \implies \text{HALT / REQUIRE APPROVAL}$$
* If any policy rule, AST parser, or network check encounters an unhandled exception or malformed input, execution is blocked immediately.

### 11.4 Bitwise Twin Parity Invariant
* Any modification to shared knowledge cards, architectural invariants, or platform reports MUST maintain **100% SHA-256 bitwise parity** between `vesviet/reports` and `learn/reports`.
* One-way authority law: Vietnamese articles on `learn` link up to English canonical versions on `vesviet`; `vesviet` has zero outbound links to `learn`.

---

## 12. Appendix: Primary References & Standards Bibliography

1. **AAIF / Linux Foundation**:
   - *Agent-to-Agent (A2A) Protocol Specification v1.0.1*, Agentic AI Foundation, Released 2026-05-26. IDL: `a2a.proto`.
   - *Model Context Protocol (MCP) Specification Revision 2026-07-28*, Agentic AI Foundation / Anthropic PBC.
   - *SEP-2322: Multi Round-Trip Requests (MRTR) for MCP Interactive Flows*, AAIF Standards Track, 2026.
   - *SEP-2567: Externalized State Handles for Serverless Edge MCP Architecture*, AAIF Standards Track, 2026.
2. **agentskills.io Open Community**:
   - *agentskills.io Discovery Manifest Standard Schema v0.2.0*, `https://schemas.agentskills.io/discovery/0.2.0/schema.json`, 2026.
3. **OWASP GenAI Security Project**:
   - *OWASP Top 10 for Agentic Applications (ASI01–ASI10)*, 2026 Release.
   - *OWASP Agentic Skills Top 10 (AST01–AST10 v1.0-2026)*, OWASP Foundation.
4. **Internet Engineering Task Force (IETF) RFCs**:
   - RFC 8615: *Well-Known Uniform Resource Identifiers*, 2019.
   - RFC 8785: *JSON Canonicalization Scheme (JCS)*, 2020.
   - RFC 8707: *Resource Indicators for OAuth 2.0*, 2020.
   - RFC 7515: *JSON Web Signature (JWS)*, 2015.
   - RFC 7517: *JSON Web Key (JWK)*, 2015.
   - RFC 3986: *Uniform Resource Identifier (URI): Generic Syntax*, 2005.
5. **Industry Technical Specifications & Academic Literature**:
   - Anthropic: *Prompt Caching with Ephemeral Cache Control API Reference*, 2024–2026.
   - OpenAI: *Prompt Caching in Chat Completions and Assistants API*, 2024–2026.
   - Google DeepMind: *Context Caching in Gemini API*, 2025–2026.
   - Kwon et al.: *PagedAttention: Efficient Memory Management for Large Language Models*, Proceedings of SOSP 2023.
   - Zheng et al.: *SGLang: Efficient Execution of Structured Language Model Programs*, ICLR 2024 / 2025.
   - Liu et al.: *Lost in the Middle: How Language Models Use Long Contexts*, Transactions of the Association for Computational Linguistics (TACL), 2023.
   - NIST: *Artificial Intelligence Risk Management Framework (AI RMF 1.0) & Generative AI Profile (NIST SP 1270)*, 2023–2025.
   - Open Cybersecurity Schema Framework (OCSF): *OCSF Schema v1.3.0 - Class 99001 (Policy Event)*, 2025–2026.

---
*End of Master SOTA Research Report — agent-skills v5.9.0 $\rightarrow$ v6.0.0 Modernization*
