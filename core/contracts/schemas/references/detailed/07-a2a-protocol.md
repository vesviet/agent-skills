# A2A Protocol (Agent-to-Agent)



#### `a2a-task.json`

**A2A Task Delegation**  
Task unit for A2A 1.0 delegation (submit, stream, get, cancel). Extends pack delegation with full lifecycle.

Required fields: `task_id`, `delegator`, `assignee_role`, `task_description`, `output_schema_ref`, `success_criteria`, `risk_tier`  
Size: 3,660 bytes  
✅ Has example

#### `a2a-task-status.json`

**A2A Task Status**  
Response for Get Task / List Tasks operations (A2A 1.0).

Required fields: `task_id`, `state`, `updated_at`  
Size: 1,717 bytes  
✅ Has example

#### `a2a-task-progress.json`

**A2A Task Progress Event**  
Server-Sent Event payload for streaming task updates (A2A Send Streaming Message / Antigravity agent.stream).

Required fields: `event`, `task_id`, `timestamp`  
Size: 1,614 bytes  
✅ Has example

#### `a2a-artifact.json`

**A2A Task Artifact**  
Deliverable returned by a worker agent (A2A Artifact / Antigravity task result).

Required fields: `task_id`, `status`  
Size: 3,042 bytes  
✅ Has example

#### `a2a-task-cancel.json`

**A2A Task Cancel Request**  
Request body for tasks/cancel (A2A 1.0).

Required fields: `task_id`, `cancel_reason`  
Size: 800 bytes  
✅ Has example

#### `a2a-message.json`

**A2A Message**  
Single message in an A2A task conversation history.

Required fields: `message_id`, `role`, `parts`  
Size: 1,403 bytes  
✅ Has example

#### `a2a-jsonrpc-envelope.json`

**A2A JSON-RPC 2.0 Envelope**  
Wire-format wrapper for A2A operations (agent.invoke, agent.stream, tasks/get, tasks/cancel).

Required fields: `jsonrpc`  
Size: 1,422 bytes  
✅ Has example

#### `a2a-push-notification-config.json`

**A2A Push Notification Config**  
Webhook configuration for async task completion (A2A 1.0 push notifications).

Required fields: `task_id`, `callback_url`, `events`  
Size: 1,254 bytes  
✅ Has example

#### `coordination-plan.json`

**Coordination Plan**

Structured multi-agent execution plan produced by Agent Coordinator. Defines phases, dependencies, gate conditions, circuit breakers, per-phase token budgets, confidence levels, and interruption recovery checkpoints for complex multi-role workflows. Consumed by all execution roles to understand their phase, sequencing, and reporting obligations. Pairs with a2a-task.json for per-phase task dispatch.

Required fields: `contract_type`, `goal`, `phases`, `execution_state`
Size: 13,665 bytes
✅ Has example
