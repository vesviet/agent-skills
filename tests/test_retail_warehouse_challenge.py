#!/usr/bin/env python3
"""Empirical Adversarial Stress-Test Suite for Omnichannel Retail Data Warehouse.

Covers:
1. AMIS Accounting Voucher Schema Validation & Adversarial Tests:
   - Valid embedded examples pass jsonschema Draft202012Validator.
   - Adversarial: Unbalanced debits vs credits (schema observation & business logic assert/flag).
   - Adversarial: Missing required fields (warehouse_code, item_code, pretax decomposition).
   - Adversarial: Invalid voucher_type & disparity with amis-accounting-standards.md.
2. DuckDB Concurrency & AsyncCrossProcessLock:
   - Intra-process coroutine serialization and DuckDB writing.
   - Cross-process OS process concurrency serialization.
   - Timeout escalation on lock contention.
   - Fail-closed semantics on distributed lockarbiter failure.
3. PII Scrubbing & Salted HMAC-SHA256:
   - Canonical phone normalization (Decree 13/2023/ND-CP).
   - Salted HMAC-SHA256 determinism, key-sensitivity, missing salt protection.
   - Pseudonym token formatting (CUST-XXXXXX and CUST-GUEST-ANON).
   - Empirical vulnerability finding in verbatim PHONE_LEAK_REGEX from pii-scrubbing.md.
   - Corrected circuit breaker verification gate (phone, email, CCCD leak detection).
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import copy
from dataclasses import dataclass
import hashlib
import hmac
import json
import multiprocessing
import os
from pathlib import Path
import random
import re
import tempfile
import time
from typing import Any, AsyncIterator, Optional

import duckdb
from filelock import FileLock, Timeout as FileLockTimeout
import jsonschema
from jsonschema import Draft202012Validator
import pyarrow as pa
import pytest


ROOT = Path(__file__).resolve().parent.parent
AMIS_SCHEMA_PATH = ROOT / "core" / "contracts" / "schemas" / "amis-voucher-contract.json"


# ============================================================================
# 1. AMIS VOUCHER SCHEMA & BUSINESS LOGIC HARNESS
# ============================================================================

def load_amis_schema() -> tuple[dict[str, Any], Draft202012Validator]:
    assert AMIS_SCHEMA_PATH.is_file(), f"Missing schema at {AMIS_SCHEMA_PATH}"
    schema_dict = json.loads(AMIS_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema_dict)
    return schema_dict, validator


def validate_amis_accounting_rules(payload: dict[str, Any]) -> list[str]:
    """Applies statutory business rules and debit-credit balance verification.
    
    Returns a list of violation messages if any rules are broken.
    """
    violations: list[str] = []

    summary = payload.get("summary", {})
    summary_debit = summary.get("total_debit", 0)
    summary_credit = summary.get("total_credit", 0)
    is_balanced = summary.get("is_balanced")

    if summary_debit != summary_credit:
        violations.append(
            f"Summary debit-credit imbalance: total_debit={summary_debit} != total_credit={summary_credit}"
        )

    if (summary_debit == summary_credit) and (is_balanced is not True):
        violations.append(
            f"Summary is_balanced flag must be True when debits equal credits, got {is_balanced}"
        )

    if (summary_debit != summary_credit) and (is_balanced is True):
        violations.append(
            f"Summary is_balanced is True but debits ({summary_debit}) != credits ({summary_credit})"
        )

    vouchers = payload.get("vouchers", [])
    computed_sum_voucher_debit = 0
    computed_sum_voucher_credit = 0

    for i, v in enumerate(vouchers):
        v_no = v.get("voucher_no", f"voucher[{i}]")
        v_debit = v.get("voucher_total_debit", 0)
        v_credit = v.get("voucher_total_credit", 0)

        if v_debit != v_credit:
            violations.append(
                f"Voucher {v_no} unbalanced: voucher_total_debit={v_debit} != voucher_total_credit={v_credit}"
            )

        computed_sum_voucher_debit += v_debit
        computed_sum_voucher_credit += v_credit

        # Check journal entries sum
        journal_entries = v.get("journal_entries", [])
        j_debit_sum = 0
        j_credit_sum = 0
        for entry in journal_entries:
            amt = entry.get("amount", 0)
            if entry.get("debit_account"):
                j_debit_sum += amt
            if entry.get("credit_account"):
                j_credit_sum += amt

        if j_debit_sum != j_credit_sum:
            violations.append(
                f"Voucher {v_no} journal entries sum mismatch: debit_sum={j_debit_sum} != credit_sum={j_credit_sum}"
            )

        # Pretax decomposition check on line items
        line_items = v.get("line_items", [])
        for li in line_items:
            l_no = li.get("line_no")
            qty = li.get("quantity", 0)
            unit_pretax = li.get("unit_price_pretax", 0)
            pretax_amount = li.get("pretax_amount", 0)
            expected_pretax = qty * unit_pretax
            if abs(expected_pretax - pretax_amount) > 1.0:
                violations.append(
                    f"Voucher {v_no} line {l_no} pretax calculation discrepancy: "
                    f"qty({qty}) * unit_price({unit_pretax}) = {expected_pretax} != pretax_amount({pretax_amount})"
                )

    return violations


# ============================================================================
# 2. ASYNC CROSS PROCESS LOCK (DUCKDB CONCURRENCY)
# ============================================================================

class DuckDBLockAcquisitionError(RuntimeError):
    """Raised when the DuckDB single-writer lock cannot be acquired."""

class DuckDBFailClosedError(DuckDBLockAcquisitionError):
    """Raised when distributed lockarbiter is unreachable and fail-closed policy triggers."""

@dataclass(frozen=True)
class LockConfig:
    timeout_seconds: float = 5.0
    base_backoff_seconds: float = 0.05
    max_backoff_seconds: float = 0.5
    jitter_fraction: float = 0.2
    redis_lease_ms: int = 30000

class AsyncCrossProcessLock:
    """Implementation conforming to overlays/retail-data-warehouse/rules/duckdb-concurrency.md."""

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

        str_key = str(self.db_path)
        if str_key not in self._coro_locks:
            self._coro_locks[str_key] = asyncio.Lock()
        self.coro_lock = self._coro_locks[str_key]
        self.file_lock = FileLock(str(self.lock_file_path), timeout=0)

    async def _acquire_redis_lock(self, token: str) -> bool:
        if not self.redis_client:
            return True
        try:
            acquired = await self.redis_client.set(
                f"lock:duckdb_writer:{self.db_path.name}",
                token,
                nx=True,
                px=self.config.redis_lease_ms,
            )
            return bool(acquired)
        except Exception as exc:
            raise DuckDBFailClosedError(f"Redis lockarbiter failure: {exc}") from exc

    async def _release_redis_lock(self, token: str) -> None:
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
        except Exception:
            pass

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[None]:
        token = f"{os.getpid()}-{time.time()}-{random.randint(1000, 9999)}"
        start_time = time.monotonic()
        attempt = 0

        await self.coro_lock.acquire()
        try:
            while True:
                elapsed = time.monotonic() - start_time
                remaining_timeout = self.config.timeout_seconds - elapsed

                if remaining_timeout <= 0:
                    raise DuckDBLockAcquisitionError(
                        f"Timed out after {self.config.timeout_seconds:.1f}s waiting for "
                        f"DuckDB lock on {self.db_path.name}"
                    )

                try:
                    self.file_lock.acquire(timeout=0.01)
                    file_lock_acquired = True
                except FileLockTimeout:
                    file_lock_acquired = False

                if file_lock_acquired:
                    try:
                        redis_acquired = await self._acquire_redis_lock(token)
                        if redis_acquired:
                            break
                        self.file_lock.release()
                    except Exception:
                        self.file_lock.release()
                        raise

                attempt += 1
                backoff = min(
                    self.config.max_backoff_seconds,
                    self.config.base_backoff_seconds * (2 ** (attempt - 1)),
                )
                jitter = backoff * self.config.jitter_fraction * (random.uniform(-1.0, 1.0))
                sleep_duration = max(0.01, min(remaining_timeout, backoff + jitter))
                await asyncio.sleep(sleep_duration)

            try:
                yield
            finally:
                await self._release_redis_lock(token)
                if self.file_lock.is_locked:
                    self.file_lock.release()
        finally:
            self.coro_lock.release()


def _os_process_writer(db_path_str: str, worker_id: int, records_count: int, barrier: Any) -> None:
    db_p = Path(db_path_str)
    barrier.wait()

    async def _run() -> None:
        lock = AsyncCrossProcessLock(db_p, config=LockConfig(timeout_seconds=10.0))
        for i in range(records_count):
            async with lock.acquire():
                con = duckdb.connect(str(db_p), read_only=False)
                try:
                    con.execute(
                        "INSERT INTO write_test_log VALUES (?, ?, CURRENT_TIMESTAMP);",
                        [worker_id, f"item-{i}"],
                    )
                finally:
                    con.close()
                await asyncio.sleep(0.01)

    asyncio.run(_run())


# ============================================================================
# 3. PII SCRUBBING & SALTED HMAC-SHA256 HARNESS
# ============================================================================

VN_PHONE_REGEX = re.compile(r"^(?:\+?84|0)(3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])([0-9]{7})$")

# Verbatim regex from overlays/retail-data-warehouse/rules/pii-scrubbing.md line 183
VERBATIM_PHONE_LEAK_REGEX = re.compile(r"(?:0|\+?84)(?:3|5|7|8|9)[0-9]{7}\b")

# Corrected regex matching full 10-digit Vietnamese mobile numbers
CORRECTED_PHONE_LEAK_REGEX = re.compile(r"(?:0|\+?84)(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])[0-9]{7}\b")

EMAIL_LEAK_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
CCCD_LEAK_REGEX = re.compile(r"\b[0-9]{12}\b")

class PIIScrubbingError(ValueError):
    """Raised when PII normalization or hashing fails."""

def normalize_vietnam_phone(raw_phone: Optional[str]) -> Optional[str]:
    if not raw_phone:
        return None
    cleaned = re.sub(r"[\s\-\.\(\)\+]", "", str(raw_phone))
    match = VN_PHONE_REGEX.match(cleaned)
    if not match:
        return None
    carrier_prefix, subscriber_number = match.groups()
    return f"84{carrier_prefix}{subscriber_number}"

def hash_phone_number(canonical_phone: Optional[str], salt: Optional[bytes] = None) -> Optional[str]:
    if not canonical_phone:
        return None
    if salt is None:
        salt_str = os.environ.get("RETAIL_PII_SALT")
        if not salt_str:
            raise PIIScrubbingError("CRITICAL: RETAIL_PII_SALT environment variable is not configured.")
        salt = salt_str.encode("utf-8")
    return hmac.new(salt, canonical_phone.encode("utf-8"), hashlib.sha256).hexdigest()

def pseudonymize_customer_name(phone_hash: Optional[str]) -> str:
    if not phone_hash:
        return "CUST-GUEST-ANON"
    return f"CUST-{phone_hash[:8].upper()}"

def assert_zero_pii_leakage_verbatim(table: pa.Table) -> None:
    """Uses the verbatim regex from pii-scrubbing.md."""
    for col_name in table.column_names:
        field = table.field(col_name)
        if pa.types.is_string(field.type):
            for value in table[col_name].to_pylist():
                if not value:
                    continue
                str_val = str(value)
                if VERBATIM_PHONE_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Phone number pattern found!")
                if EMAIL_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Email address pattern found!")
                if CCCD_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Citizen ID pattern found!")

def assert_zero_pii_leakage_corrected(table: pa.Table) -> None:
    """Uses the corrected 10-digit regex."""
    for col_name in table.column_names:
        field = table.field(col_name)
        if pa.types.is_string(field.type):
            for value in table[col_name].to_pylist():
                if not value:
                    continue
                str_val = str(value)
                if CORRECTED_PHONE_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Phone number pattern found: '{str_val}'")
                if EMAIL_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Email address pattern found: '{str_val}'")
                if CCCD_LEAK_REGEX.search(str_val):
                    raise RuntimeError(f"PII LEAK DETECTED in column '{col_name}': Citizen ID pattern found: '{str_val}'")


# ============================================================================
# PYTEST TEST CASES
# ============================================================================

class TestAMISVoucherContract:
    """Empirical adversarial test suite for amis-voucher-contract.json."""

    def test_embedded_examples_pass_schema_validation(self) -> None:
        schema_dict, validator = load_amis_schema()
        examples = schema_dict.get("examples", [])
        assert len(examples) > 0, "No examples found in amis-voucher-contract.json"

        for idx, example in enumerate(examples):
            validator.validate(example)
            violations = validate_amis_accounting_rules(example)
            assert violations == [], f"Embedded example {idx} broke accounting rules: {violations}"

    def test_adversarial_missing_warehouse_code(self) -> None:
        schema_dict, validator = load_amis_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        del payload["vouchers"][0]["warehouse_code"]

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "'warehouse_code' is a required property" in str(excinfo.value)

    def test_adversarial_missing_item_code(self) -> None:
        schema_dict, validator = load_amis_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        del payload["vouchers"][0]["line_items"][0]["item_code"]

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "'item_code' is a required property" in str(excinfo.value)

    def test_adversarial_missing_pretax_decomposition(self) -> None:
        schema_dict, validator = load_amis_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        # Case A: Missing unit_price_pretax
        payload_a = copy.deepcopy(payload)
        del payload_a["vouchers"][0]["line_items"][0]["unit_price_pretax"]
        with pytest.raises(jsonschema.ValidationError) as excinfo_a:
            validator.validate(payload_a)
        assert "'unit_price_pretax' is a required property" in str(excinfo_a.value)

        # Case B: Missing pretax_amount
        payload_b = copy.deepcopy(payload)
        del payload_b["vouchers"][0]["line_items"][0]["pretax_amount"]
        with pytest.raises(jsonschema.ValidationError) as excinfo_b:
            validator.validate(payload_b)
        assert "'pretax_amount' is a required property" in str(excinfo_b.value)

    def test_adversarial_invalid_voucher_type(self) -> None:
        schema_dict, validator = load_amis_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        
        # Arbitrary invalid string
        payload["vouchers"][0]["voucher_type"] = "unsupported_invoice_type"
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "is not one of" in str(excinfo.value)

    def test_adversarial_standards_example_voucher_type_mismatch(self) -> None:
        """Verifies that the example in amis-accounting-standards.md line 195 fails schema validation.
        
        amis-accounting-standards.md specifies: 'voucher_type': 'sales_invoice_with_stock_issue'
        amis-voucher-contract.json specifies enum: ['sales_invoice', 'delivery_note_cum_sales_invoice', ...]
        """
        schema_dict, validator = load_amis_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])
        payload["vouchers"][0]["voucher_type"] = "sales_invoice_with_stock_issue"

        with pytest.raises(jsonschema.ValidationError) as excinfo:
            validator.validate(payload)
        assert "'sales_invoice_with_stock_issue' is not one of" in str(excinfo.value)

    def test_adversarial_unbalanced_debits_vs_credits(self) -> None:
        """Evaluates debit-credit balance constraints.
        
        Finding: JSON Schema Draft 2020-12 verifies boolean typing of is_balanced,
        while statutory business accounting rules flag the arithmetic imbalance.
        """
        schema_dict, validator = load_amis_schema()
        payload = copy.deepcopy(schema_dict["examples"][0])

        # Induce severe debit-credit imbalance
        payload["summary"]["total_debit"] = 9999999
        payload["summary"]["total_credit"] = 5750000
        payload["vouchers"][0]["voucher_total_debit"] = 9999999
        payload["vouchers"][0]["voucher_total_credit"] = 5400000

        # In hardened schema: rejects is_balanced: False because schema enforces 'const: true'
        payload["summary"]["is_balanced"] = False
        with pytest.raises(jsonschema.ValidationError):
            validator.validate(payload)

        # In statutory business logic harness: Hard failure / Flagged!
        violations = validate_amis_accounting_rules(payload)
        assert len(violations) >= 2, f"Expected multiple accounting violations, got {violations}"
        assert any("Summary debit-credit imbalance" in v for v in violations)
        assert any("Voucher SHOPEEHNT0826001 unbalanced" in v for v in violations)

        # Fraudulent payload claiming is_balanced = True despite mismatch
        payload["summary"]["is_balanced"] = True
        violations_fraud = validate_amis_accounting_rules(payload)
        assert any("Summary is_balanced is True but debits" in v for v in violations_fraud)


class TestDuckDBConcurrencyLock:
    """Empirical verification of AsyncCrossProcessLock pattern from duckdb-concurrency.md."""

    @pytest.mark.asyncio
    async def test_coroutine_concurrency_serialization(self, tmp_path: Path) -> None:
        db_file = tmp_path / "test_concurrency.duckdb"
        init_con = duckdb.connect(str(db_file), read_only=False)
        init_con.execute("CREATE TABLE counter_table (val INTEGER);")
        init_con.execute("INSERT INTO counter_table VALUES (0);")
        init_con.close()

        lock = AsyncCrossProcessLock(db_file, config=LockConfig(timeout_seconds=5.0))

        async def _coro_worker(worker_id: int) -> None:
            async with lock.acquire():
                con = duckdb.connect(str(db_file), read_only=False)
                try:
                    cur_val = con.execute("SELECT val FROM counter_table;").fetchone()[0]
                    await asyncio.sleep(0.01)
                    con.execute("UPDATE counter_table SET val = ?;", [cur_val + 1])
                finally:
                    con.close()

        tasks = [_coro_worker(i) for i in range(10)]
        await asyncio.gather(*tasks)

        verify_con = duckdb.connect(str(db_file), read_only=True)
        final_val = verify_con.execute("SELECT val FROM counter_table;").fetchone()[0]
        verify_con.close()
        assert final_val == 10, f"Expected 10, got {final_val} - race condition detected!"

    def test_os_process_concurrency(self, tmp_path: Path) -> None:
        db_file = tmp_path / "multiprocess_warehouse.duckdb"
        init_con = duckdb.connect(str(db_file), read_only=False)
        init_con.execute("CREATE TABLE write_test_log (worker_id INTEGER, item_name TEXT, created_at TIMESTAMP);")
        init_con.close()

        num_processes = 3
        records_per_process = 5
        barrier = multiprocessing.Barrier(num_processes)

        processes = []
        for pid in range(num_processes):
            p = multiprocessing.Process(
                target=_os_process_writer,
                args=(str(db_file), pid, records_per_process, barrier),
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join(timeout=15.0)
            assert not p.is_alive(), f"Process {p.pid} hung or timed out"
            assert p.exitcode == 0, f"Process {p.pid} exited with error {p.exitcode}"

        check_con = duckdb.connect(str(db_file), read_only=True)
        total_rows = check_con.execute("SELECT count(*) FROM write_test_log;").fetchone()[0]
        check_con.close()
        expected_rows = num_processes * records_per_process
        assert total_rows == expected_rows, f"Expected {expected_rows} rows, found {total_rows}"

    @pytest.mark.asyncio
    async def test_lock_timeout_escalation(self, tmp_path: Path) -> None:
        db_file = tmp_path / "timeout_warehouse.duckdb"
        lock_held = AsyncCrossProcessLock(db_file, config=LockConfig(timeout_seconds=2.0))
        lock_contender = AsyncCrossProcessLock(db_file, config=LockConfig(timeout_seconds=0.2))

        async def _holder() -> None:
            async with lock_held.acquire():
                await asyncio.sleep(0.6)

        async def _contender() -> None:
            await asyncio.sleep(0.05)
            with pytest.raises(DuckDBLockAcquisitionError) as excinfo:
                async with lock_contender.acquire():
                    pytest.fail("Contender should not have acquired lock!")
            assert "Timed out after 0.2s" in str(excinfo.value)

        await asyncio.gather(_holder(), _contender())

    @pytest.mark.asyncio
    async def test_redis_fail_closed_policy(self, tmp_path: Path) -> None:
        db_file = tmp_path / "failclosed_warehouse.duckdb"

        class BrokenRedisClient:
            async def set(self, *args: Any, **kwargs: Any) -> Any:
                raise ConnectionError("Cluster network partition / Redis cluster unreachable")

        lock = AsyncCrossProcessLock(
            db_file,
            redis_client=BrokenRedisClient(),
            config=LockConfig(timeout_seconds=1.0),
        )

        with pytest.raises(DuckDBFailClosedError) as excinfo:
            async with lock.acquire():
                pytest.fail("Should have failed closed immediately on Redis error")
        assert "Redis lockarbiter failure" in str(excinfo.value)
        assert not lock.file_lock.is_locked, "FileLock was leaked after Redis fail-closed exception!"


class TestPIIScrubbingAndHashing:
    """Empirical verification of Salted HMAC-SHA256 and PII Sanitization rules."""

    def test_phone_normalization_valid_vietnamese_prefixes(self) -> None:
        test_cases = [
            ("0912345678", "84912345678"),
            ("+84 912 345 678", "84912345678"),
            ("84-912.345.678", "84912345678"),
            ("0389998888", "84389998888"),
            ("+84398765432", "84398765432"),
            ("0771234567", "84771234567"),
            ("0561234567", "84561234567"),
            ("0881234567", "84881234567"),
        ]
        for raw, expected in test_cases:
            assert normalize_vietnam_phone(raw) == expected, f"Failed on raw={raw}"

    def test_phone_normalization_invalid_and_malicious_inputs(self) -> None:
        invalid_cases = [
            None,
            "",
            "02438889999",      # Landline (Hanoi 024)
            "02839998888",      # Landline (HCMC 028)
            "19001000",         # Hotline shortcode
            "+14155552671",     # US phone
            "0123456789",       # Obsolete 11-digit prefix 012
            "091234567",        # 9 digits (too short)
            "09123456789",      # 11 digits (too long)
            "840912345678",     # Double prefix (84 + 0)
            "DROP TABLE users;--", # Injection attempt
            "<script>alert(1)</script>",
        ]
        for inv in invalid_cases:
            assert normalize_vietnam_phone(inv) is None, f"Expected None for invalid input: {inv}"

    def test_salted_hmac_sha256_determinism_and_salt_sensitivity(self) -> None:
        phone = "84912345678"
        salt_a = b"high_entropy_secret_salt_a_9981"
        salt_b = b"high_entropy_secret_salt_b_9981"

        # Determinism
        hash1 = hash_phone_number(phone, salt=salt_a)
        hash2 = hash_phone_number(phone, salt=salt_a)
        assert hash1 == hash2, "HMAC-SHA256 must be strictly deterministic for identical salt"
        assert len(hash1) == 64, "SHA256 hex digest must be exactly 64 chars"

        # Salt sensitivity (avalanche effect)
        hash_diff_salt = hash_phone_number(phone, salt=salt_b)
        assert hash1 != hash_diff_salt, "Different salt must produce completely distinct digest"

        # Non-reversible with plain SHA-256 rainbow tables
        plain_sha256 = hashlib.sha256(phone.encode("utf-8")).hexdigest()
        assert hash1 != plain_sha256, "Salted HMAC must never match plain SHA-256"

    def test_missing_salt_raises_critical_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("RETAIL_PII_SALT", raising=False)
        with pytest.raises(PIIScrubbingError) as excinfo:
            hash_phone_number("84912345678", salt=None)
        assert "CRITICAL: RETAIL_PII_SALT environment variable is not configured" in str(excinfo.value)

    def test_customer_pseudonymization_format(self) -> None:
        phone = "84912345678"
        salt = b"test_salt_1234"
        p_hash = hash_phone_number(phone, salt=salt)
        token = pseudonymize_customer_name(p_hash)

        assert token.startswith("CUST-")
        assert len(token) == 13
        assert token[5:] == p_hash[:8].upper()

        anon_token = pseudonymize_customer_name(None)
        assert anon_token == "CUST-GUEST-ANON"

    def test_empirical_vulnerability_in_verbatim_phone_leak_regex(self) -> None:
        r"""EMPIRICAL CHALLENGE: Proves that verbatim regex in pii-scrubbing.md line 183 is vulnerable.
        
        The verbatim regex r'(?:0|\+?84)(?:3|5|7|8|9)[0-9]{7}\b' matches only 9 digits total.
        Because Vietnamese mobile numbers are 10 digits (e.g. '0912345678'), the word boundary \b
        fails to match at digit 9, allowing 10-digit mobile numbers to leak into Silver undetected!
        """
        raw_10_digit_phone = "0912345678"
        table = pa.Table.from_pydict({"customer_phone": [raw_10_digit_phone]})

        # Verbatim function fails to raise RuntimeError - PII leaks undetected!
        try:
            assert_zero_pii_leakage_verbatim(table)
            leak_undetected = True
        except RuntimeError:
            leak_undetected = False

        assert leak_undetected is True, (
            "Vulnerability confirmed: Verbatim PHONE_LEAK_REGEX failed to catch 10-digit phone leak!"
        )

    def test_circuit_breaker_assert_zero_pii_leakage_corrected(self) -> None:
        """Verifies that the corrected circuit breaker catches all PII leaks."""
        clean_table = pa.Table.from_pydict({
            "order_id": ["ORD001", "ORD002"],
            "customer_token": ["CUST-A4F82B91", "CUST-GUEST-ANON"],
            "province_name": ["Hà Nội", "TP. Hồ Chí Minh"],
            "district_name": ["Quận Ba Đình", "Quận 1"],
            "net_amount": [500000.0, 750000.0],
        })
        assert_zero_pii_leakage_corrected(clean_table)

        # Leak 1: 10-digit phone
        leaked_phone_table = pa.Table.from_pydict({
            "order_id": ["ORD001"],
            "raw_customer_phone": ["0912345678"],
        })
        with pytest.raises(RuntimeError) as excinfo1:
            assert_zero_pii_leakage_corrected(leaked_phone_table)
        assert "Phone number pattern found" in str(excinfo1.value)

        # Leak 2: Email leaked
        leaked_email_table = pa.Table.from_pydict({
            "order_id": ["ORD002"],
            "customer_email": ["customer@example.com"],
        })
        with pytest.raises(RuntimeError) as excinfo2:
            assert_zero_pii_leakage_corrected(leaked_email_table)
        assert "Email address pattern found" in str(excinfo2.value)

        # Leak 3: 12-digit Citizen ID (CCCD) leaked
        leaked_cccd_table = pa.Table.from_pydict({
            "order_id": ["ORD003"],
            "national_id": ["001099012345"],
        })
        with pytest.raises(RuntimeError) as excinfo3:
            assert_zero_pii_leakage_corrected(leaked_cccd_table)
        assert "Citizen ID pattern found" in str(excinfo3.value)
