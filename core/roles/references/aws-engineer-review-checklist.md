## AWS Engineer Review Checklist

This reference checklist provides comprehensive cloud architecture, infrastructure-as-code, identity governance, compute optimization, and security verification criteria for AWS engineering to meet 2026–2027 SOTA standards. It establishes non-negotiable verification gates across OpenTofu KMS client-side state encryption, Crossplane Go compositions, Bottlerocket distroless container hosts, AWS IAM Zero-Trust with EKS Pod Identity, Karpenter declarative autoscaling, Graviton4/Trainium2/Inferentia2 compute acceleration, sidecarless VPC Lattice service networking, Bedrock PrivateLink isolation with Guardrails v2, and FinOps cost governance.

### 1. OpenTofu v1.8+ Client-Side State Encryption & IaC Architecture (`OPENTOFU-KMS-LOCK`)
- **In-Memory Client-Side State Encryption**:
  - all Infrastructure as Code (IaC) state files (`.tfstate`) and execution plan files must be encrypted client-side in-memory using OpenTofu v1.8+ before transmitting bytes to remote S3 or HTTP backends
  - configuration mandates an `encryption {}` block specifying `key_provider "aws_kms"` with authenticated AES-GCM (256-bit) and `enforced = true` on both `state` and `plan` blocks:
    ```hcl
    terraform {
      encryption {
        key_provider "aws_kms" "primary" {
          kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/state-key-uuid"
          region     = "us-east-1"
          key_spec   = "AES_256"
        }
        method "aes_gcm" "state_encryption" {
          keys = key_provider.aws_kms.primary
        }
        state {
          method   = method.aes_gcm.state_encryption
          enforced = true
        }
        plan {
          method   = method.aes_gcm.state_encryption
          enforced = true
        }
      }
    }
    ```
  - relying solely on server-side S3 bucket encryption (SSE-S3 / SSE-KMS) without client-side encryption is strictly prohibited; unencrypted state uploads must be rejected fail-closed
- **Backend Resiliency & Distributed State Locking**:
  - remote S3 state backend configured with DynamoDB distributed state locking (`dynamodb_table`), object versioning, and bucket policies denying unencrypted transport (`aws:SecureTransport: false`)
  - static analysis (TFLint, Trivy) and automated assertions (`tofu test`) executed in CI/CD before any plan promotion

### 2. Universal Cloud Control Planes & Crossplane v1.16+ Go Compositions (`CROSSPLANE-COMPOSITION-LOCK`)
- **Kubernetes-Native Cloud Resource Management**:
  - cloud infrastructure managed as Kubernetes custom resources via Composite Resource Definitions (XRDs); platform teams expose high-level declarative claims while shielding developers from raw cloud parameter complexity
  - Crossplane Compositions authoring in pipeline mode powered by compiled Go functions (`function-go-templating`) or KCL (`function-kcl`), replacing legacy unstructured YAML patch-and-transform with compile-time type validation, conditionals, and deterministic loops
- **Closed-Loop Reconciliation & Cloud Drift Correction**:
  - continuous reconciliation loops actively detect and correct out-of-band AWS resource drift against desired XRD state
  - product development teams consume claims (`AppEnvironment`, `PostgreSQLInstance`) without requiring direct AWS IAM credentials or provider access

### 3. Bottlerocket Distroless Node OS & EKS Host Security (`BOTTLEROCKET-LOCK`)
- **Distroless Container-Optimized Host OS**:
  - all managed EKS worker node pools and Karpenter node classes must enforce AWS Bottlerocket distroless container OS (`amiFamily: Bottlerocket` in `EC2NodeClass`)
  - SELinux configured and actively operating in `enforcing` mode across all worker node pools
  - Linux kernel `dm-verity` cryptographic verification of root filesystem enabled at boot time; kernel halts immediately if root partition integrity check fails
  - root filesystem mounted strictly read-only; interactive shells (`/bin/sh`, `/bin/bash`) and package managers (`apt`, `yum`) completely eliminated from host filesystem
- **Transactional Updates & Minimal Attack Surface**:
  - OS updates applied transactionally via `apiclient` over Unix domain socket (`/run/api.sock`) to inactive disk partition with automatic A/B rollback on boot failure
  - ephemeral `control-container` (SSM) and `admin-container` disabled by default in production; enabled only via auditable break-glass approval with automated expiration

### 4. AWS IAM Zero-Trust, Identity Center & Access Governance (`AWS-IAM-ZERO-TRUST-LOCK`)
- **Zero Static Credentials & Centralized SSO**:
  - organization-wide Service Control Policy (SCP) enforces `iam:CreateAccessKey` deny at the root OU; zero static IAM users with long-lived `AKIA*` access keys in production accounts
  - AWS IAM Identity Center (SSO) integrated with enterprise IdP (Okta, Microsoft Entra ID) via SAML 2.0 and SCIM for all human operator access
  - short-lived STS session credentials (1h–4h TTL) enforced for all human engineers and administrative automation
- **Least-Privilege Policy Governance**:
  - customer-managed IAM policies specify exact actions and concrete resource ARNs; wildcard (`Resource: "*"`, `Action: "*"`) permissions are strictly prohibited in production
  - IAM Access Analyzer validation executed with zero public or cross-account access findings before any policy apply
  - Security Engineer review and explicit approval completed for all IAM policy modifications prior to production rollout

### 5. AWS EKS Pod Identity (v1.31+) & Workload Credential Federation
- **Link-Local Credential Federation**:
  - all Kubernetes workload ServiceAccounts mapped via `aws eks create-pod-identity-association` (`PodIdentityAssociation`)
  - IAM trust policies scope service principal `pods.eks.amazonaws.com` with `sts:AssumeRole` and `sts:TagSession`; legacy OIDC provider trust policies (IRSA) eliminated
  - credentials delivered via link-local endpoint `169.254.170.23` (`AWS_CONTAINER_CREDENTIALS_FULL_URI`) by `eks-pod-identity-agent` daemonset, completely eliminating STS regional rate-limiting bottlenecks under rapid scaling spikes
- **Attribute-Based Access Control (ABAC)**:
  - STS session tags (`eks-cluster-name`, `kubernetes-namespace`, `kubernetes-service-account`) automatically propagated to downstream AWS API requests for fine-grained policy enforcement

### 6. Karpenter v1.0+ Declarative Autoscaling & Compute Architecture
- **Just-In-Time Node Provisioning**:
  - compute autoscaling declared via Karpenter v1.0+ `NodePool` (`karpenter.sh/v1`) and `EC2NodeClass` (`karpenter.k8s.aws/v1`) manifests, provisioning instances directly from pending pod scheduling events
  - consolidation policy configured to `WhenEmptyOrUnderutilized` with 1m `consolidateAfter` for continuous bin-packing and cost minimization
- **Disruption Budgets & Drift Rollouts**:
  - disruption budgets declared (`budgets: [{nodes: "10%"}]`) with scheduled maintenance windows to protect workload availability during node replacement
  - automated drift detection enabled on Karpenter controllers to automate AMI rollouts and NodeClass configuration updates without downtime
  - static EC2 Managed Node Groups eliminated for dynamic microservice workloads

### 7. Graviton4, Trainium2 & Inferentia2 Compute Acceleration
- **Graviton4-First Compute Standard**:
  - general-purpose compute, microservices, and database workloads default to AWS Graviton4 (c8g, m8g, r8g) ARM64 architecture, delivering 20–30% lower cost and 10–15% better performance vs x86 equivalents
  - CI/CD build pipelines enforce multi-architecture container images (`linux/arm64,linux/amd64`)
- **Specialized AI/ML Silicon Acceleration**:
  - distributed generative AI training workloads deployed on Trainium2 (trn2) UltraClusters backed by Elastic Fabric Adapter (EFA v2) networking
  - high-throughput, low-latency LLM inference workloads benchmarked and deployed on Inferentia2 (inf2) instances using AWS Neuron SDK

### 8. Sidecarless Service Networking with AWS VPC Lattice (Gateway API)
- **Sidecarless L7 Application Networking**:
  - cross-VPC and cross-account microservice communication declared via Kubernetes Gateway API (`GatewayClass: amazon-vpc-lattice`)
  - application routes declared via `HTTPRoute` manifests supporting weighted canary traffic splitting (e.g. 90/10) and path-based routing
  - zero Envoy proxy sidecars injected into pods for cross-service networking, eliminating 60–80% CPU and memory tax and removing proxy injection lifecycles
- **Network-Level IAM Authentication**:
  - Service Network Auth Policies enforce AWS IAM SigV4 mutual authentication at the network layer, denying unauthenticated requests with HTTP 403 Forbidden before reaching backend pods

### 9. Enterprise Multi-Account Architecture, Control Tower & SCP Guardrails
- **Landing Zone Governance & OU Structure**:
  - multi-account architecture deployed via AWS Control Tower with Account Factory for Terraform (AFT)
  - strict Organizational Unit (OU) hierarchy enforced: Core/Security, Infrastructure, Workloads (Production, Staging, Dev), and Sandbox
- **Non-Negotiable Service Control Policies (SCPs)**:
  - SCPs enforce root account API deny, CloudTrail and AWS Config immutability, mandatory cost allocation tags, and regional operation restrictions (`aws:RequestedRegion`)
  - centralized network hub VPC deployed with Transit Gateway, AWS Network Firewall, and VPC Peering where appropriate

### 10. Cloud Storage, Database Resiliency & KMS Encryption at Rest
- **Storage Protection & S3 Express One Zone**:
  - Amazon S3 buckets enforce default server-side encryption with Customer-Managed Keys (SSE-KMS), S3 Block Public Access enabled at account and bucket levels, and object versioning
  - S3 Express One Zone deployed for low-latency (<10ms) AI training checkpoints, embedding caches, and high-throughput data processing
- **Database High Availability & KMS Key Rotation**:
  - Amazon RDS / Aurora deployed in Multi-AZ configuration with automated daily backups, deletion protection, and Performance Insights enabled
  - Customer-Managed KMS keys (CMK) configured with annual automated key rotation for all persistent EBS volumes, RDS clusters, and Secrets Manager stores

### 11. Amazon Bedrock & AI/ML Managed Infrastructure Isolation
- **PrivateLink VPC Isolation & Model ARN Scoping**:
  - Amazon Bedrock APIs accessed exclusively via PrivateLink VPC endpoints (`com.amazonaws.<region>.bedrock-runtime`, `com.amazonaws.<region>.bedrock`); direct public routing is prohibited
  - Bedrock IAM policies specify exact model ARNs; wildcard model access (`bedrock:InvokeModel` on `*`) is strictly prohibited
- **Guardrails v2 & Token-Level Cost Tracking**:
  - production Bedrock endpoints enforce Guardrails v2 with contextual grounding threshold $\ge 0.7$, PII redaction filters, and denied topics
  - token-level cost attribution tags (`team-id`, `service-name`, `budget-tier`) attached to invocation metadata for granular billing attribution

### 12. AWS FinOps Engineering & Cost Attribution Governance
- **Shift-Left Tagging Enforcement**:
  - mandatory cost allocation tags (`team`, `service`, `environment`, `cost-center`) enforced via SCP at creation time; untagged resource provisioning blocked fail-closed
  - CloudWatch Cost Allocation Tags activated in billing console; zero untagged resources permitted in production accounts
- **Rightsizing & Savings Strategies**:
  - AWS Compute Optimizer rightsizing recommendations reviewed monthly; rightsizing executed with risk justification
  - Compute Savings Plans and Spot Fleet strategies defined for fault-tolerant and batch workloads with automated interruption handling

### 13. Cloud-Native Observability, Telemetry & AWS Config Compliance
- **ADOT & Embedded Metric Format (EMF)**:
  - AWS Distro for OpenTelemetry (ADOT) Collector DaemonSet deployed with X-Ray trace propagation and W3C traceparent headers
  - CloudWatch Embedded Metric Format (EMF) utilized for high-cardinality metric generation directly from structured logs without custom metric API latency
- **Alarms & Automated Compliance**:
  - CloudWatch composite alarms configured with SNS routing to on-call paging systems; alarms evaluate percentiles (P99 latency), not averages
  - AWS Config conformance packs (CIS AWS Foundations Benchmark) active with automated EventBridge remediation rules

### 14. Machine Contract Artifacts & DevOps Handoff (`aws-infra-spec.json`)
- **Structured JSON Delivery Artifact**:
  - handoff artifact emitted and validated against `contracts/schemas/aws-infra-spec.json`
  - mandatory properties populated: `spec_id`, `system_name`, `aws_account`, `region`, `resource_map`, `iam_roles`, `cost_attribution`
  - authoritative delivery completed to DevOps Engineer for `deployment-plan.json` generation and Kubernetes manifest binding
