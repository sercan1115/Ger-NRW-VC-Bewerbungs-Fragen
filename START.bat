@echo off
echo.
echo  ==========================================
echo   ⬡  HIGH-TEAM Bewerbungstool starten
echo  ==========================================
echo.
python start_server.py
if errorlevel 1 (
    python3 start_server.py
)
pause
