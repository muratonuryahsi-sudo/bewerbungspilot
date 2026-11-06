# Bewerbungspilot – Anleitung für den Agenten

Gilt für jeden Coding-Agenten (Claude Code, Codex, Gemini CLI …). Hier laufen alle Bewerbungen (Werkstudent, Praktikum, Abschlussarbeit) einer Person.

## Zuerst prüfen
Fehlt `einstellungen.json` oder steht dort `"eingerichtet": false`, dann ZUERST die Einrichtung machen (Skill `einrichtung`, Datei `skills/einrichtung/SKILL.md`). Vorher keine Bewerbung starten.

## Skills
- `skills/einrichtung/SKILL.md` – Ersteinrichtung Schritt für Schritt (Profil, Unterlagen, Werkzeuge).
- `skills/bewerbung/SKILL.md` – Jobsuche, neue Stelle bewerten, Anschreiben, Formular, Tracker, Mail-Abgleich.
Claude Code findet sie unter `.claude/skills/`, Codex unter `.agents/skills/` (beides Links auf `skills/`). Kennt dein Agent keine Skills, lies die Datei direkt, wenn die Person "einrichtung" oder "bewerbung" sagt oder einen Stellenlink schickt.

## Dateien
- `profil.md` – alle Fakten und Standardantworten. Einzige Quelle, nichts erfinden.
- `einstellungen.json` – Name/Kontakt für den Briefkopf, Unterlagen-Ordner, Dateinamen, welche Werkzeuge vorhanden sind.
- `bewerbungen.json` – Tracker (einzige Quelle). Nur über `tools/track.py` ändern.
- `uebersicht.html` / `bewerbungen.md` – automatisch erzeugt, nicht von Hand bearbeiten.
- Status-Werte: in Prüfung, Gespräch, Zusage, Absage, keine Antwort, nicht abgeschlossen, unklar.
- `bewerbungen/<datum>_<firma>_<stelle>/` – pro Bewerbung stellenanzeige.md, spec.json, Anschreiben (.tex + PDF).
- `recherche/` – Ergebnisse der Jobsuche.
- `portale.md` – Ablauf und Eigenheiten je Bewerbungsportal. Vor jedem Formular lesen, Neues ergänzen.
- Alle persönlichen Dateien stehen in `.gitignore` und werden nie committet.

## Werkzeuge
- `tools/track.py add|set|rm ...` – Tracker ändern und Übersicht neu erzeugen. Bei `add` den Ordner als 6. Argument mitgeben.
- `tools/anschreiben.py <spec.json>` – Anschreiben bauen (tectonic), prüfen (1 Seite, keine Links/aktiven Inhalte), PDF in den Unterlagen-Ordner legen.
- `tools/stage.py [Anschreiben.pdf]` / `tools/stage.py clean` – Uploads nach `.upload/` kopieren / aufräumen.
- `tools/gesendet.py <Anschreiben.pdf>` – nach dem Absenden nach `Anschreiben_gesendet/` verschieben.
- `tools/browser.js.md` – JS-Snippets für Formular-Scan, Shadow-DOM-Upload, StepStone-Liste.
- `tools/agy.sh` – OPTIONAL, nur wenn `"agy": true`. Delegiert Websuche und Textentwürfe an Google Antigravity (Gemini). Ist es aus, macht der Agent das selbst (Websuche/Web-Fetch).

## Optionale Fähigkeiten (in einstellungen.json)
- `browser` – Der Agent kann einen Browser steuern (z. B. Claude in Chrome, Playwright-MCP). Ohne Browser bereitet der Agent alles vor (Anschreiben, Antworten für jedes Feld, Dateiliste) und die Person füllt das Formular selbst aus.
- `gmail` – Gmail-Connector/MCP vorhanden. Ohne ihn fragt der Agent nach Absagen und Einladungen oder die Person fügt Mails ein.
- `agy` – siehe oben.

## Feste Regeln
- Kurz und direkt antworten, in der Sprache aus `profil.md` (Abschnitt Regeln für Texte).
- Texte natürlich, nicht übertrieben, nicht nach KI klingend. Keine Doppelpunkte in Sätzen.
- Nur echte Erfahrungen nennen, Lücken ehrlich benennen.
- PDFs schwarz-weiß, eine Seite, ohne Links und ohne aktive Inhalte (Portale lehnen sie sonst ab).
- Vor dem Absenden immer eine kurze Zusammenfassung zeigen und auf ein klares "senden" warten.
- Einwilligungs-Checkboxen, Logins, Passwörter, Konto anlegen und CAPTCHAs macht die Person selbst.
- Lebenslauf-Feld nur mit dem Lebenslauf. Andere Dokumente einzeln unter "Weitere Dokumente", keine zusammengefügte Mappe, außer das Portal nimmt nur eine einzige Datei.
- Textfelder: vor dem Ausfüllen die maximale Zeichenzahl (`maxLength`) prüfen.
- Hat die Person ein Formular selbst abgeschickt, nicht weiter daran arbeiten.
- Nichts endgültig löschen, nur in den Papierkorb verschieben.
- Tracker: nur abgeschickte Bewerbungen eintragen.

## Token sparen
- Bei jeder Stelle zuerst nur Eckdaten (Studiengang, Ort, Dauer, Start). Passt es nicht, kurz sagen und aufhören.
- Auf Formularseiten nie den ganzen Seitentext lesen (Länderlisten kosten Tausende Tokens), sondern das Formular-Scan-Snippet.
- Screenshots nur, wenn ein Klickziel unklar ist.
- Mail-Abgleich höchstens einmal pro Sitzung.
