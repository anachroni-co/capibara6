#!/bin/bash
# Script para iniciar Kyutai TTS Server
# Uso: ./start_kyutai_tts.sh

echo "========================================="
echo "  Iniciando Kyutai TTS Server"
echo "========================================="

cd ~/capibara6/backend

# Verificar que el archivo existe
if [ ! -f "kyutai_tts_server.py" ]; then
    echo "❌ Error: kyutai_tts_server.py no encontrado"
    echo "💡 Ejecutar primero: deploy_services_to_vm.bat"
    exit 1
fi

# Verificar dependencias
python3 -c "import moshi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ Moshi no instalado. Instalando..."
    python3 -m pip install --user moshi>=0.2.6 torch torchaudio soundfile numpy
fi

python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ Flask no instalado. Instalando..."
    python3 -m pip install --user flask flask-cors
fi

echo ""
echo "🚀 Iniciando servidor en puerto 5001..."
echo ""

python3 kyutai_tts_server.py

