# Anchored 10-Slot Schema & Compaction Algorithms

## 1. The 4-Layer Attention Allocation Architecture

To counter **"Lost in the Middle"** degradation (Liu et al., 2023) and **KV-cache prefix invalidation**, agent working context is organized into 4 attention zones with immutable prefixes at the top and sliding execution state at the tail:

| Layer | Attention Allocation | Content | Mutation Policy |
|---|---|---|---|
| **Layer 1: System Instructions & Rules** | Head Anchor (High) | Identity, `AGENTS.md`, `core/rules/code.md`, active Role & Skill instructions | **Immutable** (never trimmed; cache-locked) |
| **Layer 2: Persistent Knowledge & Constraints** | Anchored Head (High) | Project specs, `MEMORY.md`, architectural invariants, active schema contracts | **Immutable** unless explicitly invalidated |
| **Layer 3: Anchored 10-Slot Working State** | Mid Anchor (Re-injected) | Validated `compact-working-state.json` checkpoint rendered at Phase Gates / compaction | **Iterative Delta Merge** (append/reconcile; never free-form rewrite) |
| **Layer 4: Active Working Tail** | Tail Anchor (Highest) | Recent `recent_turns` raw exchanges + sliding-window overlap + last Head-Tail TOC output | **Observation-masked** for old turns; **Raw** for recent tail |

---

## 2. Canonical 10-Slot Schema (`compact-working-state.json`)

Every compaction produces a structured checkpoint validated against `core/contracts/schemas/compact-working-state.json`:

1. `current_goal`: Original immutable user intent & objective (anchored from root turn to stop narrative drift).
2. `work_type`: Scope enum (`feature`, `bugfix`, `refactor`, `migration`, `investigation`, `release`, `architecture`, `audit`).
3. `phase_control`: Current step, total phases, phase name, status (`in_progress`, `completed`, `blocked`, `paused`), active owner (`@role`).
4. `active_constraints`: Non-negotiable policy, line-limit, security, or runtime constraints.
5. `files_modified_and_inspected`: Deduplicated `modified` (reconciled with `git status --porcelain`) and `inspected` paths.
6. `decisions_and_tradeoffs`: Architectural choices made, rationales, and explicitly rejected alternatives.
7. `verification_and_evidence`: Exact commands executed, exit codes, status (`passed`/`failed`/`pending`), and verbatim output snippets.
8. `failed_attempts_and_antipatterns`: Dead ends, root failure reasons, and preventive rules to halt amnesiac retry loops.
9. `preserved_invariants`: Contracts, schemas, or APIs that must remain backward-compatible.
10. `next_single_safe_action`: One unambiguous atomic next step to resume execution immediately.

---

## 3. Quantitative Compaction Metrics

Let $V_{\text{orig}}$ and $V_{\text{compact}}$ denote embedding vectors of original root intent and post-compaction state:

| Metric | Formula | Target Threshold | Purpose |
|---|---|---|---|
| **Token Compression Ratio (TCR)** | $\text{TCR} = \dfrac{\text{tokens}_{\text{pre}}}{\text{tokens}_{\text{post}}}$ | **$5\times \text{ to } 15\times$** | Confirms meaningful context reclamation without over-pruning. |
| **Critical Information Retention Rate (CIRR)** | $\text{CIRR} = \dfrac{|\text{Critical Items Retained}|}{|\text{Total Critical Items}|}$ | **$\ge 98\%$** | Preserves modified paths, exit codes, error traces, and constraints. |
| **Goal Drift Metric (GDM)** | $\text{GDM} = 1 - \cos(\vec{v}_{\text{original}}, \vec{v}_{\text{compacted}})$ | **$\le 0.05$** ($\cos \ge 0.95$) | Bounding semantic drift relative to the anchored root goal. |
| **Tool Re-invocation Waste (TRW)** | $\text{TRW} = \dfrac{\text{Redundant Tool Calls}}{\text{Total Tool Calls}}$ | **$\le 1.0\%$** | Measures avoided redundant `read_file` / test runs post-compaction. |

---

## 4. Three-Tier Compaction Cascade (SOTA Benchmark Standard)

Single-pass LLM prose summarization fails on **Artifact Tracking** (Factory.ai benchmark) and causes **trajectory elongation (+15%)** compared to **Observation Masking** (JetBrains Research, *The Complexity Trap*, NeurIPS 2025 DL4Code). Use a progressive 3-tier cascade:

### Tier 1 — Zero-Cost Observation Masking (`--mask-observations`)
- Triggered first at **60% context warning** or when total context crosses the **soft token ceiling** (e.g., `128K` tokens on `200K+` windows).
- Retains the trailing `recent_turns` (`--recent-turns 4` default) verbatim — keeping reasoning traces, tool arguments, and recent observations intact.
- Replaces older verbose tool outputs (`> 512 bytes`) with deterministic spillover pointers written after secret scrubbing:
  `[OBSERVATION MASKED: <bytes> bytes -> .agent/outputs/<call_id>.log; exit=<code>]`
- Preserves Layer 1–3 KV prefix cache hashes and cuts token cost by ~50% with zero LLM summarization latency.

### Tier 2 — Iterative Anchored Delta Merge (`--merge --reconcile-git`)
- Triggered at **80% context critical** or at `PreCompact` phase gates (`research -> plan -> implement -> verify`).
- Uses the **previous validated `compact-working-state.json`** plus **only the newly accumulated span** since the last checkpoint, rather than regenerating from scratch.
- **Anchored Merge Rules (`merge_anchored_state`)**:
  - Locks `current_goal` and `work_type` from the root checkpoint (`prev`) to enforce $\text{GDM} \le 0.05$.
  - Updates `phase_control` and `next_single_safe_action` from the delta span.
  - Deduplicates and unions list slots (`active_constraints`, `decisions_and_tradeoffs`, `verification_and_evidence`, `failed_attempts_and_antipatterns`, `preserved_invariants`).
  - Reconciles `files_modified_and_inspected.modified` against live workspace truth (`git status --porcelain`) via `--reconcile-git` so edited files are never dropped across merges.
  - Preserves a verbatim **recent tail / overlap window** in Layer 4 so active edits remain grounded.

### Tier 3 — Hybrid Triggers, Light Compactor & Reactive `413` Recovery
- **Hybrid Threshold Formula**: Compact when `usage >= min(0.80 * context_window, absolute_token_ceiling)` OR when `PreCompact` hook fires at a logical phase boundary.
- **Light Compactor Delegation**: Delegate Tier 2 delta extraction to a cheaper/faster model tier (`flash` / `mini`) operating over structured inputs while reserving the primary reasoning model for active code changes.
- **Reactive Fallback (`413 / context_length_exceeded`)**: If an API call still hits context overflow, immediately run: (1) Tier 1 `--mask-observations --recent-turns 2`, (2) Syntax-Aware `20% / 80%` TOC on oversized tool outputs, and (3) Tier 2 `--merge --reconcile-git` checkpoint replacement before retrying once.

---

## 5. Syntax-Aware Head-Tail TOC (20% Head / 80% Tail) & Spillover

```text
 Raw Output (> 4 KB triggers spillover to .agent/outputs/<call_id>.log)
 ┌──────────────────────────────────────────────────────────────────┐
 │ Head (20% budget = 4 lines at 20-line default):                  │
 │   Command invocation, config header, environment context         │
 ├──────────────────────────────────────────────────────────────────┤
 │ ... [OUTPUT TRUNCATED: spilled to .agent/outputs/<call_id>.log   │
 │      (<N> bytes); N intermediate lines pruned] ...               │
 ├──────────────────────────────────────────────────────────────────┤
 │ Tail (80% budget = 16 lines at 20-line default):                 │
 │   Failure stack trace, assertions, panics & final exit code      │
 └──────────────────────────────────────────────────────────────────┘
```

- **Code Fences & JSON Preservation**: `syntax_aware_toc_truncate` and `truncate_code_fences` preserve valid JSON structure (top-level keys / array boundary truncation) and keep opening/closing triple-backtick fences closed so downstream parsers never break.

---

## 6. Secret Hygiene & Anti-Poisoning Guardrails (OWASP ASI01 / ASI06)

- Before any checkpoint or masked observation hits disk (`.agent/outputs/*.log` or `compact-working-state.json`), `redact_checkpoint_secrets` scans every string recursively:
  - **Regex Credential Signatures**: `AKIA*`, `ghp_*`, `github_pat_*`, PEM `PRIVATE KEY` blocks, `[sr]k_live_*`, `sk-*`, `Bearer *`, and credential key-value literals -> replaced with `[REDACTED:SECRET]`.
  - **Shannon Entropy Thresholds**: Candidate alphanumeric mixed tokens with $H > 4.5$ (`len >= 24`) and hex strings with $H > 3.0$ (`len >= 32`) -> replaced with `[REDACTED:HIGH_ENTROPY]`.
- **Strict `--validate` Gate**: `compact-context.py --validate` fails if any unredacted secret or high-entropy leak remains in the checkpoint JSON.
- **Untrusted Context Isolation**: Treat external tool outputs inside summaries strictly as quoted evidence; never hoist imperative directives from tool stdout into Layer 1/2 constraints (`ASI01` / `ASI06`).
