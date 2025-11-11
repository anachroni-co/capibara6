#!/bin/bash
# start_capibara6.sh - Script para iniciar todos los servicios de Capibara6

echo "🚀 Iniciando sistema Capibara6..."

# Verificar que Ollama esté corriendo
echo "🔍 Verificando Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama está corriendo"
else
    echo "❌ Ollama no está corriendo. Iniciando Ollama..."
    # Ajustar según cómo se inicie Ollama en su sistema
    # systemctl start ollama (si está instalado como servicio)
fi

# Iniciar el servidor backend
echo "🔌 Iniciando servidor backend en puerto 5001..."
cd backend
python3 server_gptoss.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "📊 Backend iniciado con PID: $BACKEND_PID"

# Esperar un momento para que el backend inicie
sleep 3

# Verificar que el backend esté corriendo
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "✅ Backend está corriendo en el puerto 5001"
else
    echo "❌ Backend no está respondiendo. Revisando logs..."
    tail -n 20 backend.log
    exit 1
fi

echo ""
echo "🎉 Capibara6 está listo!"
echo ""
echo "🔌 Servicios:"
echo "   Backend: http://localhost:5001"
echo "   Health check: http://localhost:5001/api/health"
echo "   Chat API: http://localhost:5001/api/chat"
echo ""
echo "🌐 Para iniciar el frontend:"
echo "   cd web && python3 -m http.server 8000"
echo "   Luego abrir: http://localhost:8000/chat.html"
echo ""
echo "📝 Documentación: FIX_CONNECTION_ISSUE.md"
echo ""
echo "PID del backend: $BACKEND_PID (guardar para detenerlo después)"