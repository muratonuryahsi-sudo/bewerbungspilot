#!/usr/bin/env python3
"""Upload-Dateien in .upload/ kopieren (Chrome lädt nur aus freigegebenen Ordnern hoch).
  stage.py [Anschreiben.pdf]            -> Lebenslauf + weitere Dokumente + optional Anschreiben
  stage.py --cv <dir> [Anschreiben.pdf] -> wie oben, aber mit dem für die Stelle gebauten CV aus dem CV-Ordner (tools/cv.py)
  stage.py clean                        -> .upload/ löschen
"""
import sys, shutil, pathlib


def cv_pfad(E, cv_dir):
    """Pfad des stellenspezifischen CV (DE oder EN, je nachdem was cv.py gebaut hat)."""
    ordner = pathlib.Path(E.get("cv_ordner") or pathlib.Path(E["unterlagen_ordner"]) / "CV_pro_Stelle").expanduser() / cv_dir
    for name in (E["lebenslauf"], E.get("cv_en", "CV.pdf")):
        if (ordner / name).exists():
            return ordner / name
    sys.exit(f"Kein CV in {ordner}. Erst tools/cv.py ausführen.")


def kopiere(E, U, extra, cv_dir=None):
    U.mkdir(exist_ok=True)
    quellen = [cv_pfad(E, cv_dir) if cv_dir else E["unterlagen_ordner"] / E["lebenslauf"]]
    quellen += [E["unterlagen_ordner"] / f for f in [*E["weitere_dokumente"], *extra]]
    for q in quellen:
        shutil.copy(q, U / q.name)
    return sorted(p.name for p in U.iterdir())


if __name__ == "__main__":
    from einstellungen import laden, ROOT
    U = ROOT / ".upload"
    args = sys.argv[1:]
    if args == ["clean"]:
        shutil.rmtree(U, ignore_errors=True); sys.exit()
    cv_dir = None
    if "--cv" in args:
        i = args.index("--cv"); cv_dir = args[i + 1]; del args[i:i + 2]
    print("\n".join(kopiere(laden(), U, args, cv_dir)))
