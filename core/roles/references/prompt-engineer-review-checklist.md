## Prompt Engineer Review Checklist

This reference checklist provides detailed prompt architecture, context optimization, and safety boundary validation criteria for prompt engineering to meet 2026–2027 Agentic SWE standards.

### 1. Token Budget Allocation & Five-Tier Context Isolation
- **Window Budget Sizing**:
  - context window limits explicitly measured for target model architecture (e.g. 128k, 200k, 1M context limits)
  - maximum total context payload bounded at $\le 85\%$ of window capacity to prevent attention degradation
  - output generation reserve of at least 15% guaranteed and protected from context starvation
- **Five-Tier Allocation Enforced**:
  - System Core (15%): immutable role instructions, tool schemas, and core invariants
  - Domain Retrieval (40%): retrieved documents, database schemas, and external knowledge chunks
  - Dynamic History (20%): turn-by-turn conversational history and tool invocation records
  - Working Memory / Scratchpad (10%): active execution plan, task state, and intermediate reasoning
  - Output Reserve (15%): generation space for final response or structured JSON artifact

### 2. Attention Architecture & Lost-in-the-Middle Mitigation
- **Primacy Anchor Placement**:
  - immutable system identity, critical negative constraints, and security boundary locks placed in first 10% of window
  - tool calling specifications and core schemas anchored at the top of context
- **Recency Anchor Placement**:
  - target task prompt, current user instruction, and immediate output format constraints repeated at final 10%
  - critical schema reminders and output delimiter rules reiterated immediately before assistant generation turn
- **Middle Section Governance**:
  - middle window (20%–80%) reserved exclusively for passive reference context and retrieved evidence
  - no security policies, negative safety rules, or schema contracts buried in the middle zone

### 3. Prefix Caching Optimization & Prompt Determinism
- **Static Preamble Invariance**:
  - system prompt, tool definitions, and few-shot exemplars assembled into a static, deterministic prefix
  - no dynamic timestamps, request IDs, or session variables injected before static system blocks
- **Cache Boundary Alignment**:
  - prefix cache break points identified and aligned to model-specific token block boundaries (e.g. 1024 or 2048 token boundaries)
  - volatile data (user query, runtime context, session tokens) appended strictly after the cached prefix

### 4. Input Sanitization & Structural Delimiter Defense
- **XML/Tag Structural Isolation**:
  - untrusted user inputs and retrieved RAG chunks wrapped in unambiguous XML tags: `<untrusted_input id="...">...</untrusted_input>`
  - instructions explicitly direct the model to treat content within delimiters as passive data, never executable instructions
- **Escape & Neutralization**:
  - delimiter collision attacks neutralized: literal closing tags (`</untrusted_input>`) inside data sanitized or escaped
  - invisible Unicode characters, bidirectional override sequences, and homoglyph attacks stripped prior to assembly
- **Canary Token Monitoring**:
  - unique, ephemeral canary tokens embedded between prompt sections to detect prompt extraction or leakage
  - automated canary breach alerts wired to terminate execution if canary appears in model completion

### 5. Schema Binding & Structured Output Guarantees
- **JSON Schema Draft 2020-12 Conformance**:
  - structured output contracts bound directly to schema definitions in `contracts/schemas/*.json`
  - strict schema mode or constrained decoding flags enabled where supported by model runtime
- **Negative Schema Guidance**:
  - prompt explicitly forbids markdown code-fence wrappers when raw JSON is expected
  - null handling, default fallbacks, and enum constraints explicitly enumerated to prevent parsing crashes

### 6. Semantic Deduplication & Context Compression
- **Redundancy Elimination**:
  - multi-turn conversation histories pruned of duplicate tool call outputs and repetitive error traces
  - sliding window truncation or semantic compaction applied to conversations exceeding threshold length
- **Document Chunk Synthesis**:
  - retrieved RAG passages deduplicated across vector query results before prompt insertion
  - boilerplate headers, navigational menus, and repeated disclaimers stripped from reference documents

### 7. Empirical Benchmark Validation & Regression Gates
- **Evaluation Dataset Coverage**:
  - prompt changes evaluated against representative test suites covering typical cases, edge cases, and adversarial attacks
  - zero prompt modifications deployed without running automated evaluation harness
- **Quantitative Quality Thresholds**:
  - benchmark suite pass rate meets or exceeds $\ge 90\%$ target threshold
  - zero detected safety regressions, prompt leakage vulnerabilities, or contract violations
  - latency and token cost deltas measured and within approved operational budget
