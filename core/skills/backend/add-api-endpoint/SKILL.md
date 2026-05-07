---
name: add-api-endpoint
description: Add or modify a service endpoint by updating the local API contract, boundary validation, handler flow, and downstream wiring. Use when creating or evolving HTTP, RPC, or similar service entrypoints.
---

# Add API Endpoint

Use this skill when a service needs a new endpoint or when an existing endpoint must change shape or behavior.

## Core Rules

- follow the repo's existing contract and routing pattern
- preserve backward compatibility unless the change is intentionally breaking
- keep validation close to the boundary
- keep transport logic thin and business logic in the repo's expected layer
- update tests and user-visible docs when the endpoint contract changes

## Suggested Process

### 1. Inspect A Similar Endpoint

Find a nearby endpoint that matches the shape you need:

- request and response format
- auth or permission model
- validation pattern
- error mapping
- test style

### 2. Update The Contract

Modify the source of truth the repo uses for APIs, such as:

- schema or IDL files
- route definitions
- typed request and response models

If the repo uses generated code, regenerate it with the local command after editing the contract.

### 3. Implement The Boundary

Add or update:

- handler or controller wiring
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
- [ ] boundary validation added
- [ ] business flow wired correctly
- [ ] compatibility risk checked
- [ ] tests added or updated

## Related Skills

- **navigate-service**: Find the right endpoint pattern before changing code
- **write-tests**: Add coverage for the new or changed endpoint
- **review-code**: Check contract and boundary safety
- **add-service-client**: Integrate downstream calls behind the endpoint
- **commit-code**: Prepare the change for delivery
