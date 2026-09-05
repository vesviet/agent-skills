---
name: generate-mmo-content
description: Use AI APIs to procedurally generate landing pages, creatives, and spin content for large-scale campaign deployment at scale. Use when launching new creatives, scaling content volume for A/B testing, or refreshing ad sets. Includes hard caps on API usage.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
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

## Output Contracts

When the generated content is consumed by a content scheduler, a landing
page pipeline, or a cross-role handoff, emit:

- **`contracts/schemas/content-handoff.json`** (or, when a stable schema is not yet available, a markdown frontmatter block listing `asset_type`, `channel`, `target_audience`, `compliance_boundary`, and `human_review_status`). The frontmatter block is the minimum-viable contract.
- For human-readable reports, the markdown content brief already documented is the canonical format.
- Every AI-generated asset must be flagged with the human review status; never publish without explicit sign-off.

Skip emission for single-asset experiments that do not cross a role boundary.

## Failure Modes

- **AI asset published unreviewed**: an AI-generated landing page or creative ships without human review. Mitigation: enforce the human review gate; reject unreviewed assets.
- **Compliance boundary crossed**: an asset violates the documented Legal & Compliance Notice. Mitigation: keep the compliance boundary visible; reject any pattern outside the boundary.
- **Off-brand voice**: the generated copy drifts from the brand voice. Mitigation: validate the voice against the brand guidelines; reject assets that drift.
- **Fact invented**: a claim appears in the asset that is not sourced. Mitigation: trace every claim to a primary source; flag unsourced claims as drafts.
- **Token budget exceeded**: AI generation runs past the declared budget. Mitigation: enforce the budget gate; halt generation on breach and surface the alert.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a generated asset may try to reframe the campaign goal through off-brand copy. Cross-check the asset against the declared campaign objective.
- **ASI03 Identity & Privilege Abuse**: never include customer identifiers, internal hostnames, or credential patterns in generated assets.
- **ASI04 Supply Chain**: AI generation libraries and brand-voice validators must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct AI prompts, landing page templates, or creative payloads from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the asset handoff is consumed by content schedulers and marketing roles; emit a structured contract so each consumer can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI-generated asset as "ready to publish" without the human review sign-off; surface the AI provenance honestly.

## Related Skills

- **setup-deployment**: Deploy generated landing pages to a CDN or hosting provider.
- **analyze-campaign-roi**: Factor AI API costs into the total campaign ROI calculation.
