#!/usr/bin/env bash
set -e

echo "=== 🦫 Iniciando entorno Capibara (TPU Preemptible) ==="

MODEL_ID=""
CLEAN=false
DOWNLOAD=false

for arg in "$@"; do
  case $arg in
    --clean) CLEAN=true ;;
    --download) DOWNLOAD=true; shift; MODEL_ID=$1 ;;
  esac
done

# ---- Contexto GCloud ----
echo "⚙️ Configurando contexto GCloud..."
gcloud config set account marco@anachroni.co
gcloud config set project mamba-001
gcloud config set compute/zone us-central1-a

# ---- Instalar dependencias base ----
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git curl

# ---- Crear entorno virtual ----
if [ ! -d "$HOME/venv" ]; then
  python3 -m venv ~/venv
fi
source ~/venv/bin/activate

# ---- Instalar librerías PyTorch/XLA y Hugging Face ----
pip install -U pip
pip install torch torchvision torchaudio
pip install torch-xla -f https://storage.googleapis.com/libtpu-releases/index.html
pip install huggingface_hub hf-transfer  # ← ¡hf-transfer incluido!

# ---- Preparar directorio local (disco rápido) ----
sudo mkdir -p /mnt/models
sudo chown $USER:$USER /mnt/models

# ---- Limpieza opcional ----
if [ "$CLEAN" = true ]; then
  echo "🧹 Limpiando procesos antiguos..."
  pkill -f "hf download" || true
  find /mnt/models/ -name "*.lock" -delete || true
  find /mnt/models/ -name "*.incomplete" -delete || true
fi

# ---- Descarga de modelo ----
if [ "$DOWNLOAD" = true ]; then
  if [ -z "$MODEL_ID" ]; then
    echo "❌ Debes indicar el modelo. Ejemplo:"
    echo "   bash startup.sh --download openchat/gpt-oss-120b"
    exit 1
  fi

  TARGET_DIR="/mnt/models/$(basename $MODEL_ID)"
  mkdir -p "$TARGET_DIR"

  echo "⬇️ Descargando modelo: $MODEL_ID → $TARGET_DIR"
  echo "🚀 Usando hf-transfer (alta velocidad)..."

  # Ejecutar con aceleración y sin symlinks
  nohup env HF_HUB_ENABLE_HF_TRANSFER=1 \
    hf download "$MODEL_ID" \
      --repo-type model \
      --include "original/*" \
      --local-dir "$TARGET_DIR" \
      --local-dir-use-symlinks False \
      > ~/download.log 2>&1 &

  echo "📝 Log: tail -f ~/download.log"
fi

# ---- Monitoreo (solo si se descarga) ----
if [ "$DOWNLOAD" = true ]; then
  echo "📊 Monitoreando progreso cada 5 min..."
  while true; do
    echo "----- $(date) -----"
    du -sh /mnt/models/* 2>/dev/null | head -n 5
    sleep 300
  done
else
  echo "✔️ Entorno listo."
fi