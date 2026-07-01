---
name: manage-mmo-assets
description: Manage and share MMO assets (Business Managers, Via, Pixels/Datasets, Anti-Detect profiles) using Role-Based Access Control (RBAC) while enforcing strict isolation to prevent cascading bans.
---

# Manage MMO Assets

Use this skill to securely acquire, organize, and share valuable marketing assets without triggering platform security algorithms or risking entire network closures ("chết chùm").

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

## Related Skills

- `deploy-mmo-infrastructure`: For setting up the ADB environments.
- `setup-tracking-system`: For configuring the tracking assets (Pixels/Datasets).
