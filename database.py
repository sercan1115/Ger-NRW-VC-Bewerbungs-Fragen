#!/usr/bin/env python3
"""SQLite-Datenbankschicht v2 – mit Stats und CSV-Export."""
import sqlite3, hashlib, hmac, os, json, csv, io
from datetime import datetime

_APP_DIR = os.path.join(
    os.environ.get('APPDATA', os.path.expanduser('~')), 'NRW_VC_Tool')
DB_PATH = os.path.join(_APP_DIR, 'data.db')


def _conn():
    os.makedirs(_APP_DIR, exist_ok=True)
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA journal_mode=WAL')
    return c


def init_db():
    os.makedirs(_APP_DIR, exist_ok=True)
    with _conn() as c:
        c.executescript('''
            CREATE TABLE IF NOT EXISTS license (
                id INTEGER PRIMARY KEY,
                key TEXT NOT NULL, role TEXT NOT NULL,
                name TEXT, expiry TEXT, hwid TEXT, team TEXT,
                activated TEXT DEFAULT (datetime("now","localtime"))
            );
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                pw_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT "VIEWER",
                created_at TEXT DEFAULT (datetime("now","localtime")),
                last_login TEXT, is_active INTEGER DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                candidate TEXT NOT NULL, interviewer TEXT, date TEXT,
                score INTEGER DEFAULT 0, sec1 INTEGER DEFAULT 0,
                sec2 INTEGER DEFAULT 0, bm INTEGER DEFAULT 0,
                live_pts INTEGER DEFAULT 0, verdict TEXT,
                duration TEXT, notes TEXT, full_json TEXT,
                created_by TEXT,
                created_at TEXT DEFAULT (datetime("now","localtime"))
            );
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY, user TEXT, action TEXT,
                detail TEXT, ts TEXT DEFAULT (datetime("now","localtime"))
            );
        ''')
        if c.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
            c.execute('INSERT INTO users (username,pw_hash,role) VALUES (?,?,?)',
                      ('admin', _hash('admin123'), 'OWNER'))
            _log_raw(c, 'system', 'first_run',
                     'Standard-Admin erstellt: admin / admin123')


# ── Passwort ──────────────────────────────────────────────────────────────────

def _hash(pw):
    s = os.urandom(32)
    k = hashlib.pbkdf2_hmac('sha256', pw.encode(), s, 310_000)
    return s.hex() + ':' + k.hex()

def _verify(pw, stored):
    try:
        sh, kh = stored.split(':')
        k = hashlib.pbkdf2_hmac('sha256', pw.encode(), bytes.fromhex(sh), 310_000)
        return hmac.compare_digest(k, bytes.fromhex(kh))
    except Exception:
        return False


# ── Audit ─────────────────────────────────────────────────────────────────────

def _log_raw(conn, user, action, detail=''):
    conn.execute('INSERT INTO audit_log (user,action,detail) VALUES (?,?,?)',
                 (user, action, detail))

def log(user, action, detail=''):
    with _conn() as c:
        _log_raw(c, user, action, detail)


# ── Lizenz ────────────────────────────────────────────────────────────────────

def save_license(key, info):
    with _conn() as c:
        c.execute('DELETE FROM license')
        c.execute('INSERT INTO license (key,role,name,expiry,hwid,team) VALUES (?,?,?,?,?,?)',
                  (key, info.get('role',''), info.get('name',''),
                   info.get('expiry',''), info.get('hwid',''), info.get('team','')))

def get_license():
    with _conn() as c:
        r = c.execute('SELECT * FROM license ORDER BY id DESC LIMIT 1').fetchone()
        return dict(r) if r else None


# ── Benutzer ──────────────────────────────────────────────────────────────────

def verify_user(username, password):
    with _conn() as c:
        r = c.execute('SELECT * FROM users WHERE username=? AND is_active=1',
                      (username,)).fetchone()
        if not r or not _verify(password, r['pw_hash']):
            return None
        c.execute('UPDATE users SET last_login=? WHERE id=?',
                  (datetime.now().strftime('%Y-%m-%d %H:%M'), r['id']))
        return dict(r)

def get_users():
    with _conn() as c:
        return [dict(r) for r in c.execute(
            'SELECT id,username,role,created_at,last_login,is_active FROM users ORDER BY id'
        ).fetchall()]

def create_user(username, password, role):
    try:
        with _conn() as c:
            c.execute('INSERT INTO users (username,pw_hash,role) VALUES (?,?,?)',
                      (username, _hash(password), role))
        return {'success': True}
    except sqlite3.IntegrityError:
        return {'success': False, 'error': 'Benutzername bereits vergeben'}

def set_user_role(uid, role):
    with _conn() as c:
        c.execute('UPDATE users SET role=? WHERE id=?', (role, uid))

def deactivate_user(uid):
    with _conn() as c:
        c.execute('UPDATE users SET is_active=0 WHERE id=?', (uid,))

def reactivate_user(uid):
    with _conn() as c:
        c.execute('UPDATE users SET is_active=1 WHERE id=?', (uid,))

def change_password(username, new_pw):
    with _conn() as c:
        c.execute('UPDATE users SET pw_hash=? WHERE username=?',
                  (_hash(new_pw), username))


# ── Sessions ──────────────────────────────────────────────────────────────────

def save_session(data, created_by):
    with _conn() as c:
        cur = c.execute('''
            INSERT INTO sessions
              (candidate,interviewer,date,score,sec1,sec2,bm,live_pts,
               verdict,duration,notes,full_json,created_by)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            data.get('name',''), data.get('inter',''), data.get('date',''),
            data.get('grand',0), data.get('s1',0), data.get('s2',0),
            data.get('bm',0), data.get('live',0), data.get('verdict',''),
            data.get('duration',''), data.get('sessionNotes',''),
            json.dumps(data, ensure_ascii=False), created_by
        ))
        return cur.lastrowid

def get_sessions(search='', username='', role=''):
    with _conn() as c:
        q = f'%{search}%'
        if role == 'VIEWER':
            rows = c.execute(
                'SELECT * FROM sessions WHERE created_by=? AND candidate LIKE ? ORDER BY created_at DESC',
                (username, q)).fetchall()
        else:
            rows = c.execute(
                'SELECT * FROM sessions WHERE candidate LIKE ? ORDER BY created_at DESC',
                (q,)).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            if d.get('full_json'):
                try:
                    d['data'] = json.loads(d['full_json'])
                except Exception:
                    pass
            result.append(d)
        return result

def delete_session(sid):
    with _conn() as c:
        c.execute('DELETE FROM sessions WHERE id=?', (sid,))

def clear_all_sessions():
    with _conn() as c:
        c.execute('DELETE FROM sessions')

def sessions_as_csv():
    """Gibt alle Sessions als CSV-String zurück."""
    with _conn() as c:
        rows = c.execute(
            'SELECT candidate,interviewer,date,score,sec1,sec2,bm,'
            'live_pts,verdict,duration,created_by,created_at FROM sessions '
            'ORDER BY created_at DESC'
        ).fetchall()
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(['Bewerber','Interviewer','Datum','Gesamt','Sek1','Sek2',
                'B/M','Live','Ergebnis','Dauer','Erstellt von','Erstellt am'])
    for r in rows:
        w.writerow(list(r))
    return buf.getvalue()


# ── Statistiken ───────────────────────────────────────────────────────────────

def get_stats():
    with _conn() as c:
        users_total  = c.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        users_active = c.execute('SELECT COUNT(*) FROM users WHERE is_active=1').fetchone()[0]
        sessions_total = c.execute('SELECT COUNT(*) FROM sessions').fetchone()[0]
        avg_score = c.execute('SELECT AVG(score) FROM sessions').fetchone()[0]
        top = c.execute(
            'SELECT verdict, COUNT(*) as cnt FROM sessions WHERE verdict!=? '
            'GROUP BY verdict ORDER BY cnt DESC LIMIT 3', ('',)
        ).fetchall()
        recent = c.execute(
            'SELECT candidate, score, verdict, created_at FROM sessions '
            'ORDER BY created_at DESC LIMIT 5'
        ).fetchall()
    return {
        'users_total':   users_total,
        'users_active':  users_active,
        'sessions_total': sessions_total,
        'avg_score':     round(avg_score, 1) if avg_score else 0,
        'top_verdicts':  [dict(r) for r in top],
        'recent':        [dict(r) for r in recent],
    }


# ── Audit-Log ─────────────────────────────────────────────────────────────────

def get_audit_log(limit=200):
    with _conn() as c:
        rows = c.execute(
            'SELECT * FROM audit_log ORDER BY id DESC LIMIT ?', (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
