#!/bin/bash
# Script para iniciar Kyutai TTS Server con virtualenv
# Uso: ./start_kyutai_tts.sh

echo "========================================="
echo "  Iniciando Kyutai TTS Server"
echo "========================================="

cd ~/capibara6/backend

# Verificar que el archivo existe
if [ ! -f "kyutai_tts_server.py" ]; then
    echo "❌ Error: kyutai_tts_server.py no encontrado"
    echo "💡 Ejecutar primero: deploy_services_to_vm.sh"
    exit 1
fi

# Crear virtualenv si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando virtualenv..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error creando virtualenv"
        echo "💡 Instalar: sudo apt install python3-venv"
        exit 1
    fi
    echo "✅ Virtualenv creado"
fi

# Activar virtualenv
source venv/bin/activate

# Verificar e instalar dependencias
echo "📦 Verificando dependencias..."

python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚙️  Instalando Flask..."
    pip install flask flask-cors
fi

python -c "import moshi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚙️  Instalando Moshi y dependencias (esto puede tardar varios minutos)..."
    pip install moshi>=0.2.6
    pip install torch torchaudio soundfile numpy transformers huggingface-hub
fi

echo ""
echo "✅ Dependencias listas"
echo ""
echo "⚠️  NOTA: Usando servidor fallback (Kyutai TTS API en investigación)"
echo "💡 El frontend usará Web Speech API del navegador"
echo "🔗 Ver: KYUTAI_TTS_PENDIENTE.md para más info"
echo ""
echo "🚀 Iniciando servidor en puerto 5001..."
echo ""

# Ejecutar servidor simple (fallback)
python kyutai_tts_server_simple.py

