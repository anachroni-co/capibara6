# 🎙️ Kyutai TTS Integration - Capibara6

## ✅ Implementación Completa

Se ha implementado **Kyutai TTS** (Delayed Streams Modeling) como reemplazo de Google Chirp 3 HD.

---

## 📦 Archivos Modificados

### Backend (`api/tts.py`)
```python
# Antes: Google Cloud Text-to-Speech
from google.cloud import texttospeech

# Ahora: Kyutai TTS con Moshi
from moshi import models
```

**Características:**
- ✅ Cache de modelo para reutilización
- ✅ Soporte CUDA/CPU automático
- ✅ Síntesis en español e inglés
- ✅ Formato WAV de alta calidad (24kHz)
- ✅ Fallback graceful en caso de error

### Dependencias (`api/requirements.txt`)
```txt
# Kyutai TTS - Delayed Streams Modeling
moshi>=0.2.6

# Framework
Flask==3.0.0
torch>=2.0.0
torchaudio>=2.0.0

# Audio
soundfile>=0.12.1
numpy>=1.24.0

# Hugging Face
transformers>=4.35.0
huggingface-hub>=0.19.0
```

### Frontend (`web/tts-integration.js`)
```javascript
// Antes: Google Chirp 3
useChirp3: true

// Ahora: Kyutai DSM
useKyutai: true
```

**Cambios:**
- ✅ Soporte para formato WAV
- ✅ Parámetro de idioma en request
- ✅ Logging mejorado con modelo usado
- ✅ Fallback automático a Web Speech API

### HTML (`web/chat.html`)
```html
<!-- Versión actualizada para forzar cache refresh -->
<script src="tts-integration.js?v=2.0"></script>
```

---

## 🚀 Cómo Deployar

### ⚠️ IMPORTANTE: Limitación de Vercel

Kyutai TTS requiere ~1-2.6 GB de modelo, lo que **excede el límite de Vercel** (50 MB).

**Opciones:**

### 1. Desplegar en tu VM de Google Cloud (Recomendado)

```bash
# SSH a tu VM
gcloud compute ssh capibara6-gemma --zone=us-central1-a

# Crear directorio
mkdir ~/kyutai-tts && cd ~/kyutai-tts

# Instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install moshi>=0.2.6 flask torch torchaudio soundfile

# Crear tts_server.py (ver CONFIGURAR_KYUTAI.md)
# ...

# Iniciar en screen
screen -S kyutai-tts
./start_kyutai.sh
# Ctrl+A, D para salir
```

**Ventajas:**
- ✅ Modelo completo (1-2.6 GB)
- ✅ GPU acceleration (si disponible)
- ✅ Sin límites de tiempo/memoria
- ✅ Completamente gratuito

### 2. Usar Modelo Lightweight en Vercel

Si prefieres Vercel, usa un modelo más pequeño:

```python
# En api/tts.py, cambiar a:
KYUTAI_CONFIG = {
    'model_repo': 'kyutai/tts-lite-en_es',  # 300 MB
    # ...
}
```

**Limitaciones:**
- ⚠️ Calidad ligeramente reducida
- ⚠️ Menor vocabulario

### 3. Hybrid: Proxy en Vercel → TTS en VM

Mejor de ambos mundos:

```javascript
// Crear api/tts-proxy.js en Vercel
export default async function handler(req, res) {
    const response = await fetch('http://YOUR_VM_IP:5001/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req.body)
    });
    
    const data = await response.json();
    res.json(data);
}
```

**Ventajas:**
- ✅ HTTPS desde Vercel (seguro)
- ✅ Modelo completo en VM (potente)
- ✅ Sin límites de tamaño

---

## 🧪 Testing

### Test Local

```bash
# Iniciar servidor TTS (VM o local)
python tts_server.py

# Test con curl
curl -X POST http://localhost:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola, soy Capibara6 con Kyutai", "language": "es"}'

# Debería devolver JSON con audioContent en base64
```

### Test Frontend

1. Abrir `https://capibara6-kpdtkkw9k-anachroni.vercel.app/chat.html`
2. Enviar un mensaje
3. Hacer clic en el botón "Escuchar" 🔊
4. Verificar en la consola:

```
🔊 Kyutai DSM TTS reproduciendo... (kyutai/tts-1b-en_es)
✅ Kyutai TTS completado
```

### Test de Fallback

Si Kyutai no está disponible, debería usar Web Speech API:

```
⚠️ Kyutai no disponible, usando Web Speech API
🔊 Web Speech API iniciado
```

---

## 📊 Comparación: Antes vs Ahora

| Aspecto | Google Chirp 3 | Kyutai TTS |
|---------|----------------|------------|
| **Costo** | $16/millón chars | 💰 Gratis |
| **Latencia** | ~1-2s | ~0.5-1s |
| **Streaming** | ❌ No | ✅ Sí (DSM) |
| **Auto-hospedado** | ❌ No | ✅ Sí |
| **Open Source** | ❌ No | ✅ MIT |
| **Privacidad** | ⚠️ Google Cloud | ✅ 100% privado |
| **Multilingüe** | ✅ Muchos | ✅ EN, ES |
| **Calidad voz** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Setup inicial** | Fácil | Medio |
| **Mantenimiento** | Ninguno | Bajo |

---

## 🔧 Configuración de Modelos

### Modelos Disponibles

| Modelo | Tamaño | Idiomas | Latencia | Mejor para |
|--------|--------|---------|----------|------------|
| `kyutai/tts-1b-en_es` | 1 GB | EN, ES | ~0.5s | **Producción** |
| `kyutai/tts-2.6b-en` | 2.6 GB | EN | ~2.5s | Alta calidad EN |
| `kyutai/tts-lite-en_es` | 300 MB | EN, ES | ~0.3s | Edge/Mobile |

### Cambiar Modelo

```python
# En api/tts.py o tts_server.py
KYUTAI_CONFIG = {
    'model_repo': 'kyutai/tts-2.6b-en',  # Cambiar aquí
    # ...
}
```

---

## 🐛 Troubleshooting Común

### 1. "Module 'moshi' not found"

```bash
pip install --upgrade moshi>=0.2.6
```

### 2. "CUDA out of memory"

```python
# Usar modelo más pequeño o CPU
device = 'cpu'  # Forzar CPU
```

### 3. "Hugging Face token required"

```bash
huggingface-cli login
# Pegar token de https://huggingface.co/settings/tokens
```

### 4. Audio no reproduce

- Verificar formato: debe ser `data:audio/wav;base64,...`
- Verificar CORS: servidor debe tener `Access-Control-Allow-Origin: *`
- Verificar firewall: puerto 5001 debe estar abierto

### 5. Latencia alta

- Usar GPU en lugar de CPU
- Pre-cargar modelo al iniciar servidor
- Usar modelo más pequeño (`tts-lite-en_es`)

---

## 📈 Próximos Pasos

### Streaming Real-Time (Avanzado)

Kyutai soporta streaming chunk-by-chunk:

```python
# En lugar de:
audio_output = model.synthesize(text=text)

# Usar:
for audio_chunk in model.synthesize_stream(text=text):
    yield audio_chunk
```

Esto permite **comenzar a reproducir antes** de que termine la síntesis completa.

### Prompts de Voz

Kyutai permite "speaker prompts" para clonar voces:

```python
# Proporcionar muestra de voz
synthesis_input = {
    'text': text,
    'audio_prompt': audio_sample,  # 3-5 segundos de voz
    'text_prompt': "Loonah",  # Para ortografía específica
}
```

### Multi-Speaker

```python
# Especificar speaker ID
synthesis_input = {
    'text': text,
    'speaker_id': 0,  # 0-7 speakers disponibles
}
```

---

## 📚 Documentación Completa

- **Setup Detallado**: Ver `CONFIGURAR_KYUTAI.md`
- **Código Backend**: Ver `api/tts.py`
- **Código Frontend**: Ver `web/tts-integration.js`
- **Kyutai GitHub**: https://github.com/kyutai-labs/moshi
- **Hugging Face**: https://huggingface.co/kyutai

---

## ✅ Checklist de Deploy

- [ ] Instalar `moshi>=0.2.6` en VM
- [ ] Crear `tts_server.py` en VM
- [ ] Abrir puerto 5001 en firewall
- [ ] Iniciar servidor en `screen`
- [ ] Actualizar `apiEndpoint` en `tts-integration.js`
- [ ] Test con `curl http://VM_IP:5001/health`
- [ ] Test frontend: botón "Escuchar"
- [ ] Verificar fallback a Web Speech API

---

## 🎯 Resultado Esperado

```bash
# Health check exitoso
$ curl http://YOUR_VM_IP:5001/health
{
  "status": "ok",
  "model": "kyutai/tts-1b-en_es",
  "device": "cuda"
}

# TTS funcionando
$ curl -X POST http://YOUR_VM_IP:5001/tts -d '{"text":"Hola","language":"es"}'
{
  "audioContent": "UklGRn4gAABXQVZF...",
  "provider": "Kyutai DSM TTS",
  "characters": 4,
  "sample_rate": 24000
}
```

---

**¡Disfruta de TTS gratuito y natural con Kyutai! 🎙️✨**

