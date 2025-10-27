@echo off
REM Script de prueba rápida para verificar las mejoras

echo 🧪 Prueba Rápida de Mejoras GPT-OSS-20B
echo =======================================

REM Verificar que el servidor esté ejecutándose
echo 🔍 Verificando servidor...
curl -s http://localhost:5001/health >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Servidor funcionando en puerto 5001
) else (
    echo ❌ Servidor no está ejecutándose. Inicia con: start_improved_server.bat
    pause
    exit /b 1
)

REM Probar pregunta simple
echo.
echo 🤖 Probando pregunta: ¿Cómo te llamas?
echo ----------------------------------------

curl -s -X POST http://localhost:5001/api/chat -H "Content-Type: application/json" -d "{\"message\": \"¿Cómo te llamas?\"}" > temp_response.json

echo 📝 Respuesta recibida:
type temp_response.json

REM Limpiar archivo temporal
del temp_response.json >nul 2>&1

echo.
echo 🎯 Prueba completada!
echo Si el servidor responde con información sobre Capibara6, las mejoras están funcionando.

pause
