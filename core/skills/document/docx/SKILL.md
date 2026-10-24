---
name: docx
description: "Use when creating, editing, inspecting, or formatting Microsoft Word (.docx) documents, enforcing DXA table column width invariants, raw XML unzipping workflows, or reading documents via pandoc markdown extraction."
allowed-tools: [read_file, write_file, edit_file, create_file, search_code]
---

# docx

## Core Rules

1. **DXA Dual-Width Invariant for Tables:** When generating Word documents using `docx-js` or OOXML, every table must declare `columnWidths` on the table element AND matching `width` on every individual `TableCell` using `WidthType.DXA` ($1\text{ in} = 1440\text{ DXA}$, $1\text{ pt} = 20\text{ DXA}$). Never use percentage widths, as they collapse in Google Docs and web office viewers.
2. **Template Preservation via XML Unzipping:** To modify existing styled documents or corporate templates, unzip the `.docx` archive, perform surgical edits in `word/document.xml` or `word/styles.xml`, and re-zip. Never attempt full-document regeneration with `docx-js` if preserving corporate typography and headers.
3. **Dual-Pass Reading:** When extracting or reviewing document content, convert `.docx` to Markdown via `pandoc -f docx -t markdown` for structural reading. For comment threads and tracked revisions, inspect `word/comments.xml` and `word/document.xml` (`<w:ins>`, `<w:del>`) directly.
4. **Standard Page Geometry:** Enforce A4 ($11906 \times 16838\text{ DXA}$) or US Letter ($12240 \times 15840\text{ DXA}$) with explicit $1\text{ in}$ ($1440\text{ DXA}$) margins on all section properties (`<w:sectPr>`).
5. **Contract Manifest Verification:** After creating or modifying a document, emit a valid `document-manifest.json` capturing file checksums, page estimates, and font configurations.

## Suggested Process

1. **Intake & Discovery:** Determine whether the task requires creating a new document from scratch or modifying an existing `.docx` template.
2. **Reading & Inspection:** Convert existing files using `pandoc -f docx -t markdown input.docx -o content.md` to review prose structure.
3. **Generation / Surgical Modification:**
   - For scratch generation, author a Node.js script using `docx` (`Packer.toBuffer`).
   - For template editing, unpack via `unzip input.docx -d unpacked/`, modify `unpacked/word/document.xml`, verify XML well-formedness, and repack via `zip -r output.docx *`.
4. **Table Formatting:** Calculate column widths in DXA (e.g. 3-column table on US Letter: $4680, 2340, 2340\text{ DXA}$ summing to $9360\text{ DXA}$ printable width). Apply both table-level and cell-level widths.
5. **Validation & Delivery:** Inspect rendering via LibreOffice conversion to PDF, verify layout fidelity, and emit `document-manifest.json`.

## Checklist

- [ ] Page size and margins are explicitly defined in DXA units ($1440\text{ DXA} = 1\text{ inch}$).
- [ ] Every table declares matching `columnWidths` at table-level and `width` on all `TableCell` elements.
- [ ] Total column widths sum up exactly to the body printable width.
- [ ] Heading styles follow strict hierarchical levels (`Heading 1`, `Heading 2`, `Heading 3`).
- [ ] Existing template track changes and comments are preserved or explicitly accepted.
- [ ] Final document is verified via LibreOffice PDF conversion and manifest is emitted.

## Related Skills

- **write-article**: Generates structured markdown prose converted into publication Word documents.
- **write-documentation**: Provides structured documentation frameworks for enterprise delivery.
- **pdf**: Converts finished Word documents into cryptographically signed PDF deliverables.

## Output Contracts

When completing document generation, emit the formal manifest:
- **Document Manifest:** `core/contracts/schemas/document-manifest.json`
