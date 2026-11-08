# Programmatic SEO (pSEO) & Social Video Hook Specifications (2026)

## 1. Programmatic SEO (pSEO) Layout & Answer-First Standards

Modern search indexing and Google AI Overviews prioritize immediate, high-density factual answers (BLUF - Bottom Line Up Front):

```
┌────────────────────────────────────────────────────────┐
│   BLUF Answer Box (Above-the-fold, <= 60 words)        │
│   - Immediate factual verdict, key differentiator      │
├────────────────────────────────────────────────────────┤
│   JSON-LD Structured Data Schema                       │
│   - Product, Review, AggregateRating, FAQPage          │
├────────────────────────────────────────────────────────┤
│   High-Information-Gain Comparison Matrix              │
│   - Primary dataset specs, real benchmark metrics      │
├────────────────────────────────────────────────────────┤
│   FAQ Accordion & Deep Technical Specifications        │
└────────────────────────────────────────────────────────┘
```

## 2. JSON-LD Schema Invariants

Every programmatic landing page must inject valid schema markup:
- `@context`: `"https://schema.org"`
- `@type`: `"Product"` or `"ItemPage"`
- `review`: Valid review author and `ratingValue` ($\le 5.0$).
- `aggregateRating`: Real review counts and verified ratings.

## 3. Multimodal Social Video Hook Pacing (TikTok / Reels / Shorts)

High-converting direct-response social video scripts follow a strict 45–60s timeline:
1. **The 3-Second Hook (0–3s)**:
   - *Negative Framing*: "Stop doing X until you see this..."
   - *Pattern Interrupt*: Visual discrepancy or counter-intuitive demonstration.
   - *Curiosity Gap*: "The secret reason why..."
2. **Agitation & Friction (3–15s)**: Clarify the painful alternative.
3. **Product Demonstration & Unique Value (15–45s)**: Visual proof and solution delivery.
4. **Actionable Call-to-Action (45–60s)**: Clear, low-friction next step.
