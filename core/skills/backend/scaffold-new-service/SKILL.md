---
name: scaffold-new-service
description: Bootstrap a new service or bounded component from repo-local templates and conventions. Use when creating a new service, worker, or deployable unit without assuming a fixed framework or folder layout.
---

# Scaffold New Service

Use this skill when a repo needs a brand-new service, worker, or similar bounded component.

## When to Use

- creating a new service, worker, or deployable unit
- bootstrapping from repo-local templates
- no fixed framework/layout assumed
- standing up a bounded component

## Core Rules

- start from the repo's template or nearest valid example — follow the **Hexagonal Architecture** layout (`api/`, `internal/service/`, `internal/biz/`, `internal/data/`, `cmd/`) or the repo's established equivalent
- keep the first version intentionally small: one entrypoint, one use case, one persistence path, one health endpoint
- define ownership and boundaries before adding features; map the DDD bounded context (what the service owns, what it does not)
- do not invent structure when the repo already has conventions; copy, rename, and adapt — never freehand scaffold from zero
- wire **baseline observability from commit 1**: `/health/live`, `/health/ready`, structured OTel tracer bootstrap, and at least one span on the primary integration boundary
- use **Wire (or the repo's DI framework)** for all constructor injection; no global variables or `init()`-based singletons
- verify every AI-generated dependency: confirm the package exists in the registry, is pinned to a real version, and has no hallucinated import paths
- confirm all environment variables and secret bindings are declared in deployment config and README before the first deploy
- check that AI-generated auth middleware, CORS config, and input validation match the repo's existing patterns — AI scaffolding defaults are often permissive
- if any code in this change was AI-generated, validate it per the risk tier defined in the backend-developer role before accepting

## Suggested Process

### 1. Clarify The Service Boundary

Define:

- what the service owns
- what it exposes
- what it depends on
- what data it manages

### 2. Pick The Best Starting Template

Prefer:

- official scaffold command
- repo template
- nearby service with the same shape

Rename paths, identifiers, and generated artifacts carefully if copying.

### 3. Create The Minimum Structure

Add only what the repo expects, such as:

- entrypoints
- contracts
- core logic
- persistence
- config
- tests
- docs

### 4. Wire The First End-To-End Flow

Set up one narrow path that proves the service shape works:

- one entrypoint
- one use case
- one persistence or dependency path
- one health or readiness path if needed

### 5. Add Basic Verification

Use skill: `write-tests`

At minimum, add:

- one happy path
- one failure or validation path
- build and startup verification

### 6. Prepare Delivery Handoff

Use skill: `setup-deployment` if delivery config is needed.

Make sure the new service has:

- docs or README starter content
- basic ownership metadata if the repo uses it
- local verification steps

## Checklist

- [ ] service boundary defined
- [ ] local template or example chosen
- [ ] identifiers renamed safely
- [ ] minimum structure created
- [ ] first end-to-end flow wired
- [ ] baseline observability wired (health endpoint, OTel spans)
- [ ] tests added
- [ ] delivery handoff prepared

## Failure Modes

- **Service scaffolded without observability**: a new service is created without OTel, health probes, or audit-trail wiring. **Mitigation:** enforce the OTel + health + audit contract in the scaffold template; reject services that ship without instrumentation.
- **Service scaffolded without auth profile**: a new service has no authn/authz. **Mitigation:** require an auth profile before the service is promoted; reject services with anonymous access to non-public routes.
- **Migration runs out of order**: a new service's first migration runs before the schema it depends on. **Mitigation:** enforce the migration order via a sequencing tool; reject out-of-order migrations.
- **Secret in scaffold**: a token or key is committed to the new service's source. **Mitigation:** use the platform secret store; run secret scanning in CI; rotate the affected credential on detection.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/implementation-result.json** — Required fields: change_summary, iles_touched[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: template and framework versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct scaffolding code, config, or scripts from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the scaffolding contract is consumed by infra and review agents; emit a structured spec so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present a scaffolded service as "production-ready" without security review; surface the residual risk honestly.

## Related Skills

- **create-migration**: Add initial schema changes if the service owns data
- **write-tests**: Add safety-net coverage
- **setup-deployment**: Add deployable source-of-truth config
- **add-telemetry-instrumentation**: Wire baseline observability for the new service
- **review-service**: Check readiness before wider rollout
- **commit-code**: Prepare the new service work for delivery
