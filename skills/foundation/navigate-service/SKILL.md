---
name: navigate-service
description: Navigate and understand an unfamiliar service by mapping its entrypoints, core flows, dependencies, and delivery boundaries
---

# Navigate Service Skill

Use this skill when the user asks to understand, explore, or orient within a specific service or bounded component.

## When to Use

- the user asks how a service works
- the user needs to find where a behavior is implemented
- the user is new to a service and needs fast orientation
- before making changes, so the local architecture is understood first
- during review or troubleshooting, when code context is incomplete

## Operating Assumptions

This skill is intentionally repo-agnostic.

- assume a service-oriented codebase, but not a fixed framework
- do not assume a fixed folder layout or service inventory
- prefer repo-local structure over generic examples
- discover boundaries from the codebase instead of from prior expectations

## Navigation Goals

When using this skill, answer these questions as quickly as possible:

1. What does this service own?
2. What are its public entrypoints?
3. Where does the core business logic live?
4. What data stores or external systems does it depend on?
5. What other services or packages does it call?
6. What configuration, rollout, or runtime constraints matter?

## Suggested Exploration Order

Adapt the order to the target repo, but usually start here:

### Step 1: Identify the Service Boundary

- find the service or component directory
- check `README`, package docs, or service docs if present
- identify the main runtime entrypoint or bootstrap path

### Step 2: Find Entrypoints

Look for the files or packages that define how requests, jobs, or messages enter the service:

- HTTP or RPC handlers
- background jobs or workers
- event consumers or subscribers
- CLI entrypoints or scheduled tasks

### Step 3: Map Core Business Flow

Locate the path from entrypoint to decision-making logic:

- boundary or handler layer
- use case or domain layer
- persistence or adapter layer

Do not assume the repo uses names like `service`, `biz`, or `data`. Follow the actual structure.

### Step 4: Inspect Persistence and State

Check where the service reads or writes state:

- repositories or query packages
- migrations or schema definitions
- cache integrations
- outbound storage adapters

### Step 5: Identify External Dependencies

Look for:

- service clients
- SDK integrations
- event publishing
- shared internal packages
- environment and config dependencies

### Step 6: Check Runtime and Delivery Context

Review the local source of truth for:

- configuration
- environment variables
- health or readiness behavior
- build, generation, or release steps

## What to Extract

When you finish exploration, you should be able to summarize:

- service purpose
- primary user or system-facing capabilities
- main code path for the feature in question
- key dependencies and side effects
- important constraints, risks, or unknowns

## Output Format

When presenting a service overview, structure the response like this:

1. Service purpose
2. Entrypoints and primary flows
3. Core business logic location
4. State and persistence model
5. External dependencies
6. Configuration and runtime considerations
7. Risks, assumptions, and open questions

## Exploration Checklist

### Initial Orientation

- [ ] service boundary identified
- [ ] main entrypoints located
- [ ] local docs or service notes checked

### Core Understanding

- [ ] main business flow mapped
- [ ] persistence layer located
- [ ] external dependencies identified

### Delivery Context

- [ ] config source reviewed
- [ ] build or generation steps noted
- [ ] rollout or runtime constraints noted

## Quick Reference

Use this when the request is narrow and you need fast orientation:

- identify the service directory
- find the main entrypoint
- trace one important request or job flow
- note persistence touchpoints
- note outbound dependencies
- summarize risks or unknowns

## Related Skills

- **review-service**: Full service review and release
- **troubleshoot-service**: Debug service issues
- **review-code**: Inspect implementation details after exploration
- **write-tests**: Add coverage once the target flow is understood
- **meeting-review**: Run a structured cross-role review
