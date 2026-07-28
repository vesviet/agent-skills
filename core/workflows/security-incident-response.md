---
description: Workflow for responding to a confirmed or suspected security incident with controlled disclosure, containment, and safe remediation
---

## Security Incident Response Workflow

Use this workflow when a confirmed or suspected security vulnerability, breach, or attack is active and requires structured, safe handling without public disclosure before mitigation.

### When To Use

- a vulnerability is reported by a researcher, user, or monitoring system
- active exploitation or unauthorized access is suspected
- sensitive data exposure is possible
- a supply chain or dependency attack is suspected

### Prerequisites

- the incident is real enough to act on (even suspected is sufficient)
- security-engineer or equivalent on-call is aware
- the team understands that no disclosure in user-visible artifacts (commits, changelogs, Slack) before the fix is shipped

### Workflow Steps

#### 1. Confirm And Classify The Incident

Role: **Security Engineer**, **Technical Lead**

Determine:

- is the report credible? (evidence of exploit, scan result, or PoC)
- what is the attack surface? (endpoint, dependency, config, authentication)
- what data or systems are at risk?
- is this active exploitation or a theoretical vulnerability?

Do not share vulnerability details in public channels, commit messages, or user-visible issue trackers.

Use skill: `conduct-research`

#### 2. Contain The Blast Radius Immediately

Role: **SRE**, **Security Engineer**, **DevOps Engineer**

Take the fastest safe mitigation first:

- disable the affected endpoint or feature flag
- rotate compromised credentials or tokens immediately
- isolate or scale down the affected service
- block the attack path at the network or WAF layer if possible
- revoke active sessions if authentication is compromised

Do not wait for root cause analysis before containment.

#### 3. Scope The Impact

Role: **Security Engineer**, **Backend Developer**

Answer:

- what data was accessible during the exposure window?
- which users, tenants, or environments are affected?
- is the data classified as confidential or restricted per `core/policies/data-classification.yaml`?
- is there evidence of exfiltration?

Use skill: `conduct-research`

Do not log or expose raw sensitive values in investigation artifacts.

#### 4. Develop And Review The Fix

Role: **Security Engineer**, **Backend Developer**, **Reviewer**

Rules:

- fix only the security issue — no opportunistic cleanup
- prefer the smallest, most reversible change
- keep the fix in a private branch until approved for disclosure

Use skill: `review-code`

Have a second reviewer confirm the fix before shipping.

#### 5. Test The Fix

Role: **Backend Developer**, **QA Engineer**, **Security Engineer**

Use skill: `write-tests`

Verify:

- the exploit path is closed
- regression coverage added for the vulnerable code path
- no new attack surface introduced by the fix

#### 6. Ship Through The Normal Emergency Path

Role: **Backend Developer**, **DevOps Engineer**

Use skill: `commit-code`

Do not create a commit until the user explicitly confirms that commit action.
Do not push, create a tag, or publish a release until the user explicitly confirms that specific action.

Coordinate security advisory timing with stakeholders before pushing to public repos.

#### 7. Disclose And Notify

Role: **Technical Lead**, **Security Engineer**

After the fix is shipped:

- notify affected users or tenants if required by policy or regulation
- publish a security advisory in coordination with stakeholders
- update CVE or vulnerability database entries if applicable
- notify downstream consumers of affected APIs or libraries

Disclosure must happen after the fix is deployed, not before.

#### 8. Conduct Post-Incident Review

Role: **Security Engineer**, **Technical Lead**, **Technical Writer**

Capture blameless:

- timeline: detection, containment, fix, disclosure
- root cause and contributing factors
- what monitoring or controls failed to catch it earlier
- action items to prevent recurrence

### Critical Rules

- never disclose vulnerability details in public commits, changelogs, or issue titles before the fix is shipped
- classify all investigation artifacts at `confidential` or `restricted` per `core/policies/data-classification.yaml`
- requires_approval for any data export or user data access during investigation
- rotate all secrets in the blast radius — do not try to determine exactly which ones were accessed

### Checklist

- [ ] incident confirmed and classified
- [ ] blast radius contained immediately
- [ ] impact scope determined without exposing raw data
- [ ] fix developed in a private branch
- [ ] fix reviewed by a second security-aware reviewer
- [ ] fix tested — exploit path closed and regression covered
- [ ] fix shipped through emergency path with explicit approvals
- [ ] disclosure coordinated and timed after fix
- [ ] post-incident review completed with action items

### Related Workflows

- [Hotfix Production](hotfix-production.md)
- [Revert Deployment](revert-deployment.md)
- [Troubleshooting](troubleshooting.md)

### Related Skills

- **conduct-research**: Investigate vulnerability scope and impact
- **review-code**: Review security-critical fix before shipping
- **write-tests**: Add regression coverage for the vulnerable path
- **commit-code**: Prepare approved fix for delivery
- **meeting-review**: Escalate cross-role incident decisions
