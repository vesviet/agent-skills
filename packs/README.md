# Packs

Packs describe how to assemble the portable core with zero or more overlays for a target team. Each pack has a `manifest.yaml` that declares which `core` and `overlays/` to include, along with 2026 governance metadata.

## Available Packs (17)

| Pack | Manifest | Composition | Capabilities |
|------|----------|-------------|-------------|
| `global-engineering` | [manifest.yaml](global-engineering/manifest.yaml) | `core` only | All general engineering |
| `hugo-authority-team` | [manifest.yaml](hugo-authority-team/manifest.yaml) | `core` + `overlays/hugo-authority-content` | v5.0.0 · Twin Hugo architecture (authority & learn Hugo sites), 100-Round Deep Research Protocol, 4-Role Swarm pipeline (@content-writer, @content-manager, @technical-writer, @seo-analyst), 10 Anchor Pillar Hubs, one-way authority flow |
| `real-estate-team` | [manifest.yaml](real-estate-team/manifest.yaml) | `core` + `overlays/real-estate-content` + `overlays/seo-publishing` | v5.0.0 · Expat housing & rental legal authority (real-estate rental portal), 5-Pillar Content Framework, <AnswerFirst> component (100% coverage across 463 posts), 61 luxury property portfolios, 98 E-E-A-T author personas, 8 empirical AEO upgrade batches |
| `hvac-content-team` | [manifest.yaml](hvac-content-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/hvac-authority-content` + `overlays/seo-publishing` | v5.0.0 · Vietnam HVAC engineering knowledge & empirical review portal, TCVN 7830:2021 CSPF & ASHRAE 55-2023 comfort metrics, Hioki 3334 / RION NL-52 empirical testbeds, 7-category strict Silo link topology, 72 HVAC product entities |
| `laravel-ecommerce-team` | [manifest.yaml](laravel-ecommerce-team/manifest.yaml) | `core` + `overlays/laravel-filament` + `overlays/laravel-ecommerce` | Laravel 13, Filament v4, PHP 8.4 |
| `b2b-catalog-team` | [manifest.yaml](b2b-catalog-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/b2b-factory-catalog` | Astro v6+, Cloudflare Workers |
| `obj-team` | [manifest.yaml](obj-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/obj-configurator` | Astro, R3F v9, WebGPU |
| `b2b-golf-team` | [manifest.yaml](b2b-golf-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/b2b-catalog-golf` | Astro v6+, Cloudflare, SEO |
| `b2b-sport-team` | [manifest.yaml](b2b-sport-team/manifest.yaml) | `core` + `overlays/astro-cloudflare` + `overlays/b2b-sport-catalog` | Astro v6+, Cloudflare, SEO |
| `ecommerce-team` | [manifest.yaml](ecommerce-team/manifest.yaml) | `core` + `overlays/go-microservices` + `overlays/ecommerce-microservices` | Go 1.25, Kratos v3, ConnectRPC |
| `data-analyst-team` | [manifest.yaml](data-analyst-team/manifest.yaml) | `core` + `overlays/data-analyst-stack` | DuckDB, dbt 1.9, Iceberg, Metabase |
| `content-sprint-team` | [manifest.yaml](content-sprint-team/manifest.yaml) | `core` + `overlays/seo-publishing` | GEO/AEO, AI Overviews, publishing cadence |
| `livestream-team` | [manifest.yaml](livestream-team/manifest.yaml) | `core` + `overlays/livestream-web` | Frontend, UX, livestream, PWA |
| `data-warehouse` | [manifest.yaml](data-warehouse/manifest.yaml) | `core` + `overlays/data-warehouse` (incl. `learning/` track) | Fullstack data warehouse, FastAPI microservices, DuckDB single-writer, Medallion Parquet, MISA AMIS VAS 14, blind recount, PII masking, 4-layer testing, dbt 1.9/Iceberg/Kafka learning track |
| `mmo-growth-team` | [manifest.yaml](mmo-growth-team/manifest.yaml) | `core` only | v5.0.0 · Full-spectrum MMO growth engineering (AI Affiliate, multi-channel S2S tracking, stealth CDP automation, 5-phase campaign lifecycle, LTV & Blended ROAS economics) |
| `landing-pages-team` | [manifest.yaml](landing-pages-team/manifest.yaml) | `core` + `overlays/go-microservices` + `overlays/ui-design-system` + `overlays/seo-publishing` | v5.0.0 · High-converting single-product landing page engine & SaaS, Cloudflare Workers Edge SSR (< 25ms TTFB), Go Kratos v2 Clean Architecture, 5 CRO templates, 2D Footwear & Apparel Matrix, VietQR Napas 247, Zalo/Messenger widgets |
| `affiliate-cashback-team` | [manifest.yaml](affiliate-cashback-team/manifest.yaml) | `core` + `overlays/seo-publishing` + `overlays/ui-design-system` | v5.0.0 · Tri-Engine Affiliate & Cashback Growth Engineering Pack for CashbackHub ecosystem (`deal-bot-dispatcher`, `cashback-api-gateway`, `cashback-pwa-web`, `pseo-nextjs-engine`), 5 VAS Financial Invariants (1010–5010), T+1 Reconciliation, curl_cffi Chrome 124+ Anti-WAF, 1-1 Chatbot PWA, Next.js 15 ISR |


### Pack Spotlight: hugo-authority-team (v5.0.0)

The `hugo-authority-team` pack orchestrates high-authority content engineering and technical publishing across the twin Hugo sites:

- **Twin Hugo Architecture**: Dual-site publishing model pairing flagship English evergreen engineering authority with Vietnamese research and deep-dive laboratory.
- **One-Way Authority Flow**: Strict `learn` &rarr; authority linking topology with zero reverse links, independent self-referential canonical URLs, and mandatory &ge;25% Information Gain over top-ranking SERP results.
- **100-Round Deep Research Protocol**: Strict 5 clusters &times; 20 rounds of primary-source investigation required before drafting or upgrading any article, producing structured research dossiers (`reports/research/{slug}-dossier.json` and markdown notes).
- **4-Role Swarm Pipeline**: End-to-end multi-agent workflow:
  - `@content-writer`: Technical drafting satisfying the 7 Technical Content Gates (Answer-First BLUF &le;60w, runnable code, quantitative density &ge;3 data points/500w, valid Mermaid diagrams, post-mortems, trade-off framing, verifiable citations).
  - `@content-manager`: Editorial audit evaluating narrative structure, brand voice, Information Gain (&ge;75/100), and E-E-A-T credibility.
  - `@technical-writer`: Technical validity audit verifying version-pinned runnable code, benchmark testbed reproducibility, and configuration artifacts.
  - `@seo-analyst`: SEO, GEO/AEO, and topology audit enforcing Answer-First blocks, one-way link rules, 10 Anchor Pillar Hub connectivity, and Schema.org JSON-LD graph metadata.
- **10 Anchor Pillar Hubs**: Structural backbone (Raft consensus, Kubernetes platform engineering, Go concurrency, eBPF Linux observability, Kafka event streaming, LSM-tree storage, zero-trust service mesh, database internals, SRE chaos engineering, AI agent infrastructure) enforcing a zero-orphan content policy.

### Pack Spotlight: real-estate-team (v5.0.0)

The `real-estate-team` pack governs content engineering, legal compliance, and AI search visibility for real estate and rental portals:

- **5-Pillar Content Framework**: Systematic partition into Intelligence (market data & yield curves), Information (Housing Law 2023 & bilingual lease compliance), Insights (unbiased compound reviews), Neighborhoods (micro-district livability audits), and Integration (cultural & utility onboarding).
- **2026/2027 GEO/AEO Standards**: Mandatory `<AnswerFirst>` callout component (&le;60 words, &ge;3 numerical data points) implemented across 100% of the 463-post corpus; anti-slop gating eliminating generic marketing prose.
- **Property-Post Entity Link Equity**: Bidirectional interconnectivity weaving 61 luxury property portfolios (`src/data/property/`) with 463 editorial guides, enforcing a zero-orphan structural policy.
- **98-Persona E-E-A-T Registry**: Author verification across 5 professional disciplines (Senior Property Attorneys, Tax CPAs, Expat Relocation Directors, Civil Engineers, and Market Analysts).
- **8-Batch Empirical AEO Upgrade Discipline**: Continuous lifecycle refactoring existing content into Masterclass grade with structured comparison tables, bilingual landlord scripts, and validated legal citations.

### Pack Spotlight: hvac-content-team (v5.0.0)

The `hvac-content-team` pack orchestrates empirical HVAC technical publishing and edge product evaluation:

- **HVAC Engineering Standards**: Grounded in thermodynamic physics: **TCVN 7830:2021** CSPF seasonal cooling efficiency metrics and **ASHRAE Standard 55-2023** thermal comfort zones (PMV/PPD metrics, occupied air velocity $0.15 - 0.25\text{ m/s}$, humidity control $45\% - 60\% RH$).
- **Hardware-Verified Empirical Instrumentation**: All product evaluations cite testbed measurements from the Ho Chi Minh City lab using **Hioki 3334** AC/DC Power Analyzers (power curve & inverter modulation) and **RION NL-52** Sound Level Meters (1-meter calibrated dBA acoustic readings).
- **7-Category Strict Silo Link Topology**: Strict silo isolation across 300 articles (`gia-ca`, `huong-dan`, `kien-thuc`, `kinh-nghiem`, `mua-sam`, `review`, `so-sanh`) eliminating topical dilution; cross-silo linkage allowed only via 72 HVAC Product Entities (`src/data/product/`).
- **Rich Schema & AI Overview Snippets**: Comprehensive Schema.org graphs (`Product`, `Review`, `HowTo`, `FAQPage`) paired with `<AnswerFirst>` blocks tailored for Google AI Overviews, Perplexity, and ChatGPT Search.
- **Astro v5 + Cloudflare Pages Edge Engine**: Microsecond edge delivery with 100/100 Core Web Vitals, automated vacuum pump verification checklists, and PCB diagnostic guides.

### Pack Spotlight: mmo-growth-team (v5.0.0)

The `mmo-growth-team` pack orchestrates full-spectrum growth engineering, programmatic traffic arbitrage, and privacy-first server-side attribution for Make Money Online (MMO) operations:

- **Full-Spectrum Growth Engineering**: Pivots from legacy proxyware/farming to advanced AI-native affiliate engines, programmatic SEO (pSEO), dynamic product feeds, and multimodal video hooks.
- **Multi-Channel Cookieless S2S Tracking**: Direct server-to-server integration with Meta Conversions API (CAPI v20+), TikTok Events API, Google Enhanced Conversions, and iOS 18+ AdAttributionKit with cryptographic UUID v4 deduplication and CTIT fraud filtering.
- **2026/2027 Stealth CDP Automation**: Next-generation anti-detect browser orchestration over Chrome DevTools Protocol (CDP), Camoufox C++ patched runtime engines, WebGPU / Canvas noise consistency, and Cloudflare Turnstile handling.
- **5-Phase Swarm Delivery Pipeline**: End-to-end multi-agent execution pipeline formalizing Offer Research → Landing/Content → S2S Tracking → Traffic/Ads → ROI Optimization & Scaling with strict A2A contract gates (`mmo-campaign-spec.json`, `mmo-roi-report.json`).
### Pack Spotlight: landing-pages-team (v5.0.0)

The `landing-pages-team` pack governs the end-to-end engineering, conversion rate optimization (CRO), and distributed infrastructure for high-converting single-product landing pages (**Carrd for Ads** — `landing-builder.example.com`):

- **Edge Serverless SSR (< 25ms TTFB)**: 100% Cloudflare Workers edge delivery with `SITES_KV` caching, 0ms cold starts, and dual host routing serving the SaaS Marketing Storefront (`landing-builder.example.com`, `www.landing-builder.example.com`), merchant subdomains (`*.landing-builder.example.com`), and Merchant Dashboard (`app.landing-builder.example.com`).
- **Clean Architecture CA-1..CA-9**: Go 1.25 + Kratos v2 backend enforcing strict architectural invariants (zero ORM leak in `biz`, Wire dependency injection, opaque-box E2E tests, zero secrets, zero linter warnings).
- **Zero-Trust Price Engine (ADR-07)**: Strict server-side recalculation of order totals against database variant models, eliminating client-side price tampering.
- **Aho-Corasick Ad Policy Scanner (ADR-09)**: High-performance linear-time scanner detecting prohibited ad phrases (TikTok/Facebook Ads compliance) before page publication.
- **2D Footwear & Apparel Variant Matrix**: Color $\times$ Size 35-44+ selection with smart availability state machine, native `<dialog id="size-guide-modal">`, 1-click Editor preset, and Telesale Telegram bot alerts (`Màu: ... | Size: ...`).
- **Vietnamese E-commerce Localization**: 1-touch COD checkout, VietQR Napas 247 dynamic QR codes, floating Zalo & Messenger contact widgets, and trusted footer legitimacy (physical warehouse address & 1-to-1 warranty).

### Pack Spotlight: affiliate-cashback-team (v5.0.0)

The `affiliate-cashback-team` pack governs the end-to-end engineering, automated deal intelligence, financial reconciliation, and conversion optimization for the CashbackHub affiliate & cashback ecosystem (`cashback.example.com` and `app.cashback.example.com`):

- **Tri-Engine 4-Microservice Architecture**:
  - `deal-bot-dispatcher`: Python 3.11 scraper with curl_cffi Chrome 124+ TLS impersonation & browser fingerprinting bypassing anti-scraping WAFs; LiteLLM Gemini Flash structured deal extraction; multi-channel Telegram/Zalo bot deal broadcasting.
  - `cashback-api-gateway`: FastAPI high-throughput financial gateway enforcing strict Double-Entry Ledger (VAS Chart of Accounts 1010–5010); T+1 automated reconciliation engine; VietQR Napas 247 dynamic payment generation and MoMo disbursement; Redis 7 idempotent deduplication; HMAC-SHA256 affiliate webhook verification.
  - `cashback-pwa-web`: React 19 + Vite + Tailwind CSS mobile-first PWA; offline-capable Service Worker; sub-second 1-1 Chatbot affiliate conversion widget with native clipboard link interception; dynamic BridgePage routing for mobile app-deep-linking.
  - `pseo-nextjs-engine`: Next.js 15+ App Router programmatic SEO engine; on-demand Incremental Static Regeneration (ISR); dynamic multi-cluster hierarchy (brand, category, voucher, store); automated Schema.org JSON-LD graphs; IndexNow push protocol.
- **5 VAS Financial Accounting Invariants**:
  - *Invariant A (Balanced Parity)*: Double-entry ledger parity $\sum \text{Debits} \equiv \sum \text{Credits}$ across TK 1010–5010 enforced at transaction boundaries (`ledger_engine.py:135`, `LedgerUnbalancedException`).
  - *Invariant B (Clawback Protection)*: Contra-Asset TK 1030 automatically debited on affiliate return/cancellation clawback, offset against subsequent cashback before user payouts (`state_machine.py:358-366`, `chk_user_clawback_debt_positive`).
  - *Invariant C (Atomic Concurrency)*: Cash-out withdrawal race conditions eliminated via row-level locking `with_for_update()` in PostgreSQL transactions (`withdrawals.py:151-156`).
  - *Invariant D (Sole Domain Exclusivity)*: Zero domain leak with strict canonical host restriction to `cashback.example.com` and `app.cashback.example.com`, HSTS 63072000s, and metadataBase enforcement (`layout.tsx:14-16`).
  - *Invariant E (Zero-Balance Floor)*: Non-negative floor on TK 2020 Available Cashback ensuring no negative payouts (`ledger_engine.py:165`, `NegativeBalanceException`, `chk_positive_available_balance`).
- **17 Operational Roles Swarm Matrix**: Multi-agent collaboration covering `@researcher`, `@reviewer`, `@seo-analyst`, `@product-manager`, `@project-manager`, `@business-analyst`, `@solution-architect`, `@technical-architect`, `@technical-lead`, `@backend-developer`, `@frontend-developer`, `@sre`, `@system-engineer`, `@task-planner`, `@teacher`, `@content-manager`, and `@content-writer`, supported by domain specialists (`@vietnam-accounting-specialist`, `@ui-ux-designer`).
- **Brand Identity & Design System**: Brand Mascot: Acorn Mascot (playful squirrel hunter mascot), Warm Canvas (`#FBF9F5`), Shopee Accent Orange (`#EE4D2D`), Acorn Gold (`#D97706`), Deep Slate (`#0F172A`), lightweight BridgePage bundle budget ($< 20\text{ KB}$), and Emil Spring physics micro-interactions.

## 2026 Manifest Schema (v2)

All manifests follow `schema_version: "2"` with these fields:

```yaml
schema_version: "2"          # Manifest format version (decoupled from pack version)

name: my-team                # Pack slug (snake_case)
description: "..."           # One-line description

version: 4.0.0               # Pack content version (SemVer)

tags: []                     # Searchable capability tags
author: user
maintained_by: platform-team
license: MIT                 # SPDX identifier (EU CRA SBOM compliance)
homepage: https://github.com/example-org/agent-skills

compatibility:
  min_pack_version: "4.0.0" # Oldest host that can load this manifest
  max_pack_version: "5.x"   # "x" = open-ended minor/patch
  requires_schema: "2"      # Parser must support schema_version 2+

includes:                    # Load order: core first, stack overlay, then project overlay
  - core
  - overlays/stack-overlay
  - overlays/project-overlay

capabilities:                # agentskills.io capability taxonomy
  - code-generation
  - backend
  - seo

data_classification: internal  # public | internal | confidential | restricted

activation:                  # IDE/agent auto-load conditions
  strategy: marker_first     # marker_first | always | explicit
  always: false              # true only for global-engineering
  markers:                   # Repo root files that trigger auto-load
    - go.mod
  glob_patterns:             # Edit patterns that trigger auto-load
    - "**/*.go"
  exclude_patterns:
    - "vendor/**"

governance:                  # Compliance declarations
  eu_ai_act_tier: minimal_risk  # unacceptable | high_risk | limited_risk | minimal_risk
  audit_logging: required
  audit_format: otel-json
  retention_days: 90
  secret_handling: env_only  # env_only | vault | runtime_injection | denied
  human_oversight:
    required: true
    gate_actions:            # Actions requiring human approval before execution
      - run_migration
      - push_to_production
      - modify_secrets
  data_policy: core/policies/data-classification.yaml
  action_policy: core/policies/action-boundaries.yaml
  review_cadence: quarterly
```

## Schema Versioning

| `schema_version` | What Changed |
|-----------------|--------------|
| `"1"` | Original format: name, description, version, tags, author, maintained_by, includes |
| `"2"` | Added: schema_version, license, homepage, compatibility, capabilities, data_classification, activation, governance |

When the manifest field structure changes (field rename, removal, or new required field), bump `schema_version`. **The pack `version` and `schema_version` change independently.**

## Pack Authoring Rules

- always include `core` as the first entry in `includes`
- list stack overlays before project-specific overlays
- all new packs MUST declare `schema_version: "2"` and `governance` block
- `data_classification` must reflect the most sensitive data the pack touches
- `eu_ai_act_tier: minimal_risk` applies to all internal engineering tooling packs
- validate after editing: `python3 core/scripts/validate-packs.py`

## Pack Discovery (2026)

Packs are discovered by AI agents via:

1. **IDE activation**: `activation.markers` + `activation.glob_patterns` in manifest (Cursor, VS Code, Kiro)
2. **A2A Agent Cards**: `core/a2a/.well-known/agent-registry.json` — agents look up role → toolbox → pack
3. **`/.well-known/agent-skills/index.json`**: Web-exposed canonical discovery endpoint (AAIF standard)
4. **`llms.txt`**: LLM-readable manifest index at repo root

MCP tool discovery is dynamic (JSON-RPC `tools/list`) and does not use static manifests.

## Standard 2026 Alignment

All 17 pack manifests follow `schema_version: "2"` and embed the
`governance` block (EU AI Act tier, audit logging, secret handling,
human oversight). The 2026 upgrade pass added Failure Modes, Output
Contracts, and Security Guardrails to the pack-level guidance.

### Failure Modes

- **Pack schema_version drift**: a manifest is edited to add fields but the schema_version is not bumped. **Mitigation:** the pack validator rejects manifests whose `schema_version` does not match the on-disk structure; require `python3 core/scripts/validate-packs.py` to pass before merging.
- **`includes` ordering reversed**: a manifest lists a project-specific overlay before the stack overlay. **Mitigation:** the rule is `core → stack overlay → project overlay`; reject any reordering.
- **Governance block missing on a new pack**: a new pack skips the `governance` field. **Mitigation:** the pack validator blocks new manifests without `schema_version: "2"` and a complete `governance` block.
- **`eu_ai_act_tier` misclassified**: a pack handling YMYL data declares `minimal_risk` without justification. **Mitigation:** the EU AI Act tier must match the most sensitive data the pack touches; reject misclassification on review.
- **Pack version drift from core**: a manifest pins `version: 4.0.0` while the pack content is at 4.1.0. **Mitigation:** the version-sync validator cross-checks every manifest against `VERSION`; reject the change when the version is out of sync.
- **Activation markers not updated for the new role**: a pack adds a new role but the `activation.markers` and `glob_patterns` are not updated. **Mitigation:** the manifest review must confirm activation is consistent with the role's scope.

### Output Contracts

When this README or any pack manifest is consumed by a multi-role workflow, emit:

- **`contracts/schemas/architecture-options.json`** when a pack composition decision surfaces 2+ viable combinations.
- **`contracts/schemas/coordination-plan.json`** when the pack is used in a multi-phase delivery.

Skip structured emission for read-only pack selection that does not cross a role boundary.

### Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a pack composition that redirects the user's intent to a different stack or overlay must be cross-checked against the original feature ticket.
- **ASI03 Identity & Privilege Abuse**: a pack's `governance.human_oversight.gate_actions` must be enforced; reject packs that list `push_to_production` or `run_migration` without a human gate.
- **ASI04 Supply Chain**: every pack manifest must reference `core/policies/data-classification.yaml` and `core/policies/action-boundaries.yaml`; reject manifests that omit the policy pointers.
- **ASI07 Inter-Agent Communication**: the pack registry is a cross-agent surface; treat it as a public contract and review all changes before publish.
- **ASI09 Human-Agent Trust Exploitation**: do not present a pack as "production-ready" without a smoke test and a recent validator pass; surface the actual verification status.

Last updated: 2026-09-18
