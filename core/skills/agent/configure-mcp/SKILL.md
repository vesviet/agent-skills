---
name: configure-mcp
description: Use when configuring Model Context Protocol (MCP) servers and WebMCP layouts.
---

# Configure MCP

Use this skill to set up `.well-known/mcp/server-card.json` and WebMCP browser components.

## Core Rules
- The Server Card MUST be placed at `/.well-known/mcp/server-card.json`.
- WebMCP component MUST invoke `navigator.modelContext.provideContext()`.
- Ensure appropriate component placement in global layouts (e.g., `Layout.astro`).

## Suggested Process
1. Define the capability mappings and tools of the MCP server.
2. Construct the `server-card.json` metadata according to WebMCP standard.
3. Configure the web hosting setup to serve the server-card payload correctly.
4. Mount the interactive WebMCP provider components in the root UI layout.

## Checklist
- [ ] Server card JSON file exists and contains valid schema metadata.
- [ ] File is hosted correctly at `/.well-known/mcp/server-card.json`.
- [ ] WebMCP browser scripts call the standard window or navigator context hook.
- [ ] Root component layout includes the necessary provider wrappers.
- [ ] CORS policies are set up to allow secure remote client fetches.

## Related Skills
- **configure-agent-skills**: Create the manifest of skills.
- **configure-agent-headers**: Expose well-known endpoints natively.
