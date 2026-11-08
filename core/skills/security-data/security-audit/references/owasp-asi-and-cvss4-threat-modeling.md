# OWASP ASI Top 10 & CVSS 4.0 Threat Modeling Specifications (2026)

## 1. Vulnerability Scoring via CVSS 4.0 & EPSS Triad

### 1.1 CVSS 4.0 Macro-Vectors & BTE Nomenclature
CVSS v4.0 introduces distinct metric groups separating the vulnerable target component from impacted subsequent systems:
- **Base Metrics (CVSS-BT)**:
  - *Vulnerable System*: Attack Vector (AV), Attack Complexity (AC), Attack Requirements (AT), Privileges Required (PR), User Interaction (UI), Vulnerable System Confidentiality (VC), Integrity (VI), Availability (VA).
  - *Subsequent Systems*: Subsequent System Confidentiality (SC), Integrity (SI), Availability (SA).
  - *Threat Metrics*: Exploit Maturity (E: Unreported / Proof-of-Concept / Attacked).
- **Environmental & Supplemental Metrics (CVSS-BTE / MSS)**:
  - *Automatable*: Evaluates whether remote exploit execution can be automated by attackers (Yes / No).
  - *Recovery*: Evaluates automated system self-recovery capability (Automatic / User / Irrecoverable).
- **The Prioritization Triad**:
  $$\text{Remediation Priority} = \text{CVSS 4.0 Score} \times \text{EPSS (Exploit Prediction Scoring)} \times \text{CISA KEV Status}$$
  Any vulnerability with $\text{EPSS} > 10\%$ or listed on the CISA Known Exploited Vulnerabilities catalog mandates emergency remediation within 24–48 hours.

---

## 2. OWASP Top 10 for Agentic Applications (ASI01–ASI10)

Auditing autonomous agent workflows requires applying the official 2026 OWASP ASI taxonomy:
1. **ASI01 Agent Goal Hijack**: Prompt injection, jailbreaking, or indirect instructions via untrusted tool outputs altering the agent's core goal.
2. **ASI02 Tool Misuse & Exploitation**: Excessive agency, lack of tool input validation, or unconstrained shell/database invocation.
3. **ASI03 Identity & Privilege Abuse**: Autonomous token assumption, lack of JIT scope bounding, or agent impersonation across trust boundaries.
4. **ASI04 Agentic Supply Chain**: Unvetted third-party skill definitions, malicious prompt templates, or poisoned model weights.
5. **ASI05 Unexpected Code Execution**: Arbitrary script execution breaking out of ephemeral sandboxes.
6. **ASI06 Memory & Context Poisoning**: Injecting malicious context into persistent memory (`MEMORY.md`, vector stores) to steer future sessions.
7. **ASI07 Insecure Inter-Agent Communication**: Lack of mutual authentication (mTLS / SVIDs) or schema validation on A2A protocol payloads.
8. **ASI08 Cascading Failures**: Unhandled exceptions in subagents cascading into multi-agent deadlocks or resource starvation.
9. **ASI09 Human-Agent Trust Exploitation**: Deceptive agent assurances, bypassing human approval gates on financial or destructive actions.
10. **ASI10 Rogue Agents**: Self-replicating autonomous loops, unmonitored external exfiltration, or loss of supervisory control.

---

## 3. Zero Trust Workload Attestation (SPIFFE/SPIRE)

- **SPIFFE ID Standard**: `spiffe://cluster.local/ns/{namespace}/sa/{serviceaccount}`.
- All service-to-service and agent-to-agent communication requires mutual TLS (mTLS) with short-lived X.509 SVIDs (SPIFFE Verifiable Identity Documents) rotated every 60 minutes.
