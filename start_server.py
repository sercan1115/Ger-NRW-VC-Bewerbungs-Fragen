#!/usr/bin/env python3
"""
High-Team Bewerbungstool – Lokaler Server
Starte dieses Skript und öffne dann http://localhost:8080 im Browser.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass  # Kein Output im Terminal

print("=" * 50)
print("  ⬡  HIGH-TEAM Bewerbungstool")
print("=" * 50)
print(f"  Server läuft auf: http://localhost:{PORT}")
print("  Drücke STRG+C zum Beenden.")
print("=" * 50)

webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server gestoppt. Auf Wiedersehen!")
        sys.exit(0)
