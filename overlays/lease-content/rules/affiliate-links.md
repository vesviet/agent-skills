# Affiliate Link Automation & Guidelines

This rule outlines the automation standard and placement guidelines for affiliate links in `leaseinvietnam`.

## 1. Automation via Redirects
- **Link Cloaking**: Use a standard markdown link pointing to the `/go/` directory instead of raw affiliate links. 
  Example: `Book your stay on [Agoda](/go/agoda) to get the best rates.`
- **Auto-Tagging**: At build time, the system will convert `[Agoda](/go/agoda)` into `<a href="/go/agoda" target="_blank" rel="sponsored nofollow" data-affiliate="true">Agoda</a>`.

## 2. Adding New Partners
- Add the redirect to `astro.config.ts`.
  ```ts
  redirects: {
    '/go/partnername': 'https://www.partner-affiliate-url.com/?aff_id=XXXXXXX',
  }
  ```

## 3. Placement Guidelines
- **Maximum**: 2 affiliate links per article.
- **Relevance**: Only place in contextually relevant sections.
- **Prohibited**: NEVER place affiliate links in scam or trust-safety articles (to maintain trust integrity).
