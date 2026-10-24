---
description: End-to-end 5-phase MMO growth campaign lifecycle — Offer Research, Landing/Content Engineering, Cookieless S2S Tracking, Traffic Acquisition, and ROI Optimization.
---

## MMO Campaign Lifecycle Workflow

Use this workflow to plan, launch, attribute, and scale Make Money Online (MMO) growth campaigns across affiliate networks, programmatic SEO, paid media, and bandwidth monetization.

### Prerequisites
- Target affiliate network / offer vertical identified (e-commerce, SaaS, lead gen, DePIN).
- Operating domain portfolio, DNS management, and CDN/edge routing (Cloudflare) configured.
- Anti-Detect Browser (ADB) environment initialized with verified residential/ISP/mobile proxy pools.
- Ad platform developer accounts (Meta Business Manager, TikTok Business Center, Google Ads) isolated via RBAC.
- Spend limits and API token usage hard caps established in accordance with BUDGET-LOCK.

### Workflow Steps

#### 1. Offer Research & Intelligence
Role: **MMO Engineer**, **Researcher**

Use skill: `conduct-research`

- Execute deep offer intelligence across target networks (Amazon, TikTok Shop, Shopee/Lazada Open Platform, CJ, Impact).
- Benchmark Earnings Per Click (EPC), Average Order Value (AOV), refund/chargeback charge rates, and affiliate payout tiers.
- Analyze top-performing competitor landing pages, creative angles, and target search queries.
- Evaluate platform compliance boundaries; verify offer terms do not require disallowed deceptive cloaking.
- Output: Synthesize offer economics into `reports/research/mmo-offer-dossier.json` and draft `contracts/schemas/mmo-campaign-spec.json`.

#### 2. Landing Page & Content Engineering
Role: **MMO Engineer**, **Content Writer**

Use skill: `generate-mmo-content`
Use skill: `write-article`

- Generate programmatic SEO (pSEO) landing pages utilizing Answer-First structure (BLUF ≤60 words) for search capture.
- Develop high-converting direct-response copywriting (AIDA / PAS frameworks) emphasizing value proposition and social proof.
- Author multimodal video hooks and scripts tailored for short-form video traffic arbitrage (TikTok, YouTube Shorts, Reels).
- Ensure zero AI-hallucinated product claims; embed schema markup (`Product`, `Review`, `FAQPage`) for generative search engine extraction.
- Output: Publish-ready landing pages and creative assets conforming to `contracts/schemas/content-handoff.json`.

#### 3. Cookieless S2S Tracking & Attribution Setup
Role: **MMO Engineer**

Use skill: `setup-tracking-system`

- Configure dual-layer attribution: client-side pixel backup paired with direct Server-to-Server (S2S) event transmission.
- Integrate modern conversion APIs: Meta CAPI v20+, TikTok Events API, and Google Enhanced Conversions.
- Enforce cryptographic deduplication by generating identical UUID v4 `event_id` parameters across client and server events.
- Deploy affiliate network postback webhooks with signature verification (HMAC-SHA256) and Click-to-Install Time (CTIT) fraud filtering.
- Verify end-to-end event firing using test payloads before committing any paid traffic budget.
- Output: Active tracking endpoints, validated postback URLs, and verification logs in `contracts/schemas/implementation-result.json`.

#### 4. Traffic Acquisition & Stealth Ad Launch
Role: **MMO Engineer**, **Security Engineer**

Use skill: `create-automation-script`
Use skill: `deploy-mmo-infrastructure`
Use skill: `manage-mmo-assets`

- Deploy isolated browser profiles using Chrome DevTools Protocol (CDP) over anti-detect browser platforms.
- Enforce WebGPU/Canvas fingerprint consistency, client audio noise injection, and TLS client hello (JA3/JA4) fingerprint alignment.
- Implement organic behavioral automation: humanized mouse splines, dynamic typing cadences, and random jitter to evade bot heuristics.
- Manage automated warmup state machines for ad accounts and dynamic residential proxy health probes.
- Safeguard credentials and payment assets: programmatically handle 2FA/TOTP tokens and enforce virtual card (VCC) isolation.
- Output: Executed campaign launch logs and infrastructure state in `contracts/schemas/implementation-result.json`.

#### 5. ROI Optimization, Attribution & Scaling
Role: **MMO Engineer**, **Data Analyst**

Use skill: `analyze-campaign-roi`
Use skill: `analyze-data`

- Calculate True ROI incorporating blended ad spend, residential proxy consumption costs, API tokens, and account die-rate depreciation.
- Measure Blended Return on Ad Spend (Blended ROAS = Total Revenue / Total Ad Spend) across all acquisition channels.
- Model multi-tier affiliate commission structures, delayed conversion payouts, and customer lifetime value (LTV).
- Enforce automated budget scaling rules: scale ad spend by 20% on winning ad sets exceeding target ROAS; immediately pause bleeders.
- Produce comprehensive financial analytics and executive performance reports.
- Output: Validated campaign performance report in `contracts/schemas/mmo-roi-report.json`.

### Checklist
- [ ] Offer EPC, AOV, and payout terms validated against affiliate network APIs
- [ ] Programmatic SEO landing page drafted with Answer-First BLUF (≤60 words)
- [ ] Direct-response copy and short-form video hooks reviewed against platform compliance
- [ ] Server-to-Server (S2S) tracking endpoints configured for Meta CAPI, TikTok Events API, and Google Enhanced Conversions
- [ ] UUID v4 event_id deduplication verified across client and server event payloads
- [ ] Postback webhook HMAC-SHA256 signature verification and CTIT fraud filtering enabled
- [ ] Anti-detect browser profiles verified for WebGPU, Canvas, and JA3/JA4 fingerprint consistency
- [ ] Residential proxy health checks and automated warmup state machine confirmed
- [ ] 2FA/TOTP programmatic token handling and VCC spending limits enforced
- [ ] True ROI, Blended ROAS, and die-rate amortized costs computed
- [ ] Automated budget scaling and bleeder-pause thresholds active

### Related Workflows
- [seo-content-lifecycle](seo-content-lifecycle.md) — Precursor workflow for organic topic clustering and SEO content development
- [content-publishing](content-publishing.md) — Production editorial pipeline for publishing review articles and advertorials
- [qa-validation](qa-validation.md) — Quality assurance protocol for landing page rendering and webhook reliability
- [security-incident-response](security-incident-response.md) — Incident response protocol for compromised ad accounts or rogue proxy routing

### Related Skills
- **setup-tracking-system**: Configure S2S postbacks, Meta CAPI, TikTok Events API, and Google Enhanced Conversions
- **create-automation-script**: Build CDP stealth automation scripts with WebGPU/Canvas fingerprint consistency
- **deploy-mmo-infrastructure**: Orchestrate dynamic proxy networks and automated warmup state machines
- **manage-mmo-assets**: Maintain isolated ad accounts, VCC payment allocations, and 2FA/TOTP credentials
- **deploy-proxyware-fleet**: Operate decentralized bandwidth monetization nodes (DePIN) with resource boundaries
- **generate-mmo-content**: Produce programmatic SEO landing pages, CRO advertorials, and video hooks
- **analyze-campaign-roi**: Calculate True ROI, Blended ROAS, customer LTV, and multi-tier payout models
- **conduct-research**: Investigate competitor ad creative intelligence and affiliate offer metrics
- **write-article**: Author long-form affiliate reviews and programmatic content
- **analyze-data**: Synthesize multi-channel attribution and ad spend datasets

### Failure Modes
- **Attribution Loss (Postback Failure)**: Affiliate network fails to fire postbacks due to URL encoding issues or network dropouts. **Mitigation:** Implement idempotent postback replay queues and local access log reconciliation.
- **Cascading Profile Ban ("Chết chùm")**: Cross-contamination of residential IPs or shared browser fingerprint hashes triggers mass suspension. **Mitigation:** Enforce strict 1:1:1 profile-to-IP-to-card isolation under ISOLATION-LOCK.
- **Budget Bleed**: Rogue automation script or unchecked campaign spends past profitability threshold during high-latency periods. **Mitigation:** Hardware API spend limits and automatic circuit-breaker pause scripts triggered under BUDGET-LOCK.

### Output Contracts
- **`contracts/schemas/mmo-campaign-spec.json`** — Formal campaign specification (target offer, tracking schema, budget caps, landing page parameters).
- **`contracts/schemas/mmo-roi-report.json`** — Comprehensive financial audit (Blended ROAS, True ROI, net margin, LTV projections, die-rate depreciation).

### Security Guardrails (OWASP ASI)
- **ASI01 Goal Hijack**: Automation script must not navigate to unauthorized ad networks or click unvetted affiliate links.
- **ASI03 Identity & Privilege Abuse**: Ad accounts and payment credentials must be accessed strictly via least-privilege RBAC; zero credential persistence in automation code.
- **ASI09 Human-Agent Trust Exploitation**: Campaign performance figures must report raw, unreconciled ad platform stats alongside verified bank postback settlements; no fabricated ROAS figures.
