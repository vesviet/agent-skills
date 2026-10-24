---
name: pptx
description: "Use when creating, editing, or inspecting PowerPoint (.pptx/.potx) presentations, authoring decks via pptxgenjs, generating visual slide thumbnail grids via thumbnail.py, duplicating layouts via add_slide.py, or pruning dead relationships via clean.py."
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# pptx

## Core Rules

1. **Widescreen 16:9 Aspect Ratio Mandate:** All presentation decks must default to 16:9 widescreen ($13.333 \times 7.5\text{ in}$ / $12192000 \times 6858000\text{ EMUs}$). Standard 4:3 is permitted only upon explicit user instruction.
2. **Visual Thumbnail Grid Review:** Never deliver a presentation deck without rendering visual thumbnails. Run `thumbnail.py deck.pptx` to generate a composite grid image and inspect layout balance, contrast, and alignment.
3. **Package Bookkeeping on XML Manipulation:** When modifying unpacked `.pptx` archives:
   - Use `add_slide.py` to clone layouts, ensuring new slides are registered in `ppt/presentation.xml` (`<p:sldIdLst>`), `ppt/_rels/presentation.xml.rels`, and `[Content_Types].xml`.
   - Use `clean.py` to purge unreferenced media files and orphaned relationship files.
4. **Anti-Slop Design Heuristics:** Forbid cliché AI slide layouts: no uniform card grids, no purple gradients, no tiny low-contrast captions ($< 12\text{pt}$), and enforce maximum 40 words per content slide.
5. **Safe Color & Typography Systems:** Ground typography in distinct paired fonts (e.g. Space Grotesk + Inter) and high-contrast color palettes (APCA $L_c \ge 75$ for body text).

## Suggested Process

1. **Storyline & Deck Architecture:** Define slide titles, visual hierarchy, and structural sequence (Title, Context, Data, Architecture, Summary).
2. **Deck Generation:**
   - For programmatic generation, use Node.js `pptxgenjs` to define slides, shapes, text boxes, and tables.
   - For template editing, unpack `.pptx`, duplicate slide layouts using `add_slide.py`, update XML content, and run `clean.py`.
3. **Visual Grid Inspection:** Run `python3 thumbnail.py deck.pptx --grid` to render a multi-slide composite thumbnail image.
4. **Design Polish:** Check typography sizes, margin consistency ($0.8\text{ in}$ padding), and visual whitespace.
5. **Validation & Delivery:** Emit `document-manifest.json` containing slide count, font metrics, and asset checksums.

## Checklist

- [ ] Presentation is configured with 16:9 widescreen aspect ratio.
- [ ] Visual thumbnail grid generated via `thumbnail.py` confirms clean visual layout.
- [ ] No unreferenced media files or broken relationship IDs remain (verified via `clean.py`).
- [ ] High contrast ratios (APCA $L_c \ge 75$) are maintained across all slide backgrounds.
- [ ] Slide text is concise ($\le 40$ words per body slide) with clear visual hierarchy.
- [ ] Final package passes OOXML validation and opens without repair warnings.

## Related Skills

- **design-system-engineering**: Applies color tokens and typography scale rules to presentation slides.
- **frontend-micro-polish**: Enforces optical alignment and spacing consistency on visual elements.
- **design-ux-flow**: Provides layout wireframes for slide architecture and diagram design.

## Output Contracts

When completing presentation deck delivery, emit:
- **Document Manifest:** `core/contracts/schemas/document-manifest.json`
- **UI Component Spec:** `core/contracts/schemas/ui-component-spec.json`
