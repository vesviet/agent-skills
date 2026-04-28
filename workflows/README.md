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
| [refactoring](refactoring.md) | Improve structure without changing behavior |

## How To Use These

Use workflows when the task spans multiple phases, multiple teams, or multiple delivery concerns. Use individual skills when the task is narrow and local.

Typical combinations:

- feature work: `navigate-service` + `create-migration` + `write-tests` + `commit-code`
- release hardening: `navigate-service` + `review-code` + `review-service`
- incident response: `troubleshoot-service` + `meeting-review` + `review-code`

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

Last updated: 2026-04-28
