---
name: configure-agent-skills
description: Creates and manages the agentskills.io manifest index at `/.well-known/agent-skills/index.json`, exposing structured API capabilities for agent orchestrators and capability-routing infrastructure to auto-discover and invoke. Use when registering, updating, or validating the skill manifest after adding or deprecating API endpoints on a service.
---

# Configure Agent Skills

Use this skill when exposing API capabilities or developer instructions through the Agent Skills manifest at `/.well-known/agent-skills/index.json`. This makes structured skill metadata discoverable by agent orchestrators, SDK clients, and capability-routing infrastructure that reads the agentskills.io schema.

## Core Rules

- The manifest MUST be placed at `/.well-known/agent-skills/index.json` at the domain root.
- The schema MUST conform to the version published by `agentskills.io` — validate before deployment.
- Each skill entry MUST have a unique `id` that is stable across versions — do not change IDs once published.
- The manifest MUST be served with `Content-Type: application/json` and appropriate CORS headers to allow agent clients to fetch it cross-origin.
- Version the manifest using the `schema_version` field so downstream agents can detect breaking changes.

## When to Use

- Registering API capabilities so agent orchestrators can auto-discover and invoke them
- Updating the skill manifest after adding or deprecating API endpoints
- Verifying that agent clients can correctly parse and route to the skills declared
- Migrating from an older skill manifest format to the current agentskills.io schema version

## Suggested Process

1. **Collect capabilities**: List all API endpoints or agent-callable operations to expose. Group by logical domain (e.g., `orders`, `products`, `agents`).

2. **Structure each skill entry**: For each capability, define:
   - `id`: stable unique slug (e.g., `assign-order-courier`)
   - `name`: human-readable name
   - `description`: what the skill does and when to invoke it
   - `endpoint`: the API path (can be relative or absolute)
   - `method`: HTTP method
   - `auth`: authentication scheme required (e.g., `bearer`, `oauth2`, `none`)
   - `input_schema`: JSON Schema for the request payload (optional but strongly recommended)
   - `output_schema`: JSON Schema for the response (optional but strongly recommended)

3. **Build the index.json**: Wrap skill entries in the agentskills.io manifest envelope:
   ```json
   {
     "schema_version": "1.0",
     "skills": [ /* skill entries */ ]
   }
   ```

4. **Place at well-known path**: Deploy `index.json` to `/.well-known/agent-skills/index.json`. For Cloudflare Pages, add to `public/.well-known/agent-skills/`. For Workers, serve from the catch-all route.

5. **Configure response headers**: Ensure `Content-Type: application/json` and `Access-Control-Allow-Origin: *` (or scoped origin) are set on the response.

6. **Validate and test**: Fetch the manifest via `curl https://yourdomain.com/.well-known/agent-skills/index.json` and validate against the agentskills.io schema. Test that agent clients can parse and invoke declared skills.

7. **Wire up discovery**: Add a Link header via `configure-agent-headers` pointing to the manifest for passive discovery without requiring active crawl.

## Output Format

- `/.well-known/agent-skills/index.json` — JSON manifest
- Response headers: `Content-Type: application/json`, `Access-Control-Allow-Origin`

## Checklist

- [ ] All exposed capabilities have stable unique `id` values.
- [ ] Each skill entry includes `name`, `description`, `endpoint`, and `method`.
- [ ] `schema_version` field is set in the manifest envelope.
- [ ] JSON payload complies with the current agentskills.io schema version.
- [ ] `index.json` is placed at `/.well-known/agent-skills/index.json`.
- [ ] Manifest is served with `Content-Type: application/json`.
- [ ] CORS headers allow agent clients to fetch the manifest.
- [ ] Relative links in the index are verified as active in the target environment.
- [ ] Link header pointing to the manifest is configured (via `configure-agent-headers`).

## Related Skills

- **configure-mcp**: Expose model context server capability endpoint — often co-deployed with agent skills manifest.
- **manage-api-catalog**: Wire up RFC 9727 API catalog linkset — complementary discovery mechanism.
- **configure-agent-headers**: Expose the well-known agent skills path via HTTP Link headers for passive discovery.

### 2026: Manifest Evolution

- **agentskills.io manifest versioning strategy:** Increment the manifest `version` field on every change to the index. Clients should cache the manifest with `ETag` and `Last-Modified` headers and revalidate before each session. Avoid breaking changes by deprecating skills (set `status: deprecated`) before removing them from the index.
- **Skill capability schema evolution:** Adding new fields to a skill's capability schema is backward-compatible. Removing or renaming fields is breaking. Use the same Expand-contract migration pattern as API versioning.
