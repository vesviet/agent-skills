# Production GenAI System Risk Register: Autonomous Support Agent

```yaml
system_id: "agentic-support-v2"
system_name: "Customer Operations Autonomous Support Agent"
assessment_date: "2026-11-08"
assessor: "security-engineer"
review_due: "2027-02-08"

governance:
  owner: "Director of Platform Engineering"
  policy_profile: "restricted-agentic"
  human_oversight_mechanism: "Dual-operator HITL modal for refunds > $50 and account changes"
  review_cadence: "quarterly"
  escalation_path: "VP Engineering & Legal Compliance"

eu_ai_act:
  risk_tier: "limited-risk"
  classification_rationale: "Customer support conversational interface; does not evaluate credit, safety-critical systems, or recruitment."
  conformity_assessment_required: false
  audit_logging_required: true
  hitl_required: true
  bias_assessment_required: false
  target_compliance_date: "2026-08-02"
  transparency_art_50:
    disclosure_banner: "You are chatting with an AI assistant."
    c2pa_metadata_tagging: true

nist_600_1_risks:
  hallucination_threshold: "< 1.5% ungrounded assertions on golden evaluation benchmark"
  model_degradation_signal: "Drop in semantic similarity below 0.88 over 7-day rolling window"
  bias_exposure: "Multi-lingual queries in non-English locales"
  data_privacy_classification: "Restricted - customer PII sanitized via presidio before LLM ingestion"
  ip_risk: "Low - model inference only, no fine-tuning on proprietary customer contracts"

owasp_asi_alignment:
  - asi_id: "ASI01"
    threat: "Direct prompt injection via user support query"
    mitigation: "Strict XML delimiter encapsulation + secondary classifier check"
  - asi_id: "ASI03"
    threat: "Agent executing unauthenticated customer refund tool"
    mitigation: "Task-scoped JWT with max $50 refund limit; higher amounts require HITL token"
  - asi_id: "ASI06"
    threat: "Customer injecting malicious instructions into persistent chat memory"
    mitigation: "OWASP ASI06 memory hygiene sanitization; rejection of system-prompt overrides"
  - asi_id: "ASI08"
    threat: "Tool timeout causing support agent infinite retry storm"
    mitigation: "Exponential backoff with circuit breaker trip at 5 failures"

autonomy_and_reversibility:
  autonomy_tier: "semi-autonomous"
  reversible_actions:
    - "search_knowledge_base"
    - "draft_ticket_reply"
    - "get_order_status"
  irreversible_actions:
    - "process_refund"
    - "cancel_subscription"
    - "update_customer_email"
  irreversible_action_policy: "Mandatory human confirmation gate"

residual_risks:
  - risk: "Edge case refund fraud under $50 limit"
    accepted_by: "Risk & Finance Committee"
    accepted_date: "2026-10-15"
    review_date: "2027-04-15"
```
