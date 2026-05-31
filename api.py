#!/usr/bin/env python3
"""PyWebView API v2 – JS ↔ Python Brücke."""
import json, os, tempfile, subprocess
import database as db
import license  as lic

ROLES      = ('OWNER', 'ADMIN', 'VIEWER')
ROLE_LVL   = {'OWNER': 3, 'ADMIN': 2, 'VIEWER': 1}


class BewerbungAPI:

    def __init__(self):
        self._user:    dict | None = None
        self._license: dict | None = None
        self._try_restore_license()

    def _try_restore_license(self):
        saved = db.get_license()
        if saved:
            r = lic.validate_license(saved['key'])
            if r['valid']:
                self._license = r

    def _has(self, *roles):
        return bool(self._user) and self._user.get('role') in roles

    def _lvl(self, n):
        return ROLE_LVL.get(self._user.get('role',''), 0) >= n if self._user else False

    @staticmethod
    def _ok(**kw):   return {'success': True,  **kw}
    @staticmethod
    def _err(msg):   return {'success': False, 'error': msg}

    # ── Lizenz ────────────────────────────────────────────────────────────────

    def get_hardware_id(self):
        return lic.get_hardware_id()

    def activate_license(self, key):
        r = lic.validate_license(key.strip())
        if r['valid']:
            db.save_license(key.strip(), r)
            self._license = r
            db.log('system', 'license_activated',
                   f'{r["name"]} | {r["role"]} | bis {r["expiry"]}')
        return r

    def get_license_info(self):
        return self._license

    # ── Auth ──────────────────────────────────────────────────────────────────

    def check_auth(self):
        # Lizenz bei jedem Check erneut validieren (Ablauf prüfen)
        if self._license:
            saved = db.get_license()
            if saved and not lic.validate_license(saved['key'])['valid']:
                self._license = None
                self._user    = None
        return {
            'licensed':  self._license is not None,
            'logged_in': self._user    is not None,
            'license':   self._license,
            'user':      self._uinfo(),
        }

    def _uinfo(self):
        if not self._user:
            return None
        return {
            'username': self._user['username'],
            'role':     self._user['role'],
            'is_default_admin':
                self._user['username'] == 'admin' and
                self._user.get('last_login') is None,
        }

    def login(self, username, password):
        if not self._license:
            return self._err('Keine gültige Lizenz aktiviert')
        user = db.verify_user(username.strip(), password)
        if not user:
            db.log(username, 'login_failed')
            return self._err('Benutzername oder Passwort falsch')
        self._user = user
        db.log(username, 'login', f'Rolle: {user["role"]}')
        return self._ok(
            username=user['username'],
            role=user['role'],
            is_default_admin=(
                user['username'] == 'admin' and user.get('last_login') is None
            )
        )

    def logout(self):
        if self._user:
            db.log(self._user['username'], 'logout')
        self._user = None
        return self._ok()

    def get_current_user(self):
        return self._uinfo()

    # ── Benutzerverwaltung ────────────────────────────────────────────────────

    def get_users(self):
        if not self._lvl(2):
            return self._err('Keine Berechtigung')
        return self._ok(users=db.get_users())

    def create_user(self, username, password, role):
        if not self._has('OWNER'):
            return self._err('Nur OWNER kann Benutzer erstellen')
        if role not in ROLES:
            return self._err('Ungültige Rolle')
        if len(password) < 6:
            return self._err('Passwort mind. 6 Zeichen')
        if len(username) < 2:
            return self._err('Benutzername mind. 2 Zeichen')
        r = db.create_user(username.strip(), password, role)
        if r['success']:
            db.log(self._user['username'], 'create_user', f'{username} | {role}')
        return r

    def set_user_role(self, uid, role):
        if not self._has('OWNER'):
            return self._err('Keine Berechtigung')
        if role not in ROLES:
            return self._err('Ungültige Rolle')
        db.set_user_role(uid, role)
        db.log(self._user['username'], 'set_role', f'uid={uid} → {role}')
        return self._ok()

    def deactivate_user(self, uid):
        if not self._has('OWNER'):
            return self._err('Keine Berechtigung')
        if self._user['id'] == uid:
            return self._err('Eigenen Account nicht deaktivierbar')
        db.deactivate_user(uid)
        db.log(self._user['username'], 'deactivate_user', f'uid={uid}')
        return self._ok()

    def reactivate_user(self, uid):
        if not self._has('OWNER'):
            return self._err('Keine Berechtigung')
        db.reactivate_user(uid)
        return self._ok()

    def change_password(self, new_password, target_username=''):
        if not self._user:
            return self._err('Nicht eingeloggt')
        if len(new_password) < 6:
            return self._err('Passwort mind. 6 Zeichen')
        target = (target_username
                  if (target_username and self._has('OWNER'))
                  else self._user['username'])
        db.change_password(target, new_password)
        db.log(self._user['username'], 'change_password', f'Ziel: {target}')
        return self._ok()

    # ── Sessions ──────────────────────────────────────────────────────────────

    def save_session(self, data_json):
        if not self._user:
            return self._err('Nicht eingeloggt')
        if not self._lvl(2):
            return self._err('VIEWER darf nicht speichern')
        try:
            data = json.loads(data_json)
            sid  = db.save_session(data, self._user['username'])
            db.log(self._user['username'], 'save_session',
                   f'{data.get("name","")} | {data.get("grand",0)} Pkt')
            return self._ok(id=sid)
        except Exception as e:
            return self._err(str(e))

    def get_sessions(self, search=''):
        if not self._user:
            return self._err('Nicht eingeloggt')
        rows = db.get_sessions(search=search,
                               username=self._user['username'],
                               role=self._user['role'])
        return self._ok(sessions=rows)

    def delete_session(self, sid):
        if not self._lvl(2):
            return self._err('Keine Berechtigung')
        db.delete_session(sid)
        db.log(self._user['username'], 'delete_session', f'id={sid}')
        return self._ok()

    def clear_all_sessions(self):
        if not self._has('OWNER'):
            return self._err('Nur OWNER kann alle Sessions löschen')
        db.clear_all_sessions()
        db.log(self._user['username'], 'clear_all_sessions')
        return self._ok()

    # ── Stats & Export ────────────────────────────────────────────────────────

    def get_stats(self):
        if not self._lvl(2):
            return self._err('Keine Berechtigung')
        stats = db.get_stats()
        if self._license:
            from datetime import date, datetime
            try:
                exp = datetime.strptime(self._license['expiry'], '%Y-%m-%d').date()
                stats['license_days_left'] = (exp - date.today()).days
                stats['license_name']      = self._license.get('name', '')
                stats['license_role']      = self._license.get('role', '')
                stats['license_expiry']    = self._license.get('expiry', '')
            except Exception:
                pass
        return self._ok(**stats)

    def export_sessions_csv(self):
        """Gibt CSV-String aller Sessions zurück."""
        if not self._lvl(2):
            return self._err('Keine Berechtigung')
        csv_data = db.sessions_as_csv()
        db.log(self._user['username'], 'export_csv')
        return self._ok(csv=csv_data)

    def open_db_folder(self):
        """Öffnet den Datenbank-Ordner im Explorer (Windows)."""
        if not self._has('OWNER'):
            return self._err('Keine Berechtigung')
        folder = os.path.dirname(db.DB_PATH)
        try:
            if os.name == 'nt':
                subprocess.Popen(['explorer', folder])
            else:
                subprocess.Popen(['xdg-open', folder])
        except Exception as e:
            return self._err(str(e))
        return self._ok()

    # ── Diverses ──────────────────────────────────────────────────────────────

    def get_audit_log(self, limit=100):
        if not self._lvl(2):
            return self._err('Keine Berechtigung')
        return self._ok(log=db.get_audit_log(min(limit, 500)))

    def get_app_info(self):
        return {
            'version':  '4.1',
            'hwid':     lic.get_hardware_id(),
            'db_path':  db.DB_PATH,
            'licensed': self._license is not None,
            'user':     self._uinfo(),
        }
