import sys, pathlib, unittest, tempfile, shutil, subprocess, json

ROOT = pathlib.Path(__file__).resolve().parent.parent


@unittest.skipUnless(shutil.which("tectonic"), "tectonic fehlt")
class Uebersicht(unittest.TestCase):
    def test_cv_pane_mit_und_ohne_cv_pdf(self):
        t = pathlib.Path(tempfile.mkdtemp())
        try:
            shutil.copy(ROOT / "generate_overview.py", t)
            for o in ("mit", "ohne"):
                (t / "bewerbungen" / o).mkdir(parents=True)
            sys.path.insert(0, str(ROOT / "tools"))
            tex = t / "bewerbungen/mit/cv.tex"
            tex.write_text("\\documentclass{article}\\begin{document}Mein Spezial-CV\\end{document}")
            subprocess.run(["tectonic", "-o", str(tex.parent), str(tex)], check=True, capture_output=True)
            e = lambda f, o: {"datum": "2026-11-24", "firma": f, "stelle": "S", "art": "Werkstudent",
                              "status": "in Prüfung", "update": "2026-11-24", "notiz": "", "ordner": o}
            (t / "bewerbungen.json").write_text(json.dumps([e("A", "mit"), e("B", "ohne")]))
            subprocess.run([sys.executable, "generate_overview.py"], cwd=t, check=True, capture_output=True)
            h = (t / "uebersicht.html").read_text(encoding="utf-8")
            self.assertIn("Mein Spezial-CV", h)
            self.assertIn("Standard-Lebenslauf (nicht auf die Stelle angepasst)", h)
        finally:
            shutil.rmtree(t, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
