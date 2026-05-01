# Software Delivery Roles

This directory defines reusable roles for the full software delivery lifecycle.

The roles are global by default. They are meant to adapt to the active repository, product domain, and team structure instead of forcing one process on every project.

All roles in this directory are defined at a principal or master-practitioner level. They are expected to operate with strong judgment, broad system awareness, and clear ownership across functions.

## Directory Purpose

Use these role definitions when you want a clear working posture for a task, review, or project phase.

Every role in this directory must follow [role-standard.md](role-standard.md) first. The individual role file then applies that principal standard to a specific function.

Each role file describes:

- mission
- when to use the role
- core responsibilities
- required inputs
- expected outputs
- decision boundaries
- collaboration patterns
- guardrails
- definition of done

## Mandatory Standard

- [role-standard](role-standard.md)

## Core Roles

### Coordination And Orchestration

- [agent-coordinator](agent-coordinator.md)

### Product And Discovery

- [product-manager](product-manager.md)
- [project-manager](project-manager.md)
- [business-analyst](business-analyst.md)
- [ui-ux-designer](ui-ux-designer.md)

### Architecture And Engineering

- [technical-architect](technical-architect.md)
- [technical-lead](technical-lead.md)
- [backend-developer](backend-developer.md)
- [frontend-developer](frontend-developer.md)
- [security-engineer](security-engineer.md)

### Quality, Delivery, And Operations

- [qa-engineer](qa-engineer.md)
- [reviewer](reviewer.md)
- [devops-engineer](devops-engineer.md)
- [sre](sre.md)
- [technical-writer](technical-writer.md)

## Lifecycle Mapping

### Discovery

- Agent Coordinator
- Product Manager
- Business Analyst
- UI/UX Designer

### Planning

- Agent Coordinator
- Product Manager
- Project Manager
- Technical Architect
- Technical Lead

### Implementation

- Agent Coordinator
- Backend Developer
- Frontend Developer
- Technical Lead
- Security Engineer

### Validation

- Agent Coordinator
- QA Engineer
- Reviewer
- Technical Lead

### Release

- Agent Coordinator
- DevOps Engineer
- SRE
- Technical Writer

### Operate And Improve

- Agent Coordinator
- SRE
- DevOps Engineer
- Reviewer
- Product Manager

## Recommended Workflows Per Role

| Role | Primary Workflows |
|------|------------------|
| Agent Coordinator | `/add-new-feature`, `/troubleshooting`, `/hotfix-production`, `/refactoring`, `/service-review-release` |
| Product Manager | `/add-new-feature` |
| Project Manager | `/add-new-feature`, `/service-review-release` |
| Business Analyst | `/add-new-feature` |
| UI/UX Designer | `/add-new-feature` |
| Technical Architect | `/setup-new-service`, `/refactoring` |
| Technical Lead | `/add-new-feature`, `/service-review-release`, `/refactoring` |
| Backend Developer | `/add-new-feature`, `/refactoring`, `/hotfix-production` |
| Frontend Developer | `/add-new-feature`, `/refactoring` |
| QA Engineer | `/service-review-release` |
| Reviewer | `/service-review-release` |
| Security Engineer | `/service-review-release`, `/hotfix-production` |
| DevOps Engineer | `/build-deploy`, `/setup-new-service`, `/revert-deployment` |
| SRE | `/troubleshooting`, `/hotfix-production`, `/revert-deployment` |
| Technical Writer | `/add-new-feature`, `/service-review-release` |

## Usage Notes

- Start with the smallest role set that can move the task forward.
- Combine roles when a task naturally spans multiple concerns.
- Prefer repo-local conventions over generic defaults when the repository already defines them.
- Treat these roles as operating modes, not job-title restrictions.
- Use Agent Coordinator when the user wants one role to drive a bug fix or feature from intake through validated handoff while coordinating other roles.

## Role Authoring Standard

Every role file must follow [role-standard.md](role-standard.md) and keep the same baseline structure:

1. H1 role title matching the filename.
2. `Mission:` and `Level:` lines.
3. Mandatory role-standard reference.
4. Principal expectations, use cases, responsibilities, inputs, outputs, decision boundaries, collaboration, guardrails, skill toolbox, output template, review checklist, anti-patterns, handoff, and definition of done.

Quality expectations:

- keep roles principal-level and outcome-oriented, not task lists only
- make boundaries explicit so the role knows when to collaborate or escalate
- include at least one Primary Skill and reference only existing skills
- keep Supporting Skills for collaboration context, not direct ownership
- include an output template that can be reused directly
- include a review checklist and anti-patterns to make quality expectations concrete
- include role handoff guidance for upstream and downstream collaboration
- make Definition Of Done strong enough for handoff to the next role

## Validation Gate

Run role validation after editing or adding roles:

```bash
python3 scripts/validate-roles.py
```

The validator checks required sections, section order, minimum content depth, toolbox references, duplicate toolbox entries, role inventory, and workflow mapping.

Last updated: 2026-05-01
