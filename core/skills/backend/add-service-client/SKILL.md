---
name: add-service-client
description: Add or modify a service-to-service client or downstream integration by following the repo's transport, timeout, retry, auth, and error-mapping patterns. Use when one service needs to call another system.
---

# Add Service Client

Use this skill when a service must call another internal service, external API, or shared platform dependency.

## When to Use

- one service needs to call another system
- adding/modifying a downstream integration
- wiring transport, timeout, retry, and auth
- mapping errors from the remote service

## Core Rules

- reuse the repo's existing client abstraction pattern
- keep transport details out of business logic when the repo separates them
- make timeouts, retries, and auth explicit
- consider circuit breakers for dependency calls that could cascade under load
- map downstream errors into local domain or boundary errors intentionally
- avoid widening the dependency surface more than necessary
- add a tracing span for the outbound call if the repo uses distributed tracing (OpenTelemetry)
- if any code in this change was AI-generated, validate it per the risk tier defined in the backend-developer role before accepting

## Suggested Process

### 1. Inspect Existing Client Patterns

Look for:

- current client wrappers
- config patterns
- auth or credential handling
- timeout and retry conventions
- test doubles or fixtures already used

### 2. Define The Narrow Interface

Decide the smallest API the local code actually needs:

- request shape
- response shape
- error conditions
- fallback behavior if applicable

### 3. Implement The Integration

Add or update:

- client construction
- config wiring
- request mapping
- response mapping
- error normalization

### 4. Check Operational Safety

Verify:

- timeout values are sensible
- retries are safe and bounded
- sensitive data is not leaked in logs
- startup behavior is acceptable if the dependency is unavailable

### 5. Add Tests

Use skill: `write-tests`

Cover:

- successful call path
- downstream error path
- timeout or unavailable dependency behavior
- response-mapping edge cases

## 2026 Inter-Service Communication Patterns

### 2026: Connect Protocol for Inter-service RPC

The Connect Protocol serves as the preferred inter-service RPC framework due to its flexibility and performance characteristics:
- **Dual Compatibility**: Connect operates seamlessly over both HTTP/1.1 and HTTP/2 transport layers, making it highly robust in environments with varying network capabilities.
- **Client Ecosystem**: Utilize `connectrpc/connect-go` for Go-based services and `connectrpc/connect-es` for TypeScript/JavaScript applications.
- **Protocol Negotiation**: It supports native gRPC, gRPC-Web, and the Connect protocol itself via dynamic content-type negotiation, enabling browser access without custom proxies.

### 2026: mTLS for Zero-Trust Identity

Zero-trust service-to-service communication relies on Mutual TLS (mTLS) to establish cryptographically verifiable identities without API keys or JWTs:
- **SPIFFE/SPIRE Integration**: Issue dynamic client certificates via a trusted internal CA managed by SPIFFE/SPIRE for automatic identity rotation.
- **Authentication Decision Table**:
  * mTLS: Best for internal, low-latency, zero-trust backend communications where network control and client identity verification are required.
  * OIDC Workload Identity: Best for cross-cloud or cloud-native platform integrations (e.g., AWS EKS to Google Cloud Run) leveraging cloud-provider IAM.
  * JSON Web Tokens (JWT): Best for user-delegated context propagation or stateless edge-to-service authentication.

### 2026: xDS Proxyless Load Balancing

Proxyless load balancing allows services to communicate directly with control planes for routing without relying on sidecar proxies:
- **xDS Control Plane**: Configure gRPC clients in Go and Java to query the xDS API directly to retrieve dynamic endpoint routing tables.
- **Performance Benefits**: Eliminates sidecar hop latency, lowers CPU/memory footprints, and simplifies container configurations.

### 2026: Model Context Protocol (MCP) Client Integrations

When service clients interact with external or internal Model Context Protocol (MCP) tool servers, they must enforce standard reliability patterns:
- **Transport Reliability**: Wrap MCP clients with explicit timeouts, exponential backoff retries, and circuit breakers using libraries like Sentinel or Go's resilient round-trippers.
- **Secure Authentication**: Ensure all outbound requests to tool servers include correct auth payloads (such as API keys, Bearer tokens, or OAuth client credentials) mapped safely from secret stores.

## Checklist

- [ ] existing client pattern reviewed
- [ ] narrow local interface defined
- [ ] config and auth wired safely
- [ ] timeout and retry behavior checked
- [ ] error mapping reviewed
- [ ] observability instrumented (OTel span on outbound call)
- [ ] tests added or updated
- [ ] Connect protocol used for browser-accessible inter-service RPC
- [ ] mTLS configured via SPIFFE/SPIRE client certificates for backend identity
- [ ] proxyless xDS client load balancing configured for high-throughput paths
- [ ] MCP tool server client wrapped with timeouts, retries, and circuit breakers

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/implementation-result.json** — Required fields: change_summary, iles_touched[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills

- **navigate-service**: Find the local client pattern before integrating
- **write-tests**: Add coverage for downstream interactions
- **review-code**: Review dependency and reliability risk
- **add-api-endpoint**: Expose the new client-backed behavior safely
- **add-telemetry-instrumentation**: Wire OTel span for the outbound call
- **commit-code**: Prepare the integration for delivery
