# Publish Log & AI Visibility Tracking

Conventions for post-publish operational tracking. Once an article is published, the `content-writer` or `seo-analyst` must log it to ensure technical implementation and visibility tracking occurs.

## 1. Publish Log Data Points

For every published article, record:
- **Date Published**
- **Target Keyword & Search Intent**
- **Live URL Slug**
- **Pillar/Cluster Mapping**
- **Internal Links Used** (Source and Target)

## 2. Schema Implementation Hand-off

- The `seo-analyst` must define the JSON-LD schema requirements (e.g., `Article`, `Review`, `RealEstateListing`, `FAQPage`) in the `seo-metadata.json`.
- The **Frontend Developer** is strictly responsible for implementing this JSON-LD schema into the codebase or CMS template based on the Analyst's spec.

## 3. Weekly AI Visibility Tracking (Rollup)

Traditional SEO tracking (Google Search Console impressions/clicks) is no longer sufficient. 
- **Weekly Task:** The `seo-analyst` must conduct a Weekly Rollup to track **AI Visibility**.
- **Metrics to Track:** Verify if the newly published URLs are being cited or extracted in:
  1. Google AI Overviews (SGE)
  2. Perplexity AI Search
  3. ChatGPT / SearchGPT
- **Feedback Loop:** If visibility is low, adjust the `fact density` and `answer-first` structural rules for the next sprint.
