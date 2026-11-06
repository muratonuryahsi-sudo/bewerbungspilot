#!/bin/sh
# Optional: agy-Delegation (Google Antigravity CLI / Gemini, sandbox, spart Claude-Tokens). Ausgabe nur in Datei, Claude liest danach gezielt.
#   agy.sh eckdaten <url> <out.md>             -> Eckdaten einer Stelle (6 Zeilen)
#   agy.sh anschreiben <stellenanzeige.md> <out.json> [de|en]  -> spec.json-Entwurf für tools/anschreiben.py
#   agy.sh recherche "<auftrag>" <out.md>      -> Jobsuche, Tabelle mit geprüften Links
#   agy.sh anzeige <url|titel+firma> <out.md>   -> Stellenanzeige als Markdown (Aufgaben/Profil/Angebot)
#   agy.sh frei "<prompt>" <out.md>            -> beliebiger Auftrag
J="$(cd "$(dirname "$0")/.." && pwd)"; PROFIL="$(cat "$J/profil.md")"; JSON="$(cat "$J/bewerbungen.json")"
mode="$1"; shift
case "$mode" in
eckdaten) P="Rufe $1 ab. Antworte NUR mit diesen 6 Zeilen, ohne Einleitung:
Titel: ...
Studiengang gefordert: ...
Ort/Arbeitsmodell: ...
Dauer/Stunden/Start: ...
Unterlagen/Anschreiben: ...
Status: offen|geschlossen|unklar (Seite leer oder nicht ladbar = unklar)"; OUT="$2";;
anschreiben) L="${3:-de}"; P="Schreibe ein Anschreiben für diese Stelle. Nutze NUR Fakten aus dem Profil, nichts erfinden, Lücken ehrlich benennen (\"noch nicht gearbeitet, arbeite mich gerne ein\").
Regeln: Sprache $L, 4 kurze Absätze, ca. 170-200 Wörter, natürlich, nicht übertrieben, nicht nach KI klingend, KEINE Doppelpunkte in Sätzen, keine Links/URLs, kein Gedankenstrich-Stil. Keine Floskeln/Steigerungen wie fundiert, genau, zügig, leidenschaftlich, eigenständig verstärken. Erfahrung exakt wie im Profil beschreiben, nichts versprechen, was nicht belegt ist. Erster Satz nicht 'Im Rahmen', sondern 'ich studiere ...' (Anrede endet mit Komma). Verfügbarkeit, Dauer und Start genau wie im Profil (Abschnitt Verfügbarkeit). LaTeX: & als \\\\& schreiben.
Gib NUR gültiges JSON aus (kein Markdown-Codeblock) mit Schlüsseln: dir, pdf, lang, firma, adresse (Zeilen mit \\\\\\\\ trennen), betreff, anrede, text (Absätze mit \\n\\n). dir = $(date +%F)_<firma>_<stelle-kurz> (je max 3 Wörter, klein, Bindestriche), pdf = Anschreiben_<Firma>_<Stelle-kurz>.pdf (max 4 Wörter, Unterstriche).
=== PROFIL ===
$PROFIL
=== STELLE ===
$(cat "$1")"; OUT="$2";;
recherche) P="$1
Prüfe jede Stelle durch Abruf der Originalseite (noch offen? Ort, Studiengang laut Profil ok, Dauer). Nur offene Stellen mit funktionierendem Link behalten. Bereits in bewerbungen.json stehende Firma+Stelle weglassen.
Ausgabe NUR als Markdown-Tabelle: | Firma | Stelle | Ort/Hybrid | Passung 1-5 | Grund (1 Satz) | Link |, sortiert nach Passung, max 10 Zeilen, danach eine Zeile 'Verworfen: ...'.
=== PROFIL ===
$PROFIL
=== BEWERBUNGEN ===
$JSON"; OUT="$2";;
anzeige) P="Rufe die Stellenanzeige $1 ab (bei Nicht-Erreichbarkeit per Websuche nach Titel+Firma die Originalanzeige suchen). Gib sie als Markdown aus, NUR mit diesen Abschnitten (Inhalte möglichst wörtlich aus der Anzeige, als Stichpunkte): ## Eckdaten (Firma, Ort/Arbeitsmodell, Art, Dauer/Stunden, Start, Kennziffer) ## Aufgaben ## Profil (gefordert / wünschenswert) ## Angebot ## Unterlagen & Kontakt. Wenn die Anzeige nicht gefunden wird, schreibe nur: NICHT GEFUNDEN."; OUT="$2";;
frei) P="$1"; OUT="$2";;
*) echo "Modus?"; exit 1;;
esac
agy --sandbox -p "WICHTIG: Benutze ausschließlich deine eingebauten Web-Such- und Web-Fetch-Werkzeuge. Keine Shell-Befehle (kein curl, kein python), keine Dateien schreiben. Gib das Ergebnis direkt als Antwort aus.

$P" --print-timeout 600s > "$OUT" 2>"$OUT.err"; rc=$?
[ -s "$OUT.err" ] || rm -f "$OUT.err"
echo "agy exit=$rc -> $OUT ($(wc -c < "$OUT") Bytes)"
