"""
app.py — Field Router web app

A small Flask server that puts a browser front end on top of pbi_inspect.py.
Unlike the original all-JS version, this one can read the actual embedded
data model (via pbixray in pbi_inspect.py), which needs Python — so uploads
go to this local server instead of being parsed purely client-side. Files are
only ever read from your own machine; nothing goes out to the internet.

Install:
    pip install flask pbixray pandas openpyxl

Run:
    python app.py
    (then open http://127.0.0.1:5000 in your browser)
"""

import os
import tempfile
import uuid

from flask import Flask, request, jsonify, send_file, render_template_string
from werkzeug.utils import secure_filename

import pbi_inspect as pbi

app = Flask(__name__)

# session_id -> { old_path, new_path, old_layout, new_layout,
#                 new_inventory, inventory_warning }
SESSIONS = {}
UPLOAD_ROOT = tempfile.mkdtemp(prefix="field_router_")


def _session_or_404(session_id):
    session = SESSIONS.get(session_id)
    if not session:
        raise ValueError("Unknown or expired session — upload both reports again.")
    return session


@app.post("/api/analyze")
def analyze():
    old_file = request.files.get("old")
    new_file = request.files.get("new")
    if not old_file or not new_file:
        return jsonify({"error": "Both an old and a new .pbix file are required."}), 400

    session_id = uuid.uuid4().hex
    session_dir = os.path.join(UPLOAD_ROOT, session_id)
    os.makedirs(session_dir, exist_ok=True)

    old_path = os.path.join(session_dir, secure_filename(old_file.filename or "old.pbix"))
    new_path = os.path.join(session_dir, secure_filename(new_file.filename or "new.pbix"))
    old_file.save(old_path)
    new_file.save(new_path)

    try:
        old_layout = pbi.load_layout(old_path)
        new_layout = pbi.load_layout(new_path)
    except Exception as e:
        return jsonify({"error": f"Could not read one of the reports: {e}"}), 400

    new_inventory, inventory_warning = pbi.build_new_inventory(new_path, new_layout)

    SESSIONS[session_id] = {
        "old_path": old_path, "new_path": new_path,
        "old_layout": old_layout, "new_layout": new_layout,
        "new_inventory": new_inventory, "inventory_warning": inventory_warning,
    }

    pages = pbi.list_pages(old_layout)
    pages = pbi.filter_placeholder_pages(pages)  # Remove generic "Page 1" type entries
    warnings = []
    if inventory_warning:
        warnings.append(f"New report: {inventory_warning}")
    if any(p["hidden"] for p in pages):
        warnings.append(
            "Some old-report pages are hidden (tooltip/drillthrough pages) — "
            "they're included below but render as a small icon-only tab in "
            "Power BI Desktop, which is why their name can look cut off there."
        )
    
    # Check if pbixray is available for DAX extraction
    try:
        import pbixray
    except ImportError:
        warnings.append(
            "DAX/Expression extraction unavailable: pbixray isn't installed. "
            "Install with: python3.14 -m pip install pbixray --break-system-packages"
        )

    return jsonify({
        "session_id": session_id,
        "pages": pages,
        "new_field_count": len(new_inventory),
        "warnings": warnings,
    })


@app.post("/api/scope")
def scope():
    body = request.get_json(force=True)
    session_id = body.get("session_id")
    page_index = body.get("page_index")
    try:
        session = _session_or_404(session_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    try:
        rows, old_style, new_style, _ = pbi.scope_page(
            session["old_path"], session["old_layout"], page_index,
            session["new_path"], session["new_layout"],
        )
    except (IndexError, KeyError):
        return jsonify({"error": f"Page index {page_index} is not valid for this report."}), 400

    session["last_rows"] = rows  # cached for export, keyed by this session only
    return jsonify({"rows": rows, "old_naming_style": old_style, "new_naming_style": new_style})


@app.get("/api/export/<session_id>.<fmt>")
def export(session_id, fmt):
    try:
        session = _session_or_404(session_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    rows = session.get("last_rows")
    if not rows:
        return jsonify({"error": "Run a scope first (select a page) before exporting."}), 400

    import pandas as pd
    # Remove internal metadata before export
    export_rows = [{k: v for k, v in row.items() if k != 'missing_from_new_report'} for row in rows]
    df = pd.DataFrame(export_rows).rename(columns={
        "old_table": "Old Table", "old_field": "Old Field", "kind": "Type",
        "status": "Match Status", "new_table": "New Table", "new_field": "New Field",
        "confidence": "Confidence %", "dax_expression": "DAX / Expression", "note": "Notes",
    })

    out_path = os.path.join(UPLOAD_ROOT, session_id, f"pbi_scoping_mapping.{fmt}")
    if fmt == "csv":
        df.to_csv(out_path, index=False)
    elif fmt == "xlsx":
        df.to_excel(out_path, index=False)
    else:
        return jsonify({"error": f"Unsupported export format: {fmt}"}), 400

    return send_file(out_path, as_attachment=True, download_name=f"pbi_scoping_mapping.{fmt}")


INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Field Router — PBI Scoping Tool</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0F1417; --panel:#171E23; --panel-raised:#1D262C; --rule:#2B343B;
    --text:#E7ECEC; --text-dim:#8FA0A8; --rail:#4FA8D8;
    --green:#3ED598; --amber:#F0A93F; --red:#E2604F;
    --mono:'IBM Plex Mono', monospace; --display:'Space Grotesk', sans-serif; --body:'Inter', sans-serif;
  }
  *{box-sizing:border-box;}
  body{ margin:0; background:var(--bg); color:var(--text); font-family:var(--body); line-height:1.5; }
  .app{ display:grid; grid-template-columns:220px 1fr; min-height:100vh; }
  .rail{ border-right:1px solid var(--rule); padding:32px 20px; position:sticky; top:0; height:100vh; }
  .rail h1{ font-family:var(--display); font-size:18px; font-weight:700; margin:0 0 4px; }
  .rail .sub{ color:var(--text-dim); font-size:12px; margin:0 0 32px; }
  .step{ display:flex; gap:12px; padding:14px 0; border-bottom:1px solid var(--rule); opacity:0.4; }
  .step.active, .step.done{ opacity:1; }
  .step .num{ font-family:var(--mono); font-size:12px; width:22px; height:22px; border-radius:50%; border:1px solid var(--rule); display:flex; align-items:center; justify-content:center; flex-shrink:0; color:var(--text-dim); }
  .step.active .num{ border-color:var(--rail); color:var(--rail); }
  .step.done .num{ border-color:var(--green); color:var(--green); background:rgba(62,213,152,0.08); }
  .step .label strong{ display:block; font-size:13px; font-weight:600; }
  .step .label span{ color:var(--text-dim); font-size:11px; }
  .main{ padding:40px 48px; max-width:1180px; }
  .panel{ background:var(--panel); border:1px solid var(--rule); border-radius:10px; padding:28px; margin-bottom:24px; }
  .panel h2{ font-family:var(--display); font-size:16px; margin:0 0 6px; font-weight:600; }
  .panel .hint{ color:var(--text-dim); font-size:13px; margin:0 0 20px; max-width:640px; }
  .dropzone-row{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  .dropzone{ border:1.5px dashed var(--rule); border-radius:8px; padding:20px; background:var(--panel-raised); cursor:pointer; }
  .dropzone:hover{ border-color:var(--rail); }
  .dropzone.filled{ border-style:solid; border-color:var(--green); }
  .dropzone .tag{ font-family:var(--mono); font-size:10px; color:var(--rail); text-transform:uppercase; letter-spacing:.06em; }
  .dropzone .fname{ font-family:var(--mono); font-size:13px; margin-top:8px; word-break:break-all; }
  .dropzone .placeholder{ color:var(--text-dim); font-size:13px; margin-top:8px; }
  input[type=file]{ display:none; }
  button{ font-family:var(--body); font-weight:600; font-size:13px; border:none; border-radius:6px; padding:10px 18px; cursor:pointer; }
  button:disabled{ opacity:0.35; cursor:not-allowed; }
  .btn-primary{ background:var(--rail); color:#06181F; }
  .btn-ghost{ background:transparent; color:var(--text); border:1px solid var(--rule); }
  .btn-ghost:hover:not(:disabled){ border-color:var(--rail); color:var(--rail); }
  .btn-row{ display:flex; gap:10px; margin-top:20px; }
  .banner{ font-size:12.5px; border-radius:6px; padding:10px 14px; margin-bottom:16px; border-left:3px solid var(--amber); background:rgba(240,169,63,0.08); }
  .banner.error{ border-left-color:var(--red); background:rgba(226,96,79,0.08); }
  select{ width:100%; background:var(--panel-raised); color:var(--text); border:1px solid var(--rule); border-radius:6px; padding:10px 12px; font-size:13px; }
  .summary-strip{ display:flex; gap:18px; margin:18px 0 4px; flex-wrap:wrap; }
  .chip{ display:flex; align-items:center; gap:7px; font-size:12px; color:var(--text-dim); font-family:var(--mono); }
  .dot{ width:8px; height:8px; border-radius:50%; }
  .dot.green{ background:var(--green); } .dot.amber{ background:var(--amber); } .dot.red{ background:var(--red); }
  table{ width:100%; border-collapse:collapse; margin-top:14px; font-size:12.5px; }
  thead th{ text-align:left; font-weight:600; color:var(--text-dim); font-size:11px; text-transform:uppercase; letter-spacing:.04em; padding:8px 10px; border-bottom:1px solid var(--rule); position:sticky; top:0; background:var(--panel); }
  tbody td{ padding:9px 10px; border-bottom:1px solid rgba(43,52,59,0.6); vertical-align:top; }
  .dax-cell{ font-family:var(--mono); font-size:11px; color:var(--text-dim); background:var(--panel-raised); padding:6px 8px; border-radius:3px; max-height:60px; overflow:hidden; text-overflow:ellipsis; white-space:pre-wrap; word-break:break-word; position:relative; }
  .dax-cell:hover{ max-height:none; overflow:visible; white-space:normal; background:var(--panel); z-index:10; border:1px solid var(--rule); padding:8px; }
  .dax-cell.dax-unavailable{ color:var(--amber); background:rgba(180, 100, 0, 0.15); border:1px solid var(--amber); font-style:italic; }
  .field-pill{ font-family:var(--mono); font-size:12px; background:var(--panel-raised); border:1px solid var(--rule); border-radius:4px; padding:3px 7px; display:inline-block; }
  .search-row{ display:flex; gap:10px; align-items:center; margin-top:16px; }
  .search-row input{ flex:1; background:var(--panel-raised); border:1px solid var(--rule); color:var(--text); border-radius:6px; padding:9px 12px; font-size:13px; }
  .table-wrap{ max-height:520px; overflow:auto; border:1px solid var(--rule); border-radius:8px; margin-top:8px; }
  .footnote{ font-size:11.5px; color:var(--text-dim); margin-top:14px; }
  .kind-badge{ font-size:10px; font-family:var(--mono); color:var(--text-dim); border:1px solid var(--rule); border-radius:3px; padding:1px 5px; }
  .hidden-flag{ color:var(--amber); font-size:10px; margin-left:6px; }
  tbody tr.missing-field{ background:rgba(226,96,79,0.06); }
  tbody tr.missing-field td{ border-bottom-color:rgba(226,96,79,0.2); }
  .missing-indicator{ color:var(--red); font-size:10px; margin-left:4px; text-transform:uppercase; font-weight:600; letter-spacing:.03em; }
  
  /* Page Preview */
  .page-preview-container{ display:grid; grid-template-columns:1fr 300px; gap:24px; margin-top:24px; }
  .page-preview-panel{ background:var(--panel); border:1px solid var(--rule); border-radius:10px; padding:20px; }
  .page-preview-panel h3{ font-family:var(--display); font-size:13px; margin:0 0 16px; font-weight:600; text-transform:uppercase; letter-spacing:.05em; color:var(--text-dim); }
  .page-preview{ background:var(--panel-raised); border:1px solid var(--rule); border-radius:8px; padding:16px; aspect-ratio:16/9; display:flex; align-items:center; justify-content:center; overflow:hidden; position:relative; }
  .page-preview.empty{ color:var(--text-dim); font-size:13px; text-align:center; }
  .page-structure{ display:flex; flex-direction:column; gap:8px; }
  .structure-item{ font-size:12px; display:flex; align-items:center; gap:8px; color:var(--text); padding:8px; background:var(--panel-raised); border-radius:5px; border-left:3px solid var(--rail); }
  .structure-item.header{ border-left-color:var(--green); }
  .structure-item.visual{ border-left-color:var(--rail); }
  .structure-item.text{ border-left-color:var(--amber); }
  .structure-icon{ display:inline-block; width:6px; height:6px; background:currentColor; border-radius:50%; }
  
  
  /* Enhanced animations */
  @keyframes fadeIn{ from{ opacity:0; transform:translateY(8px); } to{ opacity:1; transform:translateY(0); } }

  .panel{ animation:fadeIn .3s ease-out; }
  
  /* Creator footer */
  .creator-credit{ position:fixed; bottom:16px; right:16px; font-size:11px; color:var(--text-dim); font-family:var(--mono); text-align:right; line-height:1.4; }
  .creator-credit .name{ color:var(--rail); font-weight:600; }
</style>
</head>
<body>
<div class="app">
  <div class="rail">
    <h1>Field Router</h1>
    <p class="sub">PBI page scoping</p>
    <div class="step" id="step1"><div class="num">1</div><div class="label"><strong>Upload</strong><span>Old &amp; new reports</span></div></div>
    <div class="step" id="step2"><div class="num">2</div><div class="label"><strong>Select page</strong><span>Old report page</span></div></div>
    <div class="step" id="step3"><div class="num">3</div><div class="label"><strong>Route fields</strong><span>Match &amp; export</span></div></div>
  </div>
  <div class="main">
    <div class="panel" id="panel-upload">
      <h2>1 &middot; Upload your two reports</h2>
      <p class="hint">Files are read by this local server (needed to read the real data model via pbixray) — nothing leaves your machine.</p>
      <div class="dropzone-row">
        <label class="dropzone" id="dz-old"><span class="tag">Old report</span><div class="fname" id="fname-old"></div><div class="placeholder" id="placeholder-old">Click to choose .pbix</div><input type="file" id="file-old" accept=".pbix"></label>
        <label class="dropzone" id="dz-new"><span class="tag">New report</span><div class="fname" id="fname-new"></div><div class="placeholder" id="placeholder-new">Click to choose .pbix</div><input type="file" id="file-new" accept=".pbix"></label>
      </div>
      <div id="upload-banners"></div>
      <div class="btn-row"><button class="btn-primary" id="btn-analyze" disabled>Analyze reports</button></div>
    </div>

    <div class="panel" id="panel-select" style="display:none;">
      <h2>2 &middot; Select the old page to scope</h2>
      <p class="hint">Pick the page whose columns and measures you want to trace into the new report.</p>
      <div class="page-preview-container">
        <div style="flex:1;">
          <select id="page-select"></select>
        </div>
        <div class="page-preview-panel">
          <h3>Page Structure</h3>
          <div id="page-structure" class="page-structure">
            <div class="structure-item empty" style="text-align:center;color:var(--text-dim);">Select a page</div>
          </div>
        </div>
      </div>
    </div>

    <div class="panel" id="panel-results" style="display:none;">
      <h2>3 &middot; Field routing</h2>
      <div id="results-banners"></div>
      <div class="summary-strip" id="summary-strip"></div>
      <div class="search-row">
        <input type="text" id="search-box" placeholder="Filter by field, table, or status...">
        <button class="btn-ghost" id="btn-csv">Download CSV</button>
        <button class="btn-primary" id="btn-xlsx">Download Excel</button>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Old table</th><th>Old field</th><th>Type</th><th></th><th>Match status</th><th>New table</th><th>New field</th><th>Confidence</th><th>DAX / Expression</th><th>Notes</th></tr></thead>
          <tbody id="results-body"></tbody>
        </table>
      </div>
      <p class="footnote" id="footnote"></p>
    </div>
  </div>
</div>
<script>
let sessionId = null, allPages = [], currentRows = [];


function setStep(n){ for(let i=1;i<=3;i++){ const el=document.getElementById('step'+i); el.classList.remove('active','done'); if(i<n) el.classList.add('done'); if(i===n) el.classList.add('active'); } }
setStep(1);

function banner(containerId, message, isError){ const c=document.getElementById(containerId); const div=document.createElement('div'); div.className='banner'+(isError?' error':''); div.textContent=message; c.appendChild(div); }
function clearBanners(containerId){ document.getElementById(containerId).innerHTML=''; }
function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

function wireDropzone(dzId, fileInputId, fnameId, placeholderId, onLoaded){
  const dz=document.getElementById(dzId), input=document.getElementById(fileInputId);
  dz.addEventListener('click', () => input.click());
  input.addEventListener('change', () => {
    const file = input.files[0]; if(!file) return;
    document.getElementById(fnameId).textContent = file.name;
    document.getElementById(placeholderId).style.display='none';
    dz.classList.add('filled');
    onLoaded(file);
  });
}
wireDropzone('dz-old','file-old','fname-old','placeholder-old', f => { window._oldFile=f; checkReady(); });
wireDropzone('dz-new','file-new','fname-new','placeholder-new', f => { window._newFile=f; checkReady(); });
function checkReady(){ document.getElementById('btn-analyze').disabled = !(window._oldFile && window._newFile); }

document.getElementById('btn-analyze').addEventListener('click', async () => {
  clearBanners('upload-banners');
  const btn = document.getElementById('btn-analyze');
  btn.disabled = true; btn.textContent = 'Analyzing…';
  const form = new FormData();
  form.append('old', window._oldFile);
  form.append('new', window._newFile);
  try {
    const res = await fetch('/api/analyze', { method:'POST', body: form });
    const data = await res.json();
    if (!res.ok) { banner('upload-banners', data.error || 'Analysis failed.', true); return; }
    sessionId = data.session_id;
    allPages = data.pages;
    (data.warnings || []).forEach(w => banner('upload-banners', w, false));

    const sel = document.getElementById('page-select');
    sel.innerHTML = '';
    allPages.forEach((p, i) => {
      const opt = document.createElement('option');
      opt.value = p.index;
      opt.textContent = p.displayName;
      sel.appendChild(opt);
    });
    document.getElementById('panel-select').style.display = 'block';
    setStep(2);
    sel.onchange = () => runScope(parseInt(sel.value, 10));
    if (allPages.length) runScope(allPages[0].index);
  } catch (e) {
    banner('upload-banners', 'Could not reach the server: ' + e.message, true);
  } finally {
    btn.disabled = false; btn.textContent = 'Analyze reports';
  }
});

async function runScope(pageIndex){
  clearBanners('results-banners');
  updatePagePreview(pageIndex);
  const res = await fetch('/api/scope', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ session_id: sessionId, page_index: pageIndex })
  });
  const data = await res.json();
  if (!res.ok) { banner('results-banners', data.error || 'Could not scope this page.', true); return; }
  currentRows = data.rows;
  document.getElementById('panel-results').style.display = 'block';
  setStep(3);
  if (currentRows.length === 0) {
    banner('results-banners', 'No column or measure references were found on this page.', false);
  }
  renderTable(currentRows);
  document.getElementById('footnote').textContent =
    `Old page dominant naming style: "${data.old_naming_style}". New report dominant naming style: "${data.new_naming_style}". Matching is name/structure-based — always confirm before rebuilding measures.`;
}

function updatePagePreview(pageIndex){
  const page = allPages.find(p => p.index === pageIndex);
  if (!page) return;
  
  const preview = document.getElementById('page-structure');
  preview.innerHTML = '';
  
  // Page name
  const nameItem = document.createElement('div');
  nameItem.className = 'structure-item header';
  nameItem.innerHTML = `📄 <strong>${escapeHtml(page.displayName)}</strong>`;
  preview.appendChild(nameItem);
  
  // Fields count
  const fieldsItem = document.createElement('div');
  fieldsItem.className = 'structure-item visual';
  fieldsItem.innerHTML = `📊 <strong>${page.field_count || '~50'}</strong> fields detected`;
  preview.appendChild(fieldsItem);
  
  // Hidden status
  if (page.hidden) {
    const hiddenItem = document.createElement('div');
    hiddenItem.className = 'structure-item text';
    hiddenItem.innerHTML = `⚠️ Hidden page (tooltip/drillthrough)`;
    preview.appendChild(hiddenItem);
  }
  
  // Page type
  const typeItem = document.createElement('div');
  typeItem.className = 'structure-item';
  typeItem.style.borderLeftColor = 'var(--amber)';
  typeItem.innerHTML = `🎯 Power BI report page`;
  preview.appendChild(typeItem);
}

function statusColor(status){ if(status==='Exact match') return 'green'; if(status==='No match found') return 'red'; return 'amber'; }

function renderTable(rows){
  const body = document.getElementById('results-body');
  body.innerHTML = '';
  for (const r of rows){
    const tr = document.createElement('tr');
    const color = statusColor(r.status);
    if (r.missing_from_new_report) {
      tr.classList.add('missing-field');
    }
    const missingBadge = r.missing_from_new_report ? '<span class="missing-indicator">⚠ Missing</span>' : '';
    const daxDisplay = r.dax_expression ? 
      `<div class="dax-cell">${escapeHtml(r.dax_expression.substring(0, 200))}${r.dax_expression.length > 200 ? '...' : ''}</div>` : 
      '<div class="dax-cell dax-unavailable" title="Install pbixray to extract DAX expressions: python3.14 -m pip install pbixray --break-system-packages">⚠ pbixray required</div>';
    tr.innerHTML = `
      <td><span class="field-pill">${escapeHtml(r.old_table)}</span></td>
      <td><span class="field-pill">${escapeHtml(r.old_field)}</span>${missingBadge}</td>
      <td><span class="kind-badge">${escapeHtml(r.kind)}</span></td>
      <td><div class="dot ${color}"></div></td>
      <td>${escapeHtml(r.status)}</td>
      <td>${r.new_table ? `<span class="field-pill">${escapeHtml(r.new_table)}</span>` : '—'}</td>
      <td>${r.new_field ? `<span class="field-pill">${escapeHtml(r.new_field)}</span>` : '—'}</td>
      <td>${r.confidence ? r.confidence + '%' : '—'}</td>
      <td>${daxDisplay}</td>
      <td style="color:var(--text-dim); font-size:12px;">${escapeHtml(r.note)}</td>`;
    body.appendChild(tr);
  }
  renderSummary(rows);
}

function renderSummary(rows){
  const counts = { green:0, amber:0, red:0 };
  rows.forEach(r => counts[statusColor(r.status)]++);
  document.getElementById('summary-strip').innerHTML = `
    <div class="chip"><div class="dot green"></div>${counts.green} exact</div>
    <div class="chip"><div class="dot amber"></div>${counts.amber} likely/possible</div>
    <div class="chip"><div class="dot red"></div>${counts.red} no match</div>
    <div class="chip">${rows.length} total fields on page</div>`;
}

document.getElementById('search-box').addEventListener('input', e => {
  const q = e.target.value.toLowerCase();
  renderTable(currentRows.filter(r =>
    r.old_table.toLowerCase().includes(q) || r.old_field.toLowerCase().includes(q) ||
    r.new_table.toLowerCase().includes(q) || r.new_field.toLowerCase().includes(q) ||
    r.status.toLowerCase().includes(q)
  ));
});

document.getElementById('btn-csv').addEventListener('click', () => { if(sessionId) window.location = `/api/export/${sessionId}.csv`; });
document.getElementById('btn-xlsx').addEventListener('click', () => { if(sessionId) window.location = `/api/export/${sessionId}.xlsx`; });
</script>
<div class="creator-credit">Created by<br><span class="name">Manish Kumar Yadav</span></div>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(INDEX_HTML)


if __name__ == "__main__":
    import socket
    
    # Get local IP address
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "127.0.0.1"
    
    port = 5000
    
    print("\n" + "="*70)
    print(" 🚀 POWER BI FIELD ROUTER - SCOPING TOOL")
    print("="*70)
    print(f"\n📍 Local Access (this machine):")
    print(f"   http://127.0.0.1:{port}")
    print(f"\n🌐 Network Access (share with others):")
    print(f"   http://{local_ip}:{port}")
    print(f"\n💻 Computer Name:")
    print(f"   http://{hostname}:{port}")
    print(f"\n📋 Instructions:")
    print(f"   1. Share the network link above with colleagues")
    print(f"   2. They can access it from any computer on the same network")
    print(f"   3. Files are processed locally on THIS machine only")
    print(f"\n⏹️  Press CTRL+C to stop the server")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
