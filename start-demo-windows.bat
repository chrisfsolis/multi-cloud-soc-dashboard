@echo off
setlocal
cd /d %~dp0

echo Starting Multi-Cloud SOC Dashboard demo...
echo Backend:  http://127.0.0.1:8000/docs
echo Frontend: http://127.0.0.1:5174

start "SOC Dashboard Backend" cmd /k "cd /d %~dp0backend && if not exist .venv\Scripts\python.exe python -m venv .venv && call .venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
start "SOC Dashboard Frontend" cmd /k "cd /d %~dp0frontend && npm install && npm run dev -- --host 127.0.0.1 --port 5174"

echo Open http://127.0.0.1:5174 after both windows finish starting.
endlocal
