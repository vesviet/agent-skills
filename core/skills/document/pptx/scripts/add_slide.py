#!/usr/bin/env python3
"""
PowerPoint OOXML Slide Duplication Engine (add_slide.py).

Duplicates an existing slide XML, creates matching relationship files, registers
the new slide ID in ppt/presentation.xml, and updates [Content_Types].xml.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def duplicate_slide(unpacked_dir: Path, source_slide_num: int, target_slide_num: int) -> None:
    ppt_dir = unpacked_dir / "ppt"
    slides_dir = ppt_dir / "slides"
    rels_dir = slides_dir / "_rels"

    src_xml = slides_dir / f"slide{source_slide_num}.xml"
    src_rels = rels_dir / f"slide{source_slide_num}.xml.rels"
    dst_xml = slides_dir / f"slide{target_slide_num}.xml"
    dst_rels = rels_dir / f"slide{target_slide_num}.xml.rels"

    if not src_xml.exists():
        raise FileNotFoundError(f"Source slide {src_xml} does not exist.")

    # Copy slide XML and relationship file
    shutil.copy2(src_xml, dst_xml)
    if src_rels.exists():
        shutil.copy2(src_rels, dst_rels)

    # Register in [Content_Types].xml
    ct_file = unpacked_dir / "[Content_Types].xml"
    ct_text = ct_file.read_text(encoding="utf-8")
    override_entry = (
        f'<Override PartName="/ppt/slides/slide{target_slide_num}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
    )
    if override_entry not in ct_text:
        ct_text = ct_text.replace("</Types>", f"  {override_entry}\n</Types>")
        ct_file.write_text(ct_text, encoding="utf-8")

    # Register in ppt/_rels/presentation.xml.rels
    pres_rels_file = ppt_dir / "_rels" / "presentation.xml.rels"
    pres_rels_text = pres_rels_file.read_text(encoding="utf-8")

    rids = [int(m) for m in re.findall(r'Id="rId(\d+)"', pres_rels_text)]
    new_rid = f"rId{max(rids) + 1 if rids else 1}"

    rel_entry = (
        f'<Relationship Id="{new_rid}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
        f'Target="slides/slide{target_slide_num}.xml"/>'
    )
    pres_rels_text = pres_rels_text.replace("</Relationships>", f"  {rel_entry}\n</Relationships>")
    pres_rels_file.write_text(pres_rels_text, encoding="utf-8")

    # Register in ppt/presentation.xml (<p:sldIdLst>)
    pres_file = ppt_dir / "presentation.xml"
    pres_text = pres_file.read_text(encoding="utf-8")

    slide_ids = [int(m) for m in re.findall(r'<p:sldId\s+[^>]*id="(\d+)"', pres_text)]
    new_slide_id = max(slide_ids) + 1 if slide_ids else 256

    sld_entry = f'<p:sldId id="{new_slide_id}" r:id="{new_rid}"/>'
    match = re.search(r"</p:sldIdLst>", pres_text)
    if match:
        pres_text = pres_text[: match.start()] + f"  {sld_entry}\n" + pres_text[match.start() :]
        pres_file.write_text(pres_text, encoding="utf-8")

    print(f"[add_slide.py] Successfully created slide{target_slide_num}.xml (Id: {new_slide_id}, rId: {new_rid})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Duplicate a slide layout inside an unpacked PPTX directory.")
    parser.add_argument("unpacked_dir", type=Path, help="Root path of unpacked PPTX directory")
    parser.add_argument("--from-slide", type=int, required=True, help="Source slide number to clone")
    parser.add_argument("--to-slide", type=int, required=True, help="New target slide number")
    args = parser.parse_args()

    duplicate_slide(args.unpacked_dir.resolve(), args.from_slide, args.to_slide)
    return 0


if __name__ == "__main__":
    sys.exit(main())
