#!/bin/bash

echo "🚀 Iniciando servicios de Capibara6 en la VM (gpt-oss-20b)..."

# Verificar si ya hay screens corriendo
echo "📋 Screens actuales:"
screen -ls

# Matar screens existentes si los hay
echo "🔄 Limpiando screens existentes..."
screen -S gemma -X quit 2>/dev/null || true
screen -S smart-mcp -X quit 2>/dev/null || true
screen -S tts -X quit 2>/dev/null || true

# Iniciar servidor principal (Gemma)
echo "🤖 Iniciando servidor Gemma en puerto 8080..."
screen -dmS gemma bash -c "cd ~/capibara6/backend && python server.py"

# Iniciar Smart MCP
echo "🧠 Iniciando Smart MCP en puerto 5010..."
screen -dmS smart-mcp bash -c "cd ~/capibara6/backend && python smart_mcp_server.py"

# Iniciar TTS
echo "🎙️ Iniciando TTS en puerto 5002..."
screen -dmS tts bash -c "cd ~/capibara6/backend && python coqui_tts_server.py"

# Esperar un momento para que los servicios se inicien
echo "⏳ Esperando que los servicios se inicien..."
sleep 10

# Verificar estado
echo "📊 Estado de los servicios:"
screen -ls

echo "🧪 Probando servicios..."
echo "Gemma (8080):"
curl -s http://localhost:8080/completion || echo "❌ Gemma no responde"

echo "Smart MCP (5010):"
curl -s http://localhost:5010/health || echo "❌ Smart MCP no responde"

echo "TTS (5002):"
curl -s http://localhost:5002/health || echo "❌ TTS no responde"

echo "✅ Script completado!"
