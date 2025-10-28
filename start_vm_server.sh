#!/bin/bash

echo "🚀 Iniciando Servidor Capibara6 en VM..."
echo "=========================================="

# Detener procesos existentes
echo "🛑 Deteniendo procesos existentes..."
sudo pkill -f "capibara6_integrated_server.py" 2>/dev/null || true
sudo pkill -f "python.*5001" 2>/dev/null || true

# Esperar un momento
sleep 2

# Verificar que el puerto esté libre
if lsof -i :5001 >/dev/null 2>&1; then
    echo "⚠️ Puerto 5001 aún en uso, forzando liberación..."
    sudo fuser -k 5001/tcp 2>/dev/null || true
    sleep 2
fi

# Activar entorno virtual
echo "🐍 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
pip install flask flask-cors requests numpy scipy >/dev/null 2>&1

# Ejecutar servidor
echo "🌐 Iniciando servidor en puerto 5001..."
echo "🔗 URL: http://34.175.215.109:5001"
echo "📡 API: http://34.175.215.109:5001/api/chat"
echo "🏥 Health: http://34.175.215.109:5001/health"
echo "=========================================="

# Ejecutar en background con nohup
nohup python3 capibara6_integrated_server.py > server.log 2>&1 &

# Obtener PID del proceso
SERVER_PID=$!
echo "🆔 PID del servidor: $SERVER_PID"

# Esperar un momento y verificar que esté funcionando
sleep 3

if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Servidor iniciado correctamente"
    echo "📋 Para ver logs: tail -f server.log"
    echo "🛑 Para detener: kill $SERVER_PID"
else
    echo "❌ Error al iniciar el servidor"
    echo "📋 Revisar logs: cat server.log"
    exit 1
fi
