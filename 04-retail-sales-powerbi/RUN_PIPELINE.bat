@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
if not exist .venv\Scripts\python.exe (
  %PY% -m venv .venv
  if errorlevel 1 goto error
)
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
.venv\Scripts\python.exe scripts\rebuild_from_uci.py
if errorlevel 1 goto error
echo.
echo Pipeline run finished. Review the regenerated data and update the dashboard payload before publishing.
pause
exit /b 0
:error
echo.
echo Pipeline failed. The deployed dashboard can still run using the included attributed aggregate data.
echo Check Python, network access, and the error shown above.
pause
exit /b 1
