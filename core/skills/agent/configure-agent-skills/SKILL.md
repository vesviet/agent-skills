---
name: configure-agent-skills
description: Use when creating and managing the agentskills.io manifest index for agent capability routing.
---

# Configure Agent Skills

Use this skill when exposing API capabilities or instructions through the Agent Skills manifest.

## Core Rules
- The manifest MUST be placed at `/.well-known/agent-skills/index.json`.
- Conform to the schema published by `agentskills.io`.

## Suggested Process
1. Collect all API capabilities and developer instructions to expose.
2. Structure capabilities in JSON matching the agentskills.io schema spec.
3. Place index.json under the root `/.well-known/agent-skills/` path.
4. Verify JSON schema correctness locally or via sandbox testing.

## Checklist
- [ ] List of exposed API capabilities is documented.
- [ ] JSON payload complies with agentskills.io schemas.
- [ ] index.json is placed in `/.well-known/agent-skills/` directory.
- [ ] Relative links in the index are verified as active.
- [ ] Response headers are set to application/json.

## Related Skills
- **configure-mcp**: Expose model context server capability endpoint.
- **manage-api-catalog**: Wire up linkset endpoints for API discovery.
- **configure-agent-headers**: Expose well-known routing natively.
