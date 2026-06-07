---
name: configure-agent-headers
description: Use when exposing RFC 8288 Link headers and DNS-AID configurations for agentic discovery.
---

# Configure Agent Headers

Use this skill to expose well-known endpoints natively via HTTP response headers and DNS.

## Core Rules
- Serve `Link: </.well-known/...>; rel="..."` headers (e.g., via Cloudflare Pages `_headers`).
- Ensure DNS-AID ServiceMode SVCB records are documented for domain operators.

## Suggested Process
1. Identify target endpoints (e.g., Auth metadata, API Catalog, Agent Skills).
2. Configure header injection patterns matching target server routing.
3. Validate header presence and rel types via curl requests.
4. Set up fallback DNS-AID ServiceMode records if domain operator requires it.

## Checklist
- [ ] Well-known endpoints are identified for header routing.
- [ ] Link headers conform to RFC 8288 standards.
- [ ] DNS-AID ServiceMode records are mapped and documented.
- [ ] Headers are verified on target deployment environments.
- [ ] Fallback responses are functional and secure.

## Related Skills
- **configure-oauth-metadata**: Wire up oauth-authorization-server block.
- **configure-mcp**: Set up model context server card endpoint.
- **manage-api-catalog**: Wire up linkset endpoints for API discovery.
