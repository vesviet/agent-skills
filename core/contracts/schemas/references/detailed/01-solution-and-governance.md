# Solution & Governance



#### `solution-brief.json`

**Solution Brief**  
Primary machine-readable handoff from the Solution Architect, produced before requirements or architecture are locked. Consumed by Technical Architect (for adr-spec.json), Business Analyst (for feature-ticket.json), Product Manager (go/no-go), and Agent Coordinator (solution scoping gate). Captures problem framing, capability gaps, build-vs-buy decision (including MCP marketplace evaluation), AI feasibility, agent ROI, and compliance constraints.

Required fields: `contract_type`, `problem_statement`, `options_considered`, `build_vs_buy_decision`, `recommendation`  
✅ Has example

#### `ai-risk-register.json`

**AI Risk Register**  
Structured output from the ai-risk-assessment skill (owned by Business Analyst, Project Manager, or Security Engineer). Applies NIST AI RMF 1.0, the NIST AI 600-1 GenAI Profile, EU AI Act risk classification, and OWASP ASI alignment. A living lifecycle artifact consumed by Product Manager, Technical Architect, Security Engineer, and Agent Coordinator before delivery commitment.

Required fields: `contract_type`, `governance`, `eu_ai_act`, `nist_600_1_risks`, `residual_risks`  
✅ Has example
