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

- follow the repo's existing contract and routing pattern
- preserve backward compatibility unless the change is intentionally breaking
- keep validation close to the boundary
- keep transport logic thin and business logic in the repo's expected layer
- wire auth/authz middleware per the repo's security pattern for every new endpoint
- update tests and user-visible docs when the endpoint contract changes
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

- **`contracts/schemas/implementation-result.json`** — one artifact per change slice. Required fields: `change_summary` (what was added/changed), `files_touched[]`, `endpoints_added[]` with method+path, `tests_added[]` with file refs, `preserved_behavior[]` (explicitly note any auth shape, error contract, or response envelope kept identical), `validation_run` (commands + pass/fail). Set `produced_by_role` to the emitting developer role so Coordinator and Reviewer can route follow-ups without re-parsing diffs.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills

- **navigate-service**: Find the right endpoint pattern before changing code
- **write-tests**: Add coverage for the new or changed endpoint
- **review-code**: Check contract and boundary safety
- **add-service-client**: Integrate downstream calls behind the endpoint
- **add-telemetry-instrumentation**: Wire OTel spans for the endpoint
- **commit-code**: Prepare the change for delivery

## Output Contracts

- `contracts/schemas/api-contract-spec.json`
