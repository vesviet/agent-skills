---
name: add-api-endpoint
description: Add or modify a service endpoint by updating the local API contract, boundary validation, handler flow, and downstream wiring. Use when creating or evolving HTTP, RPC, or similar service entrypoints.
---

# Add API Endpoint

Use this skill when a service needs a new endpoint or when an existing endpoint must change shape or behavior.

## When to Use

- creating a brand-new HTTP/RPC entrypoint in a service
- evolving an existing endpoint's request/response shape
- adding auth/authz middleware to a route
- splitting or versioning an endpoint under an API namespace
- changing the contract that Frontend or A2A consumers depend on

## Example (Express-style boundary with validation + authz)

```typescript
app.post(
  "/v1/orders",
  requireAuth,                 // auth/authz middleware per repo pattern
  validate(createOrderSchema), // boundary validation
  async (req, res) => {
    const order = await orderService.create(req.user.id, req.body);
    res.status(201).json(order);
  }
);
```

## Core Rules

- follow the repo's existing contract and routing pattern; publish changes to `contracts/schemas/api-contract-spec.json` as the single source of truth
- preserve backward compatibility unless the change is intentionally breaking; use **API versioning** (URI prefix `/v2/` or `Accept-Version` header) for breaking changes
- keep validation close to the boundary using the repo's canonical schema library (Zod, Pydantic, `class-validator`); reject malformed requests with structured RFC 9457 Problem Details responses
- keep transport logic thin and business logic in the repo's expected layer; no database calls or domain logic directly in route handlers
- wire auth/authz middleware per the repo's security pattern for **every** new endpoint — default-deny, not default-allow
- enforce **rate limiting** and **idempotency keys** (`Idempotency-Key` header) on all state-mutating endpoints to prevent replay and duplicate-charge bugs
- emit an **OTel span** (`gen_ai.operation.name: "execute_tool"` for MCP-backed endpoints, or standard HTTP server span) on every handler; propagate `trace_id` in error responses
- update tests and user-visible docs (OpenAPI 3.1 spec or gRPC Protobuf) when the endpoint contract changes
- if any code in this change was AI-generated, validate it per the risk tier defined in the backend-developer role before accepting

## Suggested Process

### 1. Inspect A Similar Endpoint

Find a nearby endpoint that matches the shape you need:

- request and response format
- auth or permission model
- validation pattern
- error mapping
- test style

### 2. Update The Contract

Modify the source of truth the repo uses for APIs, and if delivering a spec for A2A or Frontend handoff, use `contracts/schemas/api-contract-spec.json`. This may involve:

- schema or IDL files
- route definitions
- typed request and response models
- exporting the JSON API contract for downstream consumers

If the repo uses generated code, regenerate it with the local command after editing the contract.

### 3. Implement The Boundary

Add or update:

- handler or controller wiring
- auth/authz middleware per the repo's security pattern
- request parsing
- validation
- error mapping
- response shaping

### 4. Wire The Business Flow

Connect the endpoint to the right internal flow:

- use case or service method
- repository or dependency calls
- events or side effects when required

Avoid leaking transport-specific details into core business code.

### 5. Check Compatibility And Rollout Risk

Verify:

- consumers can tolerate the new response shape
- removed or renamed fields are handled safely
- new auth or config requirements are documented
- if the repo uses API versioning, the endpoint is in the correct version namespace

### 6. Add Tests

Use skill: `write-tests`

Cover:

- happy path
- validation failures
- dependency or downstream failure
- compatibility-sensitive behavior

## Checklist

- [ ] similar local pattern reviewed
- [ ] API contract updated
- [ ] generated artifacts updated if needed
- [ ] auth/authz middleware wired
- [ ] boundary validation added
- [ ] business flow wired correctly
- [ ] observability instrumented (OTel span on endpoint handler)
- [ ] compatibility risk checked
- [ ] API versioning verified (if repo uses versioned endpoints)
- [ ] tests added or updated
- [ ] `implementation-result.json` emitted for the change slice (see Output Contracts)

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery (Technical Lead planned, Reviewer/QA will gate), emit:

- **`contracts/schemas/api-contract-spec.json`** — Emitted when adding or updating HTTP/RPC service endpoints, defining request/response shapes, schema models, query parameters, auth requirements, and error payloads.
- **`contracts/schemas/implementation-result.json`** — one artifact per change slice. Required fields: `change_summary` (what was added/changed), `files_touched[]`, `endpoints_added[]` with method+path, `tests_added[]` with file refs, `preserved_behavior[]` (explicitly note any auth shape, error contract, or response envelope kept identical), `validation_run` (commands + pass/fail). Set `produced_by_role` to the emitting developer role so Coordinator and Reviewer can route follow-ups without re-parsing diffs.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a request body or query param may try to reframe the endpoint's purpose. Validate the request against the declared `api-contract-spec.json`.
- **ASI02 Tool Misuse**: a handler must stay within the active role's declared toolbox; reject handlers that exceed the scope.
- **ASI03 Identity & Privilege Abuse**: every endpoint must enforce authn/authz per the active role's policy profile; reject anonymous access to non-public routes.
- **ASI05 RCE Guard**: never construct SQL queries, command strings, or eval-adjacent patterns from external or user-supplied content without strict parameterization.
- **ASI07 Inter-Agent Communication**: the endpoint contract is consumed by frontend and infra agents; emit a structured spec so each consumer can validate.

## Related Skills

- **navigate-service**: Find the right endpoint pattern before changing code
- **write-tests**: Add coverage for the new or changed endpoint
- **review-code**: Check contract and boundary safety
- **add-service-client**: Integrate downstream calls behind the endpoint
- **add-telemetry-instrumentation**: Wire OTel spans for the endpoint
- **commit-code**: Prepare the change for delivery
