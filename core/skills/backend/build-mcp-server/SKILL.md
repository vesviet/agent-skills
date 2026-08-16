---
name: build-mcp-server
description: Scaffolds and implements a new Model Context Protocol (MCP) server. Use when exposing new backend tools or resources to AI agents.
---

# Build MCP Server

Use this skill to create standard-compliant MCP servers that expose system capabilities securely to AI agents.

## Core Rules

- **Schema-First**: Define all tool inputs using Zod or Pydantic schemas as the absolute source of truth.
- **Versioning**: Apply SemVer 2.0 to the MCP server API. Support concurrent major versions during deprecation windows.
- **Security**: Implement OAuth 2.0 / 2.1 Resource Server patterns for authorization if the server exposes sensitive mutations or data.
- **Telemetry**: Add OpenTelemetry spans to track every tool execution, noting inputs, execution time, and outcome.
- **Stateless Execution**: Adhere to stateless request semantics where client capabilities and request metadata are passed per invocation.

## Suggested Process

### 1. Define Server Scope & Tool Contracts

Identify the capabilities, resources, and tools the MCP server will provide. For each tool:
- Define strict input schemas using Zod (TypeScript) or Pydantic (Python).
- Document clear, unambiguous tool descriptions so AI agents choose tools accurately.
- Specify returned output schemas and error response shapes.

### 2. Scaffold Server Runtime & Transport

Initialize the MCP server using the official SDK (`@modelcontextprotocol/sdk` or `mcp` Python package):
- Configure standard transports: stdio for local agent execution, streamable HTTP with SSE headers (`Accept: text/event-stream`) for remote service deployment.
- Declare server metadata (`name`, `version`) and capabilities (`tools`, `resources`, `prompts`).

### 3. Implement Tool Handlers & Boundary Validation

Wire tool registration and execution logic:
- Parse and validate incoming arguments against input schemas before executing business logic.
- Route execution to internal service methods or downstream APIs without embedding tight coupling.
- Wrap execution in structured error handling, returning informative error messages rather than raw stack traces.

### 4. Enforce Security & Authorization Middleware

Protect sensitive operations:
- For HTTP-transport servers, enforce OAuth 2.1 with PKCE or JWT bearer token validation.
- Decode tenant and user claims from the authentication context and inject them into execution context.
- Apply rate limiting and action whitelisting to prevent runaway agent execution loops.

### 5. Instrument Observability & Tracing

Use skill: `add-telemetry-instrumentation`
- Create OpenTelemetry spans for each `tools/call` invocation with standard attributes (`mcp.tool_name`, `mcp.transport_type`).
- Record token consumption, latency, and success/failure outcomes.
- Ensure no sensitive payload data or authorization credentials leak into trace logs.

### 6. Verify Protocol Compliance & Testing

Use skill: `write-tests`
- Test tool discovery via MCP Inspector or mock client initialization.
- Author unit and integration tests covering happy paths, schema validation failures, and downstream error handling.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, `endpoints_added[]` (list of MCP tools/resources), and `validation_run` output confirming the MCP schema validates.

## Checklist

- [ ] Schema-first tool definition complete with Zod or Pydantic.
- [ ] Server transport (stdio or streamable HTTP) configured with proper headers.
- [ ] Tool argument validation and boundary error handling implemented.
- [ ] Authorization guards and tenant isolation verified.
- [ ] OpenTelemetry spans instrumented for all tool calls.
- [ ] Unit and protocol compliance tests added.
- [ ] `implementation-result.json` emitted.

## Related Skills

- **configure-mcp**: Set up domain discovery, server cards, and client integration for the MCP server
- **add-api-endpoint**: Connect MCP tool handlers to internal service endpoints and business logic
- **implement-structured-outputs**: Enforce strict JSON schema validation on tool arguments and outputs
- **add-telemetry-instrumentation**: Wire OpenTelemetry spans and metrics for MCP tool executions
- **security-audit**: Review authentication, authorization boundaries, and input sanitization
- **write-tests**: Author automated test suites verifying MCP tool invocations and error scenarios
