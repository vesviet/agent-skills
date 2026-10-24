# SOTA 2026–2027 AWS EKS Workload Deployment & Governance Guide

This guide establishes the production engineering standard for deploying, scaling, and managing cloud-native containerized workloads on Amazon Elastic Kubernetes Service (EKS) in modern enterprise environments.

---

## 1. Architectural Foundations: Modern AWS EKS vs Legacy EKS

| Dimension | Legacy EKS (2020–2023) | SOTA AWS EKS (2025–2027) | Operational Benefit |
| :--- | :--- | :--- | :--- |
| **Pod IAM Authentication** | IAM Roles for Service Accounts (IRSA) via OIDC provider | **AWS EKS Pod Identity** (`eks-pod-identity-agent`) | Eliminates OIDC provider trust management, reduces STS latency, scales to >10,000 pods without bottleneck. |
| **Node Autoscaling** | Cluster Autoscaler + Static EC2 Managed Node Groups (MNG) | **Karpenter v1.0+** & **EKS Auto Mode** (`NodePool` / `EC2NodeClass`) | Sub-minute JIT node provisioning, automated underutilization consolidation, Graviton4 (`c8g`, `m8g`) & AI accelerator support. |
| **Service Networking** | Ingress ALB Controller + Istio/Linkerd sidecar proxies | **AWS VPC Lattice** via **Kubernetes Gateway API** | Sidecarless L7 routing, zero proxy CPU/memory tax, cross-VPC/cross-account connectivity with IAM auth. |
| **Secret Management** | Kubernetes Secrets plain base64 or custom sync scripts | **External Secrets Operator (ESO)** with AWS Secrets Manager | Automated secret rotation via EventBridge, zero secrets in Git, least-privilege IAM scoping. |
| **Telemetry & Tracing** | CloudWatch Container Insights agent + X-Ray daemon | **AWS Distro for OpenTelemetry (ADOT)** + Application Signals | OpenTelemetry GenAI semantic conventions, tail-sampling, distributed tracing across services. |
| **Supply Chain Security** | Basic Docker Hub pulls, mutable tags | **Amazon ECR KMS** + **AWS Signer / Cosign** + **Kyverno Fail-Closed** | Immutable tags, automated Inspector v2 vulnerability/SBOM scans, cryptographically verified image admission. |

---

## 2. AWS EKS Pod Identity Configuration

EKS Pod Identity provides credentials directly to pods via the link-local endpoint (`169.254.170.23`) managed by the `eks-pod-identity-agent` DaemonSet.

### Step 1: IAM Trust Policy (`trust-policy.json`)
The IAM Role trusts the EKS Pod Identity service principal, not an OIDC cluster issuer:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "pods.eks.amazonaws.com"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ]
    }
  ]
}
```

### Step 2: Establish the Association
```bash
aws eks create-pod-identity-association \
  --cluster-name prod-ap-southeast-1 \
  --namespace checkout \
  --service-account checkout-service-sa \
  --role-arn arn:aws:iam::123456789012:role/CheckoutServiceWorkloadRole
```

### Step 3: Kubernetes ServiceAccount Manifest
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: checkout-service-sa
  namespace: checkout
```
*Note: No `eks.amazonaws.com/role-arn` annotation is required when using Pod Identity; the mapping is authoritative at the cluster API level.*

---

## 3. Karpenter v1.0+ Declarative Compute Orchestration

Karpenter v1.0 eliminates manual node group overhead by directly provisioning EC2 instances matched to pending pod resource specifications.

### 3.1 EC2NodeClass Manifest (`al2023-nodeclass.yaml`)
```yaml
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default-al2023
spec:
  amiFamily: AL2023
  role: "KarpenterNodeRole-prod-ap-southeast-1"
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: "prod-ap-southeast-1"
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: "prod-ap-southeast-1"
  amiSelectorTerms:
    - name: "amazon-eks-node-al2023-arm64-v1.31-*"
    - name: "amazon-eks-node-al2023-x86_64-v1.31-*"
  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 100Gi
        volumeType: gp3
        iops: 3000
        throughput: 125
        encrypted: true
        kmsKeyID: "arn:aws:kms:ap-southeast-1:123456789012:key/ebs-prod-key"
  metadataOptions:
    httpEndpoint: enabled
    httpProtocolIPv6: disabled
    httpPutResponseHopLimit: 2
    httpTokens: required
  tags:
    Environment: "production"
    ManagedBy: "karpenter"
```

### 3.2 NodePool Manifest for Microservices (`general-nodepool.yaml`)
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: general-compute
spec:
  template:
    metadata:
      labels:
        workload-tier: general
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
          values: ["c8g", "m8g", "c7g", "m7g", "c6g", "m6g"]
        - key: karpenter.k8s.aws/instance-generation
          operator: Gt
          values: ["5"]
  limits:
    cpu: "1000"
    memory: "4000Gi"
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 1m
    budgets:
      - nodes: 10%
        schedule: "0 9 * * mon-fri"
        duration: 8h
```

---

## 4. Sidecarless Service Networking with AWS VPC Lattice & Gateway API

The AWS Gateway API Controller for VPC Lattice implements Kubernetes Gateway API (`gateway.networking.k8s.io/v1`) without running sidecar proxies.

### 4.1 Gateway Declaration (`lattice-gateway.yaml`)
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: vpc-lattice-gw
  namespace: default
spec:
  gatewayClassName: amazon-vpc-lattice
  listeners:
    - name: http
      port: 80
      protocol: HTTP
```

### 4.2 Progressive Canary HTTPRoute (`checkout-canary-route.yaml`)
Enables weighted traffic shifting between stable and canary versions across VPCs:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: checkout-route
  namespace: checkout
spec:
  parentRefs:
    - name: vpc-lattice-gw
      sectionName: http
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api/v1/checkout
      backendRefs:
        - name: checkout-service-stable
          port: 8080
          weight: 90
        - name: checkout-service-canary
          port: 8080
          weight: 10
```

---

## 5. Declarative Secrets with External Secrets Operator & AWS Secrets Manager

### 5.1 ClusterSecretStore (`aws-clustersecretstore.yaml`)
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secretsmanager-pod-id
spec:
  provider:
    aws:
      service: SecretsManager
      region: ap-southeast-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets
```

### 5.2 Application ExternalSecret (`app-externalsecret.yaml`)
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: order-service-secrets
  namespace: orders
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager-pod-id
    kind: ClusterSecretStore
  target:
    name: order-service-env
    creationPolicy: Owner
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: prod/orders/database
        property: url
    - secretKey: REDIS_AUTH_TOKEN
      remoteRef:
        key: prod/orders/redis
        property: auth_token
```

---

## 6. AWS Distro for OpenTelemetry (ADOT) Collector Pipeline

Deploy the ADOT Collector DaemonSet for high-fidelity trace collection and CloudWatch Application Signals:

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: adot-collector
  namespace: opentelemetry
spec:
  mode: daemonset
  config:
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
    processors:
      memory_limiter:
        check_interval: 1s
        limit_percentage: 75
        spike_limit_percentage: 15
      k8sattributes:
        auth_type: "serviceAccount"
        passthrough: false
        extract:
          metadata:
            - k8s.pod.name
            - k8s.pod.uid
            - k8s.namespace.name
            - k8s.node.name
            - k8s.deployment.name
      batch:
        send_batch_size: 8192
        timeout: 5s
    exporters:
      awsxray:
        region: ap-southeast-1
      awsemf:
        region: ap-southeast-1
        log_group_name: "/aws/eks/adot/application-signals"
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, k8sattributes, batch]
          exporters: [awsxray]
        metrics:
          receivers: [otlp]
          processors: [memory_limiter, k8sattributes, batch]
          exporters: [awsemf]
```

---

## 7. Amazon ECR Supply Chain Security & Admission Control

### 7.1 Amazon ECR Repository Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceImmutableTags",
      "Effect": "Deny",
      "Principal": "*",
      "Action": [
        "ecr:PutImage"
      ],
      "Condition": {
        "StringNotEquals": {
          "ecr:ResourceTag/Immutable": "true"
        }
      }
    }
  ]
}
```

### 7.2 Kyverno Fail-Closed Admission Verification
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-ecr-signatures
spec:
  validationFailureAction: Enforce
  failurePolicy: Fail
  webhookTimeoutSeconds: 30
  rules:
    - name: verify-image-signature
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - "123456789012.dkr.ecr.ap-southeast-1.amazonaws.com/*"
          attestors:
            - entries:
                - keys:
                    publicKeys: |-
                      -----BEGIN PUBLIC KEY-----
                      MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
                      -----END PUBLIC KEY-----
```
