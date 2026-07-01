---
name: deploy-mmo-infrastructure
description: Deploy and manage proxy pools (Residential/4G) and Anti-Detect Browser orchestration environments (via Docker/Terraform) ensuring zero IP/footprint leaks. Use when deploying a new MMO operation, expanding to new ad accounts, or migrating proxy infrastructure.
---

# Deploy MMO Infrastructure

Use this skill to provision highly anonymous, isolated infrastructure required for Make Money Online (MMO) operations, preventing tracking, fingerprinting, and cascading bans.

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
