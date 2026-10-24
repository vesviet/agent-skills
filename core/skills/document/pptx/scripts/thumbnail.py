#!/usr/bin/env python3
"""
PowerPoint Visual Slide Thumbnail Grid Generator (thumbnail.py).

Renders presentation slides to individual PNGs and stitches them into a labeled
visual contact sheet (grid.png) for automated visual QA and design review.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None


def find_converter() -> Optional[str]:
    for candidate in ["libreoffice", "soffice"]:
        if shutil.which(candidate):
            return candidate
    return None


def convert_pptx_to_images(pptx_path: Path, output_dir: Path) -> List[Path]:
    converter = find_converter()
    if not converter:
        raise RuntimeError("LibreOffice/soffice is required to convert PPTX to images.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        # Convert PPTX to PDF
        subprocess.run(
            [converter, "--headless", "--convert-to", "pdf", "--outdir", str(tmp_path), str(pptx_path)],
            check=True,
            capture_output=True,
        )
        pdf_file = tmp_path / f"{pptx_path.stem}.pdf"
        if not pdf_file.exists():
            raise RuntimeError("PDF conversion failed.")

        # Convert PDF pages to PNG using pdftoppm
        prefix = str(output_dir / "slide")
        subprocess.run(
            ["pdftoppm", "-png", "-r", "150", str(pdf_file), prefix],
            check=True,
            capture_output=True,
        )

    return sorted(output_dir.glob("slide-*.png"))


def create_thumbnail_grid(image_paths: List[Path], output_grid: Path, cols: int = 4) -> None:
    if Image is None or not image_paths:
        return

    images = [Image.open(p) for p in image_paths]
    thumb_w, thumb_h = 320, 180
    thumbs = [img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS) for img in images]

    rows = (len(thumbs) + cols - 1) // cols
    padding = 20
    label_h = 30
    cell_w = thumb_w + padding
    cell_h = thumb_h + label_h + padding

    grid_w = cols * cell_w + padding
    grid_h = rows * cell_h + padding

    grid_img = Image.new("RGB", (grid_w, grid_h), color=(245, 245, 247))
    draw = ImageDraw.Draw(grid_img)

    for idx, thumb in enumerate(thumbs):
        r = idx // cols
        c = idx % cols
        x = padding + c * cell_w
        y = padding + r * cell_h

        grid_img.paste(thumb, (x, y))
        draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline=(200, 200, 205), width=2)
        draw.text((x + 10, y + thumb_h + 8), f"Slide {idx + 1}", fill=(40, 40, 45))

    grid_img.save(output_grid)
    print(f"[thumbnail.py] Saved slide grid: {output_grid}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate visual slide thumbnails and composite grid from PPTX.")
    parser.add_argument("pptx", type=Path, help="Target .pptx presentation")
    parser.add_argument("--out", type=Path, default=Path("thumbnails"), help="Output directory for thumbnails")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns in visual grid (default: 4)")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    images = convert_pptx_to_images(args.pptx.resolve(), args.out)
    print(f"[thumbnail.py] Rendered {len(images)} slides into {args.out}")

    grid_path = args.out / "grid.png"
    create_thumbnail_grid(images, grid_path, cols=args.cols)
    return 0


if __name__ == "__main__":
    sys.exit(main())
