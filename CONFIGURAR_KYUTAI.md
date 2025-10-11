# 🎙️ Configurar Kyutai TTS (Delayed Streams Modeling)

## ¿Qué es Kyutai TTS?

**Kyutai TTS** es un sistema de síntesis de voz de última generación desarrollado por Kyutai Labs que usa **Delayed Streams Modeling (DSM)**. Es completamente **open-source** y **gratuito**, sin costos de API.

### Ventajas de Kyutai TTS

| Característica | Kyutai DSM | Google Chirp 3 |
|----------------|------------|----------------|
| **Costo** | ✅ Gratuito | ❌ $16/millón chars |
| **Latencia** | ✅ Streaming | ⚠️ Batch |
| **Calidad** | ✅ Muy natural | ✅ Muy natural |
| **Privacidad** | ✅ Auto-hospedado | ❌ Cloud |
| **Open Source** | ✅ Sí | ❌ No |
| **Multilingüe** | ✅ Español, Inglés | ✅ Muchos idiomas |
| **Streaming** | ✅ Sí (real-time) | ❌ No |

---

## 🚀 Opción 1: Deploy en Vercel (Recomendado para Producción)

### Limitaciones de Vercel

⚠️ **IMPORTANTE**: Vercel tiene limitaciones para modelos grandes:

- **Tamaño máximo**: 50 MB por función serverless
- **Memoria**: 1024 MB máximo
- **Tiempo ejecución**: 10 segundos (hobby), 60s (pro)

Kyutai TTS requiere ~1-2.6 GB de modelo, por lo que **no funcionará bien en Vercel para modelos completos**.

### Alternativa: Modelo Lightweight

Si quieres usar Vercel, necesitas:

1. Un modelo TTS más pequeño (< 50 MB)
2. O usar un servidor externo para el modelo

```bash
# NO funciona en Vercel (modelo muy grande)
pip install moshi

# Alternativa: usar un servidor externo
# Ver Opción 2 o Opción 3
```

---

## 🐳 Opción 2: Deploy en tu VM de Google Cloud (Recomendado)

Ya tienes una VM con el modelo Gemma. Puedes agregar Kyutai TTS allí mismo.

### Paso 1: Conectarse a tu VM

```bash
# Desde tu máquina local
gcloud compute ssh capibara6-gemma --zone=us-central1-a
```

### Paso 2: Crear directorio para TTS

```bash
cd ~
mkdir kyutai-tts
cd kyutai-tts
```

### Paso 3: Crear virtualenv e instalar dependencias

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar moshi y dependencias
pip install moshi>=0.2.6
pip install flask torch torchaudio soundfile numpy transformers huggingface-hub
```

### Paso 4: Crear servidor Flask

Crea `tts_server.py`:

```python
"""
Servidor TTS con Kyutai DSM
Puerto: 5001 (para no conflictuar con Gemma en 8080)
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import torch

app = Flask(__name__)
CORS(app)  # Permitir CORS

# Configuración
KYUTAI_CONFIG = {
    'model_repo': 'kyutai/tts-1b-en_es',  # Modelo 1B multilingüe
    'sample_rate': 24000,
    'temperature': 0.7,
    'top_p': 0.9,
}

# Cache del modelo
_model_cache = None

def load_model():
    """Carga el modelo Kyutai TTS"""
    global _model_cache
    
    if _model_cache is not None:
        return _model_cache
    
    print(f"📦 Cargando modelo: {KYUTAI_CONFIG['model_repo']}")
    
    from moshi import models
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = models.load_tts_model(
        hf_repo=KYUTAI_CONFIG['model_repo'],
        device=device
    )
    
    _model_cache = model
    print(f"✅ Modelo cargado en {device}")
    return model

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'model': KYUTAI_CONFIG['model_repo'],
        'device': 'cuda' if torch.cuda.is_available() else 'cpu'
    })

@app.route('/tts', methods=['POST'])
def tts():
    """Endpoint principal de TTS"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'es')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Limitar caracteres
        if len(text) > 3000:
            text = text[:3000]
        
        print(f"🎙️ Sintetizando: {len(text)} chars, lang={language}")
        
        # Cargar modelo
        model = load_model()
        
        # Sintetizar
        audio_output = model.synthesize(
            text=text,
            language=language,
            temperature=KYUTAI_CONFIG['temperature'],
            top_p=KYUTAI_CONFIG['top_p']
        )
        
        # Convertir a WAV en memoria
        import io
        import soundfile as sf
        
        audio_buffer = io.BytesIO()
        sf.write(
            audio_buffer,
            audio_output,
            KYUTAI_CONFIG['sample_rate'],
            format='WAV'
        )
        audio_buffer.seek(0)
        audio_data = audio_buffer.read()
        
        # Base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        result = {
            'audioContent': audio_base64,
            'provider': 'Kyutai DSM TTS',
            'model': KYUTAI_CONFIG['model_repo'],
            'language': language,
            'characters': len(text),
            'sample_rate': KYUTAI_CONFIG['sample_rate'],
            'format': 'wav'
        }
        
        print(f"✅ TTS exitoso: {len(audio_data)} bytes")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'fallback': True
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor Kyutai TTS en puerto 5001...")
    
    # Pre-cargar modelo al iniciar
    load_model()
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False
    )
```

### Paso 5: Crear script de inicio

Crea `start_kyutai.sh`:

```bash
#!/bin/bash
cd ~/kyutai-tts
source venv/bin/activate
python3 tts_server.py
```

```bash
chmod +x start_kyutai.sh
```

### Paso 6: Iniciar servidor en screen

```bash
# Crear sesión de screen
screen -S kyutai-tts

# Dentro de screen, iniciar servidor
./start_kyutai.sh

# Presionar Ctrl+A, luego D para salir sin cerrar

# Ver sesiones activas
screen -ls

# Reconectar más tarde
screen -r kyutai-tts
```

### Paso 7: Configurar firewall

```bash
# Abrir puerto 5001 en Google Cloud
gcloud compute firewall-rules create allow-kyutai-tts \
    --allow tcp:5001 \
    --source-ranges 0.0.0.0/0 \
    --description "Kyutai TTS server"
```

### Paso 8: Actualizar el frontend

En tu archivo `web/tts-integration.js`, actualiza la URL:

```javascript
const TTS_CONFIG = {
    // ...
    apiEndpoint: 'http://YOUR_VM_IP:5001/tts',  // Reemplaza con tu IP
    // ...
};
```

O mejor aún, crea un proxy en Vercel:

**Crea `api/tts-proxy.js`:**

```javascript
export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    try {
        const response = await fetch('http://YOUR_VM_IP:5001/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(req.body)
        });
        
        const data = await response.json();
        res.status(response.status).json(data);
        
    } catch (error) {
        res.status(500).json({
            error: error.message,
            fallback: true
        });
    }
}
```

---

## 🖥️ Opción 3: Run Locally (Desarrollo)

Para desarrollo local:

```bash
# Instalar dependencias
pip install moshi>=0.2.6 flask torch torchaudio soundfile

# Usar el mismo tts_server.py de arriba
python tts_server.py

# En otra terminal, iniciar frontend
cd web
python -m http.server 8000

# Actualizar tts-integration.js:
# apiEndpoint: 'http://localhost:5001/tts'
```

---

## 📊 Modelos Disponibles

| Modelo | Tamaño | Idiomas | Latencia | Uso |
|--------|--------|---------|----------|-----|
| `kyutai/tts-1b-en_es` | 1 GB | EN, ES | ~0.5s | Producción |
| `kyutai/tts-2.6b-en` | 2.6 GB | EN | ~2.5s | Alta calidad |
| `kyutai/tts-lite-en_es` | 300 MB | EN, ES | ~0.3s | Edge devices |

---

## 🔍 Verificar Instalación

### 1. Verificar servidor

```bash
# Health check
curl http://YOUR_VM_IP:5001/health

# Debería devolver:
# {"status": "ok", "model": "kyutai/tts-1b-en_es", "device": "cuda"}
```

### 2. Test de síntesis

```bash
curl -X POST http://YOUR_VM_IP:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola, soy Capibara6 con voz natural de Kyutai", "language": "es"}'
```

Debería devolver JSON con `audioContent` en base64.

---

## 🐛 Troubleshooting

### Error: "CUDA out of memory"

```bash
# Usar modelo más pequeño
# En tts_server.py, cambiar a:
'model_repo': 'kyutai/tts-lite-en_es',  # 300 MB en vez de 1 GB
```

### Error: "Module 'moshi' not found"

```bash
# Reinstalar moshi
pip uninstall moshi
pip install --upgrade moshi>=0.2.6
```

### Error: "Hugging Face token required"

```bash
# Login en Hugging Face
pip install huggingface-hub
huggingface-cli login
# Pegar tu token de https://huggingface.co/settings/tokens
```

---

## 💡 Consejos

### 1. Optimizar rendimiento

```python
# En tts_server.py, agregar cache de audio
from functools import lru_cache

@lru_cache(maxsize=100)
def synthesize_cached(text, language):
    # Tu código de síntesis...
    pass
```

### 2. Streaming (avanzado)

Kyutai soporta streaming real-time. Para implementar:

```python
# Ver ejemplos en:
# https://github.com/kyutai-labs/moshi/tree/main/scripts
```

### 3. Monitoreo

```bash
# Ver logs en tiempo real
screen -r kyutai-tts

# O ver archivo de log
tail -f ~/kyutai-tts/tts.log
```

---

## 🎯 Resultado Final

Una vez configurado, tendrás:

✅ TTS natural y gratuito con Kyutai  
✅ Auto-hospedado en tu propia VM  
✅ Sin costos de API  
✅ Streaming y baja latencia  
✅ Fallback automático a Web Speech API  

---

## 📚 Referencias

- **Kyutai TTS GitHub**: https://github.com/kyutai-labs/moshi
- **Hugging Face Models**: https://huggingface.co/kyutai
- **Documentación DSM**: Próximamente (paper en pre-print)
- **Moshi PyPI**: https://pypi.org/project/moshi/

---

**¡Disfruta de voces naturales sin costos! 🎙️**

