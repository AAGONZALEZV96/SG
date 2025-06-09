@echo off
echo Cerrando procesos en puertos 8000 y 8001...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do taskkill /F /PID %%a
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001"') do taskkill /F /PID %%a
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8002"') do taskkill /F /PID %%a
echo Iniciando entorno local...
sls offline start --stage local