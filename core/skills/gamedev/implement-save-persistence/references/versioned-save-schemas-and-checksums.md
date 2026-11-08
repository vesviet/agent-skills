# Versioned Save Schemas & Checksum Integrity (2026)

## 1. Architectural Foundations: Fault-Tolerant Persistence

Game save persistence must withstand sudden hardware power loss, process termination, disk corruption, and patch-induced schema evolution:

```
┌────────────────────────────────────────────────────────┐
│                   SAVE ENVELOPE                        │
├────────────────────┬───────────────────────────────────┤
│ magic_bytes        │ "GMSV" (4 bytes)                  │
│ schema_version     │ uint32 (e.g. 3)                   │
│ timestamp_utc      │ uint64 (epoch seconds)            │
│ playtime_seconds   │ uint32                            │
│ payload_sha256     │ hex string (64 characters)        │
├────────────────────┴───────────────────────────────────┤
│                 SERIALIZED PAYLOAD                     │
│  (JSON in dev / MessagePack or FlatBuffers in prod)    │
│  { player: { hp: 100, pos: [...] }, inventory: [...] } │
└────────────────────────────────────────────────────────┘
```

## 2. Monotonic Step-by-Step Migration Pipeline

When a save file with version $N$ is loaded by a game build expecting version $M$ ($M > N$):
- Direct multi-version jumps ($N \to M$) are prohibited.
- The loader executes sequential, composable transforms:
  $$N \xrightarrow{\text{migrate}_{N\to N+1}} N+1 \xrightarrow{\text{migrate}_{N+1\to N+2}} \dots \xrightarrow{\text{migrate}_{M-1\to M}} M$$
- Invariants are verified after each individual transform step.
- If $N > M$ (save from a newer patch), the save is rejected safely to prevent forward-incompatible corruption.

## 3. Transactional Write-and-Swap (Atomic Persistence)

Direct overwriting of active save files causes data loss on crash:
1. Serialize envelope and payload to `.tmp` file (`slot_0.sav.tmp`).
2. Flush OS file buffers using `fsync` / `flush()`.
3. If valid previous save exists (`slot_0.sav`), copy to `slot_0.sav.bak`.
4. Atomically rename `slot_0.sav.tmp` to `slot_0.sav`.
5. On load failure (corrupted checksum or truncated bytes), auto-recover from `.bak`.

## 4. Cross-Platform Cloud Storage Invariants

- Cloud conflict resolution prioritizes `max(timestamp_utc)` with `playtime_seconds` as tiebreaker.
- Slot identifiers must be sanitized: `^[a-zA-Z0-9_-]{1,32}$` to prevent directory traversal attacks (`../../etc/passwd`).
