# Power BI Field Router - Deployment & Usage Guide

## Overview

The **Power BI Field Router** is a web-based tool that helps you route fields between Power BI reports. It analyzes your old and new Power BI reports, matches fields with confidence scores, and provides recommendations for field mapping.

**Status:** ✅ **Production Ready** (All core features operational)

---

## System Requirements

- **Python:** 3.14.4+ (uv-managed)
- **OS:** Windows 10/11
- **Memory:** 2GB minimum (4GB+ for large reports)
- **Disk Space:** 500MB free

---

## Installation

### 1. Verify Python Installation

```powershell
python3.14 --version
```

Should output: `Python 3.14.4`

### 2. Install Dependencies

```powershell
cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"
python3.14 -m pip install -r requirements.txt
```

**Required packages:**
- flask >= 2.3.0
- pandas >= 1.5.0
- openpyxl >= 3.10.0

### 3. (Optional) Install pbixray for DAX Extraction

When ready, install pbixray to enable DAX/Expression extraction:

```powershell
python3.14 -m pip install pbixray --break-system-packages
```

**Note:** This is optional. The tool works perfectly without pbixray and gracefully falls back to visual-only field detection.

---

## Starting the Tool

### Option A: PowerShell (Recommended)

```powershell
# Allow script execution (one-time setup)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run the startup script
.\START_TOOL.ps1
```

### Option B: Batch File

Double-click `START_TOOL.bat` in Windows Explorer.

### Option C: Manual

```powershell
cd "c:\Users\manishkumar.yadav\Downloads\Scoping Tool"
python3.14 app.py
```

---

## Access the Tool

Once the server is running, open your browser and go to:

**http://127.0.0.1:5000/**

You should see:
- Field Router title
- 3-step workflow indicator
- File upload sections for old and new reports

---

## Using the Tool

### Step 1: Upload Reports

1. Click **"Old report"** and select your old Power BI .pbix file
2. Click **"New report"** and select your new Power BI .pbix file
3. Click **"Analyze reports"** button

**What happens:**
- Files are parsed locally (nothing leaves your computer)
- Pages extracted and filtered (generic "Page 1" names removed)
- Fields detected from all visuals
- Warnings displayed if any optional features unavailable

### Step 2: Select Page

After analysis completes:
1. See list of pages from old report
2. Page names are clean (no "(hidden page)" suffix)
3. Select the page you want to route

**Available pages:** Only meaningful page names shown (generic placeholders filtered out)

### Step 3: Route Fields

For the selected page:
1. Table shows all fields from old page
2. Each field has:
   - **Status:** exact match / likely / possible / no match
   - **Confidence:** 0-100% match score
   - **New Field:** Recommended field from new report
   - **Notes:** Additional details
   - **DAX/Expression:** Formula/definition (if pbixray installed)
   - **Missing:** ⚠️ badge if field missing from new report entirely

### Step 4: Export Results

Click **"Export to CSV"** or **"Export to Excel"** to download:
- All field mappings
- Match status and confidence
- Recommended new field names
- Notes and warnings
- DAX expressions (if available)

Use exported file to:
- Share with team
- Track field mapping decisions
- Recreate measures in new report
- Document migration work

---

## Field Matching Algorithm

Matches are scored on 5 tiers:

| Status | Confidence | Meaning |
|--------|-----------|---------|
| **Exact** | 100% | Exact name match |
| **Likely** | 82-99% | Very similar name (Levenshtein similarity) |
| **Possible** | 60-81% | Similar name or partial match |
| **Possible** | 0-59% | Weak match - review carefully |
| **No match** | 0% | Field not found in new report |

---

## Features

✅ **Automatic Field Detection**
- Extracts fields from all visuals
- Handles new Power BI modular format
- Removes duplicate entries
- Filters generic placeholder pages

✅ **Smart Matching**
- 5-tier confidence scoring
- Detects naming style changes (snake_case → camelCase)
- Similarity scoring using Levenshtein distance
- Highlights completely missing fields

✅ **DAX Support** (Optional)
- Shows formulas for missing measures
- Helps recreate measures in new report
- Gracefully degrades if pbixray unavailable

✅ **Professional Export**
- CSV and Excel formats
- All metadata included
- Ready to share with team
- No data leaves your computer

---

## Troubleshooting

### "Analyze reports" button disabled

**Problem:** After uploading files, button still disabled

**Solution:** 
- Both files must be .pbix format
- Files must be valid Power BI reports
- Try uploading again

### No fields appearing

**Problem:** Table empty after selecting a page

**Possible causes:**
- Page has no visuals
- Page visuals don't reference any fields
- File format not recognized

**Solution:**
- Try different page
- Check .pbix file is real Power BI report

### Missing field warnings

**Problem:** Some fields show "⚠️ MISSING" badge

**Meaning:** These fields exist in old report but are completely absent from new report

**Action needed:**
- Manually recreate the measure/column in new report
- Use DAX expression (if available) to recreate logic
- See exported notes for guidance

### "⚠️ pbixray required" shown

**Problem:** DAX/Expression column shows warnings instead of formulas

**Meaning:** pbixray library not installed (optional feature)

**Solution:**
- Tool still works without pbixray (field matching intact)
- To enable DAX extraction, run:
  ```powershell
  python3.14 -m pip install pbixray --break-system-packages
  ```
- Restart the tool after installation

### Server won't start

**Problem:** "Port 5000 already in use"

**Solution:**
- Kill existing Python processes: `Get-Process python3.14 | Stop-Process -Force`
- Try different port (edit app.py line last line: `app.run(debug=True, port=5001)`)

---

## File Structure

```
Scoping Tool/
├── app.py                    # Flask web server
├── pbi_inspect.py           # Power BI analysis library
├── test_field_router.py     # Test suite
├── requirements.txt         # Python dependencies
├── START_TOOL.bat          # Windows batch starter
├── START_TOOL.ps1          # PowerShell starter
├── QUICKSTART.md           # Quick start guide
├── README.md               # Project overview
├── BUILD_SUMMARY.md        # Build/architecture details
├── TEST_RESULTS.md         # Test results
└── Field_Router_Guide.docx # Detailed user guide
```

---

## API Reference

### POST /api/analyze
Upload and analyze two Power BI reports

**Request:**
```
multipart/form-data
- old_file: File (.pbix)
- new_file: File (.pbix)
```

**Response:**
```json
{
  "session_id": "abc123",
  "pages": [
    {
      "name": "Dashboard",
      "displayName": "Dashboard",
      "index": 0,
      "hidden": false,
      "field_count": 42
    }
  ],
  "warnings": [
    "DAX/Expression extraction unavailable...",
    "Falling back to visual-only field detection..."
  ],
  "new_field_count": 156
}
```

### POST /api/scope
Get field routing for a specific page

**Request:**
```json
{
  "session_id": "abc123",
  "page_index": 0
}
```

**Response:**
```json
[
  {
    "old_table": "Sales",
    "old_field": "TotalRevenue",
    "kind": "Measure",
    "status": "exact",
    "new_table": "Sales",
    "new_field": "TotalRevenue",
    "confidence": 1.0,
    "note": "Exact match",
    "missing_from_new_report": false,
    "dax_expression": "SUM(Sales[Amount])"
  }
]
```

### GET /api/export/<session_id>.<fmt>
Export field routing results

**Parameters:**
- `session_id`: Session ID from /api/analyze
- `fmt`: Format (csv or xlsx)

**Returns:** File download

---

## Advanced Usage

### Batch Processing Multiple Pages

1. Upload reports once
2. Select different pages and export each
3. Combine results in Excel using session_id

### Custom Field Matching

Edit `pbi_inspect.py` line ~200 to adjust:
- Confidence thresholds
- Naming style detection
- Similarity scoring weights

### Integration with Workflows

Export to CSV and import into:
- Excel for manual review
- SQL database for tracking
- Power BI for visualization
- SharePoint for team collaboration

---

## Support & Feedback

For issues or feature requests:
1. Check TEST_RESULTS.md for known test cases
2. Review BUILD_SUMMARY.md for architecture
3. Consult pbi_inspect.py docstrings for function details

---

## Version Info

- **Tool Version:** 2.0
- **Python:** 3.14.4+
- **Flask:** 2.3.0+
- **Status:** Production Ready ✅
- **Last Updated:** 2026-07-28

---

**Ready to use!** Start with `START_TOOL.ps1` or `START_TOOL.bat` and begin routing your fields.
