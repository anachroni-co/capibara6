@echo off
REM Script para deployar Smart MCP en la VM de GCP (Windows)

echo 🚀 Deployando Smart MCP a la VM...

set VM_NAME=gemma-3-12b
set ZONE=us-east1-b
set VM_HOST=34.175.104.187

echo 📁 Creando directorios...
gcloud compute ssh %VM_NAME% --zone=%ZONE% --command="mkdir -p ~/capibara6/backend"

echo 📤 Copiando archivos...
gcloud compute scp backend/smart_mcp_server.py %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%
gcloud compute scp backend/requirements.txt %VM_NAME%:~/capibara6/backend/ --zone=%ZONE%

echo ⚙️ Configurando servicio...
gcloud compute ssh %VM_NAME% --zone=%ZONE% --command="cd ~/capibara6/backend && python3 -m pip install --user -r requirements.txt"

echo.
echo ✅ Archivos copiados!
echo 📝 Ahora conéctate a la VM y ejecuta:
echo    gcloud compute ssh %VM_NAME% --zone=%ZONE%
echo    cd ~/capibara6/backend
echo    screen -S smart-mcp
echo    python3 smart_mcp_server.py
echo.
echo 🔗 Será accesible en: http://%VM_HOST%:5003
pause

