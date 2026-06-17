---
name: configure-mcp
description: Sets up the full MCP presence for a web service — server card at `/.well-known/mcp/server-card.json`, WebMCP browser provider component, and supporting host/route configuration — so AI clients auto-discover and connect without manual configuration. Use when registering a new MCP server, adding browser-side context sharing, updating tool capabilities, or debugging MCP client connectivity failures.
---

# Configure MCP

Use this skill to set up the full MCP presence for a web service: the server card at `/.well-known/mcp/server-card.json`, the WebMCP browser provider component, and the supporting host/route configuration. This makes AI clients (Claude, Copilot, custom agents) auto-discover and connect to the service's MCP server without manual configuration.

## Core Rules

- The Server Card MUST be placed at `/.well-known/mcp/server-card.json` — this path is non-negotiable per the MCP spec.
- The server card JSON MUST include all required fields: `name`, `description`, `mcp_version`, `transport` (with `url` and `type`), and `capabilities`.
- WebMCP browser component MUST invoke `navigator.modelContext.provideContext()` — do not use alternatives or polyfills that bypass this API.
- Ensure the WebMCP component is mounted in the global root layout so it is present on every page (not just specific routes).
- Do not store sensitive credentials in the server card — it is publicly readable.

## When to Use

- Registering a new MCP server so AI clients can auto-discover it from the domain
- Adding browser-side MCP context so users can share page context with AI assistants in their browser
- Updating server card capabilities after adding or removing MCP tools
- Debugging MCP client connectivity failures related to discovery or transport configuration
- Verifying that an existing MCP setup passes `isitagentready.com` scanner checks

## Suggested Process

1. **Define server capabilities**: List all MCP tools the server exposes (e.g., `list_orders`, `assign_courier`, `get_product`). Each tool needs a `name`, `description`, and `inputSchema`.

2. **Build the server card**: Create `server-card.json` with the required structure:
   ```json
   {
     "name": "My Service MCP",
     "description": "MCP server for order management operations",
     "mcp_version": "2025-03-26",
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

## Output Format

- `/.well-known/mcp/server-card.json` — server discovery metadata
- Root layout update: WebMCP provider component mounted globally

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

## Related Skills

- **configure-agent-skills**: Set up the agent skills manifest — often deployed alongside MCP for capability routing.
- **configure-agent-headers**: Expose the MCP server card via HTTP Link headers for passive discovery.
- **debug-workos-integration**: Troubleshoot WorkOS and `isitagentready.com` scanner failures.
