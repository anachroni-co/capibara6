#!/bin/bash
# Script de prueba rápida para verificar las mejoras

echo "🧪 Prueba Rápida de Mejoras GPT-OSS-20B"
echo "======================================="

# Verificar que el servidor esté ejecutándose
echo "🔍 Verificando servidor..."
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ Servidor funcionando en puerto 5001"
else
    echo "❌ Servidor no está ejecutándose. Inicia con: ./start_improved_server.sh"
    exit 1
fi

# Probar pregunta simple
echo ""
echo "🤖 Probando pregunta: ¿Cómo te llamas?"
echo "----------------------------------------"

RESPONSE=$(curl -s -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo te llamas?"}')

echo "📝 Respuesta recibida:"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"

# Extraer solo el texto de la respuesta
RESPONSE_TEXT=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('response', ''))" 2>/dev/null)

if [ -n "$RESPONSE_TEXT" ]; then
    LENGTH=${#RESPONSE_TEXT}
    echo ""
    echo "📊 Análisis de la respuesta:"
    echo "   - Longitud: $LENGTH caracteres"
    
    if [ $LENGTH -gt 50 ]; then
        echo "   ✅ Longitud adecuada (>50 caracteres)"
    else
        echo "   ⚠️ Respuesta muy corta (<50 caracteres)"
    fi
    
    if [[ "$RESPONSE_TEXT" == *"Capibara6"* ]]; then
        echo "   ✅ Menciona Capibara6"
    else
        echo "   ⚠️ No menciona Capibara6"
    fi
    
    if [[ "$RESPONSE_TEXT" == *"I am a large language model"* ]]; then
        echo "   ❌ Respuesta genérica detectada"
    else
        echo "   ✅ Respuesta específica"
    fi
else
    echo "❌ No se pudo extraer la respuesta"
fi

echo ""
echo "🎯 Prueba completada!"
echo "Si ves ✅ en todos los puntos, las mejoras están funcionando correctamente."
