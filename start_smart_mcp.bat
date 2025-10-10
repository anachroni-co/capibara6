@echo off
echo.
echo ========================================
echo  🚀 Smart MCP Server v2.0
echo  Selective RAG for Capibara6
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist .venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Instalar dependencias si es necesario
pip install -q flask flask-cors

echo.
echo ✅ Iniciando Smart MCP Server en puerto 5003...
echo.

python backend/smart_mcp_server.py

pause

