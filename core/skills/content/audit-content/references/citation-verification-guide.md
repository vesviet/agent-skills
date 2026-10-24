# Citation Verification & Outbound Link Integrity Guide

Reference protocol for `audit-content` and the `content-manager` role. Provides systematic procedures to verify external link health, eliminate citation hallucination, and ensure claim-to-source fidelity.

---

## 1. Outbound Link Integrity Protocol

Every external link in an audited or refreshed article must undergo validation:

| Check | Requirement | Remediation Action |
| :--- | :--- | :--- |
| **HTTP Status Validation** | All external links must return HTTP `200 OK`. | Replace `404 Not Found`, `410 Gone`, or `5xx` dead links with the current authoritative canonical URL or Wayback Machine permalink. |
| **Redirect Resolution** | Zero chained redirects (`301` -> `302` -> destination). | Update the link directly to the final canonical destination URL. |
| **Anchor Hygiene** | Anchor text must clearly describe the target entity or documentation topic. | Replace generic anchors ("click here", "source", "link") with descriptive entity anchors ("PostgreSQL 17 Release Notes", "RFC 9110 HTTP Semantics"). |
| **Protocol & Security** | HTTPS mandatory. Prohibit tracking params, affiliate redirects, or URL shorteners. | Strip non-essential query parameters (`utm_*`, `ref`, `fbclid`) to preserve clean canonical link equity. |

---

## 2. Claim-to-Source Fidelity Verification

Citation hallucination occurs when an author or LLM includes a real, reachable link, but the underlying page does not substantiate the assertion made in the article.

### Verification Steps
1. **Primary Number Check**: If the article states "Redis achieves 120,000 QPS on a 4-core instance", navigate to the cited benchmark link and confirm the exact number, core count, and test parameters.
2. **Contextual Alignment**: Verify that the cited author's conclusion matches the article's usage (e.g., ensure a preliminary benchmark is not cited as a universal production guarantee).
3. **Publication Date Capture**: Record the publication or last-reviewed date of the source. If a technical claim cites a source older than 24 months, check for newer vendor updates or deprecations.
4. **Source Tiering Compliance**: Ensure material architectural claims rely on Tier 1 (official docs, RFCs, specs) or Tier 2 (audited benchmarks, peer-reviewed research) sources.

---

## 3. Citation Audit Checklist

- [ ] All external URLs return HTTP 200 OK without intermediate redirect chains
- [ ] Dead links (404/410) replaced with active canonical sources or Wayback permalinks
- [ ] Every quantitative claim (latencies, percentages, costs) is directly corroborated by its cited page
- [ ] Zero citation hallucinations (verified text matches claim)
- [ ] No tracking tokens or affiliate parameters in external URLs
- [ ] Outdated technical sources (>24 months) reviewed against latest software versions
