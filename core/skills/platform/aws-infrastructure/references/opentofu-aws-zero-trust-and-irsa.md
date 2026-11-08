# OpenTofu AWS Zero-Trust & EKS Pod Identity Architecture (2026)

## 1. OpenTofu Client-Side State Encryption with AWS KMS

### 1.1 In-Memory Encryption (AES-GCM)
Remote Terraform/OpenTofu state files frequently leak plaintext database passwords, private keys, and token hashes. OpenTofu v1.13+ enforces client-side state encryption before writing to S3:
- The execution engine encrypts both state and plan files in memory using an AWS KMS Customer Master Key (CMK).
- Unencrypted state files uploaded to remote storage buckets are blocked via strict S3 bucket policies (`aws:SecureTransport` and `s3:x-amz-server-side-encryption`).

---

## 2. AWS IAM Zero-Trust & EKS Pod Identity (v1.31+)

### 2.1 EKS Pod Identity Association
Legacy IAM Roles for Service Accounts (IRSA) required complex OIDC provider thumbprints, STS AssumeRoleWithWebIdentity calls, and mutual IAM trust relationship mutations for every cluster.
- **EKS Pod Identity**: Modern clusters deploy `pods.eks.amazonaws.com` trust policies.
- **Zero Static Keys**: Root SCPs deny `iam:CreateAccessKey` cluster-wide.
- Pods obtain temporary, automatically rotated 60-minute AWS session credentials injected into the container environment via the AWS SDK:
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": { "Service": "pods.eks.amazonaws.com" },
        "Action": ["sts:AssumeRole", "sts:TagSession"]
      }
    ]
  }
  ```

---

## 3. Bottlerocket Distroless EKS Node Pools

- **Distroless Immutable Root**: Worker nodes run AWS Bottlerocket container Linux.
- **Security Invariants**:
  - `dm-verity`: Cryptographic kernel block-level integrity verification halting tampered nodes immediately.
  - SELinux enforcing by default; no interactive shells, package managers, or Python interpreters installed.
  - Updates apply atomically via A/B partition reboots.
