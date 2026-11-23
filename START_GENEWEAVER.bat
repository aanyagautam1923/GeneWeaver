@echo off
title GeneWeaver Launcher
cd /d "C:\Users\gauta\OneDrive\Desktop\GeneWeaver"

echo Starting GeneWeaver Backend...
start "GeneWeaver Backend" cmd /k "cd /d C:\Users\gauta\OneDrive\Desktop\GeneWeaver && .venv\Scripts\python.exe -m uvicorn app.api.main:app --port 8010"

timeout /t 3 /nobreak >nul

echo Starting GeneWeaver Frontend...
start "GeneWeaver Frontend" cmd /k "cd /d C:\Users\gauta\OneDrive\Desktop\GeneWeaver && python -m http.server 5510 --directory frontend"

timeout /t 2 /nobreak >nul

start "" "http://127.0.0.1:5510"

echo GeneWeaver Started!
