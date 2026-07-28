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

Last updated: 2026-06-12
