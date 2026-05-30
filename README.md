# 🇩🇪 GER | NRW VC 🎙 — Team Bewerbungssystem
### Offizielles Bewertungstool für Team-Aufnahmegespräche · Version 4.0

---

## 📋 Inhaltsverzeichnis

1. [Schnellstart](#schnellstart)
2. [Was ist das Tool?](#was-ist-das-tool)
3. [Punktesystem](#punktesystem)
4. [Bewertungsskala](#bewertungsskala)
5. [Features im Überblick](#features-im-überblick)
6. [Bedienung](#bedienung)
7. [Tastaturkürzel](#tastaturkürzel)
8. [Abschlussbericht](#abschlussbericht)
9. [Archiv & Statistiken](#archiv--statistiken)
10. [Export & Import](#export--import)
11. [Einstellungen](#einstellungen)
12. [Technische Hinweise](#technische-hinweise)

---

## Schnellstart

### Windows
1. ZIP-Datei entpacken
2. `START.bat` doppelklicken
3. Browser öffnet sich automatisch auf `http://localhost:8080`

### Mac / Linux
```bash
python3 start_server.py
```
Dann im Browser: **http://localhost:8080**

> **Hinweis:** Python 3 muss installiert sein. Download unter https://www.python.org

---

## Was ist das Tool?

Das **GER | NRW VC Team Bewerbungssystem** ist ein lokales Webtool zur strukturierten Durchführung und Auswertung von Team-Aufnahmegesprächen. Es ersetzt manuelle Punktelisten und Excel-Tabellen durch eine professionelle, animierte Oberfläche mit automatischer Auswertung.

**Für wen ist es gedacht?**
- Interviewer und High-Teamler die Aufnahmegespräche führen
- Serverleitung die Bewerbungen auswerten möchte
- Teams die ein einheitliches, nachvollziehbares Bewerbungsverfahren wollen

---

## Punktesystem

Das Bewerbungsgespräch besteht aus **zwei Sektionen**:

### 🧠 Sektion 1 — Sachliche Fragen (15 Fragen)
| Punkte | Bedeutung |
|--------|-----------|
| **0** | Keine / völlig falsche Antwort |
| **1** | Schwache, unvollständige Antwort |
| **2** | Oberflächlich, Grundverständnis vorhanden |
| **3** | Solide Antwort, wesentliche Punkte genannt |
| **4** | Sehr gute, vollständige Antwort |
| **5** | Herausragend — alle Aspekte, Beispiele, Eigeninitiative |

**Maximum: 15 × 5 = 75 Punkte**

---

### 🎭 Sektion 2 — Ingame-Situationsfragen (10 Fragen)
| Punkte | Bedeutung |
|--------|-----------|
| **0** | Falsche oder keine Reaktion |
| **1** | Teilweise richtig, wesentliche Schritte fehlen |
| **2** | Gute Reaktion, kleiner Fehler oder fehlender Schritt |
| **3** | Perfekte Reaktion — korrekt, professionell, vollständig |

**Maximum: 10 × 3 = 30 Punkte**

---

### ⚖️ Bonus- und Maluspunkte

| Bonus | Punkte |
|-------|--------|
| Hervorragendes Regelwissen | +5 |
| Sehr professionelles Auftreten | +5 |
| Ausgezeichnete Situationsreaktion | +5 |
| Besondere Teamfähigkeit | +5 |

| Malus | Punkte |
|-------|--------|
| Arrogantes / respektloses Verhalten | -5 |
| Lücken im Grundregelwerk | -5 |
| Widersprüchliche Aussagen | -10 |
| Unehrlichkeit | -10 |

---

### ◈ Live-Bewertung (5 Kategorien, je 0–5 Punkte)
- Auftreten & Professionalität
- Sprachqualität im VC
- Ruhe unter Druck
- Teamgefühl & Sympathie
- Ehrlichkeit & Reflektiertheit

**Maximum Live: 5 × 5 = 25 Punkte**

---

### 📊 Gesamtpunkte

| Sektion | Max. Punkte |
|---------|-------------|
| Sachliche Fragen | 75 |
| Situationsfragen | 30 |
| Bonus/Malus | variabel |
| Live-Bewertung | 25 |
| **Gesamt (ohne B/M)** | **105** |

---

## Bewertungsskala

| Punkte | Ergebnis | Bedeutung |
|--------|----------|-----------|
| **95–105** | ⭐ Herausragend | Absoluter Top-Kandidat. Sehr reflektiert, konstant starke Antworten, hohe RP-Reife, klare Führungsqualität. |
| **88–94** | ✅ Sehr gut | Klar geeignet. Überwiegend sehr starke Leistungen, nur geringe Schwächen. Echter Mehrwert fürs Team. |
| **78–87** | 👍 Bestanden | Geeignet. Gute Grundlagen und Verständnis, aber noch Luft nach oben (Tiefe, Konsequenz, Sicherheit). |
| **68–77** | ⚠️ Knapp bestanden | Grenzbereich. Potenzial vorhanden, jedoch erkennbare Unsicherheiten. Weitere Prüfung empfohlen. |
| **58–67** | ❌ Nicht bestanden | Mehrere relevante Schwächen. Reife, Regelverständnis oder Verantwortungsbewusstsein unzureichend. |
| **0–57** | 🚫 Deutlich ungeeignet | Wichtige Grundlagen fehlen (Regeln, Verhalten, Konfliktlösung). Aktuell nicht einsetzbar. |

> Die Skala bezieht sich auf die **Basispunkte** (Fragen + Bonus/Malus). Live-Punkte werden zusätzlich addiert.

---

## Features im Überblick

### 🎤 Gesprächsführung
- **Gesprächs-Timer** — Startet automatisch beim Beginn, wird im Bericht gespeichert. Gelb bei 30 min, Rot bei 60 min.
- **Notizen pro Frage** — Freitextfeld unter jeder Frage für eigene Anmerkungen
- **Notiz-Vorlagen** — Vorgefertigte Textbausteine per Klick einfügen (z.B. „Sehr gute Antwort", „Unsicher, hat gezögert")
- **Musterantworten** — Für jede der 25 Fragen hinterlegte Erwartungsantwort mit Mindestanforderungen
- **Fragen markieren** — Fragen für Nachbesprechung mit 🚩 flaggen
- **Kategoriefilter** — Nur Wissensfragen, Situationsfragen oder markierte Fragen anzeigen

### 📊 Auswertung
- **Echtzeit-Scorebar** — Immer sichtbar: Wissen, Situation, Bonus/Malus, Live, Gesamt + aktuelles Urteil
- **Prozentanzeige** — Jede Frage zeigt erzielte % des Maximums
- **Automatisches Fazit** — KI-generierter Empfehlungstext basierend auf allen Werten
- **Stärken/Schwächen-Analyse** — Top 3 beste und schwächste Antworten visuell hervorgehoben
- **Schwächen-Analyse mit Empfehlungen** — Konkrete Verbesserungshinweise je nach Bereich

### 📈 Diagramme (4 Charts)
- **Radar-Chart** — Wissen vs. Situation vs. Live-Eindruck als Prozent-Spinne
- **Doughnut-Chart** — Punkte-Verteilung der zwei Sektionen
- **Balken-Chart** — Anzahl Antworten je Punktwert (0–5)
- **Linien-Chart** — Score-Verlauf über alle 25 Fragen mit Durchschnittslinie

### 🗄️ Archiv & Verwaltung
- **Bewerber-Archiv** — Alle abgeschlossenen Gespräche dauerhaft gespeichert
- **Suche & Filter** — Nach Name suchen, nach Ergebnis filtern, nach Datum oder Score sortieren
- **Statistiken-Dashboard** — Gesamtauswertung aller Gespräche: Ø Score, Annahmequote, Trendlinie, häufigste Schwachstellen
- **Bewerber-Vergleich** — Im Bericht: aktueller Bewerber vs. alle Vorgänger als Balkendiagramm

### 💾 Speicherung & Export
- **Auto-Save** — Jede Eingabe wird automatisch im Browser gespeichert. Kein Datenverlust bei Seitenneuladen.
- **PDF-Export** — Vollständiger Bericht als professionelles PDF inkl. eingebetteter Diagramme
- **JSON-Export** — Rohdaten als JSON für Archivierung oder Weiterverarbeitung
- **JSON-Import** — Alten Export wieder laden und Bericht anzeigen
- **Unterbrochene Gespräche** — Nicht abgeschlossene Sessions werden erkannt und können fortgesetzt werden

### 🎨 Design & Bedienung
- **Dark / Light Mode** — Umschaltbar in den Einstellungen
- **Schriftgröße** — Klein / Mittel / Groß einstellbar
- **Sound-Feedback** — Subtile Töne bei Eingaben (deaktivierbar)
- **Konfetti-Animation** — Bei „Herausragend" (95+ Punkte)
- **Tastaturkürzel** — Komplette Steuerung ohne Maus möglich
- **Autovervollständigung** — Bekannte Bewerber-Namen werden vorgeschlagen

---

## Bedienung

### Schritt 1: Gespräch starten
1. Namen des Bewerbers eingeben
2. Datum auswählen (heute voreingestellt)
3. Interviewernamen eingeben (optional)
4. Allgemeine Notizen eintragen (optional)
5. **„Gespräch starten"** klicken → Timer startet automatisch

### Schritt 2: Fragen bewerten
- Frage **anklicken** um sie zu aktivieren (gelber Rahmen)
- Dann Punktzahl per **Klick auf den Button** oder **Tastatur (0–5 bzw. 0–3)** vergeben
- **„+ Notiz"** für eigene Anmerkungen zur Antwort
- **„+ Vorlage"** für vorgefertigte Textbausteine
- **„💡 Musterantwort"** für Erwartungsantwort und Mindestanforderungen
- **🚩** zum Markieren für spätere Nachbesprechung

### Schritt 3: Bonus, Malus, Live
- Bonus/Malus per **+/−** Buttons vergeben (mehrfach möglich)
- Live-Schieberegler für persönlichen Eindruck
- Allgemeine Gesprächsnotizen unten eintragen

### Schritt 4: Abschlussbericht
- **„Abschlussbericht →"** in der Score-Bar unten klicken
- Bericht wird mit animiertem Zähler, allen Diagrammen und automatischem Fazit aufgebaut
- **PDF exportieren**, **drucken** oder **JSON sichern**

---

## Tastaturkürzel

| Taste | Aktion |
|-------|--------|
| **0–5** | Ausgewählte Wissensfrage bewerten (max 5) |
| **0–3** | Ausgewählte Situationsfrage bewerten (max 3) |
| **Tab** | Nächste Frage auswählen |
| **Shift+Tab** | Vorherige Frage |
| **↑ / ↓** | Zwischen Fragen navigieren |
| **F** | Frage markieren / Markierung entfernen |
| **N** | Notizfeld öffnen / schließen |
| **H** | Musterantwort anzeigen |
| **?** | Shortcut-Übersicht anzeigen |
| **Esc** | Auswahl aufheben / Overlay schließen |

> Tastaturkürzel funktionieren nur wenn **kein Texteingabefeld** fokussiert ist.

---

## Abschlussbericht

Der Abschlussbericht enthält:

| Bereich | Inhalt |
|---------|--------|
| **Kopf** | Name, Datum, Interviewer, Gesprächsdauer |
| **Gesamtscore** | Animierter Zähler, Urteil mit Farbe und Erklärung |
| **Sektionsübersicht** | Wissen und Situation mit Fortschrittsbalken |
| **KPI-Kacheln** | Gesamt, Bonus/Malus, Live-Eindruck, Dauer |
| **Bewertungsskala** | Alle 6 Stufen mit Markierung des aktuellen Ergebnisses |
| **Stärken/Schwächen** | Top 3 beste und schwächste Antworten |
| **Markierte Fragen** | Alle 🚩-geflaggten Fragen zur Nachbesprechung |
| **Gesprächsnotizen** | Allgemeine Notizen des Interviewers |
| **Schwächen-Analyse** | Konkrete Verbesserungsempfehlungen |
| **Auto-Fazit** | Automatisch generierter Empfehlungstext |
| **4 Diagramme** | Radar, Doughnut, Balken, Linienchart |
| **Bewerber-Vergleich** | Vergleich mit Vorgänger-Bewerbern |
| **Detailauswertung** | Alle 25 Antworten mit Notizen, Bonus/Malus, Live |

---

## Archiv & Statistiken

### Archiv-Seite
- Zugriff über den **„Archiv"**-Tab oben in der Navigation
- **Suchfeld**: Bewerber nach Namen suchen
- **Filter**: Nach Ergebnis filtern (Herausragend, Sehr gut, Bestanden, Knapp, Nicht bestanden)
- **Sortierung**: Nach Datum (neuste zuerst) oder nach Score
- **Klick auf Eintrag**: Vollständigen Abschlussbericht öffnen
- **🗑️ Löschen**: Einzelne Einträge entfernen
- **„Archiv leeren"**: Alle Einträge löschen (mit Bestätigung)

### Statistiken-Dashboard
- Zugriff über den **„Statistiken"**-Tab
- Zeigt Auswertung über **alle bisherigen Gespräche**:
  - Gesamtanzahl Gespräche
  - Durchschnittsscore
  - Annahmequote (ab 78 Punkte = „Bestanden")
  - Höchster und niedrigster Score
  - Durchschnittliche Gesprächsdauer
  - Ergebnis-Tortendiagramm (Verteilung der 6 Stufen)
  - Score-Trendlinie (chronologischer Verlauf)
  - Top 8 schwächste Fragen über alle Bewerber

---

## Export & Import

### PDF Export
- Klick auf **„📄 PDF"** im Abschlussbericht
- Erstellt professionelles A4-Dokument mit:
  - NRW VC Branding und Header
  - Gesamtscore-Box mit Urteil
  - Alle 3 Diagramme eingebettet
  - Bewertungsskala mit Markierung
  - Alle 25 Fragen mit Scores, Prozent und Notizen
  - Bonus/Malus, Live-Bewertung, Gesprächsnotizen
  - Seitennummern und Footer
- Dateiname: `NRW_VC_[Name]_[Datum].pdf`

### JSON Export / Import
- **Export**: Klick auf **„⬇ JSON"** → speichert alle Rohdaten
- **Import**: Auf der Startseite **„⬇ JSON importieren"** → Datei auswählen → Bericht wird direkt angezeigt
- Nützlich für: Archivierung, Weitergabe, Backup
- Dateiname: `NRW_VC_[Name]_[Datum].json`

---

## Einstellungen

Erreichbar über das **⚙️-Symbol** oben rechts in der Navigation.

| Einstellung | Optionen |
|-------------|----------|
| **Farbschema** | 🌙 Dunkel (Standard) / ☀️ Hell |
| **Schriftgröße** | Klein / Mittel (Standard) / Groß |
| **Sound-Feedback** | An (Standard) / Aus |
| **Musterantworten** | An (Standard) / Aus |

Alle Einstellungen werden im Browser gespeichert und bleiben nach Neustart erhalten.

---

## Technische Hinweise

### Systemanforderungen
- **Python 3.6+** (für den lokalen Server)
- **Moderner Browser**: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **Internetzugang** beim ersten Start (für Google Fonts und Chart.js CDN)
- Nach dem ersten Laden funktioniert es auch weitgehend offline

### Datenspeicherung
- Alle Daten werden ausschließlich **lokal im Browser** gespeichert (`localStorage`)
- **Kein Server**, keine Cloud, keine externe Datenübertragung
- Daten bleiben beim Schließen des Browsers erhalten
- Beim **Löschen des Browser-Caches** gehen alle Daten verloren → vorher JSON exportieren!

### Archiv-Kapazität
- Maximal **50 Einträge** im Archiv (älteste werden automatisch entfernt)
- Statistiken basieren auf allen verfügbaren Einträgen

### Port ändern
Falls Port 8080 belegt ist, `start_server.py` öffnen und `PORT = 8080` anpassen.

---

## Häufige Fragen

**Q: Geht das auch ohne Internet?**
A: Ja, nach dem ersten Laden. Fonts und Charts werden beim ersten Aufruf gecacht. PDF-Export benötigt keine Verbindung.

**Q: Können mehrere Personen gleichzeitig das Tool nutzen?**
A: Ja, wenn sie beide den Server auf demselben PC verwenden (`http://localhost:8080`). Daten werden aber nicht synchronisiert.

**Q: Was passiert wenn ich die Seite versehentlich schließe?**
A: Das laufende Gespräch wird automatisch gespeichert. Beim nächsten Öffnen erscheint ein „Fortsetzen"-Link auf der Startseite.

**Q: Wie sichere ich das Archiv?**
A: Jeden Eintrag als JSON exportieren, oder alle auf einmal über die Browser-DevTools (`localStorage` exportieren).

**Q: Die Charts werden im PDF nicht angezeigt?**
A: Das PDF muss aus dem **Abschlussbericht** heraus exportiert werden (nicht aus dem Bearbeitungs-Bildschirm), damit die Charts geladen sind.

---

## Changelog

### v4.0 (aktuell)
- ✅ Alle Bugs behoben (sessNotes, Archiv-Index, Chart Memory Leaks)
- ✅ DOM-Cache für bessere Performance
- ✅ Debounced Updates bei Rapid-Input
- ✅ Globaler Error-Handler
- ✅ Robuste Archive-Daten mit ID-basierter Suche
- ✅ Sicherer JSON Import/Export
- ✅ 20/20 automatisierte Checks bestanden

### v3.0
- Musterantworten, Notiz-Vorlagen, % Anzeige
- Dark/Light Mode, Schriftgröße
- Archiv-Seite mit Suche, Filter, Sortierung
- Statistiken-Dashboard
- Radar-Chart, Schwächen-Analyse
- Autovervollständigung, JSON Import

### v2.0
- Auto-Save, Session-History
- Keyboard Shortcuts, Category Filter
- Konfetti, Sound-Feedback
- PDF mit eingebetteten Charts
- Stärken/Schwächen-Analyse

### v1.0
- Grundfunktionen: 25 Fragen, Timer, Bonus/Malus, Live-Bewertung
- Abschlussbericht mit Diagrammen

---

*© GER | NRW VC 🎙 — Team Bewerbungssystem · Alle Rechte vorbehalten*
