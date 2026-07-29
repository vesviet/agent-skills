---
name: configure-mcp
description: Sets up the full MCP presence for a web service — experimental Server Card discovery, WebMCP browser provider component, and supporting host/route configuration — so AI clients auto-discover and connect without manual configuration. Use when registering a new MCP server, adding browser-side context sharing, updating tool capabilities, or debugging MCP client connectivity failures.
---

# Configure MCP

Use this skill to set up the full MCP presence for a web service: the server card at `/.well-known/mcp/server-card.json`, the WebMCP browser provider component, and the supporting host/route configuration. This makes AI clients (Claude, Copilot, custom agents) auto-discover and connect to the service's MCP server without manual configuration.

## Core Rules

- Server Cards are an **experimental MCP extension** (SEP-2127, `experimental-ext-server-card`), not part of the core spec. The extension's path is `/.well-known/mcp-server-card`. This pack additionally serves `/.well-known/mcp/server-card.json` for compatibility with existing scanners — serve both and treat neither as mandated by the core spec.
- Because Server Cards are experimental, verify the current extension status and path before relying on them for production discovery; prefer the Official MCP Registry when a client supports it.
- The server card JSON MUST include all required fields: `name`, `description`, `mcp_version`, `transport` (with `url` and `type`), and `capabilities`.
- WebMCP browser components should invoke `navigator.modelContext.provideContext()`. Note that `navigator.modelContext` is a W3C **draft proposal**, experimental and flag-gated in Chromium browsers only — feature-detect before calling, and treat a polyfill as a legitimate compatibility choice rather than a violation.
- Ensure the WebMCP component is mounted in the global root layout so it is present on every page (not just specific routes).
- Do not store sensitive credentials in the server card — it is publicly readable.
- **OAuth 2.1 & PKCE**: HTTP-transport MCP servers MUST enforce OAuth 2.1 with PKCE for secure authentication. Shared static tokens or embedded credentials are prohibited.
- **Streamable HTTP Transport**: Utilize stateless HTTP-transport semantics for all tool invocations, relying on standardized stream headers (e.g., `Accept: text/event-stream`) instead of SSE-only setups.
- **Multi-Tenant Scoping**: Enforce strict tenant isolation by routing all tool requests through a validation layer that decodes tenant-scoped JWTs and applies gateway-level rate limiting.

## When to Use

- Registering a new MCP server so AI clients can auto-discover it from the domain
- Adding browser-side MCP context so users can share page context with AI assistants in their browser
- Updating server card capabilities after adding or removing MCP tools
- Debugging MCP client connectivity failures related to discovery or transport configuration
- Verifying that an existing MCP setup passes `isitagentready.com` scanner checks
- Registering tools on the Official MCP Registry for global tool discovery
- Configuring secure multi-tenant MCP gateways with JWT-scoped access control
- Implementing stateless, streamable HTTP-transport connections for real-time tool feedback

## Suggested Process

1. **Define server capabilities**: List all MCP tools the server exposes (e.g., `list_orders`, `assign_courier`, `get_product`). Each tool needs a `name`, `description`, and `inputSchema`.

2. **Build the server card**: Create `server-card.json` with the required structure:
   ```json
   {
     "name": "My Service MCP",
     "description": "MCP server for order management operations",
     "mcp_version": "2026-07-28",
     "transport": {
       "type": "http",
       "url": "https://api.example.com/mcp"
     },
     "capabilities": {
       "tools": {}
     }
   }
   ```
   Add optional fields: `icon`, `auth`, `resources`, `prompts` as needed.

3. **Place the server card**: For Cloudflare Pages, add `server-card.json` to `public/.well-known/mcp/`. For Workers, serve it from the `GET /.well-known/mcp/server-card.json` route.

4. **Verify content-type**: The server card must be served with `Content-Type: application/json`. Check this via `curl -I`.

5. **Mount WebMCP provider**: In the root layout component (e.g., `Layout.astro`, `_app.tsx`, `layout.tsx`), import and mount the WebMCP provider that calls `navigator.modelContext.provideContext()`. Ensure it runs client-side only (guard with `typeof window !== 'undefined'` if needed for SSR frameworks).

6. **Expose via Link header**: Configure a `Link: </.well-known/mcp/server-card.json>; rel="mcp-server-card"` header on the root response via `configure-agent-headers` so AI clients find the server card without a full crawl.

7. **Validate**: Scan the domain with `isitagentready.com`. Confirm the MCP server card check passes. Test tool invocation from an MCP client (e.g., Claude Desktop with the MCP extension, or a curl request to the transport URL).

## 2026 MCP Production Patterns

### 2026: OAuth 2.1 + PKCE for HTTP Transport

1. **Configure OAuth 2.1 Authorization**: Set up the authorization server endpoint and token endpoint on the MCP gateway.
2. **Enforce PKCE**: Require code verifier and challenge parameters for the authorization flow. The client uses these parameters to generate a verification token without exposing client secrets.
3. **Document Auth in Server Card**: Reference the auth endpoints in `server-card.json`:
   ```json
   "auth": {
     "type": "oauth2",
     "grant_types": ["authorization_code"],
     "authorization_endpoint": "https://auth.example.com/oauth/authorize",
     "token_endpoint": "https://auth.example.com/oauth/token",
     "pkce": true
   }
   ```

### 2026: Streamable HTTP Transport

1. **Define Stateless Semantics**: Ensure the MCP server maintains no persistent session memory on the server side. Every tool invocation request must carry the tenant/auth token.
2. **Establish Stream Headers**: Require the client to set `Accept: text/event-stream` and `Content-Type: application/json`.
3. **Stream Chunks**: Stream response chunks back to the client using chunked transfer encoding, writing each tool progress update or output segment as a structured event message.

### 2026: Official MCP Registry Discovery

1. **Prepare Registry Manifest**: Package the server card, tool schemas, and capabilities into the registry submission schema.
2. **Register Server**: Submit the manifest to the Official MCP Registry.
3. **Verify Indexing**: Confirm the registry exposes the tools and schemas to registered client discovery services.

### 2026: Multi-Tenant MCP Pattern

1. **JWT Verification**: Intercept every incoming tool request at the gateway. Validate the JSON Web Token (JWT) in the `Authorization: Bearer <JWT>` header.
2. **Scope Context**: Extract the tenant ID and user scopes from the validated JWT payload. Inject this tenant context into the request context (`context.Context`).
3. **Enforce Isolation**: Ensure all database queries and tool actions are strictly scoped using the tenant context.
4. **Gateway Rate Limiting**: Apply token-bucket rate limiting at the gateway level based on the tenant ID and user ID extracted from the JWT.

## Output Format

- `/.well-known/mcp/server-card.json` — server discovery metadata
- Root layout update: WebMCP provider component mounted globally
- Official MCP Registry submission manifest
- JWT authorization middleware and rate limiting config files

## Checklist

- [ ] Server card JSON exists at `/.well-known/mcp/server-card.json`.
- [ ] Server card includes `name`, `description`, `mcp_version`, `transport`, and `capabilities`.
- [ ] Server card is served with `Content-Type: application/json`.
- [ ] All declared tools have `name`, `description`, and `inputSchema` defined.
- [ ] WebMCP browser component calls `navigator.modelContext.provideContext()`.
- [ ] WebMCP component is mounted in the global root layout (all pages).
- [ ] CORS headers allow AI browser extensions to fetch the server card.
- [ ] Link header pointing to server card is configured (`configure-agent-headers`).
- [ ] `isitagentready.com` scanner confirms MCP server card is readable.
- [ ] HTTP-transport MCP server enforces OAuth 2.1 with PKCE.
- [ ] Server card lists OAuth 2.1 endpoints and designates PKCE requirement.
- [ ] HTTP transport uses streamable stateless semantics with correct headers (`Accept: text/event-stream`).
- [ ] MCP server is registered on the Official MCP Registry for discovery.
- [ ] Tool requests are authenticated via JWT-scoped validation per tenant.
- [ ] Gateway-level rate limiting is enforced on a per-tenant/per-user basis.


### ⚠️ Stateless Architecture Migration (MCP 2026-07-28)

> **Breaking change**: The MCP spec revision `2026-07-28` transitions MCP from stateful sessions to **fully stateless requests**. A 12-month deprecation window applies for older implementations. Source: [official changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog).
>
> Revision order, newest last: `2025-03-26` → `2025-06-18` → `2025-11-25` → `2026-07-28`. The immediate predecessor is **`2025-11-25`**, so that is the version a current-but-unmigrated server most likely reports.
>
> Governance: MCP was donated by Anthropic to the **Agentic AI Foundation (AAIF)**, a directed fund under the **Linux Foundation**, announced 2025-12-09. Source: [Anthropic announcement](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation).

**What is changing:**

| | Pre-migration (`2025-11-25` and earlier) | New (`2026-07-28`) |
|---|---|---|
| Session ID | Required handshake | **Removed** |
| Capabilities negotiation | One-time at session start | **Per-request in `_meta`** |
| Protocol version over HTTP | Negotiated at session start | **Per-request: `_meta` plus the `MCP-Protocol-Version` header** |
| Server discovery | Implicit from card | **`server/discover` RPC method** |
| Governance | Anthropic | **AAIF (Linux Foundation)** |

**Migration steps:**

1. **Add `_meta` to every request**: include the protocol version and client capabilities in the `_meta` field of every tool call request body, per the official schema (`io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientCapabilities`, `io.modelcontextprotocol/clientInfo`).
   ```json
   {
     "_meta": {
       "io.modelcontextprotocol/protocolVersion": "2026-07-28",
       "io.modelcontextprotocol/clientInfo": { "name": "my-agent-client" },
       "io.modelcontextprotocol/clientCapabilities": { "tools": true, "resources": false }
     },
     "method": "tools/call",
     "params": { ... }
   }
   ```

2. **Remove session establishment logic**: delete handshake endpoints, session ID tracking, and session state from server implementations. Every request must be self-contained.

3. **Implement `server/discover`**: add a `server/discover` RPC endpoint that returns supported protocol versions and capabilities. This replaces static capability negotiation.
   ```json
   { "method": "server/discover", "params": {} }
   // Response:
   { "supported_versions": ["2026-07-28", "2025-11-25"], "capabilities": { "tools": true } }
   ```

4. **Update `mcp_version` in server card**: set `"mcp_version": "2026-07-28"` in the server card after migration.

5. **Backward compatibility**: during the 12-month deprecation window, support the stateless `2026-07-28` alongside the stateful predecessors (`2025-11-25`, and older if clients require them) by inspecting `_meta.protocol_version` and the `MCP-Protocol-Version` header on incoming requests.

**Checklist (for 2026-07-28 readiness):**
- [ ] All tool request handlers read client identity and capabilities from `_meta`, not session state.
- [ ] `server/discover` RPC endpoint implemented and tested.
- [ ] Session ID generation and handshake code removed or gated behind legacy version check.
- [ ] `mcp_version` in server card updated to `"2026-07-28"`.
- [ ] `isitagentready.com` scan passes with new stateless server card.

---

## Related Skills

- **configure-agent-skills**: Set up the agent skills manifest — often deployed alongside MCP for capability routing.
- **configure-agent-headers**: Expose the MCP server card via HTTP Link headers for passive discovery.
- **debug-workos-integration**: Troubleshoot WorkOS and `isitagentready.com` scanner failures.
