# Proxy Pool Rotation & Anti-Detect Infrastructure Specifications (2026)

## 1. Architecture: Isolated Proxy & Profile Topology

High-concurrency automation requires strict network and hardware fingerprint isolation. Shared proxy pools or leaky DNS servers immediately trigger anti-fraud graph clustering:

```
Automated Account Worker
           │
           ▼
Anti-Detect Browser (Camoufox / Chromium Stealth)
  - Isolated Canvas / WebGL fingerprint
  - Hardware Concurrency & AudioContext spoofing
           │
           ▼ (SOCKS5 with Remote DNS Resolution)
Dedicated Proxy Sidecar (WireGuard / Shadowsocks)
  - Enforces 1:1 Account-to-IP affinity
  - Rejects Datacenter ASNs (Residential & 4G Mobile only)
           │
           ▼
Residential Proxy Exit Gateway (p95 < 1200ms, Fraud Score <= 25)
```

## 2. Dynamic Health Probing & Quality Metrics

All proxy gateways undergo active background probing before traffic routing:
1. **Latency Ceiling**: P95 latency must remain $< 1200\text{ms}$. Spike above $2500\text{ms}$ triggers automated rerouting.
2. **Fraud & IP Quality Scoring**:
   - Query Scamalytics / IPQS APIs.
   - Fraud Score must be $\le 25$.
   - Flag `is_datacenter == true` triggers immediate rejection.
3. **Leakage Verification**:
   - WebRTC ICE Candidates: Must strictly emit the proxy exit IP. Zero host network interfaces exposed.
   - DNS Resolution: Remote exit node resolution only (`socks5h://`). Zero leaks to Google/Cloudflare/AWS datacenter DNS.

## 3. The 7-Stage Warmup Finite State Machine (FSM)

Ad accounts progress through a deterministic warmup state machine before high-velocity operations:
- `INITIALIZING` (Day 0): Profile creation, hardware fingerprint generation, IP validation.
- `PASSIVE_BROWSING` (Days 1–2): Top 500 news/editorial sites, natural mouse trajectories, cookie priming.
- `COOKIE_ACCUMULATION` (Days 3–4): E-commerce sites, cart additions, advertising pixel triggers.
- `INTERACTIVE_AUTH` (Day 5): SSO OAuth logins, 2FA registration, email confirmation loops.
- `ACTIVE_WARMUP` (Days 6–7): Platform likes, natural feed scrolls, low-velocity profile edits.
- `PRODUCTION_READY` (Day 8+): Full programmatic automation and campaign operations.
- `QUARANTINE`: Automatic fail-safe state triggered on CAPTCHA storms or account checkpointing.
