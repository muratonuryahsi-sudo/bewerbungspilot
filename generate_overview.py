#!/usr/bin/env python3
"""Erzeugt uebersicht.html und bewerbungen.md aus bewerbungen.json."""
import json, html, datetime, pathlib, re
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent
P = ROOT / "bewerbungen.json"
data = json.loads(P.read_text(encoding="utf-8")) if P.exists() else []
E = ROOT / "einstellungen.json"
NAME = json.loads(E.read_text(encoding="utf-8")).get("name", "") if E.exists() else ""
data.sort(key=lambda d: d["datum"], reverse=True)

ORDER = ["in Prüfung", "Gespräch", "Zusage", "geplant", "unklar", "keine Antwort", "nicht abgeschlossen", "Absage"]
CLS = {"in Prüfung": "open", "Gespräch": "open", "Zusage": "ok", "geplant": "plan",
       "unklar": "plan", "keine Antwort": "muted", "nicht abgeschlossen": "muted", "Absage": "no"}

def fmt(d):
    if not d: return "–"
    try: return datetime.date.fromisoformat(d).strftime("%d.%m.%Y")
    except ValueError: return d

count = lambda s: sum(1 for d in data if d["status"] == s)
sent = [d for d in data if d["status"] not in ("geplant", "nicht abgeschlossen")]
stats = [("Beworben", len(sent)), ("In Prüfung", count("in Prüfung") + count("Gespräch")),
         ("Absagen", count("Absage")), ("Zusagen", count("Zusage")), ("Geplant", count("geplant"))]

DETAIL_STATUS = ("in Prüfung", "Gespräch")

def anschreiben_text(folder):
    """Anschreiben-Text ab der Anrede: aus anschreiben.txt (pdftotext) oder anschreiben.tex."""
    txt, tex = folder / "anschreiben.txt", folder / "anschreiben.tex"
    if txt.exists():
        lines = [l.strip() for l in txt.read_text(encoding="utf-8").splitlines()]
        start = next((i for i, l in enumerate(lines) if l.startswith(("Sehr geehrte", "Dear", "Hallo"))), 0)
        return re.sub(r"\n{3,}", "\n\n", "\n".join(lines[start:])).strip()
    if tex.exists():
        body = tex.read_text(encoding="utf-8").split("\\end{document}")[0]
        blocks = [b.strip() for b in body.split("\n\n")]
        start = next((i for i, b in enumerate(blocks) if b.startswith("\\textbf{")), -1)
        text = "\n\n".join(blocks[start + 1:])
        text = text.replace("\\\\[4pt]", "").replace("\\&", "&").replace("\\%", "%")
        return text.strip()
    return ""

def md_html(md):
    """Kleines Markdown → HTML (Überschriften, Listen, fett) für stellenanzeige.md."""
    out, in_list = [], False
    for line in md.splitlines():
        s = html.escape(line.strip())
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        if s.startswith(("* ", "- ")):
            if not in_list: out.append("<ul>"); in_list = True
            out.append(f"<li>{s[2:]}</li>"); continue
        if in_list: out.append("</ul>"); in_list = False
        if s.startswith("#"):
            out.append(f"<h4>{s.lstrip('#').strip()}</h4>")
        elif s:
            out.append(f"<p>{s}</p>")
    if in_list: out.append("</ul>")
    return "\n".join(out)

def details(d):
    if d["status"] not in DETAIL_STATUS or not d.get("ordner"):
        return ""
    folder = ROOT / "bewerbungen" / d["ordner"]
    ad = folder / "stellenanzeige.md"
    anzeige = md_html(ad.read_text(encoding="utf-8")) if ad.exists() else "<p>Keine Anzeige gespeichert.</p>"
    brief = anschreiben_text(folder)
    brief = f'<div class="letter">{html.escape(brief)}</div>' if brief else "<p>Kein Anschreiben (nicht verlangt).</p>"
    return (f'<details class="more"><summary>Anzeige &amp; Anschreiben</summary>'
            f'<div class="panes"><div class="pane"><h3>Stellenanzeige</h3>{anzeige}</div>'
            f'<div class="pane"><h3>Mein Anschreiben</h3>{brief}</div></div></details>')

def rows(items):
    out = []
    for d in items:
        out.append(
            f'<tr><td class="date">{fmt(d["datum"])}</td>'
            f'<td><div class="co">{html.escape(d["firma"])}</div><div class="role">{html.escape(d["stelle"])}</div>{details(d)}</td>'
            f'<td class="art">{html.escape(d["art"])}</td>'
            f'<td><span class="pill {CLS.get(d["status"],"muted")}">{html.escape(d["status"])}</span></td>'
            f'<td class="date">{fmt(d.get("update",""))}</td>'
            f'<td class="note">{html.escape(d.get("notiz",""))}</td></tr>')
    return "\n".join(out)

active = [d for d in data if d["status"] in ("in Prüfung", "Gespräch", "Zusage", "geplant", "unklar")]
active.sort(key=lambda d: ORDER.index(d["status"]))
closed = [d for d in data if d not in active]

stat_html = "".join(f'<div class="stat"><div class="num">{n}</div><div class="lbl">{l}</div></div>' for l, n in stats)
head = "<tr><th>Datum</th><th>Firma / Stelle</th><th>Art</th><th>Status</th><th>Update</th><th>Notiz</th></tr>"
now = datetime.datetime.now(ZoneInfo("Europe/Berlin")).strftime("%d.%m.%Y, %H:%M")

page = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bewerbungen</title>
<style>
:root {{ --bg:#fbfbfd; --card:#ffffff; --fg:#1d1d1f; --muted:#86868b; --line:#e8e8ed;
  --ok:#1d8a3a; --ok-bg:#e9f6ec; --no:#b3261e; --no-bg:#fbeceb; --open:#0066cc; --open-bg:#e8f1fb; --plan-bg:#f2f2f5; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:15px/1.45 -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif; }}
.wrap {{ max-width:1080px; margin:0 auto; padding:48px 24px 64px; }}
h1 {{ font:600 34px/1.1 -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif; letter-spacing:-.02em; margin:0; }}
.sub {{ color:var(--muted); margin:6px 0 32px; }}
.stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:40px; }}
.stat {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:18px 20px; }}
.num {{ font:600 30px/1 -apple-system, "SF Pro Display", sans-serif; letter-spacing:-.02em; }}
.lbl {{ color:var(--muted); font-size:13px; margin-top:6px; }}
h2 {{ font-size:20px; font-weight:600; margin:0 0 12px; letter-spacing:-.01em; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:16px; overflow-x:auto; margin-bottom:36px; }}
table {{ width:100%; border-collapse:collapse; }}
th {{ text-align:left; font-size:12px; font-weight:500; color:var(--muted); padding:14px 16px; border-bottom:1px solid var(--line); white-space:nowrap; }}
td {{ padding:14px 16px; border-bottom:1px solid var(--line); vertical-align:top; }}
tr:last-child td {{ border-bottom:none; }}
.co {{ font-weight:600; }} .role {{ color:var(--fg); opacity:.8; font-size:14px; }}
.date, .art {{ white-space:nowrap; color:var(--muted); font-variant-numeric:tabular-nums; font-size:14px; }}
.note {{ color:var(--muted); font-size:13px; min-width:160px; }}
.pill {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:12px; font-weight:500; white-space:nowrap; }}
.pill.ok {{ color:var(--ok); background:var(--ok-bg); }} .pill.no {{ color:var(--no); background:var(--no-bg); }}
.pill.open {{ color:var(--open); background:var(--open-bg); }} .pill.plan {{ color:var(--fg); background:var(--plan-bg); }}
.pill.muted {{ color:var(--muted); background:var(--plan-bg); }}
details.more {{ margin-top:8px; }}
details.more summary {{ cursor:pointer; color:var(--open); font-size:13px; list-style:none; }}
details.more summary::-webkit-details-marker {{ display:none; }}
details.more summary::before {{ content:"▸ "; }} details.more[open] summary::before {{ content:"▾ "; }}
.panes {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:12px; min-width:620px; }}
.pane {{ background:var(--bg); border:1px solid var(--line); border-radius:12px; padding:14px 16px; font-size:13px; }}
.pane h3 {{ font-size:14px; margin:0 0 8px; }} .pane h4 {{ font-size:13px; margin:12px 0 4px; }}
.pane p {{ margin:4px 0; }} .pane ul {{ margin:4px 0; padding-left:18px; }}
.letter {{ white-space:pre-wrap; line-height:1.5; }}
@media (max-width:760px) {{ .panes {{ grid-template-columns:1fr; min-width:0; }} }}
</style></head><body><div class="wrap">
<h1>Bewerbungen</h1><p class="sub">{html.escape(NAME)} · Stand {now}</p>
<div class="stats">{stat_html}</div>
<h2>Aktiv</h2><div class="card"><table>{head}{rows(active)}</table></div>
<h2>Abgeschlossen</h2><div class="card"><table>{head}{rows(closed)}</table></div>
</div></body></html>"""
(ROOT / "uebersicht.html").write_text(page, encoding="utf-8")

md = ["# Bewerbungs-Tracker", "", "Automatisch aus bewerbungen.json erzeugt (generate_overview.py). Nicht von Hand bearbeiten.", "",
      "| Datum | Firma | Stelle | Art | Status | Update | Notiz |", "|---|---|---|---|---|---|---|"]
for d in data:
    md.append(f'| {fmt(d["datum"])} | {d["firma"]} | {d["stelle"]} | {d["art"]} | {d["status"]} | {fmt(d.get("update",""))} | {d.get("notiz","")} |')
(ROOT / "bewerbungen.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"{len(data)} Einträge, Übersicht erzeugt")
