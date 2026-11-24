"""Qualitätsprüfung für Anschreiben (Regeln: docs/anschreiben_regeln.md).

pruefe(text, firma, lang, profil, anzeige) -> (fehler, warnungen)
Fehler brechen den Bau ab (außer --force), Warnungen werden nur gezeigt.
"""
import re

# Harte Floskeln (Fehler)
FLOSKELN = {
    "de": [r"hiermit bewerbe", r"mit gro(ß|ss)em interesse", r"mit gro(ß|ss)er begeisterung",
           r"schon immer (war|ist) es mein traum", r"neue herausforderung",
           r"w(ü|u)rde ich mich (sehr )?freuen", r"w(ü|u)rde mich (sehr )?freuen", r"positive r(ü|u)ckmeldung",
           r"ideale besetzung"],
    "en": [r"i am writing to express", r"thrilled to apply", r"my strong interest", r"dream (job|opportunity)",
           r"look forward to hearing from you positively"],
}
# Weiche KI-Tells (Warnung)
TELLS = {
    "de": [r"eintauch\w*", r"navigier\w*", r"bereicherung", r"facettenreich\w*", r"versiert\w*", r"synerg\w*",
           r"nahtlos\w*", r"ma(ß|ss)geblich\w*", r"ganzheitlich\w*", r"wegweisend\w*", r"innovativ\w*",
           r"dynamisch\w* umfeld", r"spannende\w* herausforderung\w*", r"fundiert\w*", r"ausgepr(ä|a)gt\w*",
           r"(ä|a)u(ß|ss)erst", r"leidenschaftlich\w*", r"brenne f(ü|u)r", r"z(ü|u)gig\w*", r"zielorientiert\w*",
           r"belastbar\w*", r"hochmotiviert\w*", r"teamf(ä|a)hig\w*", r"teamplayer", r"hands-on",
           r"mehrwert generieren", r"neues level", r"nicht nur\b.{1,80}\bsondern auch"],
    "en": [r"delve\w*", r"navigat\w*", r"tapestry", r"testament", r"realm", r"leverag\w*", r"seamless\w*",
           r"passionate about", r"hit the ground running", r"fast-paced", r"dynamic team", r"proven track record",
           r"valuable asset", r"synerg\w*", r"not only\b.{1,80}\bbut also"],
}
PLATZHALTER = [r"\bTODO\b", r"<<", r">>", r"\[(Firma|Unternehmen|Name|Ansprechpartner|Company)\]", r"\bXXX\b"]
RECHTSFORM = {"gmbh", "ag", "se", "kg", "mbh", "ltd", "co", "ohg", "ug", "kgaa", "inc", "llc", "plc", "sa", "ev",
              "haftungsbeschränkt", "limited"}
MONATE = r"(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember|January|February|March|June|July|October|December)"


def _norm(s):
    return " ".join(re.sub(r"[^\w]+", " ", s.lower().replace("&", " ")).split())


def firmenkern(firma):
    """Firmenname ohne Rechtsform (GmbH, AG, SE, KG, mbH, Ltd. ...)."""
    teile = [t for t in _norm(firma).split() if t not in RECHTSFORM]
    return " ".join(teile)


def _firma_im_text(firma, text):
    kern = firmenkern(firma)
    if not kern:
        return True
    n = _norm(text)
    teile = kern.split()
    kandidaten = [kern, " ".join(teile[:2])]
    if len(teile[0]) >= 3:
        kandidaten.append(teile[0])
    return any(k and re.search(rf"(?<!\w){re.escape(k)}(?!\w)", n) for k in kandidaten)


def _ohne_datum(s):
    """Daten, Uhrzeiten und Jahreszahlen entfernen, damit sie keine Zahlen-Warnung auslösen."""
    s = re.sub(r"\b\d{1,2}\.\s?\d{1,2}\.(\s?\d{2,4})?", " ", s)
    s = re.sub(rf"\b\d{{1,2}}\.\s?{MONATE}(\s+\d{{4}})?", " ", s)
    s = re.sub(rf"\b\d{{1,2}}\s+{MONATE}(\s+\d{{4}})?", " ", s)
    s = re.sub(r"\b\d{1,2}:\d{2}(\s?Uhr)?", " ", s)
    s = re.sub(r"\b(19|20)\d{2}\b", " ", s)
    return s


def zahlen(s):
    return set(re.findall(r"\d+(?:[.,]\d+)?", _ohne_datum(s)))


def _saetze(absatz):
    return [x for x in re.split(r"(?<=[.!?])\s+", absatz.strip()) if x]


def pruefe(text, firma="", lang="de", profil="", anzeige=""):
    f, w = [], []
    sp = "de" if lang == "de" else "en"
    low = text.lower()
    woerter = len(text.split())
    absaetze = [a for a in re.split(r"\n\s*\n", text.strip()) if a.strip()]

    # Fehler
    for p in FLOSKELN[sp]:
        m = re.search(p, low)
        if m:
            f.append(f"Floskel: '{m.group(0)}'")
    if sp == "de" and re.match(r"\s*im rahmen meines", low):
        f.append("Floskel: Einstieg 'Im Rahmen meines ...'")
    if "—" in text:
        f.append("Gedankenstrich '—' (Em-Dash)")
    if re.search(r"\s[–-]\s", text):
        f.append("Gedankenstrich ' – ' im Satz, besser Komma oder zwei Sätze")
    if re.search(r"(?<!\d):|:(?!\d)", text):
        f.append("Doppelpunkt im Text")
    for p in PLATZHALTER:
        if re.search(p, text):
            f.append(f"Platzhalter '{re.search(p, text).group(0)}'")
    if woerter > 300:
        f.append(f"{woerter} Wörter, Maximum 300")

    # Warnungen
    if woerter < 170 or woerter > 280:
        if woerter <= 300:
            w.append(f"{woerter} Wörter, Ziel 180 bis 280")
    for p in TELLS[sp]:
        m = re.search(r"(?<!\w)" + p + r"(?!\w)", low)
        if m:
            w.append(f"KI-Tell: '{m.group(0)}'")
    if firma and not _firma_im_text(firma, text):
        w.append(f"Firma '{firmenkern(firma)}' kommt im Text nicht vor")
    if not 3 <= len(absaetze) <= 5:
        w.append(f"{len(absaetze)} Absätze, Ziel 4")
    for i, a in enumerate(absaetze, 1):
        if len(a.split()) > 110:
            w.append(f"Absatz {i} hat {len(a.split())} Wörter (Textwüste)")
    ich = "Ich " if sp == "de" else "I "
    starts = [s.startswith(ich) for a in absaetze for s in _saetze(a)]
    if sum(starts) > 2 or any(a and b for a, b in zip(starts, starts[1:])):
        w.append("Zu viele Sätze mit 'Ich' am Anfang (höchstens 2, nie direkt hintereinander)")
    if absaetze and re.search(r"\b(w(ü|u)rde|k(ö|o)nnte|h(ä|a)tte|would|could)\b", absaetze[-1].lower()):
        w.append("Konjunktiv im Schlusssatz, besser Indikativ")
    if profil:
        erlaubt = zahlen(profil) | zahlen(anzeige)
        neu = sorted(zahlen(text) - erlaubt)
        if neu:
            w.append(f"Zahlen nicht in profil.md/Anzeige: {', '.join(neu)}")
    return f, w
