# Bewerbungspilot

Dein KI-Agent als Bewerbungshelfer für Werkstudentenjobs, Praktika und Abschlussarbeiten. Läuft mit **Claude Code** oder **Codex** (und anderen Agenten, die `AGENTS.md` lesen).

Was er kann:
- Stellen suchen und prüfen (passt Studiengang, Ort, Dauer?)
- Anschreiben als saubere PDF bauen, nur mit echten Fakten aus deinem Profil
- Bewerbungsformulare im Browser ausfüllen (optional), du klickst nur noch auf Absenden
- Tracker mit Übersichtsseite (`uebersicht.html`) und Abgleich mit deinen Mails (optional)

Deine persönlichen Daten (Profil, Tracker, Anschreiben) bleiben lokal auf deinem Rechner und landen nie im Repo.

## Schritt für Schritt

### 1. Voraussetzungen
- [Claude Code](https://claude.com/claude-code) **oder** [Codex CLI](https://github.com/openai/codex)
- Python 3
- tectonic und poppler für die PDFs
  - macOS: `brew install tectonic poppler`
  - Linux: tectonic laut [tectonic-typesetting.github.io](https://tectonic-typesetting.github.io), `sudo apt install poppler-utils`

Optional:
- Browser-Steuerung, damit der Agent Formulare ausfüllt. Für Claude Code ist das die Erweiterung [Claude in Chrome](https://claude.ai/chrome), für Codex z. B. ein Playwright-MCP.
- Gmail-Connector, damit Absagen und Einladungen automatisch erkannt werden.
- `agy` (Google Antigravity CLI), um Websuche und Textentwürfe auszulagern. Brauchst du nicht.

### 2. Repo holen
```sh
git clone https://github.com/muratonuryahsi-sudo/bewerbungspilot.git
cd bewerbungspilot
```

### 3. Agent starten und einrichten
```sh
claude      # oder: codex
```
Dann schreiben:
- Claude Code: `/einrichtung`
- Codex: `einrichtung starten`

Der Agent führt dich in 8 Schritten durch die Einrichtung (ca. 15–20 Minuten):
1. Überblick
2. Welcher Agent, Browser, Gmail, agy?
3. Programme prüfen
4. Lebenslauf einlesen, das spart Tipparbeit
5. Profil vervollständigen (Studium, Verfügbarkeit, Erfahrung, Skills, Suchkriterien)
6. Unterlagen-Ordner festlegen (Lebenslauf, Notenspiegel, Immatrikulation …)
7. Testlauf mit einem Probe-Anschreiben
8. Abschluss und Kurzanleitung

### 4. Benutzen
- Stellenlink schicken: `/bewerbung https://...` (Codex: einfach den Link schicken). Du bekommst eine Kurzbewertung, auf Wunsch ein Anschreiben, und mit "bewerben" füllt der Agent das Formular aus.
- `Jobs suchen`: Recherche nach deinen Suchkriterien
- `Status`: Mails abgleichen und Tracker aktualisieren
- `uebersicht.html` im Browser öffnen

Vor dem Absenden zeigt der Agent immer eine Zusammenfassung und wartet auf dein "senden". Logins, Einwilligungen und CAPTCHAs machst du selbst.

## Aufbau
| Datei / Ordner | Zweck |
|---|---|
| `AGENTS.md` | Regeln für jeden Agenten (`CLAUDE.md` verweist darauf) |
| `skills/einrichtung`, `skills/bewerbung` | Abläufe, verlinkt nach `.claude/skills` und `.agents/skills` |
| `vorlagen/` | Profil-, Einstellungs- und Anschreiben-Vorlage |
| `tools/` | Tracker, Anschreiben-Bau, Uploads, optional agy |
| `portale.md` | Erfahrungen mit Bewerbungsportalen (Taleo, Workday, StepStone …) |
| `profil.md`, `einstellungen.json`, `bewerbungen.json`, `bewerbungen/` | deine Daten, nur lokal (`.gitignore`) |

Neue Erkenntnisse zu Portalen gerne per Pull Request in `portale.md` teilen, aber ohne persönliche Daten.

## Hinweis für Windows
Die Skill-Ordner `.claude/skills` und `.agents/skills` sind Symlinks. Unter Windows `git config core.symlinks true` setzen (mit Entwicklermodus) oder die Ordner aus `skills/` dorthin kopieren.
