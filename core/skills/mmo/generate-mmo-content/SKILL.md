---
name: generate-mmo-content
description: Use AI APIs to procedurally generate landing pages, creatives, and spin content for large-scale campaign deployment at scale. Use when launching new creatives, scaling content volume for A/B testing, or refreshing ad sets. Includes hard caps on API usage.
---

# Generate MMO Content

Use this skill to automate the creation of marketing assets at scale, allowing rapid testing of hundreds of angles, landing pages, and creatives without manual intervention.

## Legal & Compliance Notice

Generating large volumes of near-duplicate ad copy/creatives specifically to bypass a platform's duplicate-content or ad-review filters can violate platform advertising policies even when each individual piece is legal content. This skill's automation mechanics are content-neutral; the `COMPLIANCE-LOCK` rule below is a floor, not a ceiling — confirm the target platform's advertising policy permits the intended volume/variation strategy before scaling a spin run.

## When to Use

- launching new ad creatives or refreshing ad sets at volume
- spinning ad copy into hundreds of unique variations for A/B tests
- procedurally generating landing pages for keyword segments
- producing varied visuals via image-gen or templating APIs
- any run that needs a hard API budget cap before execution

## Example (spin with a hard budget cap)

```python
import openai, sys

MAX_TOKENS = 50_000
used = 0
for angle in angles:
    if used >= MAX_TOKENS:
        print("Budget-Lock: token cap reached, stopping.")
        sys.exit(0)
    r = openai.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=500,
        messages=[{"role": "user", "content": f"Rewrite this ad for {angle}: {base}"}],
    )
    used += r.usage.total_tokens
```

## Core Rules

- **BUDGET-LOCK**: Always implement hard limits (e.g., max token count, max API calls per script run) to prevent infinite loops from draining API budgets. Budget caps MUST be enforced in code, not documentation only.
- **COMPLIANCE-LOCK**: Even in MMO contexts, ensure generated content does not violate extreme legal boundaries (e.g., phishing, prohibited financial products, GDPR data misuse).
- **MULTI-MODEL-FALLBACK**: Configure fallback routing across LLM providers (primary: OpenAI GPT-4o, secondary: Anthropic Claude, fallback: Google Gemini) to ensure generation uptime when any single provider hits rate limits or outages.
- **EU-AI-ACT-DISCLOSURE**: Per EU AI Act Article 50, AI-generated ad content distributed in the EU MUST include a disclosure that it was produced by AI where the content is not obviously AI-generated. Do not generate or deploy ad creatives targeting EU audiences without an appropriate disclosure mechanism.
- **SEMANTIC-DISTINCTIVENESS**: Content variations MUST be semantically distinct (different structure, angle, or value proposition) — not just character-level synonym substitution. Platforms detect shallow spinning with embedding-based similarity checks.

## Suggested Process

1. **Procedural Generation**: Use LLMs (OpenAI, Gemini, Anthropic) with configured multi-model fallback to rewrite or "spin" ad copy into distinct variations for genuine A/B testing. Confirm variation volume and strategy comply with the target platform's advertising policy.
2. **EU AI Act Compliance Check**: Verify whether target audiences are in the EU and apply disclosure metadata or visible disclosure to generated creative content accordingly.
3. **Landing Page Generation**: Procedurally generate static HTML/CSS landing pages tailored to specific keywords or audience segments.
4. **Creative Automation**: Integrate with image generation APIs or templating systems to produce varied ad visuals.
5. **Budget Guardrailing**: Inject circuit breakers in the code to stop execution if API costs exceed a predefined threshold.

## Checklist

- [ ] Content generation script handles rate limits and API errors gracefully.
- [ ] Hard caps on API usage (Budget-Lock) are implemented in the code.
- [ ] Multi-model fallback configured (OpenAI → Anthropic → Gemini) for generation uptime.
- [ ] EU AI Act Article 50 disclosure applied for EU-targeted ad creatives.
- [ ] Output variations are semantically distinct, not shallow synonym substitutions.
- [ ] Generated artifacts properly formatted and ready for deployment.
- [ ] API cost for this run is within the declared budget cap.
- [ ] Generated content does not violate compliance rules (no phishing or prohibited content).

## Related Skills

- **setup-deployment**: Deploy generated landing pages to a CDN or hosting provider.
- **analyze-campaign-roi**: Factor AI API costs into the total campaign ROI calculation.
