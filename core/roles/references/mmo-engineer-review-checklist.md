## MMO Engineer Review Checklist

This reference checklist provides operational verification criteria for multi-account growth automation, traffic acquisition, proxy infrastructure, and server-side tracking to meet SOTA 2026–2027 standards. It establishes non-negotiable verification gates across anonymity preservation, anti-detect browser profile compartmentalization, TLS JA4 fingerprint consistency, WebRTC leak defense, behavioral interaction humanization, Server-to-Server (S2S) event deduplication, budget ceilings, and legal compliance boundaries.

### 1. Anonymity & High-Trust Proxy Infrastructure (`ANONYMITY-LOCK`)
- **Zero Origin IP & Footprint Exposure**:
  - all outbound browser sessions and automation requests route strictly through dedicated Residential, ISP, or 4G/5G mobile proxy pools; datacenter IPs strictly prohibited for high-risk platform interactions
  - proxy connectivity pre-flight checks verify zero DNS leaks, IPv6 address leaks, or WebRTC IP exposure before navigating to target platforms:
    ```bash
    # Verify zero origin IP leaks across WebRTC and DNS interfaces
    curl -x "http://user:pass@proxy.internal:8080" https://api.ipify.org
    dig +short whoami.akamai.net @resolver1.opendns.com
    ```
  - proxy rotation policies enforce sticky sessions per account session ($\ge 30\text{min}$) to prevent mid-session IP flapping bans
- **Container Resource & Bandwidth Governance (`PROXYWARE-LOCK`)**:
  - bandwidth monetization nodes (EarnApp, Honeygain) deployed only with explicit CPU ($\le 0.5\text{ vCPU}$) and RAM ($\le 512\text{MB}$) container cgroup limits
  - datacenter deployment of proxyware containers without residential proxy routing strictly prohibited

### 2. Browser Profile Compartmentalization & Camoufox C++ Engine (`ISOLATION-LOCK` / `CAMOUFOX-C++-PATCH-LOCK`)
- **Strict 1:1:1 Isolation Invariant**:
  - operations must enforce strict 1:1:1 isolation: 1 ad account $\leftrightarrow$ 1 virtual corporate card (VCC) $\leftrightarrow$ 1 dedicated browser profile across $\ge 4$ diverse corporate BINs
  - zero cross-account profile sharing: local storage, IndexedDB, cookies, and cache completely siloed
  - shared Business Managers (BMs) or advertising pixels partitioned to prevent cascading suspension of adjacent assets
- **Binary-Level Fingerprint Patching (Camoufox)**:
  - browser automation must execute through C++ source-patched engines (Camoufox) where fingerprinting APIs are overridden at the binary level
  - JavaScript prototype shims (`window.cdc_`, `Runtime.enable`, `navigator.webdriver` overrides) strictly prohibited: platform bot detection scripts inspect prototype descriptors to detect JS wrappers

### 3. TLS JA4 Fingerprinting & Protocol Stack Coherence (`TLS-JA4-FINGERPRINT-LOCK`)
- **BoringSSL JA4 Parity via `curl_cffi`**:
  - HTTP client requests must impersonate genuine browser TLS signatures using BoringSSL (`curl_cffi`) matching authentic JA4 fingerprints (`t13d1516h2_...`):
    ```python
    # POSITIVE: Authentic Chrome JA4 TLS and HTTP/2 Fingerprint Impersonation
    from curl_cffi import requests
    
    session = requests.Session(impersonate="chrome124")
    response = session.get(
        "https://platform.internal/api/auth",
        headers={"Accept-Language": "en-US,en;q=0.9"},
        proxies={"https": "http://user:pass@resi.proxy:10001"}
    )
    ```
  - naive `requests` or unpatched `urllib3` calls are prohibited fail-closed (instantly flagged by Cloudflare/Akamai bot managers)
- **WebGPU / WebGL Hardware Alignment & MurmurHash3 Noise**:
  - WebGL `UNMASKED_RENDERER` and `UNMASKED_VENDOR` strings must achieve bitwise consistency with WebGPU `requestAdapter()` hardware limits and available extensions
  - Canvas 2D and WebGL rendering noise generated using deterministic MurmurHash3 seeding per browser profile to maintain consistent fingerprint hashes across sessions while evading cluster analysis

### 4. Behavioral Humanization & Fitts' Law Trajectories (`BEHAVIORAL-LOCK` / `BEZIER-FITTS-TRAJECTORY-LOCK`)
- **Cubic Bézier Cursor Movement Modeling**:
  - mouse movements follow natural cubic Bézier splines obeying Fitts' Law with human acceleration and deceleration:
    $$MT = a + b \cdot \log_2\left(1 + \frac{D}{W}\right)$$
    where $MT$ is movement time, $D$ is distance to target, and $W$ is target clickable width:
    ```python
    # POSITIVE: Cubic Bézier Curve Generation with Velocity Deceleration
    def generate_human_trajectory(p0, p3, steps=50):
        # Generate control points with human jitter
        p1 = (p0[0] + (p3[0] - p0[0]) * 0.25 + random.uniform(-20, 20), p0[1] + random.uniform(-15, 15))
        p2 = (p0[0] + (p3[0] - p0[0]) * 0.75 + random.uniform(-20, 20), p3[1] + random.uniform(-15, 15))
        trajectory = []
        for i in range(steps):
            t = i / float(steps)
            # Cubic Bézier formula: B(t) = (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3
            x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
            trajectory.append((x, y))
        return trajectory
    ```
  - straight-line instant coordinate jumps or instantaneous clicks rejected fail-closed
- **Gaussian Keystroke Jitter**:
  - keystroke intervals inject realistic log-normal typing jitter ($80\text{ms} \pm 35\text{ms}$ per character) with realistic typo and backspace frequency

### 5. Quantitative Financial Engineering & True ROI Modeling (`TRUE-ROI-FINANCIAL-LOCK`)
- **True ROI Formula Invariant**:
  - financial campaign tracking must compute **True ROI**, incorporating ad spend, residential proxy bandwidth costs, LLM tokens, and account die-rate depreciation:
    $$\text{True ROI} = \frac{\text{Net Revenue} - (\text{Ad Spend} + C_{\text{proxy}} + C_{\text{tokens}} + C_{\text{die}})}{\text{Total Cost}} \times 100\%$$
- **Thompson Sampling Autonomous Budget Allocation (`THOMPSON-SAMPLING-BUDGET-LOCK`)**:
  - multi-adset budget allocation executes via Thompson Sampling with Beta priors:
    $$\theta_k \sim \text{Beta}(\alpha_k + 1, \beta_k + 1)$$
    where $\alpha_k$ is conversions and $\beta_k$ is non-converting visits
  - kill underperforming ad sets when ROAS $< 0.75$ after $\$150.00$ ad spend
- **Weibull Survival Retention Modeling**:
  - subscription affiliate retention modeled via Weibull distribution ($t_{1/2} = \lambda (\ln 2)^{1/k}$) to forecast long-term LTV and churn

### 6. Server-to-Server (S2S) Tracking & Conversion Dedup (`TRACKING-LOCK` / `DUAL-LAYER-S2S-TRACKING-LOCK`)
- **Dual-Layer S2S Deduplication Invariant**:
  - conversion funnels implement Server-to-Server postbacks (Meta CAPI, TikTok Events API, Google Enhanced Conversions) alongside client-side browser pixels
  - client pixel events and server CAPI events share an identical deterministic `event_id` (UUIDv4) and matching `event_name`:
    ```json
    {
      "event_name": "Purchase",
      "event_time": 1729123456,
      "event_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
      "user_data": {
        "em": ["2402502ba4a1a302a9ecd20..."],
        "client_ip_address": "198.51.100.42",
        "client_user_agent": "Mozilla/5.0..."
      }
    }
    ```
  - Event Match Quality (EMQ) verified at $\ge 8.5/10.0$ and Click-to-Install Time ($t_{\text{CTIT}} \ge 2.5\text{s}$) to filter click injection fraud

### 7. Budget Ceilings & FinOps Spend Circuit Breakers (`BUDGET-LOCK`)
- **Hard Daily Spend & API Caps**:
  - advertising campaigns and automated bidding engines enforce hard-coded daily budget caps at the API level
  - LLM content generation scripts enforce per-run token ceilings and max cost thresholds; script halts automatically upon reaching 80% of budget allocation
- **PromQL Operational Spend Alerts**:
  ```promql
  # CPA threshold breach alert
  rate(ad_spend_total[1h]) / rate(conversions_total[1h]) > 45.0
  ```

### 8. Legal Compliance & Platform Terms Review (`REVIEW-SYSTEM LOCK`)
- **Mandatory Escalation for Ad Review Evasion**:
  - any technique involving cloaking, deceptive traffic routing, or fingerprint spoofing intended to evade ad review, content moderation, or regulatory safety systems requires explicit written authorization and Security Engineer review
  - compliance boundaries from `core/policies/action-boundaries.yaml` strictly upheld; unauthorized destructive actions blocked fail-closed

### 9. Gate Review & Contract Conformance Verification Table
| Verification Gate | Target Invariant | Required Tool / Command | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Proxy Leak Audit** | 0 WebRTC/DNS leaks | `curl -sS https://browserleaks.com/ip` | Only proxy residential IP exposed |
| **JA4 TLS Parity** | Authentic Chrome signature | `curl_cffi --print-ja4 https://tls.peet.ws/` | Matches authentic browser JA4 hash |
| **True ROI Margin** | True ROI $\ge 25.0\%$ | Financial analytics reconciliation script | All 4 cost components accounted |
| **Thompson Sampling** | Cutoff at ROAS $< 0.75$ | Autonomous budget governor daemon | Underperforming adsets paused |
| **S2S Match Quality** | EMQ score $\ge 8.5$ | Meta / TikTok CAPI event audit tool | EMQ $\ge 8.5/10.0$; 0 duplicate fires |
| **1:1:1 Isolation** | 0 cross-profile overlap | Profile registry auditor script | 1 account : 1 VCC : 1 profile |
| **Fitts Trajectory** | Bézier curvature valid | Mouse telemetry analysis script | Smooth velocity curve; $MT > 150\text{ms}$ |
