---
name: deploy-mmo-infrastructure
description: Deploy and manage proxy pools (Residential/4G) and Anti-Detect Browser orchestration environments (via Docker/Terraform) ensuring zero IP/footprint leaks. Use when deploying a new MMO operation, expanding to new ad accounts, or migrating proxy infrastructure.
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

## Suggested Process

1. **Proxy Pooling**: Configure Residential, 4G, or ISP proxy networks. Verify connectivity and subnet uniqueness.
2. **Environment Orchestration**: Set up Docker/Terraform to orchestrate Anti-Detect Browser (ADB) profiles or headless C++ patched environments (e.g., Camoufox).
3. **Isolation Binding**: Ensure strict mapping of 1 Profile to 1 Proxy IP in the configuration files.
4. **Leak Testing**: Run a simulated connection to check for DNS leaks or WebRTC exposure before handing off the infrastructure.

## Checklist

- [ ] Proxy provider endpoints are configured securely (no exposed credentials).
- [ ] Isolation mapping (1:1 IP to Profile) is explicitly defined in configurations.
- [ ] Docker/Terraform orchestration files are syntactically valid and tested.
- [ ] Leak test has been performed (DNS and WebRTC leaks checked).
- [ ] Subnet uniqueness is verified — no shared subnets across isolated profiles.
- [ ] Handoff documentation provided for the automation team.

## Related Skills

- **deploy-proxyware-fleet**: Containerize bandwidth monetization nodes within the provisioned infrastructure.
- **setup-deployment**: Generic CI/CD and deployment tasks outside the MMO context.
