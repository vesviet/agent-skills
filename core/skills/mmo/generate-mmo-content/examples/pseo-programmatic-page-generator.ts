export interface ProductRecord {
  slug: string;
  name: string;
  category: string;
  priceUsd: number;
  rating: number;
  reviewCount: number;
  keyFeature: string;
  pros: string[];
  cons: string[];
  faqs: Array<{ question: string; answer: string }>;
}

export class PSeoPageGenerator {
  // Generates Answer-First BLUF summary (<= 60 words)
  public generateBluf(product: ProductRecord): string {
    return (
      `The ${product.name} stands out as the premier ${product.category} for value and performance. ` +
      `Scoring ${product.rating}/5 across ${product.reviewCount} verified benchmarks, it delivers ${product.keyFeature} ` +
      `at an accessible $${product.priceUsd} price point, outperforming comparable flagship alternatives.`
    );
  }

  // Injects JSON-LD structured data schema
  public generateJsonLd(product: ProductRecord): string {
    const schema = {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: product.name,
      description: `Comprehensive benchmark review and technical analysis of the ${product.name}.`,
      offers: {
        '@type': 'Offer',
        price: product.priceUsd,
        priceCurrency: 'USD',
        availability: 'https://schema.org/InStock',
      },
      aggregateRating: {
        '@type': 'AggregateRating',
        ratingValue: product.rating,
        reviewCount: product.reviewCount,
      },
    };
    return `<script type="application/ld+json">\n${JSON.stringify(schema, null, 2)}\n</script>`;
  }

  // Renders complete programmatic HTML landing page
  public renderPage(product: ProductRecord): string {
    const bluf = this.generateBluf(product);
    const jsonLd = this.generateJsonLd(product);

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${product.name} Review & Benchmarks (2026)</title>
  ${jsonLd}
</head>
<body>
  <main class="pseo-container">
    <h1>${product.name}: Comprehensive Benchmark & Analysis</h1>
    <section class="bluf-box" style="border: 1px solid #0284c7; padding: 16px; border-radius: 8px;">
      <p><strong>Quick Verdict:</strong> ${bluf}</p>
    </section>
    <section class="specs-grid">
      <h2>Specifications</h2>
      <ul>
        <li>Price: $${product.priceUsd}</li>
        <li>Rating: ${product.rating} / 5.0</li>
        <li>Core Advantage: ${product.keyFeature}</li>
      </ul>
    </section>
  </main>
</body>
</html>`;
  }
}
