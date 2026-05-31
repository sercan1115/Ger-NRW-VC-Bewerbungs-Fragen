#!/usr/bin/env python3
"""
NRW VC — Lizenzschlüssel Generator v2
Admin-Tool mit History, Export und Schlüssel-Prüfung.
NIEMALS zusammen mit der verteilten App veröffentlichen!
"""
import sys, os, json, datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from license import generate_license, get_hardware_id, validate_license

HIST_FILE = Path(os.environ.get('APPDATA', Path.home())) / 'NRW_VC_Tool' / 'keygen_history.json'

def load_hist():
    try:
        if HIST_FILE.exists():
            return json.loads(HIST_FILE.read_text('utf-8'))
    except Exception:
        pass
    return []

def save_hist(h):
    HIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    HIST_FILE.write_text(json.dumps(h, ensure_ascii=False, indent=2), 'utf-8')

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    HAS_TK = True
except ImportError:
    HAS_TK = False

# ── Farben ────────────────────────────────────────────────────────────────────
BG   = '#0d1117'
BG2  = '#161b22'
BG3  = '#21262d'
GOLD = '#f59e0b'
FG   = '#e2e8f0'
FG2  = '#94a3b8'
FG3  = '#475569'
GRN  = '#22c55e'
RED  = '#ef4444'


class KeygenApp:
    def __init__(self):
        self.hist = load_hist()
        self.root = tk.Tk()
        self.root.title('NRW VC — Lizenz Generator')
        self.root.geometry('900x640')
        self.root.minsize(820, 580)
        self.root.configure(bg=BG)
        self._build()
        self.root.mainloop()

    # ── Widget-Helfer ─────────────────────────────────────────────────────────

    def _lbl(self, p, text, size=8, bold=False, fg=FG2):
        return tk.Label(p, text=text, bg=BG, fg=fg,
                        font=('Segoe UI', size, 'bold' if bold else 'normal'))

    def _entry(self, p, w=30, show=''):
        return tk.Entry(p, bg=BG2, fg=FG, insertbackground=GOLD, relief='flat',
                        font=('Segoe UI', 9), width=w, show=show,
                        highlightthickness=1, highlightbackground=BG3,
                        highlightcolor=GOLD)

    def _btn(self, p, text, cmd, gold=False, small=False, **kw):
        sz = 8 if small else 9
        return tk.Button(
            p, text=text, command=cmd,
            bg=GOLD if gold else BG3, fg='#000' if gold else FG,
            font=('Segoe UI', sz, 'bold' if gold else 'normal'),
            relief='flat', cursor='hand2',
            activebackground='#d97706' if gold else '#30363d',
            activeforeground='#000' if gold else FG,
            padx=12 if small else 16, pady=5 if small else 8, **kw
        )

    # ── Haupt-UI ──────────────────────────────────────────────────────────────

    def _build(self):
        # Header
        hdr = tk.Frame(self.root, bg=BG2, height=56)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)

        tk.Label(hdr, text='⬡  NRW VC — Lizenz Generator',
                 bg=BG2, fg=GOLD, font=('Segoe UI', 13, 'bold')).pack(
            side='left', padx=20, pady=14)

        # HWID dieser Maschine oben rechts
        hw_f = tk.Frame(hdr, bg=BG2)
        hw_f.pack(side='right', padx=14)
        self.this_hwid = get_hardware_id()
        tk.Label(hw_f, text='Diese Maschine:', bg=BG2, fg=FG3,
                 font=('Segoe UI', 7)).pack(side='left')
        tk.Label(hw_f, text=f'  {self.this_hwid}  ', bg=BG3, fg=GOLD,
                 font=('Consolas', 8)).pack(side='left', padx=4)
        self._btn(hw_f, '📋', self._copy_this_hwid, small=True).pack(side='left')

        tk.Frame(self.root, bg='#30363d', height=1).pack(fill='x')

        # Notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook',     background=BG,  borderwidth=0, tabmargins=0)
        style.configure('TNotebook.Tab', background=BG2, foreground=FG2,
                        padding=[18, 9], font=('Segoe UI', 8, 'bold'))
        style.map('TNotebook.Tab',
                  background=[('selected', BG)],
                  foreground=[('selected', GOLD)])
        style.configure('Treeview',
                        background=BG, fieldbackground=BG, foreground=FG,
                        rowheight=30, font=('Segoe UI', 8), borderwidth=0)
        style.configure('Treeview.Heading', background=BG2, foreground=FG2,
                        font=('Segoe UI', 8, 'bold'), relief='flat')
        style.map('Treeview',
                  background=[('selected', '#1f2937')],
                  foreground=[('selected', GOLD)])

        nb = ttk.Notebook(self.root)
        nb.pack(fill='both', expand=True)

        t1 = tk.Frame(nb, bg=BG)
        t2 = tk.Frame(nb, bg=BG)
        t3 = tk.Frame(nb, bg=BG)

        nb.add(t1, text='  🔑  Neue Lizenz  ')
        nb.add(t2, text='  📋  Erstellte Lizenzen  ')
        nb.add(t3, text='  🔍  Schlüssel prüfen  ')

        nb.bind('<<NotebookTabChanged>>',
                lambda e: self._on_tab(nb.index('current')))

        self._build_create(t1)
        self._build_history(t2)
        self._build_check(t3)

    def _on_tab(self, idx):
        if idx == 1:
            self._refresh_hist()

    def _copy_this_hwid(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.this_hwid)
        messagebox.showinfo('Kopiert', f'Hardware-ID kopiert:\n{self.this_hwid}')

    # ── Tab 1: Neue Lizenz ────────────────────────────────────────────────────

    def _build_create(self, parent):
        # Zweispaltiges Layout
        left  = tk.Frame(parent, bg=BG)
        right = tk.Frame(parent, bg=BG2, width=260)

        left.pack(side='left', fill='both', expand=True, padx=28, pady=22)
        right.pack(side='right', fill='y')
        right.pack_propagate(False)

        tk.Frame(right, bg='#30363d', width=1).pack(side='left', fill='y')

        rinner = tk.Frame(right, bg=BG2)
        rinner.pack(fill='both', expand=True, padx=16, pady=16)

        # ── Rechte Spalte: Anleitung + Rollen ─────────────────────────────
        tk.Label(rinner, text='Schnell-Anleitung', bg=BG2, fg=GOLD,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', pady=(0, 6))

        steps = [
            ('1.', 'HWID des Zielrechners eintragen\n(Keygen dort starten → kopieren)'),
            ('2.', 'Name, Rolle & Laufzeit ausfüllen'),
            ('3.', '„Generieren" klicken'),
            ('4.', 'Schlüssel per Chat/Mail senden'),
            ('5.', 'Nutzer gibt Schlüssel beim\nApp-Start ein → fertig'),
        ]
        for num, text in steps:
            f = tk.Frame(rinner, bg=BG2)
            f.pack(fill='x', pady=3)
            tk.Label(f, text=num, bg=BG2, fg=GOLD,
                     font=('Segoe UI', 8, 'bold'), width=2).pack(side='left', anchor='n')
            tk.Label(f, text=text, bg=BG2, fg=FG2,
                     font=('Segoe UI', 8), justify='left').pack(side='left', padx=6)

        tk.Frame(rinner, bg='#30363d', height=1).pack(fill='x', pady=12)

        tk.Label(rinner, text='Rollen', bg=BG2, fg=GOLD,
                 font=('Segoe UI', 8, 'bold')).pack(anchor='w', pady=(0, 6))

        for icon, role, desc in [
            ('👑', 'OWNER', 'Alles + Verwaltung'),
            ('🛡', 'ADMIN', 'Gespräche + Archiv'),
            ('👁', 'VIEWER', 'Nur lesen'),
        ]:
            f = tk.Frame(rinner, bg=BG2)
            f.pack(fill='x', pady=2)
            tk.Label(f, text=f'{icon} {role}', bg=BG2, fg=GOLD,
                     font=('Segoe UI', 8, 'bold'), width=10, anchor='w').pack(side='left')
            tk.Label(f, text=desc, bg=BG2, fg=FG2,
                     font=('Segoe UI', 8)).pack(side='left')

        # ── Linke Spalte: Formular ─────────────────────────────────────────
        left.columnconfigure(0, weight=1)

        # Name
        self._lbl(left, 'Name / Team-Bezeichnung').grid(
            row=0, column=0, sticky='w', pady=(0, 3))
        self.e_name = self._entry(left)
        self.e_name.grid(row=1, column=0, sticky='ew', pady=(0, 10))

        # Organisation
        self._lbl(left, 'Organisation (optional)').grid(
            row=2, column=0, sticky='w', pady=(0, 3))
        self.e_team = self._entry(left)
        self.e_team.grid(row=3, column=0, sticky='ew', pady=(0, 10))

        # Rolle + Laufzeit nebeneinander
        rf = tk.Frame(left, bg=BG)
        rf.grid(row=4, column=0, sticky='ew', pady=(0, 10))
        rf.columnconfigure(0, weight=1)
        rf.columnconfigure(1, weight=2)

        self._lbl(rf, 'Rolle').grid(row=0, column=0, sticky='w', padx=(0, 10))
        self._lbl(rf, 'Laufzeit').grid(row=0, column=1, sticky='w')

        self.role_var = tk.StringVar(value='ADMIN')
        ttk.Combobox(rf, textvariable=self.role_var,
                     values=['OWNER', 'ADMIN', 'VIEWER'],
                     state='readonly', width=12).grid(
            row=1, column=0, sticky='ew', padx=(0, 10), pady=(3, 0))

        self.dur_var = tk.StringVar(value='1 Jahr (365 Tage)')
        dur_cb = ttk.Combobox(rf, textvariable=self.dur_var,
                              values=['30 Tage', '90 Tage', '180 Tage',
                                      '1 Jahr (365 Tage)', '2 Jahre',
                                      'Unbegrenzt (10 Jahre)', 'Eigenes Datum…'],
                              state='readonly')
        dur_cb.grid(row=1, column=1, sticky='ew', pady=(3, 0))

        # Eigenes Datum (versteckt)
        self.exp_frame = tk.Frame(left, bg=BG)
        self.exp_frame.grid(row=5, column=0, sticky='ew')
        self._lbl(self.exp_frame, 'Datum (YYYY-MM-DD)').pack(anchor='w', pady=(0, 3))
        self.e_expiry = self._entry(self.exp_frame, w=20)
        self.e_expiry.insert(0, datetime.date.today().isoformat())
        self.e_expiry.pack(anchor='w', pady=(0, 6))
        self.exp_frame.grid_remove()
        dur_cb.bind('<<ComboboxSelected>>',
                    lambda *_: (self.exp_frame.grid()
                                if self.dur_var.get() == 'Eigenes Datum…'
                                else self.exp_frame.grid_remove()))

        # Hardware-Bindung
        hw_box = tk.LabelFrame(left, text='  Hardware-Bindung  ',
                               bg=BG, fg=FG2, font=('Segoe UI', 8),
                               relief='flat', highlightthickness=1,
                               highlightbackground='#30363d')
        hw_box.grid(row=6, column=0, sticky='ew', pady=(6, 12))
        hw_box.columnconfigure(0, weight=1)

        self.bind_var = tk.BooleanVar(value=True)
        tk.Checkbutton(hw_box, text='An Hardware-ID binden (empfohlen – verhindert Weitergabe)',
                       variable=self.bind_var, bg=BG, fg=FG,
                       selectcolor=BG2, activebackground=BG,
                       font=('Segoe UI', 8),
                       command=self._toggle_hwid).grid(
            row=0, column=0, columnspan=2, sticky='w', padx=8, pady=(8, 4))

        self._lbl(hw_box, 'Hardware-ID des Zielrechners').grid(
            row=1, column=0, sticky='w', padx=8, pady=(0, 3))

        hw_row = tk.Frame(hw_box, bg=BG)
        hw_row.grid(row=2, column=0, sticky='ew', padx=8, pady=(0, 4))
        hw_row.columnconfigure(0, weight=1)

        self.e_hwid = self._entry(hw_row, w=28)
        self.e_hwid.grid(row=0, column=0, sticky='ew')
        self._btn(hw_row, '📋 Diese Maschine',
                  self._paste_this_hwid, small=True).grid(row=0, column=1, padx=(6, 0))

        tk.Label(hw_box, text='Tipp: Keygen auf dem Zielrechner starten → HWID oben kopieren',
                 bg=BG, fg=FG3, font=('Segoe UI', 7)).grid(
            row=3, column=0, sticky='w', padx=8, pady=(0, 8))

        # Generieren-Button
        self._btn(left, '🔑  Lizenzschlüssel generieren',
                  self._generate, gold=True).grid(
            row=7, column=0, sticky='ew', pady=(0, 10))

        # Ausgabe
        out_wrap = tk.Frame(left, bg=BG3, highlightthickness=1,
                            highlightbackground='#30363d')
        out_wrap.grid(row=8, column=0, sticky='ew', pady=(0, 6))

        self.out_text = tk.Text(out_wrap, height=4, bg='#010409', fg=GOLD,
                                font=('Consolas', 9), relief='flat',
                                insertbackground=GOLD, wrap='word',
                                state='disabled', padx=12, pady=10)
        self.out_text.pack(fill='x')

        btn_row = tk.Frame(left, bg=BG)
        btn_row.grid(row=9, column=0, sticky='ew')

        self._btn(btn_row, '📋 Schlüssel kopieren',
                  self._copy_key).pack(side='left')
        self.copy_lbl = tk.Label(btn_row, text='', bg=BG, fg=GRN,
                                 font=('Segoe UI', 8))
        self.copy_lbl.pack(side='left', padx=10)

    def _toggle_hwid(self):
        self.e_hwid.config(state='normal' if self.bind_var.get() else 'disabled')

    def _paste_this_hwid(self):
        self.e_hwid.delete(0, 'end')
        self.e_hwid.insert(0, self.this_hwid)

    def _get_expiry(self):
        d = {
            '30 Tage': 30, '90 Tage': 90, '180 Tage': 180,
            '1 Jahr (365 Tage)': 365, '2 Jahre': 730,
            'Unbegrenzt (10 Jahre)': 3650,
        }
        sel = self.dur_var.get()
        if sel == 'Eigenes Datum…':
            return self.e_expiry.get().strip()
        return (datetime.date.today() +
                datetime.timedelta(days=d.get(sel, 365))).isoformat()

    def _generate(self):
        name = self.e_name.get().strip()
        if not name:
            messagebox.showerror('Fehler', 'Name darf nicht leer sein!')
            return

        role   = self.role_var.get()
        expiry = self._get_expiry()
        team   = self.e_team.get().strip()
        hwid   = ''

        if self.bind_var.get():
            hwid = self.e_hwid.get().strip()
            if not hwid:
                messagebox.showerror('Fehler',
                    'Bitte Hardware-ID eingeben oder Bindung deaktivieren.')
                return

        key = generate_license(name, role, expiry, hwid, team)

        self.out_text.config(state='normal')
        self.out_text.delete('1.0', 'end')
        self.out_text.insert('end', key + '\n\n')
        self.out_text.insert('end',
            f'Name: {name}  ·  Rolle: {role}  ·  Gültig bis: {expiry}')
        if hwid:
            self.out_text.insert('end', f'  ·  HWID: {hwid}')
        self.out_text.config(state='disabled')

        entry = {
            'key':     key,
            'name':    name,
            'role':    role,
            'expiry':  expiry,
            'hwid':    hwid,
            'team':    team,
            'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        }
        self.hist.insert(0, entry)
        save_hist(self.hist)
        self.copy_lbl.config(text='')

    def _copy_key(self):
        key = self.out_text.get('1.0', 'end').strip().split('\n')[0]
        if not key:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(key)
        self.copy_lbl.config(text='✓ In Zwischenablage kopiert!')
        self.root.after(2500, lambda: self.copy_lbl.config(text=''))

    # ── Tab 2: History ────────────────────────────────────────────────────────

    def _build_history(self, parent):
        # Toolbar
        tb = tk.Frame(parent, bg=BG2, height=48)
        tb.pack(fill='x')
        tb.pack_propagate(False)
        tk.Label(tb, text='Erstellte Lizenzen', bg=BG2, fg=FG,
                 font=('Segoe UI', 9, 'bold')).pack(side='left', padx=16, pady=13)
        self._btn(tb, '🗑 Alle löschen', self._clear_hist,
                  small=True).pack(side='right', padx=6, pady=10)
        self._btn(tb, '📤 Exportieren (.txt)', self._export_hist,
                  small=True).pack(side='right', pady=10)
        tk.Frame(parent, bg='#30363d', height=1).pack(fill='x')

        # Treeview
        cols = ('name', 'role', 'expiry', 'hwid', 'team', 'created')
        self.tree = ttk.Treeview(parent, columns=cols,
                                 show='headings', selectmode='browse')

        hdrs   = ('Name', 'Rolle', 'Gültig bis', 'HWID', 'Organisation', 'Erstellt am')
        widths = (160,    72,       100,           120,    140,             130)
        for c, h, w in zip(cols, hdrs, widths):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, minwidth=50)

        vsb = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', lambda _: self._copy_selected())
        self.tree.bind('<<TreeviewSelect>>', self._on_sel)

        # Bottom action bar
        ab = tk.Frame(parent, bg=BG2, height=46)
        ab.pack(fill='x', side='bottom')
        ab.pack_propagate(False)
        tk.Frame(ab, bg='#30363d', height=1).pack(fill='x', side='top')
        self._btn(ab, '📋 Schlüssel kopieren',
                  self._copy_selected, small=True).pack(side='left', padx=8, pady=10)
        self._btn(ab, '🗑 Eintrag entfernen',
                  self._del_selected, small=True).pack(side='left', pady=10)
        self.hist_lbl = tk.Label(ab, text='Doppelklick auf einen Eintrag = Schlüssel kopieren',
                                 bg=BG2, fg=FG3, font=('Segoe UI', 7))
        self.hist_lbl.pack(side='right', padx=12)

    def _refresh_hist(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for e in self.hist:
            self.tree.insert('', 'end', values=(
                e.get('name', ''),
                e.get('role', ''),
                e.get('expiry', ''),
                e.get('hwid', '') or '–',
                e.get('team', '') or '–',
                e.get('created', ''),
            ))

    def _on_sel(self, _):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            if 0 <= idx < len(self.hist):
                key = self.hist[idx]['key']
                self.hist_lbl.config(
                    text=f'  {key[:40]}…', fg=FG2)

    def _copy_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo('Hinweis', 'Bitte zuerst einen Eintrag auswählen.')
            return
        idx = self.tree.index(sel[0])
        if 0 <= idx < len(self.hist):
            key = self.hist[idx]['key']
            self.root.clipboard_clear()
            self.root.clipboard_append(key)
            self.hist_lbl.config(text='✓ Schlüssel kopiert!', fg=GRN)
            self.root.after(2500, lambda: self.hist_lbl.config(
                text='Doppelklick auf einen Eintrag = Schlüssel kopieren', fg=FG3))

    def _del_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        if not messagebox.askyesno('Eintrag löschen?',
                                   'Diesen Eintrag aus der History entfernen?\n'
                                   '(Der Schlüssel bleibt weiterhin gültig.)'):
            return
        idx = self.tree.index(sel[0])
        if 0 <= idx < len(self.hist):
            self.hist.pop(idx)
            save_hist(self.hist)
            self._refresh_hist()

    def _clear_hist(self):
        if not messagebox.askyesno('Alle löschen?',
                                   'Gesamte History löschen?\n'
                                   '(Bestehende Schlüssel bleiben gültig.)'):
            return
        self.hist.clear()
        save_hist(self.hist)
        self._refresh_hist()

    def _export_hist(self):
        if not self.hist:
            messagebox.showinfo('Leer', 'Keine Einträge vorhanden.')
            return
        path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text-Datei', '*.txt'), ('Alle Dateien', '*.*')],
            initialfile='NRW_VC_Lizenzen_Export.txt',
            title='Lizenzen exportieren',
        )
        if not path:
            return
        lines = [
            'NRW VC — Exportierte Lizenzen',
            f'Stand: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
            '=' * 64,
        ]
        for e in self.hist:
            lines += [
                '',
                f'Name:      {e.get("name","")}',
                f'Rolle:     {e.get("role","")}',
                f'Gültig:    bis {e.get("expiry","")}',
            ]
            if e.get('hwid'):
                lines.append(f'HWID:      {e["hwid"]}')
            if e.get('team'):
                lines.append(f'Org:       {e["team"]}')
            lines += [
                f'Erstellt:  {e.get("created","")}',
                f'Schlüssel: {e.get("key","")}',
                '-' * 64,
            ]
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        messagebox.showinfo('Export erfolgreich', f'Gespeichert unter:\n{path}')

    # ── Tab 3: Schlüssel prüfen ───────────────────────────────────────────────

    def _build_check(self, parent):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill='both', expand=True, padx=30, pady=24)
        f.columnconfigure(0, weight=1)

        tk.Label(f, text='Schlüssel prüfen', bg=BG, fg=FG,
                 font=('Segoe UI', 11, 'bold')).grid(row=0, sticky='w', pady=(0, 6))
        tk.Label(f, text='Gibt an ob ein Schlüssel gültig, abgelaufen oder gefälscht ist.',
                 bg=BG, fg=FG2, font=('Segoe UI', 8)).grid(row=1, sticky='w', pady=(0, 14))

        tk.Label(f, text='Lizenzschlüssel hier einfügen:', bg=BG, fg=FG2,
                 font=('Segoe UI', 8)).grid(row=2, sticky='w', pady=(0, 4))

        self.e_chk = tk.Text(f, height=3, bg=BG2, fg=FG, font=('Consolas', 9),
                             relief='flat', insertbackground=GOLD,
                             highlightthickness=1, highlightbackground=BG3,
                             highlightcolor=GOLD, padx=10, pady=8)
        self.e_chk.grid(row=3, sticky='ew', pady=(0, 12))

        self._btn(f, '🔍  Jetzt prüfen', self._do_check, gold=True).grid(
            row=4, sticky='w', pady=(0, 14))

        # Ergebnis-Box
        result_wrap = tk.Frame(f, bg=BG3, highlightthickness=1,
                               highlightbackground='#30363d')
        result_wrap.grid(row=5, sticky='ew')

        self.chk_out = tk.Text(result_wrap, height=9, bg='#010409', fg=FG,
                               font=('Consolas', 9), relief='flat',
                               state='disabled', padx=12, pady=10, wrap='word')
        self.chk_out.pack(fill='x')

        # Tags für Farben
        self.chk_out.tag_config('ok',   foreground=GRN)
        self.chk_out.tag_config('err',  foreground=RED)
        self.chk_out.tag_config('key',  foreground=GOLD)
        self.chk_out.tag_config('val',  foreground=FG)

    def _do_check(self):
        key = self.e_chk.get('1.0', 'end').strip()
        if not key:
            return
        r = validate_license(key)

        self.chk_out.config(state='normal')
        self.chk_out.delete('1.0', 'end')

        if r['valid']:
            self.chk_out.insert('end', '✓  GÜLTIG\n\n', 'ok')
            rows = [
                ('Name',       r.get('name',  '–')),
                ('Rolle',      r.get('role',  '–')),
                ('Gültig bis', r.get('expiry','–')),
                ('Noch',       f'{r.get("days_left", 0)} Tage'),
            ]
            if r.get('hwid'):
                rows.append(('HWID', r['hwid']))
            if r.get('team'):
                rows.append(('Org', r['team']))
            for k, v in rows:
                self.chk_out.insert('end', f'{k:<13}', 'key')
                self.chk_out.insert('end', f'{v}\n', 'val')
        else:
            self.chk_out.insert('end', '✕  UNGÜLTIG\n\n', 'err')
            self.chk_out.insert('end', r.get('error', 'Unbekannter Fehler'), 'val')

        self.chk_out.config(state='disabled')


# ── CLI-Fallback ───────────────────────────────────────────────────────────────

def run_cli():
    print('=' * 60)
    print('  NRW VC — Lizenz Generator (CLI-Modus)')
    print('=' * 60)
    while True:
        print('\n[1] Lizenz erstellen  [2] HWID  [3] Prüfen  [4] Ende')
        c = input('> ').strip()
        if c == '1':
            n = input('Name: ').strip()
            r = input('Rolle (OWNER/ADMIN/VIEWER): ').strip().upper()
            d = input('Tage gültig (z.B. 365): ').strip()
            exp = (datetime.date.today() +
                   datetime.timedelta(days=int(d))).isoformat()
            h = input('HWID (leer = keine Bindung): ').strip()
            print('\n' + generate_license(n, r, exp, h))
        elif c == '2':
            print(f'\nHWID: {get_hardware_id()}')
        elif c == '3':
            k = input('Schlüssel: ').strip()
            print(validate_license(k))
        elif c == '4':
            break


if __name__ == '__main__':
    if HAS_TK:
        KeygenApp()
    else:
        run_cli()
