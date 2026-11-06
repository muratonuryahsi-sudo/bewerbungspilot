#!/usr/bin/env python3
"""Upload-Dateien in .upload/ kopieren (Chrome lädt nur aus freigegebenen Ordnern hoch).
  stage.py [Anschreiben.pdf]   -> Lebenslauf + weitere Dokumente + optional Anschreiben
  stage.py clean               -> .upload/ löschen
"""
import sys, shutil
from einstellungen import laden, ROOT

U = ROOT / ".upload"
if sys.argv[1:] == ["clean"]:
    shutil.rmtree(U, ignore_errors=True); sys.exit()
E = laden(); U.mkdir(exist_ok=True)
for f in [E["lebenslauf"], *E["weitere_dokumente"], *sys.argv[1:]]:
    shutil.copy(E["unterlagen_ordner"] / f, U / f)
print("\n".join(sorted(p.name for p in U.iterdir())))
