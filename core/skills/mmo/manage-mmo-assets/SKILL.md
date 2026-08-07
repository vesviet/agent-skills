---
name: manage-mmo-assets
description: Manage and share MMO assets (Business Managers, Via, Pixels/Datasets, Anti-Detect profiles) using Role-Based Access Control (RBAC) while enforcing strict isolation to prevent cascading bans. Use when onboarding new ad accounts, sharing BMs with team members, auditing asset health, or recovering from a cascading ban incident.
---

# Manage MMO Assets

Use this skill to securely acquire, organize, and share marketing assets using RBAC-based access control and isolation practices intended to limit the blast radius of a single account restriction.

## Legal & Compliance Notice

Ad platforms (Meta, Google) prohibit circumventing their account, ownership, or verification policies — sharing Business Managers/Vias to route around a platform's identity or ownership checks, or maintaining "clean backup" assets specifically to survive a ban that would otherwise apply, can itself violate platform ToS regardless of the isolation hygiene used. This skill documents access-control and compartmentalization mechanics only. It does not authorize policy circumvention; any step that exists specifically to defeat a platform's account-integrity or ownership verification system falls under `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role and requires explicit written user authorization plus Security Engineer review before implementation.

## When to Use

- onboarding new ad accounts, Vias, or Business Managers (BMs)
- sharing assets with teammates via RBAC instead of raw cookies
- auditing asset health / IP overlap across silos
- compartmentalizing clean backups away from restricted assets
- responding to or recovering from a cascading ban ("chết chùm") incident

## Example (compartmentalization map)

```yaml
silos:
  - id: silo-a
    assets: [bm-101, via-22, adacct-7]
    proxy_subnet: 10.20.0.0/24
    admins: [ops-lead]
  - id: silo-b
    assets: [bm-102, via-23, adacct-8]
    proxy_subnet: 10.30.0.0/24   # no IP/admin overlap with silo-a
    admins: [growth-lead]
```

## Core Rules

- **ISOLATION-LOCK**: Never share the same residential proxy IP across unrelated ad accounts or profiles.
- **ASSET-LOCK**: Do not connect clean backup assets (Vias/BMs) to currently restricted or flagged assets until the restriction is fully lifted.

## Suggested Process

1. **Asset Inventorying**: Catalog all Vias, Business Managers (BMs), Ad Accounts, Meta Datasets (Pixels), and Domains into a secure tracking system.
2. **Team Sharing Setup**: Configure cloud-based Anti-Detect Browser (ADB) profiles to share access via Role-Based Access Control (RBAC) rather than distributing raw passwords or cookies.
3. **Compartmentalization Mapping**: Architect the connection map to ensure that a ban on one asset (e.g., one BM) does not cascade to others. Ensure no overlap of backup admins or IPs across isolated silos.

## Checklist

- [ ] All assets are cataloged and access is strictly governed by RBAC.
- [ ] No raw passwords or cookies are transmitted via insecure channels.
- [ ] Isolation mapping confirms zero IP or admin overlap between restricted and clean assets.
- [ ] Backup assets (Vias/BMs) are kept cleanly separated from any restricted assets.
- [ ] Asset catalog is up to date (no stale/orphaned entries).
- [ ] Recovery plan documented in case of cascading ban event.

## Related Skills

- **deploy-mmo-infrastructure**: Set up the ADB environments for asset access.
- **setup-tracking-system**: Configure tracking assets (Pixels/Datasets) referenced in the catalog.
