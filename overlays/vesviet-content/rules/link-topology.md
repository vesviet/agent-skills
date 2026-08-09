# Hub-and-Spoke Internal Link Topology

This rule defines the mandatory internal linking architecture for `vesviet` to ensure optimal link equity distribution and eliminate orphan pages.

## Core Principle
All content must be organized into a Hub-and-Spoke architecture. No page should exist in isolation (Zero Orphan Policy).

## The 10 Anchor Pillar Hubs
There are 10 core hubs that anchor the site:
1. `go-microservices.md` — Go & Microservices Architecture Hub
2. `architecting-21-service-ecommerce-golang-ddd.md` — System Design & E-Commerce Hub
3. `aws-eks-vs-ecs-comparison.md` — Cloud Native & Container Infrastructure Hub
4. `banking-microservices-architecture.md` — FinTech & Core Banking Systems Hub
5. `cloudflare-d1-durable-objects-realtime-cart.md` — Edge Serverless & Cloudflare Hub
6. `deploying-astro-on-cloudflare-full-stack-edge-architecture.md` — AI Frontend & Edge Hub
7. `generative-ui-with-mcp-ai-native-frontend.md` — Generative UI & MCP Engineering Hub
8. `alipay-double-11-architecture-tps.md` — Distributed Systems & High Concurrency Hub
9. `reading-map.md` — Sitewide Curated Learning Directory Hub
10. `hire.md` — Commercial Architecture Consulting Conversion Hub

## Link Injection Requirements
- **Spokes to Hubs**: Every new series sub-article, daily radar briefing, or standalone post MUST include an internal link pointing up to at least one relevant Anchor Pillar Hub.
- **Hubs to Spokes**: Hub pages must curate and link down to their respective spokes.
- **Cross-Linking**: Use contextually relevant anchor text. Avoid repetitive boilerplate links (e.g., diversify "Hire Me" anchor text with "Consult on Go Microservices").

## Orphan Elimination
- The SEO Analyst must run crawler verifications before publishing to ensure **0 orphan pages** remain in the repository.
