---
name: implement-save-persistence
description: Implements monotonic save schemas, version migration pipelines, cryptographic integrity checksums, binary and JSON serialization, and cross-platform cloud saves. Use when building game save systems, profile persistence, autosave checkpoints, or Steam Cloud synchronization.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Implement Save Persistence

Architect and implement fault-tolerant game save and persistence systems with monotonic schema versioning, atomic disk writes, cryptographic integrity verification, and cross-platform cloud synchronization.

## Core Rules

- **Atomic Write-and-Swap Operations**: Never overwrite an existing save file directly in place. Always serialize to a temporary `.tmp` file, flush to disk (`fsync`), keep a rolling `.bak` backup of the previous valid save, and perform an atomic rename to the target save slot.
- **Monotonic Schema Versioning**: Embed an explicit integer `schema_version` in every save header. Maintain deterministic step-by-step migration functions (`v1 -> v2 -> v3`) so legacy player saves upgrade cleanly after patches.
- **Cryptographic Checksum Validation**: Compute and store a SHA-256 or HMAC-SHA256 digest of the serialized payload in the save envelope to detect corrupted writes, disk bit-rot, or malformed structures before deserialization.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing save persistence implementations.

## Suggested Process

### 1. Envelope & Monotonic Schema Design
Define a strict save envelope separating header metadata from game payload:
- Header: `magic_bytes`, `schema_version`, `timestamp_utc`, `playtime_seconds`, `payload_sha256`
- Payload: structured player progression, inventory state, world flags, and deterministic RNG seeds
Support human-readable JSON for debug builds and compact binary serialization (MessagePack, FlatBuffers, or binary streams) for production releases.

### 2. Version Migration Pipeline
Register sequential migration handlers indexed by source version. When loading a save where `file.schema_version` is older than `CURRENT_SCHEMA_VERSION`, iteratively apply each upgrade transform and validate invariants before hydrating runtime state.

### 3. Atomic Disk I/O & Corruption Recovery
Execute transactional file persistence:
- Write serialized bytes to `slot_0.sav.tmp` and verify byte count and SHA-256 digest.
- Copy existing `slot_0.sav` to `slot_0.sav.bak`, then atomically replace `slot_0.sav` with `slot_0.sav.tmp`.
- If primary save checksum verification fails on load, automatically fall back to `.bak` and alert the player safely.

### 4. Cross-Platform Cloud Save Synchronization
Store saves in OS-compliant user data directories (`user://`, `Application.persistentDataPath`) scoped by platform account ID. Integrate Steam Cloud Auto-Cloud or ISteamRemoteStorage APIs, resolving timestamp and playtime conflicts deterministically across devices.

## Output Contracts

When completing save persistence implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Save files write to a `.tmp` staging file and rotate a `.bak` backup before atomic rename
- [ ] Save header includes monotonic `schema_version` and verifies SHA-256 payload checksum on load
- [ ] Sequential version migration functions upgrade legacy save fixtures without data loss
- [ ] Serialization supports deterministic round-trip encoding in both binary and debug JSON formats
- [ ] Cloud save paths are scoped per account and handle multi-device sync conflicts safely
- [ ] Headless unit tests verify migration chains, checksum failure recovery, and round-trip integrity

## Related Skills

- **manage-scene-lifecycle**: hydrating and persisting scene state across level transitions
- **integrate-game-engine**: configuring platform user directories and headless test runners
- **integrate-dialogue-narrative**: persisting narrative condition flags and branching choices
