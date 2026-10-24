# Authentic Source Matrix & Empirical Proof Verification

Reference taxonomy and verification protocol for `write-article` and the `content-writer` role. Establishes a hierarchical credibility framework to ensure all factual claims, metrics, and architectural statements are grounded in verifiable primary evidence.

---

## 1. Three-Tier Source Credibility Taxonomy

Every material assertion in an article must trace to an acceptable tier in this credibility hierarchy. Citations from unverified sources result in gate failure.

| Source Tier | Classification | Permitted Sources | Prohibited Sources |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Primary)** | Source of Truth | Official vendor documentation, RFC / W3C / ISO engineering specs, reproducible open-source repos, firsthand production telemetry, kernel traces, verified schema definitions. | Unattributed release notes, marketing landing pages without technical specs. |
| **Tier 2 (Authoritative Secondary)** | Validated Industry Evidence | Peer-reviewed academic papers, verified industry benchmarks (DORA, CNCF, IEEE), named SME interviews with verifiable LinkedIn/GitHub credentials, audited security audits. | Anonymous quotes, unverified sponsored whitepapers without methodology disclosure. |
| **Tier 3 (Contextual)** | Industry Discourse | Established technology journalism (e.g., Ars Technica, IEEE Spectrum), senior engineering blogs with named authors and code samples. | Aggregator listicles, AI-synthesized roundups, anonymous forum posts, scraper blogs. |

---

## 2. Mandatory Empirical Proof Standards

Technical and architectural articles must contain **at least two distinct empirical proof types** to substantiate claims:

1. **Production Telemetry / Benchmarks**: Quantified latency (p50/p95/p99), CPU/memory utilization, throughput numbers (RPS/QPS), or error rate deltas before and after an optimization.
2. **Reproduction Logs / Traces**: Exact console outputs, stack traces, compiler errors, network packet dumps, or `strace` logs confirming runtime behavior.
3. **Reproducible Code Repos**: Minimal, reproducible exemplars (MRE) with explicit dependencies, lockfiles, and instructions to execute locally.
4. **C2PA / Firsthand Media**: Original screenshots, architecture diagrams with author provenance, or C2PA-verified media.

---

## 3. Citation Formatting & Verification Protocol

When citing data or claims:
- **Exact Attribution**: Always cite the original author, publishing organization, and year/month of publication (e.g., "According to the 2026 CNCF Annual Survey (published March 2026)...").
- **Canonical Outbound Link**: Link directly to the primary permalink; never link through affiliate redirects or intermediate aggregators.
- **Contextual Claim Bracket**: Ensure the sentence immediately preceding or following the link isolates the exact factual takeaway so automated AI search crawlers can parse the attribution cleanly.
- **Unverified Flagging**: If a claim cannot be verified against Tier 1 or Tier 2 sources, mark it as `[UNVERIFIED - REQUIRES BENCHMARK]` and do not publish until validated.
