# Field Router — Power BI Page Scoping Tool

A Python-based tool to scope Power BI page fields across old and new reports. Includes both a CLI and a web interface.

## What It Does

- **List pages** in a Power BI `.pbix` file
- **Extract fields** (columns, measures, hierarchy levels) used on a specific page
- **Compare reports** — match fields from an old report page to a new report's inventory
- **Export results** as CSV or Excel with confidence scores and match status
- **Web interface** for interactive workflows

## Installation

### Prerequisites
- Python 3.7+ (tested with 3.14)
- pip or uv package manager

### Setup

Install required packages:

```bash
pip install flask pbixray pandas openpyxl
```

Or with uv:
```bash
uv pip install flask pbixray pandas openpyxl
```

## Usage

### CLI Mode

#### List all pages in a report
```bash
python pbi_inspect.py report.pbix --list-pages
```

#### Show fields used on a specific page
```bash
python pbi_inspect.py report.pbix --page "Sales Overview"
python pbi_inspect.py report.pbix --page 0   # or by index
```

#### Dump the full data model
```bash
python pbi_inspect.py report.pbix --model
```

#### Scope a page from one report against another
```bash
python pbi_inspect.py old.pbix --page "Dashboard" --scope new.pbix --out mapping
```

This creates:
- `mapping.csv` — tab-separated results
- `mapping.xlsx` — Excel workbook with same data

### Web Interface

Start the Flask server:
```bash
python app.py
```

Then open: **http://127.0.0.1:5000**

The browser interface provides:
1. **Upload** — Select old and new `.pbix` files
2. **Select Page** — Choose which page from the old report to scope
3. **Route Fields** — View matching results, search/filter, and export

## Features

### Field Matching Logic

Fields are matched using this precedence:

1. **Exact match** — Same table and field name
2. **Field name matches (different table)** — Same field name, different table
3. **Likely match** — Similarity score ≥ 0.82
4. **Possible match** — Similarity score 0.60–0.82
5. **No match found** — Similarity < 0.60

Comparison ignores case, spaces, underscores, and hyphens.

### Naming Convention Detection

Detects and reports naming convention styles:
- `snake_case`
- `camelCase`
- `PascalCase`
- `Title Case`
- `space separated`
- `other`

Flags rows where old and new field naming styles differ.

### Data Model Support

- **Import-mode reports** — Full access to embedded data model (tables, columns, measures, DAX)
- **Live connection reports** — Falls back to fields used in visuals (requires connection to load model)

## Architecture

### `pbi_inspect.py`
Standalone CLI module with no Flask dependency. Exports these key functions:

- `load_layout()` — Load report/layout JSON from `.pbix`
- `list_pages()` — List all pages with hidden-page flag
- `fields_on_page()` — Extract fields used on a page
- `fields_across_report()` — Extract all fields used anywhere
- `scope_page()` — Match fields between two reports
- `build_new_inventory()` — Merge data model + visual fields from new report
- `dump_model()` — Print full data model via pbixray

### `app.py`
Flask web server that reuses all functions from `pbi_inspect.py`.

**Routes:**
- `GET /` — Single-page HTML UI
- `POST /api/analyze` — Upload two reports, return page list and field count
- `POST /api/scope` — Run field matching for a selected page
- `GET /api/export/<session_id>.<csv|xlsx>` — Download export

**Sessions** are stored in-memory keyed by UUID (good enough for single-user local use).

## Technical Details

### .pbix File Format

A `.pbix` is a ZIP archive containing:

- **Report/Layout** — JSON defining pages and visuals; visuals reference fields via `{ Column: {Property: "..."}}`  or `{ Measure: {...} }` structures; config fields may contain nested JSON-encoded strings
- **DataModel** — VertiPaq compressed format (parsed by pbixray)

### Hidden Pages

Power BI supports hidden pages (tooltip, drillthrough targets, or author-hidden pages).  These:
- Exist in Report/Layout
- Render as small icon-only tabs in Desktop
- Are listed and selectable in this tool
- May have truncated names in the UI (the issue this solves)

## Known Limitations

- Sessions are in-memory and lost on server restart
- Single-user local-only (no concurrent multi-user session layer)
- Live-connection reports need a working Analysis Services connection to read the full model
- File upload size limited by Flask default (16 MB — configurable in `app.py`)

## Troubleshooting

### "Report/Layout entry not found"
File is not a valid `.pbix` or is corrupted. Check that it opens in Power BI Desktop.

### "Could not read an embedded data model"
Live-connection or thin reports don't have an embedded model. The tool falls back to fields used in visuals.

### "pbixray isn't installed"
Run: `pip install pbixray`

### Page name matching not working
Try:
- Exact capitalization match
- Page index (0-based) instead of name
- Copy/paste from `--list-pages` output to avoid whitespace issues

## Development

To test the CLI on a `.pbix` file:

```bash
python pbi_inspect.py /path/to/report.pbix --list-pages
python pbi_inspect.py /path/to/report.pbix --page 0
```

To test the web server:

```bash
python app.py
# Open http://127.0.0.1:5000 in browser
```

## License

Provided as-is for local use.
