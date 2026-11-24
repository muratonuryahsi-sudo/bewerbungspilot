import sys, pathlib, unittest, json, shutil, tempfile, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
import cv


def P(tags, de, en=None):
    return {"tags": tags, "de": de, "en": en or de + " EN"}


def item(id, tags, gruppen, pflicht=False):
    return {"id": id, "tags": tags, "pflicht": pflicht,
            "kopf": {"de": [id, "Ort", "Titel", "2026"], "en": [id, "Place", "Title", "2026"]}, "gruppen": gruppen}


def daten(**kw):
    d = {"tags": ["qa", "automatisierung", "entwicklung", "neutral"], "ausbildung": [], "erfahrung": [], "projekte": [],
         "skills": [], "sprachen": {"de": "Deutsch", "en": "German"}}
    d.update(kw)
    return d


def immer(_a):
    return True


class Auswahl(unittest.TestCase):
    def test_punkte_schnitt(self):
        self.assertEqual(cv.punkte(["qa", "test"], ["qa", "daten", "test"]), 2)

    def test_variante_mit_bestem_tag_gewinnt(self):
        g = [[P(["neutral"], "allg"), P(["qa"], "qa-text"), P(["automatisierung"], "auto-text")]]
        d = daten(erfahrung=[item("a", [], g)])
        r = cv.waehle(d, ["automatisierung"], "de", immer)
        self.assertEqual(r["erfahrung"][0]["punkte"], ["auto-text"])

    def test_ohne_treffer_nimmt_neutral(self):
        g = [[P(["qa"], "qa-text"), P(["neutral"], "allg")]]
        d = daten(erfahrung=[item("a", [], g)])
        r = cv.waehle(d, ["entwicklung"], "de", immer)
        self.assertEqual(r["erfahrung"][0]["punkte"], ["allg"])

    def test_sprache_en(self):
        d = daten(erfahrung=[item("a", [], [[P(["neutral"], "de-text", "en-text")]])])
        r = cv.waehle(d, [], "en", immer)
        self.assertEqual(r["erfahrung"][0]["punkte"], ["en-text"])
        self.assertEqual(r["erfahrung"][0]["kopf"][1], "Place")

    def test_projekte_nach_punkten_sortiert_stabil(self):
        n = [[P(["neutral"], "x")]]
        d = daten(projekte=[item("p1", ["qa"], n), item("p2", ["automatisierung"], n), item("p3", ["qa"], n)])
        r = cv.waehle(d, ["automatisierung"], "de", immer)
        self.assertEqual([p["id"] for p in r["projekte"]], ["p2", "p1", "p3"])

    def test_bullets_im_item_nach_punkten(self):
        g = [[P(["neutral"], "a")], [P(["automatisierung"], "b")]]
        d = daten(projekte=[item("p", [], g)])
        r = cv.waehle(d, ["automatisierung"], "de", immer)
        self.assertEqual(r["projekte"][0]["punkte"], ["b", "a"])

    def test_pflicht_wird_nie_gekuerzt(self):
        n = [[P(["neutral"], "x")]]
        d = daten(erfahrung=[item("a", [], n, pflicht=True)], projekte=[item("p", [], n)])
        r = cv.waehle(d, [], "de", lambda a: len(a["projekte"]) == 0)
        self.assertEqual(len(r["erfahrung"]), 1)
        self.assertEqual(r["projekte"], [])

    def test_kuerzt_niedrigste_punktzahl_zuerst_bei_gleichstand_spaeteres(self):
        n = [[P(["neutral"], "x")]]
        d = daten(projekte=[item("p1", ["qa"], n), item("p2", [], n), item("p3", [], n)])
        r = cv.waehle(d, ["qa"], "de", lambda a: len(a["projekte"]) <= 2)
        self.assertEqual([p["id"] for p in r["projekte"]], ["p1", "p2"])

    def test_unbekannter_fokus_tag_fehler(self):
        with self.assertRaises(cv.CvFehler) as c:
            cv.waehle(daten(), ["quatsch"], "de", immer)
        self.assertIn("qa", str(c.exception))

    def test_fehlende_sprache_nennt_id(self):
        it = item("projekt_x", [], [[{"tags": ["neutral"], "de": "nur de"}]])
        with self.assertRaises(cv.CvFehler) as c:
            cv.waehle(daten(projekte=[it]), [], "en", immer)
        self.assertIn("projekt_x", str(c.exception))

    def test_nicht_kuerzbar_fehler(self):
        n = [[P(["neutral"], "x")]]
        d = daten(erfahrung=[item("a", [], n, pflicht=True)])
        with self.assertRaises(cv.CvFehler):
            cv.waehle(d, [], "de", lambda a: False)

    def test_skills_nach_punkten(self):
        d = daten(skills=[{"id": "s1", "tags": ["qa"], "de": "Q", "en": "Q"},
                          {"id": "s2", "tags": ["automatisierung"], "de": "A", "en": "A"}])
        r = cv.waehle(d, ["automatisierung"], "de", immer)
        self.assertEqual(r["skills"], ["A", "Q"])


ROOT = pathlib.Path(__file__).resolve().parent.parent
E = {"name": "Erika Mustermann", "strasse": "Musterweg 1", "plz_ort": "12345 Musterstadt", "telefon": "+49 170 0000000",
     "email": "erika_m@example.com", "github": "erika", "linkedin": "erika-m"}


def beispiel_auswahl(lang="de"):
    d = json.loads((ROOT / "vorlagen/cv_daten.beispiel.json").read_text(encoding="utf-8"))
    return cv.waehle(d, ["automatisierung"], lang, immer)


class Rendern(unittest.TestCase):
    vorlage = (ROOT / "vorlagen/cv.tex").read_text(encoding="utf-8")

    def test_escape_sonderzeichen(self):
        self.assertEqual(cv.latex_escape("25 % & A_B"), "25 \\% \\& A\\_B")

    def test_rendere_ohne_links_ohne_href(self):
        t = cv.rendere(beispiel_auswahl(), E, "de", False, self.vorlage)
        self.assertNotIn("\\href", t)
        self.assertNotIn("hyperref", t)
        self.assertIn("github.com/erika", t)
        self.assertIn("erika\\_m@example.com", t)

    def test_rendere_mit_links_hat_href_und_hidelinks(self):
        t = cv.rendere(beispiel_auswahl(), E, "de", True, self.vorlage)
        self.assertIn("\\href{https://github.com/erika}", t)
        self.assertIn("hidelinks", t)

    def test_rendere_en_titel(self):
        t = cv.rendere(beispiel_auswahl("en"), E, "en", False, self.vorlage)
        self.assertIn("\\section{Education}", t)


@unittest.skipUnless(shutil.which("tectonic") and shutil.which("pdfinfo"), "tectonic/pdfinfo fehlt")
class Bauen(unittest.TestCase):
    def setUp(self):
        self.t = pathlib.Path(tempfile.mkdtemp())
        (self.t / "vorlagen").mkdir()
        shutil.copy(ROOT / "vorlagen/cv.tex", self.t / "vorlagen/cv.tex")
        shutil.copy(ROOT / "vorlagen/cv_daten.beispiel.json", self.t / "cv_daten.json")
        self.E = dict(E, unterlagen_ordner=str(self.t / "unterlagen"), cv_ordner=str(self.t / "cvs"))

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def test_bauen_beispiel_eine_seite_ohne_aktive_inhalte(self):
        pdf = cv.bauen({"dir": "x", "lang": "de", "fokus": ["automatisierung"]}, self.E, self.t)
        self.assertTrue(pdf.exists())
        self.assertTrue((self.t / "cvs/x/Lebenslauf.pdf").exists())
        self.assertEqual(cv._seiten(pdf), 1)
        txt = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
        self.assertIn("Rechnungsautomatisierung", txt)

    def test_bauen_en_mit_links(self):
        pdf = cv.bauen({"dir": "y", "lang": "en", "links": True, "fokus": ["qa"]}, self.E, self.t)
        self.assertTrue((self.t / "cvs/y/CV.pdf").exists())
        self.assertEqual(cv._seiten(pdf), 1)


if __name__ == "__main__":
    unittest.main()
