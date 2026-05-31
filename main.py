#!/usr/bin/env python3
"""
NRW VC Bewerbungstool - Desktop Application
Startet das Fenster und initialisiert alle Systeme.
"""
import sys
import os
import webview

# Pfad zu gebündelten Dateien (PyInstaller) oder aktuellem Verzeichnis
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

def main():
    from database import init_db
    from api import BewerbungAPI

    # Datenbank initialisieren
    init_db()

    # Python ↔ JavaScript Brücke
    api = BewerbungAPI()

    # Pfad zur HTML-Datei
    html_path = os.path.join(BASE_PATH, 'index.html')
    if sys.platform == 'win32':
        url = f'file:///{html_path.replace(os.sep, "/")}'
    else:
        url = f'file://{html_path}'

    # Fenster erstellen
    window = webview.create_window(
        title='⬡ NRW VC — Team Bewerbungstool v4.0',
        url=url,
        js_api=api,
        width=1440,
        height=900,
        min_size=(1100, 700),
        confirm_close=True,
        background_color='#05080f',
        text_select=False,
    )

    webview.start(
        debug=False,
        # gui='cef'  # Auskommentieren für CEF/Chromium; Standard = Edge WebView2 auf Win10/11
    )

if __name__ == '__main__':
    main()
