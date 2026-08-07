---
name: deploy-proxyware-fleet
description: Containerize and orchestrate massive fleets of passive income nodes (Honeygain, EarnApp, Pawns.app) with proxy routing and resource limits. Use when scaling bandwidth monetization nodes, migrating from datacenter to residential routing, or expanding an existing fleet.
---

# Deploy Proxyware Fleet

Use this skill to handle the large-scale deployment of bandwidth monetization applications (Proxyware) using containerization, ensuring the fleet remains profitable and resilient to platform-side node cleanup.

## Legal & Compliance Notice

Bandwidth-sharing apps (Honeygain, EarnApp, Pawns.app) prohibit multi-accounting, VM/container deployment, and IP misrepresentation in their Terms of Service — running a containerized fleet at scale is very likely a ToS violation even when technically functional, and can result in account termination or forfeited earnings with no recourse. This skill documents the technical mechanics only; it does not establish that a given deployment is authorized by the target platform. Confirm the user has read and accepts the specific platform's ToS before implementing, and treat any "spoofing" or "evasion" step as in scope for `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role (explicit written authorization + Security Engineer review) rather than default-approved automation.

## When to Use

- scaling Honeygain / EarnApp / Pawns.app nodes beyond a single host
- migrating nodes from datacenter IPs to residential routing
- adding a new proxyware app to an existing fleet
- capping resource consumption to protect the host from node bloat
- recording an earnings baseline before/after a fleet change for ROI

## Example (docker-compose with residential routing + resource caps)

```yaml
services:
  earnapp:
    image: proxyware/earnapp:latest
    network_mode: "container:vpn-gateway" # exit via residential VPN, never DC IP
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 256M
  honeygain:
    image: proxyware/honeygain:latest
    network_mode: "container:vpn-gateway"
    deploy:
      resources:
        limits:
          cpus: "0.50"
          memory: 256M
```

## Core Rules

- **PROXYWARE-LOCK**: Never deploy EarnApp/Honeygain directly on a Datacenter IP without residential proxy routing; this results in instant bans or zero earnings.
- **RESOURCE-LOCK**: Always enforce strict CPU (`cpus`) and memory (`mem_limit`) limits in Docker configurations to prevent node bloat from crashing the host machine.

## Suggested Process

1. **Containerization**: Use Docker to define lightweight headless nodes for apps like Honeygain, EarnApp, or Pawns.app.
2. **Network Routing**: Configure network routing via WireGuard, VPNs, or Proxy-chains to ensure container traffic exits through legitimate Residential IPs.
3. **Hardware/OS Fingerprint Normalization**: If the target platform's ToS permits container deployment but flags a config purely for looking virtualized, normalize the hardware/OS fingerprint reported by the container. If the platform's ToS or anti-abuse system explicitly targets and bans this technique, treat it as a `REVIEW-SYSTEM LOCK` case — escalate to the user and Security Engineer before implementing rather than deploying it as default behavior.
4. **Resource Capping**: Apply hard limits to the orchestration file (`docker-compose.yml` or Kubernetes manifests) to restrict resource consumption.

## Checklist

- [ ] Containers are routed through Residential IPs (not Datacenter IPs).
- [ ] CPU and memory limits are explicitly defined for every proxyware service.
- [ ] Hardware/OS spoofing is applied where required by platform detection.
- [ ] Orchestration files (`docker-compose.yml`) are validated.
- [ ] Network routing (WireGuard/VPN/proxy-chains) is tested end-to-end before scaling.
- [ ] Fleet earnings baseline recorded before and after deployment for ROI validation.

## Related Skills

- **deploy-mmo-infrastructure**: Set up the core proxy networks the fleet will route through.
- **setup-deployment**: Generic deployments for non-MMO infrastructure.
