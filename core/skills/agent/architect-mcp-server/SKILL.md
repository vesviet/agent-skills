---
name: architect-mcp-server
description: Architect enterprise-grade Model Context Protocol (MCP) servers, tool surfaces, schemas, transport protocols, and security perimeters. Use when designing MCP server contracts, selecting streamable HTTP or stdio transports, standardizing Zod/Pydantic schemas, externalizing state handles (SEP-2567), configuring OAuth 2.1 RFC 8707 Resource Indicators, or establishing Shadow MCP governance.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests]
---

# Architect MCP Server

Architect enterprise-grade Model Context Protocol (MCP) servers, tool surfaces, schemas, transport protocols, and security perimeters. This skill establishes architectural boundaries, ergonomics, and governance before code implementation.

## Core Rules

- **Stateless-First Architecture**: Default to stateless streamable HTTP transport adhering to MCP spec revision 2026-07-28; reserve stdio strictly for local development and CLI environments.
- **Action-Oriented Domain Prefixes**: Name tools with explicit verb-noun domain syntax (`<domain>_<action>`, e.g., `crm_search_customers`, `billing_issue_refund`); avoid vague names.
- **Strict Schema Validation**: Define strict input parameters and return types using Zod (TypeScript) or Pydantic v2 (Python); prohibit untyped JSON blobs or generic string inputs.
- **OutputSchema & Structured Content**: Constrain returned payloads with `outputSchema` and emit `structuredContent` separating structured JSON from textual explanations.
- **Actionable Error Ergonomics**: Error responses MUST return typed error categories, machine-readable error codes, and explicit remediation hints enabling autonomous agent recovery.
- **State Externalization (SEP-2567)**: Externalize session state, pagination cursors, and continuation tokens to durable stores (Redis, Cloudflare D1); prohibit sticky server memory.
- **OAuth 2.1 RFC 8707 Resource Indicators**: Require clients to specify target MCP server URIs in authorization requests to prevent token forwarding and replay attacks.
- **Registry Allowlisting & Supply Chain**: Production MCP servers must originate from vetted registries with publisher verification, code-signing, and SBOM audits (`MCP-REGISTRY LOCK`).
- **Shadow MCP Governance**: Enforce network proxy and gateway inspection to detect and block unregistered, rogue MCP servers communicating with AI runtimes (`MCP-GATEWAY LOCK`).

## When to Use

- Architecting enterprise MCP server boundaries, tool surfaces, and input/output contracts
- Selecting and specifying transport architectures (stateless streamable HTTP vs. stdio)
- Standardizing schema granularity, Zod/Pydantic validation, and actionable error envelopes
- Externalizing session handles (SEP-2567) for serverless edge and distributed cluster deployments
- Designing OAuth 2.1 RFC 8707 Resource Indicators and Enterprise-Managed Authorization
- Establishing Shadow MCP discovery, gateway routing, and supply-chain allowlisting

## Suggested Process

1. **Define Domain Boundary & Tool Surface**: Inventory operations, apply `<domain>_<action>` naming, calibrate granularity (single-action atomic vs. composite), and describe disambiguating triggers.
2. **Specify Strict Input & Output Schemas**: Author Zod or Pydantic schemas with field descriptions, validation constraints, enum values, and explicit `outputSchema` declarations.
3. **Design Actionable Error Envelopes**: Format error returns with `is_error`, `error_code`, `message`, `remediation_hint`, and `is_retriable` flags for agent self-correction.
4. **Select Transport & Externalize State**: Specify stateless streamable HTTP headers (`Accept: text/event-stream`, `Mcp-Method`), and externalize multi-turn state via SEP-2567 handles.
5. **Architect Resources & Prompts**: Declare URI-addressable resources (`system://metrics/{host}`) and reusable prompt workflows (`prompts/get`) with parameter validation.
6. **Enforce Auth & RFC 8707 Scoping**: Configure OAuth 2.1 authorization servers with PKCE, audience-restricted Resource Indicators, and Enterprise-Managed Authorization policies.
7. **Establish Governance & Emit Contracts**: Validate against OWASP ASI and MCP Top 10 guardrails, define gateway telemetry, and emit `adr-spec.json` and `architecture-options.json`.

## Checklist

- [ ] Tool names adhere to action-oriented domain prefix naming (`<domain>_<action>`).
- [ ] Every tool defines strict Zod/Pydantic input schemas and explicit `outputSchema` contracts.
- [ ] Output responses separate typed JSON from natural language via `structuredContent`.
- [ ] Error responses supply machine-readable error codes and self-correction remediation hints.
- [ ] Production transport defaults to stateless streamable HTTP (MCP 2026-07-28 revision).
- [ ] Multi-turn session handles and pagination cursors externalized via SEP-2567 to Redis or D1.
- [ ] OAuth 2.1 RFC 8707 Resource Indicators bound to target MCP server URI.
- [ ] Registry vetting, SBOM verification, and Shadow MCP gateway detection policies documented.
- [ ] Architecture decision record emitted conforming to `contracts/schemas/adr-spec.json`.

## Output Contracts

When architectural design is complete or ready for downstream implementation slices:

- **`contracts/schemas/adr-spec.json`**: Primary architectural decision record detailing MCP server contracts, transport choices, state externalization, and trust boundaries.
- **`contracts/schemas/architecture-options.json`**: Comparative options evaluation documenting trade-offs between transport modes, schema strategies, and authorization patterns.

## Failure Modes

- **Vague Tool Naming**: Tools with overlapping names (e.g., `query_data` vs `fetch_info`) cause model confusion and wrong tool invocation. Mitigation: Mandate strict `<domain>_<action>` naming with explicit negative triggers ("do NOT use for...").
- **Unstructured Error Returns**: Raw stack traces or generic "500 Error" messages cause agents to abort or loop endlessly. Mitigation: Standardize typed JSON error envelopes with remediation hints.
- **In-Memory Session Affinity**: Relying on server RAM for multi-turn conversational state causes failure during autoscaling and rolling deploys. Mitigation: Enforce SEP-2567 external state handles.
- **Token Replay Vulnerability**: Downstream MCP tools forwarding caller tokens to upstream services without audience restriction. Mitigation: Enforce OAuth 2.1 RFC 8707 Resource Indicators.

## Security Guardrails (OWASP ASI + MCP Top 10)

- **ASI02 Excessive Agency**: Limit tool capabilities to minimal required privilege; require human approval for irreversible write operations.
- **ASI04 Supply Chain Abuse**: Verify MCP server packages against signed provenance manifests; prohibit unvetted registries.
- **ASI05 Insecure Tool Execution**: Validate every input parameter against declared schemas; sanitize inputs before SQL, shell, or API dispatch.
- **ASI07 Insecure Inter-Agent Communication**: Enforce mutual authentication and RFC 8707 audience restriction on all inter-service MCP calls.
- **ASI08 Cascading Failures**: Implement circuit breakers, bulkhead isolation, and rate limiting across MCP gateways.
- **ASI09 Over-Reliance**: Provide deterministic schema validation and error hints to prevent blind acceptance of incorrect tool outputs.
- **ASI10 Rogue Agent Misbehavior**: Monitor tool call anomalies at gateway proxies and revoke access tokens upon abnormal call patterns.

## Related Skills

- **build-mcp-server**: Implement the backend code, handlers, and tests specified by this architectural design
- **configure-mcp**: Publish server discovery cards and browser WebMCP provider components
- **system-design**: Plan overall system topologies, compute sizing, and infrastructure resilience
- **decompose-agentic-system**: Decompose complex agentic workflows into sub-agent DAG execution scopes
- **agent-tool-orchestration**: Orchestrate tool call sequences, fallback chains, and parameter injection
- **security-audit**: Audit MCP authentication flows, token scopes, and transport encryption
- **add-telemetry-instrumentation**: Instrument MCP gateways with OpenTelemetry tracing and error metrics
