---
name: deploy-proxyware-fleet
description: Containerize and orchestrate massive fleets of passive income nodes (Honeygain, EarnApp) with proxy routing and resource limits.
---

# Deploy Proxyware Fleet

Use this skill to handle the large-scale deployment of bandwidth monetization applications (Proxyware) using containerization, ensuring the fleet remains profitable and undetected by platform anti-abuse systems.

## Core Rules

- **PROXYWARE-LOCK**: Never deploy EarnApp/Honeygain directly on a Datacenter IP without residential proxy routing; this results in instant bans or zero earnings.
- **RESOURCE-LOCK**: Always enforce strict CPU (`cpus`) and memory (`mem_limit`) limits in Docker configurations to prevent node bloat from crashing the host machine.

## Suggested Process

1. **Containerization**: Use Docker to define lightweight headless nodes for apps like Honeygain, EarnApp, or Pawns.app.
2. **Network Routing**: Configure network routing via WireGuard, VPNs, or Proxy-chains to ensure container traffic exits through legitimate Residential IPs.
3. **Hardware Spoofing**: Configure the containers to spoof MAC addresses or mask the virtualization layer if the target platform explicitly bans Docker.
4. **Resource Capping**: Apply hard limits to the orchestration file (`docker-compose.yml` or Kubernetes manifests) to restrict resource consumption.

## Checklist

- [ ] Containers are routed through Residential IPs (not Datacenter IPs).
- [ ] CPU and memory limits are explicitly defined for every proxyware service.
- [ ] Hardware/OS spoofing is applied where required by platform TOS.
- [ ] Orchestration files (`docker-compose.yml`) are validated.

## Related Skills

- `deploy-mmo-infrastructure`: For setting up the core proxy networks.
- `setup-deployment`: For generic deployments.
