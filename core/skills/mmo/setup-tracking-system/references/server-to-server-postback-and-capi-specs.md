# Server-to-Server (S2S) Postback & Meta CAPI Specifications (2026)

## 1. Tracking Topology in Cookieless Environments

With third-party cookie deprecation, Apple Safari ITP, and aggressive ad-blocker filtering, client-side pixel tracking experiences $>35\%$ signal loss. S2S architecture bridges edge capture to platform endpoints:

```
User Click on Ad (Meta / TikTok / Google)
            │ (Query Params: fbclid, gclid, ttclid)
            ▼
Edge Proxy / CDN Worker (Cloudflare)
  - Extracts parameters
  - Writes First-Party HTTP-Only Cookies (fbp, fbc, gclid)
  - Generates Shared UUIDv4 event_id
            │
            ├──────────────────────────────┐
            ▼ (Client Web Pixel)           ▼ (S2S API Gateway)
    Client Browser Event           Server-Side Event Dispatcher
    (Subject to ad-blockers)       - Meta CAPI v20+
            │                      - TikTok Events API v1.3
            │                      - Google Enhanced Conversions
            └──────────────┬───────────────┘
                           ▼
             Ad Platform Conversion Hub
             (Deduplicated via event_id)
```

## 2. Meta Conversions API (CAPI v20+) Standards

### 2.1 Event Match Quality (EMQ) Optimization
Target EMQ $\ge 8.0/10$ requires sending rich normalized user data parameters:
- `em`: SHA-256 lowercase email, leading/trailing whitespace stripped.
- `ph`: SHA-256 phone number normalized to international E.164 format (`+1...`).
- `fbp`: First-party Facebook browser cookie.
- `fbc`: First-party Facebook click identifier (`fb.1.{timestamp}.{fbclid}`).
- `client_ip_address`: True client IPv4 or IPv6 (extracted from `CF-Connecting-IP`).
- `client_user_agent`: Unaltered browser user agent string.

### 2.2 Deduplication Window
Meta deduplicates events received within a 48-hour window matching on `(event_name, event_id)`.

## 3. Click-to-Conversion Time (CTIT) Fraud Filtering

- **Automated Script Injection**: If $\Delta t_{\text{conversion}} - t_{\text{click}} < 2.5\text{s}$, the transaction is discarded as programmatic bot click injection.
- **Click Hijacking**: Conversion delays $> 7\text{ days}$ on short-window impulse offers are quarantined for attribution review.
