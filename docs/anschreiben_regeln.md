# Anschreiben-Regeln (kompakt)

Kurzfassung von `anschreiben_protokoll.md` (Hintergrund und Recherche). Gilt für Agent und Mensch. `tools/anschreiben.py` prüft die mechanischen Punkte automatisch.

## 1. Wann ein Anschreiben
- Verlangt → vollständig schreiben.
- Optional, aber starker Hebel (dünner CV, Quereinstieg, Pflichtpraktikum erklärungsbedürftig, echtes Interesse) → kurz und sehr konkret, 180 bis 240 Wörter.
- Portal hat nur ein Freitextfeld → gleiche Prinzipien, höchstens 90 % von `maxLength`.
- Anzeige verzichtet ausdrücklich → keins, stattdessen CV pro Stelle.

## 2. Vor dem Schreiben (aus `stellenanzeige.md`)
Rolle und Kennziffer (Betreff), Ansprechpartner (Name statt "Damen und Herren", wenn auffindbar), Unternehmenstyp und Du/Sie (Konzern und Mittelstand meist Sie, Startup der Anzeige folgen), die 2 bis 3 wichtigsten Aufgaben, Start, Dauer, Stunden, Pflichtpraktikum oder freiwillig, Sprache der Anzeige. Ein Anker pro Firma (Produkt, Team, Tech-Stack aus Anzeige oder Karriereseite). Der Text muss beim Austausch des Firmennamens kaputtgehen.

## 3. Aufbau, 180 bis 280 Wörter, eine Seite
1. **Einstieg** (2–3 Sätze). Wer schreibt, warum genau diese Stelle, stärkster Match. Muster wechseln: Studium und Aufgabe, konkreter Nutzen für die Aufgabe, Produktanker. Kein "Hiermit bewerbe ich mich", kein "Im Rahmen meines Studiums".
2. **Belege** (4–5 Sätze, höchstens 110 Wörter). Höchstens 2 Belege, einer aus der Praxis, einer aus Projekt oder Studium. Jeweils Kontext, was wirklich getan wurde (Tools aus dem Profil, die auch in der Anzeige stehen), Nutzen für die neue Stelle. Den Lebenslauf nicht wiederholen.
   Fehlt eine Kernanforderung: übertragbare Basis nennen, Lücke kurz und ehrlich, Einarbeitung zusagen (am besten mit Lern-Beleg aus dem Profil). Nie entschuldigend.
3. **Warum diese Firma** (2–3 Sätze). Anker aus Abschnitt 2, verbunden mit der eigenen Entwicklung. Was ergänzt sich, nicht nur "ich will lernen".
4. **Rahmen und Schluss** (2–3 Sätze). Start, Stunden pro Woche, Dauer oder Studienende. Gehaltswunsch nur, wenn gefordert. Schluss im Indikativ ("Auf ein Gespräch freue ich mich."), kein Konjunktiv.

## 4. Stil (Anti-KI)
- Keine Doppelpunkte in Sätzen, kein `—`, kein ` – ` im Satz. Bereiche wie 15–20 sind erlaubt.
- Verboten sind Floskeln wie "Mit großem Interesse", "neue Herausforderung", "würde mich freuen", "positive Rückmeldung" (hart geprüft).
- Vermeiden (nur Warnung): eintauchen, navigieren, Bereicherung, innovativ, fundiert, leidenschaftlich, zügig, teamfähig ohne Beleg, "nicht nur … sondern auch", Dreier-Adjektivketten.
- Kurze und mittellange Sätze mischen, aktiv statt Nominalstil. Höchstens 2 Sätze mit "Ich" am Anfang, nie direkt hintereinander.
- Englisch: gleiche Regeln, eigene Wortliste (delve, leverage, passionate about, thrilled to apply …).

## 5. Fakten
Jede Erfahrung, jedes Tool, jede Zahl muss in `profil.md` stehen. Keine Stufen verstärken (Grundkenntnisse bleiben Grundkenntnisse). Keine Beispiele aus diesem Dokument oder dem Protokoll übernehmen, sie gehören nicht der Person.

## 6. Kontrolle vor dem Bauen
- [ ] Alles belegt, keine erfundene Zahl
- [ ] Firma, Stelle, Ansprechpartner, Sprache stimmen, keine Reste
- [ ] Einstieg hat keine Floskel und nennt den stärksten Match
- [ ] Höchstens 2 Belege, jeder mit Nutzen für die Aufgabe
- [ ] Anker ist firmenspezifisch (Austausch-Test)
- [ ] Start, Stunden, Dauer stehen drin
Dann `tools/anschreiben.py` ausführen, Fehler beheben, Warnungen lesen.
