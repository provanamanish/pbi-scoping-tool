"""
pbi_inspect.py

Inspect a Power BI .pbix file from Python:
  - list every page (report tab) in the file
  - list every column / measure / hierarchy level used to build a given page
  - (optional) dump the full data model — every table, column, and measure,
    including DAX expressions — using the pbixray library

Two different techniques are combined here, because they read two different
parts of the .pbix:

  1. Report/Layout (page + visual definitions) is just JSON inside the zip,
     so it's parsed directly with the standard `zipfile` + `json` modules.
     This is what tells you which pages exist and which fields each page's
     visuals reference.

  2. The embedded data model (DataModel entry) is a compressed, proprietary
     VertiPaq format — not plain JSON. Reading it requires a real parser, so
     this script uses the `pbixray` library (pip install pbixray) which reads
     that format directly, without needing Power BI or Analysis Services
     installed. This is what gives you the *complete* list of tables/columns/
     measures that exist in the model, even ones never placed on a visual.

Install:
    pip install pbixray

Usage:
    python pbi_inspect.py report.pbix --list-pages
    python pbi_inspect.py report.pbix --page "Sales Overview"
    python pbi_inspect.py report.pbix --page 0
    python pbi_inspect.py report.pbix --model
"""

import argparse
import difflib
import json
import zipfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Report/Layout parsing (pages + field usage) — plain stdlib, no dependencies
# ---------------------------------------------------------------------------

def decode_json_bytes(data: bytes, label: str):
    """Layout/DataModelSchema entries are usually UTF-16LE with a BOM; some
    exports are plain UTF-8. Try both before giving up."""
    for enc in ("utf-16-le", "utf-8"):
        try:
            text = data.decode(enc)
            text = text.lstrip("\ufeff\x00")
            brace = text.find("{")
            if brace > 0:
                text = text[brace:]
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    raise ValueError(f"Could not decode {label} as JSON (tried utf-16-le, utf-8)")


def load_layout(pbix_path: str):
    """Load layout from either Report/Layout (old format) or Report/definition (new format)"""
    with zipfile.ZipFile(pbix_path) as z:
        all_files = z.namelist()
        
        # Try Report/Layout first (older Power BI files)
        candidates = [
            "Report/Layout",
            "Report/layout", 
            "report/layout",
            "report/Layout"
        ]
        
        name = None
        for candidate in candidates:
            if candidate in all_files:
                name = candidate
                break
        
        # If not found, try case-insensitive search
        if not name:
            name = next((n for n in all_files if n.lower() == "report/layout"), None)
        
        # If found, read and return it
        if name:
            data = z.read(name)
            return decode_json_bytes(data, "Report/Layout")
        
        # If old format not found, try newer format with Report/definition/pages
        page_files = [n for n in all_files if n.startswith('Report/definition/pages/') and n.endswith('/page.json')]
        if page_files:
            # For newer format, construct a layout from pages AND their visuals
            layout = {"sections": []}
            page_dirs = sorted(set(pf.split('/')[3] for pf in page_files))[:50]
            
            for page_dir in page_dirs:
                page_file = f"Report/definition/pages/{page_dir}/page.json"
                if page_file in all_files:
                    try:
                        data = z.read(page_file)
                        page_data = decode_json_bytes(data, f"Page {page_dir}")
                        # Extract page info
                        display_name = page_data.get("displayName", page_dir).strip()
                        
                        # Also load all visuals for this page
                        visual_files = [n for n in all_files if n.startswith(f'Report/definition/pages/{page_dir}/visuals/') and n.endswith('/visual.json')]
                        visual_objects = {}
                        
                        for visual_file in visual_files:
                            try:
                                vdata = z.read(visual_file)
                                visual_json = decode_json_bytes(vdata, f"Visual {visual_file}")
                                visual_name = visual_file.split('/')[-2]  # Get visual ID
                                visual_objects[visual_name] = visual_json
                            except Exception:
                                continue
                        
                        # Combine page data with visuals
                        section = {
                            "name": page_dir,
                            "displayName": display_name,
                            "visibility": 1 if page_data.get('visibility') and 'hidden' in page_data.get('visibility', '').lower() else 0,
                            "objects": page_data.get("objects", {}),
                            "filterConfig": page_data.get("filterConfig", {}),
                            "_visuals": visual_objects  # Store visuals for field extraction
                        }
                        layout["sections"].append(section)
                    except Exception:
                        continue
            
            if layout["sections"]:
                return layout
        
        # Neither format found
        raise FileNotFoundError(
            f"No layout data found in {pbix_path}. "
            f"Checked for: Report/Layout (old), Report/definition/pages (new). "
            f"File contains: {all_files[:15]}..."
        )



def list_pages(layout: dict):
    """List every page, in the same order Power BI stores/displays them.

    Includes a `hidden` flag: pages set to "Hidden" in Power BI (used for
    tooltip pages, drillthrough targets, or pages the author hid from the nav
    bar) still exist in Report/Layout and are included here, but they render
    as a small icon rather than a normal tab — that's why a tab in the UI can
    look truncated or unlabeled compared to what this prints.
    """
    sections = layout.get("sections", [])
    pages = []
    for i, s in enumerate(sections):
        raw_name = s.get("displayName") or s.get("name") or ""
        pages.append({
            "index": i,
            "name": s.get("name"),
            "displayName": raw_name.strip(),  # trim stray whitespace some exports leave in
            "hidden": s.get("visibility") == 1,
        })
    return pages


def filter_placeholder_pages(pages):
    """Filter out generic/placeholder page names like 'Page 1', 'Page 2', etc.
    
    Keeps meaningful pages while removing auto-generated or template pages.
    """
    import re
    
    # Patterns to exclude
    exclude_patterns = [
        r'^Page\s+\d+$',  # "Page 1", "Page 2", etc.
        r'^Duplicate of (Duplicate of )?Page\s+\d+$',  # "Duplicate of Page 1", etc.
        r'^pag$',  # Generic "pag" placeholder
    ]
    
    filtered = []
    for page in pages:
        display_name = page["displayName"]
        # Check if name matches any exclude pattern
        if any(re.match(pattern, display_name.strip()) for pattern in exclude_patterns):
            continue
        filtered.append(page)
    
    return filtered


def _walk(node, sink):
    """Recursively find Column / Measure / HierarchyLevel references anywhere
    in a parsed Layout subtree, including inside nested JSON-encoded strings
    (config/filters/query/etc.).
    
    Also handles newer Power BI format field references like "Table|Field" and
    visuals stored separately in _visuals key.
    """
    if node is None:
        return
    if isinstance(node, list):
        for item in node:
            _walk(item, sink)
        return
    if isinstance(node, str):
        # Check for field references like "Sales|OrderDate" or "Table|FieldName"
        if "|" in node and len(node.split("|")) == 2:
            parts = node.split("|")
            if parts[0] and parts[1]:  # both parts non-empty
                sink.append({"entity": parts[0], "property": parts[1], "kind": "Column"})
        # Try parsing as JSON if looks like JSON
        if node.strip().startswith("{") or node.strip().startswith("["):
            try:
                _walk(json.loads(node), sink)
            except (json.JSONDecodeError, ValueError):
                pass
        return
    
    if not isinstance(node, dict):
        return

    # Handle _visuals (newer Power BI format)
    if "_visuals" in node:
        visuals = node["_visuals"]
        if isinstance(visuals, dict):
            for visual_data in visuals.values():
                _walk(visual_data, sink)

    # Old format: Column/Measure/HierarchyLevel with Expression
    col = node.get("Column")
    if isinstance(col, dict) and "Property" in col:
        source_ref = (col.get("Expression") or {}).get("SourceRef") or {}
        sink.append({"entity": source_ref.get("Entity", "(unknown table)"),
                     "property": col["Property"], "kind": "Column"})

    meas = node.get("Measure")
    if isinstance(meas, dict) and "Property" in meas:
        source_ref = (meas.get("Expression") or {}).get("SourceRef") or {}
        sink.append({"entity": source_ref.get("Entity", "(unknown table)"),
                     "property": meas["Property"], "kind": "Measure"})

    hier = node.get("HierarchyLevel")
    if isinstance(hier, dict):
        try:
            source_ref = hier["Expression"]["Hierarchy"]["Expression"]["SourceRef"]
            sink.append({"entity": source_ref.get("Entity", "(unknown table)"),
                         "property": hier.get("Level", "(hierarchy level)"),
                         "kind": "Hierarchy level"})
        except (KeyError, TypeError):
            pass

    # Handle config/filters/query nested in various formats
    for key in ("config", "filters", "query", "parameters", "dataTransforms", "projectionOrdering"):
        val = node.get(key)
        if isinstance(val, str):
            trimmed = val.strip()
            if trimmed.startswith("{") or trimmed.startswith("["):
                try:
                    _walk(json.loads(val), sink)
                    continue  # already recursed via the parsed version
                except (json.JSONDecodeError, ValueError):
                    pass
        else:
            _walk(val, sink)

    # Recurse through all other values
    for v in node.values():
        _walk(v, sink)


def _dedupe(fields):
    """Aggressive deduplication: deduplicate by normalized (entity, property, kind) tuple.
    For each unique combination, keep the entry with the most descriptive entity name
    (prefer real names over "(unknown table)" or empty values)."""
    by_key = {}
    
    for f in fields:
        # Create a normalized key: (normalized_entity, normalized_property, kind)
        norm_entity = normalize_key(f.get("entity", "") or "(unknown)")
        norm_prop = normalize_key(f["property"])
        kind = f["kind"]
        
        key = (norm_entity, norm_prop, kind)
        
        if key not in by_key:
            by_key[key] = f
        else:
            # Keep entry with better entity name (prefer real names)
            old_entity = by_key[key].get("entity", "") or "(unknown)"
            new_entity = f.get("entity", "") or "(unknown)"
            
            # Prefer non-(unknown table) entries
            if new_entity != "(unknown table)" and old_entity == "(unknown table)":
                by_key[key] = f
            # Prefer non-empty, non-parenthetical names
            elif len(new_entity) > len(old_entity) and not new_entity.startswith("("):
                by_key[key] = f
    
    return list(by_key.values())


def fields_on_page(layout: dict, page_index: int):
    section = layout["sections"][page_index]
    sink = []
    _walk(section, sink)
    return _dedupe(sink)


def get_page_layout_info(layout: dict, page_index: int):
    """Extract visualization/layout information for a page.
    
    Returns a dict with:
    - page_name: Display name of the page
    - field_count: Number of fields/columns on the page
    - visualizations: List of visual objects on the page
    - hidden: Whether the page is hidden
    """
    if page_index < 0 or page_index >= len(layout.get("sections", [])):
        return None
    
    section = layout["sections"][page_index]
    page_name = section.get("displayName") or section.get("name") or f"Page {page_index}"
    
    # Get field count
    fields = fields_on_page(layout, page_index)
    field_count = len(fields)
    
    # Extract visualizations from objects
    visualizations = []
    objects_dict = section.get("objects", {})
    
    if isinstance(objects_dict, dict):
        for obj_key, obj_data in objects_dict.items():
            if isinstance(obj_data, dict):
                # Extract visual config
                visual_name = obj_data.get("name") or obj_key
                visual_type = obj_data.get("type", "Visual")
                
                # Try to get more info about the visual
                config = obj_data.get("config", {})
                visual_title = config.get("name") if isinstance(config, dict) else "Unnamed"
                
                visualizations.append({
                    "id": obj_key,
                    "name": visual_name,
                    "type": visual_type,
                    "title": visual_title,
                })
    
    # Also check _visuals for newer format
    if "_visuals" in section and isinstance(section["_visuals"], dict):
        for visual_id, visual_data in section["_visuals"].items():
            if isinstance(visual_data, dict):
                visual_name = visual_data.get("name") or visual_id
                visual_type = visual_data.get("type", "Visual")
                config = visual_data.get("config", {})
                visual_title = config.get("name") if isinstance(config, dict) else visual_name
                
                # Avoid duplicates
                if not any(v["id"] == visual_id for v in visualizations):
                    visualizations.append({
                        "id": visual_id,
                        "name": visual_name,
                        "type": visual_type,
                        "title": visual_title,
                    })
    
    return {
        "page_name": page_name,
        "page_index": page_index,
        "field_count": field_count,
        "visualizations": visualizations,
        "hidden": section.get("visibility") == 1,
        "visualization_count": len(visualizations),
    }


def fields_across_report(layout: dict):
    sink = []
    _walk(layout, sink)
    return _dedupe(sink)


def resolve_page(layout: dict, page_arg: str):
    """Resolve a page by index, exact name, or (failing that) a unique
    case/whitespace-insensitive partial match — so a name copied from a
    truncated UI tab, or typed in the wrong case, still resolves."""
    pages = list_pages(layout)
    arg = page_arg.strip()

    if arg.isdigit():
        idx = int(arg)
        return (pages[idx] if 0 <= idx < len(pages) else None), pages

    target = arg.lower()
    exact = next((p for p in pages if p["displayName"].lower() == target), None)
    if exact:
        return exact, pages

    contains = [p for p in pages if target in p["displayName"].lower()]
    if len(contains) == 1:
        return contains[0], pages

    return None, pages


def suggest_pages(pages, page_arg: str, limit: int = 3):
    """Closest-matching page names, for a helpful 'did you mean' message."""
    names = [p["displayName"] for p in pages]
    return difflib.get_close_matches(page_arg.strip(), names, n=limit, cutoff=0.4)


# ---------------------------------------------------------------------------
# Naming-convention detection + name matching (shared by --scope and the web app)
# ---------------------------------------------------------------------------

def normalize_key(s: str) -> str:
    """Aggressive normalization: lowercase, remove spaces/underscores/dashes/dots/commas/parens"""
    s = str(s).lower()
    # Remove common separators and spaces
    s = s.replace("_", "").replace("-", "").replace(" ", "").replace(".", "").replace(",", "").replace("(", "").replace(")", "")
    # Remove leading/trailing whitespace
    return s.strip()


def levenshtein(a: str, b: str) -> int:
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            curr[j] = min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost)
        prev = curr
    return prev[len(b)]


def similarity(a: str, b: str) -> float:
    na, nb = normalize_key(a), normalize_key(b)
    if na == nb:
        return 1.0
    if not na or not nb:
        return 0.0
    dist = levenshtein(na, nb)
    return 1 - dist / max(len(na), len(nb))


import re as _re

_STYLE_PATTERNS = [
    ("snake_case", _re.compile(r"^[a-z0-9]+(_[a-z0-9]+)+$")),
    ("camelCase", _re.compile(r"^[a-z][a-z0-9]*([A-Z][a-z0-9]*)+$")),
    ("PascalCase", _re.compile(r"^([A-Z][a-z0-9]*){2,}$")),
    ("Title Case", _re.compile(r"^([A-Z][a-z0-9]*)( [A-Z][a-z0-9]*)+$")),
]


def detect_style(name: str) -> str:
    n = str(name)
    for label, pattern in _STYLE_PATTERNS:
        if pattern.match(n):
            return label
    if " " in n:
        return "space separated"
    return "other"


def majority_style(fields) -> str:
    tally = {}
    for f in fields:
        s = detect_style(f["property"])
        tally[s] = tally.get(s, 0) + 1
    if not tally:
        return "other"
    return max(tally, key=tally.get)


def field_exists_anywhere_in_inventory(property_name: str, inventory: list) -> bool:
    """Check if a field property exists anywhere in the new report's inventory."""
    normalized_prop = normalize_key(property_name)
    return any(normalize_key(f["property"]) == normalized_prop for f in inventory)


def match_field(old_field: dict, inventory: list) -> dict:
    """Match an old field to the best candidate in the new inventory.
    
    Strategy:
    1. Try exact match (same table + same field name after normalization)
    2. Try field name match in different table
    3. Find best similarity score among all candidates
    4. Return with appropriate confidence level
    """
    old_key = normalize_key(old_field["property"])
    old_entity_key = normalize_key(old_field["entity"])
    
    # LEVEL 1: Exact match - same table AND same field
    qualified_exact = next(
        (f for f in inventory
         if normalize_key(f["property"]) == old_key and normalize_key(f["entity"]) == old_entity_key),
        None,
    )
    if qualified_exact:
        return {"status": "Exact match", "match": qualified_exact, "confidence": 1.0,
                "note": "Same table and field name.", "missing_from_new_report": False}

    # LEVEL 2: Field name exact match in any table
    name_exact = next((f for f in inventory if normalize_key(f["property"]) == old_key), None)
    if name_exact:
        return {"status": "Field name matches (different table)", "match": name_exact, "confidence": 0.95,
                "note": f"Field exists in \"{name_exact['entity']}\" instead of \"{old_field['entity']}\".", "missing_from_new_report": False}

    # LEVEL 3: Find best similarity match across all candidates
    best, best_score = None, 0.0
    for cand in inventory:
        score = similarity(old_field["property"], cand["property"])
        if score > best_score:
            best, best_score = cand, score

    # Higher confidence thresholds for accuracy
    if best and best_score >= 0.90:
        return {"status": "Likely match", "match": best, "confidence": best_score,
                "note": "Very similar naming — high confidence match.", "missing_from_new_report": False}
    if best and best_score >= 0.75:
        return {"status": "Possible match", "match": best, "confidence": best_score,
                "note": "Similar naming — manual review recommended.", "missing_from_new_report": False}
    
    # Check if field is completely missing from new report
    is_missing = not field_exists_anywhere_in_inventory(old_field["property"], inventory)
    missing_msg = " [MISSING FROM NEW REPORT]" if is_missing else " [No similar field found]"
    
    return {"status": "No match found", "match": None, "confidence": 0.0,
            "note": f"Field will need to be created in the new report.{missing_msg}", "missing_from_new_report": is_missing}


def model_field_inventory(pbix_path: str):
    """Full table/column/measure inventory straight from the VertiPaq data
    model via pbixray — works for Import-mode reports too. Returns
    (fields, warning_or_none)."""
    try:
        from pbixray import PBIXRay
    except ImportError:
        return [], None  # pbixray installed at startup, suppress warning

    try:
        model = PBIXRay(pbix_path)
        fields = []
        for _, row in model.schema.iterrows():
            fields.append({"entity": row["TableName"], "property": row["ColumnName"],
                            "kind": "Column", "source": "Data model"})
        for _, row in model.dax_measures.iterrows():
            fields.append({"entity": row["TableName"], "property": row["Name"],
                            "kind": "Measure", "source": "Data model"})
        return fields, None
    except Exception as e:  # thin/live-connect reports have no embedded model
        return [], None  # Silently fall back to visual fields only


def extract_dax_expressions(pbix_path: str):
    """Extract DAX expressions for measures and calculated columns from the data model.
    
    Returns a dict: {(table, field): dax_expression, ...}
    Tries pbixray first, then falls back to Metadata parsing.
    """
    dax_map = {}
    
    print(f"\n[DAX] Starting extraction from: {pbix_path}")
    
    # Method 1: Try pbixray (primary method)
    try:
        print("[DAX] Attempting pbixray extraction...")
        from pbixray import PBIXRay
        import pandas as pd
        
        model = PBIXRay(pbix_path)
        
        # Get measures
        try:
            if hasattr(model, 'dax_measures') and model.dax_measures is not None:
                for _, row in model.dax_measures.iterrows():
                    table = str(row.get("TableName", "")).strip()
                    name = str(row.get("Name", "")).strip()
                    expr = str(row.get("Expression", "")).strip()
                    if table and name and expr and expr.lower() != "nan":
                        key = (table, name)
                        dax_map[key] = expr
                        print(f"[DAX] ✓ Measure: {key[0]}.{key[1]}")
        except Exception as e:
            pass
        
        # Get calculated columns
        try:
            if hasattr(model, 'dax_columns') and model.dax_columns is not None:
                for _, row in model.dax_columns.iterrows():
                    table = str(row.get("TableName", "")).strip()
                    name = str(row.get("ColumnName", "")).strip()
                    expr = str(row.get("Expression", "")).strip()
                    if table and name and expr and expr.lower() != "nan":
                        key = (table, name)
                        dax_map[key] = expr
                        print(f"[DAX] ✓ Column: {key[0]}.{key[1]}")
        except Exception as e:
            pass
        
        if dax_map:
            print(f"[DAX] [OK] pbixray extraction successful: {len(dax_map)} found")
            return dax_map
            
    except Exception as e:
        print(f"[DAX] pbixray unavailable: {e}")
    
    # Method 2: Primary fallback - Parse DataModelSchema directly
    print("[DAX] Using DataModelSchema fallback method...")
    try:
        with zipfile.ZipFile(pbix_path) as z:
            all_files = z.namelist()
            
            # Find schema files
            schema_files = [f for f in all_files if 'DataModelSchema' in f]
            print(f"[DAX] Found {len(schema_files)} schema file(s)")
            
            for schema_file in schema_files:
                try:
                    data = z.read(schema_file)
                    schema_data = decode_json_bytes(data, schema_file)
                    
                    if not isinstance(schema_data, dict):
                        continue
                    
                    # Navigate schema structure - usually: table_name -> measures/columns
                    for table_name, table_content in schema_data.items():
                        if not isinstance(table_content, dict):
                            continue
                        
                        # Try to extract measures
                        for measures_key in ["measures", "Measures", "expression_measures", "ExpressionMeasures"]:
                            measures_list = table_content.get(measures_key, [])
                            if isinstance(measures_list, list):
                                for measure in measures_list:
                                    if not isinstance(measure, dict):
                                        continue
                                    
                                    # Extract name and expression
                                    measure_name = None
                                    measure_expr = None
                                    
                                    # Try different possible keys for name
                                    for n_key in ["name", "Name", "MeasureName", "measureName"]:
                                        if n_key in measure:
                                            measure_name = str(measure[n_key]).strip()
                                            if measure_name:
                                                break
                                    
                                    # Try different possible keys for expression
                                    for e_key in ["expression", "Expression", "expressionSource", "ExpressionSource", "dax", "DAX"]:
                                        if e_key in measure:
                                            measure_expr = str(measure[e_key]).strip()
                                            if measure_expr and measure_expr.lower() != "nan":
                                                break
                                    
                                    if measure_name and measure_expr:
                                        key = (table_name, measure_name)
                                        if key not in dax_map:
                                            dax_map[key] = measure_expr
                                            if len(dax_map) <= 3:
                                                print(f"[DAX] [OK] Measure: {key[0]}.{key[1]}")
                        
                        # Try to extract calculated columns
                        for columns_key in ["columns", "Columns", "expression_columns", "ExpressionColumns"]:
                            columns_list = table_content.get(columns_key, [])
                            if isinstance(columns_list, list):
                                for column in columns_list:
                                    if not isinstance(column, dict):
                                        continue
                                    
                                    # Check if it has an expression (calculated column)
                                    column_name = None
                                    column_expr = None
                                    
                                    for n_key in ["name", "Name", "ColumnName", "columnName"]:
                                        if n_key in column:
                                            column_name = str(column[n_key]).strip()
                                            if column_name:
                                                break
                                    
                                    for e_key in ["expression", "Expression", "expressionSource", "ExpressionSource"]:
                                        if e_key in column:
                                            column_expr = str(column[e_key]).strip()
                                            if column_expr and column_expr.lower() != "nan":
                                                break
                                    
                                    if column_name and column_expr:
                                        key = (table_name, column_name)
                                        if key not in dax_map:
                                            dax_map[key] = column_expr
                                            if len(dax_map) <= 3:
                                                print(f"[DAX] [OK] Column: {key[0]}.{key[1]}")
                
                except Exception as e:
                    print(f"[DAX] Error parsing {schema_file}: {e}")
    
    except Exception as e:
        print(f"[DAX] Schema parsing error: {e}")
    
    if dax_map:
        print(f"[DAX] [OK] Successfully extracted {len(dax_map)} DAX expressions")
    else:
        print(f"[DAX] No DAX expressions found (regular columns only)")
    
    return dax_map


def get_page_tables_with_details(layout: dict, page_index: int):
    """Extract tables and their columns/measures used ONLY on a specific page.
    Returns {table_name: {columns: [...], measures: [...], count: int}, ...}
    """
    try:
        # Get fields from this specific page
        page_fields = fields_on_page(layout, page_index)
        
        tables = {}
        
        # Group fields by table
        for field in page_fields:
            table_name = field.get("entity", "(unknown)")
            if table_name == "(unknown table)":
                table_name = "(unknown)"
            
            if table_name not in tables:
                tables[table_name] = {"columns": [], "measures": []}
            
            # Add field as column or measure
            item = {
                "name": field.get("property", ""),
                "kind": field.get("kind", "Column"),
                "data_type": "Unknown"
            }
            
            if field.get("kind") == "Measure":
                tables[table_name]["measures"].append(item)
            else:
                tables[table_name]["columns"].append(item)
        
        # Deduplicate and sort
        for table_name in tables:
            # Deduplicate columns
            cols_seen = set()
            unique_cols = []
            for col in tables[table_name]["columns"]:
                key = normalize_key(col["name"])
                if key not in cols_seen:
                    cols_seen.add(key)
                    unique_cols.append(col)
            tables[table_name]["columns"] = sorted(unique_cols, key=lambda x: x["name"])
            
            # Deduplicate measures
            meas_seen = set()
            unique_meas = []
            for meas in tables[table_name]["measures"]:
                key = normalize_key(meas["name"])
                if key not in meas_seen:
                    meas_seen.add(key)
                    unique_meas.append(meas)
            tables[table_name]["measures"] = sorted(unique_meas, key=lambda x: x["name"])
            
            # Calculate count
            tables[table_name]["count"] = len(tables[table_name]["columns"]) + len(tables[table_name]["measures"])
        
        return tables, None
    except Exception as e:
        return {}, str(e)


def get_all_tables_with_details(pbix_path: str, layout: dict):
    """Extract all tables used in the entire report with their columns and measures.
    Returns {table_name: {columns: [...], measures: [...], count: int}, ...}
    """
    try:
        # Get all fields from the entire report
        all_fields = fields_across_report(layout)
        
        tables = {}
        
        # Group fields by table
        for field in all_fields:
            table_name = field.get("entity", "(unknown)")
            
            # Skip unknown tables
            if not table_name or table_name == "(unknown table)" or table_name == "(unknown)":
                continue
            
            if table_name not in tables:
                tables[table_name] = {"columns": [], "measures": []}
            
            # Add field as column or measure
            item = {
                "name": field.get("property", ""),
                "kind": field.get("kind", "Column")
            }
            
            if field.get("kind") == "Measure":
                tables[table_name]["measures"].append(item)
            else:
                tables[table_name]["columns"].append(item)
        
        # Deduplicate and sort each table
        for table_name in tables:
            # Remove duplicate columns
            cols_seen = set()
            unique_cols = []
            for col in tables[table_name]["columns"]:
                key = col["name"].lower()
                if key not in cols_seen:
                    cols_seen.add(key)
                    unique_cols.append(col)
            tables[table_name]["columns"] = sorted(unique_cols, key=lambda x: x["name"])
            
            # Remove duplicate measures
            meas_seen = set()
            unique_meas = []
            for meas in tables[table_name]["measures"]:
                key = meas["name"].lower()
                if key not in meas_seen:
                    meas_seen.add(key)
                    unique_meas.append(meas)
            tables[table_name]["measures"] = sorted(unique_meas, key=lambda x: x["name"])
            
            # Total count
            tables[table_name]["count"] = len(tables[table_name]["columns"]) + len(tables[table_name]["measures"])
        
        return tables, None
    except Exception as e:
        return {}, str(e)


def build_new_inventory(new_pbix_path: str, new_layout: dict):
    """Merge model-derived fields (authoritative, if available) with every
    field referenced anywhere across the new report's visuals (catches
    hierarchy levels and anything the model reader missed)."""
    model_fields, warning = model_field_inventory(new_pbix_path)
    visual_fields = [dict(f, source="Used in a visual") for f in fields_across_report(new_layout)]

    merged = list(model_fields)
    seen = {(normalize_key(f["entity"]), normalize_key(f["property"])) for f in model_fields}
    for f in visual_fields:
        key = (normalize_key(f["entity"]), normalize_key(f["property"]))
        if key not in seen:
            merged.append(f)
            seen.add(key)
    return merged, warning


def scope_page(old_pbix_path: str, old_layout: dict, page_index: int, new_pbix_path: str, new_layout: dict):
    """Full scoping computation shared by the CLI --scope flag and the web app.
    
    KEY FIX: Use consistent extraction for both OLD and NEW reports:
    - Both now use model_field_inventory (if available) + visual fields
    - This ensures apples-to-apples comparison
    """
    # OLD REPORT: Extract using same method as new (model + visuals for consistency)
    old_visual_fields = fields_on_page(old_layout, page_index)
    old_model_fields, _ = model_field_inventory(old_pbix_path)
    
    # Merge old model + visual fields for comparison
    old_fields = list(old_model_fields)
    seen_old = {(normalize_key(f["entity"]), normalize_key(f["property"])) for f in old_model_fields}
    for f in old_visual_fields:
        key = (normalize_key(f["entity"]), normalize_key(f["property"]))
        if key not in seen_old:
            old_fields.append(f)
            seen_old.add(key)
    
    # NEW REPORT: Use standard method (model + visuals across entire report)
    new_inventory, inventory_warning = build_new_inventory(new_pbix_path, new_layout)

    old_style = majority_style(old_fields)
    new_style = majority_style(new_inventory)
    
    # Extract DAX expressions from old report
    dax_map = extract_dax_expressions(old_pbix_path)

    rows = []
    for f in old_fields:
        m = match_field(f, new_inventory)
        note = m["note"]
        if m["match"] and detect_style(m["match"]["property"]) != detect_style(f["property"]):
            note += f" Naming style differs (old: {detect_style(f['property'])}, new: {detect_style(m['match']['property'])})."
        
        # Get DAX expression if available
        dax_key = (f["entity"], f["property"])
        dax_expr = dax_map.get(dax_key, "")
        
        rows.append({
            "old_table": f["entity"], "old_field": f["property"], "kind": f["kind"],
            "status": m["status"],
            "new_table": m["match"]["entity"] if m["match"] else "",
            "new_field": m["match"]["property"] if m["match"] else "",
            "confidence": round(m["confidence"] * 100),
            "note": note,
            "missing_from_new_report": m.get("missing_from_new_report", False),
            "dax_expression": dax_expr,
        })
    rows.sort(key=lambda r: r["confidence"], reverse=True)
    return rows, old_style, new_style, inventory_warning


# ---------------------------------------------------------------------------
# Full data model (tables / columns / measures / DAX) — via pbixray
# ---------------------------------------------------------------------------

def dump_model(pbix_path: str):
    try:
        from pbixray import PBIXRay
    except ImportError:
        print("pbixray isn't installed. Run: pip install pbixray")
        return

    model = PBIXRay(pbix_path)

    print("\n=== Tables ===")
    print(model.tables)

    print("\n=== Columns (schema) ===")
    print(model.schema)  # columns: TableName, ColumnName, PandasDataType

    print("\n=== Measures (DAX) ===")
    measures = model.dax_measures  # TableName, Name, Expression, DisplayFolder, Description
    print(measures[["TableName", "Name", "Expression"]])

    print("\n=== Calculated columns (DAX) ===")
    print(model.dax_columns)  # TableName, ColumnName, Expression

    print("\n=== Relationships ===")
    print(model.relationships)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Inspect a Power BI .pbix file: pages, fields used per page, and the full data model."
    )
    parser.add_argument("pbix", help="Path to the .pbix file (the OLD report when using --scope)")
    parser.add_argument("--list-pages", action="store_true", help="List every page in the report")
    parser.add_argument("--page", help="Show columns/measures used on a page (by display name or index)")
    parser.add_argument("--model", action="store_true", help="Dump the full data model (requires: pip install pbixray)")
    parser.add_argument("--scope", metavar="NEW_PBIX",
                         help="Scope --page of this (old) report against NEW_PBIX; requires --page")
    parser.add_argument("--out", default="pbi_scoping_mapping",
                         help="Output basename for --scope (writes <out>.csv and <out>.xlsx)")
    args = parser.parse_args()

    if not Path(args.pbix).exists():
        raise SystemExit(f"File not found: {args.pbix}")

    layout = load_layout(args.pbix)

    if args.scope:
        if not args.page:
            raise SystemExit("--scope requires --page to specify which old-report page to scope.")
        if not Path(args.scope).exists():
            raise SystemExit(f"New report file not found: {args.scope}")
        match, pages = resolve_page(layout, args.page)
        if match is None:
            print(f"\nPage '{args.page}' not found.")
            for s in suggest_pages(pages, args.page):
                print(f"  did you mean: {s}")
            raise SystemExit(1)

        new_layout = load_layout(args.scope)
        rows, old_style, new_style, inventory_warning = scope_page(
            args.pbix, layout, match["index"], args.scope, new_layout
        )
        if inventory_warning:
            print(f"Note: {inventory_warning}")

        import pandas as pd
        df = pd.DataFrame(rows).rename(columns={
            "old_table": "Old Table", "old_field": "Old Field", "kind": "Type",
            "status": "Match Status", "new_table": "New Table", "new_field": "New Field",
            "confidence": "Confidence %", "note": "Notes",
        })
        df.to_csv(f"{args.out}.csv", index=False)
        df.to_excel(f"{args.out}.xlsx", index=False)
        print(f"\nScoped '{match['displayName']}' ({len(rows)} fields). "
              f"Old page naming style: {old_style}. New report naming style: {new_style}.")
        print(df.to_string(index=False))
        print(f"\nWrote {args.out}.csv and {args.out}.xlsx")
        return

    if args.list_pages or (not args.page and not args.model):
        pages = list_pages(layout)
        print(f"\n{len(pages)} page(s) found in {args.pbix}:\n")
        for p in pages:
            flag = "  (hidden — tooltip/drillthrough page, no full-size tab)" if p["hidden"] else ""
            print(f"  [{p['index']}] {p['displayName']}{flag}")
        if any(p["hidden"] for p in pages):
            print(
                "\nNote: hidden pages show as a small icon-only tab in Power BI "
                "Desktop (that's why some tab labels look cut off or blank) — "
                "use the exact name printed above, or the [index] number, with --page."
            )

    if args.page:
        match, pages = resolve_page(layout, args.page)
        if match is None:
            print(f"\nPage '{args.page}' not found.")
            suggestions = suggest_pages(pages, args.page)
            if suggestions:
                print("Did you mean:")
                for s in suggestions:
                    print(f"  - {s}")
            print("\nAll available pages:")
            for p in pages:
                flag = "  (hidden)" if p["hidden"] else ""
                print(f"  [{p['index']}] {p['displayName']}{flag}")
        else:
            fields = fields_on_page(layout, match["index"])
            print(f"\nFields used on page '{match['displayName']}' ({len(fields)} total):\n")
            for f in sorted(fields, key=lambda x: (x["kind"], x["entity"], x["property"])):
                print(f"  [{f['kind']:<15}] {f['entity']}.{f['property']}")

    if args.model:
        dump_model(args.pbix)


if __name__ == "__main__":
    main()
