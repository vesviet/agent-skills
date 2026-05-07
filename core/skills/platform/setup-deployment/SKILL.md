---
name: setup-deployment
description: Add or update deployment source-of-truth configuration for a service or component. Use when a change needs rollout manifests, release config, runtime settings, or environment wiring.
---

# Setup Deployment

Use this skill when code changes need matching deployment or runtime configuration.

## Core Rules

- edit the repo's deployment source of truth, not just the live runtime
- follow existing environment and naming patterns
- keep code, config, and rollout order aligned
- avoid changing CI-owned or release-owned metadata unless the repo expects it
- make health, readiness, and rollback behavior explicit

## Suggested Process

### 1. Inspect Existing Deployment Structure

Identify:

- where deployment config lives
- how environments are organized
- what metadata is generated versus hand-maintained
- how similar services are configured

### 2. Add Or Update Required Config

Change only what the feature needs:

- runtime config values
- environment variables
- dependency wiring
- health checks
- resource or scaling hints
- routing or service registration

### 3. Check Rollout Ordering

Verify whether rollout depends on:

- a migration
- a secret or credential update
- a new dependency endpoint
- staged consumer or producer compatibility

### 4. Validate The Source Of Truth

Run the repo-local checks that apply, such as:

- manifest validation
- template rendering
- dry-run or preview commands
- config linting

### 5. Verify Runtime Intent

Confirm that:

- the config matches code expectations
- health checks point at the right path or port
- rollback remains possible
- docs or operator notes are updated if needed

## Checklist

- [ ] deployment source of truth located
- [ ] required config added or updated
- [ ] rollout ordering checked
- [ ] validation commands run
- [ ] health and rollback behavior reviewed

## Related Skills

- **scaffold-new-service**: Add deployment config for a newly created service
- **add-api-endpoint**: Roll out endpoint-related config safely
- **review-service**: Review deployment and release readiness
- **debug-runtime-platform**: Investigate rollout failures after config changes
- **commit-code**: Prepare deployment changes for delivery
