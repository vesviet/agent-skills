# Microservices Agent Skills

Global skill pack for service-oriented engineering work. The default set is intentionally small and broadly reusable.

## Layout

- `skills/`: default global core skills
- `workflows/`: longer end-to-end operating procedures
- `rules/`: always-on repo context rules
- `role/`: reusable software delivery role definitions
- `config/`: optional environment helpers

## Skills Overview

### Core Skills

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

- start with `skills/` only
- adapt module paths, docs paths, and workflow references to the active repository

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

This pack is meant to be global and reusable. The skill set should remain broadly applicable across service-oriented repositories.

## Stats

- 9 core skills
- 7 reusable workflows
- 14 reusable role definitions
- 1 always-on global rule file

Last updated: 2026-04-28
