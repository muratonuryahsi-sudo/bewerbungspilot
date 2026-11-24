#!/usr/bin/env python3
"""CV pro Stelle bauen: tools/cv.py <spec.json>
spec: {"dir": "2026-11-24_firma_stelle", "lang": "de"|"en", "links": false, "fokus": ["qa", "automatisierung"]}
Optional: "projekte": [ids], "skills": [ids] (schränkt die Auswahl ein).
Wählt aus cv_daten.json nur vorformulierte, wahre Varianten nach Fokus-Tags, baut 1 Seite (tectonic),
legt .tex+PDF in bewerbungen/<dir>/ und eine Kopie im CV-Ordner (einstellungen.json "cv_ordner").
"""
import json, re, sys, subprocess, shutil, pathlib, tempfile

SEKTIONEN = ("ausbildung", "erfahrung", "projekte")
ZAHL = re.compile(r"\d+(?:[.,]\d+)?")


class CvFehler(Exception):
    pass


def punkte(tags, fokus):
    """Anzahl gemeinsamer Tags."""
    return len(set(tags) & set(fokus))


def _hat(text, begriff):
    """Begriff als ganzes Wort im Text (ohne Groß-/Kleinschreibung), auch für C++ oder C#."""
    return re.search(r"(?<![\w+#])" + re.escape(begriff) + r"(?![\w+#])", text, re.IGNORECASE) is not None


def _treffer(text, K):
    return len([k for k in K if _hat(text, k)])


def _variante(gruppe, fokus, K, lang):
    """Variante mit den meisten Treffern (Tags + Anzeigen-Begriffe), bei 0 die erste neutrale, sonst die erste."""
    wert = lambda p: punkte(p["tags"], fokus) + _treffer(p.get(lang, ""), K)
    best = max(gruppe, key=wert)  # max nimmt bei Gleichstand die erste
    if wert(best) > 0:
        return best
    return next((p for p in gruppe if "neutral" in p["tags"]), gruppe[0])


def _text(obj, lang, id):
    if not obj.get(lang):
        raise CvFehler(f"'{id}' hat keinen Text für Sprache '{lang}'")
    return obj[lang]


def _zahlen(texte):
    return {z for t in texte for z in ZAHL.findall(t)}


def _alle_texte(obj):
    """Alle Strings in einer Struktur (Items, Varianten, Kopf, beide Sprachen)."""
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [t for v in obj.values() for t in _alle_texte(v)]
    if isinstance(obj, list):
        return [t for v in obj for t in _alle_texte(v)]
    return []


def _ordne_zeile(text, K):
    """'Titel: a, b, c': Werkzeuge mit Treffern in der Anzeige nach vorn (stabil)."""
    titel, sep, rest = text.partition(": ")
    if not sep:
        return text
    teile, tiefe, cur = [], 0, ""
    for ch in rest:
        tiefe += ch == "("
        tiefe -= ch == ")"
        if ch == "," and tiefe == 0:
            teile.append(cur.strip()); cur = ""
        else:
            cur += ch
    teile.append(cur.strip())
    teile.sort(key=lambda t: 0 if _treffer(t, K) else 1)
    return titel + sep + ", ".join(teile)


def _ausgabe(arbeit, skills, sprachen, profil, info):
    out = {s: [{"id": it["id"], "kopf": it["kopf"], "punkte": [g["text"] for g in it["gruppen"]]}
               for it in arbeit[s]] for s in SEKTIONEN}
    out["skills"] = [s["text"] for s in skills]
    out["sprachen"] = sprachen
    out["profil"] = profil
    out["info"] = info
    return out


def waehle(daten, fokus, lang, ist_eine_seite, anzeige="", texte=None, anzeige_begriffe=None, profil=""):
    texte, anzeige_begriffe = texte or {}, anzeige_begriffe or []
    erlaubt = daten["tags"]
    falsch = [t for t in fokus if t not in erlaubt]
    if falsch:
        raise CvFehler(f"Unbekannte Fokus-Tags {falsch}. Erlaubt: {', '.join(erlaubt)}")
    begriffe = daten.get("begriffe", [])
    K = sorted(b for b in begriffe if _hat(anzeige, b))
    info = {"treffer": K, "neu": {}, "gekuerzt": []}
    ids = {it["id"] for s in SEKTIONEN for it in daten[s]}
    for i in texte:
        if i not in ids:
            raise CvFehler(f"'texte' nennt unbekannte id '{i}'. Bekannt: {', '.join(sorted(ids))}")
    arbeit = {}
    for s in SEKTIONEN:
        items = []
        for it in daten[s]:
            kopf = _text(it["kopf"], lang, it["id"])
            gruppen = []
            for g in it["gruppen"]:
                p = _variante(g, fokus, K, lang)
                gruppen.append({"text": _text(p, lang, it["id"]),
                                "score": punkte(p["tags"], fokus) + _treffer(p[lang], K)})
            gruppen = [g for _, g in sorted(enumerate(gruppen), key=lambda x: (-x[1]["score"], x[0]))]
            if it["id"] in texte:
                erlaubt_z = _zahlen(_alle_texte([it["kopf"], it["gruppen"]]))
                neu_z = _zahlen(texte[it["id"]]) - erlaubt_z
                if neu_z:
                    raise CvFehler(f"'{it['id']}': Zahlen {sorted(neu_z)} stehen nicht in deinen Fakten")
                gruppen = [{"text": t, "score": 5} for t in texte[it["id"]]]
                info["neu"][it["id"]] = list(texte[it["id"]])
            wert = punkte(it["tags"], fokus) + len({k.casefold() for k in it.get("keywords", [])} & {k.casefold() for k in K})
            items.append({"id": it["id"], "tags": it["tags"], "pflicht": it.get("pflicht", False),
                          "kopf": kopf, "gruppen": gruppen, "wert": wert})
        if s == "projekte":
            items = [it for _, it in sorted(enumerate(items), key=lambda x: (-x[1]["wert"], x[0]))]
        arbeit[s] = items
    skills = [{"text": _ordne_zeile(_text(sk, lang, sk["id"]), K),
               "score": punkte(sk["tags"], fokus) + _treffer(sk[lang], K), "i": i}
              for i, sk in enumerate(daten["skills"])]
    skills.sort(key=lambda x: (-x["score"], x["i"]))
    sprachen = _text(daten["sprachen"], lang, "sprachen")
    if profil:
        neu_z = _zahlen([profil]) - _zahlen(_alle_texte(daten))
        if neu_z:
            raise CvFehler(f"Profil: Zahlen {sorted(neu_z)} stehen nicht in deinen Fakten")
    while not ist_eine_seite(_ausgabe(arbeit, skills, sprachen, profil, info)):
        kand = [(it["wert"] + g["score"], (si, ii, gi))
                for si, s in enumerate(SEKTIONEN) for ii, it in enumerate(arbeit[s]) if not it["pflicht"]
                for gi, g in enumerate(it["gruppen"])]
        if not kand:
            raise CvFehler("Passt nicht auf eine Seite, nichts mehr zu kürzen. Mehr Pflicht-Einträge entfernen oder Texte kürzen.")
        _, (si, ii, gi) = min(kand, key=lambda k: (k[0], tuple(-x for x in k[1])))
        it = arbeit[SEKTIONEN[si]][ii]
        info["gekuerzt"].append(f"{it['id']}: {it['gruppen'][gi]['text'][:60]}")
        del it["gruppen"][gi]
        if not it["gruppen"]:
            del arbeit[SEKTIONEN[si]][ii]
    out = _ausgabe(arbeit, skills, sprachen, profil, info)
    eigene = {b.casefold() for b in begriffe}
    gesamt = " ".join(_alle_texte({k: v for k, v in out.items() if k != "info"}))
    fremd = [t for t in anzeige_begriffe if t.casefold() not in eigene and _hat(gesamt, t)]
    if fremd:
        raise CvFehler(f"Der CV nennt {fremd}, das steht nicht in deinen Fakten. Streichen oder ohne diesen Begriff formulieren.")
    return out


# ---------- Rendern ----------
TITEL = {"de": ["Akademischer Werdegang", "Berufserfahrung", "Projekte", "Skills, Sprachen \\& Tools"],
         "en": ["Education", "Professional Experience", "Projects", "Skills, Languages \\& Tools"]}


PROFIL = {"de": "Profil", "en": "Profile"}


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
    if auswahl.get("profil"):
        koerper += f"\\section{{{PROFIL[lang]}}}\n{_fmt(auswahl['profil'])}\n"
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


def bauen(spec, E, root, info=None):
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

    ap = spec.get("anzeige")
    anzeige = (root / ap).read_text(encoding="utf-8") if ap else ""
    auswahl = waehle(daten, spec.get("fokus", []), lang, passt, anzeige, spec.get("texte"),
                     spec.get("anzeige_begriffe"), spec.get("profil", ""))
    if info is not None:
        info.update(auswahl["info"])
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
    info = {}
    try:
        pdf = bauen(spec, laden(), ROOT, info)
    except CvFehler as e:
        sys.exit(f"Fehler: {e}")
    print(f"ok {pdf.relative_to(ROOT)} | 1 Seite | Fokus: {', '.join(spec.get('fokus', [])) or '-'}")
    print("Treffer aus der Anzeige:", ", ".join(info["treffer"]) or "-")
    for i, t in info["neu"].items():
        print(f"Neu formuliert ({i}):", *[f"\n  - {x}" for x in t])
    for g in info["gekuerzt"]:
        print("Gekürzt:", g)
