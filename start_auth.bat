@echo off
REM ============================================
REM SCRIPT DE INICIO - CAPIBARA6 CON AUTH (Windows)
REM ============================================

echo 🚀 Iniciando Capibara6 con Autenticación...
echo.

REM Verificar si Python está instalado
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

REM Verificar variables de entorno
echo.
echo 🔍 Verificando configuración OAuth...

if "%GITHUB_CLIENT_ID%"=="" (
    echo ⚠️  GITHUB_CLIENT_ID no configurado
    echo    Configura: set GITHUB_CLIENT_ID=tu_client_id
)

if "%GITHUB_CLIENT_SECRET%"=="" (
    echo ⚠️  GITHUB_CLIENT_SECRET no configurado
    echo    Configura: set GITHUB_CLIENT_SECRET=tu_client_secret
)

if "%GOOGLE_CLIENT_ID%"=="" (
    echo ⚠️  GOOGLE_CLIENT_ID no configurado
    echo    Configura: set GOOGLE_CLIENT_ID=tu_client_id
)

if "%GOOGLE_CLIENT_SECRET%"=="" (
    echo ⚠️  GOOGLE_CLIENT_SECRET no configurado
    echo    Configura: set GOOGLE_CLIENT_SECRET=tu_client_secret
)

if "%JWT_SECRET%"=="" (
    echo ⚠️  JWT_SECRET no configurado
    echo    Genera uno con: python -c "import secrets; print(secrets.token_hex(32))"
)

if "%SECRET_KEY%"=="" (
    echo ⚠️  SECRET_KEY no configurado
    echo    Genera uno con: python -c "import secrets; print(secrets.token_hex(32))"
)

echo.
echo 🌐 URLs de acceso:
echo    Frontend: http://localhost:8000
echo    Login:    http://localhost:8000/login.html
echo    Chat:     http://localhost:8000/chat.html
echo    Auth API: http://localhost:5001
echo.

REM Iniciar servidor de autenticación en background
echo 🔐 Iniciando servidor de autenticación...
start /B python backend\auth_server.py

REM Esperar un momento para que el servidor de auth inicie
timeout /t 3 /nobreak >nul

REM Iniciar servidor del frontend
echo 🎨 Iniciando servidor del frontend...
cd web
start /B python -m http.server 8000
cd ..

echo.
echo ✅ Capibara6 iniciado correctamente!
echo.
echo 🔗 Accede a: http://localhost:8000/login.html
echo.
echo 📋 Para detener los servidores, cierra esta ventana
echo.

pause
