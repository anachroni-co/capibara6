#!/bin/bash
# Script para descargar modelos desde Google Cloud Storage

echo "📥 Descargando Modelos GPT-OSS desde Google Cloud Storage"
echo "========================================================"

BUCKET="gs://gptoss-models"
LOCAL_DIR="/home/elect/models"

# Crear directorio local si no existe
mkdir -p "$LOCAL_DIR"

echo "📁 Directorio destino: $LOCAL_DIR"
echo "🪣 Bucket origen: $BUCKET"

# Verificar espacio disponible
AVAILABLE_SPACE=$(df /home | tail -1 | awk '{print $4}')
echo "💾 Espacio disponible: $((AVAILABLE_SPACE / 1024 / 1024)) GB"

echo ""
echo "🔍 Listando modelos disponibles..."
gsutil ls -la "$BUCKET/"

echo ""
echo "📥 Descargando modelos..."

# Descargar todos los archivos del bucket
if gsutil -m cp -r "$BUCKET/*" "$LOCAL_DIR/"; then
    echo "✅ Modelos descargados exitosamente"
    
    echo ""
    echo "📁 Contenido descargado:"
    ls -la "$LOCAL_DIR/"
    
    echo ""
    echo "🔍 Buscando archivos de modelo..."
    find "$LOCAL_DIR" -name "*.gguf" -o -name "*.bin" -o -name "*.safetensors" | head -10
    
    echo ""
    echo "🎯 Próximos pasos:"
    echo "1. Configurar servidor con: ./configure_server.sh"
    echo "2. Iniciar servidor con: ./start_improved_server.sh"
    
else
    echo "❌ Error descargando modelos"
    echo "💡 Verificar permisos y conexión"
    exit 1
fi
