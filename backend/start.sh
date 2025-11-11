<<<<<<< HEAD
<<<<<<< HEAD
#!/bin/bash
# Script de inicio rápido para el backend de capibara6 - Optimizado para Kyutai TTS

echo "🦫 Iniciando backend de capibara6 con Kyutai TTS..."

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📥 Instalando dependencias..."
pip install -q -r requirements.txt

# Verificar si existen dependencias de Kyutai TTS
echo "🧪 Verificando dependencias de Kyutai TTS..."
if python -c "import moshi" 2>/dev/null; then
    echo "✅ Kyutai TTS (moshi) disponible"
else
    echo "⚠️  Kyutai TTS (moshi) no encontrado, instalando..."
    pip install --no-cache-dir moshi>=0.2.6 torch torchaudio soundfile transformers huggingface-hub
fi

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado!"
    echo "📝 Copia env.example a .env y configura tus credenciales SMTP:"
    echo "   cp env.example .env"
    echo "   nano .env"
    exit 1
fi

# Crear directorios necesarios
mkdir -p user_data
mkdir -p logs

# Iniciar servidor integrado en puerto 5001 con Kyutai TTS completo
echo "🎵 Iniciando servidor integrado con Kyutai TTS en http://localhost:5001"
echo "🚀 Componentes: GPT-OSS-20B Proxy + Smart MCP + Kyutai TTS (reemplaza Coqui)"

# Verificar si el puerto 5001 está ocupado
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  El puerto 5001 ya está en uso, liberando..."
    fuser -k 5001/tcp 2>/dev/null || true
    sleep 2
fi

# Iniciar servidor
python capibara6_integrated_server.py

echo "🛑 Servidor detenido"
=======
=======
>>>>>>> feature/rag-infra
#!/bin/bash
# Script de inicio rápido para el backend de capibara6

echo "🦫 Iniciando backend de capibara6..."

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📥 Instalando dependencias..."
pip install -q -r requirements.txt

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado!"
    echo "📝 Copia env.example a .env y configura tus credenciales SMTP:"
    echo "   cp env.example .env"
    echo "   nano .env"
    exit 1
fi

# Crear directorio de datos
mkdir -p user_data

# Iniciar servidor
echo "🚀 Iniciando servidor en http://localhost:5000"
python server.py

<<<<<<< HEAD
>>>>>>> 249cd7d (new files)
=======
>>>>>>> feature/rag-infra
