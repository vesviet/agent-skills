---
name: agent-tool-orchestration
description: Plan and sequence agent tool use by choosing the smallest reliable tool, controlling work phase by phase, parallelizing independent reads, avoiding unsafe shell operations, and validating results. Use when a task requires multiple searches, file edits, commands, or external checks across a bug, feature, review, or debugging flow.
---

# Agent Tool Orchestration

Use this skill when a task needs disciplined tool selection and sequencing across exploration, triage, editing, validation, and reporting.

## When to Use

- a task needs multiple searches, edits, commands, or checks
- deciding the smallest reliable tool per step
- parallelizing independent reads safely
- avoiding unsafe shell while triaging a bug/feature

## Core Rules

- enforce the **Principle of Least Agency**: grant only the minimum tool subset and ephemeral capability tokens required for the active phase (e.g. read-only tools during triage/review)
- enforce **Step-Order Contracts (FSM)**: strictly sequence operations through `intake -> inspect -> plan -> validate -> mutate -> verify`; reject out-of-order mutations
- separate the **Cognitive Plane** (LLM reasoning and planning) from the **Deterministic Control Plane** (sandboxed execution, policy gating, syscall monitoring)
- prefer specialized tools over shell commands when available
- classify the work phase before choosing tools
- parallelize independent reads and searches
- do not run destructive commands without explicit user approval
- inspect before editing and validate after substantive changes
- keep tool use scoped to the user's request and repo-local conventions
- do not let a task move to the next phase without enough evidence for that phase
- when available, prefer MCP-compatible tool servers over ad-hoc integrations
- validate tool inputs and outputs against their declared contracts
- check `core/policies/action-boundaries.yaml` before any state-changing action when a role is active
- check `core/policies/data-classification.yaml` before logging, returning, or persisting sensitive data
- enable parallel tool execution as default using `asyncio.gather` or thread pools for non-interdependent operations
- choose between ReAct (linear action spaces) and LATS (Monte Carlo Tree Search tree exploration) based on task complexity
- enforce strict tool call budget management, monitoring max budgets and raising a `budget_exhausted` event if exceeded
- instrument all tool calls using OpenTelemetry (OTel) with child spans and detailed semantic attributes (OWASP ASI01–ASI10 compliance)

## Policy-As-Code (2026)

Before state-changing tools (write, delete, shell that mutates, install, migration, deployment, secrets):

1. identify the **active role** (from user assignment or coordination plan owner)
2. map the attempted action to a policy action id (for example `write_file`, `run_migration`, `push_to_production`)
3. read `core/policies/action-boundaries.yaml` for that role:
   - **allowed**: proceed
   - **requires_approval**: stop and request explicit user approval with risk summary
   - **denied**: stop and explain the boundary; recommend the owning role
4. if output may contain customer, credential, or PII data, classify it with `data-classification.yaml`:
   - **restricted** or **confidential**: do not log full payloads; redact in handoff artifacts
5. when no role entry exists, apply `default_policy: requires_approval`
6. map IDE/MCP tool names through `core/policies/mcp-tool-map.yaml` when the platform tool label differs from policy action ids

*Policies complement `core/rules/code.md`; policies take precedence for enforceable action decisions. Optional runtime: `adapters/cursor/hooks.template.json` invokes `core/scripts/hooks/check-policy.py`; approval-required and denied actions return non-zero exit codes.*

## MCP And Context Engineering

Model Context Protocol (MCP) is the 2026 industry standard for connecting agents to external tools, databases, and enterprise systems.

When orchestrating tools in an MCP-aware environment:

- **Discovery**: query the MCP server for available tools before assuming capabilities
- **Contracts**: respect the input/output schema declared by each tool server
- **Authentication**: use the standard MCP auth layer rather than embedding credentials in prompts
- **Idempotency**: prefer idempotent tool calls; confirm side effects before executing non-idempotent actions
- **Cost awareness**: set budgets for expensive tool calls (API queries, large data retrievals) and report usage

When MCP is not available, apply the same discipline manually:

- document each tool's expected input and output format
- validate responses before passing them to the next step
- treat tool failures as retriable unless explicitly marked as fatal

## Suggested Process

### 1. Classify The Work And Phase

Decide:

- whether the task is a bug, feature, review, validation, or documentation task
- whether the current phase is intake, triage, implementation, validation, review, or handoff
- what output is required before the phase can end

### 2. Choose The Smallest Reliable Tool For The Phase

Prefer:

- file read tools for known files
- search tools for code discovery
- patch tools for focused edits
- shell commands for validation, build, test, and git status

Examples:

- intake or triage: file reads, searches, logs, focused reproduction commands
- implementation: focused reads, targeted edits, nearby-pattern inspection
- validation: narrow tests, validators, build commands, smoke checks
- handoff: diff inspection, changed-file review, validation summary

### 3. Batch Independent Work

Run independent reads, globs, searches, or lints in parallel when they do not depend on each other.

### 4. Sequence Risky Actions And Phase Gates

Before commands that create files, run builds, or change state:

- verify the working directory
- check relevant parent paths
- avoid duplicating long-running processes
- confirm permissions or user approval when required
- confirm the current phase has enough evidence to justify the next action

### 5. Reopen Earlier Phases When Needed

If new evidence appears:

- reopen triage when reproduction or expected behavior changes
- reopen implementation when validation exposes a deeper cause
- reopen review when a late risk invalidates the previous recommendation

### 6. Validate The Result

After edits:

- run targeted validators or lints
- inspect failures before changing more code
- rerun the smallest check that proves the fix

## 2026 Tool Orchestration Patterns

### 2026: Parallel Tool Execution

Orchestration engines must maximize throughput by parallelizing independent tool calls:
- **Default Concurrency**: Execute independent file reads, searches, and remote API calls in parallel using async frameworks (e.g., `asyncio.gather` in Python) or thread pools.
- **Dependency Resolvers**: Compute tool execution dependency DAGs before running, ensuring sequential execution is reserved only for dependent inputs/outputs.
- **Error Propagation**: Handle failures in parallel execution blocks cleanly, capturing partial successes without blocking the entire workflow.

### 2026: LATS vs ReAct Decision Framework

Match the reasoning pattern to the complexity and risk level of the objective:
- **ReAct (Reasoning and Action)**: Use for straightforward, linear tasks where the action space is well-defined and a sequential loop is sufficient.
- **LATS (Language Agent Tree Search)**: Deploy for highly complex, multi-path coding or reasoning tasks. LATS implements Monte Carlo Tree Search (MCTS) to sample, evaluate (using LLM-as-a-judge nodes), and backtrack along multiple execution branches.
- **Backtracking**: Allow the agent to roll back the tool execution path to a previous checkpoint state if a node evaluation score drops.

### 2026: Tool Budget Enforcement and OTel Instrumentation

Ensure cost boundaries and complete operational observability:
- **Budget Tracking**: Configure a maximum monetary and count budget for each orchestration loop. Monitor usage per tool call (incorporating LLM token costs and paid API fees).
- **Event Emitting**: Raise a `budget_exhausted` event immediately when the budget limit is reached, halting state mutations and performing clean rollbacks.
- **OTel Spans**: Wrap each tool execution in an OpenTelemetry child span under the main task transaction.
- **Span Attributes**: Tag spans with standard semantic attributes including tool name, arguments, input size, execution duration, cost, and exit status.

## Output Format

When this skill is driving a multi-step task, maintain a compact internal control frame:

```markdown
## Orchestration Frame

Work type:
- ...

Current phase:
- ...

Exit criteria:
- ...

Tools selected:
- ...

Evidence required before next phase:
- ...
```

## Checklist

- [ ] task type and current phase classified
- [ ] repo constraints checked before action
- [ ] active role identified and action checked against action-boundaries.yaml
- [ ] sensitive data classified before logging or handoff
- [ ] smallest reliable tools selected
- [ ] MCP tool discovery performed when available
- [ ] tool input/output contracts validated
- [ ] independent exploration parallelized
- [ ] state-changing commands sequenced safely
- [ ] phase progression justified by evidence
- [ ] edits validated with relevant checks
- [ ] tool call costs tracked when applicable

## Related Skills

- **agent-a2a-protocol**: Full A2A lifecycle when tools participate in multi-agent handoffs
- **agent-graph-orchestration**: Advance multi-phase graphs with parallel merge gates
- **agent-delegation**: Issue A2A tasks instead of overloading a single context
- **agent-context-management**: Keep goal, evidence, and assumptions aligned
- **agent-prompt-lifecycle**: Manage prompt versioning and evaluation when orchestrating prompt-driven tasks
- **agent-quality-gate**: Run the correct completion checks
- **agent-handoff**: Report results and remaining risk clearly
- **troubleshoot-service**: Diagnose failing commands or runtime behavior
- **commit-code**: Prepare approved changes for delivery
