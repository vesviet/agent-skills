# Token Budgeting & Attention Allocation Reference (2026)

## 1. Context Architecture & Attention Dynamics

Frontier LLMs exhibit non-uniform attention distributions across long context windows. The "lost-in-the-middle" effect degrades factual recall and constraint satisfaction when critical tokens reside in the central 15%–85% region of the prompt.

```
Token Attention Weight Profile
  1.0 ┌──────────                                       ──────────┐ (High Attention)
      │ Primacy (0-15%)                                 Recency (85-100%)
      │                                                           │
  0.5 │                                                           │
      │                  Lost in the Middle (15-85%)              │
      │                  ┌────────────────────────┐               │
  0.0 └──────────────────┴────────────────────────┴───────────────┴─► Token Index
```

## 2. Five-Tier Deterministic Token Budgeting

To prevent context exhaustion and token allocation starvation, total token budget $B$ is partitioned into five deterministic allocations:

1. **System & Security Invariants ($15\%$ of $B$)**:
   - Identity, immutable operating constraints, OWASP ASI guardrails, core tool signatures.
2. **Dynamic Task Grounding ($35\%$ of $B$)**:
   - Task requirements, retrieved code snippets, verified architectural evidence.
3. **Working State & Turn History ($25\%$ of $B$)**:
   - Rolling conversation turns, tool invocation outputs compressed via 20% Head / 80% Tail TOC.
4. **Intermediate Reasoning & Scratchpad ($10\%$ of $B$)**:
   - Chain-of-thought scratchpad, checklist state, verification assertions.
5. **Output Generation Reserve ($15\%$ of $B$)**:
   - Guaranteed completion buffer preventing truncated JSON contracts.

## 3. KV Prefix Cache Optimization

Assembling prompt sequences in volatility order maximizes hardware KV cache reuse:
- **Layer 1**: Static system rules (Shared across all requests - 100% hit rate).
- **Layer 2**: Role contracts & alphabetized tool schemas (Cache Breakpoint 1).
- **Layer 3**: Repository architecture cards & persistent guidelines (Cache Breakpoint 2).
- **Layer 4**: Anchored `compact-working-state.json` (Cache Breakpoint 3).
- **Layer 5**: Rolling conversation history with TOC (Cache Breakpoint 4).
- **Layer 6**: Dynamic turn user prompt & timestamps (Uncached).

## 4. Semantic Deduplication & Density Scoring

- **Cosine Similarity Threshold**: Prune document chunks with embedding similarity $\ge 0.88$.
- **N-gram Shingling**: Strip literal n-gram duplicates (>70% overlap across 8-word shingles).
- **Information Density Filter**: Rank sentences by entropy and named entity density; trim boilerplate prose while preserving contracts, types, and numbers.
