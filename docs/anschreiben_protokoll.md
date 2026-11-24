# Evidenzbasiertes Anschreiben-Protokoll (DACH-Markt) & Umbau-Spezifikation für `bewerbungspilot`

> **Zweck dieses Dokuments:** Dieses Protokoll fasst empirische Recruiting-Studien (primär DACH-Raum, ergänzt um internationale Feldexperimente), Eye-Tracking-Erkenntnisse und Recruiter-Feedback (2024–2026) zusammen und übersetzt sie in ein **striktes Ausführungsprotokoll** für KI-Agenten (insb. Claude) sowie einen **konkreten Architektur-Umbauplan** für das Repository `bewerbungspilot`.
>
> **Zielgröße:** Maximierung der **Einladungsquote zum Bewerbungsgespräch** für Werkstudentenstellen, Praktika, Abschlussarbeiten und Berufseinstieg im deutschen Arbeitsmarkt – bei 100 % Faktentreue und 0 % KI-Klang.

---

## Teil A: Empirische Datenlage – Was Recruiter in Deutschland wirklich bewerten

### 1. Stellenwert & Realität des Anschreibens (Zahlen & Studien)

| Kennzahl / Befund | Quelle | Strategische Konsequenz |
|---|---|---|
| Nur noch ca. **55 %** der Unternehmen in Deutschland verlangen ein Anschreiben verpflichtend; ca. **34 %** der Personaler stufen es als allein entscheidend ein. | StepStone (*Hiring Trends / Application Quality*) | Anschreiben nur schreiben, wenn verlangt oder wenn es echten strategischen Mehrwert liefert (siehe Entscheidungsmatrix in Teil B). |
| **~68–75 %** des ersten Gesamteindrucks entfallen auf den Lebenslauf, **~20–22 %** auf das Anschreiben. Erstsichtung per Scan dauert **~6–7,4 Sekunden** (F-/Z-Muster). | Eye-Tracking-Studien (u. a. The Ladders, StepStone-Analysen) | Das Anschreiben wird **gescannt, nicht wie ein Roman gelesen**. Kurze Absätze (max. 3–4 Zeilen), starke Betreffzeile, starker 1. Satz, viel Weißraum. |
| Ein **maßgeschneidertes** Anschreiben steigert die Rückmelde-/Einladungsquote im Feldexperiment um bis zu **+53 %** (bzw. **+31 %** in weiteren Erhebungen) gegenüber Bewerbungen ohne bzw. mit generischem Anschreiben. **81 %** der Hiring Manager bevorzugen maßgeschneiderte gegenüber generischen Anschreiben. | ResumeGo (Feldexperiment), Zety / Employer-Umfragen | **Qualität schlägt Masse radikal.** Ein generisches Anschreiben schadet mehr als gar keines; ein gezieltes Anschreiben wirkt als starker Hebel. |
| **43–61 %** der Bewerbenden in Deutschland nutzen bereits KI (ChatGPT etc.) für Anschreiben. **54 %** der Personaler sagen, Anschreiben haben dadurch an Aussagekraft verloren; **72–80 %** klagen über austauschbare, mittelmäßige Unterlagen. | softgarden, StepStone, Statista (2024–2026) | Der Standard-KI-Ton ist heute **sofort verbrannt**. Wer natürlich, konkret und unternehmensspezifisch schreibt, sticht extrem aus der KI-Masse hervor. |
| **41 %** der deutschen Recruiter sortieren Bewerbungen **direkt aus**, wenn sie ein unreflektiert generiertes KI-Anschreiben erkennen. **72 %** lehnen mangelnde Individualisierung ab; **68–77 %** lehnen bei Rechtschreib-/Tippfehlern ab; bis zu **81 %** haben schon qualifizierte Kandidaten allein wegen Red Flags im Anschreiben abgelehnt. | softgarden (DE), Zety / ResumeLab | Ein einziges KI-Klischee, ein falscher Firmenname oder ein Copy-Paste-Fehler kann eine fachlich passende Bewerbung sofort töten. |
| **~70–76 %** der Arbeitgeber bevorzugen eine **halbe bis dreiviertel Seite** (**200–300 Wörter**). | ResumeGo / Employer-Umfragen / Career Services (TUM, RWTH, KIT) | **200–280 Wörter Fließtext** sind der empirische Sweet Spot. Niemals über 1 Seite, niemals über 300 Wörter. |

### 2. Das Zwei-Instanzen-Prinzip in Deutschland (HR vs. Fachabteilung)

Fast jede Bewerbung im deutschen Konzern- und Mittelstandsumfeld durchläuft **zwei völlig unterschiedliche Leser** – dasselbe Anschreiben muss beide bestehen:

1. **Instanz 1 – HR / Recruiter (Vorfilter, 10–30 Sekunden):**
   - Prüft **harte Rahmenbedingungen (KO-Kriterien)**: Studiengang, aktuelles Semester, Verfügbarkeit/Startdatum, Stunden/Woche (Werkstudent: 15–20 h/Woche im Semester) bzw. Pflichtpraktikum vs. freiwilliges Praktikum (Mindestlohngrenze / Studienordnung), Arbeitsort/Hybrid, Sprachniveau.
   - Prüft **Formalia & Sorgfalt**: Korrekte Anrede (Name aus Anzeige!), korrekter Firmenname, Kennziffer, fehlerfreies Deutsch/Englisch, kein Copy-Paste.
   - Prüft **echte Motivation („Warum wir?“)** und **Cultural Fit** (Tonfall passend zu Konzern/Mittelstand/Startup).
2. **Instanz 2 – Fachabteilung / Hiring Manager (Entscheider für das Gespräch):**
   - Interessiert sich kaum für allgemeine Motivation – will nur eine Frage beantwortet sehen: **„Nimmt diese Person unserem Team ab Woche 1–4 konkret Arbeit ab und versteht sie unsere Aufgaben/Tools?“**
   - Sucht nach **Belegen („Proof“)**: konkrete Projekte, Tools, Methoden, Code/Prozesse, messbare Ergebnisse oder reale Arbeitskontexte.
   - Reagiert extrem allergisch auf unbelegte Behauptungen (*„analytisch, schnell lernend, teamfähig“*) und übertriebene Versprechen.

### 3. ATS-Realität in Deutschland (Workday, SAP SuccessFactors, Taleo, Personio, Avature, softgarden)

- Das ATS parst primär den Lebenslauf, indiziert aber oft auch das Anschreiben für Volltextsuche/Matching-Scores.
- **Exakte Terminologie der Anzeige spiegeln** (nur dort, wo wirklich vorhanden!): Steht in der Anzeige „Qualitätssicherung“ oder „Continuous Integration“, genau diesen Ausdruck natürlich im Text verwenden.
- **Technisch sauberes PDF:** Reiner Text (markierbar), einspaltig, keine Tabellen/Textboxen/Grafiken, schwarz-weiß, **keine aktiven Inhalte** (`/URI`, `/Annots`, `/OpenAction`), Dateiname sauber (`Anschreiben_Vorname_Nachname_Firma.pdf` oder projektspezifische Konvention).

---

## Teil B: Das Anschreiben-Protokoll (Ausführungsstandard für Claude)

Jedes Anschreiben wird streng nach den folgenden **7 Phasen** erstellt. Keine Phase überspringen.

### Phase 0: Entscheidungsmatrix – Wann überhaupt ein Anschreiben erstellen?

| Fall | Handlung |
|---|---|
| Anschreiben in der Anzeige/im Portal **verlangt** | **Pflicht:** Vollständiges Anschreiben nach diesem Protokoll. |
| Anschreiben **optional**, aber **hoher Hebel** (Werkstudent/Praktikum mit dünnem CV, Quereinstieg/Studiengang-Schnittstelle, Pflichtpraktikums-Nachweis/Zeitraum erklärungsbedürftig, oder starkes individuelles Unternehmensinteresse) | **Empfohlen:** Knackiges, hochspezifisches Anschreiben (180–240 Wörter). |
| Portal bietet statt PDF ein **Freitextfeld** (z. B. KPMG ~600 Zeichen, dm-Fragen) | **Kompakt-Version:** Gleiche Prinzipien (Hook + 1 Beleg + Fit + Verfügbarkeit), exakt auf `maxLength` gekürzt (Puffer: max. 90 % von `maxLength`). |
| Anzeige sagt explizit **„Kein Anschreiben nötig / verzichte auf ein Anschreiben“** | **Kein Anschreiben** schicken – stattdessen Fokus voll auf den stellenspezifischen CV (`tools/cv.py`). |

---

### Phase 1: Stellenanzeigen-Dekonstruktion (vor dem ersten Satz)

Aus `stellenanzeige.md` werden vor dem Schreiben genau diese 7 Punkte extrahiert (intern als Arbeitsgrundlage, nicht als Fließtext im Brief):

1. **Rolle, Kennziffer & exakter Titel** (für Betreff).
2. **Ansprechpartner** (Name aus Anzeige, Karriereportal oder kurzer Webrecherche; nur wenn wirklich nicht auffindbar: „Sehr geehrtes Recruiting-Team,“ bzw. „Sehr geehrte Damen und Herren,“ – bei Du-Kultur: „Hallo [Vorname],“ oder „Hallo [Teamname]-Team,“).
3. **Unternehmenstyp & Kultur-Kalibrierung:**

| Unternehmenstyp | Ansprache | Tonfall | Fokus-Betonung |
|---|---|---|---|
| **Konzern** (DAX, Bosch, Siemens, Mercedes, SAP, ZEISS …) | Fast immer **Sie** (außer Anzeige duzt explizit) | Sachlich, klar, strukturiert, respektvoll, präzise | Verlässlichkeit, strukturierte Arbeitsweise, Einordnung in bestehende Teams/Prozesse, klare harte Fakten |
| **Mittelstand / Hidden Champion** (z. B. ARBURG, regionale Tech-KMU) | Meist **Sie** (Du nur wenn Anzeige klar duzt) | Bodenständig, direkt, verbindlich, pragmatisch | Anpacken (ohne das Buzzword „Hands-on“!), Vielseitigkeit, ehrliches Interesse am konkreten Produkt/Standort |
| **Startup / Scale-up / Digital-Unit** | Meist **Du** (der Anzeige folgen!) | Direkt, unbürokratisch, konkret, auf Augenhöhe | Eigeninitiative mit Beleg, Produktinteresse, schnelle Einarbeitung |

4. **Top-3-Kernaufgaben („Pain Points“):** Wobei braucht das Team konkret Entlastung? (Nicht alle 12 Bullets der Anzeige abklappern – nur die **2–3 wichtigsten** auswählen!)
5. **Muss- vs. Kann-Anforderungen + exakte Keywords:** Welche 2–3 Anforderungen aus der Anzeige passen am stärksten zu `profil.md`? Welche 1 relevante Lücke gibt es ggf.?
6. **Organisatorische Pflichtangaben:** Startdatum, Dauer, Stunden/Woche, Pflichtpraktikum vs. freiwillig, Gehaltswunsch (nur wenn explizit gefordert!).
7. **Sprache der Anzeige:** Deutsch → Deutsch, Englisch → Englisch (britisch/amerikanisch konsistent, kompakter Cover-Letter-Stil).

---

### Phase 2: 3-Stufen-Unternehmensrecherche (gegen austauschbares „Warum wir?“)

Ein Satz wie *„Ihr innovatives Unternehmen begeistert mich“* ist wertlos. Vor dem Schreiben wird ein **echter Unternehmensanker** gesucht (aus der Stellenanzeige selbst oder 1 kurzer gezielter Websuche zur Abteilung/zum Produkt):

- **Stufe 1 (Schwach – vermeiden):** Allgemeine Aussagen (*„Marktführer“, „innovativ“, „internationales Umfeld“*).
- **Stufe 2 (Gut – Standardziel):** Bezug auf ein **konkretes Produkt, eine konkrete Abteilung, einen Tech-Stack oder ein konkretes Aufgabengebiet** aus der Anzeige/Website (*„Die Kombination aus interner Qualitätssicherung und automatisierten Testabläufen in Ihrem Bereich X…“*).
- **Stufe 3 (Exzellent – maximaler Hebel):** Verbindung eines **konkreten Produkts/Projekts/Fokus des Unternehmens** mit einer **eigenen, belegten Erfahrung oder Studienvertiefung** (*„In meinem Studium habe ich mich im Projekt Y mit genau der Schnittstelle zwischen BPMN-Prozessen und Automatisierung beschäftigt, die in Ihrer Ausschreibung für das Team Z im Mittelpunkt steht.“*).

---

### Phase 3: Die 4-Absatz-Architektur (200–280 Wörter, max. 3–4 Zeilen pro Absatz)

> **Goldene Anti-Redundanz-Regel:** Das Anschreiben **wiederholt nicht den Lebenslauf**. Es wählt **maximal 2 starke Belege** (1x Praxiserfahrung, 1x Projekt/Studium) aus und übersetzt sie in **konkreten Nutzen für genau dieses Team**.

#### Layout-Kopf (DIN-5008-orientiert, sauber in LaTeX)
- **Absenderkopf:** Name, Adresse, Telefon, E-Mail (kein Foto, keine Links, schwarz-weiß).
- **Empfängeradresse:** Firma + Standort/Adresse.
- **Ort & Datum:** Rechtsbündig, aktuelles Datum (DE: `24. November 2026`, EN: `24 November 2026`).
- **Betreff (fett, ohne das Wort „Betreff:“):** Exakter Stellentitel + Kennziffer/Ref.-Nr. (falls vorhanden).
  - *Beispiel:* `Bewerbung als Werkstudent Qualitätssicherung & Testautomatisierung (Ref. 12345)`
- **Anrede:** Persönlich mit Komma am Ende → nächster Satz beginnt im Deutschen **klein** (außer bei Substantiv/Eigenname).

#### Absatz 1: Einstieg & Kernpassung (2–3 Sätze, ~40–55 Wörter)
**Ziel:** In 5 Sekunden klarmachen: *Wer schreibt hier, warum genau diese Stelle, was ist der stärkste Match?*
- **VERBOTEN:** „Hiermit bewerbe ich mich…“, „Mit großem Interesse habe ich…“, „Auf der Suche nach einer neuen Herausforderung…“, „Im Rahmen meines Studiums…“.
- **Formel (3 erprobte Einstiegsmuster – je nach Stelle variieren, nie immer denselben):**
  1. *Studium + direkter Aufgaben-Match:* `aktuell studiere ich [Studiengang] im [X.] Semester und verbinde im Arbeitsalltag bei [Firma] [konkrete Aufgabe] mit [Relevant-Skill] – genau diese Schnittstelle reizt mich an Ihrer Stelle im Bereich [Bereich].`
  2. *Konkreter Nutzen / Problembezug:* `wenn es darum geht, [konkrete Aufgabe aus Anzeige, z. B. Softwaretests sauber zu strukturieren und wiederkehrende Abläufe zu vereinfachen], bringe ich aus meiner Werkstudententätigkeit bei [Firma] direkte Praxis mit.`
  3. *Unternehmens-/Produktanker:* `an der ausgeschriebenen Position im Team [Team/Produkt] reizt mich besonders die Arbeit an [konkretes Thema aus Anzeige], da ich mich bereits im Studium und in der Praxis intensiv mit [verwandtes Thema] beschäftige.`
  *(Hinweis: Gedankenstrich `–` im obigen Muster 1 im fertigen Text durch Komma oder zwei kurze Sätze ersetzen – siehe Anti-KI-Regeln!)*

#### Absatz 2: Fachlicher Beweis 1 & 2 – „Behauptung + Beleg = Nutzen“ (4–5 Sätze, ~80–110 Wörter)
**Ziel:** Die **Fachabteilung** überzeugen. Nur die 2–3 wichtigsten Anforderungen aus Phase 1 bedienen.
- **Beleg-Formel (Mini-CAR: Context → Action → Result/Transfer):**
  - *Kontext:* Wo genau? (z. B. aktuelle Werkstudentenstelle, konkretes Hochschulprojekt)
  - *Aktion:* Was wurde **tatsächlich** gemacht? (exakte Tools/Methoden aus `profil.md`, die auch in der Anzeige stehen)
  - *Ergebnis / Nutzen für das neue Team:* Zahl, Effekt oder direkte Übertragbarkeit auf die ausgeschriebene Aufgabe.
- **Beispiel (Schlecht vs. Stark):**
  - ❌ *Schlecht (Floskel + KI):* „Ich verfüge über fundierte Kenntnisse in Python und bin äußerst analytisch sowie teamfähig. Dank meiner schnellen Auffassungsgabe kann ich mich zügig in komplexe Systeme einarbeiten.“
  - ✅ *Stark (konkret, belegt, natürlich):* „In meiner aktuellen Werkstudententätigkeit bei [Firma] plane und dokumentiere ich Softwaretests in Jira und vergleiche Datensätze in Excel, wodurch wir die Auswertung um rund ein Viertel verkürzen konnten. Zusätzlich habe ich in einem zweiköpfigen Hochschulprojekt eine REST-API mit Python, FastAPI und PostgreSQL aufgebaut und über GitHub Actions getestet. Diese Mischung aus sauberer Testarbeit und eigenem Code-Verständnis möchte ich bei Ihnen direkt in [Aufgabe aus Anzeige] einbringen.“
- **Ehrlicher Umgang mit einer relevanten Lücke (nur wenn eine Kernanforderung fehlt!):**
  - **Defizit-zu-Transfer-Formel (nie entschuldigend, nie „Obwohl mir leider fehlt…“):**
    1. Übertragbare Basis nennen.
    2. Lücke kurz, ehrlich, ohne Rechtfertigung benennen.
    3. Kurze Einarbeitung konkret zusagen (am besten mit Lern-Beleg).
  - ✅ *Stark:* „Mit [Tool X] habe ich bisher noch nicht direkt gearbeitet. Da ich mich im Studium bereits selbstständig in [ähnliches Tool Y] eingearbeitet habe, finde ich mich dort schnell zurecht.“

#### Absatz 3: Unternehmens-Fit – „Warum genau ihr?“ (2–3 Sätze, ~40–60 Wörter)
**Ziel:** Zeigen, dass dies **keine Serienbewerbung** ist.
- Konkreter Anker aus Phase 2 (Produkt, Abteilung, Arbeitsweise, Technologie, Branche oder Standort).
- Verbindung zur eigenen fachlichen Entwicklung / Motivation (authentisch, nicht schleimig!).
- Perspektivwechsel (**Du-/Sie-Perspektive statt reiner Ich-Perspektive**): Nicht nur *„Ich will bei Ihnen viel lernen“*, sondern *„Wie ergänzen sich mein Hintergrund und Ihre Aufgaben?“*.
- ❌ *Schlecht:* „Ihr Unternehmen gehört zu den führenden Anbietern und bietet spannende Entwicklungsmöglichkeiten, in denen ich meine Fähigkeiten weiter ausbauen möchte.“
- ✅ *Stark:* „An [Firma] spricht mich besonders an, dass [konkreter Aspekt, z. B. das Team interne Geschäftsprozesse direkt im eigenen Haus automatisiert statt nur Konzepte zu schreiben]. Genau an dieser praktischen Umsetzung möchte ich mitarbeiten und den Arbeitsalltag in einem [Produktions-/Software-/Beratungs-]Umfeld über mehrere Semester hinweg begleiten.“

#### Absatz 4: Rahmenbedingungen & klarer Abschluss (2–3 Sätze, ~30–50 Wörter)
**Ziel:** Alle HR-KO-Kriterien auf einen Blick beantworten + selbstbewusster Abschluss.
- **Verfügbarkeit präzise nennen:**
  - *Werkstudent:* Startdatum + Stunden/Woche im Semester (z. B. 15–20 Std./Woche) + ggf. Vollzeit in den Semesterferien + geplantes Studienende (zeigt langfristige Planbarkeit!).
  - *Pflichtpraktikum:* Startdatum + genaue Dauer laut Studienordnung + Hinweis „Pflichtpraktikum“.
  - *Gehaltswunsch:* **Nur** nennen, wenn in der Anzeige ausdrücklich gefordert (sonst weglassen!).
- **Abschlusssatz:** Indikativ, natürlich, ohne Konjunktiv.
  - ❌ *Schlecht:* „Über eine Einladung zu einem persönlichen Gespräch würde ich mich sehr freuen.“ / „Ich freue mich auf Ihre positive Rückmeldung.“
  - ✅ *Stark:* „Ich freue mich auf ein Gespräch, um gemeinsam zu schauen, wie ich Ihr Team unterstützen kann.“ oder schlicht: „Auf ein persönliches Gespräch freue ich mich.“
- **Grußformel:** `Mit freundlichen Grüßen` (kein Komma im Deutschen!) / `Kind regards,` (EN) + Name.

---

### Phase 4: Striktes Anti-KI- & Anti-Floskel-Regelwerk

Recruiter erkennen KI-Texte nicht über Detektoren, sondern an **Wortwahl, Satzrhythmus und fehlender Reibung**. Folgende Regeln gelten als **harte Ausschlusskriterien**:

#### 1. Verbotene KI-Wörter & Anglizismen-Übersetzungen („KI-Tells“)
- **Deutsch:** `eintauchen`, `navigieren`, `Bereicherung`, `facettenreich`, `versiert`, `synergistisch`, `nahtlos`, `maßgeblich`, `ganzheitlich`, `wegweisend`, `innovativ` (als leeres Firmenlob), `dynamisches Umfeld`, `spannende Herausforderung`, `Lösungsansatz` (inflationär), `fundiert`, `ausgeprägt`, `äußerst`, `leidenschaftlich`, `brenne für`, `zügig`, `zielorientiert`, `belastbar`, `hochmotiviert`, `Teamplayer` / `teamfähig` (ohne Beleg), `Hands-on-Mentalität`, `Mehrwert generieren`, `auf ein neues Level heben`.
- **Englisch:** `delve`, `navigate`, `tapestry`, `testament`, `realm`, `leverage` (inflationär), `seamless`, `passionate about`, `thrilled to apply`, `hit the ground running`, `fast-paced environment`, `dynamic team`, `proven track record`, `valuable asset`, `synergy`.

#### 2. Verbotene Floskeln & Phrasen
- `Hiermit bewerbe ich mich`
- `Mit großem Interesse habe ich` / `Mit großer Begeisterung`
- `I am writing to express my strong interest`
- `Schon immer war es mein Traum`
- `Auf der Suche nach einer neuen Herausforderung`
- `Im Rahmen meines Studiums` (als erster Satz)
- `Über eine Einladung würde ich mich sehr freuen` / jeder Konjunktiv im Schlusssatz (`würde`, `könnte`, `hätte`)
- `Auf Ihre positive Rückmeldung`
- `Bin ich davon überzeugt, eine ideale Besetzung / Bereicherung zu sein`

#### 3. Verbotene KI-Strukturmuster
- **Kein Em-Dash (`—`) und keine Gedankenstrich-Verschachtelungen (` – ... – `).**
- **Keine Doppelpunkte in Fließsätzen** (außer ggf. in der Betreffzeile bei `Ref.:`, besser komplett ohne).
- **Kein „Nicht nur X, sondern auch Y“-Schema** (klassisches LLM-Muster).
- **Keine Dreier-Adjektiv-Ketten** (*„strukturiert, zuverlässig und lösungsorientiert“*).
- **Keine identischen Absatzlängen oder weichgespülten Fazit-Sätze am Ende jedes Absatzes.**
- **Natürlicher Satzrhythmus:** Kurze Sätze (10–15 Wörter) mit mittellangen Sätzen (18–24 Wörter) mischen. Aktiv statt Passiv (*„Ich habe getestet“* statt *„Es wurden Tests durchgeführt“*). Kein Nominalstil (*„Bei der Durchführung der Analyse“* → *„Als ich die Daten ausgewertet habe“*).
- **Ich-Anapher vermeiden:** Nicht mehr als zwei Sätze im gesamten Text (und nie zwei direkt hintereinander) mit „Ich“ beginnen.

#### 4. Absolute Faktentreue (Halluzinations-Schutz)
- Jede Erfahrung, jedes Tool, jede Zahl und jede Studienangabe **muss wörtlich oder sinngemäß in `profil.md` (oder `cv_daten.json`) belegt sein**.
- Keine Verstärkung von Kompetenzstufen (wenn im Profil „Grundkenntnisse“ steht, darf daraus nie „sicherer Umgang“ oder „fundiert“ werden).
- Keine erfundenen Prozentzahlen oder Projektergebnisse.

---

## Teil C: Qualitäts-Gate & 100-Punkte-Selbstprüfung (vor Ausgabe)

Bevor Claude das Anschreiben baut und dem Nutzer vorlegt, wird der Entwurf gegen diese **8 Kriterien** geprüft. **Erst wenn kein K.-o.-Kriterium verletzt ist und ≥ 90/100 Punkte erreicht sind**, wird das PDF erzeugt.

### K.-o.-Prüfung (bei Verstoß sofort umschreiben)
- [ ] **0 erfundene Fakten/Zahlen/Tools** (100 % Deckung mit `profil.md`).
- [ ] **Korrekter Firmenname, Stellentitel, Ansprechpartner, Sprache** (0 Copy-Paste-Reste).
- [ ] **0 Wörter/Muster aus der Anti-KI- & Floskel-Sperrliste** (inkl. keine Doppelpunkte im Satz, kein `—`, kein Konjunktiv am Schluss).
- [ ] **Wortzahl im Korridor 180–280 Wörter** (hartes Limit: max. 300 Wörter), **exakt 1 Seite**, **keine aktiven PDF-Inhalte** (`/URI`, `/Annots`, `/OpenAction`).

### Qualitäts-Rubrik (100 Punkte)

| Kriterium | Max. Punkte | Prüffrage |
|---|---:|---|
| 1. Einstieg & Hook | 15 | Packt der erste Satz sofort ohne Standardfloskel und zeigt den stärksten Match? |
| 2. Belege statt Behauptungen | 25 | Sind mindestens 2 konkrete Belege (Kontext + Aktion + Ergebnis/Transfer) aus `profil.md` sauber mit den Top-Aufgaben der Anzeige verknüpft? |
| 3. Unternehmens-Fit („Warum wir?“) | 20 | Besteht der „Austausch-Test“? (Würde der Text kaputtgehen, wenn man den Firmennamen ersetzt? Wenn nein → zu generisch!) |
| 4. HR-Vollständigkeit | 10 | Sind Startdatum, Dauer/Stunden, Pflichtpraktikum/Werkstudentenstatus, Kennziffer und ggf. geforderte Angaben klar enthalten? |
| 5. Sprachnatürlichkeit & Rhythmus | 15 | Klingt der Text beim Lautlesen wie ein kluger, bodenständiger Mensch im DACH-Raum – ohne KI-Glätte, ohne Nominalstil, ohne Ich-Wiederholung? |
| 6. Kultur- & Tonfall-Passung | 10 | Passen Du/Sie und Tonfall exakt zu Konzern / Mittelstand / Startup und zur Stellenanzeige? |
| 7. Scannbarkeit & Optik | 5 | 4 luftige Absätze (je max. 3–4 Zeilen), kein Textblock, sauberes 1-Seiten-Layout? |

---

## Teil D: Konkreter Umbau-Plan für `bewerbungspilot`

Auf Basis der aktuellen Repo-Struktur sollten die folgenden gezielten Änderungen umgesetzt werden, damit `bewerbungspilot` dieses Protokoll **systematisch und technisch erzwingt** (statt nur auf Prompt-Disziplin zu hoffen):

### 1. Neues Referenzdokument im Repo anlegen
- **Datei:** `anschreiben_protokoll.md` (oder `docs/anschreiben_protokoll.md`, verlinkt aus `AGENTS.md` und `skills/bewerbung/SKILL.md`).
- Enthält das kompakte Regelwerk (Teile B & C), damit jeder Agent (Claude Code, Codex, Gemini CLI) dieselbe Quelle liest.

### 2. `tools/anschreiben.py` massiv aufwerten (Qualitäts-Gate + Robustheit)
Aktuell prüft `tools/anschreiben.py` nur `Pages == 1` und aktive PDF-Inhalte und erwartet manuelles LaTeX-Escaping.
**Konkrete Erweiterungen:**
1. **Automatisches `latex_escape()`** (analog zu `tools/cv.py`, ohne bereits escapte `\\` in `adresse` kaputtzumachen).
2. **Automatisches Qualitäts-Linting (`pruefe_text(spec)`) vor dem PDF-Bau:**
   - **Wortzahl-Check:** Warnung bei `< 170` oder `> 280` Wörtern, Fehler bei `> 310` Wörtern (Flag `--force` nur für begründete Ausnahmen).
   - **Sperrlisten-Check (DE & EN):** Harter Abbruch bei typischen KI-Wörtern/Floskeln (`hiermit bewerbe`, `mit großem interesse`, `eintauchen`, `navigieren`, `bereicherung`, `facettenreich`, `würde mich freuen`, `—`, `nicht nur .* sondern auch`, Doppelpunkt `:` im Fließtext).
   - **Platzhalter- & Hygiene-Check:** Abbruch bei `TODO`, `<<`, `>>`, `[Firma]`, `[Unternehmen]` oder fehlender Übereinstimmung von `spec["firma"]` im Text (Prüfung, ob die Firma im Anschreiben überhaupt vorkommt → Schutz gegen Copy-Paste).
   - **Absatz- & Rhythmus-Check:** Warnung, wenn ein Absatz > 85 Wörter lang ist (Textwüste) oder mehr als 2 Sätze hintereinander mit `Ich ` / `I ` beginnen.
   - **Fakten-/Zahlen-Schutz (optional gegen `profil.md`):** Warnung, wenn Prozentzahlen oder Jahreszahlen im Anschreiben vorkommen, die nicht in `profil.md` stehen (analog zum Ansatz in `AGENTS.md` für `cv.py`).
3. **Unterstützung für `kennziffer` & `ansprechpartner` in `spec.json`:** Optionales Feld `kennziffer`, das sauber im Betreff formatiert wird; Hinweis wenn generische Anrede verwendet wird.
4. **Dateinamen-Trennung gegen `cv.py`-Kollision:** `anschreiben_spec.json` (und `cv_spec.json` für `tools/cv.py`) als Konvention im Ordner `bewerbungen/<dir>/` festlegen, damit sich CV- und Anschreiben-Spec nicht überschreiben.
5. **Unit-Tests ergänzen:** Neue Datei `tests/test_anschreiben.py` (analog zu `tests/test_cv.py`), die Sperrliste, Wortzahl, Doppelpunkt-Check, Em-Dash-Check, Platzhalter-Check, LaTeX-Escaping und PDF-Bau testet.

### 3. `vorlagen/anschreiben.tex` typografisch verfeinern (DIN-5008-nah & ATS-sicher)
- `\usepackage{microtype}` ergänzen (deutlich saubererer Randausgleich und Lesbarkeit ohne aktive PDF-Inhalte).
- `\usepackage[left=2.5cm,right=2.0cm,top=2.0cm,bottom=2.0cm]{geometry}` (näher an DIN 5008 Form B, sauberer linker Anker für Eye-Tracking).
- Zeilenabstand leicht optimieren (`\linespread{1.08}`), `parskip` auf `8pt` – ergibt luftige, klar getrennte Absätze auf 1 Seite.
- Weiterhin strikt: schwarz-weiß, einspaltig, keine Links, kein `hyperref`, kein Foto, keine Boxen/Tabellen.

### 4. `skills/bewerbung/SKILL.md` & `AGENTS.md` aktualisieren
- **Bugfix in `skills/bewerbung/SKILL.md`:** Punkt `4b. CV pro Stelle` aus `## Jobsuche` in `## Neue Stelle` (zwischen Punkt 4 und 5) verschieben, wo Punkt 5 bereits mit `(siehe 4b)` darauf verweist.
- **Schritt 3 (`Anzeige sichern`) erweitern:** In `stellenanzeige.md` zusätzlich verpflichtend speichern: `Ansprechpartner`, `Kennziffer`, `Unternehmenstyp (Konzern/Mittelstand/Startup)`, `Ansprache (Du/Sie)`, `Top-3-Aufgaben`, `Unternehmensanker (1–2 Fakten über Produkt/Team)`.
- **Schritt 4 (`Anschreiben`) auf das neue Protokoll umstellen:**
  - Erst Entscheidungsmatrix prüfen (Pflicht / Optional mit Hebel / Portalfeld / Weglassen).
  - Dann 4-Absatz-Blueprint + Unternehmensanker + max. 2 Belege aus `profil.md` + ggf. Defizit-zu-Transfer-Formel.
  - Vor dem Bauen 100-Punkte-Selbstprüfung durchführen; erst danach `tools/anschreiben.py` ausführen (welches das technische Linting + PDF-Build übernimmt).
  - Im Chat dem Nutzer kurz zeigen: gewählte 2 Belege, Unternehmensanker, Wortzahl und ob Lücken adressiert wurden.

### 5. `vorlagen/profil.beispiel.md` gezielt ergänzen
Um starke Belege und Unternehmens-Fits ohne Erfinden zu ermöglichen, im Abschnitt `## Erfahrung` und `## Projekte` zwei kleine Felder ergänzen:
- `Konkretes Ergebnis / Wirkung (nur echte Fakten/Zahlen): TODO`
- `Lern-Beleg (Beispiel, wie du dich schnell in ein neues Tool eingearbeitet hast): TODO` (perfekt für die Defizit-zu-Transfer-Formel bei fehlenden Skills!).

### 6. `tools/agy.sh` synchronisieren
- Den veralteten Prompt im Modus `anschreiben` (z. B. die starre Regel `Erster Satz ... 'ich studiere ...'`) durch die neuen Protokoll-Regeln ersetzen (Kultur-Tonfall, 3 Einstiegsmuster, Mini-CAR-Belege, Unternehmensanker, erweiterte KI-Sperrliste, Wortzahl 200–280).

### 7. Kleinere Test-Hygiene im Repo mitbereinigen
- In `tests/test_overview.py` `@unittest.skipUnless(shutil.which("tectonic"), ...)` ergänzen (wie in `tests/test_cv.py`).
- In `tests/test_stage.py` `tearDown` mit `shutil.rmtree(self.t, ignore_errors=True)` ergänzen.

---

## Teil E: Direkt nutzbarer Übergabe-Prompt für Claude

Den folgenden Block kannst du zusammen mit diesem Protokoll direkt an Claude (z. B. in Claude Code im `bewerbungspilot`-Ordner) übergeben:

```text
Lies das beigefügte Dokument „Evidenzbasiertes Anschreiben-Protokoll (DACH-Markt) & Umbau-Spezifikation für bewerbungspilot“ vollständig durch.

Deine zwei Aufgaben:
1. Erneuere das Repository `bewerbungspilot` exakt auf Basis von Teil B, C und D dieses Protokolls:
   - Speichere das kompakte Anschreiben-Regelwerk (Teil B & C) im Repo und verlinke es aus `AGENTS.md` und `skills/bewerbung/SKILL.md`.
   - Erweitere `tools/anschreiben.py` um automatisches LaTeX-Escaping, das automatische Qualitäts- & Anti-KI-Linting (Wortzahl 180–280/max. 300, Sperrliste DE/EN, keine Doppelpunkte im Satz, kein Em-Dash, Platzhalter-/Firmennamen-Check, Absatzlängen-Check) und `tests/test_anschreiben.py`.
   - Verfeinere `vorlagen/anschreiben.tex` (DIN-5008-nahe Ränder, microtype, luftiges 1-Seiten-Layout, weiterhin strikt schwarz-weiß & ohne aktive Inhalte).
   - Aktualisiere `skills/bewerbung/SKILL.md` (inkl. Bugfix: Schritt 4b unter „Neue Stelle“ verschieben, `anschreiben_spec.json` vs. `cv_spec.json` trennen, Entscheidungsmatrix + 3-Stufen-Unternehmensrecherche + 100-Punkte-Gate integrieren).
   - Aktualisiere `vorlagen/profil.beispiel.md`, `tools/agy.sh` sowie die kleinen Test-Korrekturen (`test_overview.py`, `test_stage.py`).
   - Führe am Ende alle Unit-Tests aus (`python3 -m unittest discover -s tests -v`) und stelle sicher, dass alle bestehen.

2. Halte dich ab sofort bei jedem Anschreiben, das du für mich schreibst, strikt an dieses Protokoll (100 % Faktentreue zu `profil.md`, 0 % KI-Floskeln, erst ab Qualitäts-Score >= 90/100 bauen).

Erstelle zuerst einen kurzen Umsetzungsplan, welche Dateien du wie änderst, und setze ihn nach meiner Freigabe sauber um.
```
