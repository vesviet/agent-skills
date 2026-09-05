# Anti-AI Style Guide & Natural Cadence Standards

Reference guide for `write-article` and the `content-writer` role. This specification establishes actionable rules to eliminate robotic AI writing patterns, mandate empirical voice, and achieve human-grade sentence burstiness and perplexity.

---

## 1. Prohibited AI Clichés Blacklist

The following words and expressions are strictly prohibited in technical, architectural, and thought leadership articles. Their presence triggers immediate rejection during editorial review:

### English Blacklist
- **Verbs**: delve, unlock, harness, foster, revolutionize, elevate, underpin, shed light on, demystify, embark, empower.
- **Nouns**: tapestry, testament, realm, cornerstone, pinnacle, beacon, paradigm, synergy, game-changer, landscape (used abstractly, e.g., "navigating the cloud landscape").
- **Adjectives**: crucial, pivotal, multifaceted, intertwined, ever-evolving, groundbreaking, paramount, vibrant, paramount, seamless.
- **Transition Phrases**: "In conclusion", "At the end of the day", "It is important to remember", "In today's fast-paced digital world", "Needless to say", "A testament to".

### Vietnamese Equivalent Blacklist
- "Đi sâu vào" (delve into), "Bức tranh toàn cảnh" (tapestry/landscape), "Minh chứng cho" (testament to), "Mở khóa" (unlock), "Bước ngoặt / Kẻ thay đổi cuộc chơi" (game-changer), "Ngọn hải đăng" (beacon), "Không ngừng phát triển" (ever-evolving), "Cần lưu ý rằng" (it is important to remember).

---

## 2. Sentence Cadence & 20/60/20 Burstiness Rule

AI language models default to low-perplexity, uniform sentence lengths (averaging 15–20 words monotonously), creating a flat, hypnotic drone. Human writing exhibits high sentence burstiness.

All drafts must satisfy the **20/60/20 sentence distribution**:
- **~20% Short Sentences (< 12 words)**: Deliver emphatic conclusions, direct BLUF answers, punchy transitions, and clear boundaries.
- **~60% Medium Sentences (12–25 words)**: Explain mechanisms, link cause and effect, and describe standard implementation steps.
- **~20% Long / Complex Sentences (> 25 words)**: Articulate nuanced engineering trade-offs, multi-variable constraints, or comparative benchmarks.

### Cadence Evaluation Metric
- Standard deviation of sentence length across any 500-word block must be $\ge 6.5$ words.
- Monotonous blocks (three consecutive sentences within $\pm 2$ words of each other) must be broken up during editorial pass.

---

## 3. Active Voice & Subject Agency Mandate (>= 85%)

- At least **85%** of sentences must use active voice where the actor (engineer, compiler, kernel, cache, system) directly performs the action.
- Eliminate passive evasion where responsibility is obscured (e.g., "Latency was observed to be increased" -> "The garbage collector introduced 120ms stop-the-world pauses").
- Reserve passive voice exclusively when the recipient of the action is the explicit focal topic or the actor is genuinely unknown.

---

## 4. Before vs. After Rewrite Exemplars

| Dimension | AI Cliché Draft (Reject) | Senior Engineer Voice (Approved) |
| :--- | :--- | :--- |
| **Intro / Hook** | In today's fast-paced digital landscape, microservices stand as a testament to modern engineering, unlocking unprecedented agility. | Monolithic architectures fail when team count exceeds thirty engineers. Microservices decouple deployment pipelines at the cost of network latency. |
| **Explanation** | Let us delve into how distributed caching fosters seamless performance across multifaceted cloud environments. | Redis read replicas absorb 85,000 QPS of read traffic, preventing PostgreSQL connection pool exhaustion during traffic spikes. |
| **Trade-offs** | It is crucial to remember that distributed transactions require careful navigation of complex trade-offs. | Two-phase commit guarantees consistency across shards but spikes p99 write latency from 12ms to 180ms under high network jitter. |
| **Conclusion** | In conclusion, adopting event-driven architecture is a pivotal game-changer that elevates developer productivity. | Event sourcing provides an immutable audit log and zero-loss replays. Do not adopt it unless your domain requires temporal event queries. |
