@echo off
REM ============================================
REM INICIO COMPLETO - CAPIBARA6 CON MCP (Windows)
REM ============================================

echo 🤖 Iniciando Capibara6 con MCP (Model Context Protocol)...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist ".venv" (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r backend\requirements.txt

echo.
echo 🌐 URLs de acceso:
echo    Frontend: http://localhost:8000
echo    Chat:     http://localhost:8000/chat.html
echo    MCP API:  http://localhost:5003
echo.

REM Iniciar servidor MCP en background
echo 🛡️  Iniciando servidor MCP (reducción de alucinaciones)...
start /B python backend\mcp_server.py

REM Esperar un momento
timeout /t 2 /nobreak >nul

REM Iniciar servidor del frontend
echo 🎨 Iniciando servidor del frontend...
cd web
start /B python -m http.server 8000
cd ..

echo.
echo ✅ Capibara6 con MCP iniciado correctamente!
echo.
echo 📊 Servicios activos:
echo    - MCP Server: http://localhost:5003
echo    - Frontend: http://localhost:8000
echo.
echo 🛡️  MCP Activo - Reducción de alucinaciones habilitada
echo.
echo 🔗 Accede a: http://localhost:8000/chat.html
echo.
echo 📋 Para detener los servidores, cierra esta ventana
echo.

pause
