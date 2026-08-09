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

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Related Skills

- **system-design**: For cross-cloud and underlying OS/network topology.
- **setup-deployment**: For building deployment pipelines on top of the provisioned AWS infrastructure.
- **manage-secrets**: For configuring AWS Secrets Manager and rotation policies.
- **security-audit**: For reviewing IAM roles and AWS security posture.
