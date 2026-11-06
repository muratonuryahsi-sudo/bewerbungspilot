---
name: einrichtung
description: Ersteinrichtung des Bewerbungspiloten. Verwenden, wenn einstellungen.json fehlt oder "eingerichtet" false ist, oder wenn die Person "einrichtung", "setup" oder "Profil ändern" sagt. Führt Schritt für Schritt durch Profil, Unterlagen und Werkzeuge.
---

# Einrichtung (Bewerbungspilot)

Ziel: Am Ende sind `profil.md` und `einstellungen.json` vollständig, die Unterlagen liegen bereit, und ein Probe-Anschreiben lässt sich bauen.

So vorgehen:
- Immer nur EINEN Schritt auf einmal. Kurz erklären, was jetzt passiert, dann fragen oder machen, dann den Fortschritt zeigen ("Schritt 3 von 8 erledigt").
- Mit Auswahl-Fragen arbeiten, wo es geht (Claude Code AskUserQuestion, sonst nummerierte Optionen).
- Nichts erfinden. Was die Person nicht weiß, bleibt TODO und wird am Ende aufgelistet.
- Antworten sofort in die Dateien schreiben, damit nichts verloren geht, wenn die Sitzung abbricht. Wird die Einrichtung später fortgesetzt, an der ersten TODO-Stelle weitermachen.
- Alles auf Deutsch.

## Schritt 1 – Begrüßung und Überblick
Kurz erklären, was der Bewerbungspilot macht (Stellen finden und prüfen, Anschreiben als PDF, Formulare ausfüllen, Tracker mit Übersicht) und dass die Einrichtung ca. 15–20 Minuten dauert. Hinweis, dass alle persönlichen Daten nur lokal bleiben (stehen in .gitignore).
Falls noch nicht vorhanden: `vorlagen/profil.beispiel.md` → `profil.md` und `vorlagen/einstellungen.beispiel.json` → `einstellungen.json` kopieren.

## Schritt 2 – Welcher Agent und welche Werkzeuge?
Erkennen bzw. fragen und in `einstellungen.json` eintragen:
- `agent`: claude, codex oder anderer.
- `browser`: Kann der Agent einen Browser steuern? Claude Code → Erweiterung "Claude in Chrome" (claude.ai/chrome). Codex/andere → z. B. Playwright-MCP. Wenn nein, ist das okay, dann füllt die Person Formulare selbst aus.
- `gmail`: Ist ein Gmail-Connector verbunden? Optional.
- `agy`: Ist Google Antigravity (`agy`) installiert und soll es Websuche/Entwürfe übernehmen? Optional, Standard nein.

## Schritt 3 – Programme prüfen
Mit Shell-Befehlen prüfen und nur Fehlendes melden, inklusive Installationsbefehl (macOS mit Homebrew, Linux mit apt):
- `python3` (Pflicht)
- `tectonic` (Pflicht für Anschreiben-PDFs) → `brew install tectonic`
- `pdfinfo` aus poppler (Pflicht) → `brew install poppler` bzw. `apt install poppler-utils`
- `pdftotext` (gleiches Paket, zum Einlesen des Lebenslaufs)
- optional `agy`, `gh`
Erst weitermachen, wenn die Pflicht-Programme da sind, oder die Person sagt, sie installiert sie später.

## Schritt 4 – Lebenslauf einlesen (spart viel Tipparbeit)
Nach dem Pfad zum aktuellen Lebenslauf (PDF) fragen. Mit `pdftotext -layout` lesen und daraus einen Entwurf für `profil.md` machen (Stammdaten, Studium, Erfahrung, Projekte, Skills, Sprachen). Den Entwurf abschnittsweise zeigen und bestätigen lassen. Kein Lebenslauf vorhanden → die Abschnitte in Schritt 5 einzeln abfragen.

## Schritt 5 – Profil vervollständigen
Abschnitt für Abschnitt durch `profil.md` gehen und jede TODO-Stelle klären. Wichtig sind vor allem:
1. Stammdaten (Name, Adresse, Telefon, E-Mail, Staatsangehörigkeit). Gleich auch in `einstellungen.json` eintragen (name, strasse, plz_ort, ort, telefon, email).
2. Studium (Studiengang, Hochschule, Semester, Notendurchschnitt, Studienende).
3. Verfügbarkeit (Werkstudent ab wann und wie viele Stunden, Pflichtpraktikum Start und Mindestdauer laut Studienordnung, Gehaltswunsch, Ort/Umkreis).
4. Erfahrung. Bei jedem Job nachfragen, was WIRKLICH gemacht wurde. Einen ehrlichen Kurzsatz fürs Anschreiben formulieren und bestätigen lassen.
5. Projekte und Skills, inklusive "Nicht vorhanden" (wichtig, damit nichts behauptet wird).
6. Motivation und Interessen.
7. Standardantwort "Qualifikationen" (ca. 700 Zeichen) entwerfen und bestätigen lassen.
8. Suchkriterien (Art, Ort, Bereiche, Ausschlüsse) und Sprache im Chat.

## Schritt 6 – Unterlagen-Ordner
Fragen, wo die Bewerbungsunterlagen liegen sollen (Standard `~/Bewerbungsunterlagen`, iCloud/OneDrive geht auch). Ordner anlegen, falls nötig, plus Unterordner `Anschreiben_gesendet/`. Inhalt auflisten und gemeinsam festlegen:
- `lebenslauf` = Dateiname des Lebenslaufs
- `weitere_dokumente` = Notenspiegel, Immatrikulationsbescheinigung, Arbeitszeugnisse usw.
Fehlende Dokumente nennen (z. B. aktuelle Immatrikulationsbescheinigung). Hinweis: PDFs ohne Links, max. 5 MB pro Datei.
Optional einen Link `unterlagen` im Projekt auf den Ordner anlegen.

## Schritt 7 – Testlauf
- `tools/stage.py` ausführen und prüfen, dass alle Dateien gefunden werden, danach `tools/stage.py clean`.
- Ein Probe-Anschreiben bauen (spec.json mit Firma "Testfirma GmbH", kurzer Text aus dem Profil) mit `tools/anschreiben.py`, PDF zeigen und danach Probe-Ordner und Probe-PDF wieder entfernen (in den Papierkorb).
- `python3 generate_overview.py` ausführen, damit `uebersicht.html` existiert.
Fehler hier direkt beheben.

## Schritt 8 – Abschluss
`"eingerichtet": true` in `einstellungen.json` setzen. Offene TODOs auflisten. Dann kurz zeigen, wie es weitergeht:
- Stellenlink schicken (Claude Code: `/bewerbung <link>`) → Bewertung, Anschreiben, Formular.
- "Jobs suchen" → Recherche nach den Suchkriterien.
- "Status" → Mail-Abgleich und Tracker aktualisieren.
- `uebersicht.html` im Browser öffnen für den Überblick.
- Profil später ändern → "einrichtung" erneut aufrufen oder `profil.md` direkt bearbeiten.
