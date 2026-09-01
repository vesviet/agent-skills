---
name: configure-llms-txt
description: Create and maintain the llms.txt and llms-full.txt files for a domain or project, making documentation and content discoverable by AI agents, LLMs, and automated tools per the llmstxt.org specification. Use when a site or API has AI agent interfaces, when optimizing for Generative Engine Optimization (GEO) and Agentic SEO (A-SEO), or when implementing the dual-audience documentation standard required by technical-writer role.
---

# Configure llms.txt

Use this skill to implement the `llms.txt` standard for any domain that serves documentation, APIs, or content that AI agents, LLMs, or automated tools should be able to discover and ingest efficiently.

## When to Use

- a site/API has AI agent interfaces
- optimizing for GEO / Agentic SEO
- implementing dual-audience doc standard
- creating llms.txt / llms-full.txt

## Core Rules

- **Placement**: host at `/llms.txt` at the root of the domain — not in a subdirectory; scope sub-paths with `rel="describedby"` HTTP `Link` headers when hosting per-section manifests
- **Format**: strictly follow the llmstxt.org v2 Markdown structure: `# Project Name` → `> blockquote summary` → `## Sections` → `- [Title](url.md): one-sentence description`; no HTML, no nav chrome, no promotional copy
- **Token budget**: keep `/llms.txt` under **50 KB (~10K tokens)** to prevent context exhaustion in multi-turn agent sessions; defer full text to `/llms-full.txt`
- **Required elements**: H1 heading, factual blockquote summary (no marketing language), curated content inventory with `.md` or clean-text endpoint URLs
- **HTTP header discovery parity** (v2 spec): every served HTML page SHOULD emit `Link: </docs/page.md>; rel="alternate"; type="text/markdown"` and `Link: </llms.txt>; rel="describedby"` response headers so agents discover the manifest without a separate crawl
- **Not a permissions file**: `llms.txt` manages discoverability — use `robots.txt` for access control; never conflate them
- **Automated maintenance via CI**: treat `llms.txt` as a living document; a CI pipeline must validate every linked URL resolves to a clean Markdown endpoint and auto-commit updates when docs change
- **DUAL-AUDIENCE LOCK**: for any system with AI agent interfaces, `llms.txt` is a mandatory deliverable; link `/.well-known/api-catalog` (RFC 9727), `/.well-known/agent-card.json` (A2A 1.0), and MCP server cards when present — HTML-only documentation without `llms.txt` is a documentation failure

## File Structure Specification (llmstxt.org)

### Minimal `llms.txt`

```markdown
# Project Name

> One-paragraph blockquote summary of what this project/site is, its purpose,
> primary audience, and key concepts. Written for LLM context ingestion —
> precise, factual, no marketing language.

## Key Sections

- [Getting Started](https://example.com/docs/getting-started): Installation and first steps
- [API Reference](https://example.com/docs/api): Full API endpoint documentation
- [Concepts](https://example.com/docs/concepts): Core architectural concepts
- [Changelog](https://example.com/changelog): Version history

## Agent Interfaces (when applicable)

- [Agent Card](https://example.com/.well-known/agent-card.json): A2A 1.0 agent discovery
- [API Catalog](https://example.com/.well-known/api-catalog): RFC 9727 API discovery
- [MCP Server](https://example.com/.well-known/mcp/server-card.json): MCP server card
```

### `llms-full.txt` (companion file)

Full-text version: concatenate all primary documentation pages in Markdown format. Used by LLMs that can ingest large context in a single request.

```bash
# Auto-generate llms-full.txt from docs directory
find docs/ -name "*.md" | sort | while read f; do
  echo "# File: $f"
  cat "$f"
  echo ""
  echo "---"
done > public/llms-full.txt
```

## Suggested Process

### Astro
```javascript
// astro.config.mjs — static llms.txt
// Place llms.txt in public/ directory
// Astro serves public/ directly at root
// public/llms.txt → example.com/llms.txt
```

### Next.js
```javascript
// app/llms.txt/route.ts
export async function GET() {
  const content = generateLlmsTxt(); // dynamic generation from content index
  return new Response(content, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
}
```

### Workers (Cloudflare)
```typescript
// In worker handler
if (url.pathname === '/llms.txt') {
  return new Response(LLMS_TXT_CONTENT, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' }
  });
}
```

### Static sites (Hugo, Jekyll)
Place in the `static/` directory (Hugo) or root (Jekyll). CI auto-generates via build script.

## CI Automation (keep llms.txt fresh)

```yaml
# .github/workflows/update-llms-txt.yml
name: Update llms.txt
on:
  push:
    paths: ['docs/**', 'content/**', 'src/pages/**']
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Regenerate llms.txt
        run: node scripts/generate-llms-txt.js
      - name: Commit if changed
        run: |
          git diff --exit-code public/llms.txt || (git add public/llms.txt && git commit -m "chore: update llms.txt")
```

## Checklist

- [ ] `/llms.txt` accessible at domain root (not subdirectory)
- [ ] H1 heading = project/site name
- [ ] Blockquote summary is factual and machine-readable (no marketing language)
- [ ] All primary doc paths listed with accurate URLs
- [ ] Agent interfaces section present if system has `agent-card.json`, `api-catalog`, or MCP server
- [ ] `/llms-full.txt` generated if content volume > 50KB total
- [ ] `llms.txt` linked from `robots.txt` (recommended for discoverability)
- [ ] Automated CI update configured so `llms.txt` stays current on doc changes
- [ ] Verified: AI crawlers can access (no robots.txt block, no auth wall)
- [ ] Tested: fetch `curl https://yourdomain.com/llms.txt` returns valid content

## Output Format

- `/public/llms.txt` or `/static/llms.txt` — deployed at domain root
- `/public/llms-full.txt` — companion full-text (optional but recommended)
- Updated `robots.txt` with `llms.txt` reference

## Output Contracts

When the `llms.txt` / `llms-full.txt` change is consumed by an AI agent,
a doc site, or a CI gate, emit:

- **`contracts/schemas/documentation-handoff.json`** with the manifest path, the `schema_version`, the include/exclude list, and the validation timestamp.
- For human-readable reports, a markdown diff of the manifest is sufficient.

Skip emission for trivial manifest updates that do not cross a role boundary.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: external links in the manifest must be validated against the live target; treat 404s as a CI failure.
- **ASI05 RCE Guard**: never construct the manifest from external or user-supplied content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the manifest is consumed by external AI agents; treat it as a public contract and review all changes before publish.
- **ASI09 Human-Agent Trust Exploitation**: do not present a manifest as "AI-ready" without a successful schema validation run.

## Related Skills

- **write-documentation**: produces the docs that `llms.txt` indexes
- **manage-api-catalog**: RFC 9727 API catalog should be linked from `llms.txt`
- **optimize-seo**: GEO/AEO strategy depends on `llms.txt` as a discoverability primitive
- **configure-agent-headers**: `agent-card.json` endpoint referenced in `llms.txt`
