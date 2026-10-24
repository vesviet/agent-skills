# Crawl Budget and Bot Access Guide

This guide provides technical reference specifications for managing search crawler budgets, diagnosing crawl inefficiencies and spider traps, and configuring search and AI discovery bot governance.

---

## 1. Crawl Budget Architecture and Mechanics

Crawl budget represents the number of URLs search engine crawlers (e.g., Googlebot, Bingbot) can and intend to crawl on a website within a given timeframe. It is determined by the intersection of two primary factors:

$$\text{Crawl Budget} = f(\text{Crawl Capacity / Rate Limit}, \text{Crawl Demand})$$

### 1.1 Crawl Capacity (Host Load Limit)
The host load limit prevents crawlers from overwhelming site infrastructure. It depends on:
- **Server Response Latency (TTFB)**: Slower responses decrease the host load limit because the crawler throttles concurrent connections to prevent service degradation.
- **Server Errors (5xx)**: If a site returns 500, 502, or 503 errors during crawl bursts, search crawlers rapidly reduce crawl rate.
- **Configured Host Limit**: Search engine webmaster limits (e.g., Search Console crawl rate limits, though now largely automated).

### 1.2 Crawl Demand (Crawl Scheduling)
Crawl demand reflects search engine interest in indexing or refreshing content, influenced by:
- **URL Popularity & Equity**: High PageRank and strong internal linking drive frequent re-crawling.
- **Content Freshness**: Frequently updated content with verified `lastmod` headers increases crawl frequency.
- **Site Size & Inventory**: Large e-commerce or publishing catalogs require higher demand allocations.

---

## 2. Server Response Time and TTFB Diagnostics

Time to First Byte (TTFB) directly governs crawl velocity. When search engine bots crawl a site, they allocate a finite time window per session.

| TTFB Range | Crawl Impact | Classification | Recommended Action |
|------------|--------------|----------------|---------------------|
| $< 200\text{ ms}$ | High crawl velocity; crawlers fetch maximum pages per connection. | Optimal | Maintain CDN edge caching and keep-alive connections. |
| $200 - 500\text{ ms}$ | Moderate crawl rate; acceptable for typical workloads. | Acceptable | Review database query times and static asset caching. |
| $> 500\text{ ms}$ | Crawlers throttle concurrency; significant crawl budget contraction. | Bottleneck | **Issue Technical Escalation Ticket** to DevOps/Cloudflare Engineer. |
| $> 1,000\text{ ms}$ | High risk of connection timeouts, dropped crawls, and indexation lag. | Critical | Edge cache full HTML; implement stale-while-revalidate; scale origin compute. |

### Technical Escalation Trigger for TTFB
When origin TTFB exceeds 500ms on indexable templates:
1. Log sample URLs, response timings, and upstream header `Server-Timing` or `cf-cache-status`.
2. Open ticket assigned to `devops-engineer` or `cloudflare-engineer`.
3. Priority: `must_do_before_publish` for core indexable hubs; `post_publish` for deep archive nodes.

---

## 3. Spider Traps and Infinite Crawl Inefficiencies

Spider traps occur when crawlers are lured into an endless loop of dynamically generated URLs, exhausting the crawl budget before reaching authoritative content.

### 3.1 Common Spider Trap Vectors

#### A. Faceted Navigation and Parameter Permutations
E-commerce and directory sites often allow multi-select filtering (e.g., color, size, brand, sort order). Without constraints, parameters permute exponentially:
- `/products?color=red&size=m&sort=price_asc`
- `/products?size=m&color=red&sort=price_asc` (duplicate content, distinct URL)
- `/products?color=red&size=m&brand=nike&material=cotton...` ($N!$ combinations)

**Remediation**:
- Restrict crawl access to 1-parameter filters via `robots.txt` or canonicalize multi-filter URLs to the single-attribute parent category.
- Add `rel="nofollow"` to dynamic faceted filter links that generate duplicate or low-value combinations.

#### B. Session IDs and Tracking Parameters
Appending session identifiers (`?sid=...`, `?phpsessid=...`) creates unique URLs for identical content on every crawl pass.
**Remediation**:
- Eliminate session IDs from URLs; store session state in HTTP-only cookies.
- Strip tracking parameters (e.g., `utm_*`, `fbclid`, `gclid`) using canonical tags and Cloudflare URL normalization.

#### C. Infinite Calendar and Date Pickers
Booking widgets and event calendars that generate "Next Month" links indefinitely create an infinite crawling loop:
- `/events/2026/10` -> `/events/2026/11` -> ... -> `/events/2099/12`

**Remediation**:
- Block future/past empty calendar paths in `robots.txt`:
  ```robots
  Disallow: /events/*?date=
  Disallow: /events/20[3-9][0-9]/
  ```
- Implement client-side rendering for calendar navigation beyond active booking windows.

#### D. Internal Search Result Indexation
Allowing search bots to crawl internal site search results exposes the crawler to infinite keyword strings and spam injection.
**Remediation**:
- Block internal search paths in `robots.txt`:
  ```robots
  User-agent: *
  Disallow: /search
  Disallow: /search?*
  Disallow: /?s=
  ```
- Add `<meta name="robots" content="noindex, follow">` to all internal search result templates.

---

## 4. Bot Governance in `robots.txt`

Modern web discovery requires distinguishing between:
1. **Traditional Search Engine Crawlers**: Index content for web search results (Googlebot, Bingbot).
2. **Search AI & Conversational Retrieval Crawlers**: Fetch live content to answer real-time user prompts and cite sources (OAI-SearchBot, PerplexityBot, ClaudeBot).
3. **Bulk AI Training Scrapers**: Scrape large-scale content for offline foundation model pre-training (GPTBot, CCBot, Google-Extended).

### 4.1 Search and AI Bot User-Agent Reference

| User-Agent | Operator | Primary Function | Business Impact if Blocked |
|------------|----------|------------------|-----------------------------|
| `Googlebot` | Google | Primary search indexation | Complete de-indexation from Google search |
| `Bingbot` | Microsoft | Search indexation & Copilot | De-indexation from Bing, Yahoo, and Windows Copilot |
| `OAI-SearchBot` | OpenAI | Real-time SearchGPT & ChatGPT search citations | Invisibility in ChatGPT web answers and search citations |
| `PerplexityBot` | Perplexity | Real-time AI answer engine citations | Total omission from Perplexity search answers and sources |
| `ClaudeBot` | Anthropic | Web browsing and citation features | Inability for Claude to retrieve and cite site content |
| `GPTBot` | OpenAI | Model training dataset extraction | Prevents content ingestion into future GPT base weights |
| `CCBot` | Common Crawl | Public web scrape for open datasets | Prevents inclusion in open training datasets |
| `Google-Extended`| Google | Gemini/Vertex AI model training | Controls training usage without affecting Google Search ranking |

### 4.2 Standard Production `robots.txt` Configuration

```robots
# ==============================================================================
# Global Directives & Traditional Search Engines
# ==============================================================================
User-agent: *
Disallow: /api/
Disallow: /admin/
Disallow: /checkout/
Disallow: /search
Disallow: /*?*sort=
Disallow: /*?*filter=
Disallow: /*?*sid=
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# ==============================================================================
# AI Search & Retrieval Crawlers (Explicitly Allowed for Citation Visibility)
# ==============================================================================
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

# ==============================================================================
# AI Model Training Scrapers (Optional Policy Control)
# Note: Blocking training bots does NOT affect live search citations.
# ==============================================================================
User-agent: GPTBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Google-Extended
Disallow: /

# ==============================================================================
# Canonical Sitemap Declarations
# ==============================================================================
Sitemap: https://example.com/sitemap_index.xml
```

### 4.3 Directives Syntax and Specificity Rules
- **Prefix Matching**: Directives match URL paths from the start (`Disallow: /p` matches `/page`, `/product`, `/p/123`).
- **Trailing Wildcard**: `Disallow: /private/*` matches any URL under `/private/`.
- **End-of-String Anchor (`$`)**: `Disallow: /*.pdf$` blocks only URLs ending in `.pdf`.
- **Precedence Rule (RFC 9309 / Googlebot standard)**:
  - If both `Allow` and `Disallow` match a URL, the directive with the **longest match pattern** takes precedence.
  - If both patterns have identical length, `Allow` takes precedence over `Disallow`.

---

## 5. Crawler Verification and Spoofing Prevention

Malicious scrapers frequently impersonate search engine bots by forging the `User-Agent` HTTP header. Technical SEO audits must verify that server infrastructure validates genuine search bots before granting preferential rate limits or bypasses.

### 5.1 Verification Workflow (Reverse DNS Lookup)
1. Extract the client IP address from the request header (`CF-Connecting-IP`, `X-Forwarded-For`).
2. Perform reverse DNS lookup (`PTR` record) on the IP address.
   - For Googlebot, hostname must end in `.googlebot.com` or `.google.com`.
   - For Bingbot, hostname must end in `.search.msn.com`.
   - For OpenAI, verify against published IP ranges or ASN.
3. Perform forward DNS lookup (`A` / `AAAA` record) on the resolved hostname.
4. Verify that the resolved IP matches the original client IP.
