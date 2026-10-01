r"""Render the project's state.json (+ emails.json + activity log) to dashboard.html.

Self-contained: no external resources, light/dark via prefers-color-scheme.
Usage: python render_dashboard.py [--project ID] [--out PATH]
"""

from __future__ import annotations

import argparse
import html
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import guard
import pm_state
import project

STEP_COLS = [
    ("drawing_intake", "Intake"),
    ("register_review", "Register"),
    ("register_signoff", "Sign-off"),
    ("doc_checklist", "Checklist"),
    ("sow_check", "SOW"),
    ("programme_review", "Programme"),
    ("cost_review", "Cost"),
]

STATUS_META = {
    "signed_off": ("ok", "✓"),
    "in_review": ("run", "●"),
    "producing": ("run", "●"),
    "briefed": ("run", "○"),
    "awaiting_signoff": ("gate", "✋"),
    "pending": ("dim", "–"),
    "blocked": ("warn", "!"),
    "n/a": ("na", "·"),
}

def wait_groups() -> list[tuple[str, str, str]]:
    return [
        ("approval", "Approval needed", "gate"),
        ("question", f"Question for {pm_state.owner()}", "warn"),
        ("missing_input", "Missing input", "warn"),
        ("external", "External party", "dim"),
        ("email", "From email", "run"),
    ]

CSS = """
:root{--bg:#faf9f5;--card:#fff;--ink:#1a1915;--mut:#6e6a60;--bd:#e4e1d8;
--ok-bg:#eaf3de;--ok-tx:#27500a;--warn-bg:#faeeda;--warn-tx:#633806;
--gate-bg:#fcebeb;--gate-tx:#791f1f;--run-bg:#e6f1fb;--run-tx:#0c447c;--dim-bg:#f1efe8;--dim-tx:#5f5e5a;}
@media(prefers-color-scheme:dark){:root{--bg:#171613;--card:#201f1b;--ink:#ece9e2;--mut:#a3a094;--bd:#38362f;
--ok-bg:#27500a;--ok-tx:#c0dd97;--warn-bg:#633806;--warn-tx:#fac775;
--gate-bg:#791f1f;--gate-tx:#f7c1c1;--run-bg:#0c447c;--run-tx:#b5d4f4;--dim-bg:#2a2925;--dim-tx:#b4b2a9;}}
*{box-sizing:border-box}body{margin:0;padding:24px;background:var(--bg);color:var(--ink);
font:15px/1.55 "Segoe UI",system-ui,sans-serif;max-width:1100px;margin-inline:auto}
h1{font-size:21px;font-weight:600;margin:0}h2{font-size:15px;font-weight:600;margin:0 0 10px;color:var(--mut)}
.sub{color:var(--mut);font-size:13px;margin:2px 0 18px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}
.stat{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:12px 16px}
.stat b{display:block;font-size:22px;font-weight:600}.stat span{font-size:12px;color:var(--mut)}
.panel{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px 20px;margin-bottom:18px}
.item{display:flex;gap:10px;align-items:baseline;padding:7px 0;border-top:1px solid var(--bd);font-size:14px}
.item:first-of-type{border-top:none}
.tag{font-size:11px;font-weight:600;padding:2px 9px;border-radius:10px;white-space:nowrap}
.tag.gate{background:var(--gate-bg);color:var(--gate-tx)}.tag.warn{background:var(--warn-bg);color:var(--warn-tx)}
.tag.ok{background:var(--ok-bg);color:var(--ok-tx)}.tag.run{background:var(--run-bg);color:var(--run-tx)}
.tag.dim{background:var(--dim-bg);color:var(--dim-tx)}
.who{margin-left:auto;font-size:12px;color:var(--mut);white-space:nowrap}
table{border-collapse:collapse;width:100%;font-size:13px}
th{font-size:11px;color:var(--mut);font-weight:600;text-align:center;padding:4px 2px}
th:first-child{text-align:left}
td{padding:5px 4px;text-align:center;border-top:1px solid var(--bd)}
td.name{text-align:left;font-weight:600;cursor:pointer;white-space:nowrap}
td.name small{color:var(--mut);font-weight:400;margin-left:6px}
.cell{display:inline-flex;align-items:center;justify-content:center;width:34px;height:26px;border-radius:6px;font-size:13px}
.cell.ok{background:var(--ok-bg);color:var(--ok-tx)}.cell.warn{background:var(--warn-bg);color:var(--warn-tx)}
.cell.gate{background:var(--gate-bg);color:var(--gate-tx)}.cell.run{background:var(--run-bg);color:var(--run-tx)}
.cell.dim,.cell.na{background:var(--dim-bg);color:var(--dim-tx)}
.hp{font-weight:600}.hp.green{color:var(--ok-tx)}.hp.amber{color:var(--warn-tx)}.hp.red{color:var(--gate-tx)}
tr.detail>td{text-align:left;background:var(--bg);padding:14px 16px;border-top:none}
tr.detail{display:none}tr.detail.open{display:table-row}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.kv{margin:0;padding:0;list-style:none;font-size:13px}.kv li{padding:3px 0;border-top:1px solid var(--bd)}
.kv li:first-child{border-top:none}.kv b{font-weight:600}
.log{font:12px/1.8 Consolas,monospace;color:var(--mut);margin:0;padding:0;list-style:none}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--mut);margin:0 0 8px}
footer{font-size:12px;color:var(--mut);margin-top:8px}
.ansrow{display:flex;gap:6px;width:100%;margin-top:6px}
input.ans{flex:1;font:13px/1.4 inherit;padding:6px 10px;border:1px solid var(--bd);border-radius:7px;
background:var(--bg);color:var(--ink)}
input.ans:focus{outline:none;border-color:var(--run-tx)}
button{font:13px/1 inherit;padding:7px 14px;border:1px solid var(--bd);border-radius:7px;
background:var(--card);color:var(--ink);cursor:pointer}
button:hover{background:var(--dim-bg)}
button.qb{font-size:12px;padding:6px 10px}
.copyrow{display:flex;gap:10px;align-items:center;margin-top:14px;padding-top:12px;border-top:1px solid var(--bd)}
#copyans{font-weight:600}
#chatlog{max-height:280px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;margin-bottom:10px}
.msg{padding:7px 12px;border-radius:10px;max-width:82%;font-size:14px;white-space:pre-wrap}
.msg.owner{background:var(--run-bg);color:var(--run-tx);align-self:flex-end}
.msg.pm{background:var(--dim-bg);color:var(--ink);align-self:flex-start}
.msg .mts{display:block;font-size:10px;opacity:0.7;margin-top:2px}
"""

JS = """
document.querySelectorAll('td.name').forEach(function(td){
  td.addEventListener('click',function(){
    var d=document.getElementById('d-'+td.dataset.k);
    if(d){d.classList.toggle('open');}
  });
});
document.querySelectorAll('button.qb').forEach(function(b){
  b.addEventListener('click',function(){
    var inp=b.parentElement.querySelector('input.ans');
    inp.value=b.dataset.fill;inp.focus();
  });
});
var served=location.protocol!=='file:';
if(served){document.querySelectorAll('.filemode').forEach(function(el){el.style.display='none';});}
else{document.querySelectorAll('button.sendb').forEach(function(b){b.style.display='none';});
  var m=document.getElementById('copymsg');
  if(m){m.textContent='Opened as a file - start serve_dashboard.py for direct Send-to-PM.';}}
document.querySelectorAll('button.sendb').forEach(function(b){
  b.addEventListener('click',function(){
    var inp=b.parentElement.querySelector('input.ans');
    var val=inp.value.trim();
    if(!val){inp.focus();return;}
    b.textContent='Sending…';b.disabled=true;
    fetch('/answer',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({id:inp.dataset.id,q:inp.dataset.q,a:val})})
    .then(function(r){if(!r.ok)throw 0;return r.json();})
    .then(function(){b.textContent='Sent to PM';inp.disabled=true;
      b.parentElement.querySelectorAll('button.qb').forEach(function(q){q.disabled=true;});})
    .catch(function(){b.textContent='Send to PM';b.disabled=false;
      var m=document.getElementById('copymsg');
      if(m){m.textContent='Send failed - is serve_dashboard.py running?';}});
  });
});
var sa=document.getElementById('sendall');
if(sa){if(!served){sa.style.display='none';}
  sa.addEventListener('click',function(){
    var batch=[];var rows=[];
    document.querySelectorAll('input.ans').forEach(function(inp){
      if(!inp.disabled&&inp.value.trim()){
        batch.push({id:inp.dataset.id,q:inp.dataset.q,a:inp.value.trim()});rows.push(inp);}
    });
    var msg=document.getElementById('copymsg');
    if(!batch.length){msg.textContent='Nothing to send - type answers first.';return;}
    sa.textContent='Sending…';sa.disabled=true;
    fetch('/answer',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify(batch)})
    .then(function(r){if(!r.ok)throw 0;return r.json();})
    .then(function(){
      rows.forEach(function(inp){inp.disabled=true;
        var b=inp.parentElement.querySelector('button.sendb');
        if(b){b.textContent='Sent to PM';b.disabled=true;}
        inp.parentElement.querySelectorAll('button.qb').forEach(function(q){q.disabled=true;});});
      sa.textContent='Send all answers to PM';sa.disabled=false;
      msg.textContent='Sent '+batch.length+' answers - the PM is on it.';})
    .catch(function(){sa.textContent='Send all answers to PM';sa.disabled=false;
      msg.textContent='Send failed - is serve_dashboard.py running?';});
  });}
var cp=document.getElementById('chatpanel');
if(cp&&served){
  cp.style.display='';
  var lastSig='';
  function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML;}
  function loadChat(){
    fetch('/chat').then(function(r){return r.json();}).then(function(msgs){
      var last=msgs.length?msgs[msgs.length-1]:null;
      var sig=msgs.length+':'+(last?(last.ts||'')+(last.text||'').length+last.role:'');
      if(sig===lastSig)return;
      lastSig=sig;
      var log=document.getElementById('chatlog');
      var html=msgs.map(function(m){
        return '<div class="msg '+(m.role==='pm'?'pm':'owner')+'">'+esc(m.text)+
          '<span class="mts">'+(m.ts||'').slice(11,16)+'</span></div>';
      }).join('');
      if(msgs.length&&msgs[msgs.length-1].role!=='pm'){
        html+='<div class="msg pm" style="opacity:0.6">PM is on it…</div>';
      }
      log.innerHTML=html;
      log.scrollTop=log.scrollHeight;
    }).catch(function(){});
  }
  loadChat();setInterval(loadChat,1000);
  function sendChat(){
    var inp=document.getElementById('chatin');
    var t=inp.value.trim();if(!t)return;
    inp.value='';
    fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({text:t})}).then(loadChat).catch(function(){});
  }
  document.getElementById('chatsend').addEventListener('click',sendChat);
  document.getElementById('chatin').addEventListener('keydown',function(e){
    if(e.key==='Enter'){sendChat();}});
}
var rs=document.getElementById('rescan');
if(rs){if(!served){rs.style.display='none';}
  rs.addEventListener('click',function(){rs.textContent='Rescanning…';rs.disabled=true;
    fetch('/rescan',{method:'POST'}).then(function(){location.reload();})
    .catch(function(){rs.textContent='Rescan';rs.disabled=false;});});}
var copyBtn=document.getElementById('copyans');
if(copyBtn){copyBtn.addEventListener('click',function(){
  var lines=['PM answers ('+new Date().toISOString().slice(0,10)+'):'];
  var n=0;
  document.querySelectorAll('input.ans').forEach(function(inp){
    if(inp.value.trim()){n++;
      lines.push(n+'. ['+inp.dataset.id+']');
      lines.push('   Q: '+inp.dataset.q);
      lines.push('   A: '+inp.value.trim());
    }
  });
  var msg=document.getElementById('copymsg');
  if(!n){msg.textContent='Nothing to copy - type an answer first.';return;}
  var text=lines.join('\\n');
  var ta=document.createElement('textarea');
  ta.value=text;document.body.appendChild(ta);ta.select();
  try{document.execCommand('copy');msg.textContent='Copied '+n+' answer'+(n>1?'s':'')+' - paste into the Claude chat.';}
  catch(e){msg.textContent='Copy failed - select and copy this: '+text;}
  document.body.removeChild(ta);
});}
"""


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


_CFG: dict | None = None


def cfg() -> dict:
    global _CFG
    if _CFG is None:
        _CFG = pm_state.load_json(pm_state.CONFIG_PATH, default={}) or {}
    return _CFG


def report_cfg() -> dict:
    return {"currency": "$", "area_unit": "sqm", "cost_label": "Budget", **cfg().get("report", {})}


def milestone() -> str:
    return (cfg().get("programme") or {}).get("milestone", "Milestone")


def money(v) -> str:
    if v is None:
        return "–"
    return report_cfg()["currency"] + format(round(v), ",")


def cost_line(cost: dict) -> str:
    r = report_cfg()
    return (f'{esc(r["cost_label"])} <b>{money(cost.get("total"))}</b> · '
            f'{money(cost.get("per_area"))}/{esc(r["area_unit"])} · '
            f'{esc(cost.get("area") or "?")} {esc(r["area_unit"])}')


def cell(status: str | None) -> str:
    cls, glyph = STATUS_META.get(status or "pending", ("dim", "?"))
    return f'<span class="cell {cls}" title="{esc(status)}">{glyph}</span>'


def render_waiting(stores: dict) -> str:
    items = []
    for key, s in stores.items():
        for w in s.get("waiting_on", []):
            items.append((key, s["name"], w))
    if not items:
        return '<div class="panel"><h2>Waiting on</h2><p class="sub">Nothing - all clear.</p></div>'
    out = ['<div class="panel"><h2>Items outstanding — what the PM is waiting on</h2>',
           '<p class="sub">Type answers below, then copy them to the clipboard and paste into the '
           'Claude chat — the PM records each answer, unblocks work, and refreshes this page.</p>']
    groups = wait_groups()
    order = {t: i for i, (t, _, _) in enumerate(groups)}
    items.sort(key=lambda x: order.get(x[2].get("type"), 9))
    labels = {t: (lbl, cls) for t, lbl, cls in groups}
    for key, name, w in items:
        lbl, cls = labels.get(w.get("type"), ("Other", "dim"))
        wid = esc(w.get("id"))
        qtext = esc(w.get("text"))
        quick = ""
        if w.get("type") == "approval":
            quick = ('<button class="qb" data-fill="Approved.">Approve</button>'
                     '<button class="qb" data-fill="Rejected: ">Reject</button>')
        out.append(
            f'<div class="item" style="flex-wrap:wrap">'
            f'<span class="tag {cls}">{esc(lbl)}</span>'
            f'<span style="flex:1;min-width:260px"><b>{esc(name)}</b> — {qtext}</span>'
            f'<span class="who">{esc(w.get("needed_from"))} · {esc(w.get("raised"))}</span>'
            f'<span class="ansrow"><input class="ans" data-id="{wid}" data-q="{qtext}" '
            f'placeholder="Your answer / context for the PM…">{quick}'
            f'<button class="sendb">Send to PM</button></span></div>')
    out.append('<div class="copyrow"><button id="sendall">Send all answers to PM</button>'
               '<button id="copyans" class="filemode">Copy answers for the PM</button>'
               '<span id="copymsg" class="sub"></span></div></div>')
    return "".join(out)


def render_detail(key: str, s: dict) -> str:
    issue = (s.get("drawing_stage") or {}).get("latest_issue") or {}
    dh = s.get("doc_health", {})
    prog = s.get("program", {})
    cost = s.get("cost", {})
    docs = "".join(
        f'<li><span class="tag {"ok" if d["status"]=="current" else "warn" if d["status"]=="stale" else "gate" if d["status"]=="missing" else "dim"}">{esc(d["status"])}</span> '
        f'<b>{esc(doc.replace("_", " "))}</b> — {esc(d.get("detail"))}</li>'
        for doc, d in dh.get("docs", {}).items())
    discs = issue.get("disciplines_detected")
    disc_txt = ", ".join(discs) if discs else "not yet deep-scanned"
    dates = ", ".join(prog.get("milestone_dates", [])) or "–"
    return f"""
<div class="grid2">
  <div><h2>Latest issue</h2><ul class="kv">
    <li><b>{esc(issue.get("set_file", "none found"))}</b></li>
    <li>Stage: {esc(issue.get("stage_folder", "–"))} · rev {esc(issue.get("revision") or "?")} · issued {esc(issue.get("issue_date", "–"))}</li>
    <li>Disciplines: {esc(disc_txt)}</li></ul>
  <h2 style="margin-top:14px">Programme</h2><ul class="kv">
    <li>{esc(milestone())} date(s): {esc(dates)}{" — governing " + esc(prog.get("governing_date")) if prog.get("governing_date") else ""}</li>
    <li>Latest file: {esc((prog.get("latest") or {}).get("name", "–"))}</li></ul>
  <h2 style="margin-top:14px">Cost</h2><ul class="kv">
    <li>{cost_line(cost)}</li>
    <li>Contract sum: {money(cost.get("contract_sum")) if cost.get("contract_sum") else "pre-award"}</li>
    <li>{cost.get("invoices", 0)} invoices · {cost.get("purchase_orders", 0)} POs · {cost.get("quotes", 0)} quotes</li></ul></div>
</div>"""


def render_matrix(stores: dict) -> str:
    head = "<tr><th>Project</th>" + "".join(f"<th>{lbl}</th>" for _, lbl in STEP_COLS) + "</tr>"
    rows = []
    ncols = len(STEP_COLS) + 1
    for key, s in sorted(stores.items()):
        kid = esc(key).replace("/", "-").replace(" ", "_")
        pipe = s.get("pipeline", {})
        cells = "".join(f"<td>{cell(pipe.get(step, {}).get('status'))}</td>" for step, _ in STEP_COLS)
        stage = (s.get("drawing_stage") or {}).get("current") or "?"
        rows.append(
            f'<tr><td class="name" data-k="{kid}">{esc(s["name"])}<small>{esc(stage)}</small></td>{cells}</tr>')
        rows.append(f'<tr class="detail" id="d-{kid}"><td colspan="{ncols}">{render_detail(key, s)}</td></tr>')
    legend = ('<p class="legend"><span>✓ signed off</span><span>● in progress / review</span>'
              '<span>✋ awaiting your sign-off</span><span>! blocked</span><span>– pending</span></p>')
    return f'<div class="panel"><h2>Pipeline — click the project row for detail</h2>{legend}<table>{head}{"".join(rows)}</table></div>'


def render_emails() -> str:
    emails = pm_state.load_json(pm_state.EMAILS_PATH, default=[])
    if not emails:
        return ""
    out = ['<div class="panel"><h2>Email watch</h2>']
    for e in emails[:15]:
        out.append(f'<div class="item"><span class="tag run">{esc(e.get("kind", "email"))}</span>'
                   f'<span>{esc(e.get("subject"))} · {esc(e.get("sender", ""))}</span>'
                   f'<span class="who">{esc(e.get("date", ""))}</span></div>')
    out.append("</div>")
    return "".join(out)


def render_log() -> str:
    entries = pm_state.tail_jsonl(pm_state.ACTIVITY_LOG, 30)
    if not entries:
        return ""
    lis = "".join(f'<li>{esc(e.get("ts", "")[:16].replace("T", " "))} · {esc(e.get("action"))} — {esc(e.get("detail"))}</li>'
                  for e in entries)
    return f'<div class="panel"><h2>Activity</h2><ul class="log">{lis}</ul></div>'


def render_project(key: str, s: dict) -> str:
    issue = (s.get("drawing_stage") or {}).get("latest_issue") or {}
    prog = s.get("program", {})
    cost = s.get("cost", {})
    regs = s.get("artifacts", {}).get("registers", [])
    discs = issue.get("disciplines_detected")
    notes = "".join(f'<li>{esc(n)}</li>' for n in s.get("standing_notes", []))
    facts = f"""<div class="panel"><div class="grid2">
<div><h2>Drawings</h2><ul class="kv">
<li><b>{esc(issue.get("set_file", "no set found"))}</b></li>
<li>{esc(issue.get("stage_folder", "-"))} · rev {esc(issue.get("revision") or "?")} · issued {esc(issue.get("issue_date", "-"))}</li>
<li>Disciplines: {esc(", ".join(discs) if discs else "not verified")}</li>
<li>Register baseline: {esc(regs[-1]["name"] if regs else "none")}</li></ul>
<h2 style="margin-top:14px">Programme</h2><ul class="kv">
<li>{esc(milestone())}: <b>{esc(prog.get("confirmed_date") or prog.get("governing_date") or "unconfirmed")}</b></li>
<li>{esc((prog.get("latest") or {}).get("name", "-"))}</li></ul></div>
<div><h2>Cost</h2><ul class="kv">
<li>{cost_line(cost)}</li>
<li>Contract sum: {money(cost.get("contract_sum")) if cost.get("contract_sum") else "pre-award"}</li>
<li>{cost.get("purchase_orders", 0)} POs · {cost.get("invoices", 0)} invoices · {cost.get("quotes", 0)} quotes</li></ul>
{"<h2 style='margin-top:14px'>Standing instructions</h2><ul class='kv'>" + notes + "</ul>" if notes else ""}</div>
</div></div>"""
    return facts


def build_html() -> str:
    global _CFG
    _CFG = None  # re-read config on every render; the server calls this per page load
    proj = project.current()
    state = pm_state.load_state()
    stores = {k: v for k, v in state.get("projects", {}).items() if k == proj.id}
    gen = esc((state.get("generated_at") or "")[:16].replace("T", " "))

    if stores:
        key, s = next(iter(stores.items()))
        issue = (s.get("drawing_stage") or {}).get("latest_issue") or {}
        prog = s.get("program", {})
        sub = (f"Generated {gen} · {esc((s.get('drawing_stage') or {}).get('current') or '?')} stage · "
               f"rev {esc(issue.get('revision') or '?')} · {esc(milestone().lower())} "
               f"{esc(prog.get('confirmed_date') or prog.get('governing_date') or 'TBC')}")
        facts = render_project(key, s)
    else:
        sub = "Not scanned yet - run scan_state.py or press Rescan."
        facts = ""
    title = f"{esc(proj.name)} — PM dashboard"

    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{CSS}</style></head><body>
<h1>{title} <button id="rescan" style="float:right;font-weight:400">Rescan</button></h1>
<p class="sub">{sub}</p>
{render_matrix(stores)}
{render_waiting(stores)}
<div class="panel" id="chatpanel" style="display:none">
<h2>Chat with the PM</h2>
<div id="chatlog"></div>
<div class="ansrow"><input id="chatin" class="ans" placeholder="Ask the PM anything — reports, status, chasing, next steps…"><button id="chatsend">Send</button></div>
</div>
{facts}
{render_emails()}
{render_log()}
<footer>PM agent · state: {esc(str(pm_state.STATE_PATH))}</footer>
<script>{JS}</script></body></html>"""
    return pm_state.display_dates(body)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="registered project id (default: PM_PROJECT, or the only one)")
    ap.add_argument("--out", help="default: <state folder>/dashboard.html")
    args = ap.parse_args()
    project.select(args.project)
    out = guard.check(args.out or pm_state.PM_DIR / "dashboard.html", "write")
    body = build_html()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(body, encoding="utf-8")
    os.replace(tmp, out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
