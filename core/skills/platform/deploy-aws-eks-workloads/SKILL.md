---
name: deploy-aws-eks-workloads
description: Deploy, scale, and govern cloud-native application workloads on Amazon EKS using SOTA 2026-2027 AWS standards. Use when configuring Karpenter v1.0+ declarative NodePools, EKS Pod Identity associations, AWS VPC Lattice Gateway API routes, ADOT telemetry pipelines, ECR image verification, and GitOps delivery pipelines on AWS.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Deploy AWS EKS Workloads

Use this skill when deploying, configuring, and governing production Kubernetes workloads on Amazon EKS in accordance with 2026–2027 AWS Cloud-Native standards.

## When to Use

- deploying containerized applications and microservices to Amazon EKS via GitOps
- configuring declarative node autoscaling via Karpenter v1.0+ (`NodePool` and `EC2NodeClass`)
- establishing IAM credentials for pods using AWS EKS Pod Identity (replacing legacy IRSA)
- setting up sidecarless cross-VPC service communication with AWS VPC Lattice and Kubernetes Gateway API
- synchronizing application secrets from AWS Secrets Manager using External Secrets Operator (ESO)
- instrumenting EKS workloads with AWS Distro for OpenTelemetry (ADOT) and CloudWatch Application Signals
- enforcing supply chain security with Amazon ECR immutable tags, Inspector v2 SBOMs, and AWS Signer

## Core Rules

- **Mandate EKS Pod Identity**: use cluster-level Pod Identity associations (`aws eks create-pod-identity-association`) for all workload ServiceAccounts; eliminate legacy IRSA OIDC trust policy overhead and STS scaling bottlenecks.
- **Karpenter v1.0+ Declarative Autoscaling**: declare workload node requirements using `karpenter.sh/v1` `NodePool` and `karpenter.k8s.aws/v1` `EC2NodeClass`; configure consolidation policy `WhenEmptyOrUnderutilized`, disruption budgets (`budgets: [{nodes: "10%"}]`), Graviton4 (`c8g`, `m8g`), and specialized accelerators (`trn2`, `inf2`, `g6`).
- **Sidecarless VPC Lattice Mesh**: route service traffic through the AWS Gateway API Controller for VPC Lattice (`GatewayClass: amazon-vpc-lattice`) using Kubernetes Gateway API `HTTPRoute` objects; enforce IAM authorization without proxy sidecar overhead.
- **ECR Supply Chain & Immutable Tags**: pull images exclusively from KMS-encrypted Amazon ECR repositories with immutable tags (`imageTagMutability: IMMUTABLE`); enforce Kyverno admission policies verifying Cosign/AWS Signer signatures and Inspector v2 vulnerability attestations.
- **Declarative Secret Synchronization**: synchronize credentials from AWS Secrets Manager using External Secrets Operator (`ClusterSecretStore` / `ExternalSecret`) authenticated via EKS Pod Identity; never store plaintext or base64 secrets in Git.
- **Standardized ADOT Observability**: deploy AWS Distro for OpenTelemetry (ADOT) Collector with OpenTelemetry GenAI semantic conventions, X-Ray trace context propagation, and CloudWatch Application Signals.
- refer to `references/aws-eks-workload-guide.md` for production YAML manifests, Karpenter CRD configurations, and VPC Lattice gateway specs.

## Suggested Process

### 1. Configure EKS Pod Identity
Bind the target Kubernetes ServiceAccount to an AWS IAM Role via EKS Pod Identity:
```bash
aws eks create-pod-identity-association \
  --cluster-name production-eks-cluster \
  --namespace checkout \
  --service-account checkout-service-sa \
  --role-arn arn:aws:iam::123456789012:role/CheckoutServiceWorkloadRole
```

### 2. Declare Karpenter v1.0 NodePool & EC2NodeClass
Define workload compute provisioning with automated consolidation and disruption limits:
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: checkout-workloads
spec:
  template:
    spec:
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default-al2023
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand", "spot"]
        - key: kubernetes.io/arch
          operator: In
          values: ["arm64", "amd64"]
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["c8g", "m8g", "c7g", "m7g"]
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 1m
    budgets:
      - nodes: 10%
```

### 3. Synchronize Secrets via External Secrets Operator
Declare an `ExternalSecret` retrieving credentials from AWS Secrets Manager using the Pod Identity-backed SecretStore:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: checkout-database-credentials
  namespace: checkout
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager-pod-id
    kind: ClusterSecretStore
  target:
    name: checkout-db-secret
    creationPolicy: Owner
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: production/checkout/database
        property: password
```

### 4. Deploy Workload via GitOps & ArgoCD
Commit Kustomize overlays and workload manifests to the GitOps repository. Deploy via ArgoCD enforcing Server-Side Apply (`syncOptions: [ServerSideApply=true]`).

### 5. Expose Workload via VPC Lattice HTTPRoute
Expose microservice endpoints across VPCs without sidecars using Kubernetes Gateway API:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: checkout-route
  namespace: checkout
spec:
  parentRefs:
    - name: vpc-lattice-gateway
      sectionName: http
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api/v1/checkout
      backendRefs:
        - name: checkout-service
          port: 8080
```

### 6. Verify Deployment & Observability
Check pod status, Pod Identity credential mounts (`AWS_CONTAINER_CREDENTIALS_FULL_URI`), ADOT trace exports in AWS X-Ray, and CloudWatch Application Signals SLO metrics.

## Checklist

- [ ] Verify EKS Pod Identity association is created for the target ServiceAccount (`aws eks create-pod-identity-association`)
- [ ] Confirm Karpenter v1.0+ NodePool specifies `WhenEmptyOrUnderutilized` consolidation and disruption budget
- [ ] Ensure ExternalSecret targets Secrets Manager via Pod Identity SecretStore with zero credentials in Git
- [ ] Validate container image is pulled from KMS-encrypted ECR with immutable tags and Kyverno verification
- [ ] Verify Kubernetes Gateway API HTTPRoute is bound to VPC Lattice gateway without proxy sidecar injection
- [ ] Confirm ADOT Collector is exporting traces to AWS X-Ray and emitting CloudWatch Application Signals metrics

## Related Skills

- **setup-deployment**: GitOps delivery pipelines and ArgoCD application manifests
- **aws-infrastructure**: Provisioning foundational AWS resources (VPC, control planes, IAM roles)
- **debug-runtime-platform**: Diagnosing pod crash loops, networking issues, and ephemeral debugging
- **manage-secrets**: Enterprise secret management workflows and credential rotation
- **add-telemetry-instrumentation**: OpenTelemetry Collector pipelines and distributed tracing
