# Agent Infrastructure



#### `agent-card.json`

**A2A Agent Card**  
Self-describing manifest for agent discovery (A2A 1.0 / Antigravity). Publish at /.well-known/agent-card.json per role or use pack registry.

Required fields: `name`, `description`, `url`, `version`, `protocol_version`, `capabilities`, `skills`  
Size: 4,901 bytes  
✅ Has example

#### `agent-trace-span.json`

**Agent Trace Span**  
Lightweight observability span for agent sessions (OpenTelemetry GenAI-aligned fields).

Required fields: `trace_id`, `span_id`, `role`, `operation`, `status`  
Size: 1,867 bytes  
✅ Has example

#### `compact-working-state.json`

**Compact Working State Specification**  
Anchored 10-slot working state checkpoint for in-flight agent context window compaction, attention management, and persistent memory handoff.

Required fields: `contract_type`, `current_goal`, `work_type`, `phase_control`, `active_constraints`, `files_modified_and_inspected`, `decisions_and_tradeoffs`, `verification_and_evidence`, `failed_attempts_and_antipatterns`, `preserved_invariants`, `next_single_safe_action`  
✅ Has example

---
