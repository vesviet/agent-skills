---
description: Closed-loop 2027 Agentic SWE feature delivery workflow enforcing spec freeze, Red-Green TDD, sandbox execution, adversarial review, and human-in-the-loop approval.
---

## Feature Delivery Workflow

Use this workflow for end-to-end engineering of new features or non-trivial enhancements requiring verified contracts, strict Red-Green TDD, isolated sandbox execution, and adversarial review.

### Prerequisites

- A drafted feature ticket conforms to `core/contracts/schemas/feature-ticket.json`
- Technical architecture boundaries and failure domains are identified
- Isolated sandbox execution environment (container or MicroVM) is available
- Target repository branch and baseline automated test suites pass cleanly

### Workflow Steps

#### 1. Spec Review and Contract Freeze

Role: **Solution Architect**, **Technical Lead**

Use skill: `plan-technical-delivery`

Review and freeze the functional specifications and interface boundaries before authoring any code:

- Validate acceptance criteria in `feature-ticket.json` for deterministic testability.
- If API endpoints, event schemas, or database schemas are altered, define and freeze `api-contract-spec.json` and `schema-migration.json`.
- Perform initial blast radius assessment (`impact_tier`, `failure_domains`, downstream consumer dependencies).
- Mark contract status as frozen. Unfreezing requires formal change control.

#### 2. Test Authoring (Red Stage)

Role: **QA Engineer**, **Backend Developer**

Use skill: `write-tests`

Author automated verification tests strictly against the frozen specification prior to implementation:

- Author unit, integration, and contract test cases covering all acceptance criteria scenarios and edge cases.
- Implement property-based tests for algorithmic or data-transformation boundaries.
- Run the newly authored tests in the local environment and verify that all new assertions FAIL cleanly with expected error messages (Red Gate).
- Verify that failing tests do not fail due to syntax or environmental errors, but exclusively due to missing implementation.

#### 3. Implementation (Green Stage)

Role: **Backend Developer**, **Frontend Developer**

Use skill: `commit-code`

Implement the minimal deterministic code necessary to satisfy the failing tests:

- Write targeted business logic and component code until all Red tests transition to PASS (Green Gate).
- Follow anti-vibe-slop principles: avoid redundant wrappers, unneeded dependencies, or hallucinated edge-case workarounds.
- Perform safe refactoring while ensuring all tests continue passing without regression.
- Maintain contract immutability: do not alter frozen schemas to accommodate convenient shortcuts.

#### 4. Sandbox Execution and Mutation Verification

Role: **QA Engineer**, **Technical Lead**

Use skill: `agent-quality-gate`

Execute comprehensive verification in an isolated execution sandbox:

- Run the full test suite in an isolated environment (`tier_0_ephemeral_container` or `tier_1_isolated_microvm`) to guarantee environment independence and prevent secret leakage.
- Execute mutation testing (e.g., Stryker, mutmut) against the modified business logic.
- Enforce the mutation kill rate threshold (minimum 75% mutants killed) to eliminate tautological or dummy test suites.
- Emit `test-report.json` capturing execution telemetry, passed scenarios, and mutation scores.

#### 5. Adversarial Code Review

Role: **Reviewer**, **Security Engineer**

Use skill: `review-code`

Conduct multi-dimensional adversarial inspection of the implementation and test proofs:

- Review code diff against anti-vibe-slop heuristics: verify proper error handling, resource lifecycle management, and boundary validations.
- Audit for concurrency hazards, race conditions, memory leaks, and N+1 query patterns.
- Perform OWASP ASI security audit: inspect for ASI01 (Goal Hijacking), ASI04 (Supply Chain / Dependency Tampering), and ASI05 (Unexpected Code Execution).
- Emit findings into `code-review-finding.json` categorized as Blocking, Important, or Follow-Up.

#### 6. HITL Approval and Delivery Gate

Role: **Technical Lead**, **Product Manager**

Use skill: `meeting-review`

Complete human-in-the-loop sign-off and assemble the release package:

- Review verification evidence: test execution proof, mutation score (>= 75%), static analysis report, and adversarial review sign-off.
- Verify that blast radius remains bounded within the initial assessment.
- Confirm explicit human approval for release branch staging or pull request creation.
- Assemble and emit `pull-request-spec.json` documenting PR metadata, test reports, touched files, and reviewer attestations.

### Checklist

- [ ] Functional specifications and interface contracts frozen in `feature-ticket.json` and `api-contract-spec.json`
- [ ] Initial blast radius and failure domains documented
- [ ] Automated tests authored and verified failing deterministically in Red stage
- [ ] Minimal implementation completed and verified passing in Green stage
- [ ] Tests and mutation analysis executed in isolated sandbox tier
- [ ] Mutation kill rate meets or exceeds the 75% threshold
- [ ] Adversarial review completed covering anti-vibe-slop and OWASP ASI guardrails
- [ ] Code review findings classified as Blocking, Important, or Follow-Up with all Blocking items resolved
- [ ] Human-in-the-loop architectural and product sign-off obtained
- [ ] `pull-request-spec.json` assembled and validated with full execution proofs

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [QA Validation](qa-validation.md)
- [Code Review](code-review.md)
- [Build & Deploy](build-deploy.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills

- **plan-technical-delivery**: Decompose feature tickets into verifiable milestone gates
- **write-tests**: Author independent Red tests and property-based verification suites
- **commit-code**: Stage verified changes under explicit user confirmation
- **agent-quality-gate**: Execute test suites and mutation testing within isolated sandboxes
- **review-code**: Adversarial multi-dimensional inspection against vibe slop and ASI vulnerabilities
- **meeting-review**: Human-in-the-loop review and architectural sign-off

### Failure Modes

- **Implementation precedes Red test**: developer writes code before tests fail, leading to self-fulfilling or tautological tests. **Mitigation:** enforce CI check or execution log proving test suite failed prior to implementation commits.
- **Spec drift mid-flight**: requirements change during implementation without unfreezing contracts. **Mitigation:** immediately halt implementation, return to Step 1, and re-freeze updated contracts with stakeholder sign-off.
- **Mock-only verification**: tests pass with mocks but fail against real services. **Mitigation:** execute integration tests against ephemeral service containers in Step 4.
- **Low mutation score**: tests provide high line coverage but fail to detect injected faults (<75% mutation kill rate). **Mitigation:** block Step 4 gate until surviving mutants are killed with assertions.
- **Bypassed HITL gate**: automated release triggers without human approval. **Mitigation:** enforce strict policy boundary requiring manual confirmation before PR merge or deployment.

### Output Contracts

When this workflow produces structured handoffs, emit:

- **`contracts/schemas/feature-ticket.json`** — Scoped requirements and frozen acceptance criteria.
- **`contracts/schemas/api-contract-spec.json`** — Frozen endpoint or schema definitions when interfaces change.
- **`contracts/schemas/test-report.json`** — Execution proof, sandbox tier, and mutation test scores.
- **`contracts/schemas/code-review-finding.json`** — Prioritized findings from adversarial code review.
- **`contracts/schemas/pull-request-spec.json`** — Complete pull request specification and sign-off package.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijacking**: Spec freeze and contract validation prevent prompt injection from overriding core feature requirements.
- **ASI04 Supply Chain Abuse**: All third-party dependencies introduced must undergo vulnerability reachability checks prior to sandbox execution.
- **ASI05 Unexpected Execution**: Code execution and test runs are strictly restricted to ephemeral sandbox tiers; no uncontained host execution is permitted.
- **ASI09 Human-Agent Trust Exploitation**: Mathematical proof of test execution and mutation scores is required; agent claims of completion without artifact evidence are rejected.
