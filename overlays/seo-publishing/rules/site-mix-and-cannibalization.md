# Site Mix And Cannibalization — Lease + May Lanh

Content cluster balance, 7-day keyword discipline, topical authority mapping, and AI visibility for the dual-site sprint overlay. Updated for 2025–2026 SEO standards.

## Lease in Vietnam (leaseinvietnam)

### Content clusters (rotate across 7 days)

| Cluster | Examples |
| ------- | -------- |
| guides | Step-by-step rental, visas, contracts |
| neighborhood-comparison | District vs district, area guides |
| trust-safety | Deposits, scams, legal checklists |
| market-radar | Trends, pricing signals |

### Weekly requirements

- At least **1 post** in the week links prominently to a high-value **property/** listing
- Balance clusters: avoid 3+ consecutive posts in the same cluster unless sprint theme dictates it

### Cannibalization

- Do not assign the same **primary keyword intent** as any Lease post in the last **7 days** (check publish-log.md and plan inventory)
- Similar neighborhoods (e.g. Thao Dien vs An Phu) need distinct primary keywords and angles

### High-value link examples

- property/* listings aligned with neighborhood topic
- Existing guides/trust-safety posts for supporting anchors

### Topical Authority — Pillar–Cluster Map (Lease)

Define pillar pages per cluster. Every new article must link to its pillar:

| Pillar topic | Pillar page (create if absent) | Cluster articles link here |
| ------------ | ----------------------------- | -------------------------- |
| Complete guide to renting in Vietnam | /guides/complete-rental-guide | All guides/* posts |
| Ho Chi Minh City neighborhoods | /guides/hcmc-neighborhoods | All neighborhood-comparison/* posts |
| Rental safety and trust | /guides/rental-safety | All trust-safety/* posts |
| Vietnam rental market trends | /guides/market-overview | All market-radar/* posts |

- Each cluster article = **supporting** or **supplementary** position
- Pillar pages should be **evergreen**, updated quarterly with links to newest cluster articles
- Verify pillar–cluster balance weekly: each pillar page should have ≥3 supporting articles

### Information Gain (Lease)

- Each brief must document what unique value the article adds: local insider knowledge, original photos, real lease examples, Vietnamese legal specifics
- YMYL-adjacent: rental contracts, deposits, legal rights → require elevated E-E-A-T (firsthand experience, source citations)

## May Lanh Treo Tuong (maylanhtreotuong)

### Content clusters

| Cluster | Path hints |
| ------- | ---------- |
| buying-guide | huong-dan/* |
| technical explainer | kien-thuc/* |
| comparison-review | so-sanh/*, review/* |

### Weekly requirements

- At least **1 post** per week links to a high-value **product/** page
- Prefer posts that connect explainers to a specific SKU when comparing brands

### Cannibalization

- No duplicate primary intent vs May lanh posts in last **7 days**
- Avoid back-to-back same brand comparison (e.g. two Daikin vs X posts) without differentiated primary keyword

### High-value link examples

- product/daikin-*, product/casper-*, bang-gia/* when price intent fits

### Topical Authority — Pillar–Cluster Map (May lanh)

| Pillar topic | Pillar page (create if absent) | Cluster articles link here |
| ------------ | ----------------------------- | -------------------------- |
| Complete guide to wall-mounted AC | /huong-dan/may-lanh-treo-tuong-tong-hop | All buying-guide/* posts |
| AC technical knowledge | /kien-thuc/kien-thuc-may-lanh | All technical explainer/* posts |
| Brand and model comparison | /so-sanh/so-sanh-may-lanh-tong-hop | All comparison-review/* posts |

- Same pillar–cluster rules as Lease: supporting articles link to pillar, pillar updated quarterly
- Verify pillar–cluster balance weekly: each pillar page should have ≥3 supporting articles

### Information Gain (May lanh)

- Each brief must document unique value: hands-on test results, local pricing data, energy efficiency comparisons specific to Vietnam climate
- Product reviews: require firsthand testing data or documented expert interview — do not rewrite manufacturer specs only

## Cross-Site Rules

- Lease and May lanh keywords are independent — duplication across sites is allowed
- Dual-site day: brief **both** sites before drafting either
- Carry-over posts re-enter board with new date; re-check cannibalization against updated 7-day window
- Each site maintains its own pillar–cluster map independently

## Entity SEO — Cross-Site

- Define **Organization** entity for each site with stable `@id` (e.g. `https://leaseinvietnam.com/#organization`)
- Each site should have **Person** schema for recurring authors
- Use `sameAs` links to social profiles and authoritative external sources
- Schema implementation is Frontend responsibility; SEO Analyst specifies requirements in brief

## AI Visibility — Cross-Site

- Weekly: search top 3 primary keywords per site in Google AI Overview, Perplexity, and ChatGPT
- Track citation presence in publish-log weekly rollup
- Identify **citation gaps**: keywords where competitors are cited but we are not → priority for next week
- Ensure robots.txt allows AI bots: OAI-SearchBot, PerplexityBot, ClaudeBot, BingBot

## SEO Analyst Checklist (per post)

### Traditional SEO
- [ ] Cluster label assigned
- [ ] Primary keyword unique on that site for 7 days
- [ ] ≥3 internal links listed with anchors
- [ ] High-value property/product link included when weekly quota not yet met
- [ ] Brief documents search intent and FAQ need

### GEO / AEO
- [ ] Answer-first block specified (≤60 words per H2)
- [ ] Query fan-out list included (3–5 sub-questions)
- [ ] Answer format specified per section
- [ ] Fact density target documented

### Topical Authority
- [ ] Pillar page URL assigned
- [ ] Cluster position documented (supporting/supplementary)
- [ ] Information gain documented (unique value vs top SERP results)

### E-E-A-T
- [ ] Experience proof type specified
- [ ] Author entity documented
- [ ] YMYL-adjacent flag set when applicable

### Schema
- [ ] Schema types recommended (Article, FAQPage, HowTo, Product)
- [ ] Technical SEO ticket created for Frontend when schema changes needed
