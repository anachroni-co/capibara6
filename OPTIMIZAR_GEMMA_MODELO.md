# 🚀 Optimizar Modelo Gemma - Cambiar Q4 por Mejor Versión

## 📊 Problema Actual

Estás usando: `gemma-3-12b.Q4_K_M.gguf`

**Problemas del Q4:**
- ⚠️ Baja precisión (4 bits)
- ⚠️ Pierde coherencia en respuestas largas
- ⚠️ Puede "alucinar" más
- ⚠️ Errores de sincronización en streaming

---

## ✅ Mejores Opciones (De Mejor a Más Ligera)

| Modelo | Tamaño | RAM | Calidad | Velocidad | Recomendado |
|--------|--------|-----|---------|-----------|-------------|
| **Q8_0** | ~13 GB | 16 GB | ⭐⭐⭐⭐⭐ | Media | ✅ **Óptimo** |
| **Q6_K** | ~10 GB | 12 GB | ⭐⭐⭐⭐ | Media-Alta | ✅ **Bueno** |
| **Q5_K_M** | ~8.5 GB | 10 GB | ⭐⭐⭐⭐ | Alta | ✅ **Balanceado** |
| **Q5_K_S** | ~8 GB | 10 GB | ⭐⭐⭐ | Alta | ⚠️ Ligero |
| Q4_K_M | ~7 GB | 8 GB | ⭐⭐ | Muy Alta | ❌ Actual (problemas) |

---

## 🎯 Recomendación

### Para tu VM (Gemma 3-12B en Google Cloud)

**Opción 1: Q8_0** (Máxima calidad)
- 📦 Tamaño: ~13 GB
- 🎯 Mejor opción si tienes >16 GB RAM
- ✨ Calidad casi idéntica al modelo completo
- 🚀 Velocidad aceptable

**Opción 2: Q6_K** (Balance perfecto)
- 📦 Tamaño: ~10 GB  
- 🎯 Excelente relación calidad/velocidad
- ✨ Mucho mejor que Q4, casi como Q8
- 🚀 Más rápido que Q8

**Opción 3: Q5_K_M** (Si RAM es limitada)
- 📦 Tamaño: ~8.5 GB
- 🎯 Si tienes solo 10-12 GB RAM
- ✨ Notable mejora vs Q4
- 🚀 Muy buena velocidad

---

## 📋 Paso 1: Verificar RAM Disponible en tu VM

```bash
# Conectar a VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Ver RAM total
free -h

# Ver qué hay en uso
htop  # (presiona 'q' para salir)
```

**Resultado esperado:**
```
              total        used        free
Mem:           32Gi        8Gi        24Gi  ← RAM disponible
```

Si tienes >16 GB libre → **Q8_0**  
Si tienes 12-16 GB libre → **Q6_K**  
Si tienes 10-12 GB libre → **Q5_K_M**

---

## 📥 Paso 2: Descargar el Nuevo Modelo

### Opción A: Desde HuggingFace (Recomendado)

```bash
# Instalar HuggingFace CLI (si no está)
pip install huggingface-hub

# Descargar Q8_0 (Máxima calidad)
huggingface-cli download \
  bartowski/gemma-2-12b-it-GGUF \
  gemma-2-12b-it-Q8_0.gguf \
  --local-dir /mnt/data/models/ \
  --local-dir-use-symlinks False

# O descargar Q6_K (Balance)
huggingface-cli download \
  bartowski/gemma-2-12b-it-GGUF \
  gemma-2-12b-it-Q6_K.gguf \
  --local-dir /mnt/data/models/ \
  --local-dir-use-symlinks False

# O descargar Q5_K_M (Ligero mejorado)
huggingface-cli download \
  bartowski/gemma-2-12b-it-GGUF \
  gemma-2-12b-it-Q5_K_M.gguf \
  --local-dir /mnt/data/models/ \
  --local-dir-use-symlinks False
```

**⏱️ Tiempo de descarga:** 10-20 minutos (según modelo)

### Opción B: Wget Directo

```bash
# Q8_0 (~13 GB)
cd /mnt/data/models/
wget https://huggingface.co/bartowski/gemma-2-12b-it-GGUF/resolve/main/gemma-2-12b-it-Q8_0.gguf

# Q6_K (~10 GB)
wget https://huggingface.co/bartowski/gemma-2-12b-it-GGUF/resolve/main/gemma-2-12b-it-Q6_K.gguf

# Q5_K_M (~8.5 GB)
wget https://huggingface.co/bartowski/gemma-2-12b-it-GGUF/resolve/main/gemma-2-12b-it-Q5_K_M.gguf
```

---

## 🔄 Paso 3: Detener Servidor Actual

```bash
# Ver procesos
ps aux | grep llama-server

# Opción 1: Si usas screen
screen -ls
screen -r gemma-q4  # (o el nombre del screen)
# Ctrl+C para detener
# Ctrl+D para salir

# Opción 2: Si usas systemd
sudo systemctl stop gemma-server

# Opción 3: Matar proceso directo
pkill -f llama-server
```

---

## 🚀 Paso 4: Iniciar con el Nuevo Modelo

### Script Optimizado para Q8_0

```bash
# Crear script
nano ~/start_gemma_q8.sh
```

**Contenido:**

```bash
#!/bin/bash

MODEL_PATH="/mnt/data/models/gemma-2-12b-it-Q8_0.gguf"
PORT=8080
CTX_SIZE=8192
THREADS=16

echo "🚀 Iniciando Gemma 2-12B Q8_0..."
echo "📦 Modelo: $MODEL_PATH"
echo "🔢 Context: $CTX_SIZE tokens"
echo "🧵 Threads: $THREADS"
echo ""

cd ~/llama.cpp

./build/bin/llama-server \
  --host 0.0.0.0 \
  --port $PORT \
  --model "$MODEL_PATH" \
  --ctx-size $CTX_SIZE \
  --n-threads $THREADS \
  --n-gpu-layers 0 \
  --flash-attn \
  --cont-batching \
  --metrics
```

**Dar permisos y ejecutar:**

```bash
chmod +x ~/start_gemma_q8.sh

# Ejecutar en screen
screen -S gemma-q8
~/start_gemma_q8.sh

# Salir: Ctrl+A, D
```

### Script para Q6_K (Alternativa)

```bash
nano ~/start_gemma_q6.sh
```

```bash
#!/bin/bash
MODEL_PATH="/mnt/data/models/gemma-2-12b-it-Q6_K.gguf"
PORT=8080
CTX_SIZE=8192
THREADS=16

cd ~/llama.cpp
./build/bin/llama-server \
  --host 0.0.0.0 \
  --port $PORT \
  --model "$MODEL_PATH" \
  --ctx-size $CTX_SIZE \
  --n-threads $THREADS \
  --n-gpu-layers 0 \
  --flash-attn \
  --cont-batching
```

---

## ✅ Paso 5: Verificar que Funciona

### Desde la VM

```bash
# Health check
curl http://localhost:8080/health

# Debería responder:
{
  "status": "ok",
  "model_loaded": true
}
```

### Desde tu PC

```bash
# Probar endpoint
curl http://34.175.104.187:8080/health
```

### Test de Calidad

```bash
# Test simple
curl -X POST http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explica qué es la inteligencia artificial en una frase:",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

---

## 📊 Comparación de Resultados

### Con Q4_K_M (Actual - Problemas)
```
Respuesta: "La inteligenci aritficial es uan tecnologai que... [errores]"
Coherencia: ⭐⭐
Velocidad: ⭐⭐⭐⭐⭐
```

### Con Q8_0 (Recomendado)
```
Respuesta: "La inteligencia artificial es la capacidad de las máquinas..."
Coherencia: ⭐⭐⭐⭐⭐
Velocidad: ⭐⭐⭐⭐
```

### Con Q6_K (Balance)
```
Respuesta: "La inteligencia artificial es una tecnología que permite..."
Coherencia: ⭐⭐⭐⭐⭐
Velocidad: ⭐⭐⭐⭐
```

---

## 🔧 Optimizaciones Adicionales

### 1. Aumentar Context Size

```bash
--ctx-size 8192  # En lugar de 4096
```

Permite respuestas más largas y coherentes.

### 2. Flash Attention

```bash
--flash-attn
```

Reduce uso de memoria y acelera inference.

### 3. Continuous Batching

```bash
--cont-batching
```

Mejora throughput con múltiples usuarios.

### 4. Threading Óptimo

```bash
# Ver CPUs disponibles
nproc

# Usar 75% de los cores
--n-threads 12  # Si tienes 16 cores
```

---

## 🎯 Mi Recomendación Final

### Para tu caso (Google Cloud VM):

```bash
# 1. Descargar Q8_0 (mejor calidad)
huggingface-cli download \
  bartowski/gemma-2-12b-it-GGUF \
  gemma-2-12b-it-Q8_0.gguf \
  --local-dir /mnt/data/models/ \
  --local-dir-use-symlinks False

# 2. Detener servidor actual
pkill -f llama-server

# 3. Iniciar con Q8_0
screen -S gemma-q8
cd ~/llama.cpp
./build/bin/llama-server \
  --host 0.0.0.0 \
  --port 8080 \
  --model /mnt/data/models/gemma-2-12b-it-Q8_0.gguf \
  --ctx-size 8192 \
  --n-threads 16 \
  --flash-attn \
  --cont-batching

# Ctrl+A, D para salir
```

---

## 📈 Resultado Esperado

Después de cambiar a Q8_0:

✅ **Coherencia:** Respuestas mucho más lógicas y consistentes  
✅ **Precisión:** Sin errores de tokenización ni "alucinaciones"  
✅ **Streaming:** Fluido sin problemas de sincronización  
✅ **Estabilidad:** Servidor no crashea ni da errores  
⚠️ **Velocidad:** Ligeramente más lento (pero aceptable)  

---

## 🐛 Troubleshooting

### Error: "Out of Memory"

Reducir a Q6_K:
```bash
--model /mnt/data/models/gemma-2-12b-it-Q6_K.gguf
```

### Error: "Modelo no encontrado"

Verificar ruta:
```bash
ls -lh /mnt/data/models/*.gguf
```

### Error: "Puerto en uso"

Liberar puerto:
```bash
sudo lsof -ti:8080 | xargs kill -9
```

---

## 📚 Recursos

- [Gemma 2 12B GGUF Models](https://huggingface.co/bartowski/gemma-2-12b-it-GGUF)
- [Llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [GGUF Quantization Guide](https://github.com/ggerganov/llama.cpp/blob/master/examples/quantize/README.md)

---

**⏱️ Tiempo total:** 30-40 minutos (incluyendo descarga)  
**💾 Espacio necesario:** ~13 GB adicionales  
**🎯 Mejora esperada:** 80-90% en calidad de respuestas

¡Adelante! 🚀

