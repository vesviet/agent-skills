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
| [commit-code](skills/foundation/commit-code/SKILL.md) | Pre-commit validation and commit flow |
| [create-migration](skills/foundation/create-migration/SKILL.md) | Add safe schema migrations |
| [meeting-review](skills/foundation/meeting-review/SKILL.md) | Structured multi-angle technical review |
| [navigate-service](skills/foundation/navigate-service/SKILL.md) | Understand an unfamiliar service quickly |
| [performance-profiling](skills/foundation/performance-profiling/SKILL.md) | Profile hot paths and regressions |
| [review-code](skills/foundation/review-code/SKILL.md) | Review code changes with P0/P1/P2 findings |
| [review-service](skills/foundation/review-service/SKILL.md) | Full service readiness and release review |
| [troubleshoot-service](skills/foundation/troubleshoot-service/SKILL.md) | Diagnose build, startup, and runtime failures |
| [write-tests](skills/foundation/write-tests/SKILL.md) | Add or improve unit and integration tests |

### Backend And Platform

| Skill | What it covers |
|-------|----------------|
| [add-api-endpoint](skills/backend/add-api-endpoint/SKILL.md) | Add or evolve service endpoints safely |
| [add-event-handler](skills/backend/add-event-handler/SKILL.md) | Add event consumers or publishers in local patterns |
| [add-service-client](skills/backend/add-service-client/SKILL.md) | Add service-to-service integrations and client calls |
| [add-telemetry-instrumentation](skills/platform/add-telemetry-instrumentation/SKILL.md) | Add logging, metrics, and tracing to a service |
| [debug-runtime-platform](skills/platform/debug-runtime-platform/SKILL.md) | Debug rollout, runtime, and environment issues beyond app code |
| [scaffold-new-service](skills/backend/scaffold-new-service/SKILL.md) | Create a new service from local templates and conventions |
| [setup-deployment](skills/platform/setup-deployment/SKILL.md) | Add or update deployment source-of-truth config |

### Frontend

| Skill | What it covers |
|-------|----------------|
| [add-ui-component](skills/frontend/add-ui-component/SKILL.md) | Build reusable UI components in local design patterns |
| [add-page-route](skills/frontend/add-page-route/SKILL.md) | Add or modify frontend pages and route flows |
| [integrate-api-client](skills/frontend/integrate-api-client/SKILL.md) | Connect frontend state to backend APIs safely |
| [frontend-testing](skills/frontend/frontend-testing/SKILL.md) | Add or improve UI and interaction test coverage |

### Security, Data, And Documentation

| Skill | What it covers |
|-------|----------------|
| [manage-secrets](skills/security-data/manage-secrets/SKILL.md) | Add, rotate, and review secret handling safely |
| [database-maintenance](skills/security-data/database-maintenance/SKILL.md) | Handle operational database maintenance safely |
| [security-audit](skills/security-data/security-audit/SKILL.md) | Review security posture and trust-boundary risk |
| [write-documentation](skills/documentation/write-documentation/SKILL.md) | Draft or update technical documentation clearly |
| [write-tech-radar](skills/documentation/write-tech-radar/SKILL.md) | Draft technology radar and recommendation entries |

## Workflows

See [workflows/README.md](workflows/README.md).

- `/add-new-feature`
- `/build-deploy`
- `/hotfix-production`
- `/revert-deployment`
- `/refactoring`
- `/service-review-release`
- `/setup-new-service`
- `/troubleshooting`

## How To Adapt This Pack

When installing the pack into a different repository:

- start with the foundation skills first
- add backend, frontend, platform, security, or docs skills based on repo needs
- adapt module paths, docs paths, workflow references, and environment naming to the active repository

## Agent Compatibility

This pack includes adapter files for all major AI coding agents:

| Agent | Adapter File | Auto-Loads |
|-------|-------------|------------|
| OpenAI Codex | `skills/*/agents/openai.yaml` | Skills via `$skill-name` |
| Cursor | `.cursorrules` + `.cursor/rules/agent-skills.md` | Rules, Roles, Skills, Workflows |
| Claude Code | `CLAUDE.md` | Rules, Roles, Skills, Workflows |
| Antigravity / Gemini | `AGENTS.md` | Rules, Roles, Skills, Workflows |
| GitHub Copilot | `.github/copilot-instructions.md` | Rules, Skills summary |

All adapters point back to the same source of truth (`rules/code.md`, `role/role-standard.md`, `workflows/README.md`) instead of duplicating content.

## Installation

### Option 1: Clone Into Your Project (Recommended)

Clone or add as a submodule, then each agent will auto-detect its adapter file:

```bash
# as submodule
git submodule add <repo-url> agent-skills

# or just clone
git clone <repo-url> agent-skills
```

### Option 2: Symlink Skills Into Codex

```bash
cd agent-skills
mkdir -p ~/.codex/skills
for d in skills/*/*; do
  ln -sfn "$PWD/$d" "$HOME/.codex/skills/$(basename "$d")"
done
```

### Option 3: Copy Adapter Files Into Existing Repos

Copy only the adapter file(s) you need into your target project root:

```bash
# For Cursor
cp agent-skills/.cursorrules your-project/
cp -r agent-skills/.cursor your-project/

# For Claude Code
cp agent-skills/CLAUDE.md your-project/

# For Antigravity / Gemini
cp agent-skills/AGENTS.md your-project/

# For GitHub Copilot
cp -r agent-skills/.github your-project/
```

## Scope

This pack is meant to become a full global engineering pack. The foundation set should remain broadly reusable, while implementation and delivery skills should stay generic enough to adapt across different repositories and stacks.

## Stats

- 25 implemented skills
- 8 reusable workflows
- 14 reusable role definitions (each with Skill Toolbox)
- 1 always-on global rule file
- 6 taxonomy categories
- 5 agent adapters (Codex, Cursor, Claude, Antigravity, Copilot)

Last updated: 2026-04-28
