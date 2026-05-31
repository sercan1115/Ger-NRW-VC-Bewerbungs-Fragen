# -*- mode: python ; coding: utf-8 -*-
# PyInstaller Build-Spec für NRW VC Bewerbungstool
# Aufruf: pyinstaller build.spec

import os
SRC = os.path.abspath('src')

a = Analysis(
    [os.path.join(SRC, 'main.py')],
    pathex=[SRC],
    binaries=[],
    datas=[
        (os.path.join(SRC, 'index.html'), '.'),
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'clr',
        'database',
        'license',
        'api',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'PIL', 'scipy'],
    noarchive=False,
    # Bytecode verschlüsseln (optionaler Schutz)
    # cipher=PYZ_CIPHER,   # entkommentieren + PYZ_CIPHER='IhrGeheimerKey' setzen
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NRW_VC_Tool_v4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,          # UPX-Kompression (muss installiert sein)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,     # Kein schwarzes Terminal-Fenster
    disable_windowed_traceback=False,
    icon=os.path.join(SRC, 'icon.ico') if os.path.exists(os.path.join(SRC, 'icon.ico')) else None,
    version_file=None,
)

# ── Keygen als separate EXE ──────────────────────────────────────────────────
a2 = Analysis(
    [os.path.join(SRC, 'keygen.py')],
    pathex=[SRC],
    binaries=[],
    datas=[],
    hiddenimports=['license', 'tkinter'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz2 = PYZ(a2.pure, a2.zipped_data)

exe2 = EXE(
    pyz2,
    a2.scripts,
    a2.binaries,
    a2.datas,
    [],
    name='NRW_VC_Keygen',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)
