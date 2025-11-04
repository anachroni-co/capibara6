@echo off
echo ========================================
echo  Iniciando Servidor MCP - Capibara6
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist .venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo ADVERTENCIA: No se encontro entorno virtual
    echo Ejecutando con Python del sistema
)

echo.
echo Iniciando servidor MCP en http://localhost:5003
echo.

cd backend
python mcp_server.py

pause

