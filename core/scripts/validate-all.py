#!/usr/bin/env python3
"""Run all core pack validators.

2026 upgrades:
- --format text|json|sarif  structured output for CI consumption
- --parallel                run validators concurrently (ThreadPoolExecutor)
- --fail-fast               stop on first failure
- exit 0 = pass, exit 1 = fail, exit 2 = script error
- SARIF 2.1.0 output compatible with GitHub Code Scanning upload-sarif action
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent

VALIDATORS = (
    "validate-rules.py",
    "validate-skills.py",
    "validate-roles.py",
    "validate-workflows.py",
    "validate-packs.py",
    "validate-overlays.py",
    "validate-2026-compliance.py",
    "validate-contracts.py",
    "validate-a2a-compliance.py",
    "validate-agent-cards.py",
    "validate-standardization.py",
    "validate-version-sync.py",
    "validate-indexes.py",
    "validate-policy-consistency.py",
    "validate-skill-ownership.py",
    "validate-contract-coverage.py",
)

TOOL_NAME = "agent-pack-validator"
TOOL_VERSION = "4.0.0"


@dataclass
class ValidatorResult:
    name: str
    passed: bool
    exit_code: int
    output: str
    duration_ms: float
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def run_validator(script: str) -> ValidatorResult:
    path = ROOT / script
    t0 = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        duration = (time.monotonic() - t0) * 1000
        output = (result.stdout + result.stderr).strip()
        passed = result.returncode == 0
        errors: list[str] = []
        warnings: list[str] = []
        for line in output.splitlines():
            stripped = line.lstrip("- ").strip()
            if line.startswith("warning:"):
                warnings.append(stripped.removeprefix("warning:").strip())
            elif not passed and stripped and not stripped.startswith("Pass") and not stripped.startswith("All"):
                if any(stripped.startswith(p) for p in ("- ", "core/", "contract", "version", "missing", "unknown")):
                    errors.append(stripped.lstrip("- "))
        return ValidatorResult(
            name=script,
            passed=passed,
            exit_code=result.returncode,
            output=output,
            duration_ms=round(duration, 1),
            errors=errors,
            warnings=warnings,
        )
    except Exception as exc:  # noqa: BLE001
        duration = (time.monotonic() - t0) * 1000
        return ValidatorResult(
            name=script,
            passed=False,
            exit_code=2,
            output=str(exc),
            duration_ms=round(duration, 1),
            errors=[str(exc)],
        )


def emit_text(results: list[ValidatorResult]) -> None:
    for r in results:
        print(r.output)


def emit_json(results: list[ValidatorResult]) -> None:
    report = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "passed": all(r.passed for r in results),
        "total": len(results),
        "failed": sum(1 for r in results if not r.passed),
        "results": [
            {
                "name": r.name,
                "passed": r.passed,
                "exit_code": r.exit_code,
                "duration_ms": r.duration_ms,
                "errors": r.errors,
                "warnings": r.warnings,
            }
            for r in results
        ],
    }
    print(json.dumps(report, indent=2))


def emit_sarif(results: list[ValidatorResult]) -> None:
    """Emit SARIF 2.1.0 report compatible with GitHub Code Scanning upload-sarif."""
    sarif_results = []
    rules: list[dict] = []
    rule_ids: set[str] = set()

    for r in results:
        rule_id = r.name.removesuffix(".py").replace("-", "_")
        if rule_id not in rule_ids:
            rule_ids.add(rule_id)
            rules.append(
                {
                    "id": rule_id,
                    "name": r.name.removesuffix(".py").replace("-", " ").title(),
                    "shortDescription": {"text": f"Agent pack validator: {r.name}"},
                    "defaultConfiguration": {"level": "error"},
                }
            )
        if not r.passed:
            for err in r.errors or [r.output[:500]]:
                sarif_results.append(
                    {
                        "ruleId": rule_id,
                        "level": "error",
                        "message": {"text": err},
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {
                                        "uri": f"core/scripts/{r.name}",
                                        "uriBaseId": "%SRCROOT%",
                                    }
                                }
                            }
                        ],
                    }
                )
        for warn in r.warnings:
            sarif_results.append(
                {
                    "ruleId": rule_id,
                    "level": "warning",
                    "message": {"text": warn},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {
                                    "uri": f"core/scripts/{r.name}",
                                    "uriBaseId": "%SRCROOT%",
                                }
                            }
                        }
                    ],
                }
            )

    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": TOOL_NAME,
                        "version": TOOL_VERSION,
                        "informationUri": "https://github.com/vesviet/agent-skills",
                        "rules": rules,
                    }
                },
                "results": sarif_results,
            }
        ],
    }
    print(json.dumps(sarif, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run all core pack validators.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exit codes:\n"
            "  0 = all validators passed\n"
            "  1 = one or more validators failed\n"
            "  2 = script error (missing validator, crash)\n"
        ),
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "sarif"],
        default="text",
        help="Output format (default: text). Use 'sarif' for GitHub Code Scanning.",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run validators concurrently using a thread pool.",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop after the first failing validator (text mode only).",
    )
    args = parser.parse_args()

    results: list[ValidatorResult] = []

    try:
        if args.parallel:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                futures = {pool.submit(run_validator, v): v for v in VALIDATORS}
                # collect in original order
                ordered: dict[str, ValidatorResult] = {}
                for future in concurrent.futures.as_completed(futures):
                    script = futures[future]
                    ordered[script] = future.result()
            results = [ordered[v] for v in VALIDATORS if v in ordered]
        else:
            for script in VALIDATORS:
                r = run_validator(script)
                if args.format == "text":
                    print(r.output)
                results.append(r)
                if args.fail_fast and not r.passed:
                    break
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        emit_json(results)
    elif args.format == "sarif":
        emit_sarif(results)
    elif args.parallel:
        # parallel mode buffered text — emit now
        emit_text(results)

    overall_passed = all(r.passed for r in results)
    if args.format == "text" and overall_passed:
        print("All core validators passed.")

    return 0 if overall_passed else 1


if __name__ == "__main__":
    sys.exit(main())
