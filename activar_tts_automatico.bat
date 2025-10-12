@echo off
echo ========================================
echo   Activar Coqui TTS en la VM
echo ========================================
echo.
echo Conectando a la VM y ejecutando script...
echo.

REM Copiar script a la VM
echo [1/3] Copiando script a la VM...
gcloud compute scp EJECUTAR_EN_VM.sh gemma-3-12b:~/ --zone=europe-southwest1-b

REM Ejecutar script en la VM
echo [2/3] Ejecutando script en la VM...
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b --command="chmod +x ~/EJECUTAR_EN_VM.sh && ~/EJECUTAR_EN_VM.sh"

echo.
echo [3/3] Verificando desde exterior...
timeout /t 3 /nobreak > nul
curl http://34.175.104.187:5002/health

echo.
echo ========================================
echo   Proceso completado
echo ========================================
echo.
echo Ahora ve al chat y recarga la pagina:
echo https://www.capibara6.com/chat.html
echo Presiona: Ctrl + Shift + R
echo.
pause

