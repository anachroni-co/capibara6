@echo off
echo ============================================
echo   Copiando Archivos a VM (Puerto 5002)
echo ============================================
echo.

set VM_NAME=gemma-3-12b
set ZONE=europe-southwest1-b

echo Copiando servidores actualizados...
gcloud compute scp backend/coqui_tts_server.py %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%
gcloud compute scp backend/kyutai_tts_server_simple.py %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%
gcloud compute scp backend/smart_mcp_server.py %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%

echo.
echo Copiando scripts de inicio...
gcloud compute scp backend/start_coqui_tts_py311.sh %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%
gcloud compute scp backend/start_smart_mcp.sh %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%
gcloud compute scp backend/check_all_services.sh %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%

echo.
echo Configurando firewall para puerto 5002...
gcloud compute firewall-rules create allow-coqui-tts --allow=tcp:5002 --source-ranges=0.0.0.0/0 --description="Coqui TTS Server" 2>nul
if %errorlevel% equ 0 (
    echo Firewall configurado
) else (
    echo Firewall ya existe o error configurandolo
)

echo.
echo ============================================
echo   Archivos Copiados!
echo ============================================
echo.
echo Proximos pasos EN LA VM:
echo.
echo 1. Verificar servicios:
echo    cd ~/capibara6/backend
echo    chmod +x check_all_services.sh
echo    ./check_all_services.sh
echo.
echo 2. Iniciar Smart MCP (si no esta activo):
echo    screen -S smart-mcp
echo    chmod +x start_smart_mcp.sh
echo    ./start_smart_mcp.sh
echo    [Ctrl+A, D]
echo.
echo 3. Iniciar Coqui TTS (si no esta activo):
echo    screen -S coqui-tts
echo    chmod +x start_coqui_tts_py311.sh
echo    ./start_coqui_tts_py311.sh
echo    [Ctrl+A, D]
echo.
echo ============================================
pause

