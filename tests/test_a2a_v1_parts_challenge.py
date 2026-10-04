#!/usr/bin/env python3
"""Empirical Challenge & Verification Suite for A2A v1.0 Unified Part Model.

Validates resolution of GitHub Issue #1:
- A2A v1.0 drops the mandatory 'kind' discriminator in favor of member presence
  ("text", "data", "file", "file_ref").
- Unified Part objects without 'kind' MUST validate successfully against:
  1. a2a-message.json
  2. a2a-artifact.json
  3. a2a-task.json
  4. a2a-task-status.json
  5. a2a-task-progress.json
- Backwards compatibility: legacy v0.x parts with 'kind' MUST still validate.
- Invalid parts (empty object, kind-only, invalid types) MUST fail validation.
- Referenced schema resolution (a2a-task-status -> a2a-message) MUST succeed.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from dateutil import parser
import jsonschema
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "core" / "contracts" / "schemas"


def build_format_checker() -> jsonschema.FormatChecker:
    checker = copy.deepcopy(Draft202012Validator.FORMAT_CHECKER)

    @checker.checks("date-time")
    def _check_datetime(val: Any) -> bool:
        if not isinstance(val, str):
            return True
        try:
            parser.isoparse(val)
            return True
        except Exception:
            return False

    return checker


FORMAT_CHECKER = build_format_checker()


def build_registry() -> Registry:
    registry = Registry()
    for path in SCHEMAS_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        res = Resource.from_contents(data)
        registry = registry.with_resource(uri=path.name, resource=res)
        if "$id" in data:
            registry = registry.with_resource(uri=data["$id"], resource=res)
    return registry


GLOBAL_REGISTRY = build_registry()


def load_schema(schema_name: str) -> tuple[dict, Draft202012Validator]:
    path = SCHEMAS_DIR / schema_name
    assert path.is_file(), f"Schema file not found: {path}"
    schema_dict = json.loads(path.read_text(encoding="utf-8"))
    
    validator = Draft202012Validator(
        schema_dict,
        format_checker=FORMAT_CHECKER,
        registry=GLOBAL_REGISTRY
    )
    return schema_dict, validator


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

def test_bundled_examples() -> None:
    """Ensure all 5 A2A schemas' bundled examples pass schema validation."""
    schemas_to_check = [
        "a2a-message.json",
        "a2a-artifact.json",
        "a2a-task.json",
        "a2a-task-status.json",
        "a2a-task-progress.json",
    ]
    for name in schemas_to_check:
        schema_dict, validator = load_schema(name)
        examples = schema_dict.get("examples", [])
        assert examples, f"{name} has no bundled examples"
        for idx, ex in enumerate(examples):
            errors = list(validator.iter_errors(ex))
            assert not errors, f"{name} example[{idx}] failed validation: {[e.message for e in errors]}"
    print("PASS: test_bundled_examples (all 5 A2A schemas validate bundled examples)")


def test_a2a_v1_pure_message_parts() -> None:
    """Verify a2a-message.json accepts unified v1.0 parts without 'kind'."""
    _, validator = load_schema("a2a-message.json")

    # Pure text part (no kind)
    msg_text = {
        "message_id": "msg-101",
        "role": "worker",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [
            {"text": "Task execution completed successfully."}
        ]
    }
    assert validator.is_valid(msg_text), "Pure text part failed validation"

    # Pure data part (no kind)
    msg_data = {
        "message_id": "msg-102",
        "role": "agent",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [
            {"data": {"status": "ok", "items_processed": 42}}
        ]
    }
    assert validator.is_valid(msg_data), "Pure data part failed validation"

    # Pure file object part (no kind)
    msg_file = {
        "message_id": "msg-103",
        "role": "worker",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [
            {"file": {"name": "diff.patch", "mime_type": "text/x-diff", "bytes": 1024}}
        ]
    }
    assert validator.is_valid(msg_file), "Pure file part failed validation"

    # Pure file_ref part (no kind)
    msg_file_ref = {
        "message_id": "msg-104",
        "role": "delegator",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [
            {"file_ref": "contracts/schemas/a2a-task.json"}
        ]
    }
    assert validator.is_valid(msg_file_ref), "Pure file_ref part failed validation"

    # Multimodal parts in single message
    msg_multimodal = {
        "message_id": "msg-105",
        "role": "agent",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [
            {"text": "Here is the architectural evaluation:"},
            {"data": {"tps": 610000, "p99_latency_ms": 12.4}},
            {"file_ref": "reports/knowledge/ecommerce/alipay-610k-tps.md"},
            {"file": {"uri": "https://storage.internal/traces/trace-001.bin"}}
        ]
    }
    assert validator.is_valid(msg_multimodal), "Multimodal parts message failed validation"
    print("PASS: test_a2a_v1_pure_message_parts (pure v1.0 parts without kind pass a2a-message.json)")


def test_a2a_v1_pure_artifact_parts() -> None:
    """Verify a2a-artifact.json accepts unified v1.0 parts without 'kind'."""
    _, validator = load_schema("a2a-artifact.json")

    artifact = {
        "task_id": "task-uuid-v4-9988",
        "state": "completed",
        "status": "completed",
        "parts": [
            {"text": "Unified v1.0 Part deliverable emitted by worker."},
            {"data": {"slices_shipped": 3, "verified": True}},
            {"file_ref": "core/contracts/schemas/a2a-artifact.json"}
        ],
        "evidence": [
            "100% tests pass on main branch."
        ]
    }
    assert validator.is_valid(artifact), f"Unified artifact failed validation: {list(validator.iter_errors(artifact))}"
    print("PASS: test_a2a_v1_pure_artifact_parts (pure v1.0 parts pass a2a-artifact.json)")


def test_backwards_compatibility_legacy_parts() -> None:
    """Ensure legacy v0.x parts with explicit 'kind' discriminator remain valid."""
    _, msg_validator = load_schema("a2a-message.json")
    _, art_validator = load_schema("a2a-artifact.json")

    legacy_msg = {
        "message_id": "msg-legacy-001",
        "role": "agent",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [
            {"kind": "text", "text": "Legacy text part"},
            {"kind": "data", "data": {"foo": "bar"}},
            {"kind": "file", "file_ref": "legacy/path.txt"},
            {"kind": "json", "data": {"version": 0.3}}
        ]
    }
    assert msg_validator.is_valid(legacy_msg), "Legacy message parts failed validation"

    legacy_art = {
        "task_id": "task-legacy-002",
        "status": "completed",
        "parts": [
            {"kind": "text", "text": "Legacy artifact part"},
            {"kind": "file", "file_ref": "evidence/proof.txt"}
        ]
    }
    assert art_validator.is_valid(legacy_art), "Legacy artifact parts failed validation"
    print("PASS: test_backwards_compatibility_legacy_parts (v0.x parts with kind remain valid)")


def test_adversarial_invalid_parts_rejected() -> None:
    """Verify malformed, empty, or kind-only parts are rejected by schema."""
    _, msg_validator = load_schema("a2a-message.json")
    _, art_validator = load_schema("a2a-artifact.json")

    # 1. Empty part object {}
    bad_empty = {
        "message_id": "msg-bad-01",
        "role": "worker",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [{}]
    }
    assert not msg_validator.is_valid(bad_empty), "Empty part {} unexpectedly passed validation"

    # 2. Kind-only part without any payload content
    bad_kind_only = {
        "message_id": "msg-bad-02",
        "role": "worker",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [{"kind": "text"}]
    }
    assert not msg_validator.is_valid(bad_kind_only), "Kind-only part unexpectedly passed validation"

    # 3. Metadata-only part without any payload content
    bad_meta_only = {
        "message_id": "msg-bad-03",
        "role": "worker",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [{"metadata": {"annotation": "no body"}}]
    }
    assert not msg_validator.is_valid(bad_meta_only), "Metadata-only part unexpectedly passed validation"

    # 4. Invalid kind enum
    bad_kind_enum = {
        "message_id": "msg-bad-04",
        "role": "worker",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [{"kind": "unsupported_kind", "text": "foo"}]
    }
    assert not msg_validator.is_valid(bad_kind_enum), "Invalid kind enum unexpectedly passed validation"

    # 5. Invalid data type for text (e.g. integer instead of string)
    bad_text_type = {
        "message_id": "msg-bad-05",
        "role": "worker",
        "timestamp": "2026-10-05T08:00:00Z",
        "parts": [{"text": 12345}]
    }
    assert not msg_validator.is_valid(bad_text_type), "Non-string text part unexpectedly passed validation"

    # 6. Invalid data type for data (e.g. string instead of object)
    bad_data_type = {
        "task_id": "task-bad-06",
        "status": "completed",
        "parts": [{"data": "invalid-scalar-data"}]
    }
    assert not art_validator.is_valid(bad_data_type), "Non-object data part unexpectedly passed validation"

    # 7. Invalid data type for file (e.g. array instead of object)
    bad_file_type = {
        "task_id": "task-bad-07",
        "status": "completed",
        "parts": [{"file": ["not", "an", "object"]}]
    }
    assert not art_validator.is_valid(bad_file_type), "Non-object file part unexpectedly passed validation"

    print("PASS: test_adversarial_invalid_parts_rejected (empty, kind-only, and malformed parts rejected)")


def test_task_status_with_referenced_v1_messages() -> None:
    """Verify a2a-task-status.json validates messages via $ref with unified v1.0 parts."""
    _, validator = load_schema("a2a-task-status.json")

    status_payload = {
        "task_id": "task-stream-009",
        "state": "working",
        "delegator": "agent-coordinator",
        "assignee_role": "backend-developer",
        "interaction_mode": "stream",
        "updated_at": "2026-10-05T08:15:00Z",
        "messages": [
            {
                "message_id": "msg-001",
                "role": "delegator",
                "timestamp": "2026-10-05T08:00:00Z",
                "parts": [
                    {"text": "Start slice-01 implementation."}
                ]
            },
            {
                "message_id": "msg-002",
                "role": "worker",
                "timestamp": "2026-10-05T08:14:00Z",
                "parts": [
                    {"text": "Slice-01 code committed; running tests."},
                    {"data": {"tests_run": 15, "tests_passed": 15}}
                ]
            }
        ]
    }
    assert validator.is_valid(status_payload), f"Task status with v1.0 messages failed: {list(validator.iter_errors(status_payload))}"
    print("PASS: test_task_status_with_referenced_v1_messages (a2a-task-status with $ref to a2a-message passes)")


def main() -> int:
    print("=== A2A v1.0 Unified Part Model Test Suite ===")
    test_bundled_examples()
    test_a2a_v1_pure_message_parts()
    test_a2a_v1_pure_artifact_parts()
    test_backwards_compatibility_legacy_parts()
    test_adversarial_invalid_parts_rejected()
    test_task_status_with_referenced_v1_messages()
    print("=== ALL 6/6 TEST SUITES PASSED (A2A Issue #1 Verified Fixed) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
