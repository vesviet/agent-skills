## Review Checklist

### Service Integrity
- local architecture and layer boundaries are preserved
- business logic, invariants, and state transitions match requirements
- bug fixes are verified against the original issue and nearby regression-prone paths
- validation, authorization, and error mapping are handled at the boundary
- data writes, migrations, queries, and existing records are rollout-safe
- contracts, schemas, and events remain compatible where required
- integrations, jobs, retries, and async flows are idempotent or otherwise safely handled when needed
- side effects are verified intentionally, not assumed from a passing response
- tests cover the main behavior, risky edge cases, and impact radius
- runtime config, logs, monitoring, and release impact are considered
- unverified risk is called out explicitly instead of implied away

### AI-Generated Code Validation (when AI tools contributed to this change)
- risk tier classified: [high / medium / low]
- correctness: intended behavior implemented including unstated edge cases
- security: OWASP Top 10 checked; no hardcoded secrets, no missing input validation, no overly broad permissions
- domain correctness: domain model, invariants, and business rules are respected (not hallucinated)
- test coverage: tests validate logic, not just implementation shape (mutation test run for high-risk paths)
- dependency hygiene: new dependencies passed security policy (age, maintenance, SBOM impact)
- LLM integration: centralized service layer used, prompt injection defense applied, outputs validated before use

### MCP Tool Contracts (when MCP tools are created or modified)
- tool names are stable identifiers; no renames without major version bump
- input/output schemas defined with JSON Schema (Zod/Pydantic source-of-truth)
- tool version declared in `tools/list` metadata with SemVer
- both old and new major versions co-exist for the full deprecation window when making breaking changes
- tool usage telemetry verified before retiring any version
- behavioral contracts documented: idempotency, error codes, rate limits

### LLM Structured Outputs (when LLM responses are parsed in pipelines)
- provider-level structured output enforcement configured (native Structured Outputs API or XGrammar/Outlines for self-hosted)
- Pydantic/Zod schema used as source-of-truth for both generation constraints and runtime validation
- double-validation applied: constrained generation + runtime schema validation
- no regex or string matching for LLM response parsing
- retry-on-validation-error configured (max 2 retries before returning structured error)

### A2A Receiver (when service accepts incoming A2A tasks)
- Agent Card identity verification implemented for all incoming A2A callers
- formal task contract validation: I, O, S, R, T fields validated before execution
- agent allowlist maintained; unverified agents rejected
- pre-execution PDP checks trust score, sensitivity, resource impact, and rate limits
- PDP decisions logged with agent identity, task ID, trust score, sensitivity, decision, and timestamp
- error attribution distinguishes: local failure vs. upstream agent failure vs. contract violation

### Durable Workflows (when AI agent tasks are long-running)
- durable execution framework used (CF Workflows or Temporal) for tasks >30s or with HITL steps
- every LLM call and external API call wrapped in retryable Step/Activity
- Workflow/Activity code is deterministic (no direct API calls or rand() in Workflow functions for Temporal)
- in-flight migration safety handled with workflow versioning API
- step-level observability configured

### Observability
- OTel spans added on all new integration points (DB, external API, event publish, async job, cache)
- span names are intent-driven, not generic HTTP method names
- business-relevant span attributes included (no PII); error spans marked with status and reason
- trace context propagated across service boundaries
- tail-based sampling strategy applied: errors and slow traces always kept
- GenAI calls traced with model name, token counts, latency, and prompt template version (if applicable)
