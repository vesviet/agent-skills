# Software Delivery Roles

This directory defines reusable roles for the full software delivery lifecycle.

The roles are global by default. They are meant to adapt to the active repository, product domain, and team structure instead of forcing one process on every project.

All roles in this directory are defined at a principal or master-practitioner level. They are expected to operate with strong judgment, broad system awareness, clear ownership across functions, and explicit impact analysis when behavior changes.

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

## Quality Baseline

All roles in this pack are expected to:

- make preserved versus changed behavior explicit
- check likely impact radius instead of trusting narrow local success
- surface skipped checks and residual risk instead of implying certainty
- hand off enough context that the next role can validate or act without guesswork
- use Agent Coordinator as the controlling role when one role must drive a full bug or feature across specialist roles

## Core Roles

### Coordination And Orchestration

- [agent-coordinator](agent-coordinator.md)

### Product And Discovery

- [product-manager](product-manager.md)
- [project-manager](project-manager.md)
- [task-planner](task-planner.md)
- [business-analyst](business-analyst.md)
- [researcher](researcher.md)
- [ui-ux-designer](ui-ux-designer.md)

### Architecture And Engineering

- [technical-architect](technical-architect.md)
- [technical-lead](technical-lead.md)
- [backend-developer](backend-developer.md)
- [frontend-developer](frontend-developer.md)
- [mobile-engineer](mobile-engineer.md)
- [3d-graphics-engineer](3d-graphics-engineer.md)
- [ecommerce-engineer](ecommerce-engineer.md)
- [security-engineer](security-engineer.md)

### Quality, Delivery, And Operations

- [agent-discovery-engineer](agent-discovery-engineer.md)
- [qa-engineer](qa-engineer.md)
- [reviewer](reviewer.md)
- [devops-engineer](devops-engineer.md)
- [cloudflare-engineer](cloudflare-engineer.md)
- [sre](sre.md)
- [technical-writer](technical-writer.md)
- [content-writer](content-writer.md)
- [seo-analyst](seo-analyst.md)

### Content Strategy And Editorial

- [content-manager](content-manager.md)

### Data And Analytics

- [data-analyst](data-analyst.md)
- [data-engineer](data-engineer.md)

### Education And Mentoring

- [teacher](teacher.md)


## Lifecycle Mapping

### Discovery

- Agent Coordinator
- Product Manager
- Business Analyst
- Researcher
- UI/UX Designer

### Planning

- Agent Coordinator
- Product Manager
- Project Manager
- Task Planner
- Technical Architect
- Technical Lead

### Implementation

- Agent Coordinator
- Backend Developer
- Frontend Developer
- Mobile Engineer
- E-commerce Engineer
- Technical Lead
- Security Engineer

### Validation

- Agent Coordinator
- QA Engineer
- Reviewer
- Mobile Engineer
- Technical Lead

### Release

- Agent Coordinator
- DevOps Engineer
- Cloudflare Engineer
- Mobile Engineer
- SRE
- Technical Writer
- SEO Analyst
- Content Writer
- Content Manager

### Operate And Improve

- Agent Coordinator
- SRE
- DevOps Engineer
- Cloudflare Engineer
- Reviewer
- Product Manager

### Data And Reporting

- Data Analyst
- Data Engineer
- Business Analyst
- Agent Coordinator

### Content And SEO

- Task Planner
- Content Manager
- SEO Analyst
- Content Writer
- Researcher

### Learning And Enablement

- Teacher
- Technical Writer
- Content Writer


## Recommended Workflows Per Role

| Role | Primary Workflows |
|------|------------------|
| Agent Coordinator | `/add-new-feature`, `/troubleshooting`, `/hotfix-production`, `/refactoring`, `/service-review-release`, `/agent-a2a-delegation` |
| Agent Discovery Engineer | `/build-deploy`, `/setup-new-service`, `/troubleshooting` |
| Product Manager | `/add-new-feature` |
| Project Manager | `/add-new-feature`, `/service-review-release` |
| Task Planner | `/add-new-feature`, `/refactoring`, `/troubleshooting` |
| Business Analyst | `/add-new-feature` |
| Researcher | `/add-new-feature`, `/troubleshooting` |
| UI/UX Designer | `/add-new-feature` |
| Technical Architect | `/setup-new-service`, `/refactoring` |
| Technical Lead | `/add-new-feature`, `/service-review-release`, `/refactoring` |
| Backend Developer | `/add-new-feature`, `/refactoring`, `/hotfix-production` |
| Frontend Developer | `/add-new-feature`, `/refactoring` |
| Mobile Engineer | `/add-new-feature`, `/refactoring`, `/troubleshooting`, `/hotfix-production` |
| 3D Graphics Engineer | `/add-new-feature`, `/refactoring`, `/troubleshooting` |
| QA Engineer | `/service-review-release` |
| Reviewer | `/service-review-release` |
| Security Engineer | `/service-review-release`, `/hotfix-production` |
| DevOps Engineer | `/build-deploy`, `/setup-new-service`, `/revert-deployment` |
| Cloudflare Engineer | `/build-deploy`, `/setup-new-service`, `/revert-deployment`, `/hotfix-production` |
| SRE | `/troubleshooting`, `/hotfix-production`, `/revert-deployment` |
| Technical Writer | `/add-new-feature`, `/service-review-release` |
| Content Writer | `/add-new-feature`, `/service-review-release` |
| SEO Analyst | `/add-new-feature`, `/service-review-release` |
| Content Manager | `/add-new-feature`, `/service-review-release` |
| Data Analyst | `/add-new-feature`, `/troubleshooting` |
| Data Engineer | `/troubleshooting`, `/setup-new-service` |
| Ecommerce Engineer | `/add-new-feature`, `/refactoring`, `/hotfix-production`, `/troubleshooting` |
| Teacher | `/add-new-feature`, `/refactoring` |

## Usage Notes

- Start with the smallest role set that can move the task forward.
- Combine roles when a task naturally spans multiple concerns.
- Prefer repo-local conventions over generic defaults when the repository already defines them.
- Treat these roles as operating modes, not job-title restrictions.
- Use Agent Coordinator when the user wants one role to control a bug fix or feature from intake through validated handoff while coordinating other specialist roles and phase gates.
- Do not treat "looks correct" or "one check passed" as sufficient when the change affects shared logic, contracts, data, or release behavior.

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
- make impact radius, skipped checks, and residual risk explicit where they materially affect handoff quality

## Validation Gate

Run role validation after editing or adding roles:

```bash
python3 core/scripts/validate-roles.py
python3 core/scripts/validate-2026-compliance.py
```

The validator checks required sections, section order, minimum content depth, toolbox references, duplicate toolbox entries, role inventory, and workflow mapping. The 2026 compliance validator checks A2A/contract coverage, coordinator wiring, full policy coverage, and graph orchestration infrastructure.

Last updated: 2026-05-22
