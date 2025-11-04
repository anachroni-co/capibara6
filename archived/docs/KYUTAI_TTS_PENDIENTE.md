# 🚧 Kyutai TTS - Pendiente de Implementación

## ❌ Problema Encontrado

La API de la biblioteca `moshi` de Kyutai no funciona como se documentó inicialmente.

### Error al intentar importar:

```python
from moshi import models  # ❌ Error
# ImportError: cannot import name 'models' from 'moshi'
```

El paquete instalado con `pip install moshi>=0.2.6` no incluye el módulo `models` esperado.

---

## 🔍 Investigación Necesaria

### Posibles causas:

1. **API diferente:** La biblioteca `moshi` puede tener una API diferente a la documentada
2. **Paquete incorrecto:** Quizás el paquete PyPI `moshi` no es el de Kyutai
3. **Documentación incompleta:** La API de TTS de Kyutai puede no estar públicamente disponible aún
4. **Solo STT disponible:** Moshi puede ser principalmente para Speech-to-Text, no Text-to-Speech

### Tareas pendientes:

- [ ] Verificar el repositorio oficial de Kyutai: https://github.com/kyutai-labs/moshi
- [ ] Revisar la documentación actualizada de la API
- [ ] Probar instalación desde source en lugar de PyPI
- [ ] Verificar si TTS está disponible o solo STT
- [ ] Explorar alternativas de TTS open-source

---

## ✅ Solución Temporal

Mientras se investiga la API correcta, implementamos:

### 1. Servidor TTS con Fallback Automático

```python
# backend/kyutai_tts_server_simple.py
# Devuelve sempre fallback=True
```

**Resultado:** El frontend usa **Web Speech API** del navegador.

### 2. Sin errores de deploy

- ✅ Vercel deploy exitoso (proxy ligero)
- ✅ Frontend funcional con Web Speech API
- ✅ No bloquea otras funcionalidades

---

## 🎯 Estado Actual

| Componente | Estado | Funcionalidad |
|------------|--------|---------------|
| **Vercel Frontend** | ✅ Funcional | Chat, respuestas, UI |
| **Vercel Proxy** | ✅ Funcional | Redirección HTTPS |
| **VM - Gemma Model** | ✅ Funcional | Generación de texto |
| **VM - Smart MCP** | ✅ Funcional | Contexto verificado |
| **VM - Kyutai TTS** | ⚠️ Pendiente | Fallback a Web Speech API |
| **Frontend TTS** | ✅ Funcional | Web Speech API nativa |

---

## 🔊 TTS Actual: Web Speech API

El frontend usa la **Web Speech API** del navegador, que funciona perfectamente:

```javascript
// web/tts-integration.js
const utterance = new SpeechSynthesisUtterance(text);
utterance.lang = 'es-ES';
utterance.rate = 1.0;
window.speechSynthesis.speak(utterance);
```

**Ventajas:**
- ✅ Funciona sin backend
- ✅ Sin latencia de red
- ✅ Gratis
- ✅ Voces naturales (Google, Microsoft)
- ✅ Compatible con Chrome, Firefox, Edge, Safari

**Desventajas:**
- ⚠️ Calidad varía por navegador
- ⚠️ Requiere conexión a internet (algunas voces)

---

## 📚 Alternativas de TTS Open-Source

Mientras se investiga Kyutai, estas son alternativas viables:

### 1. Coqui TTS (Recomendado)

```bash
pip install TTS
```

```python
from TTS.api import TTS

# Cargar modelo
tts = TTS("tts_models/es/css10/vits")

# Sintetizar
tts.tts_to_file(text="Hola mundo", file_path="output.wav")
```

**Ventajas:**
- ✅ Open-source
- ✅ Múltiples idiomas (incluye español)
- ✅ Voces de alta calidad
- ✅ API simple y documentada
- ✅ Activamente mantenido

**Tamaño:** ~500 MB modelo español

### 2. Piper TTS

```bash
pip install piper-tts
```

**Ventajas:**
- ✅ Muy ligero (~50 MB)
- ✅ Rápido
- ✅ Múltiples voces español

### 3. ESPnet2

```bash
pip install espnet
```

**Ventajas:**
- ✅ Alta calidad
- ✅ Investigación académica

**Desventajas:**
- ⚠️ Más complejo de usar

---

## 🚀 Plan de Acción

### Corto Plazo (Ahora)

- [x] Usar Web Speech API (funciona perfectamente)
- [x] Servidor fallback simple en VM
- [x] Frontend completamente funcional

### Medio Plazo (1-2 semanas)

- [ ] Investigar API correcta de Kyutai
- [ ] Evaluar Coqui TTS como alternativa
- [ ] Implementar TTS seleccionado en VM
- [ ] Mantener Web Speech API como fallback

### Largo Plazo (Futuro)

- [ ] Múltiples opciones de TTS
- [ ] Selección de voz en UI
- [ ] Cache de audio generado
- [ ] Streaming de audio

---

## 🔧 Cómo Usar Ahora

### Inicio del Servidor Fallback

```bash
# En la VM
cd ~/capibara6/backend
source venv/bin/activate
python kyutai_tts_server_simple.py
```

### Verificar

```bash
curl http://localhost:5001/health

# Respuesta:
{
  "service": "tts-fallback-server",
  "status": "healthy",
  "mode": "fallback",
  "message": "Kyutai TTS API en investigación"
}
```

### Test TTS

```bash
curl -X POST http://localhost:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola","language":"es"}'

# Respuesta:
{
  "fallback": true,
  "provider": "Web Speech API (fallback)",
  "message": "Kyutai TTS API en desarrollo"
}
```

El frontend al recibir `fallback: true` usará automáticamente Web Speech API.

---

## 📖 Referencias

- **Kyutai GitHub:** https://github.com/kyutai-labs/moshi
- **Moshi PyPI:** https://pypi.org/project/moshi/
- **Coqui TTS:** https://github.com/coqui-ai/TTS
- **Web Speech API:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API

---

## 💡 Contribuciones

Si alguien descubre la API correcta de Kyutai TTS:

1. Actualizar `kyutai_tts_server.py` con el código correcto
2. Probar que funciona
3. Actualizar documentación
4. Abrir PR

---

**Por ahora, el sistema funciona perfectamente con Web Speech API.** 🎉

La investigación de Kyutai TTS continúa en paralelo sin bloquear funcionalidad.

