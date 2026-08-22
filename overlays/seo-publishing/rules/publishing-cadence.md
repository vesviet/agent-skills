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
