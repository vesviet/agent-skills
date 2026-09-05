---
name: configure-agent-skills
description: Creates and manages the agentskills.io manifest index at `/.well-known/agent-skills/index.json`, exposing structured API capabilities for agent orchestrators and capability-routing infrastructure to auto-discover and invoke. Use when registering, updating, or validating the skill manifest after adding or deprecating API endpoints on a service.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Configure Agent Skills

Use this skill when exposing API capabilities or developer instructions through the Agent Skills manifest at `/.well-known/agent-skills/index.json`. This makes structured skill metadata discoverable by agent orchestrators, SDK clients, and capability-routing infrastructure that reads the agentskills.io schema.

## Core Rules

- The manifest MUST be placed at `/.well-known/agent-skills/index.json` at the domain root.
- The schema MUST conform to the version published by `agentskills.io` — validate before deployment.
- Each skill entry MUST have a unique `id` that is stable across versions — do not change IDs once published.
- The manifest MUST be served with `Content-Type: application/json` and appropriate CORS headers to allow agent clients to fetch it cross-origin.
- Version the manifest using the `schema_version` field so downstream agents can detect breaking changes.
- Validate the manifest against the published `agentskills.io` schema before every deploy; reject schema-drifted manifests (OWASP ASI04)
- Treat the manifest as a public, signed contract: do not include internal-only skill descriptions or unreleased capabilities without an explicit `status: beta` flag
- Every skill entry that points to an authenticated endpoint must declare its `auth` scheme; do not infer auth from the URL (OWASP ASI03)
- Set `ETag` and `Last-Modified` headers on the served manifest so clients can detect silent changes (OWASP ASI01 — Goal Hijack via stale contract)

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

## Output Contracts

The manifest itself is the primary artifact. When a change must be communicated
to another agent (CI pipeline, infra agent, or registry publisher), emit:

- **`contracts/schemas/api-contract-spec.json`** describing the manifest shape, the schema version, the list of skill ids, and any deprecated entries. The consuming agent can then validate before publishing.
- For human-readable reports, a markdown diff against the previous `schema_version` is sufficient.

Skip emission for routine single-skill additions that do not cross a role boundary.

## Failure Modes

- **Schema version drift**: the manifest is published without bumping `schema_version` after a breaking change. Mitigation: enforce the expand-contract migration; never remove or rename fields without a version bump.
- **Stale skill id**: a skill id is renamed after publication, breaking existing agent clients. Mitigation: skill ids are immutable once published; deprecate via `status: deprecated` and keep the id stable.
- **CORS misconfiguration**: the manifest is blocked for cross-origin agent clients. Mitigation: serve with `Access-Control-Allow-Origin` set to a scoped origin (or `*` only for fully public manifests) and verify with a CORS preflight.
- **Auth not declared**: a skill entry points to an authenticated endpoint but the `auth` field is missing or `none`. Mitigation: every authenticated entry must declare its scheme; CI must reject entries with no `auth` that point to non-public paths.
- **Caching a stale manifest**: an agent client uses a cached manifest from a prior `schema_version`. Mitigation: set `ETag` and `Last-Modified`; clients should revalidate before each session.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a malicious or compromised manifest could redirect agents to attacker-controlled endpoints. Validate every `endpoint` and `method` field against the operator's own domain allowlist.
- **ASI03 Identity & Privilege Abuse**: every skill entry that touches authenticated resources must declare its `auth` scheme; do not infer auth from URL or description.
- **ASI04 Supply Chain**: the manifest schema must be validated against the published `agentskills.io` schema before every deploy; treat schema drift as a CI failure.
- **ASI07 Inter-Agent Communication**: the manifest is consumed by external agents; treat it as a public contract and review all changes before publish.
- **ASI09 Human-Agent Trust Exploitation**: do not present a manifest as "compliant" without a successful schema validation run; surface the validator output in the deploy record.
