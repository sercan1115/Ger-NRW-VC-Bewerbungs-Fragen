<div align="center">

```
███╗   ██╗██████╗ ██╗    ██╗    ██╗   ██╗ ██████╗
████╗  ██║██╔══██╗██║    ██║    ██║   ██║██╔════╝
██╔██╗ ██║██████╔╝██║ █╗ ██║    ██║   ██║██║
██║╚██╗██║██╔══██╗██║███╗██║    ╚██╗ ██╔╝██║
██║ ╚████║██║  ██║╚███╔███╔╝     ╚████╔╝ ╚██████╗
╚═╝  ╚═══╝╚═╝  ╚═╝ ╚══╝╚══╝       ╚═══╝   ╚═════╝
     Bewerbungstool  ·  Desktop Edition  v4.1
```

**Professionelles Bewerbungsgesprächs-Tool für Teams**  
*Lizenzverwaltung · Rollensystem · Signierte Keys · Hardware-Bindung*

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?style=flat-square&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)
![Version](https://img.shields.io/badge/Version-4.1-gold?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square)

</div>

---

## 📋 Inhaltsverzeichnis

- [Über das Projekt](#-über-das-projekt)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Voraussetzungen](#-voraussetzungen)
- [Installation & Build](#-installation--build)
- [Erster Start](#-erster-start)
- [Lizenzsystem](#-lizenzsystem)
- [Benutzerverwaltung](#-benutzerverwaltung)
- [Rollensystem](#-rollensystem)
- [Sicherheit](#-sicherheit)
- [Projektstruktur](#-projektstruktur)
- [Datenbank & Datenspeicherung](#-datenbank--datenspeicherung)
- [EXE-Schutz](#-exe-schutz)
- [Bekannte Einschränkungen](#-bekannte-einschränkungen)
- [Lizenz](#-lizenz)

---

## 🎯 Über das Projekt

Das **NRW VC Bewerbungstool** ist eine vollständige Desktop-Applikation zur strukturierten Durchführung, Bewertung und Archivierung von Bewerbungsgesprächen. Es wurde speziell für Teams entwickelt, die regelmäßig Bewerbungsgespräche führen und dabei eine einheitliche, nachvollziehbare Bewertung benötigen.

Die Anwendung läuft als native **Windows-EXE** ohne Browser oder Internetverbindung. Die gesamte Daten­verarbeitung erfolgt **lokal** – kein Cloud-Zugriff, keine Telemetrie.

> **Hinweis:** Der `NRW_VC_Keygen.exe` ist ausschließlich für den Administrator bestimmt und darf **niemals öffentlich verteilt** werden.

---

## ✨ Features

### 🎤 Gesprächsführung
- Strukturiertes Bewerbungsgespräch in zwei Sektionen (jeweils mit Bewertungsskala)
- Echtzeit-Score-Berechnung mit Bonus/Malus-System
- Live-Impression-Wertung
- Integrierter Timer mit Pause-Funktion
- Notizfeld für den Interviewer
- Automatische Empfehlung (Einladen / Absagen / Warteliste)

### 📦 Archiv
- Alle abgeschlossenen Gespräche werden in einer SQLite-Datenbank gespeichert
- Volltextsuche im Archiv
- Detailbericht pro Bewerber als PDF-Export (via jsPDF)
- CSV-Export aller Sessions über das Admin-Panel

### 🔐 Lizenzsystem
- **HMAC-SHA256 signierte Lizenzschlüssel** – fälschungssicher
- **Hardware-ID-Bindung** – verhindert Weitergabe der Lizenz
- Ablaufdatum pro Lizenz konfigurierbar (30 Tage bis 10 Jahre)
- Lizenzschlüssel-Generator mit History und Export (separater `Keygen.exe`)
- Automatische Prüfung beim App-Start

### 👥 Benutzerverwaltung
- Mehrbenutzerbetrieb mit individuellem Login
- Drei Rollen: `OWNER`, `ADMIN`, `VIEWER`
- Benutzer erstellen, deaktivieren, reaktivieren
- Passwörter jederzeit änderbar
- Vollständiger Audit-Log aller Aktionen

### ⚙ Admin-Panel (In-App)
- Übersichts-Dashboard (Sessions, Ø Score, Lizenz-Restlaufzeit)
- Benutzerverwaltung mit Rollenvergabe
- Archiv-Export als CSV
- Audit-Log mit Zeitstempel

---

## 🛠 Tech Stack

| Komponente | Technologie | Zweck |
|---|---|---|
| **GUI-Framework** | [PyWebView 5](https://pywebview.flowrl.com/) | Native Desktop-Fenster mit Web-Technologien |
| **Frontend** | HTML5, CSS3, Vanilla JS | Benutzeroberfläche |
| **Backend** | Python 3.10+ | Logik, Lizenz, Datenbank |
| **Datenbank** | SQLite 3 (stdlib) | Persistente Datenspeicherung |
| **Lizenzkrypto** | `hmac`, `hashlib` (stdlib) | HMAC-SHA256 Signierung |
| **Passwort-Hashing** | PBKDF2-HMAC-SHA256 (stdlib) | Sichere Passwort-Speicherung |
| **Charts** | Chart.js (CDN) | Statistik-Diagramme |
| **PDF** | jsPDF (CDN) | Berichts-Export |
| **Packaging** | PyInstaller 6 | EXE-Erstellung |
| **Admin-GUI** | Tkinter (stdlib) | Keygen-Oberfläche |

---

## 📦 Voraussetzungen

### Für die Ausführung (EXE)
- **Windows 10 oder 11** (64-bit)
- [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/) *(auf Win 10/11 meist vorinstalliert)*
- Keine weitere Installation notwendig

### Für den Build (Quellcode)
- **Python 3.10 oder höher** – [python.org](https://www.python.org/downloads/)
  - ⚠️ Beim Installieren **„Add Python to PATH"** aktivieren!
- **pip** (wird mit Python mitgeliefert)
- Optional: [UPX](https://upx.github.io/) für kleinere EXE (in `PATH` legen)

---

## 🚀 Installation & Build

### Option A – Vorkompilierte EXE verwenden
Die fertige EXE kann direkt heruntergeladen und gestartet werden.  
Kein Python, kein Build-Prozess notwendig.

### Option B – Selbst aus dem Quellcode bauen

**1. Repository klonen**
```bash
git clone https://github.com/DEIN-USERNAME/nrw-vc-bewerbungstool.git
cd nrw-vc-bewerbungstool
```

**2. Abhängigkeiten installieren**
```bash
pip install pywebview pyinstaller
```

**3. EXE bauen**
```bash
# Windows: Doppelklick auf build.bat
build.bat

# oder manuell:
pyinstaller build.spec
```

**4. Ergebnis**
```
dist/
├── NRW_VC_Tool_v4.exe    ← Haupt-App (verteilen)
└── NRW_VC_Keygen.exe     ← Admin-Tool (NUR für dich!)
```

> 💡 **Tipp:** Mit [Nuitka](https://nuitka.net/) statt PyInstaller erhält man eine stärkere Obfuskation (kompiliert zu nativem C-Code):
> ```bash
> pip install nuitka
> nuitka --standalone --onefile --windows-disable-console src/main.py
> ```

---

## 🎬 Erster Start

### Schritt 1 – Lizenz aktivieren

Beim ersten Start erscheint das Lizenz-Aktivierungsfenster:

```
┌─────────────────────────────────────────────┐
│  ⬡ NRW VC Bewerbungstool   Lizenz aktivieren│
│                                             │
│  Deine Hardware-ID                          │
│  ┌──────────────────────┐  [📋 Kopieren]   │
│  │  A3F2B1C09D4E        │                  │
│  └──────────────────────┘                  │
│                                             │
│  Lizenzschlüssel                            │
│  ┌──────────────────────────────────────┐  │
│  │ NRW-XXXXX-XXXXX-XXXXX-XXXXX-…       │  │
│  └──────────────────────────────────────┘  │
│                                             │
│              [  Aktivieren →  ]             │
└─────────────────────────────────────────────┘
```

**Hardware-ID ermitteln:**
- Die ID wird direkt im Aktivierungsfenster angezeigt → `📋 Kopieren` klicken
- Alternativ: `NRW_VC_Keygen.exe` auf dem Zielrechner starten → ID oben rechts ablesen
- Oder das folgende Skript auf dem Zielrechner ausführen:

```python
# hwid.py – Hardware-ID ermitteln
import hashlib, uuid, platform, subprocess

parts = [f"{uuid.getnode():012x}", platform.node().lower()]
try:
    r = subprocess.run(['wmic','diskdrive','get','SerialNumber'],
                       capture_output=True, text=True, timeout=4)
    lines = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    if len(lines) > 1: parts.append(lines[1])
except: pass

hwid = hashlib.sha256("|".join(parts).encode()).hexdigest()[:12].upper()
print("Hardware-ID:", hwid)
input()
```

### Schritt 2 – Lizenzschlüssel erstellen (`Keygen.exe`)

```
┌──────────────────────────────────────────────────────────────┐
│  Tab: Neue Lizenz                                            │
│                                                              │
│  Name:          [Thomas Müller                 ]             │
│  Organisation:  [GER | NRW VC                  ]            │
│  Rolle:         [ADMIN ▼]    Laufzeit: [1 Jahr ▼]           │
│                                                              │
│  ☑ An Hardware-ID binden                                    │
│  HWID: [A3F2B1C09D4E        ] [📋 Diese Maschine]           │
│                                                              │
│  [ 🔑 Lizenzschlüssel generieren ]                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ NRW-ABCDE-F1234-GHIJK-56789-LMNOP-QR               │   │
│  │ Name: Thomas Müller · Rolle: ADMIN · bis 2026-05-31 │   │
│  └──────────────────────────────────────────────────────┘   │
│  [ 📋 Schlüssel kopieren ]  ✓ In Zwischenablage kopiert!    │
└──────────────────────────────────────────────────────────────┘
```

Der generierte Schlüssel wird:
- In der **History** (`Tab: Erstellte Lizenzen`) dauerhaft gespeichert
- Kann jederzeit über **Doppelklick** erneut kopiert werden
- Kann als `.txt`-Datei **exportiert** werden

### Schritt 3 – Anmelden

Standard-Login beim ersten Start:

| Feld | Wert |
|---|---|
| Benutzername | `admin` |
| Passwort | `admin123` |

> ⚠️ **Sicherheitshinweis:** Das Standard-Passwort **sofort ändern!**  
> Die App erkennt automatisch, wenn das Standard-Passwort noch aktiv ist, und zeigt eine Warnung an.  
> Admin-Panel öffnen (⚙) → Tab **Passwort** → neues Passwort vergeben.

---

## 🔑 Lizenzsystem

### Funktionsweise

```
Admin (Keygen)                      App (User)
──────────────────────────────────────────────────────
1. HWID des Nutzers erhalten   →   User sendet HWID
2. Schlüssel generieren        →
3. Schlüssel an User senden    →   User trägt Key ein
                                   App prüft Signatur ✓
                                   App prüft Ablauf   ✓
                                   App prüft HWID     ✓
                                   → Zugang gewährt
```

### Schlüsselformat

```
NRW-ABCDE-F1234-GHIJK-56789-LMNOP-QR
│   └──────────────────────────────┘
│    Base32-kodierter Payload + HMAC-Signatur
└── Prefix zur Identifikation
```

Der Payload enthält:
- `name` – Name des Lizenznehmers
- `role` – Zugewiesene Rolle (OWNER / ADMIN / VIEWER)
- `expiry` – Ablaufdatum (YYYY-MM-DD)
- `hwid` – Hardware-ID (optional, bei Bindung)
- `team` – Organisation (optional)

### Laufzeit-Optionen

| Option | Dauer |
|---|---|
| Kurztest | 30 Tage |
| Standard | 90 / 180 Tage |
| Jahres-Lizenz | 365 Tage |
| 2-Jahres-Lizenz | 730 Tage |
| Unbegrenzt | 3.650 Tage (~10 Jahre) |
| Eigenes Datum | Frei wählbar |

### Hardware-ID Änderung

Tauscht ein Nutzer die Netzwerkkarte oder setzt den PC neu auf, ändert sich die Hardware-ID. In diesem Fall:
1. Neue HWID vom Nutzer anfordern
2. Neuen Schlüssel mit der neuen HWID generieren
3. Neuen Schlüssel zusenden

---

## 👥 Benutzerverwaltung

Neue Benutzer werden im **Admin-Panel** (⚙ oben rechts) unter **➕ Erstellen** angelegt.

```
Admin-Panel → Tab: Benutzer
──────────────────────────────────────────────────────────────
  thomas        👑 OWNER    Erstellt: 2025-01-15  Login: 2025-05-30
  [OWNER ▼]  [Deaktivieren]

  sarah         🛡 ADMIN    Erstellt: 2025-02-01  Login: 2025-05-29
  [ADMIN ▼]  [Deaktivieren]

  beobachter    👁 VIEWER   Erstellt: 2025-03-10  Noch nie eingeloggt
  [VIEWER ▼] [Deaktivieren]
──────────────────────────────────────────────────────────────
```

### Benutzer erstellen

```
Admin-Panel → Tab: ➕ Erstellen

  Benutzername: [thomas             ]
  Passwort:     [••••••••           ]
  Rolle:        [ADMIN ▼            ]

  [ Benutzer erstellen ]
  ✓ Benutzer "thomas" erfolgreich erstellt
```

### Passwort ändern

- **Eigenes Passwort:** Admin-Panel → Passwort → Feld leer lassen
- **Fremdes Passwort** (nur OWNER): Admin-Panel → Passwort → Benutzernamen eintragen

---

## 🎭 Rollensystem

| Berechtigung | 👑 OWNER | 🛡 ADMIN | 👁 VIEWER |
|---|:---:|:---:|:---:|
| Bewerbungsgespräch führen | ✅ | ✅ | ✅ |
| Sessions speichern | ✅ | ✅ | ❌ |
| Eigene Sessions einsehen | ✅ | ✅ | ✅ |
| Alle Sessions einsehen | ✅ | ✅ | ❌ |
| Benutzer erstellen | ✅ | ❌ | ❌ |
| Benutzer deaktivieren | ✅ | ❌ | ❌ |
| Rolle eines Benutzers ändern | ✅ | ❌ | ❌ |
| Fremde Passwörter ändern | ✅ | ❌ | ❌ |
| Alle Sessions löschen | ✅ | ❌ | ❌ |
| CSV-Export | ✅ | ✅ | ❌ |
| Audit-Log einsehen | ✅ | ✅ | ❌ |
| Admin-Panel öffnen | ✅ | ✅ | ❌ |

---

## 🔒 Sicherheit

### Passwort-Hashing

Alle Passwörter werden mit **PBKDF2-HMAC-SHA256** gehasht und gesalzen:

```python
# 310.000 Iterationen – weit über dem NIST-Minimum (Brute-Force-Schutz)
key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 310_000)
```

Das Klartext-Passwort wird **niemals** gespeichert.

### Lizenz-Signierung

Lizenzschlüssel werden mit **HMAC-SHA256** signiert:

```
Signatur = HMAC-SHA256(signing_key, json_payload)
```

- Der Signing-Key ist im Quellcode verschleiert (auf mehrere Variablen verteilt)
- Ohne den korrekten Signing-Key können keine gültigen Schlüssel erstellt werden
- Jede Manipulation am Schlüssel wird beim Prüfen erkannt

### Hardware-Bindung

Der Hardware-Fingerabdruck wird aus folgenden Komponenten berechnet:

```python
components = [
    f"{uuid.getnode():012x}",   # MAC-Adresse der Netzwerkkarte
    platform.node().lower(),    # Computername
    disk_serial_number,         # Festplatten-Seriennummer (Windows)
]
hwid = sha256("|".join(components))[:12].upper()
```

### Audit-Log

Jede sicherheitsrelevante Aktion wird geloggt:

```
Zeitpunkt            Benutzer   Aktion              Detail
───────────────────────────────────────────────────────────
2025-05-30 14:32     admin      login               Rolle: OWNER
2025-05-30 14:33     admin      create_user         thomas | ADMIN
2025-05-30 14:35     thomas     login               Rolle: ADMIN
2025-05-30 14:50     thomas     save_session        Max Müller | 87 Pkt
2025-05-30 15:10     admin      change_password     Ziel: thomas
```

---

## 📁 Projektstruktur

```
nrw-vc-bewerbungstool/
│
├── src/
│   ├── main.py          # Einstiegspunkt – PyWebView-Fenster
│   ├── license.py       # Lizenzsystem (HMAC, Hardware-ID)
│   ├── database.py      # SQLite-Datenbankschicht
│   ├── api.py           # JavaScript ↔ Python Brücke (PyWebView API)
│   ├── keygen.py        # Admin-Tool: Lizenzschlüssel-Generator
│   └── index.html       # Frontend (HTML/CSS/JS, Single-File-App)
│
├── build.spec           # PyInstaller-Konfiguration
├── build.bat            # Build-Skript (Windows)
├── requirements.txt     # Python-Abhängigkeiten
├── README.md            # Diese Datei
└── LICENSE              # Lizenzinformationen
```

### Laufzeit-Dateien (werden automatisch erstellt)

```
%APPDATA%\NRW_VC_Tool\
├── data.db                      # SQLite-Datenbank (Benutzer, Sessions, Log)
└── keygen_history.json          # History des Keygen (nur auf Admin-Maschine)
```

---

## 💾 Datenbank & Datenspeicherung

Die Datenbank liegt unter `%APPDATA%\NRW_VC_Tool\data.db` und enthält vier Tabellen:

```sql
-- Aktivierte Lizenz
CREATE TABLE license (id, key, role, name, expiry, hwid, team, activated);

-- Benutzerkonten (Passwörter als PBKDF2-Hash)
CREATE TABLE users (id, username, pw_hash, role, created_at, last_login, is_active);

-- Bewerbungssessions (vollständige JSON-Daten)
CREATE TABLE sessions (id, candidate, interviewer, date, score, sec1, sec2,
                       bm, live_pts, verdict, duration, notes, full_json,
                       created_by, created_at);

-- Audit-Log aller Aktionen
CREATE TABLE audit_log (id, user, action, detail, ts);
```

**Backup:** Den Ordner `%APPDATA%\NRW_VC_Tool\` regelmäßig sichern.  
**Pfad öffnen:** Admin-Panel → Archiv → „📂 Datenbankordner öffnen"

---

## 🛡 EXE-Schutz

| Maßnahme | Methode | Schutzgrad |
|---|---|---|
| Python-Bytecode verbergen | PyInstaller | ⭐⭐ |
| Dateikompression | UPX | ⭐ |
| String-Verschleierung | Signing-Key geteilt | ⭐⭐ |
| Kein Konsolenfenster | `console=False` | ⭐ |
| Nativer C-Code | Nuitka (optional) | ⭐⭐⭐⭐ |
| Bytecode-Verschlüsselung | PyInstaller `--key` | ⭐⭐⭐ |

**Maximaler Schutz mit Nuitka:**
```bash
pip install nuitka
nuitka --standalone --onefile \
       --windows-disable-console \
       --windows-product-name="NRW VC Bewerbungstool" \
       --windows-file-version="4.1.0.0" \
       src/main.py
```

> ⚠️ Kein Schutz ist vollständig unknackbar. Die eingesetzten Maßnahmen schützen effektiv gegen Gelegenheitsangriffe und automatisierte Tools.

---

## ⚠️ Bekannte Einschränkungen

- **Windows only** – PyWebView auf macOS/Linux benötigt andere GUI-Backends (getestet nur auf Windows 10/11)
- **Single-User-Modus** – Mehrere Benutzer können nicht gleichzeitig auf dieselbe Datenbankdatei zugreifen (kein Netzwerk-Modus)
- **WebView2 notwendig** – Auf sehr alten Windows-10-Versionen muss die [WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/) manuell installiert werden
- **HMAC vs. asymmetrische Signatur** – Der Signing-Key ist im Binary enthalten. Für maximale Sicherheit kann auf RSA/ECDSA (z.B. mit der `cryptography`-Library) umgestellt werden

---

## 📄 Lizenz

Copyright © 2025 NRW VC. Alle Rechte vorbehalten.

Dieses Projekt steht unter einer proprietären Lizenz.  
Siehe [`LICENSE`](./LICENSE) für Details.

---

<div align="center">

Entwickelt für **NRW VC** · Built with ❤️ and Python

</div>
