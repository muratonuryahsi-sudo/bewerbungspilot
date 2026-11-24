#!/usr/bin/env python3
"""Anschreiben bauen: tools/anschreiben.py <spec.json> [--force]
spec (bewerbungen/<dir>/anschreiben_spec.json):
  {"dir": "2026-10-29_firma_stelle", "pdf": "Anschreiben_Firma_Stelle.pdf", "lang": "de"|"en",
   "firma": "...", "adresse": "Zeile1\\\\Zeile2", "betreff": "...", "kennziffer": "optional",
   "anrede": "...", "text": "Absatz\\n\\nAbsatz"}
LaTeX-Sonderzeichen (& % # _ $) werden automatisch escaped, schon escapte (\\&) bleiben unverändert.
Prüft den Text vorher (tools/anschreiben_lint.py, Regeln in docs/anschreiben_regeln.md). Fehler brechen ab,
mit --force wird trotzdem gebaut. Baut mit tectonic, prüft 1 Seite und keine /URI /Annots /OpenAction,
legt .tex+PDF in bewerbungen/<dir>/ und das PDF oben in den Unterlagen-Ordner.
"""
import json, re, sys, subprocess, shutil, pathlib, datetime
from anschreiben_lint import pruefe

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
          "November", "Dezember"]


def entescape(s):
    """\\& \\% \\# \\_ \\$ zurück zu & % # _ $ (ein vorangestelltes \\\\ für Zeilenumbruch bleibt)."""
    return re.sub(r"(?<!\\)\\([&%#_$])", r"\1", s)


def latex_escape(s):
    """Idempotent: & und \\& ergeben beide \\&."""
    return re.sub(r"([&%#_$])", r"\\\1", entescape(s))


def datum_text(de, heute=None):
    t = heute or datetime.date.today()
    return f"{t.day}. {MONATE[t.month - 1]} {t.year}" if de else t.strftime("%-d %B %Y")


def baue_tex(s, E, vorlage, heute=None):
    de = s.get("lang", "de") == "de"
    betreff = s["betreff"]
    kz = s.get("kennziffer")
    if kz and kz not in betreff:
        betreff += f" (Ref. {kz})"
    tex = vorlage.split("\n", 1)[1]
    werte = dict(LANG="ngerman" if de else "english", NAME=latex_escape(E["name"]),
                 ADRESSZEILE=latex_escape(f'{E["strasse"]}, {E["plz_ort"]}'),
                 KONTAKT=f'{latex_escape(E["telefon"])} $|$ {latex_escape(E["email"])}', ORT=latex_escape(E["ort"]),
                 FIRMA=latex_escape(s["firma"]), ADRESSE=latex_escape(s["adresse"]), DATUM=datum_text(de, heute),
                 BETREFF=latex_escape(betreff), ANREDE=latex_escape(s["anrede"]), TEXT=latex_escape(s["text"]),
                 GRUSS="Mit freundlichen Grüßen" if de else "Kind regards")
    for k, v in werte.items():
        tex = tex.replace(f"<<{k}>>", v)
    return tex


def lese(p):
    p = pathlib.Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def bauen(s, E, root, force=False):
    """Gibt (pdf, fehler, warnungen) zurück. Bei Fehlern ohne force wird nicht gebaut (pdf=None)."""
    root = pathlib.Path(root)
    fehler, warn = pruefe(entescape(s["text"]), s["firma"], s.get("lang", "de"), lese(root / "profil.md"),
                          lese(root / "bewerbungen" / s["dir"] / "stellenanzeige.md"))
    if fehler and not force:
        return None, fehler, warn
    tex = baue_tex(s, E, (root / "vorlagen/anschreiben.tex").read_text(encoding="utf-8"))
    d = root / "bewerbungen" / s["dir"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "anschreiben.tex").write_text(tex, encoding="utf-8")
    r = subprocess.run(["tectonic", "-o", str(d), str(d / "anschreiben.tex")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-800:]
    pdf = d / "anschreiben.pdf"
    raw = pdf.read_bytes()
    pages = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    n = next(l.split()[-1] for l in pages.splitlines() if l.startswith("Pages"))
    bad = [k.decode() for k in (b"/URI", b"/Annots", b"/OpenAction") if k in raw]
    assert n == "1" and not bad, f"Seiten={n} aktiv={bad}"
    shutil.copy(pdf, pathlib.Path(E["unterlagen_ordner"]) / s["pdf"])
    return pdf, fehler, warn


if __name__ == "__main__":
    from einstellungen import laden, ROOT
    args = [a for a in sys.argv[1:] if a != "--force"]
    spec = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    pdf, fehler, warn = bauen(spec, laden(), ROOT, force="--force" in sys.argv)
    for x in warn:
        print("Warnung:", x)
    for x in fehler:
        print("FEHLER:", x)
    if pdf is None:
        sys.exit("Nicht gebaut. Text korrigieren (oder mit --force bauen).")
    print(f"ok {spec['pdf']} | 1 Seite | {len(spec['text'].split())} Wörter")
