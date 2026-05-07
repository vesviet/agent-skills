---
name: integrate-api-client
description: Connect frontend code to backend APIs by following the repo's request, caching, auth, error-handling, and state-management patterns. Use when a UI needs to read or mutate backend data.
---

# Integrate API Client

Use this skill when frontend code needs to call a backend API or when an existing integration must change.

## Core Rules

- reuse the repo's existing data-fetching and mutation pattern
- keep transport details out of presentational components when possible
- make loading, error, and retry behavior explicit
- preserve auth and sensitive-data handling rules
- avoid duplicated request logic when a shared client already exists

## Suggested Process

### 1. Inspect Existing API Usage

Find how the repo currently handles:

- request construction
- auth headers or session context
- caching or stale-data behavior
- error normalization
- optimistic updates or invalidation

### 2. Define The Data Contract

Clarify:

- endpoint or operation used
- request payload
- response shape
- error cases the UI must handle
- whether the call is query, mutation, or streaming-like behavior

### 3. Add Or Update The Client Layer

Implement the narrowest useful integration:

- client helper or hook
- request serialization
- response mapping
- cache key or invalidation logic when the repo uses it

### 4. Connect The UI

Wire the integration into the right layer:

- page-level loader
- container or view-model layer
- mutation handler
- form submit or interaction callback

### 5. Check State And Failure Behavior

Verify:

- loading states are visible
- retries are appropriate
- stale data is invalidated correctly
- failure messages are useful but safe
- auth expiration or permission failures are handled intentionally

### 6. Add Tests

Use skill: `frontend-testing`

Cover:

- success path
- API failure path
- loading state
- mutation side effects or cache updates

## Checklist

- [ ] local data-fetching pattern reviewed
- [ ] request and response contract defined
- [ ] client or hook updated
- [ ] UI wiring added
- [ ] loading and error states handled
- [ ] tests added or updated

## Related Skills

- **add-page-route**: Place the data integration into route flow
- **add-ui-component**: Render the integrated state in reusable UI
- **frontend-testing**: Add coverage for network-driven states
- **review-code**: Review data flow, auth, and error handling risk
- **commit-code**: Prepare the integration for delivery
