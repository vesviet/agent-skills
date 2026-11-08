#!/usr/bin/env python3
"""
Inspect and discover interactive AcroForm fields in PDF documents.

Scans PDF files using pypdf, reporting field names, types, default values,
and validation flags (Required, Read-Only). Emits formatted tables or JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import pypdf
    from pypdf import PdfReader
except ImportError:
    pypdf = None
    PdfReader = None

FIELD_TYPE_MAP: Dict[str, str] = {
    "/Tx": "Text",
    "/Btn": "Button/Checkbox",
    "/Ch": "Choice/Dropdown",
    "/Sig": "Signature",
}


def inspect_pdf_fields(pdf_path: Path) -> Dict[str, Any]:
    if pypdf is None:
        raise RuntimeError("pypdf is required. Install via 'pip install pypdf>=4.0.0'.")

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        raise ValueError(f"Failed to parse PDF document: {exc}") from exc

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise PermissionError(f"PDF is encrypted and requires a password: {exc}") from exc

    raw_fields = reader.get_fields() or {}
    fields_list: List[Dict[str, Any]] = []

    for name, field_obj in raw_fields.items():
        if not isinstance(field_obj, dict):
            continue

        raw_type = str(field_obj.get("/FT", "Unknown"))
        readable_type = FIELD_TYPE_MAP.get(raw_type, raw_type)
        value = field_obj.get("/V", "")
        flags = int(field_obj.get("/Ff", 0) or 0)

        read_only = bool(flags & 1)
        required = bool(flags & 2)

        fields_list.append({
            "name": name,
            "type": readable_type,
            "field_type_raw": raw_type,
            "value": str(value) if value is not None else "",
            "read_only": read_only,
            "required": required,
        })

    return {
        "file": str(pdf_path),
        "page_count": len(reader.pages),
        "is_fillable": len(fields_list) > 0,
        "field_count": len(fields_list),
        "fields": fields_list,
    }


def format_text_table(data: Dict[str, Any]) -> str:
    lines = [
        "=" * 70,
        f"PDF ACROFORM FIELD AUDIT: {data['file']}",
        "=" * 70,
        f"Page Count   : {data['page_count']}",
        f"Is Fillable  : {data['is_fillable']}",
        f"Field Count  : {data['field_count']}",
        "-" * 70,
    ]

    if not data["fields"]:
        lines.append("No interactive AcroForm fields discovered in this document.")
        lines.append("=" * 70)
        return "\n".join(lines)

    lines.append(f"{'#':<4} {'Field Name':<30} {'Type':<18} {'Flags':<12}")
    lines.append("-" * 70)

    for idx, f in enumerate(data["fields"], 1):
        flags = []
        if f["required"]:
            flags.append("REQ")
        if f["read_only"]:
            flags.append("RO")
        flags_str = ",".join(flags) if flags else "-"
        lines.append(f"{idx:<4} {f['name'][:28]:<30} {f['type'][:16]:<18} {flags_str:<12}")

    lines.append("=" * 70)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect interactive AcroForm fields in a PDF.")
    parser.add_argument("pdf_path", type=Path, help="Path to input PDF file")
    parser.add_argument("--json", action="store_true", help="Emit output as JSON")
    parser.add_argument("--strict", action="store_true", help="Exit 2 if no fillable fields exist")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Save report to file")
    args = parser.parse_args()

    try:
        report = inspect_pdf_fields(args.pdf_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    out_content = json.dumps(report, indent=2) if args.json else format_text_table(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out_content, encoding="utf-8")
    else:
        print(out_content)

    if args.strict and not report["is_fillable"]:
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
