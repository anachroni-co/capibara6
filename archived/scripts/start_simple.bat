@echo off
REM ============================================
REM INICIO SIMPLE - CAPIBARA6 (Solo Frontend)
REM ============================================

echo 🚀 Iniciando Capibara6 (modo simple)...
echo.

echo 📋 Configuración:
echo    - Autenticación: DESHABILITADA
echo    - Consenso: DESHABILITADO
echo    - Modelo: Capibara6 (Gemma3-12B)
echo    - Servidor: http://34.175.89.158:8080
echo.

echo 🎨 Iniciando servidor del frontend...
cd web
python -m http.server 8000

echo.
echo ✅ Servidor iniciado!
echo.
echo 🔗 Accede a: http://localhost:8000/chat.html
echo.
echo 📋 Para detener el servidor: Ctrl + C
echo.
