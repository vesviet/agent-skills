# 2026 Tool Orchestration Patterns (Reference)

Deep patterns extracted from `SKILL.md` to keep the main file under 200 lines.
Load this file only when implementing or reviewing an orchestration engine, a
budget enforcement policy, or an OTel instrumentation layout.

## Parallel Tool Execution

Orchestration engines must maximize throughput by parallelizing independent tool calls:

- **Default Concurrency**: Execute independent file reads, searches, and remote API calls in parallel using async frameworks (e.g., `asyncio.gather` in Python) or thread pools.
- **Dependency Resolvers**: Compute tool execution dependency DAGs before running, ensuring sequential execution is reserved only for dependent inputs/outputs.
- **Error Propagation**: Handle failures in parallel execution blocks cleanly, capturing partial successes without blocking the entire workflow.

## LATS vs ReAct Decision Framework

Match the reasoning pattern to the complexity and risk level of the objective:

- **ReAct (Reasoning and Action)**: Use for straightforward, linear tasks where the action space is well-defined and a sequential loop is sufficient.
- **LATS (Language Agent Tree Search)**: Deploy for highly complex, multi-path coding or reasoning tasks. LATS implements Monte Carlo Tree Search (MCTS) to sample, evaluate (using LLM-as-a-judge nodes), and backtrack along multiple execution branches.
- **Backtracking**: Allow the agent to roll back the tool execution path to a previous checkpoint state if a node evaluation score drops.

## Tool Budget Enforcement and OTel Instrumentation

Ensure cost boundaries and complete operational observability:

- **Budget Tracking**: Configure a maximum monetary and count budget for each orchestration loop. Monitor usage per tool call (incorporating LLM token costs and paid API fees).
- **Event Emitting**: Raise a `budget_exhausted` event immediately when the budget limit is reached, halting state mutations and performing clean rollbacks.
- **OTel Spans**: Wrap each tool execution in an OpenTelemetry child span under the main task transaction.
- **Span Attributes**: Tag spans with standard semantic attributes including tool name, arguments, input size, execution duration, cost, and exit status.

## Policy-As-Code Reference

Before any state-changing tool (write, delete, shell that mutates, install,
migration, deployment, secrets), the orchestration engine must:

1. identify the active role
2. map the attempted action to a policy action id
3. read `core/policies/action-boundaries.yaml` and apply the verdict (allowed, requires_approval, denied)
4. classify any output containing customer/credential/PII data with `core/policies/data-classification.yaml`
5. when no role entry exists, apply `default_policy: requires_approval`
6. map IDE/MCP tool names through `core/policies/mcp-tool-map.yaml` when the platform tool label differs from policy action ids

Policies complement `core/rules/code.md`; policies take precedence for enforceable action decisions. Optional runtime: `adapters/cursor/hooks.template.json` invokes `core/scripts/hooks/check-policy.py`; approval-required and denied actions return non-zero exit codes.

## Orchestration Control Frame

When this skill drives a multi-step task, maintain a compact internal control frame:

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
