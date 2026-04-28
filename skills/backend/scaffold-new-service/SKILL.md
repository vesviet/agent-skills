---
name: scaffold-new-service
description: Bootstrap a new service or bounded component from repo-local templates and conventions. Use when creating a new service, worker, or deployable unit without assuming a fixed framework or folder layout.
---

# Scaffold New Service

Use this skill when a repo needs a brand-new service, worker, or similar bounded component.

## Core Rules

- start from the repo's template or nearest valid example
- keep the first version intentionally small
- define ownership and boundaries before adding features
- do not invent structure when the repo already has conventions
- leave the new service ready for tests, docs, and delivery wiring

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
- [ ] tests added
- [ ] delivery handoff prepared

## Related Skills

- **create-migration**: Add initial schema changes if the service owns data
- **write-tests**: Add safety-net coverage
- **setup-deployment**: Add deployable source-of-truth config
- **review-service**: Check readiness before wider rollout
- **commit-code**: Prepare the new service work for delivery
