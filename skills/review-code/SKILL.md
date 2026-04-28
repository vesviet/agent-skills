---
name: review-code
description: Review code changes in Go microservices or similar service-oriented backends. Use for PR reviews, local change reviews, and pre-merge audits that should report P0, P1, and P2 findings first.
---

# Review Code

Use this skill to review concrete changes, not to explain architecture in the abstract.

If the user asks for a full service audit or release readiness pass, hand off to `review-service`.

## Inputs To Gather

- changed files
- purpose of the change
- affected services, libraries, APIs, events, or migrations
- local repo standards under `docs/standards/` or equivalent

If the repo does not have standards docs, use the checklist below directly.

## Review Standard

Review in this order.

### 1. Correctness And Architecture

- preserve layer boundaries such as handler -> biz -> data
- keep business logic out of transport layers
- keep data access behind interfaces when the codebase uses repositories
- avoid hidden globals and stateful singletons unless initialization is explicit and safe
- do not manually edit generated files

### 2. API And Contract Safety

- validate requests close to the boundary
- preserve protobuf field numbers and use `reserved` for removed fields
- keep REST and gRPC naming consistent
- check backward compatibility for public methods, payloads, and enums
- confirm error mapping is appropriate for callers

### 3. Data And State Changes

- wrap multi-step writes in transactions
- avoid N+1 queries
- use parameterized queries
- make list endpoints paginated when data can grow
- verify migrations are reversible or at least rollout-safe
- prefer expand/migrate/contract over destructive schema changes

### 4. Concurrency And Reliability

- propagate `context.Context`
- avoid unmanaged goroutines
- respect timeouts and cancellation
- clean up connections, files, and streams
- make retries and idempotency explicit for critical paths

### 5. Security

- no hardcoded secrets
- enforce authn/authz where needed
- avoid leaking credentials or PII in logs
- validate and sanitize user-controlled input
- call out trust-boundary changes clearly

### 6. Platform And Operations

- verify config added in code exists in config or manifests
- check health probes, resource requests, and rollout assumptions when deployment files changed
- verify event consumers or downstream clients will survive the change
- verify shared-library version changes are intentional and safe

### 7. Testing And Maintenance

- check meaningful coverage around changed business logic
- prefer table-driven tests where they fit
- ensure error paths and boundary cases are tested
- call out fragile naming, duplication, or unclear ownership

## Output Format

Findings come first. Keep summaries brief.

```markdown
## Findings

### P0
1. [path/to/file.go:123] Clear description of a blocking issue

### P1
1. [path/to/file.go:45] Clear description of a high-severity issue

### P2
1. [path/to/file.go:78] Clear description of a maintainability gap

## Open Questions

- Assumption or repo-specific detail that needs confirmation

## Notes

- brief positive observations
- remaining validation gaps
```

If there are no findings, say so explicitly and mention residual risk such as unrun tests, unreviewed deployment config, or missing integration coverage.

## Repo-Specific Adapters

Adapt these references to the active repository:

- standards docs: `docs/standards/...`
- infrastructure docs: `docs/infrastructure/...`
- deployment manifests: `gitops/`, `deploy/`, `k8s/`, or equivalent
- shared library: `common/` or your internal platform module

Skip any category the repo genuinely does not use. Do not invent GitOps, protobuf, or shared-library findings when those concepts are absent.
