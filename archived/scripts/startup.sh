#!/bin/bash
set -e

echo "=== 🚀 Inicializando entorno GPT-OSS-120B en TPU v5litepod-64 ==="

# Variables base
BUCKET_NAME="gptoss-models"
MOUNT_DIR="/mnt/models"
MODEL_DIR="$MOUNT_DIR/gpt-oss-120b"
ZONE="us-central1-a"
LOG_FILE="$HOME/download.log"

# ==========================================================
# 1. Instalación de dependencias básicas
# ==========================================================
sudo apt update -y
sudo apt install -y python3-pip git-lfs gcsfuse nload iftop htop tmux

# ==========================================================
# 2. Montaje del bucket remoto
# ==========================================================
echo "Montando bucket $BUCKET_NAME..."
sudo mkdir -p $MOUNT_DIR
sudo gcsfuse --implicit-dirs $BUCKET_NAME $MOUNT_DIR

# Verificación
if df -h | grep -q "$MOUNT_DIR"; then
  echo "✅ Bucket montado correctamente en $MOUNT_DIR"
else
  echo "❌ Error montando bucket $BUCKET_NAME"
  exit 1
fi

# ==========================================================
# 3. Instalar versión reciente de Hugging Face Hub
# ==========================================================
pip install -U pip
pip install -U "huggingface_hub[cli]" gpt-oss

# ==========================================================
# 4. Autenticación automática (usa token desde metadata)
# ==========================================================
if [ -n "$HUGGINGFACE_TOKEN" ]; then
  echo "$HUGGINGFACE_TOKEN" | hf auth login --token
  echo "✅ Autenticado en Hugging Face (token desde metadata)"
else
  echo "⚠️ No se encontró HUGGINGFACE_TOKEN. Debes ejecutar manualmente:"
  echo "   hf auth login"
fi

# ==========================================================
# 5. Preparar directorios
# ==========================================================
sudo mkdir -p $MODEL_DIR
sudo chmod -R 777 $MODEL_DIR
echo "Estructura preparada en $MODEL_DIR"

# ==========================================================
# 6. Lanzar descarga con reanudación
# ==========================================================
echo "📦 Iniciando descarga del modelo GPT-OSS-120B..."
nohup hf download openai/gpt-oss-120b \
  --include "original/*" \
  --repo-type model \
  --local-dir $MODEL_DIR \
  --resume-download > $LOG_FILE 2>&1 &

echo "✅ Descarga iniciada en segundo plano."
echo "Monitoriza con:"
echo "  tail -f $LOG_FILE"
echo "  sudo nload ens9"
echo "  du -sh $MODEL_DIR/.cache/huggingface/download/original/"

# ==========================================================
# 7. Resumen final
# ==========================================================
echo "=== 🧩 Configuración completada ==="
df -h $MOUNT_DIR
ps aux | grep 'hf download' | grep -v grep
