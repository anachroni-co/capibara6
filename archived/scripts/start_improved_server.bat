@echo off
REM Script para iniciar el servidor mejorado de Capibara6 en Windows

echo 🚀 Iniciando Servidor Capibara6 Mejorado...
echo ==========================================

REM Verificar si el puerto 5001 está en uso
netstat -ano | findstr :5001 >nul 2>&1
if %errorlevel% == 0 (
    echo ⚠️ Puerto 5001 ya está en uso. Deteniendo proceso...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001') do (
        taskkill /PID %%a /F >nul 2>&1
    )
    timeout /t 2 >nul
)

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 📦 Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Instalar dependencias si es necesario
if exist "backend\requirements.txt" (
    echo 📋 Verificando dependencias...
    pip install -r backend\requirements.txt >nul 2>&1
)

REM Cambiar al directorio backend
cd backend

echo 🔧 Iniciando servidor en puerto 5001...
echo 🌐 URL: http://localhost:5001
echo 📡 API: http://localhost:5001/api/chat
echo 🏥 Health: http://localhost:5001/health
echo.
echo Presiona Ctrl+C para detener el servidor
echo ==========================================

REM Iniciar el servidor
python capibara6_integrated_server.py

pause
