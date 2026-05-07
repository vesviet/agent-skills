---
name: add-service-client
description: Add or modify a service-to-service client or downstream integration by following the repo's transport, timeout, retry, auth, and error-mapping patterns. Use when one service needs to call another system.
---

# Add Service Client

Use this skill when a service must call another internal service, external API, or shared platform dependency.

## Core Rules

- reuse the repo's existing client abstraction pattern
- keep transport details out of business logic when the repo separates them
- make timeouts, retries, and auth explicit
- map downstream errors into local domain or boundary errors intentionally
- avoid widening the dependency surface more than necessary

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

## Checklist

- [ ] existing client pattern reviewed
- [ ] narrow local interface defined
- [ ] config and auth wired safely
- [ ] timeout and retry behavior checked
- [ ] error mapping reviewed
- [ ] tests added or updated

## Related Skills

- **navigate-service**: Find the local client pattern before integrating
- **write-tests**: Add coverage for downstream interactions
- **review-code**: Review dependency and reliability risk
- **add-api-endpoint**: Expose the new client-backed behavior safely
- **commit-code**: Prepare the integration for delivery
