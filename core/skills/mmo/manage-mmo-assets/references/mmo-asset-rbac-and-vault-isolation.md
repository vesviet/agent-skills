# MMO Asset RBAC & Vault Isolation Specifications (2026)

## 1. Silo Compartmentalization Architecture

Cascading platform bans ("chết chùm") propagate along graph edges linking ad accounts: shared payment methods, identical ASN subnets, common admin users, or co-located pixel IDs. Strict silo compartmentalization eliminates these graph linkages:

```
┌────────────────────────────────────────────────────────┐
│                      SILO ALPHA                        │
│  - ASN: AS15169 (Residential ISP Pool 1)               │
│  - VCC: BIN 424242 (Stripe Issuing Account A)          │
│  - Admin: Via Identity Alpha (TOTP Seed Alpha)         │
│  - Vault Path: secret/mmo/silos/alpha                  │
└────────────────────────────────────────────────────────┘
                           ▲
             STRICT GRAPH PARTITION (Zero Overlap)
                           ▼
┌────────────────────────────────────────────────────────┐
│                      SILO BETA                         │
│  - ASN: AS7018 (4G Mobile Pool 2)                      │
│  - VCC: BIN 532959 (Airwallex Account B)               │
│  - Admin: Via Identity Beta (TOTP Seed Beta)           │
│  - Vault Path: secret/mmo/silos/beta                   │
└────────────────────────────────────────────────────────┘
```

## 2. Programmatic RFC 6238 TOTP Integration

- Store raw base32 TOTP secret seeds exclusively within HashiCorp Vault / AWS Secrets Manager.
- Generate dynamic 6-digit verification tokens on-demand during login workflows.
- Clock drift tolerance: allow $\pm 1$ time-step window ($30\text{s}$) to avoid authentication rejections due to server NTP offsets.

## 3. Virtual Commercial Card (VCC) & BIN Diversity

- **1:1 Binding**: Exactly one virtual commercial card per advertising account.
- **BIN Diversity**: Sourcing VCCs across multiple financial institutions (Stripe, Airwallex, Privacy) ensures that a fraud flag on one card issuer's BIN does not freeze accounts across other silos.
- **Velocity Controls**: Enforce daily and monthly spending caps at the card level.
- **Immediate Quarantine**: If a card payment fails or triggers an ad account review, that VCC is immediately quarantined and retired. Never reassign a flagged card to a clean account.
