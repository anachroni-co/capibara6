#!/bin/bash
# Script para configurar el servidor con los modelos descargados

echo "⚙️ Configurando Servidor con Modelos GPT-OSS"
echo "==========================================="

MODELS_DIR="/home/elect/models"
SERVER_CONFIG="/home/elect/backend/capibara6_integrated_server.py"

echo "📁 Directorio de modelos: $MODELS_DIR"

# Verificar si existen modelos
if [ ! -d "$MODELS_DIR" ]; then
    echo "❌ Directorio de modelos no existe"
    echo "💡 Ejecutar primero: ./download_models.sh"
    exit 1
fi

# Buscar archivos de modelo
MODEL_FILES=$(find "$MODELS_DIR" -name "*.gguf" -o -name "*.bin" -o -name "*.safetensors" | head -5)

if [ -z "$MODEL_FILES" ]; then
    echo "❌ No se encontraron archivos de modelo"
    echo "💡 Verificar que los modelos se descargaron correctamente"
    exit 1
fi

echo "✅ Modelos encontrados:"
echo "$MODEL_FILES"

# Obtener el modelo principal (el más grande o el primero)
MAIN_MODEL=$(find "$MODELS_DIR" -name "*.gguf" | head -1)
if [ -z "$MAIN_MODEL" ]; then
    MAIN_MODEL=$(find "$MODELS_DIR" -name "*.bin" | head -1)
fi

if [ -z "$MAIN_MODEL" ]; then
    MAIN_MODEL=$(find "$MODELS_DIR" -name "*.safetensors" | head -1)
fi

echo ""
echo "🎯 Modelo principal: $MAIN_MODEL"

# Crear script de inicio del modelo
cat > /home/elect/start_model.sh << EOF
#!/bin/bash
# Script para iniciar el modelo GPT-OSS-20B

MODEL_PATH="$MAIN_MODEL"
echo "🚀 Iniciando modelo GPT-OSS-20B..."
echo "📁 Modelo: \$MODEL_PATH"

# Verificar si el modelo existe
if [ ! -f "\$MODEL_PATH" ]; then
    echo "❌ Error: Modelo no encontrado en \$MODEL_PATH"
    exit 1
fi

# Iniciar el servidor del modelo (ajustar según el tipo de servidor)
if [[ "\$MODEL_PATH" == *.gguf ]]; then
    echo "🔧 Iniciando servidor llama.cpp..."
    # Ajustar parámetros según tu configuración
    ./llama-server -m "\$MODEL_PATH" --port 8080 --host 0.0.0.0 --ctx-size 4096 --threads 8
elif [[ "\$MODEL_PATH" == *.bin ]]; then
    echo "🔧 Iniciando servidor transformers..."
    # Ajustar según tu configuración
    python3 -m transformers.serving --model "\$MODEL_PATH" --port 8080
else
    echo "❌ Formato de modelo no soportado: \$MODEL_PATH"
    exit 1
fi
EOF

chmod +x /home/elect/start_model.sh

echo ""
echo "✅ Script de inicio del modelo creado: /home/elect/start_model.sh"

# Crear script de inicio completo
cat > /home/elect/start_complete_system.sh << EOF
#!/bin/bash
# Script para iniciar el sistema completo

echo "🚀 Iniciando Sistema Completo Capibara6"
echo "======================================"

# Función para limpiar procesos al salir
cleanup() {
    echo "🛑 Deteniendo servicios..."
    pkill -f "llama-server"
    pkill -f "capibara6_integrated_server"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar modelo en background
echo "📡 Iniciando modelo GPT-OSS-20B..."
./start_model.sh &
MODEL_PID=\$!

# Esperar a que el modelo esté listo
echo "⏳ Esperando a que el modelo esté listo..."
sleep 10

# Verificar que el modelo esté funcionando
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ Modelo funcionando correctamente"
else
    echo "⚠️ Modelo no responde, continuando..."
fi

# Iniciar servidor integrado
echo "🌐 Iniciando servidor integrado..."
cd /home/elect/backend
python3 capibara6_integrated_server.py &
SERVER_PID=\$!

echo ""
echo "🎉 Sistema iniciado correctamente!"
echo "📡 Modelo: http://localhost:8080"
echo "🌐 Servidor: http://localhost:5001"
echo "🏥 Health: http://localhost:5001/health"
echo ""
echo "Presiona Ctrl+C para detener todo"

# Esperar
wait
EOF

chmod +x /home/elect/start_complete_system.sh

echo ""
echo "✅ Script del sistema completo creado: /home/elect/start_complete_system.sh"

echo ""
echo "🎯 Comandos disponibles:"
echo "1. Iniciar solo el modelo: ./start_model.sh"
echo "2. Iniciar sistema completo: ./start_complete_system.sh"
echo "3. Probar sistema: ./test_quick.sh"

echo ""
echo "📊 Información del modelo:"
echo "   - Ruta: $MAIN_MODEL"
echo "   - Tamaño: $(du -h "$MAIN_MODEL" | cut -f1)"
echo "   - Tipo: $(file "$MAIN_MODEL" | cut -d: -f2)"
