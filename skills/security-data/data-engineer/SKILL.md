---
name: data-engineer
description: Collect, clean, compare, and report on tabular data from Excel and CSV sources. Use when a task involves reading spreadsheet data, diffing datasets, or generating formatted Excel reports for analysis or stakeholder delivery.
---

# Data Engineer

Use this skill when the task involves reading spreadsheet data, comparing datasets for differences, or producing formatted Excel reports.

## When to Use

- importing data from Excel or CSV into a clean queryable format
- comparing two datasets to find added, removed, or changed rows
- generating a formatted Excel report for stakeholders or audit
- building a read-compare-report pipeline from raw spreadsheet inputs
- any task described as "comprade", "so sánh data", "báo cáo", or "check khác nhau"

## Core Rules

- read all source data as string first, then convert types explicitly after cleaning
- normalize column names and whitespace before any comparison
- use UTF-8-SIG encoding for all output to preserve Vietnamese and special characters
- log row counts before and after every transformation for traceability
- timestamp all report filenames so outputs never silently overwrite
- do not modify source files; treat inputs as read-only
- validate import results against source before proceeding to compare or report

## First Questions To Answer

1. Where are the source files and what format are they in?
2. Which sheet or sheets should be read?
3. What column or columns form the unique key for matching rows?
4. Which columns should be compared or included in the report?
5. What output format does the user need: summary, detailed diff, or formatted Excel?

## Suggested Process

### Step 1: Set Up The Working Directory

Create the standard directory layout if it does not exist:

```
<project>/data-engineer/
├── input/        ← source Excel and CSV files
├── store/        ← cleaned intermediate data as CSV
├── reports/      ← generated Excel reports
└── scripts/      ← reusable Python scripts
```

Confirm Python 3 and required packages are available. Install if missing:

```bash
pip3 install --user openpyxl pandas xlsxwriter
```

### Step 2: Import Source Data

Read the Excel or CSV file into a pandas DataFrame:

- use `dtype=str` to prevent silent type coercion
- strip whitespace from column names and normalize to lowercase with underscores
- drop rows that are completely empty
- save the cleaned result to `store/` as CSV with `encoding="utf-8-sig"`

Print a summary: column names, shape, and a five-row preview.

### Step 3: Compare Datasets (When Applicable)

When the task requires finding differences between two datasets:

- merge on the identified key columns with `how="outer"` and `indicator=True`
- classify rows as only-in-A, only-in-B, or matched
- for matched rows, iterate compare columns and record cell-level changes
- handle NaN by filling with empty string before comparison
- print a summary: counts for added, removed, matched, and changed cells

### Step 4: Generate The Report

Create a formatted Excel workbook using xlsxwriter:

- use a professional header style: bold white text on dark blue background with borders
- auto-fit column widths with a maximum of 50 characters
- freeze the header row on every sheet
- enable auto-filter on data sheets
- use VND currency format `#,##0 ₫` where applicable
- highlight changed cells in yellow, errors in red, passed items in green
- include a Summary sheet with metadata: source files, row counts, timestamp

Save the report to `reports/` with a timestamped filename.

### Step 5: Verify And Hand Off

Confirm:

- row counts match expectations
- Vietnamese characters render correctly in the output Excel
- all requested sheets and columns are present
- report opens without errors in Excel

## Output Format

When presenting results, include:

- source files used
- row counts at each stage
- summary of differences found (if comparing)
- path to the generated report
- any data quality issues discovered

## Comparison Modes

| Mode | When to use | What it produces |
|------|-------------|------------------|
| Row diff | finding added or removed records | list of keys only in one dataset |
| Cell diff | finding changed values in matching records | key, column, old value, new value |
| Summary | quick overview | counts only |
| Full audit | detailed stakeholder report | all of the above in a formatted Excel |

## Report Formatting Standards

| Element | Standard |
|---------|----------|
| Header | bold, white on dark blue, centered, bordered |
| Data cells | thin borders, text wrap, vertical center |
| Numbers | `#,##0` for integers, `#,##0.00` for decimals |
| Currency | `#,##0 ₫` for VND |
| Changed cells | yellow background `#FFF2CC` |
| Error cells | red background `#FFE0E0` |
| OK cells | green background `#E2EFDA` |
| Column width | auto-fit with max 50 chars |
| Freeze | always freeze header row |
| Filter | always enable auto-filter |

## Common Pitfalls

- comparing floats read as strings leads to false positives: normalize numeric columns before diff
- Excel date serial numbers require explicit conversion with a known epoch
- large files over 100 MB should use chunked reading
- old `.xls` format requires the `xlrd` package instead of `openpyxl`
- files open in Excel on Windows will cause permission errors during read

## Checklist

- [ ] working directory structure created
- [ ] required Python packages installed
- [ ] source files placed in input directory
- [ ] import script reads data correctly with matching row counts
- [ ] column names cleaned and types converted
- [ ] cleaned data saved to store directory
- [ ] comparison uses correct key columns (when applicable)
- [ ] NaN and empty values handled consistently
- [ ] report has professional formatting with headers, borders, and filters
- [ ] report filename includes timestamp
- [ ] Vietnamese characters display correctly in output
- [ ] all scripts run successfully
- [ ] results verified against source data

## Related Skills

- **database-maintenance**: Use when cleaned data needs to move into a production database
- **security-audit**: Review data handling for sensitive or PII content
- **write-documentation**: Document data pipelines and report specifications
- **review-code**: Review data processing scripts for correctness
- **commit-code**: Commit finalized scripts to version control
