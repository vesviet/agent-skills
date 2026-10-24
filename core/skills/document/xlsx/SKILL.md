---
name: xlsx
description: "Use when creating, analyzing, or modifying Microsoft Excel (.xlsx/.xlsm) workbooks, enforcing the Zero Formula Error invariant via recalc.py, dynamic formula injection, two-pass model reading, and openpyxl streaming."
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests, execute_command]
---

# xlsx

## Core Rules

1. **Zero Formula Errors Invariant:** Never deliver a spreadsheet where automated recalculation yields `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`, `#NULL!`, or `#NUM!`. Always run `recalc.py` to verify formula validity.
2. **Dynamic Formula Injection Law:** Always write dynamic formula expressions (`=SUM(C2:C50)`, `=XLOOKUP(...)`, `=IFERROR(...)`). Never hardcode calculated totals or summary aggregates as raw numbers.
3. **Two-Pass Reading Strategy:** When reading existing workbooks with `openpyxl`, perform two passes:
   - Pass 1: `openpyxl.load_workbook(path, data_only=False)` to inspect formula expressions and calculation lineage.
   - Pass 2: `openpyxl.load_workbook(path, data_only=True)` to inspect cached evaluation values.
4. **Memory-Safe Streaming at Scale:** For workbooks exceeding 10,000 rows, use `openpyxl` with `write_only=True` or `read_only=True` to prevent process out-of-memory (OOM) crashes.
5. **External Link Guard:** Inspect workbooks for external workbook links (`[External.xlsx]`) before recalculating. If external links are at risk, warn the user and do not strip them unless `--force` is specified.

## Suggested Process

1. **Architecture & Schema Planning:** Define sheet names, header columns, data types, and explicit calculation flows.
2. **Workbook Construction:** Build the workbook using Python `openpyxl`. Apply explicit number formatting (`#,##0.00`, `YYYY-MM-DD`, `0.0%`).
3. **Formula Injection:** Write uppercase formulas with exact coordinate bounds. Ensure header frozen panes are set (`ws.freeze_panes = 'A2'`).
4. **Formula Recalculation:** Execute `python3 recalc.py target.xlsx` to force recalculation via headless LibreOffice and audit error states.
5. **Validation & Handoff:** Ensure zero formula errors are reported, verify summary totals against database ground truth, and emit `document-manifest.json`.

## Checklist

- [ ] All formulas are written dynamically; zero hardcoded summary totals exist.
- [ ] Formula names and functions use standard Excel uppercase syntax.
- [ ] `recalc.py` executes cleanly with 0 formula errors found.
- [ ] Header rows have frozen panes enabled and distinct background fill styling.
- [ ] Numbers, currencies, and dates have explicit cell formatting applied.
- [ ] Large dataset exports (>10,000 rows) use memory-safe streaming mode.

## Related Skills

- **analyze-data**: Performs quantitative data modeling before export into Excel models.
- **build-data-pipeline**: Ingests database records into clean analytical spreadsheets.
- **query-analytical-engine**: Queries data lakehouse engines to populate analytical workbooks.

## Output Contracts

When completing workbook delivery, emit:
- **Document Manifest:** `core/contracts/schemas/document-manifest.json`
- **Data Analysis Report:** `core/contracts/schemas/data-analysis-report.json`
