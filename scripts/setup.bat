@echo off
echo 🚀 Configurando DynamoDB Local para SG Backend...

echo 📦 Limpiando instalación anterior...
if exist node_modules rmdir /s /q node_modules
if exist .serverless rmdir /s /q .serverless

echo 📦 Instalando dependencias...
call npm install

echo 💾 Instalando DynamoDB Local...
call npm run dynamodb:install

echo ✅ Configuración completada!
echo.
echo 📋 Comandos disponibles:
echo   npm run dev          - Ejecutar backend + DynamoDB local
echo   npm run dynamodb:start - Solo DynamoDB local
echo   npm run start        - Solo backend (requiere DynamoDB corriendo)
echo   npm run seed         - Poblar base de datos con datos de prueba
echo.
echo 🎯 Para empezar:
echo   1. npm run dev
echo   2. En otra terminal: npm run seed

pause
