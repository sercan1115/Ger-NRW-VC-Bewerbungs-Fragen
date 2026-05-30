# ⬡ High-Team Bewerbungstool (GER | NRW VC)

Ein maßgeschneidertes, hochperformantes und rein lokales Web-Tool zur professionellen Evaluierung, Zeitmessung und statistischen Auswertung von Team-Bewerbungsgesprächen. 

Dieses Tool wurde speziell für das **High-Team** entwickelt, um Bewerbungsprozesse zu standardisieren, objektive Scores zu ermitteln und strukturierte Daten für das Archiv bereitzustellen.

---

## 🚀 Key Features

- **Live-Scoring-System:** Intuitive Punktevergabe (0-5 und 0-3 Skalen) für verschiedene Bewertungskategorien mit automatischer Berechnung des Gesamtergebnisses.
- **Integrierter Interview-Timer:** Behalte die Zeit während des Gesprächs immer im Blick (Start, Pause, Reset) inklusive optischer Fortschrittsanzeige.
- **Stärken- & Schwächen-Analyse:** Automatisch generierte Fazite basierend auf den vergebenen Punktzahlen, um Schwachstellen und Spitzenleistungen sofort zu identifizieren.
- **Echtzeit-Statistiken:** Interaktive Diagramme (unter Nutzung von Chart.js) zeigen die häufigsten Schwachstellen und Durchschnittswerte im Verlauf aller Bewerbungen.
- **Daten-Exporte:**
  - 📄 **PDF-Export:** Generiert direkt im Browser einen sauberen, druckfertigen Bewertungsbogen (via jsPDF).
  - 💾 **JSON-Backup:** Exportiere und importiere Bewerbungsdaten, um sie im Team zu teilen oder extern zu sichern.
- **Modernes Interface:** Vollständig optimiertes Dark-Theme, anpassbare Musterlösungen und integrierte Tastaturkürzel für schnelle Bedienung während des Interviews.

---

## 🛠️ Tech Stack

- **Backend:** Python 3 (Standardbibliothek, keine externen Abhängigkeiten notwendig)
- **Frontend:** HTML5, CSS3 (Custom Properties, responsive Layouts), Vanilla JavaScript
- **Bibliotheken:** Chart.js (via CDN für Statistiken), jsPDF (via CDN für PDF-Generierung)

---

## 💻 Installation & Start

Da das Tool als lokaler Server konzipiert wurde, ist keine aufwendige Installation oder Internetdatenbank nötig. Alle Daten verbleiben sicher auf deinem lokalen Rechner.

### Voraussetzungen
- Installiertes **Python 3.x**

### Schritt-für-Schritt Startanleitung

1. **Repository herunterladen / klonen:**
   Lade die Spieldateien in einen gemeinsamen Ordner herunter.
   
2. **Server starten:**
   Öffne dein Terminal (Eingabeaufforderung / PowerShell) in diesem Ordner und führe das Start-Skript aus:
   ```bash
   python start_server.py
