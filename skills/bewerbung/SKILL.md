---
name: bewerbung
description: Verwenden, wenn die Person Jobs suchen will (Werkstudent, Praktikum, Abschlussarbeit), einen Stellenlink oder Stellentext schickt, ein Anschreiben oder das Ausfüllen eines Bewerbungsformulars möchte oder ihren Bewerbungsstatus/Tracker aktualisieren will.
---

# Bewerbung (Bewerbungspilot)

Zuerst `AGENTS.md`, `einstellungen.json` und `profil.md` lesen. Fehlt `einstellungen.json` oder ist `"eingerichtet": false` → erst den Skill `einrichtung` ausführen.
Fähigkeiten aus `einstellungen.json` beachten: `browser`, `gmail`, `agy`. Ist eine davon false, den beschriebenen Ersatzweg nehmen.

## Start: welcher Modus?
- Link oder Stellentext → "Neue Stelle".
- "Status", "update", "durum" o. ä. → nur Mail-Abgleich.
- Sonst (kein Link, z. B. "Jobs suchen") → "Jobsuche". Als erste Frage: Werkstudent, Praktikum oder beides? Optional Schwerpunkt.

## Mail-Abgleich (höchstens einmal pro Sitzung)
- `gmail: true` → per Connector nach Mails seit dem letzten `update`-Datum suchen, z. B. `(Bewerbung OR application) after:JJJJ/MM/TT`. Snippet reicht meist.
- `gmail: false` → fragen, ob Absagen, Eingangsbestätigungen oder Einladungen gekommen sind.
Änderungen mit `tools/track.py set ...` eintragen. Nur die Änderungen in 1–3 Zeilen nennen.

## Jobsuche
1. Kriterien aus `profil.md` (Suchkriterien, Verfügbarkeit).
2. Suchen: `agy: true` → `tools/agy.sh recherche "<Auftrag>" recherche/<datum>_<art>.md`. Sonst selbst mit Websuche, 4–5 Anfragen parallel (Art + Fachrichtung + Ort, Umkreis, große Arbeitgeber der Region, StepStone/Indeed/LinkedIn/Hochschul-Jobportal).
3. Jede Stelle auf der Originalseite prüfen (noch offen, Ort, Studiengang, Dauer). Nur offene Stellen mit funktionierendem Link.
4. Bereits in `bewerbungen.json` stehende Stellen weglassen.
5. Top 5–10 nach Passung sortieren und in `recherche/<datum>_<art>.md` speichern (Firma, Stelle, Ort, Passung 1–5, Grund, Link). Im Chat nur eine kurze Liste.
6. Die Person wählt aus → pro Stelle "Neue Stelle".

## Neue Stelle
1. **Eckdaten holen.** `agy: true` → `tools/agy.sh eckdaten <url> <out>`. Sonst Web-Fetch, bei leerer Seite (JavaScript-Portale) im Browser. Nur Studiengang, Ort, Dauer/Stunden/Start, Unterlagen, Status.
2. **Kurzbewertung (max. 8 Zeilen).** Passt es? Stärken aus dem Profil, Lücken ehrlich, Hinweise (Ort, Dauer vs. Verfügbarkeit, Pflichtdokumente, Referral-Link). Passt es klar nicht → sagen und fragen, ob trotzdem.
3. **Anzeige sichern.** Ordner `bewerbungen/<JJJJ-MM-TT>_<firma>_<stelle>/` anlegen, Anzeige als `stellenanzeige.md` speichern (Eckdaten, Aufgaben, Profil, Angebot, Unterlagen). Mit agy: `tools/agy.sh anzeige <url> <ordner>/stellenanzeige.md`.
4. **Anschreiben (wenn verlangt oder sinnvoll).** Sprache der Anzeige, 4 kurze Absätze, ca. 200 Wörter. Nur Fakten aus `profil.md`, keine Doppelpunkte in Sätzen, Lücken ehrlich. `spec.json` im Ordner schreiben (Felder siehe Kopf von `tools/anschreiben.py`, `&` als `\\&`), dann `python3 tools/anschreiben.py <spec.json>`. Entwurf optional per `tools/agy.sh anschreiben`, danach gegen das Profil prüfen. Das PDF liegt danach im Unterlagen-Ordner.
5. **Formular (wenn die Person "bewerben" sagt).** Vorher `portale.md` lesen.
   - `python3 tools/stage.py <Anschreiben.pdf>` → Dateien liegen in `.upload/`.
   - Mit Browser: Cookies ablehnen, Felder aus dem Profil, zuerst Uploads, dann Textfelder, danach Werte per Formular-Scan (`tools/browser.js.md`) prüfen. Lebenslauf-Feld nur Lebenslauf, Rest einzeln. `maxLength` beachten.
   - Ohne Browser: Liste aller Felder mit fertigen Antworten zum Kopieren und die Dateiliste ausgeben. Die Person füllt selbst aus.
   - Login, Konto, Einwilligungen, CAPTCHA macht immer die Person.
   - Vor dem Absenden kurze Zusammenfassung zeigen und auf "senden" warten.
6. **Nach dem Absenden.** `python3 tools/gesendet.py <Anschreiben.pdf>`, `python3 tools/stage.py clean`, dann `python3 tools/track.py add "<Firma>" "<Stelle>" <Art> "in Prüfung" "<Notiz>" "<ordner>"`. Auch wenn die Person selbst abgeschickt hat. Neue Portal-Erkenntnisse kurz in `portale.md` ergänzen.

## Stil
Kurz und direkt, in der Sprache aus dem Profil. Statusmeldungen in einer Zeile.
