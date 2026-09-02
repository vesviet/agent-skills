## Review Checklist

### Distributed System Validation
- acceptance criteria are **observable** and mapped to explicit assertions (clear pass/fail)
- critical user journeys include negative paths and boundary cases, not only happy paths
- permissions/roles/tenancy are validated where applicable (no unauthorized access)
- data correctness is verified (not only responses): invariants, constraints, and persistence state
- side effects are verified: events published/consumed, cache behavior, search indexing, downstream calls
- async flows are validated with eventual consistency in mind (timing windows and retries)
- compatibility is considered when relevant (mixed versions, schema evolution, safe migrations)
- defects include environment, reproduction, expected, actual, evidence, and suspected blast radius
- skipped checks and residual risk are explicit and justified
- release confidence is supported by evidence, not confidence language
### AI / LLM System Validation (when applicable)

- property-based assertions defined (no exact-match assertions for non-deterministic outputs)
- golden dataset version-controlled and seeded with production failures
- LLM-as-Judge calibrated against human benchmarks before use as a deployment gate
- trajectory evaluation conducted for multi-step agents (not just final output)
- tool-call accuracy validated (parameters, selection, no unauthorized chaining)
- hallucination cascade mitigation verified at intermediate steps
- context window exhaustion simulated for multi-turn interactions
- adversarial tool-chaining and privilege escalation test cases included
- CI/CD regression gate configured against golden dataset
- **CI eval gate passes** for prompt/model/tool changes (golden dataset, calibrated judge ≥85%)

### MCP & Agent Validation (when applicable)

- **MCP stateless protocol validated**: HTTP transport, externalized session state, registry allowlist
- **WebMCP validated**: context emission, action allowlist, HITL modals, background sync, origin validation
- **A2A contract tests pass**: schema validation, behavioral invariants, error envelope for all agent boundaries
- **MCP schema drift detection**: pinned schemas diff-checked in CI against live registry

### EU AI Act Compliance (when AI features in scope)

- Article 50 disclosure UI validated: `<AIDisclosureBanner>` before first interaction, plain language
- C2PA marking verified on AI-generated media (deadline 2026-12-02)
- Annex type identified with correct deadline (Annex III: 2027-12-02; Annex I: 2028-08-02)
- `data-ai-generated="true"` attributes on AI-rendered containers

### Resilience & Chaos Engineering (when applicable)
- chaos experiment charter documented (hypothesis, fault type, scope, success criteria, result)
- graceful degradation validated under controlled fault injection
- recovery behavior validated: system returns to health without manual intervention within MTTR target
- shift-right rollback trigger criteria defined and observable in production telemetry
- production near-misses surfaced and added to golden dataset or regression checklist

### Accessibility (WCAG 2.2, when UI is in scope)
- automated a11y scan completed (contrast, ARIA, heading structure, alt text)
- keyboard-only navigation tested for critical flows
- screen reader walkthrough conducted for P0 user journeys
- WCAG 2.2 new criteria checked: Focus Not Obscured, Dragging Movements, Target Size
- a11y defects classified with same severity framework as functional defects
