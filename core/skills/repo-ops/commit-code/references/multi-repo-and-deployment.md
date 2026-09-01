# Commit Code — Multi-Repo and Deployment (Reference)

## Multi-Repo Or Shared Module Changes

When a change spans more than one repo or module:

1. identify the dependency order
2. validate and land the upstream change first when required
3. update downstream consumers to the correct version or revision
4. revalidate after the dependency update
5. keep each commit scoped to one repo or module boundary

## Deployment Or Release Config Changes

If deployment or release configuration changed:

- commit the source-of-truth config, not just a live runtime patch
- avoid release metadata edits that CI or the platform is supposed to own
- capture any rollout dependency or manual follow-up clearly


