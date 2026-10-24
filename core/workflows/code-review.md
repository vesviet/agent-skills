---
description: Multi-dimensional code review workflow integrating static analysis, anti-vibe-slop inspection, OWASP ASI security checks, and execution proof verification.
---

## Code Review Workflow

Use this workflow to perform comprehensive, multi-dimensional code reviews on proposed code changes, pull requests, or release candidates to ensure high architectural integrity, security robustness, and code determinism.

### Prerequisites

- A proposed code diff or pull request with clear ticket reference
- Clean compilation and baseline automated test execution results
- Access to static analysis, linter, and security audit toolchains
- Associated delivery artifacts (such as `feature-ticket.json` or `test-report.json`) available for context

### Workflow Steps

#### 1. Static Analysis and Linter Verification

Role: **Reviewer**, **QA Engineer**

Use skill: `agent-quality-gate`

Execute and verify automated static analysis gates before manual inspection:

- Run type checking, syntax linters, and style analyzers across all modified and newly created files.
- Verify cyclomatic complexity thresholds, dead code analyzers, and dependency boundary linters.
- Enforce a strict zero-warning policy: all automated lint and type errors must be resolved prior to manual review.
- Inspect formatting consistency against existing project conventions.

#### 2. Adversarial Anti-Vibe-Slop Inspection

Role: **Reviewer**, **Technical Lead**

Use skill: `review-code`

Conduct deep adversarial code inspection targeting subtle AI-generated bugs (vibe slop):

- Check for hallucinated library functions, unvalidated parameters, and silent exception swallows (`catch (Exception e) {}`).
- Inspect error handling paths: ensure errors fail fast with actionable, structured messages rather than generic fallback defaults.
- Scrutinize concurrency and state: inspect for race conditions, deadlock risks, unclosed resource handles, and thread safety.
- Detect performance regressions: look for N+1 database queries, unindexed lookups, memory retention leaks, and unbounded loops.
- Verify that the implementation directly solves the ticket scope without unnecessary abstraction layers or speculative facades.

#### 3. OWASP ASI and Security Audit

Role: **Security Engineer**, **Reviewer**

Use skill: `security-audit`

Audit the diff against the OWASP Top 10 for Agentic Applications and classical application security standards:

- Check **ASI01 Goal Hijacking**: verify that prompt templates, LLM system instructions, or dynamic command builders cannot be manipulated by untrusted user inputs.
- Check **ASI04 Supply Chain Abuse**: evaluate newly introduced packages for typosquatting, provenance attestations, known CVEs, and dependency reachability.
- Check **ASI05 Unexpected Execution**: confirm that dynamic code execution, eval calls, shell commands, or deserialization logic are strictly forbidden or safely sandboxed.
- Verify secrets management: ensure no API tokens, private keys, database credentials, or sensitive PII are committed in the diff.
- Verify authorization enforcement: ensure endpoints and operations validate permissions at the server boundary.

#### 4. Execution Proof and Mutation Verification

Role: **QA Engineer**, **Reviewer**

Use skill: `write-tests`

Verify the authenticity and efficacy of the automated tests:

- Inspect the test suite diff: verify that tests exercise genuine behavior and boundary conditions rather than tautologies or trivial assertions.
- Verify execution proofs: inspect CI test logs, execution sandbox isolation tier (`tier_0_ephemeral_container` or `tier_1_isolated_microvm`), and environment flags.
- Inspect mutation test scores (Stryker, mutmut, go-mutesting): verify that the mutation kill rate meets or exceeds the required 75% threshold.
- For bug fixes, confirm that a failing reproduction test was verified Red prior to the fix commit (`reproduction_test_verified: true`).

#### 5. Review Verdict and Deliverable Sign-Off

Role: **Reviewer**, **Technical Lead**

Use skill: `review-code`

Synthesize findings, communicate actionable feedback, and assign review verdict:

- Classify all findings into standard pack priorities:
  - **Blocking**: must be resolved before merge or release.
  - **Important**: should be addressed before general release; requires explicit sign-off if deferred.
  - **Follow-Up**: non-blocking technical debt or minor suggestions tracked in follow-up tickets.
- Avoid non-standard numeric priority tags.
- Emit structured review findings in `code-review-finding.json`.
- Set pull request review status in `pull-request-spec.json`: `APPROVED`, `CHANGES_REQUESTED`, or `ESCALATE_HITL`.

### Checklist

- [ ] Static analysis, linters, and type checkers pass with zero errors and zero warnings
- [ ] Adversarial inspection completed with anti-vibe-slop checklist verified
- [ ] Concurrency, resource lifecycle, and error handling audited
- [ ] OWASP ASI security review executed covering ASI01, ASI04, and ASI05
- [ ] Secrets scan completed with zero hardcoded credentials detected
- [ ] Test execution proof and sandbox isolation tier verified
- [ ] Mutation testing score verified against minimum 75% kill threshold
- [ ] For bug fixes, failing reproduction test verified Red prior to fix
- [ ] Findings categorized strictly as Blocking, Important, or Follow-Up
- [ ] `code-review-finding.json` emitted and `pull-request-spec.json` updated with review verdict

### Related Workflows

- [Feature Delivery](feature-delivery.md)
- [Bug Fix](bug-fix.md)
- [Tech Repo Review](tech-repo-review.md)
- [Security Incident Response](security-incident-response.md)
- [QA Validation](qa-validation.md)

### Related Skills

- **agent-quality-gate**: Execute automated linters, type checks, and static analyzers
- **review-code**: Conduct deep semantic and adversarial code analysis
- **security-audit**: Audit codebase for OWASP ASI vulnerabilities and credential leaks
- **write-tests**: Inspect test suite quality, boundary coverage, and mutation sensitivity
- **commit-code**: Stage review documentation and merge preparations under user confirmation

### Failure Modes

- **Superficial rubber-stamping**: approving code based purely on passing CI without adversarial inspection for hidden vibe-slop. **Mitigation:** enforce explicit anti-vibe-slop checklist sign-off in Step 2.
- **Tautological test evasion**: tests pass 100% but assert meaningless invariants (`assert true`). **Mitigation:** enforce Step 4 mutation test score verification (kill rate >= 75%).
- **OWASP ASI blind spot**: focusing solely on syntax style while missing prompt injection or sandbox evasion risks. **Mitigation:** mandatory security engineer review on all agent-facing or code-executing components.
- **Unclear finding severity**: feedback leaves the author unsure whether an issue blocks merge. **Mitigation:** mandatory classification into Blocking, Important, and Follow-Up.
- **Unverified execution claims**: reviewer trusts claims of successful execution without inspecting sandbox logs. **Mitigation:** Step 4 requires verifying the raw execution proof artifact.

### Output Contracts

When this workflow produces structured handoffs, emit:

- **`contracts/schemas/code-review-finding.json`** — Prioritized review findings with line-level references and remediation guidance.
- **`contracts/schemas/pull-request-spec.json`** — Updated pull request specification with reviewer attestations and verdict.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijacking**: Code reviewers must inspect prompt construction logic to prevent user data from poisoning agent instructions.
- **ASI04 Supply Chain Abuse**: Reviewers must verify lockfiles, package registries, and dependency provenance to prevent malicious package injection.
- **ASI05 Unexpected Execution**: Code under review must never include uncontained eval, dynamic script invocation, or execution paths escaping the designated sandbox.
- **ASI09 Human-Agent Trust Exploitation**: Reviewers must independently verify all agent assertions against execution artifacts and telemetry.
