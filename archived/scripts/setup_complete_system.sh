#!/bin/bash
# Script completo para configurar el sistema GPT-OSS-20B

echo "🚀 Configuración Completa del Sistema GPT-OSS-20B"
echo "================================================"

# Verificar que estamos en la VM
if [ ! -f "/home/elect/backend/capibara6_integrated_server.py" ]; then
    echo "❌ Error: No se encontró el directorio del proyecto"
    echo "💡 Asegúrate de estar en /home/elect"
    exit 1
fi

echo "✅ Directorio del proyecto encontrado"

# Paso 1: Verificar Google Cloud Storage
echo ""
echo "🔍 Paso 1: Verificando Google Cloud Storage..."
if ./check_cloud_storage.sh; then
    echo "✅ Google Cloud Storage configurado"
else
    echo "❌ Error con Google Cloud Storage"
    exit 1
fi

# Paso 2: Descargar modelos
echo ""
echo "📥 Paso 2: Descargando modelos..."
if ./download_models.sh; then
    echo "✅ Modelos descargados"
else
    echo "❌ Error descargando modelos"
    exit 1
fi

# Paso 3: Configurar servidor
echo ""
echo "⚙️ Paso 3: Configurando servidor..."
if ./configure_server.sh; then
    echo "✅ Servidor configurado"
else
    echo "❌ Error configurando servidor"
    exit 1
fi

# Paso 4: Instalar dependencias
echo ""
echo "📦 Paso 4: Instalando dependencias..."
cd /home/elect/backend
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "✅ Dependencias instaladas"
else
    echo "⚠️ No se encontró requirements.txt"
fi

# Paso 5: Hacer scripts ejecutables
echo ""
echo "🔧 Paso 5: Configurando permisos..."
cd /home/elect
chmod +x *.sh
chmod +x backend/*.py

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Comandos disponibles:"
echo "1. Verificar sistema: ./check_cloud_storage.sh"
echo "2. Iniciar modelo: ./start_model.sh"
echo "3. Iniciar sistema completo: ./start_complete_system.sh"
echo "4. Probar sistema: ./test_quick.sh"
echo ""
echo "🌐 URLs del sistema:"
echo "   - Modelo: http://localhost:8080"
echo "   - Servidor: http://localhost:5001"
echo "   - Health: http://localhost:5001/health"
echo ""
echo "🚀 Para iniciar todo: ./start_complete_system.sh"
