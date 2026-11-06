#!/usr/bin/env python3
"""Nach dem Absenden: Anschreiben in <unterlagen>/Anschreiben_gesendet/ verschieben.  gesendet.py <Anschreiben.pdf>"""
import sys, shutil
from einstellungen import laden, ROOT

E = laden(); f = sys.argv[1]
ziel = E["unterlagen_ordner"] / "Anschreiben_gesendet"; ziel.mkdir(exist_ok=True)
shutil.move(E["unterlagen_ordner"] / f, ziel / f)
(ROOT / ".upload" / f).unlink(missing_ok=True)
print(f"ok {f} -> Anschreiben_gesendet/")
