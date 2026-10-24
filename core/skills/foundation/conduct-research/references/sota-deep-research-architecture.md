# SOTA Deep Research Architecture: 2026–2027 Engineering Standard

**Document ID**: `REF-RESEARCH-SOTA-2026`  
**Classification**: Engineering Architecture Standard & Reference Dossier  
**Target Release**: Canonical `agent-skills` v5.6.0 & Downstream DMS `.agents` v2.12.0  
**Owning Role**: `@researcher` (Principal Technical Researcher)  
**Companion Skill**: `conduct-research` (`core/skills/foundation/conduct-research/SKILL.md`)  
**Data Contract**: `contracts/schemas/research-report.json` (Draft 2020-12)  
**Associated Checklist**: `core/roles/references/researcher-review-checklist.md`

---

## Executive Summary

Autonomous AI research agents in 2026–2027 face an epistemic crisis: the recursive saturation of the open web with synthetic, ungrounded AI summaries. Naive search-and-summarize workflows generate circular hallucination cascades ($A \rightarrow B \rightarrow A$) and deliver diluted, low-density prose. 

This reference dossier establishes the state-of-the-art (SOTA) deep research engineering standard for the agent ecosystem. It formalizes four mandatory architectural pillars:
1. **Stanford STORM Architecture**: Multi-perspective persona discovery (Skeptical Auditor, Compliance Reviewer, Domain Specialist, Technical Architect) and 5-turn simulated conversational interviews prior to query formulation.
2. **Citation Directed Acyclic Graph (DAG)**: Mathematical topological representation $G = (V, E)$ enforcing strict acyclicity ($\text{Cycle}(G) = \emptyset$) via 3-color Depth-First Search (DFS), zero-AI-primary citation locks, and multi-source triangulation ($\ge 3$ independent primary records).
3. **Chain-of-Verification (CoVe) & C2PA Provenance**: Atomic claim decomposition ($P_{\text{claim}} = \bigwedge p_j$), isolated query execution against original primary documents, structured verification matrix evaluation (`verified`, `refuted`, `unverifiable`), and C2PA Content Credentials / watermark cryptographic inspection.
4. **Quantitative Information Density (ID)**: Exact mathematical ratio $\text{ID} = \frac{N_{\text{Named Entities}} + N_{\text{Quantified Metrics}}}{N_{\text{Total Words}}} \ge 0.12$ paired with rigorous fluff elimination rules.

All autonomous research artifacts emitted across the canonical framework and downstream bundles must satisfy these mathematical and procedural constraints.

---

## 1. The AI-Saturated Information Crisis & Epistemic Collapse

### 1.1 The Synthetic Echo Chamber Dilemma

Between 2023 and 2026, the volume of synthetic, machine-generated web content increased by an order of magnitude. Search engine results pages (SERPs) are dominated by SEO-optimized content farms that ingest model summaries and republish paraphrased variants. When an autonomous research agent queries the web and treats commodity search snippets or AI overviews as authoritative evidence, it enters a closed synthetic feedback loop:

$$\text{Agent Model } M_1 \xrightarrow{\text{generates}} \text{Synthetic Web Content } S_1 \xrightarrow{\text{indexed by}} \text{Search Engine} \xrightarrow{\text{retrieved by}} \text{Agent Model } M_2 \xrightarrow{\text{synthesizes}} S_2$$

This creates circular citation chains where Claim $A$ cites Secondary Source $B$, Source $B$ cites Blog $C$, and Blog $C$ cites an earlier synthetic generation of Claim $A$ ($A \rightarrow B \rightarrow C \rightarrow A$). In this environment, consensus does not indicate truth; it indicates algorithmic replication.

### 1.2 The Hallucination Cascade in Agentic Systems

In multi-agent architectures, epistemic errors are catastrophic. If the `@researcher` accepts an unverified hallucination (such as a fictitious API parameter, a non-existent regulatory exemption, or an unbenchmarked throughput metric), that finding is codified into `research-report.json`. Downstream agents accept this input as ground truth:
- The `@technical-architect` designs system blueprints around invalid interfaces.
- The `@business-analyst` authors feature tickets with flawed regulatory premises.
- The `@backend-developer` writes integration code against hallucinated protocols.

The error compounds across agent boundaries, leading to complete project failure.

### 1.3 The Mandate for Formal Grounding

To guarantee epistemic integrity, research workflows must transition from probabilistic heuristic summarization to formal, verifiable methods:
- **Topological Invariants**: Citation structures must be mathematically represented and validated as directed acyclic graphs.
- **Source Quarantine**: Generative AI tools are quarantined strictly to query formulation and topic exploration; they are prohibited from serving as primary or secondary evidentiary citations.
- **Atomic Disaggregation**: Compound factual statements must be factored into discrete propositions and individually evaluated against human-authored primary artifacts.
- **Cryptographic Provenance**: Digital assets must be validated through PKI signatures and digital watermarking standards.
- **Information Density Enforcement**: Verbal padding and boilerplate transitions must be algorithmically measured and rejected.

---

## 2. Stanford STORM Architecture & Persona Discovery Protocol

### 2.1 Theoretical Foundations

The STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Questioning) framework, pioneered by Stanford University researchers (NAACL 2024 / arXiv:2402.14207), demonstrates that pre-synthesis perspective modeling significantly outperforms standard retrieval-augmented generation (RAG). 

Single-prompt or single-angle research invariably exhibits confirmation bias: the agent searches for terms affirming its initial framing and synthesizes generic, consensus-weighted responses. STORM mitigates this by decomposing the research objective through automated persona discovery and simulated multi-turn expert interviews before issuing authoritative search queries.

```
       ┌────────────────────────────────────────────────────────┐
       │                Research Objective & Topic              │
       └───────────────────────────┬────────────────────────────┘
                                   │
               [Persona Discovery Engine: 4 Orthogonal Experts]
                                   │
       ┌───────────────┬───────────┴───────────┬────────────────┐
       ▼               ▼                       ▼                ▼
┌─────────────┐ ┌─────────────┐         ┌─────────────┐  ┌─────────────┐
│  Skeptical  │ │ Compliance  │         │   Domain    │  │  Technical  │
│   Auditor   │ │  Reviewer   │         │ Specialist  │  │  Architect  │
└──────┬──────┘ └──────┬──────┘         └──────┬──────┘  └──────┬──────┘
       │               │                       │                │
       └───────────────┴───────────┬───────────┴────────────────┘
                                   │
                 [5-Turn Simulated Conversational Interview]
                                   │
       ┌───────────────────────────┴────────────────────────────┐
       ▼                                                        ▼
┌───────────────────────────────┐        ┌─────────────────────────────┐
│  Extracted Empirical Queries  │        │  Hierarchical Research DAG  │
│   (Targeted Primary Probes)   │        │     (Dependency Outline)    │
└───────────────────────────────┘        └─────────────────────────────┘
```

### 2.2 Automated Persona Discovery Mechanics

Prior to executing any external search queries, the `@researcher` inspects the research prompt and instantiates four mandatory expert personas. Each persona is assigned a strict analytical stance, core focus areas, and falsification targets:

| Persona | Operational Stance | Core Analytical Focus | Mandatory Falsification Targets |
| :--- | :--- | :--- | :--- |
| **Skeptical Auditor** | Adversarial, falsification-driven | Hidden trade-offs, stress limits, vendor lock-in, circular citations, unproven claims | Marketing claims, unverified performance benchmarks, single-source dependencies |
| **Compliance Reviewer** | Statutory, regulatory, legal | EU AI Act (Reg 2024/1689), GDPR, TCVN, ISO/IEC standards, auditability, legal liabilities | Ambiguous licensing, undocumented data handling, missing regulatory notifications |
| **Domain Specialist** | Empirical, operational | Field benchmarks, p99 latencies, real-world failure modes, tooling ergonomics, edge cases | Idealized lab benchmarks, synthetic toy examples, unversioned API guides |
| **Technical Architect** | Structural, systems-engineering | Graph topology, interface contracts, computational complexity ($O(n)$), blast radius, backwards compatibility | Breaking schema changes, cyclic dependencies, unbounded resource consumption |

#### Dynamic Persona Specialization
While the four base personas are universal, their internal inquiry templates must be dynamically parameterized based on the domain:
- **Logistics & Supply Chain**: Persona focuses on WMS/TMS integrations, pallet throughput, Cold Chain compliance, TCVN warehouse standards, and ERP message brokers.
- **Distributed Systems / Database**: Persona focuses on Raft consensus partition behavior, MVCC snapshot isolation anomalies, p99 tail latency, and POSIX memory semantics.
- **Cybersecurity & Cryptography**: Persona focuses on PKI revocation models, side-channel vulnerabilities, zero-trust attestation, and C2PA manifest tampering.

### 2.3 The 5-Phase Simulated Conversational Interview

The agent executes a structured 5-turn simulated dialogue between a Perspective-Guided Questioner (playing each persona) and an Information Provider (equipped with code and document retrieval tools):

1. **Turn 1 — Perspective Stance Declaration**:
   - Each persona articulates its unique angle, boundary constraints, and 3–5 targeted inquiry vectors.
   - *Example (Skeptical Auditor)*: "I am probing Redis 7.4 Lua script fencing. I will not accept marketing claims of 'high reliability.' I demand to see the exact fencing token propagation mechanism and split-brain partition behavior."

2. **Turn 2 — Multi-Turn Inquiry Execution**:
   - The persona poses detailed, technically probing questions to the Information Provider.
   - Questions must target implementation mechanics rather than high-level definitions.
   - *Example*: "When a network partition isolates the Redis master, how does Lua script execution interact with `min-replicas-to-write`? Does an in-flight script receive an `ETIMEDOUT` or does it execute partially?"

3. **Turn 3 — Iterative Query Extraction**:
   - The dialogue identifies specific information voids. Instead of querying "Redis 7.4 features", the agent generates targeted empirical query strings:
     - `redis 7.4 lua script fencing token split brain behavior POSIX`
     - `site:redis.io/docs/ "min-replicas-to-write" script failure semantics`
     - `github.com/redis/redis commit "script fencing"`

4. **Turn 4 — Adversarial Challenge & Evidence Filtering**:
   - If the Information Provider returns marketing copy, SEO blog summaries, or ungrounded claims, the persona explicitly rejects the evidence:
     - *Rejection Log*: `[REJECT: Marketing copy from vendor site without reproducible benchmark harness. Re-querying repository commit logs.]`

5. **Turn 5 — Outline Construction & Synthesis**:
   - The findings across all four persona interviews are synthesized into a hierarchical research outline where each section is bound to explicit node dependencies and verification criteria.

---

## 3. Citation Directed Acyclic Graph (DAG) Topology

### 3.1 Mathematical Formulation

Let the citation graph be formalized as a finite directed graph:

$$G = (V, E)$$

where the vertex set $V$ is partitioned into three disjoint subsets:

$$V = V_{\text{claim}} \cup V_{\text{source}} \cup V_{\text{evidence}}$$

- **$V_{\text{claim}}$ (Propositional Claims)**: The set of discrete assertions, conclusions, or inferences formulated in the research synthesis.
- **$V_{\text{source}}$ (Grounding Sources)**: The set of external, human-authored documents, standards, or repositories (URLs, RFC numbers, commit SHAs).
- **$V_{\text{evidence}}$ (Extracted Artifacts)**: Specific verbatim snippets, data tables, or cryptographic tokens extracted from a source that ground a claim.

The directed edge set $E \subseteq V \times V$ consists of ordered pairs $(u, v)$ denoting directed epistemic dependencies:

$$e = (u, v) \in E \implies u \text{ depends on, cites, or is grounded by } v$$

#### Directed Edge Semantics
Every edge $e \in E$ is typed and weighted:
- `cites` ($V_{\text{claim}} \to V_{\text{source}}$): A claim directly asserts factual grounding in an external source.
- `corroborates` ($V_{\text{source}} \to V_{\text{claim}}$ or $V_{\text{source}} \to V_{\text{source}}$): An independent source confirms the proposition asserted in a claim or another source.
- `derives_from` ($V_{\text{claim}} \to V_{\text{claim}}$): A higher-level inference is logically deduced from lower-level verified claims.
- `contradicts` ($V_{\text{source}} \to V_{\text{claim}}$ or $V_{\text{source}} \to V_{\text{source}}$): Evidence directly conflicts with an assertion or another source.

### 3.2 The Strict Acyclicity Invariant

The fundamental invariant of the citation network is mathematical acyclicity:

$$\forall v \in V, \quad \text{Path}(v \leadsto v) = \emptyset \iff \text{Cycle}(G) = \emptyset$$

A cycle in $G$ represents circular reasoning, an epistemic feedback loop, or synthetic echo chamber amplification. Any research artifact whose citation graph contains a cycle is rejected fail-closed.

#### Edge Validation Constraints
1. **Self-Loop Invariant**: No node may cite itself:
   $$\forall u \in V, \quad (u, u) \notin E$$
2. **Endpoint Existence Invariant**: Every edge must connect defined nodes:
   $$\forall (u, v) \in E, \quad u \in V \land v \in V$$
3. **Weight Bound**: Edge weights representing corroboration confidence must be bounded:
   $$\forall e \in E, \quad w(e) \in [0.0, 1.0]$$

### 3.3 Topological Cycle Detection Algorithm (3-Color DFS)

To enforce acyclicity deterministically, citation graphs are evaluated using a 3-color Depth-First Search (DFS) algorithm. Nodes are classified into three disjoint states:
- **White (Color 0)**: Unvisited node.
- **Gray (Color 1)**: Node currently being processed in the active recursion call stack. A directed traversal encountering a Gray node detects a back-edge, proving the existence of a directed cycle.
- **Black (Color 2)**: Node completely explored, including all reachable descendants.

```
       [Start DFS at White Node u]
                    │
                    ▼
          [Mark Node u as Gray (1)]
          [Push u to Recursion Stack]
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  [Traverse Edge (u, v)]   [All Out-Edges Visited?]
        │                       │
 ┌──────┴──────┐                ▼
 │ State of v? │        [Mark Node u as Black (2)]
 └──────┬──────┘        [Pop u from Recursion Stack]
        │                       │
 ┌──────┼──────────────┐        ▼
 ▼      ▼              ▼      [Return Acyclic]
[White] [Gray]      [Black]
 (0)     (1)          (2)
  │       │            │
  │  [CYCLE FOUND!]  [Ignore: Cross/Forward Edge]
  │  [Return Cycle]
  │
[Recursive Call: DFS(v)]
```

#### Time and Space Complexity
- Time Complexity: $O(|V| + |E|)$
- Space Complexity: $O(|V|)$ for the recursion stack and color array.

### 3.4 Zero-AI-Primary Source Citation Lock (`ZERO-AI-PRIMARY-CITATION-LOCK`)

Research graphs enforce a strict 4-tier source taxonomy. Autonomous research agents are prohibited from citing synthetic AI outputs as primary or secondary sources:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Tier 1: Primary Evidence (Citable — Highest Authority)                 │
│ - Peer-reviewed academic journals, official RFCs, statutory gazettes   │
│ - Source code repositories (commit SHAs), live hardware benchmarks     │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 2: Secondary Evidence (Citable with Methodological Context)       │
│ - Audited industry whitepapers, vendor architectural documentation     │
│ - Verified engineering blogs with reproducible code repositories       │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 3: Tertiary Reference (Orientation & Discovery Only — Not Citable)│
│ - Wikipedia, community wikis, uncurated aggregators                    │
├────────────────────────────────────────────────────────────────────────┤
│ Tier 4: Generative AI Outputs (QUERY-ONLY LOCK — NEVER CITABLE)        │
│ - ChatGPT, Perplexity, Gemini, Google AI Overviews, Claude summaries   │
│ - RULE: Use solely for query brainstorming; never appear as V_source   │
└────────────────────────────────────────────────────────────────────────┘
```

If an agent attempts to insert an AI tool into $V_{\text{source}}$, the validation engine triggers an immediate schema violation: `[ERROR: ZERO-AI-PRIMARY-CITATION-LOCK violated. AI-generated source cannot ground factual claims.]`

### 3.5 Multi-Source Empirical Triangulation

For critical technical benchmarks, architectural limits, and regulatory interpretations, single-source grounding is insufficient. The research standard mandates empirical triangulation across at least **three independent, non-affiliated primary sources**:

$$\text{Triangulated}(c) \iff |\{s \in \text{PrimarySources}(c) \mid \text{Affiliation}(s) \text{ is pairwise disjoint}\}| \ge 3$$

#### Disjoint Affiliation Rule
Sources are independent if and only if they share no corporate parent, joint venture funding, shared authorship, or syndication relationship. For example, three tech blogs republishing the same vendor press release constitute $N=1$ independent source, not $N=3$.

### 3.6 Contradiction Preservation Protocol

In commodity research, conflicting data points are often smoothed over or averaged out to present a false consensus. In SOTA Deep Research, contradictions are first-class architectural entities:
- Conflicting primary sources are modeled in $G$ using divergent edges:
  $$(s_1, c_1) \in E \quad \text{and} \quad (s_2, c_2) \in E \quad \text{with} \quad (c_1, c_2) \in E_{\text{contradicts}}$$
- The synthesis must document the exact operational variables (OS kernel version, hardware harness, benchmark concurrency) explaining the variance.
- If the contradiction cannot be resolved empirically, it is surfaced as an open risk in `synthesis.triangulation.unresolved_contradictions`.

---

## 4. Chain-of-Verification (CoVe) & Multi-Layer Digital Provenance

### 4.1 Theoretical Foundations of CoVe

Chain-of-Verification (Meta AI, 2023 / arXiv:2309.11495) addresses the phenomenon of self-delusion in generative models: when an LLM writes a compound narrative paragraph, earlier generated hallucinated clauses bias subsequent clauses.

CoVe forces a structural decoupling between claim drafting and claim verification. By factoring a draft synthesis into atomic assertions and querying each assertion in total isolation, confirmation bias is eliminated.

```
       ┌────────────────────────────────────────────────────────┐
       │                 Draft Synthesis Claim                  │
       │   "Redis 7.4 supports Lua fencing and hits 610k TPS"   │
       └───────────────────────────┬────────────────────────────┘
                                   │
               [Step 1: Atomic Proposition Factorization]
                                   │
       ┌───────────────────────────┴────────────────────────────┐
       ▼                                                        ▼
┌─────────────────────────────────┐      ┌──────────────────────────────────┐
│ Proposition p1:                 │      │ Proposition p2:                  │
│ "Redis 7.4 supports Lua fencing"│      │ "Redis 7.4 hits 610k TPS"        │
└──────────────┬──────────────────┘      └──────────────┬───────────────────┘
               │                                        │
 [Step 2: Isolated Query Generation]      [Step 2: Isolated Query Generation]
               │                                        │
               ▼                                        ▼
┌─────────────────────────────────┐      ┌──────────────────────────────────┐
│ Query: "Redis 7.4 Lua script    │      │ Query: "Redis 7.4 standalone TPS │
│ fencing tokens documentation"   │      │ benchmark Graviton3 hardware"    │
└──────────────┬──────────────────┘      └──────────────┬───────────────────┘
               │                                        │
 [Step 3: Primary Document Retrieval]     [Step 3: Primary Document Retrieval]
               │                                        │
               ▼                                        ▼
┌─────────────────────────────────┐      ┌──────────────────────────────────┐
│ Primary Doc: redis.io release   │      │ Primary Doc: Bench results show  │
│ confirms script fencing feature │      │ 240k TPS (not 610k TPS)          │
└──────────────┬──────────────────┘      └──────────────┬───────────────────┘
               │                                        │
 [Step 4: Status Evaluation]              [Step 4: Status Evaluation]
               │                                        │
               ▼                                        ▼
┌─────────────────────────────────┐      ┌──────────────────────────────────┐
│ Status: [verified]              │      │ Status: [refuted]                │
│ Action: Retain in synthesis     │      │ Action: Revise draft to 240k TPS │
└─────────────────────────────────┘      └──────────────────────────────────┘
```

### 4.2 The 4-Step CoVe Execution Protocol

1. **Step 1: Baseline Hypothesis Formulation**:
   - The agent drafts the substantive finding based on initial multi-hop retrieval.

2. **Step 2: Atomic Proposition Decomposition**:
   - The finding is decomposed into a conjunction of atomic propositions:
     $$P_{\text{claim}} = \bigwedge_{j=1}^m p_j$$
   - Each proposition $p_j$ must contain exactly one subject, one predicate, and one quantifiable object or constraint. Compound clauses containing "and", "due to", or "resulting in" must be factored into separate propositions.

3. **Step 3: Isolated Verification Querying**:
   - For each proposition $p_j$, the agent generates an independent verification question $Q_j$ and an isolated query string.
   - **Context Quarantine Rule**: The query formulation prompt must receive *only* proposition $p_j$. It must not receive the surrounding draft narrative or other propositions. This prevents prompt leakage from inducing confirmation bias.

4. **Step 4: Verification Status Matrix Assignment**:
   - The retrieved primary document evidence is audited against $p_j$:
     - `verified`: The primary document explicitly corroborates the proposition with identical or more stringent metrics.
     - `refuted`: The primary document directly contradicts the proposition. The synthesis draft must be amended immediately to reflect reality.
     - `unverifiable`: The primary document is inaccessible (e.g. 404, paywall) or does not mention the specific metric. The claim is auto-demoted to `[UNVERIFIED]`.

### 4.3 CoVe Verification Matrix Specification

The results of the CoVe process must be serialized into the structured data contract under `cove_verification_matrix`:

```json
{
  "total_claims_assessed": 2,
  "verified_claims_count": 1,
  "refuted_claims_count": 1,
  "unverifiable_claims_count": 0,
  "matrix": [
    {
      "claim_id": "claim_redis_fencing",
      "atomic_proposition": "Redis 7.4 supports Lua script engine fencing tokens.",
      "verification_question": "Does Redis 7.4 implement fencing tokens for Lua script execution?",
      "isolated_query_used": "Redis 7.4 Lua script fencing tokens official documentation",
      "primary_source_urls": ["https://raw.githubusercontent.com/redis/redis/7.4/00-RELEASENOTES"],
      "verification_status": "verified",
      "confidence_score": "High",
      "c2pa_provenance_checked": false,
      "c2pa_status": "not_applicable"
    },
    {
      "claim_id": "claim_redis_throughput",
      "atomic_proposition": "Redis 7.4 achieves 610k TPS on AWS Graviton3 c7g.2xlarge hardware.",
      "verification_question": "What is the measured standalone redis-benchmark throughput on AWS c7g.2xlarge?",
      "isolated_query_used": "Redis 7.4 benchmark AWS c7g.2xlarge throughput TPS",
      "primary_source_urls": ["https://redis.io/blog/redis-7-4-performance-benchmarks/"],
      "verification_status": "refuted",
      "confidence_score": "High",
      "c2pa_provenance_checked": false,
      "c2pa_status": "not_applicable"
    }
  ]
}
```

### 4.4 C2PA Cryptographic Content Credentials & Provenance

In 2026–2027, multimodal evidence (architecture diagrams, system topology charts, benchmark screenshots, and executive PDFs) frequently incorporates generative AI or edited artifacts. To verify media authenticity, autonomous research agents integrate the Coalition for Content Provenance and Authenticity (C2PA Technical Specification v1.3 / ISO/IEC 23000-22).

#### The C2PA Manifest Architecture
A C2PA-compliant asset embeds an authenticated JUMBF (JPEG Universal Metadata Box Format) container containing:
1. **Assertions**: Claims regarding asset creation (author identity, hardware camera/capture details, software edits).
2. **Hard Bindings**: Cryptographic SHA-256 hashes of the underlying asset bytes.
3. **Signatures**: Digital signatures executed using an X.509 PKI certificate chain rooted in an authoritative Certificate Authority (CA) trust list.

```
┌────────────────────────────────────────────────────────┐
│ Digital Asset (PNG, WebP, PDF)                         │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Raw Media Stream (Pixels / Bitstream)              │ │
│ └────────────────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────────────────┐ │
│ │ JUMBF Container (C2PA Manifest Box)                │ │
│ │  - Assertion: "created_by_author: @tech-lead"      │ │
│ │  - Assertion: "software_agent: drawio-cli v24.1"   │ │
│ │  - Hard Binding: SHA256(Raw Media Stream)          │ │
│ │  - PKI Signature: Signed by Root CA X.509 Cert     │ │
│ └────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

#### Inspection and Verification Protocol
When a research artifact includes or references digital media evidence, the agent invokes `c2patool`:

```bash
c2patool inspect diagram.png --detailed
```

The resulting manifest is evaluated against the following state machine:
- `signed_valid`: Cryptographic signature is intact, certificate chains to an audited root CA, and SHA-256 hash matches the media bytes.
- `watermark_detected`: Latent statistical or transform-domain watermarking (such as Google DeepMind SynthID, Digimarc, or C2PA synthetic metadata tags) indicates AI generation. The asset is labeled as synthetic.
- `unverified_provenance`: The asset lacks a valid C2PA manifest or the signature is broken. Absence of credentials does not prove fraud, but the asset cannot be granted Tier 1 credibility. It is marked `[UNVERIFIED — provenance not established]`.
- `not_applicable`: Pure textual artifacts or raw source code files where C2PA metadata is not supported.

---

## 5. Quantitative Information Density (ID) & Anti-Fluff Governance

### 5.1 The Mathematical Formulation

Large Language Models naturally drift toward verbose, low-entropy phrasing ("delve into", "pave the way", "crucial cornerstone in the modern landscape"). This conversational fluff obscures factual gaps and dilutes technical precision.

The SOTA Deep Research standard enforces a strict quantitative Information Density threshold:

$$\text{ID} = \frac{N_{\text{Named Entities}} + N_{\text{Quantified Metrics}}}{N_{\text{Total Words}}} \ge 0.12$$

Any substantive synthesis section in `research-report.json` or research markdown briefs that fails to achieve $\text{ID} \ge 0.12$ is rejected fail-closed during automated linting.

### 5.2 Formal Taxonomical Extraction Rules

#### 1. Named Entities ($N_{\text{Named Entities}}$)
A recognized named entity must represent a concrete, formal, real-world identifier:
- **Capitalized Proper Technical Nouns**: `PostgreSQL`, `Kubernetes`, `Kafka`, `Redis`, `Linux Kernel`.
- **Formal Engineering & Safety Standards**: `TCVN 7830:2021`, `ASHRAE 55-2023`, `RFC 9110`, `ISO/IEC 42001`, `IEEE 802.11ax`.
- **Statutory Frameworks & Regulations**: `EU AI Act (Regulation 2024/1689)`, `GDPR Article 17`, `Decree 13/2023/ND-CP`.
- **Specific Hardware Models & Microarchitectures**: `AWS Graviton3`, `Intel Xeon Platinum 8480+`, `NVIDIA H100 SXM5`, `Hioki PW3338`.
- **Standardized Cryptographic / Protocol Identifiers**: `ECDSA P-256`, `SHA-256`, `POSIX shm`, `JUMBF`, `gRPC`.

*Exclusions*: Generic domain words (e.g., "software", "database", "system", "architecture", "microservice") do NOT count as named entities.

#### 2. Quantified Metrics ($N_{\text{Quantified Metrics}}$)
A quantified metric must consist of a numerical value bound to a measurement unit or benchmark dimension:
- **Latencies & Timestamps**: `0.15ms`, `12.4μs`, `420ms`, `2026-10-23T02:00:00Z`.
- **Throughput & Bandwidth Rates**: `610k TPS`, `1.2 GB/s`, `10 Gbps`, `4,500 req/sec`.
- **Percentages & Ratios**: `99.999%`, `0.12`, `14.2%`, `15x`.
- **Memory & Storage Capacities**: `64 GB`, `512 MiB`, `2 TB`, `4 KB page`.
- **Physical Quantities**: `250W TDP`, `3.2 GHz`, `45 dBA`, `24°C`.

*Exclusions*: Standalone numbers without units or context (e.g., "step 1", "two factors") do NOT count as quantified metrics.

#### 3. Total Words ($N_{\text{Total Words}}$)
The count of whitespace-delimited tokens in substantive narrative paragraphs (excluding markdown headers, code block syntax markers, and table delimiters).

### 5.3 Concrete Calculation Examples

#### Negative Example (Low Density — REJECTED):
> *"In today's fast-paced digital world, it is vital to delve into database technologies to ensure high performance. Modern systems must pave the way for cutting-edge solutions that can help businesses grow effectively. By adopting reliable storage tools, engineers can unlock significant value and improve overall scalability."*
- Words: 44
- Named Entities: 0
- Quantified Metrics: 0
- $\text{ID} = \frac{0 + 0}{44} = 0.00 < 0.12 \implies$ **FAIL (Fluff detected)**

#### Positive Example (High Density — PASSED):
> *"Redis 7.4 deployed on AWS Graviton3 c7g.2xlarge running Linux Kernel 6.8 achieves 240k TPS under redis-benchmark with 50 concurrent connections, bounding p99 tail latency to <= 0.18ms while consuming 512 MiB of POSIX shm memory."*
- Words: 33
- Named Entities: `Redis 7.4`, `AWS Graviton3`, `c7g.2xlarge`, `Linux Kernel 6.8`, `redis-benchmark`, `POSIX shm` ($N_{\text{NE}} = 6$)
- Quantified Metrics: `240k TPS`, `50 concurrent connections`, `<= 0.18ms`, `512 MiB` ($N_{\text{QM}} = 4$)
- Total Tokens: $N_{\text{NE}} + N_{\text{QM}} = 10$
- $\text{ID} = \frac{10}{33} \approx 0.303 \ge 0.12 \implies$ **PASS (High-signal technical brief)**

### 5.4 The 4 Anti-Fluff Governance Rules

1. **Rule 1 — Absolute Ban on Conversational Clichés**:
   - The phrases *"delve into"*, *"pave the way"*, *"testament to"*, *"in today's world"*, *"crucial cornerstone"*, *"game changer"*, and *"revolutionize"* are strictly forbidden. Research containing these phrases is rejected during linting.
2. **Rule 2 — Elimination of Weak Modals and Speculative Hedges**:
   - Phrases such as *"might potentially be able to"*, *"could perhaps consider"*, and *"it is widely believed"* must be replaced with empirical data or labeled explicitly as `[INFERENCE]`.
3. **Rule 3 — Fact Packing & Noun-Phrase Density**:
   - Every sentence must assert an empirical constraint, a verifiable benchmark, an interface contract, or an architectural trade-off. Sentences serving purely as narrative bridges must be pruned.
4. **Rule 4 — Actionable Operational Specificity**:
   - Recommendations must specify exact file paths, environment variables, configuration parameters, or CLI flags.

---

## 6. Machine Handoff & Contract Delivery

### 6.1 Draft 2020-12 `research-report.json` Specification

Autonomous research is not delivered as conversational prose; it is delivered as a typed, machine-validating data contract conforming to JSON Schema Draft 2020-12.

The contract specifies top-level fields ensuring seamless programmatic consumption:

| Top-Level Property | JSON Type | Mandatory Invariant |
| :--- | :--- | :--- |
| `contract_type` | `string` | Must be `"research-report"` |
| `objective` | `string` | Clear description of research problem |
| `execution_metrics` | `object` | `depth_mode` (`"deep"` requires $\ge 10$ rounds; `"scoped"` requires $\ge 3$ rounds and `scope_waiver_note`) |
| `citation_dag` | `object` | `is_acyclic: true`, `cycle_check_algorithm: "dfs_three_color"`, `nodes` ($\ge 1$), `edges` |
| `cove_verification_matrix` | `object` | `total_claims_assessed`, `verified_claims_count`, `matrix` ($\ge 1$ atomic proposition) |
| `information_density` | `object` | `density_score` ($\ge 0.12$), `status: "passed"` |
| `synthesis` | `object` | `key_findings`, `critical_gaps`, `confidence_score` (`"High"`, `"Medium"`, `"Low"`) |
| `raw_data_references` | `array` | $\ge 1$ source item; each source must specify `url`, `credibility` (Tier 1–3), and `source_type` |
| `recommended_next_roles` | `array` | $\ge 1$ role item with `role` and `rationale` |

### 6.2 Downstream Agent Handshake Protocol

When `@researcher` completes an investigation, the resulting contract routes to downstream roles without manual intervention:

```
                          ┌─────────────────────────────┐
                          │    research-report.json     │
                          │   (Draft 2020-12 Contract)  │
                          └──────────────┬──────────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 │                       │                       │
                 ▼                       ▼                       ▼
   ┌───────────────────────────┐ ┌───────────────┐ ┌───────────────────────────┐
   │   @technical-architect    │ │ @business-    │ │      @content-writer      │
   │                           │ │  analyst      │ │                           │
   │ Ingests:                  │ │ Ingests:      │ │ Ingests:                  │
   │ - citation_dag            │ │ - key_findings│ │ - verified findings       │
   │ - empirical benchmarks    │ │ - critical_gaps│ │ - primary URLs           │
   │ Produces:                 │ │ Produces:     │ │ Produces:                 │
   │ - architecture-options.json│ │ - feature-   │ │ - content-handoff.json    │
   │ - adr-spec.json           │ │   ticket.json │ │                           │
   └───────────────────────────┘ └───────────────┘ └───────────────────────────┘
```

1. **Handoff to `@technical-architect`**:
   - Architect parses `citation_dag` to extract component dependencies, p99 latencies, and hardware limits.
   - Outputs: `core/contracts/schemas/architecture-options.json` or `core/contracts/schemas/adr-spec.json`.
2. **Handoff to `@business-analyst`**:
   - Analyst parses `synthesis.critical_gaps` and `cove_verification_matrix` to define scope constraints and acceptance criteria.
   - Outputs: `core/contracts/schemas/feature-ticket.json`.
3. **Handoff to `@content-writer`**:
   - Content writer ingests high-density verified facts and live primary URLs, ensuring the final publication contains 0% AI hallucination.
   - Outputs: `core/contracts/schemas/content-handoff.json`.

---

## 7. Operational Anti-Patterns & Failure Modes

The following catalog identifies the ten deadly anti-patterns in autonomous research and their mandatory remediations:

| # | Anti-Pattern | Operational Failure Mode | Mandatory Remediation |
|---| :--- | :--- | :--- |
| 1 | **Circular AI Echo Chamber** | Citing AI summaries that quote earlier LLM generations. | Reject fail-closed via `ZERO-AI-PRIMARY-CITATION-LOCK`. Trace claims back to human-authored RFCs or repository commits. |
| 2 | **Single-Perspective Blindness** | Querying only for confirming evidence; ignoring failure modes. | Execute STORM automated persona discovery. Mandate Skeptical Auditor and Compliance Reviewer probes before searching. |
| 3 | **Compound Claim Smuggling** | Combining a true fact with an ungrounded hallucination in one sentence. | Decompose into atomic propositions ($P = \bigwedge p_j$) via CoVe. Verify each proposition via isolated queries. |
| 4 | **Artificial Contradiction Smoothing** | Averaging conflicting benchmark numbers into a single synthetic figure. | Preserve contradictions in the Citation DAG using `relationship: "contradicts"`. Document divergent test conditions. |
| 5 | **Diluted Conversational Fluff** | Generating polite filler paragraphs ("delve into", "pave the way"). | Enforce $\text{ID} \ge 0.12$. Reject reports failing entity/metric ratios during AST lint checks. |
| 6 | **Unverified AI Citation Hallucination** | Accepting a URL emitted by an AI tool without verifying liveness or content. | Perform `read_url_content` or `curl -sI`. If 404 or content mismatch, flag `[AI-CITATION MISMATCH]`. |
| 7 | **Deep Mode Round Truncation** | Terminating research after 4 or 5 rounds when configured for deep mode. | Schema validation enforces `total_rounds >= 10` when `depth_mode: "deep"`. Truncated reports fail schema validation. |
| 8 | **Stripped Media Provenance Trust** | Assuming an unlabeled diagram or chart is human-authored. | Inspect via `c2patool`. If C2PA manifest is absent or invalid, label asset as `[UNVERIFIED PROVENANCE]`. |
| 9 | **Stale Documentation Anachronism** | Citing deprecated API syntax or obsolete standards from 2021. | Verify git commit dates and official release tags. Mandate current major version alignment (e.g. Astro v5, Redis 7.4). |
| 10 | **Scope Waiver Evasion** | Executing scoped depth (< 10 rounds) without documenting authorization. | Schema validation enforces non-empty `scope_waiver_note` when `depth_mode: "scoped"`. |

---

## 8. Reference Implementations & Automation Scripts

Below are reference Python implementations codified for inclusion in automated validation pipelines and test suites (e.g. `tests/test_researcher_sota_challenge.py`).

### 8.1 Citation DAG Topological Cycle Detector (3-Color DFS)

```python
"""
Citation DAG Cycle Detector
Algorithm: 3-Color Depth-First Search (DFS)
Complexity: Time O(|V| + |E|), Space O(|V|)
"""

from typing import Any, Dict, List, Tuple


def check_citation_dag_acyclicity(
    nodes: List[Dict[str, Any]], 
    edges: List[Dict[str, Any]]
) -> Tuple[bool, List[str]]:
    """
    Evaluates whether a directed citation graph G = (V, E) is strictly acyclic.
    
    Color Codes:
      0: White (Unvisited)
      1: Gray (Active in current recursion stack -> indicates back-edge/cycle)
      2: Black (Fully explored)
      
    Returns:
      (is_acyclic, cycle_path)
    """
    node_ids = {n["node_id"] for n in nodes}
    
    # 1. Edge endpoint validation & self-loop check
    adj: Dict[str, List[str]] = {nid: [] for nid in node_ids}
    for e in edges:
        u = e.get("from_node_id")
        v = e.get("to_node_id")
        
        if u not in node_ids or v not in node_ids:
            raise ValueError(f"Malformed edge ({u} -> {v}): endpoint not in V")
            
        if u == v:
            # Self-loop detected immediately
            return False, [u, v]
            
        adj[u].append(v)
        
    color: Dict[str, int] = {nid: 0 for nid in node_ids}
    cycle_path: List[str] = []
    
    def dfs(curr: str, stack: List[str]) -> bool:
        color[curr] = 1  # Mark Gray
        stack.append(curr)
        
        for neighbor in adj.get(curr, []):
            if color[neighbor] == 1:
                # Cycle detected: back-edge to an active ancestor
                cycle_start = stack.index(neighbor)
                cycle_path.extend(stack[cycle_start:] + [neighbor])
                return True
            if color[neighbor] == 0:
                if dfs(neighbor, stack):
                    return True
                    
        stack.pop()
        color[curr] = 2  # Mark Black
        return False

    for nid in sorted(node_ids):
        if color[nid] == 0:
            if dfs(nid, []):
                return False, cycle_path

    return True, []
```

### 8.2 Quantitative Information Density Calculator

```python
"""
Quantitative Information Density (ID) Calculator
Formula: ID = (Named Entities + Quantified Metrics) / Total Words >= 0.12
"""

import re
from typing import Dict, Any


# Regex patterns for named entities and quantified metrics
ENTITY_PATTERN = re.compile(
    r"\b("
    r"[A-Z][a-zA-Z0-9]*(?:[\s-][A-Z0-9][a-zA-Z0-9]*)*|"  # Proper nouns (e.g. AWS Graviton3, Redis)
    r"TCVN\s*\d+(?::\d+)?|"                               # Vietnamese Standards (TCVN 7830:2021)
    r"RFC\s*\d+|"                                         # RFC Standards (RFC 9110)
    r"EU\s*AI\s*Act(?:\s*Article\s*\d+)?|"                # EU Regulations
    r"GDPR(?:\s*Article\s*\d+)?|"                         # GDPR clauses
    r"ASHRAE\s*\d+(?:-\d+)?|"                             # ASHRAE standards
    r"POSIX(?:\s*shm)?|"                                  # POSIX specifications
    r"C2PA(?:\s*v?\d+\.\d+)?"                             # C2PA standards
    r")\b"
)

METRIC_PATTERN = re.compile(
    r"\b("
    r"\d+(?:\.\d+)?\s*(?:ms|μs|ns|s|min|h)|"              # Latencies (0.15ms, 12.4μs)
    r"\d+(?:\.\d+)?\s*(?:k|M|G|T)?\s*(?:TPS|req/s|QPS)|"  # Throughput (610k TPS, 240k QPS)
    r"\d+(?:\.\d+)?\s*(?:%|percent)|"                     # Percentages (99.99%)
    r"\d+(?:\.\d+)?\s*(?:B|KB|MB|GB|TB|KiB|MiB|GiB)|"     # Memory/Storage (512 MiB, 64 GB)
    r"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}Z?)?|"       # ISO Timestamps (2026-10-23)
    r"\d+(?:\.\d+)?\s*(?:x|X)|"                           # Multipliers (15x)
    r"<=\s*\d+(?:\.\d+)?|>=?\s*\d+(?:\.\d+)?"             # Inequalities (<= 0.18ms)
    r")\b",
    re.IGNORECASE
)

FLUFF_PATTERN = re.compile(
    r"\b("
    r"delve into|delving into|"
    r"pave the way|paves the way|"
    r"testament to|a testament to|"
    r"in today'?s (?:fast-paced|digital|modern) world|"
    r"crucial cornerstone|"
    r"game changer|paradigm shift"
    r")\b",
    re.IGNORECASE
)


def calculate_information_density(text: str) -> Dict[str, Any]:
    """
    Computes the Information Density score of a given research synthesis.
    """
    # Strip markdown headers, table markers, and code blocks
    cleaned_text = re.sub(r"```[\s\S]*?```", "", text)
    cleaned_text = re.sub(r"#+.*", "", cleaned_text)
    cleaned_text = re.sub(r"\|.*?\|", "", cleaned_text)
    
    words = [w for w in cleaned_text.split() if w.strip()]
    total_words = len(words)
    
    if total_words == 0:
        return {
            "total_words": 0,
            "named_entities_count": 0,
            "quantified_metrics_count": 0,
            "density_score": 0.0,
            "status": "failed",
            "fluff_detected": []
        }
        
    named_entities = ENTITY_PATTERN.findall(cleaned_text)
    quantified_metrics = METRIC_PATTERN.findall(cleaned_text)
    fluff_matches = FLUFF_PATTERN.findall(cleaned_text)
    
    ne_count = len(named_entities)
    qm_count = len(quantified_metrics)
    density_score = round((ne_count + qm_count) / total_words, 4)
    
    passed = (density_score >= 0.12) and (len(fluff_matches) == 0)
    
    return {
        "total_words": total_words,
        "named_entities_count": ne_count,
        "quantified_metrics_count": qm_count,
        "density_score": density_score,
        "formula": "ID = (Named Entities + Quantified Metrics) / Total Words",
        "status": "passed" if passed else "failed",
        "fluff_detected": list(set(fluff_matches))
    }
```

---

## 9. Conclusion & Compliance Mandate

The SOTA Deep Research architecture codified in this document provides a formal, non-negotiable engineering foundation for all research tasks across the agent ecosystem. 

By unifying:
1. **Stanford STORM** pre-search multi-perspective persona discovery,
2. **Citation DAG** mathematical acyclicity and zero-AI primary source locks,
3. **Chain-of-Verification (CoVe)** isolated atomic claim verification and C2PA cryptographic provenance, and
4. **Quantitative Information Density** ($\text{ID} \ge 0.12$) anti-fluff enforcement,

the framework ensures that downstream autonomous agents receive mathematically grounded, empirically triangulated, and epistemically unassailable research reports.
