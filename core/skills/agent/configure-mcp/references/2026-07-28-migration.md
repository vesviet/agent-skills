# Configure MCP — MCP 2026-07-28 Migration (Reference)

Deep migration reference extracted from `SKILL.md` to keep the main file
under 200 lines. Load this file when migrating an existing MCP server to
the stateless `2026-07-28` revision, when reviewing whether a current
deployment meets the new requirements, or when onboarding a new MCP
implementation.

## Stateless Architecture Migration (MCP 2026-07-28)

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
