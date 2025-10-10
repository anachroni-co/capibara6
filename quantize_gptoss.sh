#!/bin/bash
set -e

echo "=== ⚙️ Cuantificación INT8 de gpt-oss-120B ==="

MODEL_ORIG="/mnt/models/gpt-oss-120b/original"
MODEL_OUT="/mnt/models/gpt-oss-120b-int8"

# Activar entorno virtual (creado por startup.sh)
source /opt/venv/bin/activate

# Instalar dependencias necesarias
pip install -U auto-gptq transformers accelerate safetensors --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu122/

# Verificar existencia del modelo original
if [ ! -d "$MODEL_ORIG" ]; then
  echo "❌ No se encontró el modelo original en $MODEL_ORIG"
  exit 1
fi

# Crear carpeta destino
mkdir -p "$MODEL_OUT"

# Ejecutar cuantificación
python - <<'PY'
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from transformers import AutoTokenizer
import torch, os

model_name = "/mnt/models/gpt-oss-120b/original"
save_dir = "/mnt/models/gpt-oss-120b-int8"

print(f"🧩 Cargando modelo desde {model_name}...")
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
quant_config = BaseQuantizeConfig(bits=8, group_size=128, desc_act=False)

model = AutoGPTQForCausalLM.from_pretrained(
    model_name,
    quantize_config=quant_config,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("⚙️ Iniciando cuantificación a INT8...")
model.quantize(examples=["El mundo cambia con la inteligencia artificial."])

print(f"💾 Guardando modelo cuantizado en {save_dir} ...")
model.save_quantized(save_dir)
tokenizer.save_pretrained(save_dir)

print("✅ Cuantificación completada correctamente.")
PY

# Mostrar tamaño final
echo "📦 Tamaño final del modelo cuantizado:"
du -sh "$MODEL_OUT"

echo "=== 🟢 Proceso de cuantificación finalizado ==="
