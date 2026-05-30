#!/usr/bin/env python3
"""
High-Team Bewerbungstool – Lokaler Server
Starte dieses Skript und öffne dann die angezeigte URL im Browser.
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
        pass  # Kein Output im Terminal, um die Konsole sauber zu halten

def start_server():
    global PORT
    # Versuche Ports von 8080 bis 8089, falls einer belegt ist
    while PORT < 8090:
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print("=" * 50)
                print("  ⬡  HIGH-TEAM Bewerbungstool")
                print("=" * 50)
                print(f"  Server läuft auf: http://localhost:{PORT}")
                print("  Drücke STRG+C zum Beenden.")
                print("=" * 50)
                
                webbrowser.open(f"http://localhost:{PORT}")
                
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n  Server gestoppt. Auf Wiedersehen!")
                    sys.exit(0)
        except OSError as e:
            # Fehler 98 (Linux/Mac) oder 10048 (Windows): Port wird bereits genutzt
            if e.errno == 98 or e.errno == 10048:
                print(f"  Port {PORT} ist belegt, versuche {PORT + 1}...")
                PORT += 1
            else:
                raise
    
    print("Kein freier Port im Bereich 8080-8089 gefunden.")
    sys.exit(1)

if __name__ == "__main__":
    start_server()
