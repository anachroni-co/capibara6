@echo off
REM Script para subir las mejoras GPT-OSS-20B a la VM de Google Cloud

echo 🚀 Subiendo Mejoras GPT-OSS-20B a la VM
echo =======================================

REM Configuración de la VM
set VM_USER=gmarco
set VM_IP=34.175.215.109
set VM_PATH=/home/elect

echo 📡 Conectando a la VM: %VM_USER%@%VM_IP%
echo 📁 Directorio destino: %VM_PATH%
echo.

REM Verificar conexión SSH
echo 🔍 Verificando conexión SSH...
ssh -o ConnectTimeout=10 -o BatchMode=yes %VM_USER%@%VM_IP% exit >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Conexión SSH exitosa
) else (
    echo ❌ Error: No se puede conectar a la VM
    echo 💡 Asegúrate de que:
    echo    - La VM esté ejecutándose
    echo    - Tengas las claves SSH configuradas
    echo    - El firewall permita conexiones SSH
    pause
    exit /b 1
)

echo.
echo 📦 Subiendo archivos mejorados...

REM Crear directorio de respaldo en la VM
echo 💾 Creando respaldo de archivos originales...
ssh %VM_USER%@%VM_IP% "mkdir -p %VM_PATH%/backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"

REM Subir archivos del backend mejorados
echo 📤 Subiendo archivos del backend...

REM Servidor integrado mejorado
scp backend\capibara6_integrated_server.py %VM_USER%@%VM_IP%:%VM_PATH%/backend/
echo    ✅ capibara6_integrated_server.py

REM Servidor GPT-OSS mejorado
scp backend\server_gptoss.py %VM_USER%@%VM_IP%:%VM_PATH%/backend/
echo    ✅ server_gptoss.py

REM Nueva configuración optimizada
scp backend\gpt_oss_optimized_config.py %VM_USER%@%VM_IP%:%VM_PATH%/backend/
echo    ✅ gpt_oss_optimized_config.py

REM Script de pruebas
scp backend\test_gpt_oss_improvements.py %VM_USER%@%VM_IP%:%VM_PATH%/backend/
echo    ✅ test_gpt_oss_improvements.py

REM Subir archivos del frontend
echo 📤 Subiendo archivos del frontend...
scp web\chat-app.js %VM_USER%@%VM_IP%:%VM_PATH%/web/
echo    ✅ chat-app.js

REM Subir scripts de inicio
echo 📤 Subiendo scripts de inicio...
scp start_improved_server.sh %VM_USER%@%VM_IP%:%VM_PATH%/
echo    ✅ start_improved_server.sh

scp test_quick.sh %VM_USER%@%VM_IP%:%VM_PATH%/
echo    ✅ test_quick.sh

REM Hacer scripts ejecutables en la VM
echo 🔧 Configurando permisos en la VM...
ssh %VM_USER%@%VM_IP% "chmod +x %VM_PATH%/start_improved_server.sh %VM_PATH%/test_quick.sh"

REM Instalar dependencias si es necesario
echo 📋 Verificando dependencias en la VM...
ssh %VM_USER%@%VM_IP% "cd %VM_PATH%/backend && pip3 install -r requirements.txt"

echo.
echo 🎉 ¡Archivos subidos exitosamente!
echo.
echo 📋 Próximos pasos en la VM:
echo 1. Conectar a la VM: ssh %VM_USER%@%VM_IP%
echo 2. Ir al directorio: cd %VM_PATH%
echo 3. Iniciar servidor mejorado: ./start_improved_server.sh
echo 4. Probar mejoras: ./test_quick.sh
echo.
echo 🌐 URLs en la VM:
echo    - Servidor: http://localhost:5001
echo    - API: http://localhost:5001/api/chat
echo    - Health: http://localhost:5001/health

pause
