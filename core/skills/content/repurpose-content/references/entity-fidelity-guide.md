# Cross-Format Entity Fidelity & Anti-Hallucination Guide

Reference manual for `repurpose-content` and the `content-writer` role. Governs technical precision preservation, semantic drift prevention, and anti-hallucination audits during multi-channel content adaptation.

---

## 1. Principles of Cross-Format Entity Fidelity

When adapting deep technical architecture articles into short-form formats (X threads, LinkedIn posts, executive newsletters, video scripts), condensation must never compromise technical correctness:

1. **Exact Entity Preservation**: Named technical entities (APIs, system components, algorithm names, version numbers, configuration flags) must be preserved verbatim. Never substitute generic descriptors (e.g., do not replace `epoll` with "network handler", or `PostgreSQL 17 streaming replication` with "database sync").
2. **Metric Integrity**: Quantitative benchmarks (latencies, throughput, memory footprints) must retain their numerical values, units, and measurement qualifiers (e.g., "8ms p99 write latency on NVMe" must not be condensed into "blazing fast writes").
3. **Constraint Preservation**: Architectural caveats, prerequisite configurations, and environmental trade-offs must survive condensation. Omitting constraints creates misleading technical advice.

---

## 2. Metric Translation Without Semantic Drift

| Parent Asset Technical Claim | Permitted Condensed Adaptation | Prohibited Semantic Drift (Reject) |
| :--- | :--- | :--- |
| "Redis replica reads reduce primary database CPU utilization by 42% under 80,000 QPS load." | "Offloading reads to Redis replicas slashed primary DB CPU load by 42% at 80k QPS." | "Redis makes your database dramatically faster." *(Drains metrics and context)* |
| "Rust's ownership model eliminates data races at compile time with zero garbage collection overhead." | "Rust guarantees memory safety without a garbage collector by enforcing ownership at compile time." | "Rust is 100% bug-free software." *(Severe factual hallucination)* |
| "Upgrading to HTTP/3 reduced p95 handshake latency by 35ms on mobile networks with >2% packet loss." | "HTTP/3 cut p95 handshake latency by 35ms on lossy mobile connections (>2% loss)." | "HTTP/3 makes mobile apps load instantly." *(Oversimplification)* |

---

## 3. Anti-Hallucination Audit Protocol & Entity Mapping Matrix

Before publishing any repurposed variant, authors and editors must map source entities to variant representations:

### Entity Mapping Verification Matrix

| Source Entity / Metric | Target Channel | Repurposed Expression | Drift Risk Level | Audit Gate |
| :--- | :--- | :--- | :---: | :---: |
| `8ms p99 latency` | X Thread (Tweet 3) | `8ms p99 write latency` | Zero | **PASS** |
| `Two-phase commit` | LinkedIn Post | `2PC distributed commit` | Zero | **PASS** |
| `PostgreSQL 17 NVMe` | Newsletter | `PostgreSQL on NVMe storage` | Zero | **PASS** |
| `sub-50ms warm cache` | Video Script | `sub-50ms cache response` | Zero | **PASS** |

### Audit Gate Rules
- **Zero Hallucination Mandate**: No fabricated anecdotes, dramatic hypothetical failures, or ungrounded statistics may be introduced to increase social engagement.
- **Traceability Guarantee**: Every causal relationship ("X caused Y") asserted in a social variant must be directly verifiable in the source article text.
