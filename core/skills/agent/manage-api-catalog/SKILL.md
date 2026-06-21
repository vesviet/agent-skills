---
name: manage-api-catalog
description: Use when publishing and maintaining RFC 9727 API Catalog registries for automated API discovery by agents, developer tools, and client SDKs.
---

# Manage API Catalog

Use this skill to create and maintain the `/.well-known/api-catalog` Linkset file per RFC 9727. The API Catalog provides a machine-readable index of all public API endpoints, their OpenAPI specifications, and documentation URLs — enabling agent orchestrators and developer tooling to auto-discover a service's API surface without prior knowledge.

## Core Rules

- Format strictly according to RFC 9727 — the catalog is a Linkset document, not a generic JSON file.
- Map endpoints for OpenAPI specifications using `service-meta` relation type, and documentation using `service-doc`.
- The catalog MUST be placed at `/.well-known/api-catalog` (no `.json` extension per RFC 9727 spec).
- Serve with `Content-Type: application/linkset+json` or `application/linkset` as required by the request `Accept` header.
- Keep catalog entries stable — do not remove or rename existing `anchor` values once published; deprecate using the `status` field if the spec supports it.

## When to Use

- Publishing a new API service's endpoint catalog for agent discovery
- Adding a new API version or endpoint to an existing catalog
- Verifying that agent clients and developer tooling can correctly parse the Linkset format
- Making a service compliant with agentic discovery standards (RFC 9727 is referenced by WorkOS and `isitagentready.com`)
- Updating or deprecating catalog entries after API changes

## Suggested Process

1. **Collect API specs and docs**: Gather all OpenAPI spec file URLs (e.g., `https://api.example.com/openapi.yaml`) and human-readable documentation URLs (e.g., `https://docs.example.com/api/orders`) for each logical API group.

2. **Build the Linkset document**: Structure each API group as a Linkset object with `anchor` (the canonical base URL for the API) and the relevant `service-meta` and `service-doc` links:
   ```json
   {
     "linkset": [
       {
         "anchor": "https://api.example.com/v1",
         "service-meta": [{ "href": "https://api.example.com/openapi.yaml", "type": "application/yaml" }],
         "service-doc": [{ "href": "https://docs.example.com/api/v1", "type": "text/html" }]
       }
     ]
   }
   ```

3. **Place at well-known path**: Deploy the catalog to `/.well-known/api-catalog`. For Cloudflare Pages, add as `public/.well-known/api-catalog` (no extension, ensure routing doesn't add one). For Workers, serve from `GET /.well-known/api-catalog`.

4. **Configure response headers**: Set `Content-Type: application/linkset+json` on the response. Add `Access-Control-Allow-Origin: *` or scoped CORS headers for cross-origin agent fetches.

5. **Validate format**: Run `curl https://yourdomain.com/.well-known/api-catalog -H "Accept: application/linkset+json"` and confirm:
   - Response status `200 OK`
   - `Content-Type: application/linkset+json`
   - Valid JSON Linkset structure

6. **Wire up discovery**: Add a `Link` header via `configure-agent-headers` pointing to the catalog (`rel="https://www.iana.org/assignments/link-relations/api-catalog"`) so agent scanners find it passively.

7. **Verify in scanner**: Check that `isitagentready.com` (or equivalent) confirms the API catalog is readable.

## Output Format

- `/.well-known/api-catalog` — Linkset JSON document (no file extension)
- Response headers: `Content-Type: application/linkset+json`, `Access-Control-Allow-Origin`

## Checklist

- [ ] Catalog file uses Linkset format per RFC 9727 (not plain JSON or OpenAPI).
- [ ] All API groups have `anchor` values that match their canonical base URLs.
- [ ] OpenAPI spec URL (`service-meta`) is active, reachable, and returns valid spec.
- [ ] Documentation URL (`service-doc`) is reachable and human-readable.
- [ ] File exists at `/.well-known/api-catalog` (no `.json` extension).
- [ ] Linkset returns `Content-Type: application/linkset+json` response header.
- [ ] CORS headers allow cross-origin agent fetches.
- [ ] Link header pointing to catalog is configured via `configure-agent-headers`.
- [ ] Scanner (e.g., `isitagentready.com`) confirms catalog is readable.

## Related Skills

- **configure-agent-headers**: Expose the API catalog via HTTP Link headers for passive agent discovery.
- **configure-agent-skills**: Set up the Agent Skills index manifest for capability-level (not endpoint-level) discovery.
- **configure-mcp**: Set up the MCP server card — often deployed alongside the API catalog for dual-mode discovery.
\n### 2026: RFC 9727 and Catalog Versioning

- **RFC 9727 API Catalog implementation:** Publish `/.well-known/api-catalog` returning a `linkset+json` document with `anchor`, `href`, and `type: application/openapi+json` link relations for each API. This enables automated API discovery by agent orchestrators and developer tooling.
- **API catalog versioning:** Each catalog entry should include a `version` field and a `deprecated` boolean flag. Automated clients (agents, SDKs) use the catalog to select the highest non-deprecated version without human intervention.\n