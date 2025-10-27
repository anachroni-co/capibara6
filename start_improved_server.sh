#!/bin/bash
# Script para iniciar el servidor mejorado de Capibara6

echo "🚀 Iniciando Servidor Capibara6 Mejorado..."
echo "=========================================="

# Verificar si el puerto 5001 está en uso
if lsof -i :5001 > /dev/null 2>&1; then
    echo "⚠️ Puerto 5001 ya está en uso. Deteniendo proceso..."
    PID=$(lsof -ti :5001)
    kill -9 $PID
    sleep 2
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "📦 Activando entorno virtual..."
    source venv/bin/activate
fi

# Instalar dependencias si es necesario
if [ -f "backend/requirements.txt" ]; then
    echo "📋 Verificando dependencias..."
    if command -v pip3 &> /dev/null; then
        pip3 install -r backend/requirements.txt > /dev/null 2>&1
    elif command -v pip &> /dev/null; then
        pip install -r backend/requirements.txt > /dev/null 2>&1
    else
        echo "⚠️ Advertencia: No se encontró pip instalado"
    fi
fi

# Cambiar al directorio backend
cd backend

echo "🔧 Iniciando servidor en puerto 5001..."
echo "🌐 URL: http://localhost:5001"
echo "📡 API: http://localhost:5001/api/chat"
echo "🏥 Health: http://localhost:5001/health"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "=========================================="

# Detectar comando de Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: No se encontró Python instalado"
    exit 1
fi

echo "🐍 Usando: $PYTHON_CMD"

# Iniciar el servidor
$PYTHON_CMD capibara6_integrated_server.py
