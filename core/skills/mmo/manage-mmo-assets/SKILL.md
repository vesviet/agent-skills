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
- **ASN-SILO-ISOLATION**: Each silo MUST use proxy pools from distinct ASNs (not just different IPs from the same residential network provider). Platform graph-association algorithms correlate accounts sharing the same ASN pool — distinct ASNs reduce cascading ban blast radius.
- **EXPONENTIAL-BACKOFF-RATE-LIMIT**: All automation against ad platform APIs MUST implement adaptive rate limiting with Poisson-distributed delays and immediate throttling upon HTTP 429, 503, or platform-specific checkpoint challenges. Never use fixed-interval polling.
- **BAN-BLAST-RADIUS-AUDIT**: After any account restriction, audit the full connection graph (shared BMs, pixels, domains, admin accounts) before re-activating any assets in the same silo. Activate clean assets only after confirming zero graph overlap.

## Suggested Process

1. **Asset Inventorying**: Catalog all Vias, Business Managers (BMs), Ad Accounts, Meta Datasets (Pixels), and Domains into a secure tracking system with ASN assignments per silo.
2. **Team Sharing Setup**: Configure cloud-based Anti-Detect Browser (ADB) profiles to share access via Role-Based Access Control (RBAC) rather than distributing raw passwords or cookies.
3. **Compartmentalization Mapping**: Architect the connection map to ensure a ban on one asset does not cascade to others. Ensure no overlap of backup admins, IPs, or ASNs across isolated silos.
4. **Adaptive Rate Limiting**: Implement Poisson-distributed delay profiles for all platform API interactions; detect and respond to checkpoint challenges before proceeding.

## Checklist

- [ ] All assets cataloged and access governed by RBAC.
- [ ] No raw passwords or cookies transmitted via insecure channels.
- [ ] Silos use distinct ASNs for proxy pools — not just different IPs from the same ASN.
- [ ] Isolation mapping confirms zero IP, ASN, or admin overlap between restricted and clean assets.
- [ ] Backup assets (Vias/BMs) kept cleanly separated from any restricted assets.
- [ ] Exponential backoff with Poisson-distributed delays implemented for platform API calls.
- [ ] Post-restriction ban blast-radius audit completed before reactivating any silo assets.
- [ ] Asset catalog up to date (no stale/orphaned entries).
- [ ] Recovery plan documented in case of cascading ban event.

## Output Contracts

When the asset handoff is consumed by a fleet operator, a release
pipeline, or a cross-role handoff, emit:

- **`contracts/schemas/deployment-plan.json`** capturing the asset id, the destination, the credential handling, the rotation status, and the rollback path.
- For human-readable reports, a markdown summary of the asset inventory, the rotation cadence, and the compliance boundaries.

Skip emission for local asset lookups that do not cross a role boundary.

## Failure Modes

- **Credential in asset export**: a token or account credential is committed to the export. Mitigation: load credentials at runtime from a secret store; never commit credentials.
- **Asset rotation missed**: a Business Manager or account past its rotation cadence is still in use. Mitigation: enforce the rotation schedule; reject assets past their cadence.
- **Asset handover not verified**: the receiving agent cannot read the new asset. Mitigation: verify the receiving agent's read access before treating the handover as complete.
- **Compliance boundary crossed**: an asset handling pattern violates the documented Legal & Compliance Notice. Mitigation: keep the compliance boundary visible; reject any pattern outside the boundary.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: account credentials and Business Manager access are scoped to the asset's owner; never embed them in committed files.
- **ASI04 Supply Chain**: asset sharing tools and rotation services must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct asset handoff payloads, rotation commands, or handover scripts from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by infra and security roles; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present the asset inventory as "compliant" without naming the Legal & Compliance boundary; surface the residual risk honestly.

## Related Skills

- **deploy-mmo-infrastructure**: Set up the ADB environments for asset access.
- **setup-tracking-system**: Configure tracking assets (Pixels/Datasets) referenced in the catalog.
