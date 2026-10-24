# Pillar-Cluster Architecture & Funnel Strategy Playbook

This playbook establishes architectural specifications for organizing domain content into authoritative hub-and-spoke pillar-cluster models, enforcing Silo internal link discipline, grounding topics in entity knowledge graphs, and balancing the TOFU/MOFU/BOFU audience journey.

---

## 1. Hub-and-Spoke Pillar-Cluster Architecture

Websites that publish unlinked, flat chronological articles dilute their topical authority across competing URLs. The **Pillar-Cluster Model** organizes content into tight semantic hierarchies that search engines and AI answer engines can easily crawl, index, and cite.

```
                           +------------------------+
                           |   CORE PILLAR PAGE     |
                           |  (Definitive Overview) |
                           +-----------+------------+
                                       |
          +----------------------------+----------------------------+
          |                            |                            |
          v                            v                            v
+-------------------+        +-------------------+        +-------------------+
|  CLUSTER SPOKE 1  |<======>|  CLUSTER SPOKE 2  |<======>|  CLUSTER SPOKE 3  |
| (Deep Sub-Intent) |        | (Deep Sub-Intent) |        | (Deep Sub-Intent) |
+-------------------+        +-------------------+        +-------------------+
```

### 1.1 Structural Specifications

| Architectural Component | Target Length | Keyword Intent & Search Volume | Semantic Scope |
| :--- | :--- | :--- | :--- |
| **Core Pillar Hub** | 3,000–5,000 words | Broad Informational / High Volume | Complete macro-entity breakdown; introduces every sub-topic and links to deep clusters |
| **Cluster Spokes (6–12 per Pillar)** | 1,500–2,500 words | Long-tail Informational & Commercial | Laser-focused deep dive into a single sub-intent, problem variant, or operational step |

---

## 2. Silo Internal Linking Topology & Governance Rules

Internal links transfer PageRank, communicate topical relationships, and prevent keyword cannibalization. To maintain topical relevance, implement strict **Silo Linking Topology**:

### 2.1 The Four Inviolable Silo Linking Rules

1. **Rule 1: Mandatory Upward Cluster-to-Pillar Links**:
   - Every Cluster Page must link up to its parent Pillar Page within the first 200 words of body copy.
   - Anchor text must use the exact or partial-match target entity of the Pillar (e.g., *"Read our complete guide to [distributed transaction architecture]"*). Generic anchors like *"click here"* or *"read more"* are strictly forbidden.

2. **Rule 2: Comprehensive Downward Pillar-to-Cluster Links**:
   - The Pillar Page must systematically link out to every child Cluster Page from its corresponding H2 or H3 section.
   - The Pillar serves as the authoritative switchboard for the topic.

3. **Rule 3: Horizontal Sibling Links Restrained to the Same Silo**:
   - Cluster Pages may cross-link to other Cluster Pages **only if** they belong to the same parent Pillar Silo.
   - **Cross-Silo Linking Restriction**: A Cluster Page in *Silo A (e.g., Database Indexing)* must never link directly to a Cluster Page in *Silo B (e.g., Kubernetes Ingress)*. Any cross-topic navigation must route up through *Pillar A* or *Pillar B*. This prevents semantic entropy and topical dilution.

4. **Rule 4: Zero Orphan Page Guarantee**:
   - Every published URL must possess at least **3 internal inbound links** from authoritative, contextual parent or sibling pages. Unlinked orphan pages are rejected during pipeline validation.

```
TOPOLOGY MATRIX:

[ Silo A: Database Optimization ]         [ Silo B: Kubernetes Networking ]
   Pillar A                                   Pillar B
    ├── Cluster A1 (B-Tree Indexes)            ├── Cluster B1 (Ingress Controllers)
    ├── Cluster A2 (Connection Pooling)        ├── Cluster B2 (Service Mesh mTLS)
    └── Cluster A3 (Vacuum Tuning)             └── Cluster B3 (Network Policies)

Allowed Links:
- Cluster A1 <---> Pillar A (Bidirectional)
- Cluster A1 <---> Cluster A2 (Sibling within same Silo)
- Pillar A   <---> Pillar B (Inter-pillar cross-reference)

Prohibited Links:
- Cluster A1  ---> Cluster B2 (Direct cross-silo cluster link — Dilutes semantic focus)
```

---

## 3. Entity Knowledge Graph Grounding

Search engines (Google Knowledge Graph) and Generative AI engines (Perplexity, ChatGPT, Claude) evaluate authority by mapping content to machine-readable entities rather than simple keyword frequencies.

### 3.1 Wikidata QID & Schema.org Mapping Protocol
Before finalizing any pillar or cluster brief, ground the primary topic in canonical knowledge graphs:

1. **Entity Identification**:
   - Search [Wikidata.org](https://www.wikidata.org) for the definitive entity identifier (e.g., PostgreSQL is `Q192490`; eBPF is `Q105972379`).
2. **Schema.org `@graph` Alignment**:
   - In the page JSON-LD metadata, declare the entity under `about` and `mentions`:
     ```json
     {
       "@context": "https://schema.org",
       "@type": "TechArticle",
       "headline": "Complete Architectural Guide to eBPF Kernel Tracing",
       "about": [
         {
           "@type": "Thing",
           "name": "Extended Berkeley Packet Filter",
           "sameAs": "https://www.wikidata.org/wiki/Q105972379"
         }
       ]
     }
     ```
3. **Entity Salience Density**:
   - Ensure the primary entity and its top 3 semantic co-occurrences (properties, creator, associated protocols) appear naturally in the opening section and H2 headers.

---

## 4. Audience Funnel Journey Mapping (TOFU / MOFU / BOFU)

A healthy content portfolio must not over-index on top-of-funnel traffic that never converts, nor bottom-of-funnel conversion pages that attract zero search volume. Maintain the **40 / 40 / 20 Portfolio Distribution**:

```
+---------------------------------------------------------------------------------------+
| PORTFOLIO FUNNEL BALANCE: 40% TOFU / 40% MOFU / 20% BOFU                              |
+---------------------------------------------------------------------------------------+
| [TOFU: 40% Awareness]     ==> Symptom queries, architectural foundations, guides      |
| [MOFU: 40% Consideration] ==> Vendor teardowns, architectural vs. comparisons, POCs   |
| [BOFU: 20% Decision]      ==> Migration playbooks, TCO calculators, enterprise specs  |
+---------------------------------------------------------------------------------------+
```

### 4.1 Funnel Stage Specifications

#### 1. TOFU (Top of Funnel - Awareness - 40% Target)
- **User Mindset**: Experiencing a technical symptom or researching an architectural concept; unaware of vendor solutions.
- **Search Query Formats**:
  - *"Why does PostgreSQL connection count spike during surges?"*
  - *"Understanding Linux epoll vs select I/O multiplexing"*
  - *"What is CSPF energy efficiency standard?"*
- **Primary KPIs**: Unique organic search visitors, total impressions, newsletter subscriptions, social shares.
- **Inter-Funnel Bridge**: Every TOFU article must feature a contextual bridge callout box leading to a comparative MOFU evaluation guide (e.g., *"Now that you understand connection pooling limits, compare the 3 primary pooling architectures"*).

#### 2. MOFU (Middle of Funnel - Consideration - 40% Target)
- **User Mindset**: Actively evaluating solution categories, comparing design patterns, or testing open-source frameworks.
- **Search Query Formats**:
  - *"PgBouncer vs Odyssey vs AWS RDS Proxy: Benchmark Comparison"*
  - *"Self-hosted ClickHouse vs Managed Snowflake for Time-Series"*
  - *"Astro vs Next.js for Cloudflare Pages Deployment"*
- **Primary KPIs**: Documentation views, CLI installations (`npm i` / `docker pull`), interactive tool uses, whitepaper downloads.
- **Inter-Funnel Bridge**: Interactive ROI calculators, feature matrices with direct migration checklists leading to BOFU decision pages.

#### 3. BOFU (Bottom of Funnel - Decision - 20% Target)
- **User Mindset**: Preparing to purchase, switch vendors, or commit production traffic to a specific platform.
- **Search Query Formats**:
  - *"Migrate from AWS RDS Proxy to Managed EdgeGate: Zero Downtime Step-by-Step"*
  - *"EdgeGate Enterprise Pricing, SLAs, and SOC 2 Compliance Specs"*
  - *"Datadog vs EdgeGate TCO at 100M Daily Events"*
- **Primary KPIs**: Self-service trial conversions, sales engineering call bookings, contract signings.
- **Conversion Elements**: Transparent pricing tables, enterprise security documentation, 1-click sandbox deploys, money-back guarantees.

---

## 5. Editorial Cadence & Capacity Scheduling

To sustain topical velocity without burning out engineering or editorial contributors, schedule releases according to maturity tiers:

| Site Maturity Stage | Total Publishing Cadence | TOFU / MOFU / BOFU Weekly Ratio | Review & Gate SLA |
| :--- | :--- | :--- | :--- |
| **Sprint / Launch (0–6 Months)** | 5 posts / week | 2 TOFU : 2 MOFU : 1 BOFU | 24-hour turnaround on Information Gain checks |
| **Growth / Expansion (6–18 Months)**| 3 posts / week | 1 TOFU : 1 MOFU : 1 BOFU | 48-hour turnaround; bi-weekly decay audits |
| **Mature / Authority (>18 Months)** | 1–2 posts / week | 50% New Content : 50% Decay Refresh | Monthly ROT audits; weekly AI share-of-voice checks |
