# Engineering Delivery



#### `feature-ticket.json`

**Feature Ticket Specification**  
Structured output from Business Analyst. Consumed by Technical Architect (for adr-spec.json), Technical Lead (for technical-delivery-plan.json), and Backend/Frontend Developers as the source of truth for scope, acceptance criteria, and business rules. Also optionally triggers Data Analyst and SEO Analyst handoffs.

Required fields: `contract_type`, `title`, `type`, `acceptance_criteria`  
Size: 8,811 bytes  
✅ Has example

#### `technical-delivery-plan.json`

**Technical Delivery Plan**  
Structured implementation plan produced by Technical Lead. Consumed by Backend Developer, Frontend Developer, Mobile Engineer, QA Engineer, Reviewer, Agent Coordinator, and Technical Writer. One plan per feature or major slice grouping. Slices map directly to implementation-result.json emits.

Required fields: `contract_type`, `work_title`, `goal_summary`, `slices`, `quality_gates`, `readiness_status`  
Size: 7,879 bytes  
✅ Has example

#### `adr-spec.json`

**Architecture Decision Record**  
Structured output from Technical Architect documenting an Architecture Decision Record (ADR). Consumed by Backend Developer, Frontend Developer, Mobile Engineer, Cloudflare Engineer, Technical Lead, and Reviewer as a binding technical constraint. Supersedes earlier ADRs when architecture evolves.

Required fields: `contract_type`, `title`, `status`, `context`, `options_considered`, `decision`, `consequences`  
Size: 6,884 bytes  
✅ Has example

#### `architecture-options.json`

**Architecture Options Brief**  
Structured options analysis before an ADR is accepted.

Required fields: `contract_type`, `title`, `context`, `options`  
Size: 3,107 bytes  
✅ Has example

#### `implementation-result.json`

**Implementation Result**  
Structured output from a code implementation step. Emitted by Backend Developer, Frontend Developer, Mobile Engineer, 3D Graphics Engineer, or Cloudflare Engineer per delivery slice. Used by Technical Lead, Reviewer, Agent Coordinator, and QA Engineer for phase gate evidence. One document per slice.

Required fields: `contract_type`, `files_changed`, `breaking_changes`, `validation_run`  
Size: 6,448 bytes  
✅ Has example

#### `api-contract-spec.json`

**API Contract Specification**  
Structured output defining an API endpoint contract. Used for backend-to-frontend handoff and A2A delegation.

Required fields: `contract_type`, `endpoint`, `method`, `response_success`, `response_errors`  
Size: 3,605 bytes  
✅ Has example

#### `deployment-plan.json`

**Deployment Plan**  
Structured output for a deployment strategy and execution plan.

Required fields: `contract_type`, `version`, `environments`, `steps`, `rollback_plan`  
Size: 3,276 bytes  
✅ Has example

#### `edge-deployment-spec.json`

**Edge Deployment Specification**  
Structured Cloudflare edge deployment handoff: Wrangler, bindings, DNS/cache, rollout, and rollback.

Required fields: `contract_type`, `platform`, `project_ref`, `deployment_target`, `version`, `environments`, `wrangler_config_path`, `deploy_steps`, `rollback_plan`  
Size: 6,794 bytes  
✅ Has example

#### `system-design-spec.json`

**System Design Specification**  
Structured output from System Engineer for cloud-agnostic system topology, capacity models, and AI infrastructure specifications. Consumed by AWS Engineer (as upstream input for managed service provisioning), DevOps Engineer (as infrastructure baseline), Cloudflare Engineer (origin topology), and SRE (SLO design inputs).

Required fields: `contract_type`, `spec_id`, `system_name`, `design_trigger`, `nfr_targets`, `topology`, `capacity_model`  
Size: varies  
✅ Has example

#### `aws-infra-spec.json`

**AWS Infrastructure Specification**  
Machine-readable AWS infrastructure handoff produced by the AWS Engineer. Consumed by DevOps Engineer (EKS cluster endpoint, ECR repo URIs, pipeline inputs), SRE (Multi-AZ topology for SLO design), Security Engineer (IAM roles for review), and System Engineer (cross-layer integration). Contains resource_map, iam_roles (with review status), cost_attribution, monitoring_config, and iac_reference.

Required fields: `contract_type`, `spec_id`, `system_name`, `aws_account`, `region`, `resource_map`, `iam_roles`, `cost_attribution`  
Size: varies  
❌ No example yet
