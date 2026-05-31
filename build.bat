@echo off
chcp 65001 >nul
echo ══════════════════════════════════════════════════════
echo   NRW VC Bewerbungstool v4.1  —  EXE Builder
echo ══════════════════════════════════════════════════════

python --version >nul 2>&1
if errorlevel 1 ( echo [FEHLER] Python nicht gefunden! & pause & exit /b 1 )

echo [1/3] Installiere Abhaengigkeiten...
pip install pywebview pyinstaller --quiet

echo [2/3] Bereinige alte Builds...
if exist dist  rmdir /s /q dist
if exist build rmdir /s /q build

echo [3/3] Baue EXE...
pyinstaller build.spec
if errorlevel 1 ( echo [FEHLER] Build fehlgeschlagen! & pause & exit /b 1 )

echo.
echo ══════════════════════════════════════════════════════
echo   FERTIG!
echo   App:    dist\NRW_VC_Tool_v4.exe
echo   Keygen: dist\NRW_VC_Keygen.exe
echo.
echo   WICHTIG: Keygen.exe NIEMALS verteilen!
echo ══════════════════════════════════════════════════════
pause
