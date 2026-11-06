"""Gemeinsame Einstellungen aus einstellungen.json (wird bei der Einrichtung erstellt)."""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def laden():
    p = ROOT / "einstellungen.json"
    if not p.exists():
        sys.exit("einstellungen.json fehlt. Erst die Einrichtung machen (in Claude Code: /einrichtung).")
    e = json.loads(p.read_text(encoding="utf-8"))
    e["unterlagen_ordner"] = pathlib.Path(e["unterlagen_ordner"]).expanduser()
    return e
