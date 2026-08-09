---
name: content-audit-refresh
description: 4-Sprint workflow for auditing, repairing schema, expanding content, and enforcing link topology for vesviet.
version: 1.0.0
roles:
  - seo-analyst
  - content-writer
  - content-manager
---

# Content Audit & Refresh Workflow (`vesviet`)

This workflow dictates the 4-sprint operational execution plan for resolving technical content debt on the `vesviet` site.

## 4-Sprint Timeline

### Sprint 1: Schema Repair & GEO Baseline
- **`seo-analyst`**: Identify all files missing mandatory schema fields (`tags`, `categories`, `cover`).
- **`content-writer`**: Add the `> **Answer-first:**` summary blocks to the top 50 performing posts.
- **`content-manager`**: Ensure 100% schema validation passes.

### Sprint 2: Content Refresh & Technical Depth
- **`content-writer`**: Expand all underperforming articles and series sub-articles (currently < 1,400 words).
- **Injection**: Add Go struct code, Kubernetes manifests, system design sequence diagrams, and benchmarks.
- **Verification**: Ensure all target posts now exceed the 1,400+ word baseline.

### Sprint 3: Link Topology & Orphan Elimination
- **`seo-analyst`**: Map the 124 orphan pages to the 10 Anchor Pillar Hubs.
- **`content-writer`**: Execute link injections from orphaned spokes up to the Hubs.
- **`content-manager`**: Re-architect `reading-map.md` into 6 curated visual learning paths. Diversify `hire.md` anchor texts.
- **Verification**: Crawler must report 0 orphan pages.

### Sprint 4: Consolidation & Redirects
- **`content-manager`**: Merge thin content (< 1,000w) into parent Series or monthly Tech Radar Digests.
- **`seo-analyst`**: Implement 301 Permanent Redirects via Hugo aliases and Cloudflare `_redirects` file.
- **Verification**: Run `hugo --gc --minify` to confirm zero build warnings or broken aliases.
