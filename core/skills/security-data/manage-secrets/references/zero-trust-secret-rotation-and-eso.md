# Zero-Trust Secret Rotation & External Secrets Operator (ESO) Architecture (2026)

## 1. Kubernetes External Secrets Operator (ESO v0.10+)

### 1.1 Namespace-Scoped SecretStore Isolation
Using cluster-wide `ClusterSecretStore` resources with unrestricted wildcard path access violates least privilege. Production GitOps clusters must enforce namespace-scoped `SecretStore` bindings:
- **ServiceAccount Token Projection**: ESO authenticates to HashiCorp Vault or AWS Secrets Manager using Kubernetes projected ServiceAccount tokens (JWTs) via OIDC Workload Identity Federation.
- **Synchronized Native Secrets**: ESO continuously synchronizes remote keys into Kubernetes native `v1/Secret` objects while preserving encryption in transit and at rest.

---

## 2. Dynamic Credential Rotation Lifecycle

### 2.1 The 4-Stage Zero-Downtime Rotation Cycle
Static long-lived API keys are prohibited. All service credentials must follow an automated 4-stage lifecycle:
1. **Provision New Credential**: Generate a new credential pair ($K_2$) alongside the active credential ($K_1$) in the upstream secret store (Vault/AWS SM).
2. **Dual-Accept State**: Consumers accept both $K_1$ and $K_2$ for signature verification and authentication during the transition window (typically 30–60 minutes).
3. **Switch Primary Producer**: Senders switch to emitting $K_2$ for outbound requests.
4. **Revoke Stale Credential**: Decommission $K_1$ once metrics confirm zero traffic authenticated with $K_1$.

---

## 3. GitOps Secret Hygiene with SOPS and age (X25519)

- **PGP/GPG Deprecation**: PGP/GPG encryption for committed GitOps manifests is fully deprecated.
- **SOPS + age**: All encrypted secrets stored in git repositories must use Mozilla SOPS with `age` public key encryption:
  ```bash
  sops --encrypt --age $(cat age.pub) secret.enc.yaml
  ```
- **Push Protection**: Automated pre-commit hooks running Gitleaks or TruffleHog scan every git commit for high-entropy tokens.
