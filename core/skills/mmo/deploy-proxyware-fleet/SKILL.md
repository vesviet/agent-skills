---
name: deploy-proxyware-fleet
description: Containerize and orchestrate massive fleets of passive income nodes (Honeygain, EarnApp, Pawns.app) with proxy routing and resource limits. Use when scaling bandwidth monetization nodes, migrating from datacenter to residential routing, or expanding an existing fleet.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
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
- **CONTAINER-EPHEMERAL-DISKS**: Container root filesystems MUST be mounted read-only (`readOnlyRootFilesystem: true`) with volatile browser cache placed on `tmpfs` mounts (`/tmp` and `/dev/shm`, minimum 2 GiB for Chromium/browser stability). Sync only required cookie/storage data to persistent encrypted stores.
- **REMOTE-DNS-LOCK**: All DNS resolution MUST occur on the proxy exit node via SOCKS5 remote DNS or HTTP CONNECT. Never resolve DNS through the host's local resolver — this leaks the datacenter identity behind the residential proxy.

## Suggested Process

1. **Containerization**: Use Docker to define lightweight headless nodes for apps like Honeygain, EarnApp, or Pawns.app with read-only root filesystems and tmpfs volumes.
2. **Network Routing**: Configure network routing via WireGuard, VPNs, or Proxy-chains to ensure container traffic exits through legitimate Residential IPs. Verify remote DNS is enforced.
3. **Hardware/OS Fingerprint Normalization**: If the target platform's ToS permits container deployment but flags a config purely for looking virtualized, normalize the hardware/OS fingerprint reported by the container. If the platform's ToS or anti-abuse system explicitly targets and bans this technique, treat it as a `REVIEW-SYSTEM LOCK` case — escalate to the user and Security Engineer before implementing rather than deploying it as default behavior.
4. **Resource Capping**: Apply hard limits to the orchestration file (`docker-compose.yml` or Kubernetes manifests). Set cgroup CPU and memory quotas to prevent Chromium rendering memory leaks triggering oom-killer.

## Checklist

- [ ] Containers routed through Residential IPs (not Datacenter IPs).
- [ ] CPU and memory limits explicitly defined for every proxyware service.
- [ ] Container root filesystem mounted read-only (`readOnlyRootFilesystem: true`).
- [ ] `tmpfs` mounts configured for `/tmp` and `/dev/shm` (minimum 2 GiB).
- [ ] Remote DNS enforced via proxy exit node — no host resolver leaks.
- [ ] Hardware/OS spoofing applied where required by platform detection.
- [ ] Orchestration files (`docker-compose.yml`) validated.
- [ ] Network routing (WireGuard/VPN/proxy-chains) tested end-to-end before scaling.
- [ ] Fleet earnings baseline recorded before and after deployment for ROI validation.

## Output Contracts

When the proxyware fleet is consumed by an infra agent, a release
pipeline, or a cross-role handoff, emit:

- **`contracts/schemas/deployment-plan.json`** capturing the fleet size, the node distribution, the credential handling, the network posture, and the rollback path.
- For human-readable reports, a markdown summary of the fleet topology, the operational caveats, and the compliance boundaries.

Skip emission for local sandbox experiments that do not cross a role boundary.

## Failure Modes

- **Credential in fleet config**: a token or API key is committed to the fleet config. Mitigation: load credentials at runtime from a secret store; never commit credentials.
- **Fleet size exceeds threat model**: more nodes are deployed than the threat model requires. Mitigation: size the fleet to the documented workload; reject over-broad defaults.
- **Node cleanup not verified**: the fleet leaves orphan nodes or containers. Mitigation: implement and verify cleanup paths; assert the post-deploy state.
- **Compliance boundary crossed**: a deployment pattern violates the documented Legal & Compliance Notice. Mitigation: keep the compliance boundary visible; reject any pattern outside the boundary.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: node credentials are scoped to the fleet runtime; never embed them in committed files.
- **ASI04 Supply Chain**: proxyware images and orchestration tools must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct fleet config, network policies, or node distributions from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by infra and security roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the fleet as "compliant" without naming the Legal & Compliance boundary; surface the residual risk honestly.

## Related Skills

- **deploy-mmo-infrastructure**: Set up the core proxy networks the fleet will route through.
- **setup-deployment**: Generic deployments for non-MMO infrastructure.
