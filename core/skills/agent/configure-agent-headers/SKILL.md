---
name: configure-agent-headers
description: Exposes well-known agentic endpoints via RFC 8288 HTTP Link headers and optional DNS-AID SVCB records, making a web service natively discoverable by AI agents without requiring dedicated well-known endpoint scans. Use when declaring agent-readiness (MCP server, API catalog, OAuth metadata, agent skills) on a Cloudflare Pages or Workers site without changing application routing.
---

# Configure Agent Headers

Use this skill to expose well-known agentic endpoints natively via HTTP response headers (RFC 8288 Link headers) and DNS Service Bindings (DNS-AID). This is the lowest-friction way to declare agent-readiness — no routing changes, no new pages, just headers and optional DNS records.

## Core Rules

- Serve `Link: </.well-known/...>; rel="..."` headers on all primary responses (especially `GET /`).
- Link header format MUST conform to RFC 8288 — use `rel` types that match the agentic discovery spec.
- DNS-AID SVCB records are optional but recommended for domain operators who want DNS-level discoverability.
- Headers must be set at the edge or CDN level — do not rely solely on origin application code which may not apply to all routes.
- Do not expose internal-only endpoints via Link headers. Only publicly accessible discovery endpoints.

## When to Use

- Making a Cloudflare Pages / Workers site agent-ready without changing application code
- Declaring MCP server presence, API catalog, agent skills manifest, or oauth metadata via headers
- Setting up DNS-AID for domain-level agent discoverability (enterprise or DNS-operator contexts)
- Verifying that an existing site already exposes correct Link headers for agentic scanners

## Suggested Process

1. **Identify target endpoints**: List all well-known paths to expose — typically a subset of: `/.well-known/mcp/server-card.json`, `/.well-known/api-catalog`, `/.well-known/agent-skills/index.json`, `/.well-known/oauth-protected-resource`, `/.well-known/oauth-authorization-server`.

2. **Choose header injection method**: For Cloudflare Pages, use the `_headers` file in `public/`. For Workers/Workers for Platforms, set headers in the worker response. For other CDNs, use their header injection config.

3. **Format Link headers**: Each well-known path needs its own `Link` header line with the correct `rel` type:
   ```
   /.well-known/mcp/server-card.json: rel="mcp-server-card"
   /.well-known/api-catalog: rel="https://www.iana.org/assignments/link-relations/api-catalog"
   /.well-known/oauth-authorization-server: rel="https://www.iana.org/assignments/link-relations/oauth-authorization-server"
   ```
   Refer to each spec for the canonical `rel` string.

4. **Deploy and verify**: Run `curl -I https://yourdomain.com/` and confirm the Link headers appear. Use `isitagentready.com` or a similar scanner to confirm agent-readable discovery.

5. **Configure DNS-AID (optional)**: Add `SVCB` records to the domain's DNS pointing to the agentic service metadata endpoint. Document the record values for the domain operator.

6. **Audit scope**: Check that no internal-only endpoints are leaked via Link headers. Review the list of exposed `rel` types against the domain's actual capabilities.

### 2026: Link Header Security and DNS-AID SVCB Adoption

- Link header security: when exposing `Link: <url>; rel="mcp-server"`, ensure the target URL is under your own domain; third-party URLs in Link headers can enable agent phishing attacks.
- DNS-AID SVCB adoption status: DNS-AID is still an IETF draft (not RFC) as of mid-2026; implement Link headers as primary discovery mechanism; DNS-AID only as supplementary signal for DNS-aware clients.

## Output Format

- `public/_headers` or worker response headers file with Link header entries
- DNS-AID SVCB record configuration (documentation for DNS operator, if needed)

## Checklist

- [ ] Well-known endpoints are identified and all publicly accessible.
- [ ] Link headers conform to RFC 8288 syntax — correct angle-bracket format and `rel` types.
- [ ] Headers appear on `GET /` response (verified via `curl -I`).
- [ ] DNS-AID SVCB records are documented if domain-level discovery is needed.
- [ ] No internal-only endpoints are exposed via Link headers.
- [ ] Link headers verified in target deployment environment (staging then production).
- [ ] `isitagentready.com` or equivalent scanner confirms headers are readable.
- [ ] Headers are set at edge, not just origin (so all routes receive them).

## Related Skills

- **configure-oauth-metadata**: Wire up the `oauth-authorization-server` and `oauth-protected-resource` endpoints that Link headers will point to.
- **configure-mcp**: Set up the MCP server card endpoint declared in Link headers.
- **manage-api-catalog**: Wire up the RFC 9727 API catalog endpoint declared in Link headers.
- **configure-agent-skills**: Set up the agent skills index manifest declared in Link headers.
