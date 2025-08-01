@echo off
cd /d "%~dp0"
echo Reawakening Bart... bracing for sarcasm.
uvicorn main:app --reload --port 5000
pause
