---
description: Generic workflow for building, validating, releasing, and verifying a change
---

## Build & Deploy Workflow

Use this workflow when a change is ready to move from local verification into a shared environment.

### When To Use

- after a feature or bug fix is complete
- after code review approval
- before handing a change to QA or release owners

### Prerequisites

- local implementation is complete
- verification commands pass locally
- release risk is understood

### Critical Rules

- prefer the repo's official CI/CD path over ad hoc local release steps
- do not edit generated release metadata by hand unless the repo explicitly expects that
- do not create a commit until the user explicitly confirms that commit action
- do not push, create a tag, or publish a release until the user explicitly confirms that specific action

### Workflow Steps

#### 1. Run Pre-Release Checks

Role: **Backend Developer**, **Frontend Developer**

From the target repo, run the normal quality gates:

- tests
- lint or static analysis
- build
- contract generation if the repo uses it

Also check:

- no accidental debug code
- no transient files staged for release
- no local-only config or credentials leaked into the change

#### 2. Review Release Impact

Role: **Reviewer**, **Technical Lead**

Use skill: `review-code`

Confirm:

- public contracts remain compatible unless the release is intentionally breaking
- schema or config changes are accounted for
- release notes or changelog entries are updated if the repo expects them
- dependent services or clients have been considered

#### 3. Prepare The Release Artifact

Role: **Backend Developer**, **Frontend Developer**

Use skill: `commit-code`

Depending on the repo, this may mean:

- pushing a branch
- opening a change request
- creating a version tag
- updating a release branch
- handing the change to an automated promotion pipeline

Follow the repo-local mechanism instead of assuming a specific Git provider or deployment repo.
Treat each remote or release-facing action as separately gated approval.

#### 4. Trigger Delivery

Role: **DevOps Engineer**

Use the repository's normal release path:

- CI pipeline
- deployment manifest update (GitOps via Argo CD or Flux v2 — update manifests in the source-of-truth repo, not runtime patching)
- package publish
- release promotion job (use Argo Rollouts for canary/blue-green with automated metric analysis when Kubernetes is the target)

Capture the release reference that matters locally, such as:

- commit SHA
- build number
- artifact version
- deployment revision

For SLSA compliance: verify the CI pipeline produces a signed provenance attestation (via Sigstore cosign / GitHub Artifact Attestations) before promoting to production. Admission control (Kyverno or OPA Gatekeeper) should reject images lacking valid signatures at the cluster boundary.

Track DORA metrics for this deployment: Deployment Frequency, Lead Time for Changes, and Change Failure Rate. Record these against the release reference.

#### 4b. Cloudflare Edge Release (optional)

Role: **Cloudflare Engineer**

When the target repo deploys via Wrangler (Workers, Pages, or bound services):

Use skill: `wrangler`

Emit `contracts/schemas/edge-deployment-spec.json` when machine handoff is required.

Coordinate with **DevOps Engineer** on secrets, environment names, and promotion order—do not bypass repo CI gates.

#### 5. Verify Rollout

Role: **DevOps Engineer**, **SRE**

After delivery starts:

- confirm the rollout reached the intended environment
- inspect logs and health checks
- verify critical dependencies are reachable
- run a focused smoke test on the changed path

Prefer repo-local dashboards, manifests, or service discovery entries over guessing direct URLs.

For Cloudflare targets, `debug-workers-edge` is not in this step's toolbox: delegate to **Cloudflare Engineer** when edge logs, bindings, or routing fail smoke checks, and record the handoff.

#### 6. Monitor And Decide

Role: **SRE**

For the first few minutes after rollout:

- watch error rates
- watch latency or resource spikes
- confirm no alerts or regressions appear

If problems appear:

- pause further promotion
- compare the current revision with the last known good one
- follow the repo's rollback or recovery procedure

#### 7. Record Outcome

Role: **Technical Lead**, **Technical Writer**

Capture:

- what was released
- where it was released
- how it was verified
- any follow-up work or residual risk

### Rollback Guidance

If rollback is needed:

- use the repo's standard rollback path first
- avoid manual edits that bypass the normal source of truth
- verify recovery using the same smoke checks as the forward deploy

### Checklist

- [ ] pre-release checks completed
- [ ] release impact reviewed
- [ ] release artifact prepared through the repo-local path
- [ ] delivery triggered with explicit approval when required
- [ ] rollout verified in the target environment
- [ ] monitoring reviewed for regressions
- [ ] outcome and residual risk recorded

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [Service Review & Release](service-review-release.md)
- [Troubleshooting](troubleshooting.md)
- [Hotfix Production](hotfix-production.md)

### Related Skills

- **review-code**: Review release-impacting implementation changes
- **commit-code**: Prepare approved changes for delivery
- **wrangler**: Wrangler CLI for deploying, developing, and managing Workers
- **debug-workers-edge**: Edge runtime diagnosis when rollout fails
- **troubleshoot-service**: Investigate failures during validation or rollout
- **review-service**: Confirm broad release readiness before shipping

### Failure Modes

- **Deploy without rollback verified**: a release ships but the previous deployment ID is not rollbackable. **Mitigation:** verify the rollback path and the previous artifact before applying the new release; reject the deploy when the path is not confirmed.
- **Pipeline silently skips a stage**: a CI step is marked optional and bypasses the gate. **Mitigation:** enforce a hard gate (non-zero exit) on every required stage; reject pipelines that allow skip; surface the skip in the deploy record.
- **Secret in pipeline config**: a token or key is committed to a CI variable file. **Mitigation:** use the platform secret store; run secret scanning in CI; rotate the affected credential on detection.
- **Region failover not tested**: a multi-region deploy has never exercised the failover. **Mitigation:** schedule a quarterly failover drill; surface the drill result; reject production cutover without a recent passing drill.
- **Permanent feature flag**: a flag is shipped without a `cleanup_target_date`. **Mitigation:** every flag must carry an ISO 8601 cleanup date; CI must reject the deploy if any flag is permanent.

### Output Contracts

When this workflow produces a structured handoff, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run` proving the deploy succeeded.
- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output for the build pipeline.
- **`contracts/schemas/incident-report.json`** — When the deploy triggers an anomaly; capture the trace span ids, the threshold, and the recommended action.

### Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: deploy credentials must be scoped to the deploy-owning role; reject deploys that request broader auth scopes than the role's `action-boundaries.yaml` profile.
- **ASI05 RCE Guard**: never construct deploy scripts, IaC modules, or rollback commands from external content without strict schema validation.
- **ASI08 Cascading Failures**: when a deploy step fails, surface the failure to the coordinator before allowing the next stage to proceed; never silently absorb a partial failure.
- **ASI09 Human-Agent Trust Exploitation**: do not present the deploy as "successful" without the smoke test passing; surface the actual `validation_run` evidence honestly.
