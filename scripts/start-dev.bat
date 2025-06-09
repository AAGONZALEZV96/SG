@echo off
title SG Backend Development

echo 🚀 Iniciando entorno de desarrollo...

:: Check if DynamoDB Local is installed
if not exist .dynamodb\DynamoDBLocal.jar (
    echo 💾 DynamoDB Local no encontrado. Instalando...
    python scripts/install_dynamodb.py
)

:: Start DynamoDB Local in background
echo 🗄️ Iniciando DynamoDB Local...
start /B java -Djava.library.path=.dynamodb/DynamoDBLocal_lib -jar .dynamodb/DynamoDBLocal.jar -sharedDb -port 8000

:: Wait a moment for DynamoDB to start
timeout /t 3 /nobreak > nul

:: Start Serverless Offline
echo 🌐 Iniciando Serverless Offline...
call serverless offline start

pause
