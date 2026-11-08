#!/usr/bin/env python3
"""Context Pruner and Reorderer (2026).

Applies semantic deduplication, token budgeting, and lost-in-the-middle
attention reordering to optimize context windows for frontier LLMs.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ContextChunk:
    chunk_id: str
    content: str
    relevance_score: float
    token_count: int
    is_mandatory: bool = False


class ContextOptimizer:
    def __init__(self, max_token_budget: int = 16000):
        self.max_budget = max_token_budget
        self.reserve_budget = int(max_token_budget * 0.15)  # 15% generation buffer
        self.usable_budget = max_token_budget - self.reserve_budget

    def prune_and_reorder(self, chunks: List[ContextChunk]) -> List[ContextChunk]:
        """Prunes low-relevance chunks and arranges optimal attention order."""
        # 1. Deduplicate identical or near-duplicate content
        seen_hashes = set()
        deduped: List[ContextChunk] = []
        for chunk in chunks:
            content_key = " ".join(chunk.content.strip().lower().split()[:20])
            if content_key not in seen_hashes:
                seen_hashes.add(content_key)
                deduped.append(chunk)

        # 2. Sort by relevance descending, respecting mandatory items
        deduped.sort(key=lambda c: (c.is_mandatory, c.relevance_score), reverse=True)

        # 3. Fit within usable budget
        selected: List[ContextChunk] = []
        current_tokens = 0
        for chunk in deduped:
            if current_tokens + chunk.token_count <= self.usable_budget:
                selected.append(chunk)
                current_tokens += chunk.token_count
            elif chunk.is_mandatory:
                selected.append(chunk)
                current_tokens += chunk.token_count

        # 4. Attention Reordering (Primacy & Recency placement)
        # Top-tier items go to Primacy (beginning) and Recency (end)
        # Lower-tier items placed in the center zone
        if len(selected) <= 2:
            return selected

        primacy_items: List[ContextChunk] = []
        recency_items: List[ContextChunk] = []
        middle_items: List[ContextChunk] = []

        for i, chunk in enumerate(selected):
            if i % 3 == 0:
                primacy_items.append(chunk)
            elif i % 3 == 1:
                recency_items.insert(0, chunk)
            else:
                middle_items.append(chunk)

        # Final order: Primacy -> Middle -> Recency
        return primacy_items + middle_items + recency_items


if __name__ == "__main__":
    optimizer = ContextOptimizer(max_token_budget=1000)
    sample_chunks = [
        ContextChunk("c1", "System Security Invariants: Zero trust credentials", 1.0, 150, True),
        ContextChunk("c2", "Background doc: Legacy migration history 2021", 0.4, 300),
        ContextChunk("c3", "Current API contract: POST /v1/checkout", 0.95, 200, True),
        ContextChunk("c4", "Optional feature notes: dark mode toggle", 0.2, 250),
    ]
    optimized = optimizer.prune_and_reorder(sample_chunks)
    print(f"Retained {len(optimized)} chunks in optimal attention sequence:")
    for idx, c in enumerate(optimized):
        print(f"  [{idx + 1}] {c.chunk_id} (Score: {c.relevance_score}, Tokens: {c.token_count})")
