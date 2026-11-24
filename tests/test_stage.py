import sys, pathlib, unittest, tempfile, shutil
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
import stage


class Stage(unittest.TestCase):
    def setUp(self):
        self.t = pathlib.Path(tempfile.mkdtemp())
        u = self.t / "unterlagen"; (u / "cvs/job1").mkdir(parents=True)
        (u / "Lebenslauf.pdf").write_text("standard"); (u / "Noten.pdf").write_text("n")
        (u / "cvs/job1/Lebenslauf.pdf").write_text("angepasst")
        self.E = {"unterlagen_ordner": u, "cv_ordner": str(u / "cvs"), "lebenslauf": "Lebenslauf.pdf",
                  "weitere_dokumente": ["Noten.pdf"]}

    def tearDown(self):
        shutil.rmtree(self.t, ignore_errors=True)

    def test_standard_cv(self):
        U = self.t / ".upload"
        self.assertEqual(stage.kopiere(self.E, U, []), ["Lebenslauf.pdf", "Noten.pdf"])
        self.assertEqual((U / "Lebenslauf.pdf").read_text(), "standard")

    def test_cv_option_nimmt_stellen_cv(self):
        U = self.t / ".upload"
        stage.kopiere(self.E, U, [], "job1")
        self.assertEqual((U / "Lebenslauf.pdf").read_text(), "angepasst")


if __name__ == "__main__":
    unittest.main()
