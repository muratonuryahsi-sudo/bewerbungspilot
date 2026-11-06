#!/usr/bin/env python3
"""Anschreiben bauen: tools/anschreiben.py <spec.json>
spec: {"dir": "2026-10-29_firma_stelle", "pdf": "Anschreiben_Firma_Stelle.pdf", "lang": "de"|"en",
       "firma": "...", "adresse": "Zeile1\\\\Zeile2", "betreff": "...", "anrede": "...", "text": "Absatz\n\nAbsatz"}
LaTeX-Sonderzeichen (&, %) im Text selbst escapen. Baut mit tectonic, prüft 1 Seite und keine /URI /Annots /OpenAction,
legt .tex+PDF in bewerbungen/<dir>/ und das PDF oben in den Unterlagen-Ordner.
"""
import json, sys, subprocess, shutil, pathlib, datetime
from einstellungen import laden, ROOT

E = laden()
s = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
de = s.get("lang", "de") == "de"
M = ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]
t = datetime.date.today()
datum = f"{t.day}. {M[t.month-1]} {t.year}" if de else t.strftime("%-d %B %Y")
tex = (ROOT / "vorlagen/anschreiben.tex").read_text(encoding="utf-8").split("\n", 1)[1]
for k, v in dict(LANG="ngerman" if de else "english", NAME=E["name"], ADRESSZEILE=f'{E["strasse"]}, {E["plz_ort"]}',
                 KONTAKT=f'{E["telefon"]} $|$ {E["email"]}', ORT=E["ort"], FIRMA=s["firma"], ADRESSE=s["adresse"],
                 DATUM=datum, BETREFF=s["betreff"], ANREDE=s["anrede"], TEXT=s["text"],
                 GRUSS="Mit freundlichen Grüßen" if de else "Kind regards").items():
    tex = tex.replace(f"<<{k}>>", v)
d = ROOT / "bewerbungen" / s["dir"]; d.mkdir(parents=True, exist_ok=True)
(d / "anschreiben.tex").write_text(tex, encoding="utf-8")
r = subprocess.run(["tectonic", "-o", str(d), str(d / "anschreiben.tex")], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[-800:]
pdf = d / "anschreiben.pdf"; raw = pdf.read_bytes()
pages = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
np = next(l.split()[-1] for l in pages.splitlines() if l.startswith("Pages"))
bad = [k.decode() for k in (b"/URI", b"/Annots", b"/OpenAction") if k in raw]
assert np == "1" and not bad, f"Seiten={np} aktiv={bad}"
shutil.copy(pdf, E["unterlagen_ordner"] / s["pdf"])
print(f"ok {s['pdf']} | 1 Seite | {len(s['text'].split())} Wörter")
