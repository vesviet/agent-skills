#!/usr/bin/env python3
"""
PowerPoint Package Cleanup and Relationship Auditor (clean.py).

Scans unpacked PPTX archives, removing unreferenced media assets, orphaned
relationship targets, and dead slide definitions.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Set


def clean_presentation_package(unpacked_dir: Path) -> int:
    ppt_dir = unpacked_dir / "ppt"
    pres_file = ppt_dir / "presentation.xml"
    pres_rels_file = ppt_dir / "_rels" / "presentation.xml.rels"
    media_dir = ppt_dir / "media"

    if not pres_file.exists() or not pres_rels_file.exists():
        print(f"Error: Invalid unpacked PPTX structure in {unpacked_dir}", file=sys.stderr)
        return 1

    pres_text = pres_file.read_text(encoding="utf-8")
    pres_rels_text = pres_rels_file.read_text(encoding="utf-8")

    # Find all referenced rIds in presentation.xml
    referenced_rids = set(re.findall(r'<p:sldId\s+[^>]*r:id="([^"]+)"', pres_text))

    # Identify active slides
    active_slides: Set[str] = set()
    for match in re.finditer(r'<Relationship\s+Id="([^"]+)"\s+[^>]*Target="slides/([^"]+)"', pres_rels_text):
        rid, target = match.group(1), match.group(2)
        if rid in referenced_rids:
            active_slides.add(target)

    # Prune orphaned slide files
    slides_dir = ppt_dir / "slides"
    pruned_slides = 0
    if slides_dir.exists():
        for slide_file in slides_dir.glob("slide*.xml"):
            if slide_file.name not in active_slides:
                slide_file.unlink()
                rels_file = slides_dir / "_rels" / f"{slide_file.name}.rels"
                if rels_file.exists():
                    rels_file.unlink()
                pruned_slides += 1

    # Prune unreferenced media files
    pruned_media = 0
    if media_dir.exists():
        all_rels_text = ""
        for rel_file in unpacked_dir.glob("**/*.rels"):
            all_rels_text += rel_file.read_text(encoding="utf-8", errors="ignore")

        for media_file in media_dir.iterdir():
            if media_file.name not in all_rels_text:
                media_file.unlink()
                pruned_media += 1

    print("=" * 60)
    print("PPTX PACKAGE CLEANUP AUDIT")
    print("=" * 60)
    print(f"Active slides preserved : {len(active_slides)}")
    print(f"Orphaned slides pruned  : {pruned_slides}")
    print(f"Unused media pruned     : {pruned_media}")
    print("🎉 Package cleanup complete.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune orphaned slides and media in unpacked PPTX.")
    parser.add_argument("unpacked_dir", type=Path, help="Root path of unpacked PPTX directory")
    args = parser.parse_args()

    return clean_presentation_package(args.unpacked_dir.resolve())


if __name__ == "__main__":
    sys.exit(main())
