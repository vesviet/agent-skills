---
name: pdf
description: "Use when reading, extracting, creating, or modifying PDF documents, parsing text and tables via pdfplumber/pypdf, discovering and filling interactive AcroForms, performing OCR, or verifying digital signatures."
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# pdf

## Core Rules

1. **Deterministic AcroForm Discovery & Population:** Inspect fillable PDF forms using `pypdf` (`reader.get_fields()`). Programmatically populate form widgets with strict field-name mapping before attempting visual raster stamping.
2. **Tripartite PDF Extraction:** Combine `pypdf` for fast text/metadata extraction, `pdfplumber` for tabular cell coordinate extraction, and `tesseract`/OCR for scanned raster pages.
3. **Visual Layout Verification:** Never assume programmatic PDF generation rendered cleanly without visual checks. Convert pages to PNG via `pdftoppm -png -r 150 doc.pdf page` to inspect table border alignment, font clipping, and multi-page overflows.
4. **Signature & Bounding Box Integrity:** When processing proofs of delivery (ePOD) or legal contracts, verify signature vector presence ($w \ge 100\text{px}, h \ge 50\text{px}$) and timestamps. Never accept blank or 0-byte signature fields.
5. **Font Embedding & ASCII Dash Rule:** Embedded fonts must be subsetted. Hyphens must use standard ASCII (`-`, U+002D) rather than non-breaking hyphens (U+2011) which cause corrupted glyph rendering in headless PDF engines.

## Suggested Process

1. **Document Classification:** Determine if the PDF is text-native, scanned image, or interactive AcroForm.
2. **Interactive Form Processing:**
   - Run `check_fillable_fields.py` to list field names and types.
   - Author a JSON mapping payload matching form keys.
   - Run `fill_fillable_fields.py input.pdf values.json output.pdf`.
3. **Table & Text Extraction:** Use `pdfplumber` to extract tables into structured CSV/JSON, preserving table header hierarchies.
4. **Visual Quality Gate:** Render pages to high-resolution PNGs via `pdftoppm` and inspect for visual defects or clipping.
5. **Contract Manifest:** Emit `document-manifest.json` with page count, embedded font metrics, and SHA-256 checksums.

## Checklist

- [ ] Document type (native, scanned, or AcroForm) is identified before processing.
- [ ] All fillable form field keys are verified against `reader.get_fields()`.
- [ ] Tables are extracted with structural column boundaries intact.
- [ ] Rendered pages verified via `pdftoppm` show zero clipped text or overlapping frames.
- [ ] Signatures and verification stamps meet minimum dimensional and bounding requirements.
- [ ] Finished PDF includes embedded font subsets and valid PDF/A compliance metadata.

## Related Skills

- **write-documentation**: Author technical specifications converted to executive PDF manuals.
- **release-notes**: Compiles release artifacts into customer-facing PDF documentation.
- **docx**: Converts source Word manuscripts into finalized PDF publications.

## Output Contracts

When completing PDF generation or form filling, emit:
- **Document Manifest:** `core/contracts/schemas/document-manifest.json`
