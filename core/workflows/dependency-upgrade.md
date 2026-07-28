---
description: Workflow for safely upgrading dependencies with regression testing, security review, and controlled rollout
---

## Dependency Upgrade Workflow

Use this workflow when upgrading third-party libraries, frameworks, runtimes, or infrastructure dependencies in a controlled and regression-safe way.

### When To Use

- applying security patches from vulnerability advisories (CVE, Dependabot, Snyk)
- upgrading to a new minor or major version of a key dependency
- resolving version conflicts between transitive dependencies
- keeping dependencies within support windows before EOL

### Prerequisites

- the dependency to upgrade and the target version are identified
- the reason for the upgrade is clear (security, compatibility, EOL, feature need)
- the team has a way to run the full test suite

### Upgrade Risk Tiers

| Tier | Scope | Approval Required |
|------|-------|-------------------|
| Patch (`1.2.3` → `1.2.4`) | Bug/security fix only | Reviewer |
| Minor (`1.2.x` → `1.3.x`) | New features, backward compatible | Technical Lead |
| Major (`1.x.x` → `2.x.x`) | Breaking changes possible | Technical Architect |

### Workflow Steps

#### 1. Assess The Upgrade

Role: **Backend Developer**, **Security Engineer**

Determine:

- what changed in the target version? (changelog, release notes, security advisories)
- are there breaking changes in the API or runtime behavior?
- does the new version require minimum runtime or peer dependency changes?
- are there known issues or CVEs being fixed?

Use skill: `conduct-research`

#### 2. Check Transitive Impact

Role: **Backend Developer**, **Technical Lead**

Before changing the manifest:

- identify all packages that depend on this dependency transitively
- check whether other packages in the project also pin this dependency at a conflicting version
- verify the target version is compatible with the current runtime (Node.js, Python, JVM, etc.)

Use skill: `navigate-service`

#### 3. Apply The Upgrade

Role: **Backend Developer**

Upgrade through the repo's package manager:

- update the manifest file (for example: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`)
- run the dependency resolution command (for example: `npm install`, `pip install`, `go mod tidy`)
- commit the updated lock file — do not regenerate without reviewing the diff

For major version upgrades, adapt the call sites to the new API before running tests.

#### 4. Review The Upgrade Diff

Role: **Reviewer**, **Security Engineer**

Use skill: `review-code`

Verify:

- only the intended package and its transitive tree changed
- no unexpected packages were added, removed, or version-bumped
- no known malicious or compromised versions introduced (check advisory databases)
- lock file changes are consistent with the manifest update

For security patches: confirm the CVE is addressed by the target version.

#### 5. Run Full Verification

Role: **Backend Developer**, **QA Engineer**

Use skill: `write-tests` if existing tests do not cover the upgraded code paths.

Run:

- full test suite
- lint and static analysis
- build
- integration tests if available

If tests fail after the upgrade:

- check if the failure is caused by a breaking change in the new version
- check whether a test fixture or mock needs updating to match new behavior
- do not suppress the failure — investigate before proceeding

#### 6. Verify Security Posture

Role: **Security Engineer**, **Backend Developer**

For security-driven upgrades:

- rerun the vulnerability scanner to confirm the advisory is resolved
- verify no new advisories were introduced by the upgrade
- check the diff for new network calls, data access patterns, or permission requirements in the new version

#### 7. Prepare Delivery

Role: **Backend Developer**, **Technical Lead**

Use skill: `commit-code`

Do not create a commit until the user explicitly confirms that commit action.
Do not push, create a tag, or publish a release until the user explicitly confirms that specific action.

Include in the commit or change description:

- dependency name and version range upgraded
- reason (security patch CVE number, EOL, feature need)
- test result summary

#### 8. Monitor After Release

Role: **SRE**, **DevOps Engineer**

After the change is deployed:

- watch for unexpected runtime errors, performance changes, or behavior differences
- check logs for deprecation warnings from the new version
- verify dependent systems remain healthy

### Checklist

- [ ] upgrade reason and breaking change risk assessed
- [ ] transitive impact checked
- [ ] upgrade applied through the repo's package manager
- [ ] lock file diff reviewed — no unexpected changes
- [ ] full test suite, lint, and build pass
- [ ] security posture verified for security-driven upgrades
- [ ] delivery prepared with explicit approval
- [ ] post-release monitoring confirms stability

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [Security Incident Response](security-incident-response.md)
- [Build \& Deploy](build-deploy.md)

### Related Skills

- **conduct-research**: Investigate the dependency changelog and advisory databases
- **navigate-service**: Identify call sites before applying breaking API changes
- **review-code**: Review the manifest, lock file, and call site changes
- **write-tests**: Add coverage for newly-upgraded code paths
- **commit-code**: Prepare approved upgrade changes for delivery
