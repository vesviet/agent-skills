---
description: Holistic technical review of a repository covering architecture fitness, code quality, security posture, dependency health, and documentation completeness — not a pre-release gate but an ongoing engineering health audit
---

## Tech Repo Review Workflow

Use this workflow for a comprehensive, non-release-gating technical audit of a repository. Unlike `service-review-release`, this is not triggered by a deployment — it is triggered by a need to understand the full technical health of a repo: architecture fitness, accumulated tech debt, security posture, dependency drift, and documentation gaps.

### When To Use

- onboarding to an unfamiliar codebase before contributing
- periodic engineering health review (quarterly, after major milestones)
- assessing acquisition, handover, or ownership transfer of a repo
- before planning a major refactor or architectural change
- identifying tech debt that should be scheduled and tracked
- security posture review outside of an active incident

### Prerequisites

- access to the repository source code and history
- the target review scope is defined (full repo, a subsystem, or a surface area)
- relevant architecture decisions, ADRs, or standards docs are accessible if they exist

### Workflow Steps

#### 1. Define Review Scope And Goals

Role: **Reviewer**, **Technical Architect**

Before opening any files:

- what is the review goal? (onboarding, debt assessment, security posture, handover, pre-refactor)
- what is in scope? (full repo, one service, one module, one architectural concern)
- what risk areas are most important to the current team?
- are there known problem areas to focus on first?

Document the scope so findings stay proportionate to the declared goal.

#### 2. Map The Repository Structure

Role: **Reviewer**, **Technical Architect**

Use skill: `navigate-service`

Build a structural map:

- entry points, main packages, and service boundaries
- layering: how is the code organized (handlers, business logic, data, shared)?
- cross-cutting concerns: auth, logging, config, error handling, observability
- external integrations: APIs consumed, events published/consumed, datastores
- CI/CD and deployment configuration: what is the pipeline and what does it validate?

Note any structural anomalies: circular imports, god packages, layer violations, undocumented entry points.

#### 3. Assess Architecture Fitness

Role: **Technical Architect**, **Reviewer**

Use skill: `navigate-service`

Evaluate:

- **boundary clarity**: are service or module boundaries well-defined and respected?
- **dependency direction**: do dependencies point inward (stable ← unstable)? Are abstractions in the right layer?
- **scalability assumptions**: are current architectural choices compatible with expected growth?
- **AI/agentic system fitness**: if LLMs, agents, or MCP tools are in scope — are probabilistic behavior, context windows, and tool-call trust treated as first-class concerns?
- **fitness functions**: is there automated CI enforcement of key architectural constraints, or are they advisory-only?

Escalate significant structural debt as Blocking or Important findings.

#### 4. Review Code Quality

Role: **Reviewer**

Use skill: `review-code`

Sample representative areas — do not try to read every line. Focus on:

- **correctness**: are there obvious logic bugs, edge case gaps, or unsafe assumptions?
- **error handling**: are errors propagated correctly? Are failures visible in logs?
- **test coverage**: what is the coverage strategy? Are risky paths tested?
- **duplication and coupling**: is there unnecessary duplication or tight coupling that creates fragility?
- **naming and readability**: can a new engineer follow the logic without the original author?

Classify findings: Blocking (correctness/security), Important (quality risk), Follow-Up (tech debt).

#### 5. Review Security Posture

Role: **Security Engineer**, **Reviewer**

Use skill: `security-audit`

Assess:

- **trust boundaries**: are auth and authz checks at the right layers?
- **input validation**: are external inputs validated before use?
- **secret handling**: are secrets in environment variables or secret managers — never hardcoded?
- **dependency exposure**: do dependencies have known CVEs? Are versions pinned appropriately?
- **logging safety**: is sensitive data (PII, tokens, credentials) excluded from logs?
- **attack surface**: are debug routes, admin surfaces, or internal APIs exposed to untrusted networks?

Do not expose real exploit details or credentials in review findings.

#### 6. Assess Dependency Health

Role: **Reviewer**, **Technical Architect**

Check:

- **version currency**: are major dependencies at reasonably current versions?
- **EOL risk**: are any runtimes, frameworks, or libraries approaching end-of-life?
- **CVE exposure**: run a dependency audit (for example: `npm audit`, `pip-audit`, `go mod verify`, `snyk test`, `trivy fs`)
- **reachability analysis**: use **Endor Labs**, **Snyk Reachability**, or **osv-scanner** to determine if CVEs in transitive dependencies are actually reachable via the application's call graph — up to 80% of transitive CVE alerts can be safely deprioritized when the vulnerable code path is provably unreachable
- **transitive risk**: are there deep transitive dependencies with supply-chain risk? Check with **Socket.dev** or **Phylum** for malicious install scripts, behavioral diffs, and typosquatting signals
- **lock file integrity**: are lock files committed and consistent with the manifest?
- **automation**: is **Renovate** (preferred for monorepos/polyglot) or Dependabot configured for ongoing dependency management with appropriate schedule windows and auto-merge rules for passing CI?
- **SLSA provenance**: do CI-built artifacts include signed Sigstore provenance attestations (cosign / GitHub Artifact Attestations)?

Classify stale or vulnerable dependencies by severity.

#### 7. Review Documentation Completeness

Role: **Technical Architect**, **Reviewer**

Check minimum documentation:

- **README**: does it explain what the service does, how to run it locally, and how to contribute?
- **architecture docs**: are key design decisions documented (ADRs, diagrams, service maps)?
- **operational runbook**: is there guidance for common ops tasks, health checks, and incident response?
- **API contracts**: are public contracts documented and versioned?
- **onboarding gap**: can a new engineer get the service running locally in under 30 minutes from the docs?

Flag missing or severely outdated docs as Important or Follow-Up.

#### 8. Compile And Deliver Findings

Role: **Reviewer**, **Technical Architect**

Use skill: `review-code`

Emit `code-review-finding.json` with findings categorized:

- **Blocking**: correctness bugs, active security vulnerabilities, critical structural violations
- **Important**: significant tech debt, dependency EOL, missing critical docs, architecture drift
- **Follow-Up**: style, readability, minor improvement opportunities

For each finding:
- file or module reference (when applicable)
- severity classification
- concrete recommendation
- estimated effort (low/medium/high) when useful for scheduling

Produce a summary with:
- overall health signal: Healthy / Needs Attention / Significant Risk
- top 3 findings requiring immediate action
- recommended remediation roadmap

### Review Output Template

```markdown
## Tech Repo Review: <repo>

Date: YYYY-MM-DD
Reviewer: <name>
Scope: <full repo | subsystem | surface>
Overall Health: Healthy / Needs Attention / Significant Risk

### Issue Summary
- Blocking: <count>
- Important: <count>
- Follow-Up: <count>

### Blocking Issues
1. <file or module>: <description and recommendation>

### Important Issues
1. <area>: <description and recommendation>

### Architecture Notes
<Key observations about structure, boundaries, fitness>

### Security Posture
<Key observations about trust boundaries, exposure, CVEs>

### Dependency Health
<Key observations about versions, EOL, lock file>

### Documentation Gaps
<Key missing or outdated docs>

### Recommended Roadmap
1. Immediate: <action>
2. Short-term (next sprint): <action>
3. Planned (next quarter): <action>
```

### Checklist

- [ ] review scope and goals documented
- [ ] repository structure mapped
- [ ] architecture fitness assessed — boundary clarity, dependency direction, AI fitness
- [ ] code quality sampled — correctness, error handling, test coverage
- [ ] security posture reviewed — trust boundaries, secrets, CVEs, attack surface
- [ ] dependency health audited — versions, EOL, CVEs, lock file
- [ ] documentation completeness checked
- [ ] code-review-finding.json emitted with Blocking/Important/Follow-Up classification
- [ ] overall health signal declared and remediation roadmap provided

### Related Workflows

- [service-review-release](service-review-release.md)
- [security-incident-response](security-incident-response.md)
- [refactoring](refactoring.md)
- [dependency-upgrade](dependency-upgrade.md)

### Related Skills

- **navigate-service**: Map the repository structure before reviewing it
- **review-code**: Review code quality and correctness across the codebase
- **review-service**: Full-service release readiness pass when pre-release scope is needed
- **security-audit**: Review security posture, trust boundaries, and attack surface
- **write-tech-radar**: Capture technology health and direction for the team
