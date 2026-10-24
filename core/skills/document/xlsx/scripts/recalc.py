#!/usr/bin/env python3
"""
Excel Formula Recalculation and Auditing Oracle (recalc.py).

Zero-Formula-Error Guardrail for Financial Settlement (BF-12) & 20M Reports (LMO-5547).
Enforces the Zero Formula Error invariant on generated and modified Excel workbooks.
Integrates headless LibreOffice recalculation, external link risk detection,
and cell-level error auditing.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

try:
    import openpyxl
except ImportError:
    openpyxl = None

EXCEL_ERROR_TOKENS: Set[str] = {
    "#NULL!",
    "#DIV/0!",
    "#VALUE!",
    "#REF!",
    "#NAME?",
    "#NUM!",
    "#N/A",
}


def find_libreoffice_binary() -> Optional[str]:
    """Locate headless LibreOffice / soffice binary across standard system paths."""
    candidates = [
        "libreoffice",
        "soffice",
        "/snap/bin/libreoffice",
        "/usr/bin/libreoffice",
        "/usr/bin/soffice",
        "/usr/local/bin/libreoffice",
        "/usr/local/bin/soffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]
    for candidate in candidates:
        if shutil.which(candidate) or os.path.isfile(candidate):
            return candidate
    return None


def get_recalc_staging_dir() -> Path:
    """
    Get a staging directory accessible by LibreOffice.
    Snap-confined LibreOffice cannot access host /tmp or hidden directories in $HOME.
    """
    snap_common = Path.home() / "snap" / "libreoffice" / "common"
    if snap_common.exists():
        staging_root = snap_common / "recalc_staging"
    else:
        staging_root = Path.home() / "recalc_staging"
        try:
            staging_root.mkdir(parents=True, exist_ok=True)
        except Exception:
            staging_root = Path(tempfile.gettempdir())
    staging_root.mkdir(parents=True, exist_ok=True)
    return staging_root


def external_links_at_risk(workbook_path: Path) -> List[str]:
    """
    Detect external workbook links and dependencies in the .xlsx package.
    Recalculating workbooks with external links in headless environments can drop
    or corrupt linked values.
    """
    risks: List[str] = []
    if not zipfile.is_zipfile(workbook_path):
        return ["Not a valid OOXML zip package"]

    try:
        with zipfile.ZipFile(workbook_path, "r") as z:
            for name in z.namelist():
                if name.startswith("xl/externalLinks/") and name.endswith(".xml"):
                    risks.append(f"External link part found: {name}")

            # Scan sheet XMLs for external references: [1]Sheet1!A1 or '[Book.xlsx]Sheet'!A1
            sheet_regex = re.compile(r"\[\d+\]|'\[[^\]]+\]")
            for name in z.namelist():
                if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
                    content = z.read(name).decode("utf-8", errors="ignore")
                    if sheet_regex.search(content):
                        risks.append(f"External workbook formula reference found in {name}")
    except Exception as e:
        risks.append(f"Package inspection error: {e}")

    return risks


def run_headless_recalculation(
    libreoffice_bin: str, workbook_path: Path, timeout_sec: int = 30
) -> Tuple[bool, str, Optional[Path], Optional[str]]:
    """
    Invoke LibreOffice in headless mode to force recalculation of formulas and save results to a temporary .xlsx workbook.
    Returns: (success, message, recalculated_workbook_path, staging_directory_path)
    """
    staging_root = get_recalc_staging_dir()
    run_id = f"recalc_{os.getpid()}_{uuid.uuid4().hex[:8]}"
    run_dir = staging_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    profile_dir = run_dir / "profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    in_dir = run_dir / "in"
    in_dir.mkdir(parents=True, exist_ok=True)
    out_dir = run_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    staged_input = in_dir / workbook_path.name
    try:
        shutil.copyfile(workbook_path, staged_input)
    except Exception as e:
        return False, f"Staging copy error: {e}", None, str(run_dir)

    cmd = [
        libreoffice_bin,
        "--headless",
        f"-env:UserInstallation=file://{profile_dir}",
        "--convert-to",
        "xlsx",
        "--outdir",
        str(out_dir),
        str(staged_input),
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
        out_file = out_dir / staged_input.name
        if res.returncode != 0 or not out_file.is_file():
            err_msg = res.stderr.strip() or f"conversion failed (exit {res.returncode})"
            return False, f"LibreOffice failed: {err_msg}", None, str(run_dir)
        return True, "Headless recalculation completed", out_file, str(run_dir)
    except subprocess.TimeoutExpired:
        return False, f"Headless recalculation timed out after {timeout_sec}s", None, str(run_dir)
    except Exception as e:
        return False, f"Execution error: {str(e)}", None, str(run_dir)


def audit_workbook_errors(
    workbook_path: Path,
    recalculated_path: Optional[Path] = None,
    allow_unresolved_external: bool = False,
) -> Dict[str, Any]:
    """
    Scan workbook for formula errors using openpyxl two-pass verification.
    Pass 1: data_only=False (inspect formulas, syntax errors).
    Pass 2: data_only=True (inspect computed cached values from recalculated or original workbook).
    """
    if openpyxl is None:
        return {
            "status": "FAILED",
            "error": "openpyxl library is required for cell-level formula auditing",
            "errors_found": True,
            "error_count": 1,
            "errors": [{"error": "openpyxl not installed"}],
            "error_details": [],
            "formula_count": 0,
            "total_cells_checked": 0,
            "zero_error_invariant_verified": False,
        }

    errors: List[Dict[str, str]] = []
    formula_count = 0
    total_cells = 0
    external_regex = re.compile(r"\[\d+\]|'\[[^\]]+\]")

    try:
        # Pass 1: data_only=False (inspect formulas, syntax errors)
        wb_formula = openpyxl.load_workbook(workbook_path, data_only=False, read_only=False)
    except Exception as e:
        return {
            "status": "FAILED",
            "error": f"Failed to load workbook formulas: {e}",
            "errors_found": True,
            "error_count": 1,
            "errors": [{"error": str(e)}],
            "error_details": [],
            "formula_count": 0,
            "total_cells_checked": 0,
            "zero_error_invariant_verified": False,
        }

    try:
        # Pass 2: data_only=True (inspect computed cached values from recalculated or original workbook)
        data_source = recalculated_path if (recalculated_path and recalculated_path.is_file()) else workbook_path
        wb_data = openpyxl.load_workbook(data_source, data_only=True, read_only=False)
    except Exception:
        wb_data = None

    for sheet_name in wb_formula.sheetnames:
        ws_formula = wb_formula[sheet_name]
        ws_data = wb_data[sheet_name] if wb_data and sheet_name in wb_data.sheetnames else None

        for row in ws_formula.iter_rows():
            for cell in row:
                total_cells += 1
                coord = cell.coordinate
                val_formula = cell.value

                formula_str = ""
                cell_has_error = False
                if isinstance(val_formula, str) and val_formula.startswith("="):
                    formula_count += 1
                    formula_str = val_formula
                    # Check for literal error token inside formula expression
                    for err_token in EXCEL_ERROR_TOKENS:
                        if err_token in formula_str:
                            errors.append({
                                "sheet": sheet_name,
                                "cell": coord,
                                "error_type": "formula_syntax_error",
                                "value": formula_str,
                                "formula": formula_str,
                            })
                            cell_has_error = True
                            break

                # Check evaluated value in data sheet if not already recorded as formula syntax error
                if not cell_has_error and ws_data is not None:
                    val_eval = ws_data[coord].value
                    val_eval_str = str(val_eval).strip() if val_eval is not None else ""
                    if val_eval_str in EXCEL_ERROR_TOKENS:
                        # Under --force, unresolved remote external dependencies evaluating to #N/A or #REF!
                        # in headless mode (due to missing remote files) are bypassed
                        is_external_ref = bool(external_regex.search(formula_str))
                        if allow_unresolved_external and is_external_ref and val_eval_str in {"#N/A", "#REF!"}:
                            pass
                        else:
                            errors.append({
                                "sheet": sheet_name,
                                "cell": coord,
                                "error_type": val_eval_str,
                                "value": val_eval_str,
                                "formula": formula_str,
                            })

    wb_formula.close()
    if wb_data:
        wb_data.close()

    errors_found = len(errors) > 0
    return {
        "status": "FAILED" if errors_found else "SUCCESS",
        "file": str(workbook_path),
        "total_cells_checked": total_cells,
        "formula_count": formula_count,
        "error_count": len(errors),
        "errors_found": errors_found,
        "errors": errors,
        "error_details": errors,
        "zero_error_invariant_verified": not errors_found,
        "tool": "recalc.py",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Excel workbook for formula errors (BF-12 / LMO-5547).",
        usage="%(prog)s [workbook] [--file FILE] [--output-dir DIR] [--json] [--verbose] [--timeout SEC] [--force] [--zero-error-fail]",
    )
    parser.add_argument("workbook", nargs="?", default=None, type=Path, help="Target .xlsx workbook path")
    parser.add_argument("--file", type=Path, default=None, help="Target .xlsx workbook path (alternative to positional)")
    parser.add_argument("--output-dir", type=Path, default=None, help="Directory to save audit report")
    parser.add_argument("--timeout", type=int, default=30, help="Recalculation timeout in seconds (default: 30)")
    parser.add_argument("--force", action="store_true", help="Force recalculation even if external links are detected")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    parser.add_argument("--zero-error-fail", action="store_true", help="Explicitly assert zero formula error invariant (always enforced)")

    args = parser.parse_args()

    target_path = args.file or args.workbook
    if not target_path:
        parser.print_help(sys.stderr)
        return 2

    wb_path = target_path.resolve()
    if not wb_path.is_file():
        print(f"Error: File not found: {wb_path}", file=sys.stderr)
        return 2

    # Check external links
    risks = external_links_at_risk(wb_path)
    if risks and not args.force:
        msg = f"Warning: External dependencies detected in {wb_path.name}:\n" + "\n".join(f"  - {r}" for r in risks)
        msg += "\nRecalculation aborted to protect external data. Use --force to override."
        if args.json:
            result = {
                "status": "FAILED",
                "recalc_executed": False,
                "external_links_status": "blocked",
                "risks": risks,
                "errors_found": True,
                "error_count": len(risks),
                "zero_error_invariant_verified": False,
            }
            print(json.dumps(result, indent=2))
        else:
            print(msg, file=sys.stderr)
        return 1

    # Attempt headless recalculation if LibreOffice is present
    lo_bin = find_libreoffice_binary()
    recalc_executed = False
    recalc_message = ""
    recalculated_path: Optional[Path] = None
    staging_dir: Optional[str] = None

    if lo_bin:
        success, recalc_message, recalculated_path, staging_dir = run_headless_recalculation(
            lo_bin, wb_path, args.timeout
        )
        recalc_executed = success
    else:
        recalc_message = "LibreOffice not detected; skipping headless recalculation pass"

    try:
        # Audit workbook errors
        audit = audit_workbook_errors(
            wb_path,
            recalculated_path=recalculated_path,
            allow_unresolved_external=args.force,
        )
    finally:
        if staging_dir and os.path.isdir(staging_dir):
            shutil.rmtree(staging_dir, ignore_errors=True)

    audit["recalc_executed"] = recalc_executed
    audit["recalc_engine"] = "libreoffice-headless" if lo_bin else "openpyxl-data-only"
    audit["recalc_message"] = recalc_message
    audit["external_links_status"] = "clean" if not risks else ("forced" if args.force else "risk_detected")

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        report_file = args.output_dir / f"{wb_path.stem}_recalc_report.json"
        with open(report_file, "w") as f:
            json.dump(audit, f, indent=2)

    if args.json:
        print(json.dumps(audit, indent=2))
        return 1 if audit["errors_found"] else 0
    else:
        print("=" * 80)
        print(f"EXCEL FORMULA INTEGRITY AUDIT: {wb_path.name}")
        print("=" * 80)
        print(f"Status            : {audit['status']}")
        print(f"Engine            : {audit['recalc_engine']}")
        print(f"Recalc Executed   : {audit['recalc_executed']} ({recalc_message})")
        print(f"External Links    : {audit['external_links_status']}")
        print(f"Total Errors Found: {audit['error_count']}")
        print(f"Formulas Checked  : {audit['formula_count']}")
        print(f"Cells Checked     : {audit['total_cells_checked']}")
        print("-" * 80)
        if audit["errors_found"]:
            print(f"{'Sheet':<20} | {'Cell':<8} | {'Error':<12} | {'Formula'}")
            print("-" * 80)
            for err in audit["error_details"]:
                sheet = err.get("sheet", "")
                cell = err.get("cell", "")
                val = err.get("value") or err.get("error_type", "")
                formula = err.get("formula", "")
                print(f"{sheet:<20} | {cell:<8} | {val:<12} | {formula}")
            print("=" * 80)
            print("❌ VERDICT: FAIL (Zero Formula Error invariant violated)")
            return 1
        else:
            print("🎉 VERDICT: PASS (Zero formula errors detected)")
            return 0


if __name__ == "__main__":
    sys.exit(main())
