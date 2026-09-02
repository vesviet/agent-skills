# Publishing Cadence & Operational Runbook

Rules for the daily operation of the SEO Publishing overlay — cadence limits, scheduling, and per-post baselines.

## 1. Dual-Site Sprint Cadence

- **Maximum Output:** 2 posts per day total.
- **Distribution:** 1 post for Lease in Vietnam + 1 post for Máy Lạnh Treo Tường.
- **Cadence Window:** Rolling **7-day Topic Board** cycle.

## 2. Per-Post Baseline Requirements

Every post must satisfy three optimization layers before going live:

### A. GEO / AEO Layer (Generative & Answer Engine Optimization) — 2026

**2026 Research Insights:**
- 76% of AI search citations still originate from Google top-10 — do NOT abandon classic SEO
- 85% of AI brand mentions come from third-party sources (press, forums, independent reviews)

**Required:**
- **Answer-First Structure:** Introduction MUST answer core intent within ≤60 words.
- **Fact Density:** Replace generic filler with concrete specs and data (≥3 verifiable data points/500w).
- **Query Fan-Out:** Structure headings to address logical follow-up questions (People Also Ask / LLM follow-ups).
- **Schema/JSON-LD:** Specify structured data type per article (Article, FAQPage, Product, HowTo, BreadcrumbList).
- **AI Extractability:** Format key facts as standalone paragraphs scannable by AI citation engines.
- **Multimodal Optimization:** Accurate, descriptive Alt text on all images for Visual Search (Google Lens, AI image search).
- **Do NOT block AI crawlers** at CDN/WAF level — allowlist Googlebot, GPTBot, ClaudeBot, PerplexityBot.
- **Avoid thin AI-generated content** — penalized by 2026 algorithms; inject firsthand experience.

### B. E-E-A-T & Trust Layer

- **Experience Proof:** Draft MUST contain explicit evidence of first-hand experience.
- **Author Entity:** Author clearly declared and linked to an established entity page.
- **Third-Party Earned Media:** Actively pursue external mentions (press, forums, independent reviews) — far more weighted than self-published content for AI citations.

### C. Traditional SEO Layer

- Primary keyword in title, URL slug, and meta description.
- Minimum 3 internal links (preferably 4+ as per `overlays/lease-content` rules).
- Schema/JSON-LD specifications documented for Frontend Developer to implement.

## 3. AI Visibility Tracking (Weekly)

Track AI citation presence across:
- Google AI Overviews (Google Search)
- Perplexity AI
- ChatGPT / Bing Copilot

Verify: which articles appear as citations in relevant AI-generated answers. Log in weekly rollup.

## 4. Vietnam Market Specifics (2026)

- 93% of Vietnamese SMEs now use AI tools — conversational commerce is table stakes.
- Integrate AI chatbot on Messenger/Zalo for product discovery alongside standard SEO.
- Vietnamese-language content benefits from Zalo SEO optimization alongside Google.

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `See `core/skills/content/optimize-seo/SKILL.md` and the `seo-content-brief.json` schema.` for the related skill output contract reference.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/content/optimize-seo/SKILL.md` and the `seo-content-brief.json` schema.

Last updated: 2026-09-01
