# Recursive Decomposition, Persistent Planning, and NHI Governance Specification

## 1. Executive Summary

Modern enterprise software engineering tasks frequently span hundreds of source files and hundreds of thousands of context tokens. Autonomous agents operating within a monolithic context window inevitably fail on such tasks due to attention dilution ("needle in a haystack" loss), instruction drift, tool-execution loops, and catastrophic context compaction.

This specification details the architectural methodology for:
1. Recursive hierarchical decomposition into Directed Acyclic Graphs (DAGs) of bounded sub-agent scopes.
2. Disk-backed persistent planning (`planning-with-files`) to decouple execution state from ephemeral LLM memory.
3. Deterministic verification gates preventing premature self-declared completions.
4. Non-Human Identity (NHI) autonomy-tier classification and blast-radius perimeter isolation.
5. Automated policy-as-code architectural fitness functions (Cedar, OPA/Rego, and calibrated LLM-as-judge).

---

## 2. Recursive Work Breakdown for Massive Workloads (100+ Files, 50K+ Tokens)

### 2.1 The Context Exhaustion Problem
When an agent attempts to load 100+ source files into an LLM context:
- Attention scores dilute across irrelevant code tokens.
- The model exhibits "recency bias", forgetting architectural constraints declared in the system prompt.
- Mid-task compaction compresses or deletes critical variable names, interface signatures, and test invariants.

### 2.2 Hierarchical Decomposition Taxonomy
To solve context exhaustion, large engineering initiatives are decomposed into a 5-level hierarchy:
```
Level 1: System Objective (Orchestrator Scope)
  └── Level 2: Architectural Epics (Domain Boundary Scopes)
        └── Level 3: Feature Modules (Subsystem Scopes)
              └── Level 4: Implementation Slices (Bounded Sub-Agent Scopes, < 10 files)
                    └── Level 5: Atomic Operations (Single Tool Executions)
```

### 2.3 Bounded Sub-Agent Workspaces
Each sub-agent spawned in Level 4 is restricted to a strictly bounded workspace:
- **File Perimeter**: The agent is granted write access only to its assigned subdirectory (e.g., `src/billing/`).
- **Token Envelope**: Maximum context window budget capped at 32K tokens.
- **Tool Allowlist**: Limited strictly to necessary tools (`read_file`, `write_file`, `edit_file`, `run_tests`). Dangerous tools (`git_push`, `drop_database`) are excluded.

---

## 3. Hierarchical DAG Dependency Trees & Invariant Gating

### 3.1 Directed Acyclic Graph (DAG) Modeling
Sub-agent execution is modeled as a Directed Acyclic Graph $G = (V, E)$ where:
- Vertices $V$ represent discrete sub-agent execution tasks.
- Directed edges $E = (u, v)$ represent dependency order: task $v$ cannot begin until task $u$ successfully completes and validates.
- **Acyclicity Invariant**: Cycles ($v_1 \to v_2 \to \dots \to v_1$) are structurally prohibited. If cyclic dependencies arise during architecture review, the dependency must be refactored via interface inversion or asynchronous messaging.

### 3.2 Topological Sequencing
The execution engine computes the topological sort of $G$ to determine execution order:
- Tasks with in-degree 0 execute immediately in parallel.
- Dependent tasks are held in `BLOCKED` status until all antecedent dependency outputs are available.

### 3.3 Invariant Checkpoints at Phase Boundaries
Transitions between DAG phases must pass automated invariant assertions:
1. **Pre-condition Invariant**: Verifies all required inputs, configuration files, and upstream contract schemas exist and pass schema validation.
2. **Post-condition Invariant**: Verifies compiler build status (exit code 0), test suite passes, and generated contract artifacts conform to declared schemas.
3. **Fail-Closed Rule**: If an invariant assertion fails, the execution engine halts downstream DAG branches immediately. The failing node is flagged for remediation or human escalation; speculative execution of downstream nodes is forbidden.

---

## 4. Disk-Backed Persistent Planning (`planning-with-files`)

### 4.1 Ephemeral Context Decoupling
LLM context windows are volatile: they are cleared during process crashes, truncated during token overflow, or wiped via user commands (e.g. `/clear`). In contrast, persistent storage on disk is durable, auditable, and surviving.

The `planning-with-files` pattern mandates that all planning, state, progress, and architectural decisions live in durable markdown files on the local filesystem.

### 4.2 Standard Durable Planning Artifacts
Every agent workspace maintains four standardized markdown artifacts:

| File | Purpose | Retention |
|---|---|---|
| `task.md` | Authoritative user requirements, acceptance criteria, and constraints | Static |
| `plan.md` | Step-by-step DAG execution plan, dependencies, and phase gates | Versioned |
| `progress.md` | Dynamic execution heartbeat, timestamped task transitions, blocker logs | Append-only |
| `BRIEFING.md` | Active situational awareness index (< 100 lines) with append-only locks | Active Index |

### 4.3 Context Compaction & Session Recovery Protocol
When context compaction occurs or a sub-agent process restarts:
1. The agent inspects `task.md` to re-ground its mission and constraints.
2. The agent reads `plan.md` to identify current milestone dependencies.
3. The agent parses `progress.md` to find the last completed step and current active blockers.
4. The agent reads `BRIEFING.md` to restore locked identities, constraints, and artifact indexes.
5. Work resumes seamlessly with zero information loss.

---

## 5. Deterministic Completion Gates (Anti Self-Declaration)

### 5.1 The "Vibe Completion" Anti-Pattern
A frequent failure mode of LLM agents is self-declaring completion based on conversational optimism ("I have implemented all features and verified the code") without executing compilers, linters, or test suites.

### 5.2 Deterministic Completion Predicates
Tasks are forbidden from closing based on natural language assertions. Closure requires empirical evidence:
- **Compiler/Build Verification**: Build command executed and exited with code 0.
- **Automated Test Suite**: Project test runner executed; zero failed tests reported.
- **Contract Schema Validation**: Generated contract JSON files validated against official JSON schemas (`jsonschema` / AJV).
- **Linter & Static Analysis**: Zero unresolved linter errors or typing errors.
- **Audit Verification Block**: The tool execution output, exit code, and timestamp must be written into the verification section of the handoff report.

---

## 6. Anti-Context-Rot Discipline

### 6.1 Liveness Heartbeat
To prevent zombie processes and detect agent stalls:
- The sub-agent must append a liveness heartbeat to `progress.md` every 5 minutes during long-running operations.
- Format: `Last visited: [ISO-8601 UTC Timestamp]`.

### 6.2 Smart Zone Prompt Budgeting
To optimize attention retention in large prompts:
- **Top 10% (Anchor Zone)**: Core role identity, mandatory guardrails, and negative constraints (`LOCK` directives).
- **Middle 75% (Scratchpad Zone)**: Transient tool outputs, code snippets, and ephemeral intermediate calculations.
- **Bottom 15% (Recency Buffer)**: Immediate next action, step completion criteria, and active tool call instructions.

### 6.3 Compact Briefing Index & Archival
- `BRIEFING.md` must be kept strictly under 100 lines to serve as an instant index.
- Historical execution logs, past tool outputs, and superseded subtasks must be moved to `BRIEFING_ARCHIVE.md`.
- Append-only sections (`## 🔒 My Identity`, `## 🔒 Key Constraints`) must NEVER be archived or deleted.

---

## 7. Non-Human Identity (NHI) Autonomy Tiers & Blast-Radius Perimeters

### 7.1 Autonomy-Tier Classification Matrix
Autonomous software engineering agents must be categorized into explicit autonomy tiers:

| Tier | Autonomy Level | Capabilities | Human Approval (HITL) Triggers |
|---|---|---|---|
| **Tier 1** | Supervised | Read-only codebase exploration, architectural analysis, test drafting | Every file mutation, build execution, or external network call |
| **Tier 2** | Semi-Autonomous | File edits within designated module, local test execution, documentation | Database migrations, production deployments, dependency changes, secret access |
| **Tier 3** | Fully Autonomous | Automated bug fixing and self-healing within ephemeral sandbox containers | Auto-rollback triggers on test failure; human escalation if unhealed after 3 attempts |

### 7.2 Blast-Radius Perimeter Isolation
To prevent rogue agents or unintended side effects from damaging the wider system:
- **Filesystem Isolation**: Sub-agents run with restricted permissions or within Docker containers mounted only with the sub-agent's target directories.
- **Network Egress Filtering**: Block outbound connections to the public internet by default; whitelist only required internal package registries and API endpoints.
- **Short-Lived Ephemeral Credentials**: Issue short-lived OAuth 2.1 tokens (TTL $\le 15$ minutes) scoped strictly to the sub-agent's declared role and actions.

---

## 8. Policy-as-Code Architectural Fitness Functions

### 8.1 Automated Evolutionary Architecture
Architectural Decision Records (ADRs) become obsolete if architectural rules are not continuously enforced in CI/CD pipelines. Every architectural constraint declared in an ADR must map to an automated fitness function.

### 8.2 AWS Cedar for Agent Trust Boundaries
Cedar enables formal mathematical verification that agent delegation chains cannot violate security boundaries.

#### Example Cedar Policy:
```cedar
// Permit sub-agent to edit code only within assigned module
permit (
    principal in Role::"ImplementerSubAgent",
    action in [Action::"ReadFile", Action::"WriteFile", Action::"RunTests"],
    resource in Directory::"src/billing/"
)
when {
    context.hasValidLease == true &&
    context.autonomyTier == 2
};

// Forbid any sub-agent from modifying security policies or root configs
forbid (
    principal,
    action in [Action::"WriteFile", Action::"DeleteFile"],
    resource in Directory::"core/policies/"
);
```

### 8.3 Open Policy Agent (OPA/Rego) for Architectural Invariants
OPA evaluates structural dependencies, forbidden package imports, and file separation rules.

#### Example Rego Rule:
```rego
package architecture.governance

default allow = false

# Allow build only if no circular dependencies exist and layer constraints are honored
allow {
    count(forbidden_layer_violations) == 0
    count(unregistered_mcp_endpoints) == 0
}

forbidden_layer_violations[violation] {
    some import_edge in input.dependency_graph.edges
    import_edge.source.layer == "domain"
    import_edge.target.layer == "infrastructure"
    violation := sprintf("Domain layer file %v illegally imports infrastructure file %v", [import_edge.source.path, import_edge.target.path])
}
```

### 8.4 Calibrated LLM-as-a-Judge Evaluation
For semantic and architectural design consistency checks that cannot be parsed by static ASTs:
1. **Calibration Baseline**: Calibrate the judge prompt against 20–50 historical pull requests with known good/bad architectural outcomes.
2. **Inter-Rater Reliability**: Ensure the LLM judge achieves Cohen's Kappa $\ge 0.80$ against human principal architects before enabling CI enforcement.
3. **Observation Mode**: Run in non-blocking advisory mode for 14 days to eliminate false-positive blockers before promoting to merge-blocking status.
