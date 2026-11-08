# llms.txt & llms-full.txt Standard Specification (2026)

## 1. Specification Overview (llmstxt.org v2)

The `llms.txt` standard specifies how websites, APIs, and software documentation provide machine-readable discovery interfaces optimized for AI agents and LLMs.

```
Domain Root (/)
  ├── /llms.txt          # Concise, token-budgeted index & section manifest
  ├── /llms-full.txt     # Concatenated full-text corpus for long-context models
  └── /.well-known/      # Machine discovery (api-catalog, agent-card, mcp)
```

## 2. Structural Requirements for `/llms.txt`

1. **Title H1**: `# Project or Product Name`
2. **Blockquote Summary**: `> Factual, dense summary of project architecture and purpose. No marketing fluff.`
3. **Sections H2**: Categorized navigation links (`## Core Documentation`, ## API Reference`, `## Agent Interfaces`).
4. **Link Pattern**: `- [Page Title](https://example.com/docs/page.md): Concise description of content.`
5. **v2 Link Relations**:
   - HTTP Header: `Link: </llms.txt>; rel="describedby"`
   - HTML Header: `<link rel="alternate" type="text/markdown" href="/docs/page.md">`

## 3. High-Context Ingestion (`/llms-full.txt`)

For frontier LLMs with 1M+ context windows:
- Concatenates authoritative markdown source files in dependency order.
- Each section preceded by `# File: /path/to/source.md` delimiter.
- Strict exclusion of interactive widgets, raw binary embeds, or duplicated header navigation chrome.

## 4. Agentic Interface Discovery

When a platform supports agentic protocols, `llms.txt` must explicitly index:
- `/.well-known/agent-card.json`: A2A 1.0 agent discovery.
- `/.well-known/api-catalog`: RFC 9727 API discovery.
- `/.well-known/mcp/server-card.json`: Model Context Protocol server capabilities.
- `/.well-known/ucp`: Universal Commerce Protocol checkout capabilities.
