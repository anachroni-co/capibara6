#!/bin/bash
# Script para verificar acceso a Google Cloud Storage

echo "🔍 Verificando Acceso a Google Cloud Storage"
echo "============================================="

# Verificar si gcloud está instalado
if command -v gcloud &> /dev/null; then
    echo "✅ gcloud CLI está instalado"
    gcloud version
else
    echo "❌ gcloud CLI no está instalado"
    echo "💡 Instalar con: curl https://sdk.cloud.google.com | bash"
    exit 1
fi

echo ""
echo "🔐 Verificando autenticación..."
if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "✅ Autenticado en Google Cloud"
    gcloud auth list --filter=status:ACTIVE
else
    echo "❌ No estás autenticado"
    echo "💡 Ejecutar: gcloud auth login"
    exit 1
fi

echo ""
echo "📦 Verificando acceso al bucket de modelos..."
if gsutil ls gs://gptoss-models/ > /dev/null 2>&1; then
    echo "✅ Acceso al bucket gs://gptoss-models confirmado"
    echo ""
    echo "📁 Contenido del bucket:"
    gsutil ls -la gs://gptoss-models/
else
    echo "❌ No se puede acceder al bucket gs://gptoss-models"
    echo "💡 Verificar permisos y configuración"
    exit 1
fi

echo ""
echo "🔍 Buscando modelos GPT-OSS..."
MODELS=$(gsutil ls gs://gptoss-models/ | grep -E "\.(gguf|bin|safetensors)$" || echo "No se encontraron modelos")
echo "Modelos encontrados:"
echo "$MODELS"

echo ""
echo "💾 Verificando espacio en disco..."
df -h /home

echo ""
echo "🎯 Próximos pasos:"
echo "1. Si hay modelos, descargar con: ./download_models.sh"
echo "2. Si no hay modelos, subir con: ./upload_models.sh"
echo "3. Configurar servidor con: ./configure_server.sh"
