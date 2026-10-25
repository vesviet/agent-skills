---
name: context-optimization
description: Use when optimizing LLM agent context windows, allocating token budgets, pruning semantic duplicates, scoring relevance density, and ordering context to mitigate lost-in-the-middle degradation.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter]
version: 2.0.0
---

# Context Optimization

Maximize effective reasoning density in agent context windows by allocating strict token budgets, eliminating redundant context via semantic deduplication, and structuring prompt sequences to eliminate lost-in-the-middle attention degradation.

## When to Use

- Constructing multi-turn agent execution loops with growing conversation histories
- Injecting multi-document retrieval-augmented generation (RAG) contexts into system prompts
- Compacting multi-agent message transcripts before dispatching downstream tasks
- Mitigating attention dilution and instruction forgetting in high-capacity LLMs
- Staying within hard token budget ceilings while preserving critical grounding facts

## Core Rules

- **Five-Tier Token Budget Allocation**:
  - Context capacity must be partitioned into strict deterministic slices:
    1. *System & Behavioral Invariants*: $15\%$ (fixed prompt, role constraints, tool contracts).
    2. *Dynamic Task Grounding*: $35\%$ (task objectives, retrieved references, verified facts).
    3. *Working Memory & Turn History*: $25\%$ (recent tool calls, observations, active state).
    4. *Scratchpad & Intermediate Reasoning*: $10\%$ (scratch notes, plan checklists).
    5. *Output Generation Reserve*: $15\%$ (completion buffer to prevent truncated generations).
- **Lost-in-the-Middle Priority Ordering**:
  - Frontier LLMs demonstrate highest attention retrieval accuracy at the extreme prompt boundaries (primacy and recency effects).
  - *Boundary Placement*: Position mandatory constraints, system instructions, and schema definitions at the very top ($0\%-15\%$).
  - *Recency Placement*: Position current turn objective, active input parameters, and explicit completion format triggers at the very bottom ($85\%-100\%$).
  - *Middle Zone*: Confine secondary reference data, supporting documentation, and historical tool logs to the central window ($15\%-85\%$).
- **Semantic & Syntactic Deduplication**:
  - Compute sliding 4-gram overlaps across retrieved documents; drop paragraphs with $> 70\%$ verbatim overlap.
  - Apply vector cosine thresholding: if $\text{sim}(e_a, e_b) \ge 0.88$, merge or discard the lower-relevance passage.
- **Relevance Density Scoring**:
  - Every injected token must contribute directly to task resolution:
    $$\text{Density} = \frac{\text{Entity and Assertion Token Count}}{\text{Total Segment Token Count}}$$
  - Strip markdown decorative wrappers, repeated navigation headers, and verbose boilerplate when density falls below $0.40$.
- **Context Engineering 2026 (Anthropic-aligned)**:
  - *Context rot is real*: performance degrades as the window fills with low-value tokens — treat context as a scarce runtime resource, not free capacity.
  - *Compaction over overflow*: near the window limit, summarize the conversation and reinitialize a fresh context; keep raw records with stable identifiers so compaction is recoverable.
  - *Just-in-time retrieval over pre-loading*: fetch context at the moment of need via tools instead of stuffing everything upfront.
  - *Durable notes over transcript replay*: persist structured notes/memory files (decisions, entity IDs, task state) outside the window; hydrate new sessions from notes, never full raw transcripts.
  - *Sub-agent isolation*: dispatch heavy reading to fresh-context sub-agents; return only distilled results to the orchestrator window.

## Suggested Process

1. **Calculate In-Flight Token Consumption**:
   - Tokenize prompt components using target model tokenizers (e.g. tiktoken cl100k or o200k).
   - Evaluate available window margin against output reserve requirements.
2. **Prune and Deduplicate Ingested Content**:
   - Run n-gram and semantic similarity deduplication across candidate context passages.
   - Collapse repetitious error logs, stack traces, and identical tool call arguments into summarized counts.
3. **Restructure Passage Sequences**:
   - Reorder retrieved documents: place highest-relevance evidence at the top and immediate query grounding at the bottom.
   - Isolate secondary background material in the middle tier.
4. **Compress Conversation and Memory Turns**:
   - For dialogues exceeding 8 turns, summarize completed subtask milestones into an immutable context summary.
   - Retain only the last 3 turns of verbatim raw tool invocations and results.
5. **Verify Context Integrity**:
   - Verify that all schema requirements, critical entity IDs, and active task objectives survived pruning.

## Output Contracts

When context optimization produces structured task dispatches or plans, emit `contracts/schemas/coordination-plan.json`:
- `plan_id`: Unique identifier for the optimized orchestration dispatch.
- `phases`: Sliced execution stages respecting token budget allocations.
- `handoffs`: Minimized context payloads carrying only verified entity references.

## Failure Modes

- **Lost-in-the-Middle Forgetting**: Placing critical safety constraints in the center of a 100k token window where attention fades. Mitigation: anchor non-negotiable rules at the top and repeat key invariants directly preceding the final user prompt.
- **Aggressive Over-Pruning**: Truncating necessary domain terminology or schema fields during compression. Mitigation: preserve structured contract JSON definitions intact; compress only unstructured prose.
- **Context Window Thrashing**: Expanding and contracting context dynamically between turns, causing unstable cache hit rates. Mitigation: standardize static prompt prefix boundaries to leverage prefix prompt caching.
- **Boilerplate Token Bloat**: Passing raw web HTML or unparsed API responses into context. Mitigation: extract pure text and structured data tables prior to prompt assembly.

## Checklist

- [ ] Token budget partitions configured (system, grounding, memory, scratchpad, reserve)
- [ ] Output generation reserve of at least 15% preserved to prevent response truncation
- [ ] Primacy and recency ordering verified: critical rules at top, immediate task trigger at bottom
- [ ] Syntactic n-gram and semantic similarity deduplication applied to retrieved documents
- [ ] Conversation history older than 3 turns compressed into milestone summaries
- [ ] Static system prompt prefixes kept stable across turns to maximize prefix caching
- [ ] Raw JSON and stack traces stripped of redundant whitespace and repeated log lines
- [ ] Compaction with recoverable raw records replaces blind truncation near window limits
- [ ] Just-in-time retrieval preferred over pre-loading; durable notes hydrate new sessions instead of transcript replay
- [ ] Verified that all essential entity IDs, URLs, and contract requirements remain intact

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: pruning or reordering promotes middle-zone untrusted content toward the prompt boundary while dropping the system invariants that constrain it. Mitigation: never compress, relocate, or trim the system-and-invariants tier; keep untrusted content confined to the middle zone inside its delimiters.
- **ASI04 Supply Chain**: token counts computed with a different tokenizer than the target model (or an unpinned embedding model for cosine dedup) silently mis-size every budget slice. Mitigation: pin the tokenizer version (cl100k/o200k) matching the deployed model and use one pinned embedding model for similarity scoring.
- **ASI06 Context & Memory Poisoning**: density scoring strips provenance tags and trust delimiters from retrieved passages, erasing the trusted/untrusted boundary in the assembled window. Mitigation: exclude trust markers and provenance metadata from density scoring; never strip `<untrusted_data>` wrappers during compression.
- **ASI07 Inter-Agent Communication**: summarized handoff payloads pass unverified facts downstream as established grounding. Mitigation: `handoffs` in `coordination-plan.json` must carry only verified entity references and preserve the fact/assumption boundary for receiving agents.
- **ASI09 Human-Agent Trust Exploitation**: reporting token savings while critical schema fields or entity IDs were truncated during pruning. Mitigation: complete the integrity verification (schema requirements, entity IDs, active objectives survived) before reporting any savings figure.

## Related Skills

- **agent-tool-orchestration**: Coordinating tool executions within token-bounded contexts.
- **agent-graph-orchestration**: Orchestrating multi-agent state machines across bounded context nodes.
- **agent-evaluation**: Evaluating agent reasoning performance under varying context lengths.
- **prompt-injection-defense**: Sanitizing and delimiting untrusted inputs within optimized context boundaries.
- **systematic-debugging**: Diagnosing context leakage and token exhaustion failures.
