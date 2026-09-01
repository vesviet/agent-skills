---
name: aws-infrastructure
description: Provision, configure, and optimize AWS managed services following IaC-first discipline. Use when provisioning VPC, EC2, EKS, RDS, Lambda, S3, Bedrock, or SageMaker infrastructure; authoring IAM roles and policies; enforcing FinOps tagging and rightsizing; or configuring CloudWatch, X-Ray, and AWS Config observability.
---

# AWS Infrastructure

Use this skill when designing or deploying AWS-native infrastructure, configuring IAM roles and policies, applying FinOps cost-optimization strategies, or setting up observability for AWS services.

## When to Use

- provisioning a new VPC, EKS cluster, RDS instance, Lambda, or S3 bucket via IaC
- authoring or reviewing IAM roles, SCPs, or resource policies for least privilege
- applying FinOps cost-allocation tags and rightsizing recommendations
- enabling CloudWatch / X-Ray / AWS Config observability on a service
- producing the `aws-infra-spec.json` handoff for DevOps or System Engineer

## Example (Terraform)

```hcl
resource "aws_instance" "app" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"

  tags = {
    "team-id"      = "growth"
    "service-name" = "checkout"
    "budget-tier"  = "standard"
  }
}

resource "aws_cloudwatch_metric_alarm" "cpu" {
  alarm_name          = "checkout-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  threshold           = 80
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  evaluation_periods  = 2
  dimensions = {
    InstanceId = aws_instance.app.id
  }
}
```

## Core Rules

- **IaC First**: All infrastructure must be defined in CloudFormation, Terraform, or AWS CDK. No manual dashboard clicks in production.
- **Least Privilege IAM**: All IAM roles and policies must follow the principle of least privilege. Do not use wildcard `*` permissions unless strictly necessary and documented.
- **FinOps Enforcement**: Apply mandatory cost allocation tags to all resources (`team-id`, `service-name`, `budget-tier`). Implement rightsizing recommendations from Compute Optimizer.
- **Cross-Layer Awareness**: Coordinate with System Engineer for OS and network requirements, and DevOps Engineer for deployment pipelines.
- **EKS-AUTO-MODE**: Use EKS Auto Mode (GA 2026, Karpenter-based) for new clusters — eliminates manual node group management; Karpenter auto-provisions right-sized Graviton4 nodes on demand based on pending pod requirements.
- **GRAVITON4-FIRST**: Default all new compute to AWS Graviton4 (C8g, M8g, R8g) for 20-30% lower cost and 10-15% better performance vs x86 equivalents; build multi-arch images (`linux/amd64,linux/arm64`) as standard practice.
- **IAM-IDENTITY-CENTER**: All human and CI/CD access MUST use IAM Identity Center (SSO) with short-lived credentials. Prohibit creation of IAM Users with AKIA* long-lived access keys via SCP (`iam:CreateAccessKey` deny at root OU).
- **BEDROCK-GUARDRAILS-V2**: All production Bedrock endpoints MUST have Guardrails v2 with contextual grounding enabled — configure grounding threshold ≥ 0.7 to block hallucinated responses not grounded in the provided context.
- **S3-EXPRESS-AIWORKLOADS**: Use S3 Express One Zone for AI/ML training data, embedding caches, and high-throughput inference checkpoints requiring < 10ms latency at scale; standard S3 for compliance/backup/audit storage.

## Suggested Process

### Step 1: Collect Inputs
Gather requirements, including capacity needs, network topology inputs from System Engineer, security constraints, and cost limits.

### Step 2: Design Architecture
Draft the AWS architecture, mapping out VPCs, subnets, managed services (EKS, RDS, Lambda), and AI services (Bedrock, SageMaker). 

### Step 3: Author IAM and Security Policies
Draft IAM roles, resource policies, and SCPs. Submit them to the Security Engineer for review and approval.

### Step 4: Implement IaC
Write the infrastructure code. Ensure all FinOps tags are applied and observability tools (CloudWatch, X-Ray) are enabled.

### Step 5: Validate and Output
Test the IaC in a staging environment. Produce the `aws-infra-spec.json` handoff document to specify the provisioned resources, endpoints, and IAM roles.

## Checklist

- [ ] All resources defined in IaC.
- [ ] IAM roles and policies follow least privilege and have been reviewed by Security Engineer.
- [ ] Mandatory FinOps tags are applied to all taggable resources.
- [ ] Observability (CloudWatch, X-Ray) is configured for relevant services.
- [ ] `aws-infra-spec.json` is generated for downstream consumption.

## Output Contracts

When provisioning or updating AWS cloud infrastructure as part of a multi-role delivery, emit:

- **`contracts/schemas/aws-infra-spec.json`** — Emitted upon IaC specification and staging verification to document provisioned cloud resources, endpoints, IAM roles, and FinOps cost allocation tags. Set `produced_by_role: aws-engineer`.
- **`contracts/schemas/deployment-plan.json`** — Emitted when infrastructure modifications require an ordered rollout plan, documenting infrastructure changes, configuration updates, and validation runs.

Skip emission for local sandbox experimentation where no cloud resources are provisioned.

## Failure Modes

- **Manual dashboard change**: a resource is created or modified via the AWS console without IaC. Mitigation: enforce IaC-only via SCP; surface drift as a CI failure.
- **Wildcard IAM permission**: a policy grants `Action: "*"` on `Resource: "*"`. Mitigation: reject wildcard policies at code review; require least-privilege justification.
- **Missing FinOps tags**: a resource is provisioned without `team-id`, `service-name`, `budget-tier`. Mitigation: enforce tag policy via AWS Config; reject untagged resources in IaC.
- **Long-lived access key**: an IAM user with `AKIA*` key is created. Mitigation: enforce `iam:CreateAccessKey` deny SCP at the root OU; require IAM Identity Center for all human/CI access.
- **Bedrock without Guardrails**: a Bedrock endpoint is deployed without Guardrails v2. Mitigation: enforce Guardrails v2 with grounding threshold ≥ 0.7; reject ungrounded endpoints.
- **VRAM under-provisioned**: GPU memory allocation ignores KV cache + activation + safety headroom. Mitigation: enforce the GPU-VRAM formula at design time; require ≥ 15% headroom.
- **Multi-arch image missing**: a container image is built for `linux/amd64` only. Mitigation: enforce multi-arch build (`linux/amd64,linux/arm64`) in CI; default to Graviton4.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: IAM roles must follow least privilege; reject wildcard policies; require IAM Identity Center with short-lived credentials.
- **ASI04 Supply Chain**: Bedrock Guardrails v2 must be enabled on all production endpoints; S3 buckets must enforce `aws:SecureTransport` and block public access by default.
- **ASI05 RCE Guard**: never construct IAM policy JSON, user data scripts, or SSM commands from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the `aws-infra-spec.json` is consumed by multiple downstream roles; treat it as a public contract and review all changes before deploy.
- **ASI09 Human-Agent Trust Exploitation**: do not present an architecture as "least privilege" without a wildcard scan; surface any remaining wildcards honestly.

## Related Skills

- **system-design**: For cross-cloud and underlying OS/network topology.
- **setup-deployment**: For building deployment pipelines on top of the provisioned AWS infrastructure.
- **manage-secrets**: For configuring AWS Secrets Manager and rotation policies.
- **security-audit**: For reviewing IAM roles and AWS security posture.
