# Field Router — Quick Start Guide

## What You Now Have

Two files that work together to scope Power BI page fields:

| File | Purpose |
|------|---------|
| **pbi_inspect.py** | CLI tool for analyzing Power BI `.pbix` files (no browser, no dependencies except pandas for export) |
| **app.py** | Flask web server providing a browser UI on top of pbi_inspect.py |
| **requirements.txt** | Install dependencies with: `pip install -r requirements.txt` |

## Installation (One-time)

```bash
# Install dependencies
pip install -r requirements.txt

# Or if you have uv:
uv pip install --system -r requirements.txt
```

## Getting Started

### Option 1: CLI (Command Line)

```bash
# List all pages in a report
python pbi_inspect.py "C:\Reports\sales.pbix" --list-pages

# Show fields on page "Dashboard" (by name)
python pbi_inspect.py "C:\Reports\sales.pbix" --page "Dashboard"

# Show fields on page 0 (by index)
python pbi_inspect.py "C:\Reports\sales.pbix" --page 0

# Scope "Dashboard" from old report against new report
python pbi_inspect.py "C:\Reports\old_sales.pbix" --page "Dashboard" \
  --scope "C:\Reports\new_sales.pbix" --out mapping_results

# Outputs: mapping_results.csv and mapping_results.xlsx
```

### Option 2: Web Interface (Browser)

```bash
# Start the server
python app.py

# Open http://127.0.0.1:5000 in your browser
```

Then:
1. Upload old `.pbix` and new `.pbix`
2. Select the page you want to scope
3. View results in an interactive table
4. Download as CSV or Excel

## What Each Tool Does

### pbi_inspect.py

**CLI Usage:**
```bash
python pbi_inspect.py FILE [OPTIONS]

OPTIONS:
  --list-pages              List all pages in FILE
  --page NAME_OR_INDEX      Show fields on a page (by name or 0-based index)
  --model                   Dump full data model (requires pbixray)
  --scope NEW_FILE          Scope the --page against NEW_FILE
  --out BASENAME            Export results to BASENAME.csv and BASENAME.xlsx
```

**As a Library:**
```python
import pbi_inspect as pbi

# Load a report
layout = pbi.load_layout("report.pbix")

# Get pages
pages = pbi.list_pages(layout)
for p in pages:
    print(f"Page {p['index']}: {p['displayName']}")

# Get fields on a page
fields = pbi.fields_on_page(layout, page_index=0)

# Match fields from old page to new report
rows, old_style, new_style, warning = pbi.scope_page(
    "old.pbix", old_layout, 0,
    "new.pbix", new_layout
)
```

### app.py

**Web Server:**
```bash
python app.py
# Server runs on http://127.0.0.1:5000 (debug mode)
```

The web interface is a single-page application with:
- Step 1: Upload two reports
- Step 2: Select a page from the old report
- Step 3: View interactive results + export

## Field Matching Precedence

Results show match status based on field name similarity:

| Status | Meaning |
|--------|---------|
| **Exact match** | Same table AND field name → 100% confidence |
| **Field name matches (different table)** | Same field name, different table → 90% confidence |
| **Likely match** | Similar names (≥82% match) → 82–99% confidence |
| **Possible match** | Somewhat similar (60–82%) → 60–81% confidence |
| **No match found** | Very different or new field → 0% confidence |

Comparison is **case-insensitive** and ignores spaces, underscores, hyphens.

## Example Workflows

### Scenario 1: Migrate one dashboard

```bash
# See what pages are in the old report
python pbi_inspect.py old_report.pbix --list-pages

# Export the "Sales Dashboard" page mapping
python pbi_inspect.py old_report.pbix --page "Sales Dashboard" \
  --scope new_report.pbix --out sales_mapping

# Open sales_mapping.xlsx in Excel, review and manually rebuild measures
```

### Scenario 2: Bulk analysis (all pages)

```bash
# Get overview of all pages
python pbi_inspect.py old_report.pbix --list-pages

# For each page, run scope and save results
for page in "Dashboard", "Details", "Trends"; do
  python pbi_inspect.py old_report.pbix --page "$page" \
    --scope new_report.pbix --out "mapping_${page}"
done
```

### Scenario 3: Live model inspection

```bash
# Dump the full embedded data model
python pbi_inspect.py report.pbix --model

# Shows:
# - All tables
# - All columns (schema)
# - All DAX measures (with expressions)
# - All calculated columns
# - All relationships
```

## Troubleshooting

### "File not found"
Make sure the path to the `.pbix` is correct. Use absolute paths or relative paths from the current directory.

### "Report/Layout entry not found"
The file is not a valid `.pbix`, or it's corrupted. Try opening it in Power BI Desktop first.

### "Page not found"
Try listing pages with `--list-pages` first. Page names are case-sensitive (but the tool does fuzzy matching). If a page name looks truncated in Power BI, it's likely a hidden page — check the `(hidden)` flag in the page list.

### "pbixray isn't installed"
Run `pip install pbixray`

### Flask server won't start
Make sure port 5000 is not in use. Change it in `app.py` line: `app.run(debug=True, port=5001)`

## Data Privacy

- **CLI**: Reads files from disk; nothing leaves your computer
- **Web Server**: Local only (http://127.0.0.1:5000); files stored in system temp directory; deleted on server restart or manually

No data is sent to external servers.

## Next Steps

1. **Install**: `pip install -r requirements.txt`
2. **Test CLI**: `python pbi_inspect.py yourfile.pbix --list-pages`
3. **Test Web**: `python app.py` → open http://127.0.0.1:5000
4. **Run scoping**: Either CLI or web, depending on your preference

## Support

Refer to [README.md](README.md) for full documentation and technical details.
