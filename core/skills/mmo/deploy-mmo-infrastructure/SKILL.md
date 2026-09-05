---
name: deploy-mmo-infrastructure
description: Deploy and manage proxy pools (Residential/4G) and Anti-Detect Browser orchestration environments (via Docker/Terraform) ensuring zero IP/footprint leaks. Use when deploying a new MMO operation, expanding to new ad accounts, or migrating proxy infrastructure.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Deploy MMO Infrastructure

Use this skill to provision isolated proxy and browser-profile infrastructure for Make Money Online (MMO) operations.

## Legal & Compliance Notice

Anti-detect browsers and fingerprint normalization exist in a grey zone: using them to manage multiple legitimate accounts is common practice, but using them specifically to evade a platform's fraud, ownership, or ad-review detection is a ToS violation on most ad and affiliate platforms and can carry account or payment-processor consequences beyond the immediate operation. This skill documents proxy/browser provisioning mechanics only. Anonymity and isolation techniques used to protect legitimate multi-account operations are in scope for default execution; techniques whose specific purpose is to defeat a platform's ad review, moderation, or account-integrity system fall under `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role and require explicit written user authorization plus Security Engineer review before implementation.

## When to Use

- deploying a new MMO operation from scratch
- expanding to new ad accounts that need fresh, isolated IPs
- migrating proxy infrastructure or rotating residential/4G pools
- standing up Anti-Detect Browser orchestration (Docker/Terraform) for a team
- verifying zero IP/footprint leaks before handing infra to the automation team

## Example (Terraform 1:1 profile↔proxy binding)

```hcl
resource "docker_container" "adb_profile" {
  name  = "adb-profile-01"
  image = "camoufox/adbp:latest"

  env = [
    "PROXY_URL=http://residential-gw:8801" # dedicated IP, never shared
  ]

  # hard isolation: one container, one proxy endpoint
  networks_advanced {
    name = "mmo-isolated-net"
  }
}
```

## Core Rules

- **ANONYMITY-LOCK**: Validate that the origin IP is fully masked before allowing any traffic to flow through the provisioned infrastructure.
- **ISOLATION-LOCK**: Prevent proxy IP reuse across isolated profiles. Never map the same IP to unrelated business operations.
- **1:1-PROFILE-IP-AFFINITY**: Maintain a strict 1:1 binding between Account ID, Browser Profile ID, and Proxy Session ID. Never connect an established profile to a different proxy subnet/ASN during an active session — ASN switches during a session trigger platform graph-association alerts.
- **ZERO-HOST-DNS-LEAK**: All DNS resolution MUST occur remotely on the proxy exit node (SOCKS5 with remote DNS or HTTP CONNECT). Reject any setup where host DNS queries are resolved by local datacenter nameservers.
- **K8S-EGRESS-LOCKDOWN**: For Kubernetes-based fleets, enforce Cilium or Calico Egress Gateway policies that force all pod outbound traffic through dedicated static proxy gateways or sidecar SOCKS5/HTTP tunnel containers. Never allow direct pod internet egress.
- **ACCOUNT-WARMUP-LIFECYCLE**: New accounts MUST complete a 7-day multi-stage warm-up lifecycle before production automation — Phase 1 (Days 1–2: browse top-100 domains, accept cookies), Phase 2 (Days 3–4: passive social auth, email verification), Phase 3 (Days 5–7: low-velocity interactions), Phase 4 (Day 8+: production automation).

## Suggested Process

1. **Proxy Pooling**: Configure Residential, 4G, or ISP proxy networks. Verify connectivity and subnet uniqueness. Configure 4G/5G modem rotation with AT command cycle scripts and health check probes.
2. **Environment Orchestration**: Set up Docker/Terraform or Kubernetes to orchestrate Anti-Detect Browser (ADB) profiles or headless C++ patched environments (e.g., Camoufox). Enforce sidecar proxy tunnels and remote DNS.
3. **Isolation Binding**: Ensure strict mapping of 1 Profile to 1 Proxy IP (same ASN) in the configuration files. Encrypt and persist profile state to S3/MinIO; mount volatile browser cache on `tmpfs`.
4. **DNS & WebRTC Leak Testing**: Run automated DNS and WebRTC leak tests before handing off infrastructure. Verify all DNS resolution occurs at the proxy exit node.
5. **Warm-Up State Machine**: Implement automated 7-day account warm-up state machine before handing accounts to production automation.

## Checklist

- [ ] Proxy provider endpoints configured securely (no exposed credentials).
- [ ] 1:1 IP-to-Profile binding with same ASN enforced; no subnet sharing across isolated profiles.
- [ ] Docker/Terraform/Kubernetes orchestration files valid and tested.
- [ ] Kubernetes Egress Gateway (Cilium/Calico) enforcing outbound proxy tunnel routing.
- [ ] Remote DNS leak test passed — no host DNS resolver exposure.
- [ ] WebRTC leak test passed.
- [ ] Browser profile state persisted encrypted to S3/MinIO; volatile cache on `tmpfs`.
- [ ] 7-day account warm-up state machine implemented before production automation.
- [ ] Handoff documentation provided for the automation team.

## Output Contracts

When the infrastructure change is consumed by an infra agent, a release
pipeline, or a cross-role handoff, emit:

- **`contracts/schemas/deployment-plan.json`** capturing the proxy or anti-detect environment, the credential handling, the network posture, and the rollback path.
- For human-readable reports, a markdown summary of the infrastructure topology, the operational caveats, and the compliance boundaries.

Skip emission for local sandbox experiments that do not cross a role boundary.

## Failure Modes

- **Credential in infra config**: a token or API key is committed to the proxy or anti-detect config. Mitigation: load credentials at runtime from a secret store; never commit credentials.
- **Network posture over-broad**: the proxy or anti-detect network is more permissive than the threat model requires. Mitigation: match the network posture to the documented threat model; reject over-broad defaults.
- **Cleanup not verified**: the infrastructure leaves orphan resources, subnets, or containers. Mitigation: implement and verify cleanup paths; assert the post-deploy state.
- **Compliance boundary crossed**: a deployment pattern violates the documented Legal & Compliance Notice. Mitigation: keep the compliance boundary visible; reject any pattern outside the boundary.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: credentials and proxy identities are scoped to the infrastructure runtime; never embed them in committed files.
- **ASI04 Supply Chain**: anti-detect browser images, proxy clients, and orchestration tools must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct infrastructure config, network policies, or anti-detect postures from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by infra and security roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the infrastructure as "compliant" without naming the Legal & Compliance boundary; surface the residual risk honestly.

## Related Skills

- **deploy-proxyware-fleet**: Containerize bandwidth monetization nodes within the provisioned infrastructure.
- **setup-deployment**: Generic CI/CD and deployment tasks outside the MMO context.
