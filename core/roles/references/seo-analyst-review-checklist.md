## SEO Analyst Review Checklist

This reference checklist provides comprehensive, actionable criteria for evaluating technical SEO crawlability, bot governance, connected Schema.org `@graph` architecture, Core Web Vitals, Wikidata entity salience, Answer-First BLUF formulation, and agentic AI discovery.

### 1. Technical SEO & Crawl Budget Diagnostics
- **Clean Indexability & Status Codes**: Audited URLs return direct 200 OK responses; zero soft 404s, unhandled 5xx server errors, or unauthorized 403 blocks on indexable content.
- **Redirect Chain Mitigation (≤1 hop)**: Redirect paths resolve in ≤1 hop; zero redirect chains (>1 hop) or cyclical redirect loops; legacy 302 temporary redirects converted to permanent 301s; permanently removed content serves 410 Gone.
- **XML Sitemap Hygiene**: XML sitemaps (`sitemap.xml`, `sitemap-index.xml`) contain exclusively 200 OK canonical URLs; zero 3xx redirects, 4xx errors, or `noindex` URLs included; `<lastmod>` tags use ISO 8601 format reflecting actual content updates; total URLs per sitemap remain under 50,000 (uncompressed file size < 50MB).
- **Canonical Architecture**: Every indexable page features an explicit, self-referential canonical tag (`<link rel="canonical" href="...">`) pointing to the absolute HTTPS URL; zero cross-domain canonical conflicts or cyclical canonical tags.
- **Rendering Strategy & Hydration Crawlability**: Critical content, primary headings (H1, H2), and navigational links are present in the initial server-rendered HTML (SSG/SSR) rather than relying exclusively on client-side JavaScript execution.
- **Crawl Budget & Depth Optimization**: High-value pages sit within ≤3 clicks from the homepage; crawl traps (infinite faceted navigation, parameter loops) are blocked via `robots.txt` or URL parameter directives.

### 2. Search & AI Bot Crawlability Governance
- **Multi-Bot `robots.txt` Permissions**: `robots.txt` explicitly allows legitimate search engine crawlers (Googlebot, Bingbot) and AI answer engine retrieval crawlers:
  - `User-agent: Googlebot` — `Allow: /`
  - `User-agent: Bingbot` — `Allow: /`
  - `User-agent: OAI-SearchBot` — `Allow: /`
  - `User-agent: PerplexityBot` — `Allow: /`
  - `User-agent: ClaudeBot` — `Allow: /`
  - `User-agent: Applebot-Extended` — `Allow: /`
- **Zero Asset Crawl Blocking**: CSS stylesheets, client JavaScript bundles, fonts, and responsive media required for rendering and layout evaluation are never disallowed in `robots.txt`.
- **`X-Robots-Tag` & Meta Robots Parity**: HTTP response header `X-Robots-Tag` matches on-page `<meta name="robots">` directives; zero conflicting `noindex` directives across headers and HTML.
- **Edge & WAF Firewall Allowlisting**: Cloudflare bot management, WAF rules, and edge rate-limiters allow verified IP ranges and ASNs of search and AI crawlers without presenting CAPTCHAs, rate-limit drops, or Cloudflare Managed Challenge screens.
- **Search Generative AI Feature Inclusion**: Site eligibility confirmed in Google Search Console's "Search generative AI features" settings (avoiding silent opt-out of AI Overviews and AI Mode).

### 3. Core Web Vitals (CWV) & Page Experience Invariants
- **Interaction to Next Paint (INP < 200ms)**: Main thread remains responsive during user interactions; long JavaScript tasks (>50ms) are chunked via `scheduler.yield()` or `requestIdleCallback()`; UI event handlers and transitions execute off-thread or non-blockingly.
- **Largest Contentful Paint (LCP < 2.5s)**: Hero image, banner video poster, or primary typography block loads within 2.5 seconds; above-the-fold images declare `fetchpriority="high"` and responsive `srcset`; render-blocking CSS and web fonts are preloaded or eliminated.
- **Cumulative Layout Shift (CLS < 0.1)**: All image, video, embed, and iframe elements declare explicit `width` and `height` attributes or CSS `aspect-ratio`; dynamic ad units and promotional banners reserve placeholder space to eliminate layout jumps.
- **Mobile Viewport & Touch Ergonomics**: Viewport meta tag configured correctly (`width=device-width, initial-scale=1`); interactive touch targets meet the minimum 24×24px threshold (WCAG 2.5.8 and Google Mobile Experience standards).
- **Field Data Calibration (CrUX)**: Real-user performance verified via Chrome User Experience Report (CrUX) at the 75th percentile rather than relying solely on lab-based synthetic Lighthouse runs.

### 4. Connected Schema.org `@graph` Architecture & Entity Validation
- **Unified `@graph` JSON-LD Block**: All page structured data is consolidated into a single `<script type="application/ld+json">` utilizing the Schema.org `@graph` array syntax; zero disconnected, isolated schema islands.
- **Deterministic Entity `@id` Cross-Referencing**: Entities reference one another via persistent URI fragments (e.g., `https://example.com/#website`, `https://example.com/#organization`, `https://example.com/authors/jane-doe#author`, `https://example.com/post/slug#article`, `https://example.com/post/slug#faq`).
- **Author & Publisher E-E-A-T Modeling**:
  - `Organization` node includes canonical `name`, `url`, `logo`, and verified corporate identifiers.
  - `Person` author node includes `name`, `jobTitle`, `worksFor` pointing to `#organization`, `sameAs` links to authoritative profiles (LinkedIn, GitHub, Google Scholar, ORCID), and `knowsAbout` entity URIs.
- **`TechArticle` / `Article` Entity Grounding**:
  - Contains `headline`, `description`, `datePublished`, `dateModified`, `author`, `publisher`, and `isPartOf`.
  - Specifies `proficiencyLevel` (e.g., "Beginner", "Intermediate", "Expert"), `dependencies`, and `targetPlatform`.
- **1:1 Visual Parity (Anti-Phantom Schema)**: Every question/answer in `FAQPage`, step in `HowTo`, or specification in `Product` microdata matches visible on-page copy 100% verbatim; zero phantom markup violating Google spam policies (`RICH-SNIPPETS-VALIDATION LOCK`).
- **Zero-Error Rich Results Compliance**: Validated against Schema.org Validator and Google Rich Results Test API with 0 errors and 0 unhandled warnings (`SCHEMA-GRAPH-INTEGRITY LOCK`).

### 5. Wikidata Entity Disambiguation & Entity Salience
- **Authoritative Wikidata QID Mapping**: Core topics, frameworks, tools, and organizations mapped to unambiguous Wikidata identifiers (e.g., PostgreSQL → `Q182496`, Kubernetes → `Q22661304`, QUIC → `Q18153406`).
- **`about` vs `mentions` Separation in Schema**:
  - `about` array: Strictly reserved for the primary subject entity (1–2 primary conceptual entities that the document is fundamentally about, linked with `sameAs: "https://www.wikidata.org/wiki/Q..."`).
  - `mentions` array: Used for peripheral, supporting, or comparative technologies and entities referenced in the text (e.g., benchmarked alternatives, dependency libraries).
- **Semantic Triples Formulation**: Article thesis structured around explicit Subject-Predicate-Object triples validated in narrative prose.
- **Lead Sentence Syntactic Salience**: Primary entity positioned as the grammatical subject in the opening sentence under each H2 heading; vague pronouns ("it", "this tool", "the system") banned in opening 50 words of major sections.
- **Topical Entity Co-Occurrence**: 5–8 semantically related entities naturally distributed throughout the content to establish topical depth and Knowledge Graph proximity.

### 6. Answer-First (BLUF) & Generative Engine Optimization (GEO)
- **Strict Two-Sentence BLUF Formulation (≤60 words total)**:
  - *Sentence 1 (≤30 words)*: Direct, conclusive answer satisfying the heading query with zero throat-clearing, introductory fluff, or rhetorical questions.
  - *Sentences 2–3 (≤30 words)*: Quantified metric proof, empirical data, or boundary conditions validating Sentence 1.
- **Query Fan-Out Coverage**: 3–5 related sub-questions (from People Also Ask and LLM query expansions) resolved in dedicated H3 sections on a single comprehensive page (prohibiting thin page-per-variant sprawl).
- **Quantitative Fact Density**: Content maintains a minimum of 3 verifiable, concrete data points (benchmark numbers, hardware parameters, version tags) per 500 words.
- **Modular Data Formatting**: Specification sets, benchmark results, and feature matrices rendered as structured Markdown tables or numbered procedural steps to maximize passage extraction by AI engines.
- **GEO Extractability Index Score (≥80/100)**: Evaluated across BLUF clarity (25 pts), fact density (25 pts), entity salience (25 pts), and modular formatting (25 pts); score ≥80 required for sign-off.
- **Engine-Specific Citation Optimization**: Applied formatting aligned with Perplexity (bracketed inline sources `[1]`), SearchGPT (entity-accurate conversational summaries), and Google AI Overviews (atomic BLUF passages and procedural steps).

### 7. Agentic AI Discovery & Compliance Governance
- **`/llms.txt` and `/llms-full.txt` Manifests**: Machine discovery files deployed with accurate site descriptions, primary documentation links, and clean markdown context; strictly scoped to developer agent tools (Cursor, Claude, Perplexity Pages) and never presented as Google ranking signals (`LLMS-TXT-SCOPE LOCK`).
- **OWASP ASI Compliance Safeguards**:
  - *ASI01 Goal Hijack Prevention*: Briefs and keyword maps strictly align with user/business intent rather than manipulating search query vectors.
  - *ASI03 Identity & Privilege Protection*: Zero internal tokens, private endpoints, or staging URLs leaked in sitemaps, robots.txt, or schema blocks.
  - *ASI04 Tool & Agent Supply Chain*: Third-party SEO tooling, scrapers, and bot identifiers verified against official registries.
  - *ASI07 Structured Contract Interoperability*: Handoff artifacts validate cleanly against JSON schema contracts (`seo-content-brief.json`, `seo-audit-report.json`, `seo-metadata.json`).
  - *ASI09 Non-Exploitative AI Metrics*: AI citation metrics reported with multi-run confidence intervals; zero guarantee claims of LLM placement.
- **MCP Stateless Protocol Verification**: Agent endpoints comply with MCP 2026-07-28 stateless HTTP transport, externalized state, and server card declarations (`/.well-known/mcp/server-card.json`).
- **EU AI Act Article 50 Disclosures**: AI-assisted content features `<AIDisclosureBanner>` elements, `data-ai-generated="true"` container tags, and DOMPurify sanitization.
- **C2PA Content Credentials Provenance**: Technical watermark metadata present on AI-generated visual media assets.

### 8. Traditional SEO & Search Intent Governance
- **Search Intent & Keyword Mapping**: Search intent unambiguously classified (informational, commercial, navigational, transactional); exactly one primary keyword per page; 2–4 secondary keywords assigned.
- **On-Page Metadata Limits**:
  - Title tag ≤ 60 characters with primary keyword in leading position.
  - Meta description ≤ 160 characters with compelling action-oriented summary.
  - URL slug is clean, lowercase, kebab-case, containing the primary keyword without stop-word bloat.
- **7-Day Cannibalization Audit**: Overlap check completed against site inventory and publishing sprint boards; zero conflicting primary keyword assignments across active URLs.
- **Internal Linking Topology**: Minimum 3 contextual internal links adhering to Silo link topology (cluster → pillar upward authority, contextual cross-cluster links); natural anchor text variation (zero exact-match spam).
- **Structured Machine Handoff**: Emission of `contracts/schemas/seo-content-brief.json`, `contracts/schemas/seo-audit-report.json`, or `contracts/schemas/seo-metadata.json` matching schema definitions.
