#!/usr/bin/env python3
"""
Lizenzsystem – Hardware-ID-Bindung + HMAC-SHA256 signierte Schlüssel.
Der Admin generiert Schlüssel mit keygen.py (privater Teil bleibt geheim).
Die App prüft nur – sie kennt den privaten Schlüssel NICHT.
"""
import hashlib
import hmac
import json
import base64
import struct
import platform
import uuid
import subprocess
from datetime import date, datetime

# ── SIGNING SECRET ────────────────────────────────────────────────────────────
# Aufgeteilt und verschleiert, damit einfache Binär-Analyse nicht sofort
# den kompletten Key findet. Vor Distribution bitte eigene Werte setzen!
_S0 = b'\x4e\x52\x57'          # "NRW"
_S1 = b'\x5f\x56\x43'          # "_VC"
_S2 = b'\x5f\x42\x45\x57'      # "_BEW"
_S3 = b'\x45\x52\x42\x55'      # "ERBU"
_S4 = b'\x4e\x47\x53\x54'      # "NGST"
_S5 = b'\x4f\x4f\x4c\x5f'      # "OOL_"
_S6 = b'\x32\x30\x32\x35'      # "2025"
_S7 = b'\x5f\x53\x45\x43'      # "_SEC"
_S8 = b'\x52\x45\x54\x4b'      # "RETK"
_S9 = b'\x45\x59\x58\x59\x5a'  # "EYXYZ"

def _signing_key() -> bytes:
    """Signing-Key aus Teilen zusammensetzen und hashen."""
    raw = _S0 + _S1 + _S2 + _S3 + _S4 + _S5 + _S6 + _S7 + _S8 + _S9
    return hashlib.sha256(raw).digest()


# ── HARDWARE ID ───────────────────────────────────────────────────────────────

def get_hardware_id() -> str:
    """
    Stabiler Hardware-Fingerabdruck.
    Kombiniert: MAC-Adresse + Maschinenname + (Windows) Festplatten-Seriennummer.
    Gibt 12-stelligen HEX-String zurück, z.B.  A3F2B1C09D4E
    """
    parts = []

    # 1. MAC-Adresse (stabielster Wert)
    mac = uuid.getnode()
    parts.append(f"{mac:012x}")

    # 2. Hostname (oft stabil)
    parts.append(platform.node().lower())

    # 3. Windows: Festplatten-Seriennummer via WMIC
    if platform.system() == 'Windows':
        try:
            r = subprocess.run(
                ['wmic', 'diskdrive', 'get', 'SerialNumber'],
                capture_output=True, text=True, timeout=4
            )
            lines = [l.strip() for l in r.stdout.splitlines() if l.strip()]
            if len(lines) > 1:
                parts.append(lines[1])
        except Exception:
            pass

    combined = "|".join(parts)
    return hashlib.sha256(combined.encode()).hexdigest()[:12].upper()


# ── ENCODING / DECODING ───────────────────────────────────────────────────────

def _pack(data: dict) -> str:
    """Payload → signierter Base32-Key-String."""
    payload = json.dumps(data, separators=(',', ':'), sort_keys=True).encode()

    sig = hmac.new(_signing_key(), payload, hashlib.sha256).digest()[:16]

    # Aufbau: 2 Byte Länge | Payload | 16 Byte Signatur
    blob = struct.pack('>H', len(payload)) + payload + sig
    encoded = base64.b32encode(blob).decode().rstrip('=')

    # Format: NRW-XXXXX-XXXXX-XXXXX-...
    chunks = [encoded[i:i+5] for i in range(0, len(encoded), 5)]
    return 'NRW-' + '-'.join(chunks)


def _unpack(key: str) -> dict | None:
    """Key-String → dict, oder None bei Fehler/Fälschung."""
    try:
        raw = key.upper().replace('NRW-', '').replace('-', '').replace(' ', '')
        pad = (8 - len(raw) % 8) % 8
        blob = base64.b32decode(raw + '=' * pad)

        if len(blob) < 3 + 16:
            return None

        length = struct.unpack('>H', blob[:2])[0]
        if len(blob) < 2 + length + 16:
            return None

        payload  = blob[2:2 + length]
        sig_stored = blob[2 + length:2 + length + 16]

        sig_check = hmac.new(_signing_key(), payload, hashlib.sha256).digest()[:16]

        if not hmac.compare_digest(sig_stored, sig_check):
            return None   # Signatur ungültig → gefälscht oder beschädigt

        return json.loads(payload.decode())
    except Exception:
        return None


# ── PUBLIC API ────────────────────────────────────────────────────────────────

def validate_license(key: str) -> dict:
    """
    Prüft einen Lizenzschlüssel vollständig.

    Gibt zurück:
      {'valid': True,  'role': ..., 'expiry': ..., 'name': ..., 'team': ..., 'hwid': ...}
      {'valid': False, 'error': '...'}
    """
    if not key or not key.upper().startswith('NRW-'):
        return {'valid': False, 'error': 'Kein gültiger NRW-Lizenzschlüssel'}

    data = _unpack(key)
    if data is None:
        return {'valid': False, 'error': 'Signatur ungültig – Schlüssel wurde manipuliert oder ist falsch'}

    # Ablaufdatum prüfen
    try:
        expiry = datetime.strptime(data['expiry'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        return {'valid': False, 'error': 'Ablaufdatum fehlt oder hat falsches Format'}

    if expiry < date.today():
        delta = (date.today() - expiry).days
        return {'valid': False, 'error': f'Lizenz abgelaufen (seit {delta} Tagen, am {data["expiry"]})'}

    # Hardware-ID prüfen (falls gebunden)
    if data.get('hwid'):
        current = get_hardware_id()
        if data['hwid'].upper() != current.upper():
            return {
                'valid': False,
                'error': (
                    f'Hardware-ID stimmt nicht überein.\n'
                    f'Lizenz: {data["hwid"]}\n'
                    f'Dieses Gerät: {current}\n\n'
                    f'Bitte wende dich an deinen Administrator.'
                )
            }

    days_left = (expiry - date.today()).days

    return {
        'valid':      True,
        'role':       data.get('role',  'VIEWER'),
        'expiry':     data.get('expiry', ''),
        'name':       data.get('name',  'Unbekannt'),
        'team':       data.get('team',  ''),
        'hwid':       data.get('hwid',  ''),
        'days_left':  days_left,
    }


def generate_license(name: str, role: str, expiry: str,
                     hwid: str = '', team: str = '') -> str:
    """
    Erstellt einen neuen signierten Lizenzschlüssel.
    Nur im keygen.py / Admin-Tool verwenden – NIEMALS in der verteilten App!
    """
    payload = {
        'name':   name,
        'role':   role,
        'expiry': expiry,
        'team':   team,
    }
    if hwid:
        payload['hwid'] = hwid.upper()
    return _pack(payload)
