---
name: durable-objects
description: Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage, alarms, WebSockets, or reviewing DO code for best practices. Covers Workers integration, wrangler config, and testing with Vitest. Biases towards retrieval from Cloudflare docs over pre-trained knowledge.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Durable Objects

Build stateful, coordinated applications on Cloudflare's edge using Durable Objects.

## Retrieval Sources

Your knowledge of Durable Objects APIs and configuration may be outdated. **Prefer retrieval over pre-training** for any Durable Objects task.

| Resource | URL |
|----------|-----|
| Docs | https://developers.cloudflare.com/durable-objects/ |
| API Reference | https://developers.cloudflare.com/durable-objects/api/ |
| Best Practices | https://developers.cloudflare.com/durable-objects/best-practices/ |
| Examples | https://developers.cloudflare.com/durable-objects/examples/ |

Fetch the relevant doc page when implementing features.

## When to Use

- Creating new Durable Object classes for stateful coordination
- Implementing RPC methods, alarms, or WebSocket handlers
- Reviewing existing DO code for best practices
- Configuring wrangler.jsonc/toml for DO bindings and migrations
- Writing tests with `@cloudflare/vitest-pool-workers`
- Designing sharding strategies and parent-child relationships

## Reference Documentation

- `./references/rules.md` - Core rules, storage, concurrency, RPC, alarms
- `./references/testing.md` - Vitest setup, unit/integration tests, alarm testing
- `./references/workers.md` - Workers handlers, types, wrangler config, observability

Search: `blockConcurrencyWhile`, `idFromName`, `getByName`, `setAlarm`, `sql.exec`

## Core Principles

### Use Durable Objects For

| Need | Example |
|------|---------|
| Coordination | Chat rooms, multiplayer games, collaborative docs |
| Strong consistency | Inventory, booking systems, turn-based games |
| Per-entity storage | Multi-tenant SaaS, per-user data |
| Persistent connections | WebSockets, real-time notifications |
| Scheduled work per entity | Subscription renewals, game timeouts |

### Do NOT Use For

- Stateless request handling (use plain Workers)
- Maximum global distribution needs
- High fan-out independent requests

## Quick Reference

Code samples (wrangler config, basic DO pattern, stub creation, storage
operations, alarms, Vitest quick start) live in
[`references/code-patterns.md`](references/code-patterns.md). The deeper
guides (rules, testing, workers wiring) are in:

- `./references/rules.md` - Core rules, storage, concurrency, RPC, alarms
- `./references/testing.md` - Vitest setup, unit/integration tests, alarm testing
- `./references/workers.md` - Workers handlers, types, wrangler config, observability

Search: `blockConcurrencyWhile`, `idFromName`, `getByName`, `setAlarm`, `sql.exec`

## Core Rules

1. **Model around coordination atoms** - One DO per chat room/game/user, not one global DO
2. **Use `getByName()` for deterministic routing** - Same input = same DO instance
3. **Use SQLite storage** - Configure `new_sqlite_classes` in migrations
4. **Initialize in constructor** - Use `blockConcurrencyWhile()` for schema setup only
5. **Use RPC methods** - Not fetch() handler (compatibility date >= 2024-04-03)
6. **Persist first, cache second** - Always write to storage before updating in-memory state
7. **One alarm per DO** - `setAlarm()` replaces any existing alarm

## Anti-Patterns (NEVER)

- Single global DO handling all requests (bottleneck)
- Using `blockConcurrencyWhile()` on every request (kills throughput)
- Storing critical state only in memory (lost on eviction/crash)
- Using `await` between related storage writes (breaks atomicity)
- Holding `blockConcurrencyWhile()` across `fetch()` or external I/O

## Suggested Process
1. Model the coordinate entity as a distinct class extend `DurableObject`.
2. Configure bindings and storage class migrations in wrangler config.
3. Establish initial schema setups synchronously inside constructor using `blockConcurrencyWhile`.
4. Expose actions using RPC methods instead of fetch request handlers.
5. Create Vitest suites to perform state validation and integration runs.

## Checklist
- [ ] Durable Object class is defined and exported.
- [ ] Bindings and migrations are added to wrangler config.
- [ ] Schema setup uses blockConcurrencyWhile in constructor.
- [ ] Object logic leverages RPC methods where possible.
- [ ] Unit and integration tests are written and passing.
- [ ] For complex DOs, evaluate `@cloudflare/actors` library (Cloudflare-recommended over raw DO API — provides SQL schema migration helpers and alarm lifecycle management).
- [ ] Outbound connections checked: DOs stay alive for active outbound connections up to 15 minutes (critical for LLM token streaming use cases).
- [ ] SQLite storage monitored: 10 GB per-DO limit (billing started Jan 7 2026); run `VACUUM` after bulk deletes to reclaim space.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Single global DO**: a single DO handles all requests, creating a hot partition. Mitigation: model around coordination atoms; one DO per chat room, user, or game instance.
- **`blockConcurrencyWhile` on every request**: schema setup is rerun on every request, killing throughput. Mitigation: use `blockConcurrencyWhile` only in the constructor for initial setup.
- **In-memory only state**: critical state lives only in memory and is lost on eviction. Mitigation: persist first, then update in-memory state; never rely on memory alone.
- **Multiple alarms**: a DO sets multiple alarms via parallel `setAlarm()` calls. Mitigation: `setAlarm()` replaces any existing alarm; design for one alarm per DO.
- **Outbound connection for LLM streaming**: a DO closes its outbound connection before streaming completes. Mitigation: DOs stay alive for active outbound connections up to 15 minutes; structure the streaming call accordingly.
- **SQLite 10 GB limit hit**: bulk deletes leave the DO close to the 10 GB per-DO storage limit. Mitigation: run `VACUUM` after bulk deletes; monitor storage size.
- **Migration missing**: a new storage class is added without a migration entry. Mitigation: add a migration tag (`new_sqlite_classes`) for every new DO class.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: DO bindings must follow least-privilege scoping; reject DO classes that expose write APIs to unauthenticated callers.
- **ASI04 Supply Chain**: `cloudflare:workers` and `@cloudflare/vitest-pool-workers` versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct SQL queries from external or user-supplied content without parameterized queries; treat `sql.exec` inputs as a hostile surface.
- **ASI07 Inter-Agent Communication**: the deployment plan is consumed by Cloudflare Engineer and DevOps; emit a structured contract so each role can validate the rollout.
- **ASI09 Human-Agent Trust Exploitation**: do not present a DO as "scalable" while still using a single global DO; surface the routing model honestly.

## Related Skills
- **wrangler**: Manage deployment environments and bindings.
- **debug-workers-edge**: Troubleshoot execution at the edge.
