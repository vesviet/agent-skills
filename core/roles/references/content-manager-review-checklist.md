## Content Manager Review Checklist

This reference checklist provides actionable governance rubrics for evaluating portfolio content strategy, pillar-cluster taxonomy, audience lifecycle journeys, 3-tier decay triage SLAs, ROT pruning, and safe multi-channel distribution loops.

### Strategy Quality & Pillar-Cluster Architecture
- **Pillar-Cluster Taxonomy**: Content is organized into defined pillar pages anchoring comprehensive sub-topic clusters; orphan articles or unanchored topics are prohibited.
- **Internal Linking Topology**: Every cluster article links upward to its canonical parent pillar page and laterally to related cluster sibling nodes, reinforcing topical authority.
- **Topical Authority Hierarchy**: Semantic hierarchy maps primary domain entities to sub-clusters, preventing topic cannibalization before production briefs are commissioned.
- **Full-Funnel Journey Alignment (TOFU / MOFU / BOFU)**: Content portfolio maintains balanced allocation across Top of Funnel (awareness & educational guides), Middle of Funnel (evaluation & architecture trade-offs), and Bottom of Funnel (conversion, decision frameworks, direct product fit).
- **Target Audience Segmentation**: Target audience segments are specific and differentiated, not generic ("all developers").
- **Non-Commodity Moat Strategy**: Documented plan identifying proprietary data, internal tooling, or unique practitioner benchmarks that protect against AI commodity generation.
- **AI Content Governance Policy**: Explicit policy defining human editorial review gates, C2PA provenance tracking, and disclosure standards.

### Top 10 SERP Information Gain Gate
- **Competitor SERP Differential**: Verified against top 10 search ranking pages (not just top 3); consensus content patterns mapped and documented.
- **Non-Commodity Score Threshold (≥75/100)**: Evaluated per scoring matrix; candidate topics failing this threshold are rejected or rescoped.
- **Information Gain Vectors**: At least one of the 5 vectors is verified (primary data/benchmarks, proprietary architecture/workflows, counter-consensus trade-offs, production incident postmortems, interactive tools).
- **Zero Skyscraper Paraphrasing**: Outright rejection of briefs or drafts that merely compile and reword ranking competitor consensus.
- **Mandatory Substance Requirement**: Every brief specifies at least one non-negotiable empirical proof element (telemetry trace, SME transcript quote, reproduction log).

### Anti-Slop & Boilerplate Governance
- **Commission Gate Compliance**: Every brief assigned to Content Writer includes an explicit `unique_angle` statement and `boilerplate_risk` flags for high-risk topics.
- **Approve Gate Verification**: Writer's Anti-Slop Gate (`anti_slop_gate.gate_passed: true`) verified before any draft advances to publication.
- **Zero Blacklisted AI Clichés**: Zero tolerance for banned robotic tropes ("delve", "tapestry", "testament", "unlock", "game-changer", "beacon", "foster", "realm", "crucial", "harness", "navigating", etc.).
- **20/60/20 Burstiness & Cadence Verification**: Sentence lengths follow natural human distribution (~20% short, ~60% medium, ~20% complex); no 3 consecutive sentences of identical word length.
- **Boilerplate Elimination**: Intros, mid-sections, and conclusions verified free of generic throat-clearing, tour-guide transitions, or redundant summaries.
- **Portfolio-Level Slop Scans**: Regular library audits document `slop_risk_inventory` to catch intro formula drift or repetitive phrasing across published URLs.

### Expert Authenticity & SME Verification
- **Practitioner Credential Verification**: SME bylines validated against active digital footprints (LinkedIn, GitHub, Google Scholar, corporate bio).
- **Schema.org Person Binding**: Author entities include verified, authoritative `sameAs` profile URLs.
- **Archived Interview Provenance**: Raw interview audio or transcripts archived; direct quotes and case study metrics trace to specific timestamps.
- **Anti-Synthetic Persona Prohibition**: Strictly ban stock-photo profiles, simulated practitioner avatars, or invented expert personas.

### 3-Tier Content Decay Monitoring & Remediation SLAs
- **Comprehensive Decay Scanning**: Regular monitoring scans active across all 3 tiers:
  - *Tier 1 (Algorithmic SERP Decay)*: Organic rank drops (>3 positions) or sustained impression deterioration (>25% MoM).
  - *Tier 2 (GEO / AI Engine Citation Decay)*: Citation tracking across Google AI Overviews, SearchGPT, and Perplexity flagging URLs with ≥15% citation drop over 30 days.
  - *Tier 3 (Factual & Temporal Decay)*: Outdated statistics (>18 months), deprecated tooling/API syntax, or broken outbound links.
- **Enforced Remediation SLAs**:
  - *Action 1 — Quick Patch (≤15 days)*: Remediate outdated statistics, deprecated code snippets, and broken links.
  - *Action 2 — Structural Rewrite (≤30 days)*: High-decay assets (Tier 1 rank loss >3, Tier 2 ≥15% GEO citation drop) undergo full BLUF restructuring and fresh empirical proof integration.
  - *Action 3 — Consolidation (≤20 days)*: Merge cannibalizing or thin URLs into comprehensive pillar guides with 301 redirects mapped.
  - *Action 4 — Decommissioning (≤10 days)*: Deprecate obsolete assets with 410 Gone or 301 redirects.
- **ROT Content Pruning**: Systematically audit and prune Redundant, Outdated, and Trivial (ROT) URLs to prevent domain authority dilution and crawl budget waste.

### Editorial Calendar & Resource Allocation
- **Full Assignment Clarity**: Every calendar item specifies topic, pillar, format, unique angle, assigned writer, and deadline.
- **Pre-Production Briefing**: SEO content brief or strategic brief signed off before writing commences.
- **Portfolio Pillar Balance**: Publishing cadence maintains proportional balance across pillars without single-topic flooding.
- **Capacity Calibration**: Production commitments match verified team velocity and SME interview availability.

### Safe Multi-Channel Distribution & Semantic Drift Prevention
- **Upfront Distribution Loops**: Every pillar article is paired with an upfront distribution plan across target channels (LinkedIn, X/Twitter, newsletter, video).
- **Repurposing Matrix Alignment**: Specific formats mapped per channel (technical thread, executive summary, video script).
- **Semantic Drift Guardrails**: Derivative assets verified to preserve all primary architectural trade-offs, security warnings, configuration constraints, and failure modes.
- **Attribution & Analytics**: Canonical URL tags and standardized UTM campaign parameters configured across all distribution surfaces.
- **Timeline Synchronization**: Distribution sequencing coordinated directly with editorial calendar milestones.

### Content Audit & Portfolio Health
- **Data-Driven Audit Decisions**: Classifications (`keep`, `refresh`, `expand`, `consolidate`, `redirect`, `retire`) grounded in verified GSC, analytics, and citation data.
- **Cannibalization Resolution**: Conflicting search intents identified and resolved through structural merging or clear intent differentiation.
- **Prioritized Refresh Pipeline**: High-value decaying pillars prioritized over net-new production to protect existing search moats.

### Performance Measurement & Governance
- **Pre-Production KPI Alignment**: Target business outcomes, organic session goals, and conversion metrics established prior to drafting.
- **AI Share of Voice (AI SOV)**: Citation velocity and presence across generative answer engines tracked alongside traditional organic traffic.
- **Data-Traceable Decisions**: Strategy pivots, content prunes, and calendar adjustments directly supported by historical performance telemetry.
