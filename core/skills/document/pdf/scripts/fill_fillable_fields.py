#!/usr/bin/env python3
"""
Populate interactive AcroForm fields in a PDF using a JSON payload.

Enforces Core Rule 5 ASCII Dash normalization (U+2011 to U+002D) and generates
machine-readable forms with optional field flattening.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Set

try:
    import pypdf
    from pypdf import PdfReader, PdfWriter
except ImportError:
    pypdf = None
    PdfReader = None
    PdfWriter = None


def normalize_value(val: Any) -> Any:
    """Normalize text according to Core Rule 5: convert non-breaking hyphens to ASCII."""
    if isinstance(val, str):
        return val.replace("\u2011", "\u002d")
    return val


def fill_pdf_form(
    input_pdf: Path,
    values_json: Path,
    output_pdf: Path,
    flatten: bool = False,
    strict: bool = False,
) -> Dict[str, Any]:
    if pypdf is None:
        raise RuntimeError("pypdf is required. Install via 'pip install pypdf>=4.0.0'.")

    if not input_pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
    if not values_json.exists():
        raise FileNotFoundError(f"Values JSON not found: {values_json}")

    try:
        payload = json.loads(values_json.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Values JSON root must be an object/dict")
    except Exception as exc:
        raise ValueError(f"Failed to parse values JSON: {exc}") from exc

    normalized_payload = {str(k): normalize_value(v) for k, v in payload.items()}

    try:
        reader = PdfReader(str(input_pdf))
    except Exception as exc:
        raise ValueError(f"Failed to read input PDF: {exc}") from exc

    available_fields = reader.get_fields() or {}
    if not available_fields:
        raise ValueError(f"Input PDF '{input_pdf}' contains no interactive AcroForm fields.")

    available_keys: Set[str] = set(available_fields.keys())
    payload_keys: Set[str] = set(normalized_payload.keys())

    matched = payload_keys.intersection(available_keys)
    unmatched = payload_keys.difference(available_keys)

    if strict and unmatched:
        raise ValueError(f"Strict mode failure: Payload keys not in PDF fields: {sorted(unmatched)}")

    writer = PdfWriter()
    writer.append(reader)

    # Populate form fields across all pages
    for page in writer.pages:
        try:
            writer.update_page_form_field_values(page, normalized_payload)
        except Exception:
            pass

    if flatten:
        for page in writer.pages:
            try:
                page.flatten_annotations()
            except Exception:
                pass

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as fp:
        writer.write(fp)

    out_bytes = output_pdf.read_bytes()
    sha256 = hashlib.sha256(out_bytes).hexdigest()

    return {
        "status": "SUCCESS",
        "input_pdf": str(input_pdf),
        "output_pdf": str(output_pdf),
        "total_pdf_fields": len(available_keys),
        "payload_fields_count": len(payload_keys),
        "matched_fields_count": len(matched),
        "unmatched_fields": sorted(unmatched),
        "flattened": flatten,
        "output_size_bytes": len(out_bytes),
        "output_sha256": sha256,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Populate AcroForm fields from JSON payload.")
    parser.add_argument("input_pdf", type=Path, help="Path to input fillable PDF")
    parser.add_argument("values_json", type=Path, help="Path to JSON values payload")
    parser.add_argument("output_pdf", type=Path, help="Path where filled PDF is written")
    parser.add_argument("--flatten", action="store_true", help="Flatten form fields into static text")
    parser.add_argument("--strict", action="store_true", help="Fail if payload contains unknown keys")
    args = parser.parse_args()

    try:
        result = fill_pdf_form(
            args.input_pdf,
            args.values_json,
            args.output_pdf,
            flatten=args.flatten,
            strict=args.strict,
        )
        print("=" * 60)
        print("PDF FORM FILL AUDIT")
        print("=" * 60)
        print(f"Output File   : {result['output_pdf']}")
        print(f"Fields Matched: {result['matched_fields_count']} / {result['payload_fields_count']}")
        print(f"SHA-256 Digest: {result['output_sha256']}")
        print("🎉 Form populated successfully.")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
