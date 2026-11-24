import sys, pathlib, unittest, json, shutil, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import anschreiben as A
import anschreiben_lint as L

SATZ = "Ich teste Software in Jira und vergleiche Daten in Excel. "
GUT = "\n\n".join([
    "wenn es darum geht, Firmware sauber zu testen, bringe ich Praxis aus meiner Werkstudententätigkeit mit. " * 2,
    "Bei der Firma Beispiel plane ich Tests und dokumentiere die Ergebnisse. Parallel habe ich ein Hochschulprojekt "
    "mit Python umgesetzt. " * 2,
    "An der Beispiel GmbH reizt mich die Nähe zwischen Test und Entwicklung. " * 2,
    "Ich kann ab dem 1. Februar 2027 mit 20 Stunden pro Woche starten. Auf ein Gespräch freue ich mich.",
])


def lint(text, **kw):
    kw.setdefault("firma", "Beispiel GmbH")
    return L.pruefe(text, **kw)


class Lint(unittest.TestCase):
    def test_guter_text_ohne_fehler(self):
        f, w = lint(GUT)
        self.assertEqual(f, [])

    def test_floskel_ist_fehler(self):
        f, _ = lint("Hiermit bewerbe ich mich als Werkstudent. " + GUT)
        self.assertTrue(any("hiermit bewerbe" in x for x in f))
        f, _ = lint(GUT + " Über eine Einladung würde ich mich sehr freuen.")
        self.assertTrue(any("freuen" in x for x in f))

    def test_im_rahmen_nur_als_einstieg(self):
        f, _ = lint("Im Rahmen meines Studiums teste ich. " + GUT)
        self.assertTrue(any("Im Rahmen" in x for x in f))

    def test_em_dash_und_gedankenstrich(self):
        self.assertTrue(lint("Das ist gut — wirklich. " + GUT)[0])
        self.assertTrue(lint("Das ist gut – wirklich. " + GUT)[0])
        self.assertEqual(lint("Das sind 15–20 Stunden. " + GUT)[0], [])

    def test_doppelpunkt_ausser_uhrzeit(self):
        self.assertTrue(any("Doppelpunkt" in x for x in lint("Ich kann: starten. " + GUT)[0]))
        self.assertEqual(lint("Gespräch ab 10:30 Uhr möglich. " + GUT)[0], [])

    def test_platzhalter(self):
        for p in ("TODO", "[Firma]", "<<TEXT>>"):
            self.assertTrue(any("Platzhalter" in x for x in lint(p + " " + GUT)[0]), p)

    def test_wortzahl(self):
        lang = ("wort " * 301).strip()
        self.assertTrue(any("Maximum 300" in x for x in lint(lang)[0]))
        _, w = lint("Kurz. Beispiel GmbH.")
        self.assertTrue(any("Ziel 180" in x for x in w))

    def test_ki_tells_sind_nur_warnung(self):
        f, w = lint("Ich bin leidenschaftlich und versiert. " + GUT)
        self.assertEqual(f, [])
        self.assertTrue(any("leidenschaftlich" in x for x in w))

    def test_englisch_nutzt_englische_listen(self):
        f, _ = lint("I am writing to express my interest. We delve into tests.", lang="en", firma="")
        self.assertTrue(f)
        f, w = lint("I test software.", lang="de", firma="")
        self.assertEqual(f, [])

    def test_ich_anapher(self):
        _, w = lint("Ich teste. Ich plane. " + GUT)
        self.assertTrue(any("'Ich'" in x for x in w))

    def test_absatz_zu_lang(self):
        _, w = lint(("wort " * 120) + "\n\nkurz\n\nkurz\n\nkurz")
        self.assertTrue(any("Textwüste" in x for x in w))

    def test_firma_ohne_rechtsform(self):
        self.assertEqual(L.firmenkern("Beispiel GmbH"), "beispiel")
        for firma, text in [("SAP SE", "Bei SAP arbeite ich gern."), ("Muster AG", "Die Muster stellt ein."),
                            ("Foo Bar KG", "Foo Bar sucht."), ("Acme Ltd.", "Acme ist toll."),
                            ("Test mbH", "Test passt."), ("1&1 Telecommunication SE", "Bei 1&1 teste ich.")]:
            _, w = L.pruefe("Text " + text, firma=firma)
            self.assertFalse(any("kommt im Text nicht vor" in x for x in w), firma)
        _, w = L.pruefe("Text ohne Namen.", firma="Beispiel GmbH")
        self.assertTrue(any("kommt im Text nicht vor" in x for x in w))

    def test_zahlen_gegen_profil_und_anzeige(self):
        profil = "Ich habe 25 % schneller getestet."
        _, w = L.pruefe("Das war 25 % schneller und 40 % besser. Beispiel.", firma="Beispiel", profil=profil)
        self.assertTrue(any("40" in x and "25" not in x for x in w))
        _, w = L.pruefe("Ich arbeite 15 Stunden.", firma="", profil=profil, anzeige="15 bis 20 Stunden")
        self.assertFalse(any("Zahlen" in x for x in w))

    def test_daten_und_uhrzeiten_loesen_keine_zahlenwarnung_aus(self):
        text = ("Ab dem 1. Februar 2027 und bis 31.07.2027, 24 November 2026, "
                "Gespräch um 10:30 Uhr, im Jahr 2026. Beispiel.")
        _, w = L.pruefe(text, firma="Beispiel", profil="Nur 25 hier.")
        self.assertFalse(any("Zahlen" in x for x in w), w)


class Escape(unittest.TestCase):
    def test_idempotent(self):
        self.assertEqual(A.latex_escape("Q & A"), "Q \\& A")
        self.assertEqual(A.latex_escape("Q \\& A"), "Q \\& A")
        for s in ("1&1 und 50 % mehr", "1\\&1 und 50 \\% mehr", "a_b #1 $5"):
            einmal = A.latex_escape(s)
            self.assertEqual(A.latex_escape(einmal), einmal)
        self.assertEqual(A.latex_escape("1&1"), A.latex_escape("1\\&1"))
        self.assertEqual(A.latex_escape("1&1"), "1\\&1")

    def test_zeilenumbruch_bleibt(self):
        self.assertEqual(A.latex_escape("Zeile1\\\\Zeile2 & Co"), "Zeile1\\\\Zeile2 \\& Co")

    def test_entescape(self):
        self.assertEqual(A.entescape("a \\& b \\% c"), "a & b % c")


@unittest.skipUnless(shutil.which("tectonic") and shutil.which("pdfinfo"), "tectonic/pdfinfo fehlt")
class Bauen(unittest.TestCase):
    def setUp(self):
        self.t = pathlib.Path(tempfile.mkdtemp())
        (self.t / "vorlagen").mkdir()
        shutil.copy(ROOT / "vorlagen/anschreiben.tex", self.t / "vorlagen")
        (self.t / "unterlagen").mkdir()
        self.E = {"name": "Erika Muster", "strasse": "Weg 1", "plz_ort": "12345 Ort", "telefon": "+49 1",
                  "email": "e@example.org", "ort": "Ort", "unterlagen_ordner": self.t / "unterlagen"}
        self.spec = {"dir": "2026-01-01_beispiel_stelle", "pdf": "Anschreiben_Beispiel.pdf", "lang": "de",
                     "firma": "Beispiel GmbH", "adresse": "Beispiel GmbH\\\\Weg 2\\\\54321 Stadt",
                     "betreff": "Bewerbung als Werkstudent Q&A", "kennziffer": "R-42",
                     "anrede": "Sehr geehrte Damen und Herren,", "text": GUT + " Wir testen bei 1&1."}

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def test_baut_pdf_mit_kennziffer_und_escape(self):
        pdf, f, w = A.bauen(self.spec, self.E, self.t)
        self.assertEqual(f, [])
        self.assertTrue(pdf.exists())
        self.assertTrue((self.t / "unterlagen/Anschreiben_Beispiel.pdf").exists())
        tex = (self.t / "bewerbungen" / self.spec["dir"] / "anschreiben.tex").read_text(encoding="utf-8")
        self.assertIn("Q\\&A (Ref. R-42)", tex)
        self.assertIn("1\\&1", tex)

    def test_fehler_stoppt_bau_force_baut(self):
        self.spec["text"] = "Hiermit bewerbe ich mich. " + GUT
        pdf, f, _ = A.bauen(self.spec, self.E, self.t)
        self.assertIsNone(pdf)
        self.assertTrue(f)
        pdf, f, _ = A.bauen(self.spec, self.E, self.t, force=True)
        self.assertTrue(pdf.exists())


if __name__ == "__main__":
    unittest.main()
