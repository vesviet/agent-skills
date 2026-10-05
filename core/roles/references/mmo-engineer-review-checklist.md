## MMO Engineer Review Checklist

This reference checklist provides operational verification criteria for multi-account growth automation, traffic acquisition, proxy infrastructure, and server-side tracking to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across anonymity preservation, anti-detect browser profile compartmentalization, TLS JA4 fingerprint consistency, WebRTC leak defense, behavioral interaction humanization, Server-to-Server (S2S) event deduplication, budget ceilings, and legal compliance boundaries.

### 1. Anonymity & High-Trust Proxy Infrastructure (`ANONYMITY-LOCK`)
- **Zero Origin IP & Footprint Exposure**:
  - all outbound browser sessions and automation requests route strictly through dedicated Residential, ISP, or 4G/5G mobile proxy pools; datacenter IPs strictly prohibited for high-risk platform interactions
  - proxy connectivity pre-flight checks verify zero DNS leaks, IPv6 address leaks, or WebRTC IP exposure before navigating to target platforms
  - proxy rotation policies enforce sticky sessions per account session ($\ge 30\text{min}$) to prevent mid-session IP flapping bans
- **Container Resource & Bandwidth Governance (`PROXYWARE-LOCK`)**:
  - bandwidth monetization nodes (EarnApp, Honeygain) deployed only with explicit CPU ($\le 0.5\text{ vCPU}$) and RAM ($\le 512\text{MB}$) container cgroup limits
  - datacenter deployment of proxyware containers without residential proxy routing strictly prohibited

### 2. Browser Profile Compartmentalization & Isolation (`ISOLATION-LOCK`)
- **Strict Account Compartmentalization**:
  - each ad account, social profile, or marketplace merchant runs in an isolated, hermetic browser profile (GoLogin, Multilogin, AdsPower, or patched Chromium CDP)
  - zero cross-account profile sharing: local storage, IndexedDB, cookies, and cache completely siloed
  - shared Business Managers (BMs) or advertising pixels partitioned to prevent cascading suspension of adjacent assets
- **Hardware Fingerprint Consistency**:
  - Canvas 2D, WebGL, AudioContext, and Client Rects fingerprints randomized consistently at profile creation and locked permanently for that profile's lifetime
  - screen resolution, device pixel ratio, and WebGL renderer (`ANGLE (NVIDIA...)` vs Apple GPU) match declared User-Agent OS profile

### 3. TLS JA4 Fingerprinting & Protocol Stack Coherence
- **TLS Client Hello & JA4 Fingerprint Parity**:
  - HTTP/TLS client libraries (tls-client, curl-impersonate, Playwright patched engines) match the JA4 fingerprint of legitimate Chrome, Safari, or Firefox browsers exactly
  - Cipher suites, TLS extensions, supported elliptic curves, and ALPN negotiate in authentic browser sequence
- **HTTP/2 SETTINGS & Header Ordering**:
  - HTTP/2 `SETTINGS` frame parameters (HEADER_TABLE_SIZE, INITIAL_WINDOW_SIZE, MAX_CONCURRENT_STREAMS) match standard browser defaults
  - pseudo-headers (`:method`, `:authority`, `:scheme`, `:path`) and request headers preserve authentic casing and order

### 4. WebRTC Leak Defense & Network Isolation
- **WebRTC STUN/TURN Leak Prevention**:
  - browser profile enforces `media.peerconnection.enabled = false` or binds WebRTC candidates strictly to proxy interface IPs
  - public STUN server IP reflection tests verify that the host's actual public IP is never leaked via ICE candidate discovery
- **Timezone, Geolocation & Locale Alignment**:
  - system timezone offset, browser language headers (`Accept-Language`), and Geolocation API coordinates synchronized dynamically with the geolocated proxy IP

### 5. Behavioral Humanization & Organic Interaction Curves (`BEHAVIORAL-LOCK`)
- **Non-Uniform Interaction Patterns**:
  - mouse movements follow natural cubic Bézier curves with randomized acceleration and deceleration; straight-line instant coordinate jumps rejected
  - keystroke intervals inject realistic Gaussian typing jitter ($80\text{ms} \pm 35\text{ms}$ per character) with realistic typo and backspace frequency
  - interaction scripts incorporate randomized pause intervals, page scrolling deceleration, and reading dwell times
- **AI Safety & Moderation Boundaries**:
  - behavioral humanization concerns client-side bot detection heuristics only; bypassing AI safety guardrails, platform moderation filters, or content safety policies is strictly denied

### 6. Server-to-Server (S2S) Tracking & Conversion Dedup (`TRACKING-LOCK`)
- **Dual Tracking & Deterministic Event Deduplication**:
  - conversion funnels implement Server-to-Server postbacks (Meta Conversions API CAPI, TikTok Events API, Google Enhanced Conversions) alongside client-side tags
  - client pixel events and server CAPI events share an identical deterministic `event_id` (UUIDv4) and matching `event_name` to enable 100% duplicate event deduplication
- **First-Party Data Hashing & Privacy Compliance**:
  - customer match parameters (email, phone number) normalized (lowercase, trimmed, E.164 format) and hashed client-side or in-memory using SHA-256 before transmission

### 7. Budget Ceilings & FinOps Spend Circuit Breakers (`BUDGET-LOCK`)
- **Hard Daily Spend & API Caps**:
  - advertising campaigns and automated bidding engines enforce hard-coded daily budget caps at the API level
  - LLM content generation scripts enforce per-run token ceilings and max cost thresholds; script halts automatically upon reaching 80% of budget allocation
  - automated spend monitoring alerts operator immediately if cost-per-acquisition (CPA) breaches threshold

### 8. Legal Compliance & Platform Terms Review (`REVIEW-SYSTEM LOCK`)
- **Mandatory Escalation for Ad Review Evasion**:
  - any technique involving cloaking, deceptive traffic routing, or fingerprint spoofing intended to evade ad review, content moderation, or regulatory safety systems requires explicit written authorization and Security Engineer review
  - compliance boundaries from `core/policies/action-boundaries.yaml` strictly upheld; unauthorized destructive actions blocked fail-closed
