# Workflows

This directory contains reusable, longer-form workflows that sit above the individual skills.

## Available Workflows

| Workflow | Use it for |
|----------|------------|
| [build-deploy](build-deploy.md) | Build, validate, ship, and verify a change |
| [add-new-feature](add-new-feature.md) | End-to-end feature work across code, tests, docs, and rollout |
| [service-review-release](service-review-release.md) | Full readiness review before release |
| [troubleshooting](troubleshooting.md) | Diagnose build, startup, runtime, and platform problems |
| [setup-new-service](setup-new-service.md) | Bootstrap a new service or bounded component |
| [hotfix-production](hotfix-production.md) | Handle urgent production incidents safely |
| [revert-deployment](revert-deployment.md) | Safely roll back a failed deployment or release |
| [refactoring](refactoring.md) | Improve structure without changing behavior |
| [agent-a2a-delegation](agent-a2a-delegation.md) | Full A2A 1.0 delegate with discovery, streaming, and artifact validation |
| [security-incident-response](security-incident-response.md) | Respond to confirmed or suspected security incidents with safe containment and disclosure |
| [data-migration](data-migration.md) | Plan, execute, and verify database schema migrations safely |
| [dependency-upgrade](dependency-upgrade.md) | Safely upgrade dependencies with regression testing and security review |
| [seo-keyword-brief](seo-keyword-brief.md) | SEO Analyst: research intent, define keywords, map topical authority, produce seo-content-brief.json |
| [content-publishing](content-publishing.md) | Brief → draft → SEO audit → publish → publish-log (Content Writer + SEO Analyst + User) |
| [seo-content-lifecycle](seo-content-lifecycle.md) | End-to-end: Topic plan → SEO brief → Deep research → Draft → Audit → Publish (All Content Roles) |
| [content-audit](content-audit.md) | Content Manager: baseline audit → read → research latest standards → update → SEO re-audit → republish |
| [tech-repo-review](tech-repo-review.md) | Holistic repo health audit: architecture fitness, code quality, security posture, dependency health, docs |
| [qa-validation](qa-validation.md) | QA: coverage audit → risk-based test plan → execute → release confidence verdict |

## How To Use These

Use workflows when the task spans multiple phases, multiple teams, or multiple delivery concerns. Use individual skills when the task is narrow and local.

Typical combinations:

- feature work: `navigate-service` + `create-migration` + `write-tests` + `commit-code`
- release hardening: `navigate-service` + `review-code` + `review-service`
- edge release (Cloudflare): `wrangler` + `debug-workers-edge`
- incident response: `troubleshoot-service` + `meeting-review` + `review-code`

## Execution Standard (Checklist Driven)

When executing any workflow, the Agent MUST output a markdown checklist `[ ]` for all steps. The Agent MUST process only ONE step at a time, mark it as `[x]`, and explain the result before moving to the next step. Do not skip steps or execute multiple steps at once without explicit user permission.

## Skill Toolbox Rule For Workflow Steps

A workflow step may name a skill that is only **Supporting** for the role tagged on that step. When that happens, the SKILL TOOLBOX LOCK still applies: the tagged role must delegate to the role that holds the skill as Primary, or obtain explicit user permission, rather than executing it directly.

Before executing a step, resolve the skill it names:

1. If the skill is Primary for the tagged role — execute it.
2. If it is Supporting — identify the Primary owner in `core/roles/` and delegate, recording the handoff.
3. If it is in neither list — stop and ask the user.

Steps that commonly need this: `conduct-research`, `review-code`, `troubleshoot-service`, `navigate-service`, `create-migration`, and `database-maintenance` when driven by a planning, security, or operations role rather than by a developer role.

`commit-code` is Primary for **Backend Developer**, **Frontend Developer**, and **Mobile Engineer**. Other roles hold it as Supporting and must route commits through one of those roles — subject, always, to the rule in `core/rules/code.md` that no commit happens without explicit user confirmation.

## Adaptation Notes

These workflows are intentionally generic.

- Prefer repo-local standards, templates, and delivery checklists when they exist.
- Treat all commands and paths as examples unless they match the target repository.
- Adapt environment names, deployment commands, generated-code steps, and docs paths to the local setup.
- If a workflow step depends on tooling the repo does not use, skip that step and follow the local equivalent.

## Principles

- inspect before changing
- validate before committing
- prefer repo-local source of truth over assumptions
- keep public contracts backward compatible when possible
- capture findings, risk, and follow-up explicitly

## Workflow Authoring Standard

Every workflow file should include:

1. YAML frontmatter with a concise `description`.
2. One `## <Name> Workflow` title.
3. `### Prerequisites`.
4. `### Workflow Steps` with sequential `#### N. Step Name` headings.
5. A `Role:` line under every workflow step.
6. `### Checklist` covering the major workflow steps.
7. `### Related Workflows`.
8. `### Related Skills` using `- **skill-name**: description`.

Use `Blocking`, `Important`, and `Follow-Up` for prioritized findings. Do not introduce workflow-specific severity labels that conflict with the rest of the pack.

## Validation Gate

Run workflow validation after editing or adding workflows:

```bash
python3 core/scripts/validate-workflows.py
```

The validator checks frontmatter, required sections, sequential steps, role ownership, checklists, related workflow links, skill references, and stale priority labels.

Last updated: 2026-08-22

## 2026 Standards Embedded

All workflows now incorporate the following 2026 engineering standards:

- **AI-Assisted Delivery**: AI coding assistants (Cursor Agent, Copilot Agent, Claude Code) require `AGENTS.md` / `.cursorrules` root context files scoped to architecture boundaries before triggering multi-file agentic edits. AI code review tools (CodeRabbit, Qodo Merge) are advisory — human sign-off required on security-critical paths.
- **Mutation Testing Gate**: AI-generated test suites must achieve mutation score ≥75% (Stryker, mutmut, go-mutesting) before counting toward coverage. Branch coverage ≥85% on core business logic replaces line coverage as the primary QA KPI.
- **GitOps & Sigstore**: Deployments use Argo CD ApplicationSets or Flux HelmReleases as source of truth. CI artifacts must include Sigstore cosign provenance attestations (SLSA v1.0/v1.1). Kyverno/OPA Gatekeeper enforce no-unsigned-image admission.
- **OpenFeature**: Feature flag rollout uses the CNCF OpenFeature SDK for vendor-neutral flag evaluation — enables phased migration gating, circuit-breaker auto-revert, and shadow-write patterns.
- **DORA Metrics**: Deployment Frequency, Lead Time, Change Failure Rate, and MTTR are tracked per release. MTTR clock starts at confirmed production impact.
- **Contract Testing**: Pact v4 and Specmatic (OpenAPI/AsyncAPI as executable contracts) replace manual integration tests for service boundary changes.
- **Dependency Governance**: Renovate (preferred over Dependabot for polyglot stacks) automates upgrades. SBOM reachability analysis (Endor Labs, Snyk Reachability) deprioritizes unreachable CVEs. Socket.dev/Phylum guards against supply chain attacks.
- **Incident Response**: NIST CSF 2.0 Govern (GV.RR) pre-authorized containment, CycloneDX 1.6 SBOM blast radius queries, Zero-Trust SPIFFE/SPIRE + Cilium microsegmentation, and CVSS 4.0 × EPSS × CISA KEV triage triad.
- **Data Migration**: pgroll / Atlas for zero-downtime Postgres schema changes, dbt Core 1.9+ microbatch for idempotent time-slice backfills, OpenFeature canary flag gating for rollout phases.

## Standard 2026 Alignment

This file is part of the agent-skills engineering pack. The 2026 upgrade
pass added this footer so every prose file in the pack carries a
consistent Standard 2026 pointer.

- **OWASP ASI**: applied as described in `core/roles/role-standard.md`
  (ASI01-ASI10) and the per-skill `## Security Guardrails (OWASP ASI)` sections.
- **Failure Modes**: the rule in this file can be violated by drift, missing
  context, or untracked exceptions. Concrete failure scenarios belong in the
  related skill or workflow's `### Failure Modes` section.
- **Output Contracts**: structured artifacts produced under this file must
  conform to schemas in `core/contracts/schemas/`.
- **Skill Toolbox Lock**: this file's rules are enforced by the role that
  owns the affected action; the runtime gate is
  `core/scripts/hooks/check-policy.py`.
- **Commit / publish gate**: changes that affect user-visible behavior
  follow the META-RULE in `core/rules/code.md` — no commit, no push, no
  publish without explicit user confirmation.

Last updated: 2026-09-02
