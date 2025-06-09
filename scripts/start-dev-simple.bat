@echo off
title SG Backend - Desarrollo Local

echo 🚀 Iniciando SG Backend en modo desarrollo...
echo.

:: Set environment variables
set IS_OFFLINE=true
set STAGE=dev
set USERS_TABLE=users-table-dev
set ATTENDANCE_TABLE=attendance-table-dev
set GRADES_TABLE=grades-table-dev

:: Check if Java is installed
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Java no está instalado o no está en el PATH
    echo 💡 Instala Java desde: https://www.oracle.com/java/technologies/downloads/
    pause
    exit /b 1
)

:: Check if DynamoDB Local is installed
if not exist .dynamodb\DynamoDBLocal.jar (
    echo 💾 Instalando DynamoDB Local...
    call npm run dynamodb:install
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar DynamoDB Local
        pause
        exit /b 1
    )
)

:: Start DynamoDB Local
echo 🗄️ Iniciando DynamoDB Local en puerto 8000...
start /B "DynamoDB Local" java -Djava.library.path=.dynamodb/DynamoDBLocal_lib -jar .dynamodb/DynamoDBLocal.jar -sharedDb -port 8000

:: Wait for DynamoDB to start
echo ⏳ Esperando que DynamoDB Local esté listo...
timeout /t 5 /nobreak > nul

:: Create tables
echo 📋 Creando tablas...
python scripts/create_tables.py

:: Wait a moment
timeout /t 2 /nobreak > nul

:: Seed data
echo 🌱 Poblando datos de prueba...
python scripts/seed_data.py

:: Start Serverless Offline
echo 🌐 Iniciando API en http://localhost:3000...
call serverless offline start --stage dev

pause
