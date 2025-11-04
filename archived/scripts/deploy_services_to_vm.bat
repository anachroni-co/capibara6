@echo off
echo ========================================
echo  Deploy Kyutai TTS + Smart MCP a VM
echo ========================================
echo.

REM Configuracion de la VM
set VM_NAME=gemma-3-12b
set ZONE=europe-southwest1-b
set VM_USER=gmarco

echo [1/7] Creando directorios en la VM...
gcloud compute ssh %VM_NAME% --zone=%ZONE% --command="mkdir -p ~/capibara6/backend"
if %errorlevel% neq 0 (
    echo ERROR: No se pudo conectar a la VM
    echo Verifica que la VM este corriendo: gcloud compute instances list
    pause
    exit /b 1
)

echo.
echo [2/7] Copiando servidor Kyutai TTS...
gcloud compute scp backend/kyutai_tts_server.py %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%

echo.
echo [3/7] Copiando servidor Smart MCP...
gcloud compute scp backend/smart_mcp_server.py %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%

echo.
echo [4/7] Copiando requirements...
gcloud compute scp backend/requirements.txt %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%

echo.
echo [5/7] Copiando scripts de inicio...
gcloud compute scp backend/start_kyutai_tts.sh %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%
gcloud compute scp backend/start_smart_mcp.sh %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%

echo.
echo [6/7] Configurando firewall GCP (si no existe)...
gcloud compute firewall-rules describe allow-kyutai-tts >nul 2>&1
if %errorlevel% neq 0 (
    echo Creando regla de firewall para puerto 5001...
    gcloud compute firewall-rules create allow-kyutai-tts --allow=tcp:5001 --source-ranges=0.0.0.0/0 --description="Kyutai TTS Server"
) else (
    echo Regla de firewall para TTS ya existe
)

gcloud compute firewall-rules describe allow-smart-mcp >nul 2>&1
if %errorlevel% neq 0 (
    echo Creando regla de firewall para puerto 5003...
    gcloud compute firewall-rules create allow-smart-mcp --allow=tcp:5003 --source-ranges=0.0.0.0/0 --description="Smart MCP Server"
) else (
    echo Regla de firewall para MCP ya existe
)

echo.
echo [7/7] Preparando virtualenv y permisos en la VM...
gcloud compute ssh %VM_NAME% --zone=%ZONE% --command="cd ~/capibara6/backend && chmod +x start_kyutai_tts.sh start_smart_mcp.sh && echo 'Permisos configurados'"

echo.
echo ========================================
echo  Deploy completado!
echo ========================================
echo.
echo Proximos pasos:
echo.
echo 1. Conectar a la VM:
echo    gcloud compute ssh %VM_NAME% --zone=%ZONE%
echo.
echo 2. Iniciar Kyutai TTS (en screen):
echo    screen -S kyutai-tts
echo    cd ~/capibara6/backend
echo    ./start_kyutai_tts.sh
echo    [Ctrl+A, D para salir]
echo    (La primera vez instalara dependencias - tardara ~5 min)
echo.
echo 3. Iniciar Smart MCP (en otro screen):
echo    screen -S smart-mcp
echo    cd ~/capibara6/backend
echo    ./start_smart_mcp.sh
echo    [Ctrl+A, D para salir]
echo.
echo 4. Verificar servicios:
echo    curl http://$(gcloud compute instances describe %VM_NAME% --zone=%ZONE% --format="get(networkInterfaces[0].accessConfigs[0].natIP)"):5001/health
echo    curl http://$(gcloud compute instances describe %VM_NAME% --zone=%ZONE% --format="get(networkInterfaces[0].accessConfigs[0].natIP)"):5003/health
echo.
echo Servicios disponibles:
echo - Gemma Model:  Puerto 8080
echo - Kyutai TTS:   Puerto 5001
echo - Smart MCP:    Puerto 5003
echo.
echo ========================================
pause

