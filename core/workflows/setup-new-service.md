---
description: Workflow for bootstrapping a new service or bounded component in a reusable way
---

## Setup New Service Workflow

Use this workflow when creating a new service, worker, or bounded component from scratch.

### Prerequisites

- the service name and purpose are clear
- ownership and dependency boundaries are known
- repo-local templates and architectural conventions have been located

### Workflow Steps

#### 1. Define Scope

Role: **Technical Architect**, **Technical Lead**, **Product Manager**

Write down:

- what the service owns
- what contracts it exposes
- what data it manages
- what dependencies it needs
- what should stay outside its boundary

#### 2. Choose The Starting Point

Role: **Technical Lead**, **Technical Architect**

Prefer one of these, in order:

- an official repo template
- a local scaffold command
- a nearby service that already matches the desired shape

If copying an existing service:

- remove generated files that should be regenerated
- remove transient artifacts
- rename imports, module paths, and service identifiers carefully

#### 3. Create The Initial Structure

Role: **Backend Developer**, **Frontend Developer**

Create only the directories the repo actually uses.

Common examples:

- public contract or API definitions
- command or entrypoint packages
- domain or business logic
- persistence or adapters
- configuration
- tests
- docs

Do not invent extra folders if the local template already defines the right structure.

#### 4. Define Contracts And Data

Role: **Backend Developer**, **Technical Lead**

If the service exposes an API or event contract:

- define the initial contract using the repo's normal schema format
- generate any derived code with the repo's standard command
- keep the first contract intentionally small

If the service owns persistent data:

- create an initial migration using the local migration tool
- keep the first schema narrow and easy to evolve
- document any ordering or rollout constraints

Use skill: `create-migration` when schema work is involved.

#### 5. Implement The Core Flow

Role: **Backend Developer**, **Frontend Developer**

Set up the smallest end-to-end path that proves the service shape:

- boundary or handler
- core use case
- persistence or dependency adapter
- basic configuration
- health or readiness behavior if the repo uses it

Use the repo's existing DI, bootstrap, and config patterns rather than inventing new ones.

#### 6. Add Tests

Role: **Backend Developer**, **QA Engineer**

Use skill: `write-tests`

Cover:

- one core happy path
- one validation or failure path
- migration or persistence basics if applicable

Run the repo's normal test, build, and lint commands.

#### 7. Add Documentation

Role: **Technical Writer**, **Backend Developer**

Document at least:

- service purpose
- key dependencies
- local setup steps
- how to run verification
- rollout or environment notes if they are needed

Use repo-local README or service-doc templates when they exist.

#### 8. Wire It Into Delivery

Role: **DevOps Engineer**

Add the minimum delivery plumbing the repo expects, such as:

- CI checks with Sigstore provenance attestation (cosign) so every build artifact is cryptographically signed from the start
- deployment manifests (GitOps source of truth: Argo CD ApplicationSet or Flux HelmRelease)
- package publishing metadata
- ownership or alerting metadata

If the org uses a **Platform Engineering** IDP (Backstage, Port, or Cortex): register the new service in the software catalog with owner, tier, lifecycle, and dependency links — this enables self-service environment provisioning, scorecards, and dependency graph visibility.

If the service uses feature flags: wire the **OpenFeature SDK** from the first deploy rather than adding it later — decoupling flag evaluation from deployment from the start avoids brittle big-bang feature activations.

Follow the source of truth already used by the repo.

#### 9. Verify Locally

Role: **Backend Developer**, **Frontend Developer**

Before handing off:

- run the service locally if possible
- exercise the core path
- verify config loading
- confirm generated files are current

#### 10. Prepare The Initial Delivery

Role: **Backend Developer**, **Technical Lead**

Use skill: `commit-code`

Before committing:

- remove transient files
- confirm templates were fully renamed
- confirm docs and ownership info are present
- confirm the repo-local release path is understood

Do not create a commit until the user explicitly confirms that commit action.
Do not push, tag, or publish until the user explicitly confirms that specific action.

### Checklist

- [ ] service name and scope defined
- [ ] local template or scaffold chosen
- [ ] initial structure created
- [ ] contracts defined if needed
- [ ] initial schema or migration added if needed
- [ ] core flow implemented
- [ ] tests added
- [ ] docs added
- [ ] delivery plumbing connected
- [ ] local verification completed

### Related Workflows

- [Add New Feature](add-new-feature.md)
- [Service Review & Release](service-review-release.md)
- [Build & Deploy](build-deploy.md)

### Related Skills

- **navigate-service**: Inspect local service patterns before scaffolding
- **create-migration**: Add initial schema changes safely
- **write-tests**: Add coverage for the first working flow
- **review-service**: Check readiness before broader rollout
- **commit-code**: Prepare approved service setup changes for delivery
