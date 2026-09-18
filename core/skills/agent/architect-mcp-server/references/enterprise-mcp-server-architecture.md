# Enterprise Model Context Protocol (MCP) Server Architecture Specification

## 1. Executive Architecture Overview

The Model Context Protocol (MCP) defines an open standard for secure, bi-directional communication between AI agent runtimes (clients) and backend tools, data sources, and services (servers). In enterprise environments, MCP servers transition from lightweight local scripts to distributed, multi-tenant microservices operating under zero-trust network architectures.

This specification establishes the architectural patterns, schema contracts, transport standards, state externalization mechanisms, and security boundaries required for production-grade enterprise MCP servers.

---

## 2. Tool Surface Contract Design & Ergonomics

### 2.1 Action-Oriented Naming & Namespacing
In large enterprise deployments hosting hundreds of tools across disparate microservices, LLMs face severe tool selection degradation if tool surfaces lack namespace discipline.
- **Naming Pattern**: Tools MUST strictly use `<domain>_<action>` snake_case syntax (e.g., `crm_get_customer`, `billing_issue_refund`, `github_create_pull_request`).
- **Disambiguation Descriptions**: Every tool description MUST clearly articulate:
  1. *Capability*: What the tool deterministically executes.
  2. *Intended Trigger*: The exact scenario when an agent should invoke the tool.
  3. *Negative Trigger*: Explicit anti-patterns when the tool must NOT be used (pointing to preferred sibling tools).

### 2.2 Atomic Granularity vs. God Tools
- **Single Responsibility Principle**: Prefer granular, single-purpose tools over monolithic composite tools containing complex branching logic.
- **Minimal Required Parameter Sets**: Keep required parameters to the absolute minimum necessary for execution. Optional parameters must feature explicit default behaviors in their schema definitions.

### 2.3 Strict Schema Definition (Zod & Pydantic v2)
Every MCP tool contract must be authored in Zod (TypeScript) or Pydantic v2 (Python) generating standard JSON Schema Draft 2020-12 representations. Freeform strings and untyped dictionaries are strictly prohibited.

#### TypeScript (Zod) Example:
```typescript
import { z } from "zod";

export const CustomerRefundInputSchema = z.object({
  customerId: z.string().uuid().describe("Unique UUID of the target customer account."),
  invoiceId: z.string().regex(/^INV-\d{6}$/).describe("Target invoice identifier formatted as INV-XXXXXX."),
  amountCents: z.number().int().positive().max(500000).describe("Refund amount in integer cents (USD). Must not exceed 500,000 cents ($5,000.00)."),
  reason: z.enum(["duplicate_billing", "fraudulent_charge", "customer_satisfaction", "service_outage"])
    .describe("Business justification code for the refund transaction."),
  idempotencyKey: z.string().min(16).max(64)
    .describe("Client-generated cryptographic UUID/hash preventing duplicate refund execution.")
}).strict();

export const CustomerRefundOutputSchema = z.object({
  refundId: z.string().uuid().describe("Unique identifier of the executed refund transaction."),
  status: z.enum(["succeeded", "pending_review", "declined"]),
  settlementTimestamp: z.string().datetime().describe("ISO-8601 UTC timestamp of settlement."),
  remainingBalanceCents: z.number().int().nonnegative().describe("Remaining balance on invoice post-refund.")
}).strict();
```

#### Python (Pydantic v2) Example:
```python
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid

class RefundReason(str, Enum):
    DUPLICATE_BILLING = "duplicate_billing"
    FRAUDULENT_CHARGE = "fraudulent_charge"
    CUSTOMER_SATISFACTION = "customer_satisfaction"
    SERVICE_OUTAGE = "service_outage"

class CustomerRefundInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: uuid.UUID = Field(..., description="Unique UUID of target customer account.")
    invoice_id: str = Field(..., pattern=r"^INV-\d{6}$", description="Invoice ID formatted as INV-XXXXXX.")
    amount_cents: int = Field(..., gt=0, le=500000, description="Refund amount in cents. Max 500,000 cents ($5,000.00).")
    reason: RefundReason = Field(..., description="Business justification code.")
    idempotency_key: str = Field(..., min_length=16, max_length=64, description="Client-generated idempotency key.")

class CustomerRefundOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    refund_id: uuid.UUID = Field(..., description="Unique identifier of executed refund.")
    status: str = Field(..., description="Transaction status.")
    settlement_timestamp: datetime = Field(..., description="ISO-8601 UTC settlement timestamp.")
    remaining_balance_cents: int = Field(..., ge=0, description="Remaining balance post-refund.")
```

### 2.4 OutputSchema & StructuredContent Separation
Enterprise MCP servers must enforce structured returns rather than stringified unstructured text dumps. MCP clients use the `outputSchema` to validate the returned JSON data.
- **Response Format**: Responses must separate structured JSON payloads from human-readable conversational explanations:
```json
{
  "content": [
    {
      "type": "text",
      "text": "Refund RF-90218 successfully processed for invoice INV-109284 in the amount of $45.00."
    },
    {
      "type": "json",
      "json": {
        "refundId": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "status": "succeeded",
        "settlementTimestamp": "2026-09-18T06:30:00Z",
        "remainingBalanceCents": 0
      }
    }
  ]
}
```

### 2.5 Actionable Error Ergonomics
When a tool call encounters an error, returning generic status codes (e.g. `500 Internal Server Error`) or unformatted stack traces causes LLM agents to either hallucinate fixes or terminate prematurely. Enterprise MCP servers implement structured error ergonomics:
```json
{
  "is_error": true,
  "error_code": "CUSTOMER_ACCOUNT_LOCKED",
  "category": "business_precondition_failed",
  "message": "Customer ID 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d is locked due to suspected security compromise.",
  "remediation_hint": "Invoke sec_query_account_status to check lock conditions or route request to Tier 2 human supervisor.",
  "is_retriable": false
}
```

---

## 3. Transport Architecture: Stateless Streamable HTTP

### 3.1 Protocol Evolution & Deprecation Policy
- **Spec Revision 2026-07-28**: Deprecates legacy stateful Server-Sent Events (SSE) connections with in-memory sticky sessions (`Mcp-Session-Id`) and dynamic client registration (RFC 7591).
- **Default Transport**: Enterprise MCP servers MUST implement Stateless Streamable HTTP transport over HTTPS.
- **Stdio Transport Boundary**: Stdio transport (`stdin`/`stdout` JSON-RPC 2.0 frames) is restricted strictly to local CLI developer environments, containerized desktop testing, and single-user IDE extensions. In stdio mode, all application logs, debug traces, and telemetry must route exclusively to `stderr`.

### 3.2 Gateway Header Routing
Enterprise API gateways (Envoy, Cloudflare Workers, Kong) route MCP traffic without unmarshaling entire JSON-RPC request bodies by inspecting standard gateway routing headers:
- `Mcp-Protocol-Version: 2026-07-28`
- `Mcp-Method: tools/call` (or `tools/list`, `resources/read`, `server/discover`)
- `Mcp-Name: crm_get_customer`
- `Accept: text/event-stream`
- `Authorization: Bearer <OAuth 2.1 Token>`

### 3.3 Chunked Transfer & Progress Streaming
Long-running tools (e.g. data warehouse queries, code synthesis, container builds) must stream progress notifications over chunked HTTP streaming to prevent gateway timeout drops:
```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Transfer-Encoding: chunked

event: progress
data: {"progressToken": 1, "progress": 25, "total": 100, "message": "Querying partition 2026-09..."}

event: progress
data: {"progressToken": 1, "progress": 85, "total": 100, "message": "Aggregating metrics..."}

event: result
data: {"content": [{"type": "json", "json": {"totalRows": 450000, "latencyMs": 1420}}]}
```

---

## 4. SEP-2567 State Handle Externalization

### 4.1 The Stateless Edge Imperative
Edge runtimes (Cloudflare Workers, Fastly Compute, AWS Lambda) spin up and tear down instances dynamically. Maintaining in-memory state or session maps on server instances is an anti-pattern.

### 4.2 State Handle Architecture (SEP-2567)
Under SEP-2567, all conversational context, pagination cursors, and multi-turn transaction states are decoupled from the server process and externalized to high-performance distributed key-value stores (Redis Cluster, Cloudflare D1/KV, DynamoDB):
1. **Initial Tool Invocation**: Tool completes partial work and returns an opaque cryptographic state handle (token) to the caller agent in the response envelope.
2. **Handle Storage**: The state handle maps to serialized, encrypted execution context in distributed storage with an explicit Time-to-Live (TTL, default 900s).
3. **Continuation Call**: The agent supplies `stateHandle: "<token>"` in subsequent tool calls. Any serverless instance in the global cluster decrypts the handle, resumes execution, and advances state.

---

## 5. Resource & Prompt Architectural Models

### 5.1 Resource Ingestion
Resources allow agents to ingest context without burning tool-calling round-trips:
- **URI Template Standard**: Declare deterministic URI templates:
  - `system://metrics/{hostname}/cpu`
  - `repo://{org}/{repo}/file/{filepath}`
  - `db://tenant/{tenantId}/schema`
- **MIME Type Negotiation**: Resources must declare standard MIME types (`application/json`, `text/markdown`, `text/csv`).
- **Subscription Architecture**: Subscriptions replace polling. Clients register interest via `subscriptions/listen`, and the server broadcasts change notifications when the underlying resource changes.

### 5.2 Parameterized Prompt Templates
Enterprise MCP servers publish standardized prompt workflows via `prompts/list` and `prompts/get`. These prompt templates allow centralized prompt engineering across agent teams:
- Templates validate arguments using JSON Schema.
- Prompts dynamically bind to local server resources and tools.

---

## 6. Security Model & Trust Perimeters

### 6.1 OAuth 2.1 with RFC 8707 Resource Indicators
In an enterprise agent ecosystem, an agent may hold a bearer token with broad permissions. If that token is passed to an untrusted MCP server, that server could maliciously replay the token against other corporate APIs.
- **RFC 8707 Resource Indicators**: The client agent MUST request an audience-restricted token specifying the exact MCP server URI:
  ```http
  POST /oauth/token HTTP/1.1
  Host: auth.enterprise.com
  Content-Type: application/x-www-form-urlencoded

  grant_type=authorization_code
  &code=SplxlOBeZQQYbYS6WxSbIA
  &client_id=agent-planner-service
  &code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
  &resource=urn:mcp:crm-billing-service
  ```
- **Audience Enforcement**: The MCP server validates that the decoded JWT `aud` claim matches its own canonical resource URI (`urn:mcp:crm-billing-service`). Tokens without matching resource indicators are rejected with HTTP 403.

### 6.2 Enterprise-Managed Authorization (EMA)
For deployments with $\ge 3$ MCP servers, authorization decisions must be offloaded from application code to an Enterprise-Managed Authorization gateway:
- Evaluates Open Policy Agent (OPA/Rego) or AWS Cedar policies.
- Validates tenant boundary, user clearance level, tool classification tier, and request parameter bounds.

### 6.3 Supply Chain Registry Vetting & SBOM
Production MCP servers must be vetted before deployment:
- Server images and packages must be signed via Cosign / Sigstore.
- Dependencies verified against Software Bill of Materials (SBOM) with zero critical/high CVEs.
- Manifests registered in the enterprise internal MCP registry.

### 6.4 Shadow MCP Detection & Quarantine
Developers or malicious actors may spin up unapproved MCP servers on local workstations or internal networks, exposing data to unauthorized AI models.
- **Gateway Telemetry**: Enterprise egress proxies inspect traffic for JSON-RPC 2.0 signatures containing `mcp_version`, `tools/call`, or `server/discover`.
- **Automatic Quarantine**: Unregistered MCP endpoints are blocked, and an alert is dispatched to SecOps (`MCP-GATEWAY LOCK`).
