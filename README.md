# Engineering Agent Skills

Global engineering skill pack for software delivery work. The pack starts with a broadly reusable service-oriented foundation and is expanding toward a full global engineering pack.

## Layout

- `skills/`: default global core skills
- `workflows/`: longer end-to-end operating procedures
- `rules/`: always-on repo context rules
- `role/`: reusable software delivery role definitions
- `config/`: optional environment helpers

## Taxonomy

The full-pack target is organized into six categories:

- foundation: portable skills used across most codebases
- backend: service and API implementation skills
- frontend: UI, routing, client integration, and frontend testing skills
- platform: deployment, runtime, and delivery skills
- security-data: secrets, database operations, and security review skills
- documentation: docs, change communication, and technical radar skills

See [skills/README.md](skills/README.md) for the current inventory and roadmap.

## Skills Overview

### Foundation

| Skill | What it covers |
|-------|----------------|
| [commit-code](skills/commit-code/SKILL.md) | Pre-commit validation and commit flow |
| [create-migration](skills/create-migration/SKILL.md) | Add safe schema migrations |
| [meeting-review](skills/meeting-review/SKILL.md) | Structured multi-angle technical review |
| [navigate-service](skills/navigate-service/SKILL.md) | Understand an unfamiliar service quickly |
| [performance-profiling](skills/performance-profiling/SKILL.md) | Profile hot paths and regressions |
| [review-code](skills/review-code/SKILL.md) | Review code changes with P0/P1/P2 findings |
| [review-service](skills/review-service/SKILL.md) | Full service readiness and release review |
| [troubleshoot-service](skills/troubleshoot-service/SKILL.md) | Diagnose build, startup, and runtime failures |
| [write-tests](skills/write-tests/SKILL.md) | Add or improve unit and integration tests |

### Backend And Platform

| Skill | What it covers |
|-------|----------------|
| [add-api-endpoint](skills/add-api-endpoint/SKILL.md) | Add or evolve service endpoints safely |
| [add-event-handler](skills/add-event-handler/SKILL.md) | Add event consumers or publishers in local patterns |
| [add-service-client](skills/add-service-client/SKILL.md) | Add service-to-service integrations and client calls |
| [debug-runtime-platform](skills/debug-runtime-platform/SKILL.md) | Debug rollout, runtime, and environment issues beyond app code |
| [scaffold-new-service](skills/scaffold-new-service/SKILL.md) | Create a new service from local templates and conventions |
| [setup-deployment](skills/setup-deployment/SKILL.md) | Add or update deployment source-of-truth config |

### Frontend

| Skill | What it covers |
|-------|----------------|
| [add-ui-component](skills/add-ui-component/SKILL.md) | Build reusable UI components in local design patterns |
| [add-page-route](skills/add-page-route/SKILL.md) | Add or modify frontend pages and route flows |
| [integrate-api-client](skills/integrate-api-client/SKILL.md) | Connect frontend state to backend APIs safely |
| [frontend-testing](skills/frontend-testing/SKILL.md) | Add or improve UI and interaction test coverage |

### Security, Data, And Documentation

| Skill | What it covers |
|-------|----------------|
| [manage-secrets](skills/manage-secrets/SKILL.md) | Add, rotate, and review secret handling safely |
| [database-maintenance](skills/database-maintenance/SKILL.md) | Handle operational database maintenance safely |
| [security-audit](skills/security-audit/SKILL.md) | Review security posture and trust-boundary risk |
| [write-documentation](skills/write-documentation/SKILL.md) | Draft or update technical documentation clearly |
| [write-tech-radar](skills/write-tech-radar/SKILL.md) | Draft technology radar and recommendation entries |

## Workflows

See [workflows/README.md](workflows/README.md).

- `/add-new-feature`
- `/build-deploy`
- `/hotfix-production`
- `/refactoring`
- `/service-review-release`
- `/setup-new-service`
- `/troubleshooting`

## How To Adapt This Pack

When installing the pack into a different repository:

- start with the foundation skills first
- add backend, frontend, platform, security, or docs skills based on repo needs
- adapt module paths, docs paths, workflow references, and environment naming to the active repository

## Installation

Each core skill already contains:

- `SKILL.md`
- `agents/openai.yaml`

One simple install approach is symlinking only the core skills into your Codex skills directory:

```bash
cd agent-skills
mkdir -p ~/.codex/skills
for d in skills/*; do
  ln -sfn "$PWD/$d" "$HOME/.codex/skills/$(basename "$d")"
done
```

## Scope

This pack is meant to become a full global engineering pack. The foundation set should remain broadly reusable, while implementation and delivery skills should stay generic enough to adapt across different repositories and stacks.

## Stats

- 24 implemented skills
- 7 reusable workflows
- 14 reusable role definitions
- 1 always-on global rule file
- 6 taxonomy categories

Last updated: 2026-04-28
