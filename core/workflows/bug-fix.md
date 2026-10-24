---
description: Standardized bug fix workflow enforcing a mandatory Failing Reproduction Test (Red Gate) before code modification to eliminate blind fixes and regressions.
---

## Bug Fix Workflow

Use this workflow to diagnose, isolate, and remediate software defects in a disciplined manner that guarantees reproducibility and prevents regression.

### Prerequisites

- A reported bug, error log, crash report, or telemetry anomaly with identifiable symptoms
- Access to the target codebase and isolated testing environment
- Clean git status with baseline automated test suites passing

### Workflow Steps

#### 1. Symptom Ingestion and Defect Scoping

Role: **Site Reliability Engineer**, **QA Engineer**

Use skill: `troubleshoot-service`

Ingest incoming incident or bug reports and scope the failure boundary:

- Extract relevant error logs, stack traces, distributed traces, and environment parameters.
- Identify the exact inputs, user actions, or data states that triggered the anomaly.
- Determine whether production impact is active and requires immediate containment (if so, refer to `hotfix-production.md` for mitigation first).
- Frame the defect hypothesis with explicit expected vs actual behavior.

#### 2. Failing Reproduction Test Authoring (Red Gate)

Role: **QA Engineer**, **Backend Developer**

Use skill: `write-tests`

Author an automated test that deterministically reproduces the defect before touching any application code:

- **Mandatory Red Gate**: Any modification of production source code is strictly forbidden until an automated test reproducing the defect is authored and executed.
- Author a unit or integration test simulating the exact inputs and asserting expected behavior.
- Execute the test in an isolated test environment and confirm that it FAILS with the exact symptom reported.
- Verify that the failure is deterministic (not flaky) and isolate the test from external network dependencies.
- Record the failure evidence for inclusion in the verification audit trail.

#### 3. Root Cause Isolation and Blast Radius Assessment

Role: **Technical Lead**, **Backend Developer**

Use skill: `navigate-service`

Locate the exact defect mechanism and assess the blast radius of potential remediation:

- Trace execution flow through the codebase to pinpoint the root cause (e.g., off-by-one, race condition, unhandled null state, type mismatch).
- Assess the blast radius: identify failure domains, affected components, downstream consumers, and potential data corruption risks.
- Verify whether existing database records or cache entries are in an inconsistent state that requires data migration or cleanup.
- Formulate the smallest possible deterministic fix strategy.

#### 4. Targeted Minimal Remediation (Green Gate)

Role: **Backend Developer**, **Frontend Developer**

Use skill: `commit-code`

Apply the minimal code change necessary to resolve the defect:

- Implement the targeted fix directly addressing the isolated root cause.
- Execute the reproduction test and confirm that it now passes cleanly (Green Gate).
- Adhere strictly to the minimal change principle: no refactoring, code formatting, or unrelated cleanup in the fix diff.
- Ensure all preserved behaviors identified in the ticket remain intact.

#### 5. Regression Suite and Mutation Sensitivity Gate

Role: **QA Engineer**, **Technical Lead**

Use skill: `agent-quality-gate`

Validate the fix against the wider system and verify test sensitivity:

- Run the full test suite in an isolated sandbox tier to confirm zero regressions across existing functionality.
- Execute mutation testing on the fixed code block to ensure the new reproduction test is sensitive and capable of killing subtle mutants.
- Verify that performance and resource usage characteristics remain within acceptable SLO limits.
- Emit `test-report.json` with `reproduction_test_verified: true` and recorded mutation scores.

#### 6. Review and Fix Verification Proof Handoff

Role: **Reviewer**, **Technical Lead**

Use skill: `review-code`

Conduct code review and assemble verification artifacts for release:

- Review the fix diff to verify that changes are minimal, targeted, and free of anti-vibe-slop patterns.
- Validate the verification proof: confirm reproduction test logs (Red transitioning to Green) and full regression suite pass.
- Classify any review observations into Blocking, Important, or Follow-Up.
- Update `pull-request-spec.json` and prepare for staging or merge under explicit user confirmation.

### Checklist

- [ ] Symptom ingested with stack traces and reproduction parameters identified
- [ ] Automated reproduction test authored and verified failing in Red state before any code edit
- [ ] Root cause pinpointed and blast radius evaluated across downstream consumers
- [ ] Minimal targeted remediation implemented without unrelated opportunistic changes
- [ ] Reproduction test verified passing in Green state
- [ ] Full regression suite executed in isolated sandbox with zero existing test failures
- [ ] Mutation testing performed to confirm reproduction test sensitivity
- [ ] `test-report.json` emitted confirming reproduction_test_verified is true
- [ ] Code review completed with all Blocking items resolved
- [ ] `pull-request-spec.json` assembled with complete execution and verification proofs

### Related Workflows

- [Hotfix Production](hotfix-production.md)
- [Troubleshooting](troubleshooting.md)
- [Feature Delivery](feature-delivery.md)
- [Code Review](code-review.md)
- [QA Validation](qa-validation.md)

### Related Skills

- **troubleshoot-service**: Isolate symptoms, traces, and failing execution paths
- **write-tests**: Author deterministic reproduction test cases and regression assertions
- **navigate-service**: Inspect affected code paths and caller boundaries
- **commit-code**: Stage verified minimal bugfix with explicit user confirmation
- **agent-quality-gate**: Run regression and mutation test validation gates
- **review-code**: Verify bugfix minimal footprint and anti-regression proof

### Failure Modes

- **Blind fix attempt**: developer modifies source code without authoring a failing reproduction test first. **Mitigation:** hard gate in CI/review requiring proof of Red test execution prior to fix commit.
- **Flaky reproduction test**: test intermittently passes due to timing or unseeded randomness. **Mitigation:** run test 10 times consecutively in isolated sandbox before declaring it a valid reproduction.
- **Overreaching refactor**: bugfix includes opportunistic cleanup that introduces new latent defects. **Mitigation:** code review rejects diffs containing changes outside the isolated defect boundary.
- **Unaddressed data corruption**: bug is fixed in code but corrupt data in storage remains uncorrected. **Mitigation:** Step 3 blast radius check must assess storage state and schedule data-migration.md if data repair is required.
- **Unverified regression**: fix solves the immediate bug but breaks edge cases elsewhere. **Mitigation:** Step 5 requires full regression suite execution, not just the reproduction test.

### Output Contracts

When this workflow produces structured handoffs, emit:

- **`contracts/schemas/test-report.json`** — Execution report documenting the failing reproduction test, green pass, and regression suite status.
- **`contracts/schemas/code-review-finding.json`** — Code review assessment for the bugfix diff.
- **`contracts/schemas/pull-request-spec.json`** — Completed PR specification with reproduction verification flag and blast radius assessment.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijacking**: Defect descriptions must be sanitized to prevent malicious bug reports from prompting unauthorized code paths.
- **ASI04 Supply Chain Abuse**: Verify that the bug was not introduced by compromised or tampered upstream dependencies.
- **ASI05 Unexpected Execution**: Reproduction tests must run inside an isolated sandbox tier (`tier_0_ephemeral_container` or `tier_1_isolated_microvm`) to protect host environments.
- **ASI09 Human-Agent Trust Exploitation**: Proof of prior failure (Red) and subsequent pass (Green) must be provided in verifiable logs; verbal assertions of `it works now` are rejected.
