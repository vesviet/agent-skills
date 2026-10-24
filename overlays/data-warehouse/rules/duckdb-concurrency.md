# DuckDB Concurrency & Single-Writer Governance

Operational standard and runtime governance for embedded DuckDB 1.5+ write operations in omnichannel retail architectures. This rule establishes strict single-writer multi-process serialization, resilient lock acquisition with exponential backoff and jitter, connection lifecycle discipline, and architectural segregation between OLTP (SQLite WAL) and OLAP (DuckDB).

## 1. Concurrency Architecture & Failure Domain

### 1.1 The DuckDB Concurrency Constraint
DuckDB utilizes an embedded columnar database engine optimized for vectorized OLAP workloads. By design:
- Multiple concurrent reader processes can safely query a single DuckDB database file simultaneously when connected in `read_only=True` mode.
- **Strictly only ONE writer process** can hold an open write handle to a `.duckdb` database file at any given moment.

When multiple processes (such as multiple ASGI Uvicorn workers, Celery/RQ background tasks, or cron ETL scripts) attempt to open concurrent write connections without coordination, DuckDB triggers an unrecoverable IO collision:
```text
duckdb.IOException: Could not set lock on file ".../warehouse.duckdb": Resource temporarily unavailable
```
Uncoordinated write attempts cause transaction aborts, corrupted lock headers, worker restarts, and data loss.

### 1.2 Multi-Tier Serialization via `AsyncCrossProcessLock`
To enforce absolute single-writer governance across asynchronous coroutines, multiple operating system processes, and containerized multi-node deployments, all write operations must pass through `AsyncCrossProcessLock`.

The lock combines three distinct synchronization tiers:
1. **Tier 1: In-Process Asynchronous Lock (`asyncio.Lock`)**:
   - Serializes concurrent coroutines running inside the same Python event loop.
   - Prevents intra-process contention and eliminates unnecessary OS kernel lock requests within the same worker.
2. **Tier 2: Host-Level Inter-Process File Lock (`filelock.FileLock`)**:
   - Acquires an exclusive file lock on a dedicated auxiliary lockfile (`<database>.duckdb.lock`).
   - Prevents independent Python OS processes (e.g., separate Uvicorn worker PIDs) on the same host from opening simultaneous write connections.
3. **Tier 3: Distributed Cluster Lock (Redis Lock with Fail-Closed Semantics)**:
   - When running across multiple containers, pods, or host nodes, an atomic Redis lock (`SET lock:duckdb_writer <uuid> NX PX <lease_ms>`) acts as the distributed arbiter.
   - **Fail-Closed Mandate**: If the Redis cluster is unreachable, encounters a network partition, or times out, lock acquisition **MUST FAIL CLOSED** immediately. Bypassing the distributed lock to "attempt writing anyway" is strictly prohibited under all circumstances.

---

## 2. Implementation Specification: `AsyncCrossProcessLock`

The following reference implementation provides the production-grade implementation required for all data pipelines and write endpoints.

```python
"""Single-writer governance for DuckDB multi-process concurrency."""

from __future__ import annotations

import asyncio
import logging
import os
import random
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator, Optional

import duckdb
from filelock import FileLock, Timeout as FileLockTimeout

logger = logging.getLogger("retail.duckdb.concurrency")


class DuckDBLockAcquisitionError(RuntimeError):
    """Raised when the DuckDB single-writer lock cannot be acquired."""


class DuckDBFailClosedError(DuckDBLockAcquisitionError):
    """Raised when distributed lockarbiter is unreachable and fail-closed policy triggers."""


@dataclass(frozen=True)
class LockConfig:
    """Configuration parameters for DuckDB single-writer acquisition."""
    timeout_seconds: float = 30.0
    base_backoff_seconds: float = 0.1
    max_backoff_seconds: float = 3.0
    jitter_fraction: float = 0.2
    redis_lease_ms: int = 30000


class AsyncCrossProcessLock:
    """Three-tier cross-process lock coordinator for DuckDB single-writer operations.
    
    Combines asyncio.Lock (coroutine tier), FileLock (host process tier),
    and Redis atomic key (cluster tier, fail-closed).
    """

    _coro_locks: dict[str, asyncio.Lock] = {}

    def __init__(
        self,
        db_path: Path | str,
        lock_file_path: Optional[Path | str] = None,
        redis_client: Optional[object] = None,
        config: Optional[LockConfig] = None,
    ) -> None:
        self.db_path = Path(db_path).resolve()
        self.lock_file_path = (
            Path(lock_file_path).resolve()
            if lock_file_path
            else self.db_path.with_suffix(".duckdb.lock")
        )
        self.redis_client = redis_client
        self.config = config or LockConfig()

        # In-process coroutine lock registration
        str_key = str(self.db_path)
        if str_key not in self._coro_locks:
            self._coro_locks[str_key] = asyncio.Lock()
        self.coro_lock = self._coro_locks[str_key]

        # OS file lock on auxiliary lock file
        self.file_lock = FileLock(str(self.lock_file_path), timeout=0)

    async def _acquire_redis_lock(self, token: str) -> bool:
        """Acquire atomic cluster lock via Redis. Fails closed on any network error."""
        if not self.redis_client:
            return True  # Standalone single-host mode
        try:
            # Atomic SET ... NX PX
            acquired = await self.redis_client.set(
                f"lock:duckdb_writer:{self.db_path.name}",
                token,
                nx=True,
                px=self.config.redis_lease_ms,
            )
            return bool(acquired)
        except Exception as exc:
            logger.error("Redis lockarbiter connection failed: %s. Enforcing FAIL-CLOSED policy.", exc)
            raise DuckDBFailClosedError(f"Redis lockarbiter failure: {exc}") from exc

    async def _release_redis_lock(self, token: str) -> None:
        """Release cluster lock using Lua script to verify ownership token."""
        if not self.redis_client:
            return
        lua_release = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        try:
            await self.redis_client.eval(
                lua_release,
                1,
                f"lock:duckdb_writer:{self.db_path.name}",
                token,
            )
        except Exception as exc:
            logger.warning("Error releasing Redis lock token %s: %s", token, exc)

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[None]:
        """Acquire in-process, OS, and cluster locks with backoff and jitter."""
        token = f"{os.getpid()}-{time.time()}-{random.randint(1000, 9999)}"
        start_time = time.monotonic()
        attempt = 0

        # Tier 1: Coroutine serialization
        await self.coro_lock.acquire()
        try:
            # Tier 2 & 3: Multi-process and cluster acquisition loop
            while True:
                elapsed = time.monotonic() - start_time
                remaining_timeout = self.config.timeout_seconds - elapsed

                if remaining_timeout <= 0:
                    raise DuckDBLockAcquisitionError(
                        f"Timed out after {self.config.timeout_seconds:.1f}s waiting for "
                        f"DuckDB lock on {self.db_path.name}"
                    )

                try:
                    # Attempt non-blocking FileLock acquisition
                    self.file_lock.acquire(timeout=0.01)
                    file_lock_acquired = True
                except FileLockTimeout:
                    file_lock_acquired = False

                if file_lock_acquired:
                    try:
                        redis_acquired = await self._acquire_redis_lock(token)
                        if redis_acquired:
                            # All three tiers acquired successfully
                            break
                        # Release file lock if Redis cluster acquisition did not succeed
                        self.file_lock.release()
                    except Exception:
                        self.file_lock.release()
                        raise

                # Calculate exponential backoff with randomized jitter
                attempt += 1
                backoff = min(
                    self.config.max_backoff_seconds,
                    self.config.base_backoff_seconds * (2 ** (attempt - 1)),
                )
                jitter = backoff * self.config.jitter_fraction * (random.uniform(-1.0, 1.0))
                sleep_duration = max(0.05, min(remaining_timeout, backoff + jitter))

                logger.debug(
                    "Lock contention on %s. Retrying in %.3fs (attempt %d)",
                    self.db_path.name,
                    sleep_duration,
                    attempt,
                )
                await asyncio.sleep(sleep_duration)

            # Yield control to the caller while holding all locks
            try:
                yield
            finally:
                # Release Tier 3 (Redis)
                await self._release_redis_lock(token)
                # Release Tier 2 (FileLock)
                if self.file_lock.is_locked:
                    self.file_lock.release()
        finally:
            # Release Tier 1 (asyncio.Lock)
            self.coro_lock.release()
```

---

## 3. Connection Lifecycle Management

### 3.1 Write Connections: Strict Ephemeral Pattern
Write connections must NEVER be held as global variables, connection pools, or persistent application state. Every write operation must follow this exact lifecycle:

```python
# CORRECT: Ephemeral write connection wrapped in AsyncCrossProcessLock
async def insert_gold_daily_sales(db_path: Path, parquet_path: Path) -> None:
    lock = AsyncCrossProcessLock(db_path)
    async with lock.acquire():
        # Open write handle ONLY after acquiring the lock
        con = duckdb.connect(str(db_path), read_only=False)
        try:
            con.execute("BEGIN TRANSACTION;")
            con.execute("""
                MERGE INTO gold_daily_sales AS target
                USING (SELECT * FROM read_parquet(?)) AS source
                ON target.store_id = source.store_id 
                   AND target.sale_date = source.sale_date
                WHEN MATCHED THEN UPDATE SET
                    gross_revenue = source.gross_revenue,
                    net_revenue = source.net_revenue,
                    order_count = source.order_count,
                    updated_at = CURRENT_TIMESTAMP
                WHEN NOT MATCHED THEN INSERT VALUES (
                    source.store_id, source.sale_date, source.gross_revenue,
                    source.net_revenue, source.order_count, CURRENT_TIMESTAMP
                );
            """, [str(parquet_path)])
            con.execute("COMMIT;")
        except Exception:
            con.execute("ROLLBACK;")
            raise
        finally:
            # MUST explicitly close before releasing the lock
            con.close()
```

### 3.2 Read Connections: Pooled / Long-Lived
Read operations do not acquire `AsyncCrossProcessLock`. Multiple workers can connect simultaneously:
```python
# CORRECT: Read-only connection for analytical queries
def query_store_inventory_turnover(db_path: Path, store_id: str) -> list[tuple]:
    with duckdb.connect(str(db_path), read_only=True) as con:
        return con.execute("""
            SELECT sku, current_stock, turnover_rate
            FROM gold_inventory_metrics
            WHERE store_id = ?
            ORDER BY turnover_rate DESC
        """, [store_id]).fetchall()
```

---

## 4. Architectural Segregation: OLTP (SQLite WAL) vs. OLAP (DuckDB)

To prevent analytical DuckDB locks from starving high-speed retail checkout or physical barcode scanning, omnichannel retail systems enforce strict database tiering:

| Architecture Boundary | OLTP Ingestion Layer | OLAP Analytical Warehouse |
|:---|:---|:---|
| **Underlying Engine** | SQLite (WAL Mode) | DuckDB 1.5+ |
| **Concurrency Model** | Concurrent readers + serialized non-blocking writer | Concurrent readers + `AsyncCrossProcessLock` writer |
| **Write Latency SLA** | $< 2\text{ms}$ per transaction | Batch micro-intervals ($10\text{s} - 5\text{min}$) |
| **Primary Workload** | Barcode scan stream, POS receipts, cart events | Medallion aggregation, cohort analysis, AMIS sync feeds |
| **Storage Layout** | Row-oriented SQLite tables (`store/buffer_oltp.db`) | Columnar partitioned Parquet & DuckDB Gold tables |

### 4.1 SQLite WAL Configuration
Every SQLite OLTP database instance must be initialized with the following pragmas:
```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
PRAGMA foreign_keys = ON;
```

### 4.2 Micro-Batch CDC Pipeline to DuckDB
A lightweight asynchronous worker drains committed events from SQLite WAL every $N$ seconds, formats them into a Bronze/Silver Parquet chunk, and acquires `AsyncCrossProcessLock` to commit the data into DuckDB Gold tables:
```text
[POS / Scanners] ──(HTTP/WS)──> [FastAPI Worker] ──(Append)──> [SQLite WAL]
                                                                     │
                                                      (Batch Drain every 15s)
                                                                     ▼
                                                          [Parquet Staging]
                                                                     │
                                                         (AsyncCrossProcessLock)
                                                                     ▼
                                                          [DuckDB Gold Warehouse]
```

---

## 5. Failure Modes & Operational Runbook

### 5.1 Lock Starvation & Timeout Escalation
- **Symptom**: `DuckDBLockAcquisitionError: Timed out after 30.0s waiting for DuckDB lock`.
- **Root Cause**: A long-running analytical query held a write connection instead of `read_only=True`, or an unhandled exception terminated a worker without closing the write handle.
- **Remediation**:
  1. Inspect active processes holding `.duckdb.lock` via OS tools (`lsof` or `handle.exe`).
  2. Verify whether any batch job is executing long-running unindexed `MERGE` statements.
  3. Ensure all analytical read endpoints explicitly instantiate `read_only=True`.

### 5.2 Stale Lockfile Protocol
If an abrupt operating system kill signal (`SIGKILL` / `kill -9`) terminates a Python process while holding `filelock.FileLock`, modern OS kernels automatically release the file descriptor lock. However, if using NFS or network-attached mounts where lockfiles persist:
1. Verify the owning PID recorded in the lock telemetry is no longer running.
2. Only after PID validation, safely remove the orphaned `.duckdb.lock` file.
3. Emit a structured incident event conforming to `core/contracts/schemas/incident-report.json`.

---

## Standard 2026 Alignment

This overlay rule file is part of the agent-skills engineering pack. The 2026
upgrade pass added the following Standard 2026 alignment footer to every
overlay rule file in the pack.

- **OWASP ASI**: applied as described in the core pack — see
  `core/roles/role-standard.md` (ASI01-ASI10) and the per-skill
  `## Security Guardrails (OWASP ASI)` section in each skill. The rules in this
  file are applied by the role that owns the affected action; the runtime
  gate is `core/scripts/hooks/check-policy.py` with
  `core/policies/action-boundaries.yaml`.
- **Failure Modes** (overlay-specific): the rules in this file can be violated
  by drift, missing context, or untracked exceptions. The owning role is
  expected to surface concrete failure scenarios in the workflow's
  `### Failure Modes` section and to capture remediations via
  `contracts/schemas/incident-report.json` when the rule is bypassed.
- **Output Contracts**: when a rule in this file produces a structured
  artifact (brief, plan, config, content handoff, audit event), the artifact
  must conform to the corresponding schema in `core/contracts/schemas/`.
  See `core/skills/security-data/build-data-pipeline/SKILL.md` and the `data-pipeline-spec.json` schema.
- **Skill Toolbox Lock**: a rule in this file is enforced by the role whose
  Skill Toolbox lists the related skill as Primary. Roles that hold the
  skill as Supporting must delegate rather than execute directly (per
  `core/workflows/README.md`).
- **Commit / publish gate**: rule changes that affect user-visible behavior
  must follow the META-RULE in `core/rules/code.md` — no commit, no push,
  no publish without explicit user confirmation.

See `core/skills/security-data/build-data-pipeline/SKILL.md` and the `data-pipeline-spec.json` schema.

Last updated: 2026-09-05
