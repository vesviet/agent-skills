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

- Product Manager
- Business Analyst
- UI/UX Designer

### Planning

- Product Manager
- Project Manager
- Technical Architect
- Technical Lead

### Implementation

- Backend Developer
- Frontend Developer
- Technical Lead
- Security Engineer

### Validation

- QA Engineer
- Reviewer
- Technical Lead

### Release

- DevOps Engineer
- SRE
- Technical Writer

### Operate And Improve

- SRE
- DevOps Engineer
- Reviewer
- Product Manager

## Recommended Workflows Per Role

| Role | Primary Workflows |
|------|------------------|
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

Last updated: 2026-04-28
