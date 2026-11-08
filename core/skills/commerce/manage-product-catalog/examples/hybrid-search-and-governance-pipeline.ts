/**
 * Hybrid Search (RRF) & AI Content Governance Pipeline
 *
 * Implements:
 * - Reciprocal Rank Fusion (RRF) combining BM25 keyword ranking and pgvector dense cosine search
 * - Human-in-the-Loop AI content governance review gate
 * - Brand voice linter detecting disallowed claims prior to publishing
 */

export interface ProductCatalogItem {
  id: string;
  sku: string;
  title: string;
  description: string;
  status: 'draft' | 'pending_review' | 'published';
  embedding: number[];
  governanceMetadata?: {
    model: string;
    promptHash: string;
    reviewedBy?: string;
    reviewedAt?: string;
    bannedWordsPassed: boolean;
  };
}

export interface SearchResult {
  productId: string;
  title: string;
  score: number;
}

export class HybridSearchPipeline {
  private readonly RRF_K = 60;

  /**
   * Computes Reciprocal Rank Fusion across BM25 and Dense Vector ranking lists.
   */
  public computeRrf(
    bm25RankedIds: string[],
    denseRankedIds: string[]
  ): Array<{ productId: string; rrfScore: number }> {
    const scores = new Map<string, number>();

    // Accumulate BM25 reciprocal ranks
    bm25RankedIds.forEach((id, rankIndex) => {
      const rank = rankIndex + 1;
      const current = scores.get(id) || 0;
      scores.set(id, current + 1 / (this.RRF_K + rank));
    });

    // Accumulate Dense Vector reciprocal ranks
    denseRankedIds.forEach((id, rankIndex) => {
      const rank = rankIndex + 1;
      const current = scores.get(id) || 0;
      scores.set(id, current + 1 / (this.RRF_K + rank));
    });

    // Sort by combined RRF score descending
    return Array.from(scores.entries())
      .map(([productId, rrfScore]) => ({ productId, rrfScore }))
      .sort((a, b) => b.rrfScore - a.rrfScore);
  }
}

export class ProductGovernanceEngine {
  private readonly BANNED_TERMS = [
    'miracle cure',
    'guaranteed 100% profit',
    'risk-free',
    'FDA approved without clinical trial',
  ];

  /**
   * Pre-review automated brand voice and regulatory linter.
   */
  public lintProductCopy(description: string): { passed: boolean; violations: string[] } {
    const violations: string[] = [];
    const lower = description.toLowerCase();

    for (const term of this.BANNED_TERMS) {
      if (lower.includes(term)) {
        violations.push(term);
      }
    }

    return {
      passed: violations.length === 0,
      violations,
    };
  }

  /**
   * Approves transition from draft to published, enforcing mandatory human review.
   */
  public approveForPublish(
    item: ProductCatalogItem,
    reviewerId: string
  ): ProductCatalogItem {
    const lint = this.lintProductCopy(item.description);
    if (!lint.passed) {
      throw new Error(`Cannot publish product with regulatory violations: ${lint.violations.join(', ')}`);
    }

    if (!reviewerId || reviewerId.trim() === '') {
      throw new Error('Mandatory human reviewer ID required before publishing AI content');
    }

    return {
      ...item,
      status: 'published',
      governanceMetadata: {
        model: item.governanceMetadata?.model || 'manual',
        promptHash: item.governanceMetadata?.promptHash || 'n/a',
        reviewedBy: reviewerId,
        reviewedAt: new Date().toISOString(),
        bannedWordsPassed: true,
      },
    };
  }
}
