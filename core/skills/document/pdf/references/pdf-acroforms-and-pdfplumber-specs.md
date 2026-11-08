# PDF AcroForms, pdfplumber & Form Extraction Specifications (2026)

## 1. Overview & Tooling Architecture

Automated PDF document processing enforces a deterministic tripartite extraction architecture:

```
                    Input PDF Document
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
     Interactive Form?   Native Text?   Scanned Raster?
            │               │               │
     pypdf AcroForm     pdfplumber     Tesseract OCR
    get_fields() API    Cell Extractor  Confidence Gate
            │               │               │
            └───────────────┼───────────────┘
                            ▼
              Document Manifest & Validation
               (document-manifest.json)
```

## 2. AcroForm Discovery & Population Invariants

1. **Discovery API**:
   Use `pypdf.PdfReader.get_fields()`. Never parse raw PDF dictionary syntax with ad-hoc regex.
2. **Field Classification**:
   Distinguish text fields (`/Tx`), choice fields (`/Ch`), checkboxes (`/Btn`), and signature blocks (`/Sig`).
3. **Form Filling Semantics**:
   - Write using `PdfWriter.update_page_form_field_values()`.
   - Set `/NeedAppearances` flag to `true` in `/AcroForm` catalog to force visual rendering across diverse PDF viewers.
   - Flatten annotations when producing immutable archival PDF/A deliverables.

## 3. Tabular Data Extraction with `pdfplumber`

When parsing invoices, financial statements, and manifests:
- Extract bounding boxes using explicit horizontal and vertical line detection:
  ```python
  table_settings = {
      "vertical_strategy": "lines",
      "horizontal_strategy": "lines",
      "snap_tolerance": 3,
      "join_tolerance": 3,
  }
  tables = page.extract_tables(table_settings)
  ```
- Normalize column alignment, strip leading/trailing whitespace, and preserve multiline cell wraps.

## 4. Visual Verification Gate

Before committing generated PDFs:
1. Render pages to high-resolution PNGs: `pdftoppm -png -r 150 document.pdf page_preview`.
2. Inspect for visual defects, truncated table cells, text overflows, and missing font subsets.
3. Verify signature vector presence: $w \ge 100\text{px}, h \ge 50\text{px}$.
