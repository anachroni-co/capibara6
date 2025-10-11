# 🎙️ Coqui TTS - Implementación para Capibara6

## ✨ Por qué Coqui TTS

| Característica | Coqui TTS | Web Speech API | Kyutai |
|----------------|-----------|----------------|--------|
| **Calidad en español** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⚠️ No disponible |
| **Open Source** | ✅ Sí | ❌ No | ✅ Sí |
| **Control total** | ✅ Sí | ❌ No | ✅ Sí |
| **Clonación de voz** | ✅ Sí | ❌ No | ✅ Sí |
| **Sin costos** | ✅ Gratis | ✅ Gratis | ✅ Gratis |
| **Latencia** | ~0.5-2s | ~0s | N/A |
| **Funciona offline** | ✅ Sí | ❌ No | ✅ Sí |

---

## 🚀 Instalación en VM

### Paso 1: Copiar archivos

**Desde tu PC:**

```bash
# Copiar servidor Coqui
gcloud compute scp backend/coqui_tts_server.py gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b

# Copiar script de inicio
gcloud compute scp backend/start_coqui_tts.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b
```

### Paso 2: Conectar a la VM

```bash
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

### Paso 3: Instalar y ejecutar

```bash
cd ~/capibara6/backend

# Dar permisos
chmod +x start_coqui_tts.sh

# Iniciar servidor (en screen para que persista)
screen -S coqui-tts
./start_coqui_tts.sh

# La PRIMERA vez tardará ~5-10 minutos:
# - Instala Coqui TTS (~200 MB)
# - Descarga modelo español (~100 MB)
# - Carga el modelo en memoria

# Ctrl+A, D para salir del screen
```

---

## 📊 Modelos Disponibles

### Modelo por defecto: `tts_models/es/css10/vits`

**Características:**
- ✅ Español de España
- ✅ Alta calidad natural
- ✅ Basado en VITS (neural)
- ✅ Tamaño: ~100 MB
- ✅ Rápido (~0.5-1s por frase)

### Otros modelos español:

```python
# En coqui_tts_server.py, cambiar model_name:

# 1. Multihablante (mejor calidad, más lento)
'tts_models/multilingual/multi-dataset/xtts_v2'

# 2. FastSpeech2 (más rápido, menos calidad)
'tts_models/es/mai/tacotron2-DDC'

# 3. VITS CSS10 (recomendado - balance perfecto)
'tts_models/es/css10/vits'  # ← Actual
```

---

## 🔧 Configuración Avanzada

### Ajustar velocidad

```python
# En coqui_tts_server.py
COQUI_CONFIG = {
    'speed': 1.2,  # Más rápido (1.0 = normal, 0.8 = más lento)
}
```

### Usar XTTS v2 (clonación de voz)

```python
# Modelo multilingüe con clonación
COQUI_CONFIG = {
    'model_name': 'tts_models/multilingual/multi-dataset/xtts_v2',
    'speaker_wav': '/path/to/voice/sample.wav',  # 3-10 segundos de voz
}

# En synthesize_audio():
tts.tts_to_file(
    text=text,
    file_path=tmp_path,
    speaker_wav=COQUI_CONFIG['speaker_wav'],  # Clonar esta voz
    language='es'
)
```

---

## 🎯 Testing

### 1. Health check

```bash
# Desde la VM
curl http://localhost:5001/health

# Respuesta esperada:
{
  "service": "coqui-tts",
  "status": "healthy",
  "model": "tts_models/es/css10/vits",
  "model_loaded": true,
  "provider": "Coqui TTS (VITS)"
}
```

### 2. Test de síntesis

```bash
curl -X POST http://localhost:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola, soy Capibara6 con voz natural de Coqui TTS","language":"es"}'

# Respuesta: JSON con audioContent en base64
```

### 3. Test desde tu PC

```bash
# Obtener IP de la VM
VM_IP=$(gcloud compute instances describe gemma-3-12b --zone=europe-southwest1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

# Test directo
curl http://$VM_IP:5001/health
```

---

## 🌐 Configurar Vercel

### Actualizar variable de entorno

Ve a: https://vercel.com/tu-proyecto → Settings → Environment Variables

```
Name:  KYUTAI_TTS_URL
Value: http://TU_IP_VM:5001/tts
```

(Sí, la variable se llama KYUTAI_TTS_URL pero ahora apunta a Coqui - funciona igual)

### Re-deploy

El proxy JavaScript (`api/tts.js`) funciona igual con Coqui que con cualquier otro backend TTS.

---

## 📈 Rendimiento

### Métricas esperadas:

| Métrica | CPU | GPU (T4) | GPU (A100) |
|---------|-----|----------|------------|
| **Primera carga** | ~60s | ~30s | ~10s |
| **Síntesis (100 chars)** | ~2s | ~0.5s | ~0.3s |
| **Síntesis (500 chars)** | ~8s | ~1.5s | ~0.8s |
| **Memoria RAM** | ~2 GB | ~3 GB | ~3 GB |
| **Memoria GPU** | N/A | ~2 GB | ~2 GB |

### Optimización:

```python
# Para GPU (si disponible):
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'
tts = TTS(model_name='...').to(device)

# Para CPU (reduce threads para menos RAM):
import torch
torch.set_num_threads(2)
```

---

## 🔊 Calidad de Audio

### Características del audio generado:

- **Sample rate:** 22050 Hz
- **Formato:** WAV (sin compresión)
- **Canales:** Mono
- **Bitrate:** ~350 kbps
- **Tamaño:** ~200-500 KB por frase

### Comparación de calidad:

```
Texto: "Hola, soy Capibara6, tu asistente de IA"

Web Speech API (Chrome):  ⭐⭐⭐    (robótico)
Coqui VITS:               ⭐⭐⭐⭐   (natural)
Coqui XTTS v2:            ⭐⭐⭐⭐⭐ (muy natural)
Google Chirp 3 HD:        ⭐⭐⭐⭐⭐ (muy natural, $16/millón chars)
```

---

## 🐛 Troubleshooting

### Error: "TTS not found"

```bash
cd ~/capibara6/backend
source venv/bin/activate
pip install TTS
```

### Error: "No module named 'torch'"

Coqui TTS instala automáticamente PyTorch. Si falla:

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Error: "Model download failed"

```bash
# Descargar modelo manualmente
python -c "from TTS.api import TTS; TTS('tts_models/es/css10/vits')"
```

### Servidor lento en CPU

```python
# Usar modelo más ligero
COQUI_CONFIG = {
    'model_name': 'tts_models/es/mai/tacotron2-DDC',  # Más rápido
}
```

### Audio entrecortado

```python
# Aumentar sample rate
COQUI_CONFIG = {
    'sample_rate': 44100,  # Mejor calidad (por defecto: 22050)
}
```

---

## 📊 Comparación: Coqui vs Otros

### vs Web Speech API

| Aspecto | Coqui TTS | Web Speech API |
|---------|-----------|----------------|
| Control | ✅ Total | ❌ Ninguno |
| Offline | ✅ Sí | ❌ No |
| Calidad | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Setup | Medio | Fácil |
| Latencia | ~1s | ~0s |

### vs Google Chirp 3 HD

| Aspecto | Coqui TTS | Google Chirp 3 |
|---------|-----------|----------------|
| Costo | ✅ $0 | ❌ $16/millón |
| Privacidad | ✅ 100% privado | ⚠️ Google Cloud |
| Clonación voz | ✅ Sí | ❌ No |
| Calidad | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### vs Kyutai/Moshi

| Aspecto | Coqui TTS | Kyutai/Moshi |
|---------|-----------|--------------|
| API | ✅ Documentada | ⚠️ No disponible |
| Funciona | ✅ Sí | ❌ No |
| Español | ✅ Excelente | ⚠️ No probado |

---

## 🎉 Resultado Final

Una vez configurado tendrás:

```
Usuario
  ↓ HTTPS
Vercel (proxy JavaScript ~2 KB)
  ↓ HTTP
VM Google Cloud
  ├─ Gemma Model     :8080
  ├─ Smart MCP       :5003
  └─ Coqui TTS       :5001  ← ✨ Nuevo
```

**Ventajas finales:**
- ✅ Voz natural en español de alta calidad
- ✅ Sin costos de API
- ✅ Control total (velocidad, tono, etc.)
- ✅ Posibilidad de clonar voces
- ✅ Funciona offline
- ✅ Open source y extensible

---

## 📚 Referencias

- **Coqui TTS GitHub:** https://github.com/coqui-ai/TTS
- **Documentación:** https://docs.coqui.ai/
- **Modelos disponibles:** https://github.com/coqui-ai/TTS#released-models
- **Paper VITS:** https://arxiv.org/abs/2106.06103
- **Paper XTTS:** https://arxiv.org/abs/2306.15694

---

**¡Listo para implementar! Ejecuta el script de inicio y disfruta de voces naturales.** 🎙️✨

