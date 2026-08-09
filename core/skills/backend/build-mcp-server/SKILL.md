---
name: build-mcp-server
description: Scaffolds and implements a new Model Context Protocol (MCP) server. Use when exposing new backend tools or resources to AI agents.
---

# Build MCP Server

Use this skill to create standard-compliant MCP servers that expose system capabilities securely to AI agents.

## Core Rules
- **Schema-First**: Define all tool inputs using Zod or Pydantic schemas as the absolute source of truth.
- **Versioning**: Apply SemVer 2.0 to the MCP server API. Support concurrent major versions during deprecation windows.
- **Security**: Implement OAuth 2.0 Resource Server patterns for authorization if the server exposes sensitive mutations or data.
- **Telemetry**: Add OpenTelemetry spans to track every tool execution, noting inputs, execution time, and outcome.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, `endpoints_added[]` (list of MCP tools/resources), and `validation_run` output confirming the MCP schema validates.

## Checklist
- [ ] Schema-first tool definition complete.
- [ ] SemVer versioning applied.
- [ ] Authorization guards verified.
- [ ] OTel telemetry instrumented.
- [ ] `implementation-result.json` emitted.
