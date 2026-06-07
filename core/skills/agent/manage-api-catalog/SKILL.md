---
name: manage-api-catalog
description: Use when publishing and maintaining RFC 9727 API Catalog registries for automated API discovery.
---

# Manage API Catalog

Use this skill to create and maintain the `/.well-known/api-catalog` Linkset file.

## Core Rules
- Format strictly according to RFC 9727.
- Map endpoints for OpenAPI specifications (`service-meta`) and documentation (`service-doc`).

## Suggested Process
1. Collect all API endpoints and spec paths (OpenAPI, docs) to catalog.
2. Format the catalog linkset according to RFC 9727 spec syntax.
3. Save the catalog to `/.well-known/api-catalog` at the target root.
4. Verify response headers are set to `application/linkset+json` or `application/linkset` as required.

## Checklist
- [ ] Catalog matches standard RFC 9727 syntax.
- [ ] OpenAPI spec URL (`service-meta`) is active and validated.
- [ ] Documentation URL (`service-doc`) is reachable.
- [ ] File exists at `/.well-known/api-catalog`.
- [ ] Linkset returns correct HTTP response headers.

## Related Skills
- **configure-agent-headers**: Expose well-known endpoints natively.
- **configure-agent-skills**: Set up the skill index.
