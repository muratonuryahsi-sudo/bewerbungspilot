#!/usr/bin/env python3
"""Tracker pflegen + Übersicht neu erzeugen.
  track.py set "<firma>" "<stelle-teil>" <status> ["notiz"]   # vorhandenen Eintrag ändern (update=heute)
  track.py add "<firma>" "<stelle>" <art> <status> ["notiz"] ["ordner"]  # neuen Eintrag; ordner = bewerbungen/<ordner> für Detailansicht
  track.py rm "<firma>" "<stelle-teil>"
"""
import json, sys, subprocess, datetime, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "bewerbungen.json"
d = json.loads(P.read_text(encoding="utf-8")) if P.exists() else []
today = datetime.date.today().isoformat()
cmd, firma, stelle, *rest = sys.argv[1:]
hit = lambda e: e["firma"] == firma and stelle.lower() in e["stelle"].lower()
if cmd == "add":
    art, status, *n = rest
    e = dict(datum=today, firma=firma, stelle=stelle, art=art, status=status, update=today, notiz=n[0] if n else "")
    if len(n) > 1: e["ordner"] = n[1]
    d.append(e)
elif cmd == "set":
    status, *n = rest
    m = [e for e in d if hit(e)]
    assert len(m) == 1, f"{len(m)} Treffer"
    m[0].update(status=status, update=today, **({"notiz": n[0]} if n else {}))
elif cmd == "rm":
    m = [e for e in d if hit(e)]
    assert len(m) == 1, f"{len(m)} Treffer"
    d.remove(m[0])
P.write_text("[\n" + ",\n".join(" " + json.dumps(e, ensure_ascii=False, separators=(",", ":")) for e in d) + "\n]\n", encoding="utf-8")
subprocess.run([sys.executable, str(ROOT / "generate_overview.py")], check=True)
