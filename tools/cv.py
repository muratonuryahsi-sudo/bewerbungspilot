#!/usr/bin/env python3
"""CV pro Stelle bauen: tools/cv.py <spec.json>
spec: {"dir": "2026-11-24_firma_stelle", "lang": "de"|"en", "links": false, "fokus": ["qa", "automatisierung"]}
Optional: "projekte": [ids], "skills": [ids] (schränkt die Auswahl ein).
Wählt aus cv_daten.json nur vorformulierte, wahre Varianten nach Fokus-Tags, baut 1 Seite (tectonic),
legt .tex+PDF in bewerbungen/<dir>/ und eine Kopie im CV-Ordner (einstellungen.json "cv_ordner").
"""
import json, sys, subprocess, shutil, pathlib, tempfile

SEKTIONEN = ("ausbildung", "erfahrung", "projekte")


class CvFehler(Exception):
    pass


def punkte(tags, fokus):
    """Anzahl gemeinsamer Tags."""
    return len(set(tags) & set(fokus))


def _variante(gruppe, fokus):
    """Variante mit den meisten Fokus-Treffern, bei 0 die erste neutrale, sonst die erste."""
    best = max(gruppe, key=lambda p: punkte(p["tags"], fokus))  # max nimmt bei Gleichstand die erste
    if punkte(best["tags"], fokus) > 0:
        return best
    return next((p for p in gruppe if "neutral" in p["tags"]), gruppe[0])


def _text(obj, lang, id):
    if not obj.get(lang):
        raise CvFehler(f"'{id}' hat keinen Text für Sprache '{lang}'")
    return obj[lang]


def _ausgabe(arbeit, skills, sprachen):
    out = {s: [{"id": it["id"], "kopf": it["kopf"], "punkte": [g["text"] for g in it["gruppen"]]}
               for it in arbeit[s]] for s in SEKTIONEN}
    out["skills"] = [s["text"] for s in skills]
    out["sprachen"] = sprachen
    return out


def waehle(daten, fokus, lang, ist_eine_seite):
    erlaubt = daten["tags"]
    falsch = [t for t in fokus if t not in erlaubt]
    if falsch:
        raise CvFehler(f"Unbekannte Fokus-Tags {falsch}. Erlaubt: {', '.join(erlaubt)}")
    arbeit = {}
    for s in SEKTIONEN:
        items = []
        for it in daten[s]:
            kopf = _text(it["kopf"], lang, it["id"])
            gruppen = []
            for g in it["gruppen"]:
                p = _variante(g, fokus)
                gruppen.append({"text": _text(p, lang, it["id"]), "score": punkte(p["tags"], fokus)})
            gruppen = [g for _, g in sorted(enumerate(gruppen), key=lambda x: (-x[1]["score"], x[0]))]
            items.append({"id": it["id"], "tags": it["tags"], "pflicht": it.get("pflicht", False),
                          "kopf": kopf, "gruppen": gruppen})
        if s == "projekte":
            items = [it for _, it in sorted(enumerate(items), key=lambda x: (-punkte(x[1]["tags"], fokus), x[0]))]
        arbeit[s] = items
    skills = [{"text": _text(sk, lang, sk["id"]), "score": punkte(sk["tags"], fokus), "i": i}
              for i, sk in enumerate(daten["skills"])]
    skills.sort(key=lambda x: (-x["score"], x["i"]))
    sprachen = _text(daten["sprachen"], lang, "sprachen")
    while not ist_eine_seite(_ausgabe(arbeit, skills, sprachen)):
        kand = [(punkte(it["tags"], fokus) + g["score"], (si, ii, gi))
                for si, s in enumerate(SEKTIONEN) for ii, it in enumerate(arbeit[s]) if not it["pflicht"]
                for gi, g in enumerate(it["gruppen"])]
        if not kand:
            raise CvFehler("Passt nicht auf eine Seite, nichts mehr zu kürzen. Mehr Pflicht-Einträge entfernen oder Texte kürzen.")
        _, (si, ii, gi) = min(kand, key=lambda k: (k[0], tuple(-x for x in k[1])))
        it = arbeit[SEKTIONEN[si]][ii]
        del it["gruppen"][gi]
        if not it["gruppen"]:
            del arbeit[SEKTIONEN[si]][ii]
    return _ausgabe(arbeit, skills, sprachen)


# ---------- Rendern ----------
TITEL = {"de": ["Akademischer Werdegang", "Berufserfahrung", "Projekte", "Skills, Sprachen \\& Tools"],
         "en": ["Education", "Professional Experience", "Projects", "Skills, Languages \\& Tools"]}


def latex_escape(s):
    for a, b in (("&", "\\&"), ("%", "\\%"), ("$", "\\$"), ("#", "\\#"), ("_", "\\_")):
        s = s.replace(a, b)
    return s


def _fmt(s):
    """Escapen und **fett** in \\textbf umsetzen."""
    import re
    return re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", latex_escape(s))


def _zeile(s):
    """'Titel (Stufe): a, b' mit fettem Teil vor dem ersten ': '."""
    k, _, rest = s.partition(": ")
    return f"\\textbf{{{_fmt(k)}:}} {_fmt(rest)}" if rest else _fmt(s)


def _liste(punkte_):
    if not punkte_:
        return ""
    return "\\begin{itemize}\n" + "\n".join(f"  \\item {_fmt(p)}" for p in punkte_) + "\n\\end{itemize}\n"


def _kopf(sektion, k):
    if sektion == "projekte":
        z = f"\\textbf{{{_fmt(k[0])}}}" + (f"\\hfill\\textit{{{_fmt(k[1])}}}" if len(k) > 1 and k[1] else "")
        if len(k) > 2 and k[2]:
            z += f"\\\\\n\\textit{{{_fmt(k[2])}}}"
        return z + "\n"
    a, b, c, d = (_fmt(x) for x in k)
    return f"\\entry{{{a}}}{{{b}}}{{{c}}}{{{d}}}\n"


def rendere(auswahl, E, lang, links, vorlage):
    zeilen = [_fmt(f'{E["strasse"]}, {E["plz_ort"]}'), f'{_fmt(E["telefon"])} $|$ {_fmt(E["email"])}']
    gh, li = E.get("github", ""), E.get("linkedin", "")
    if links:
        teile = ([f"\\href{{https://github.com/{gh}}}{{\\underline{{GitHub}}}}"] if gh else []) + \
                ([f"\\href{{https://www.linkedin.com/in/{li}}}{{\\underline{{LinkedIn}}}}"] if li else [])
    else:
        teile = ([f"github.com/{_fmt(gh)}"] if gh else []) + ([f"linkedin.com/in/{_fmt(li)}"] if li else [])
    if teile:
        zeilen.append(" $|$ ".join(teile))
    kontakt = "\\\\\n  ".join(zeilen)
    koerper = ""
    for sek, titel in zip(SEKTIONEN, TITEL[lang]):
        if not auswahl[sek]:
            continue
        koerper += f"\\section{{{titel}}}\n"
        blocks = [_kopf(sek, it["kopf"]) + _liste(it["punkte"]) for it in auswahl[sek]]
        koerper += "\\vspace{3pt}\n".join(blocks) + "\n"
    koerper += f"\\section{{{TITEL[lang][3]}}}\n" + "\\\\\n".join(_zeile(s) for s in [*auswahl["skills"], auswahl["sprachen"]]) + "\n"
    pre = "\\usepackage[hidelinks,pdfstartview={}]{hyperref}" if links else ""
    return (vorlage.replace("<<PREAMBEL_LINKS>>", pre).replace("<<NAME>>", _fmt(E["name"]))
            .replace("<<KONTAKT>>", kontakt).replace("<<KOERPER>>", koerper))


# ---------- Bauen ----------
def _seiten(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    return int(next(l.split()[-1] for l in out.splitlines() if l.startswith("Pages")))


def _tectonic(tex_pfad):
    r = subprocess.run(["tectonic", "-o", str(tex_pfad.parent), str(tex_pfad)], capture_output=True, text=True)
    if r.returncode != 0:
        raise CvFehler("tectonic: " + r.stderr[-800:])
    return tex_pfad.with_suffix(".pdf")


def bauen(spec, E, root):
    """Baut bewerbungen/<dir>/cv.tex + cv.pdf, prüft 1 Seite und aktive Inhalte, kopiert ins CV-Ordner. Gibt Pfad zurück."""
    root = pathlib.Path(root)
    lang, links = spec.get("lang", "de"), bool(spec.get("links", False))
    daten = json.loads((root / "cv_daten.json").read_text(encoding="utf-8"))
    if spec.get("projekte"):
        byid = {p["id"]: p for p in daten["projekte"]}
        daten["projekte"] = [byid[i] for i in spec["projekte"]]
    if spec.get("skills"):
        byid = {s["id"]: s for s in daten["skills"]}
        daten["skills"] = [byid[i] for i in spec["skills"]]
    vorlage = (root / "vorlagen/cv.tex").read_text(encoding="utf-8")

    def passt(auswahl):
        with tempfile.TemporaryDirectory() as t:
            tex = pathlib.Path(t) / "cv.tex"
            tex.write_text(rendere(auswahl, E, lang, links, vorlage), encoding="utf-8")
            return _seiten(_tectonic(tex)) == 1

    auswahl = waehle(daten, spec.get("fokus", []), lang, passt)
    d = root / "bewerbungen" / spec["dir"]
    d.mkdir(parents=True, exist_ok=True)
    tex = d / "cv.tex"
    tex.write_text(rendere(auswahl, E, lang, links, vorlage), encoding="utf-8")
    pdf = _tectonic(tex)
    raw = pdf.read_bytes()
    bad = [k.decode() for k in (b"/URI", b"/Annots", b"/OpenAction") if k in raw] if not links else []
    if _seiten(pdf) != 1 or bad:
        raise CvFehler(f"Seiten={_seiten(pdf)} aktiv={bad}")
    ziel_ordner = pathlib.Path(E.get("cv_ordner") or pathlib.Path(E["unterlagen_ordner"]) / "CV_pro_Stelle").expanduser()
    name = E.get("lebenslauf", "Lebenslauf.pdf") if lang == "de" else E.get("cv_en", "CV.pdf")
    ziel = ziel_ordner / spec["dir"] / name
    ziel.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(pdf, ziel)
    return pdf


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from einstellungen import laden, ROOT
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    try:
        pdf = bauen(spec, laden(), ROOT)
    except CvFehler as e:
        sys.exit(f"Fehler: {e}")
    print(f"ok {pdf.relative_to(ROOT)} | 1 Seite | Fokus: {', '.join(spec.get('fokus', [])) or '-'}")
