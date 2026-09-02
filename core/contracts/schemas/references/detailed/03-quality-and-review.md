# Quality & Review



#### `code-review-finding.json`

**Code Review Finding**  
Structured output from the Reviewer role using the review-code skill. Emitted per change set or PR. Consumed by developers (for fixes), Technical Lead (for delivery readiness), Agent Coordinator (as phase gate evidence), and QA (for validation gaps). One document covers the full review; findings[] contains individual issues.

Required fields: `contract_type`, `change_ref`, `findings`, `review_matrix`, `blast_radius_assessment`, `merge_recommendation`  
Size: 7,905 bytes  
✅ Has example

#### `test-report.json`

**QA Test Report**  
Structured output from QA Engineer using write-tests, frontend-testing, or review-service skills. Emitted after test execution. Consumed by Technical Lead, Reviewer, Project Manager, and Agent Coordinator as release confidence evidence. Complements code-review-finding.json — review catches code issues, test-report catches behavior risk.

Required fields: `contract_type`, `ticket_ref`, `environment`, `status`, `scenarios_executed`, `release_recommendation`  
Size: 6,341 bytes  
✅ Has example

#### `validation-result.json`

**Validation Result**  
Structured output from a validation or quality gate step.

Required fields: `contract_type`, `phase_reviewed`, `checks_run`, `passed`, `decision`  
Size: 2,651 bytes  
✅ Has example

#### `security-audit.json`

**Security Audit Report**  
Structured output for a security audit or vulnerability assessment.

Required fields: `contract_type`, `target`, `audit_type`, `findings`, `overall_risk_score`  
Size: 2,776 bytes  
✅ Has example

#### `performance-audit.json`

**Performance Audit Result**  
Structured output for a frontend or 3D performance audit.

Required fields: `contract_type`, `target`, `findings`, `verdict`  
Size: 3,286 bytes  
✅ Has example

#### `incident-report.json`

**Incident Report**  
Structured output for SRE incident response and post-mortems.

Required fields: `contract_type`, `severity`, `status`, `impact`, `timeline`  
Size: 3,524 bytes  
✅ Has example
