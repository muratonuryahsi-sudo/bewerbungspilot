# Portal-Notizen

Vor jedem Formular hier nachsehen. Neue Erkenntnisse kurz ergänzen (ohne persönliche Daten, die Datei ist im Repo).

## Allgemein
- Login, Konto anlegen, Einwilligungen und CAPTCHA macht die Person selbst. Portal-Tabs am Anfang öffnen, damit sie sich in einem Rutsch einloggen kann.
- Uploads: zuerst `tools/stage.py [Anschreiben.pdf]`, dann aus `.upload/` hochladen. Cloud-Pfade (iCloud) lehnt Chrome oft ab.
- Während einer Bewerbung keine Tabs schließen, sonst ist der Login oft weg.
- Element-Referenzen ändern sich nach einem Re-Render. Nach jedem Upload neu suchen.
- React-Felder (StepStone, Workday, Siemens): klicken + tippen statt Wert direkt setzen. Klassische Formulare (Taleo, KPMG): Wert setzen geht.
- Beim Setzen per JavaScript immer `maxLength` prüfen, sonst Fehler beim Absenden.

## Taleo (z. B. Mercedes-Benz, tas-daimler.taleo.net)
- Ablauf: Datenschutzhinweis → Login → Lebenslauf (manuell) → Persönliche Infos → Jobspezifische Fragen → Bildung → Berufserfahrung → Anhänge → Prüfen.
- Alte Daten im Konto prüfen (Wohnort, Staatsangehörigkeit).
- Anhänge: alte Dateien nicht als "relevant" markieren, neue schon. Lebenslauf-Spalte = Lebenslauf.
- Mercedes verlangt oft "Nachweis Pflichtpraktikum" und "Nachweis Regelstudienzeit".

## StepStone Schnelle Bewerbung
- Login nötig. CV- und Anschreiben-Upload über versteckte `input[type=file]`.
- Absenden bedeutet Zustimmung zu Datenschutz/AGB der Firma, keine separate Checkbox.
- "Ich bin interessiert" führt manchmal auf ein externes Portal (neuer Tab).

## KPMG (jobs.kpmg.de)
- Kein Login. Statt Anschreiben ein Freitextfeld (ca. 600 Zeichen).
- Uploads im Shadow DOM (`kpmg-upload#cv`, `#attachments`), Snippet in `tools/browser.js.md`. Nach jedem Upload neues Input.
- Weitere Fragen sind Shadow-Textareas, Wert über nativen Setter und `input`/`change` mit `composed:true`.

## Workday (z. B. ZEISS)
- Cookies ablehnen → Bewerben → "Manuell bewerben" → Login/Konto.
- Adresse getrennt (Straße / Hausnummer). Upload: ein Input mit multiple, alle Dateien in einem Aufruf.
- Datum: ins Tag-Feld klicken und Ziffern tippen (z. B. 01032027). Dropdowns öffnen → Option suchen → klicken.

## Siemens (Avature)
- Profil wird aus altem CV vorbefüllt und ist oft falsch. Vor dem Absenden korrigieren.
- Staatsangehörigkeit ist ein Such-Dropdown. Viele Stellen fordern ET/Mechatronik.

## SuccessFactors (z. B. ARBURG)
- Konto anlegen → Aktivierungsmail. Session läuft nach ca. 30 min ab.
- Dokumente liegen im Profil, nicht pro Bewerbung. Mehrere Bewerbungen nacheinander absenden und das Anschreiben jeweils tauschen.
- "Pflichtpraktikum" heißt dort teils "Praxissemester".

## Oracle Recruiting Cloud (z. B. Atruvia)
- E-Mail eingeben, Code per Mail. Ein Formular, "WEITERLEITEN" = Absenden.
- Nimmt nur EINE PDF (max. 5 MB) als Lebenslauf → hier ausnahmsweise Mappe mit `pdfunite` bauen, Anschreiben separat.

## dm / dmTECH
- Magic-Link-Login per Mail, gilt nur im Tab, in dem der Link geöffnet wurde. 15-min-Timer.
- Fragen-Textareas mit kleinem `maxLength` (z. B. 45/90/180).
- Uploads im Shadow DOM (`dm-upload#cv`, `#coverLetter`, `#attachments`).
- Ist die Stelle weg, ist die Bewerbungsseite leer (410).

## SAP
- jobs.sap.com ist unvollständig, besser careers.sap.com/search/?q=...&locationsearch=...
