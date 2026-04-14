@echo off
REM --- AI Catalyst C3 launcher (Windows) ---
REM Double-click this to start the dev server (if needed) and open today's lesson.

set "REPO_ROOT=%~dp0..\.."
pushd "%REPO_ROOT%\app"

REM If nothing is listening on 3000, start the dev server in a new window.
powershell -NoProfile -Command "if (-not (Test-NetConnection -ComputerName localhost -Port 3000 -WarningAction SilentlyContinue -InformationLevel Quiet)) { Start-Process cmd -ArgumentList '/c','cd /d %CD% && npm run dev' -WindowStyle Minimized }"

REM Wait a moment and open the browser.
timeout /t 3 /nobreak >nul
start "" "http://localhost:3000/"
popd
