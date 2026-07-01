---
name: generate-mmo-content
description: Use AI APIs to procedurally generate landing pages, creatives, and spin content for large-scale campaign deployment at scale. Use when launching new creatives, scaling content volume for A/B testing, or refreshing ad sets. Includes hard caps on API usage.
---

# Generate MMO Content

Use this skill to automate the creation of marketing assets at scale, allowing rapid testing of hundreds of angles, landing pages, and creatives without manual intervention.

## Core Rules

- **BUDGET-LOCK**: Always implement hard limits (e.g., max token count, max API calls per script run) to prevent infinite loops from draining API budgets.
- **COMPLIANCE-LOCK**: Even in MMO contexts, ensure generated content does not violate extreme legal boundaries (e.g., phishing).

## Suggested Process

1. **Procedural Generation**: Use LLMs (OpenAI, Gemini, Anthropic) to rewrite or "spin" ad copy, creating hundreds of unique variations to bypass duplicate content filters.
2. **Landing Page Generation**: Procedurally generate static HTML/CSS landing pages tailored to specific keywords or audience segments.
3. **Creative Automation**: Integrate with image generation APIs or templating systems to produce varied ad visuals.
4. **Budget Guardrailing**: Inject circuit breakers in the code to stop execution if API costs exceed a predefined threshold.

## Checklist

- [ ] Content generation script handles rate limits and API errors gracefully.
- [ ] Hard caps on API usage (Budget-Lock) are implemented in the code.
- [ ] Output variations are sufficiently distinct to avoid basic duplicate content filters.
- [ ] Generated artifacts are properly formatted and ready for deployment.
- [ ] API cost for this run is within the declared budget cap.
- [ ] Generated content does not violate compliance rules (no phishing or prohibited content categories).

## Related Skills

- **setup-deployment**: Deploy generated landing pages to a CDN or hosting provider.
- **analyze-campaign-roi**: Factor AI API costs into the total campaign ROI calculation.
