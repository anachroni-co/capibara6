# 🎭 Clonación de Voz con XTTS v2

## ✨ Características Nuevas

El sistema TTS de Capibara6 ahora incluye:

### 1. **3 Voces Predefinidas**
- 👩 **Sofía**: Voz femenina cálida y profesional
- 👧 **Ana**: Voz femenina joven y amigable  
- 👨 **Carlos**: Voz masculina clara y firme

### 2. **Clonación de Voz Personalizada**
- Sube un audio de 5-10 segundos
- XTTS v2 clona la voz automáticamente
- Usa la voz clonada en el chat

### 3. **Preview de Voces**
- Botón 🔊 en cada voz para probarla
- Frase de demostración en español

---

## 🚀 Cómo Usar

### Seleccionar Voz Predefinida

1. Abrir el panel "🎤 Seleccionar Voz" en el chat
2. Hacer clic en una de las 3 voces predefinidas
3. Opcional: Probar la voz con el botón ▶️
4. La voz seleccionada se usará para todos los botones 🔊

### Clonar una Voz Personalizada

1. **Grabar un audio:**
   - 5-10 segundos de duración (recomendado)
   - Hablar claramente en español
   - Sin ruido de fondo
   - Formato: WAV, MP3, OGG

2. **Subir el audio:**
   - Arrastrar el archivo al área de clonación
   - O hacer clic para seleccionar desde el explorador

3. **Esperar procesamiento:**
   - XTTS v2 extraerá las características de la voz
   - Tarda ~5-10 segundos

4. **Usar la voz clonada:**
   - La voz aparecerá en "Voces Clonadas"
   - Se selecciona automáticamente
   - Probar con el botón ▶️

---

## 🏗️ Arquitectura

### Backend (XTTS v2)

```python
# Voces predefinidas usan speaker embeddings
tts.tts_to_file(
    text=text,
    speaker="Claribel Dervla",  # Sofía
    language="es"
)

# Voces clonadas usan speaker_wav
tts.tts_to_file(
    text=text,
    speaker_wav="path/to/audio.wav",
    language="es"
)
```

### Frontend (Selector de Voces)

```javascript
// Obtener voz seleccionada
const voiceId = getSelectedVoice();

// Sintetizar con esa voz
await speakText("Hola mundo", button, voiceId);
```

### API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/voices` | GET | Lista voces disponibles |
| `/clone` | POST | Clona voz desde audio |
| `/tts` | POST | Síntesis con voz específica |
| `/test-voice` | POST | Prueba una voz |

---

## 📋 Voces Predefinidas (Speakers de XTTS v2)

### Femeninas

1. **Sofía** → `Claribel Dervla`
   - Tono: Profesional y cálido
   - Edad: Adulta
   - Ideal para: Explicaciones técnicas, tutoriales

2. **Ana** → `Daisy Studious`
   - Tono: Joven y amigable
   - Edad: Joven adulta
   - Ideal para: Conversación casual, historias

### Masculinas

3. **Carlos** → `Gilberto Mathias`
   - Tono: Clara y firme
   - Edad: Adulto
   - Ideal para: Narración, presentaciones

---

## 🔧 Configuración del Servidor

### Iniciar TTS con Clonación

```bash
# Conectar a VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Detener TTS anterior (si existe)
screen -r coqui-tts
# Ctrl+C → Ctrl+D

# Iniciar nuevo servidor con clonación
cd ~/capibara6/backend
screen -S coqui-xtts
./start_coqui_tts_py311.sh

# Salir: Ctrl+A, D
```

### Verificar que Funciona

```bash
# Health check
curl http://localhost:5002/health

# Debe mostrar:
{
  "status": "healthy",
  "model": "xtts_v2",
  "features": ["voice_cloning", "multilingual", "custom_voices"],
  "predefined_voices": 3
}
```

### Probar Endpoint de Voces

```bash
curl http://localhost:5002/voices

# Debe mostrar:
{
  "status": "success",
  "voices": {
    "predefined": {
      "sofia": {...},
      "ana": {...},
      "carlos": {...}
    },
    "custom": {}
  }
}
```

---

## 🌐 Configuración en Vercel

### Variables de Entorno

Ya configuradas, no es necesario cambiar:

```
KYUTAI_TTS_URL=http://34.175.104.187:5002/tts
```

### Nuevos Endpoints Proxy

Agregados automáticamente:

- `/api/tts-voices` → Lista voces
- `/api/tts-clone` → Clona voces (solo en desarrollo local)

**⚠️ Nota:** La clonación de voz en producción requiere conexión directa al servidor TTS debido a limitaciones de Vercel con `multipart/form-data`.

---

## 📱 Uso en el Frontend

### Interfaz

```
┌─────────────────────────────────────────┐
│ 🎤 Seleccionar Voz              [▼]     │
├─────────────────────────────────────────┤
│ VOCES PREDEFINIDAS                      │
│ ○ 👩 Sofía - Profesional         [▶️]   │
│ ● 👧 Ana - Amigable              [▶️]   │
│ ○ 👨 Carlos - Clara              [▶️]   │
│                                         │
│ 🎭 CLONAR VOZ PERSONALIZADA             │
│ ┌──────────────────────────────────┐    │
│ │  📤 Arrastra audio o haz clic    │    │
│ │  WAV, MP3 (5-10 seg recomendado) │    │
│ └──────────────────────────────────┘    │
│                                         │
│ VOCES CLONADAS                          │
│ ○ 🎭 Mi Voz Personalizada        [▶️]   │
└─────────────────────────────────────────┘
```

### JavaScript API

```javascript
// Inicializar selector
await initVoiceSelector();

// Obtener voz seleccionada
const voice = getSelectedVoice();  // 'sofia', 'ana', 'carlos', 'custom_1', etc.

// Probar una voz
await testVoice('sofia');

// Sintetizar con voz específica
await speakText('Hola mundo', buttonElement, 'carlos');
```

---

## 🎙️ Consejos para Clonar Voces

### Audio Ideal

✅ **Bueno:**
- 5-10 segundos de duración
- Hablar claramente y naturalmente
- Una sola persona hablando
- Sin música ni ruido de fondo
- Calidad: 16 kHz o superior
- Formato: WAV preferido (MP3 también funciona)

❌ **Evitar:**
- Audio muy corto (<3 seg)
- Múltiples voces
- Ruido de fondo excesivo
- Música de fondo
- Eco o reverberación
- Compresión excesiva

### Ejemplos de Frases para Grabar

```
"Hola, mi nombre es [nombre]. Esta es una muestra de mi voz 
para usar en el asistente de Capibara6. Espero que el resultado 
sea de alta calidad y suene natural."
```

```
"Buenos días. Estoy grabando este audio para crear una voz 
personalizada. La tecnología de síntesis de voz ha avanzado 
mucho en los últimos años."
```

---

## 🔍 Troubleshooting

### La voz clonada no suena bien

**Causas posibles:**
- Audio muy corto (menos de 5 segundos)
- Ruido de fondo
- Mala calidad de grabación
- Múltiples personas hablando

**Solución:**
- Re-grabar con audio más limpio
- Usar al menos 5-10 segundos
- Grabar en ambiente silencioso

### No puedo clonar voz en producción

**Causa:**
Vercel serverless functions no soportan `multipart/form-data` grandes fácilmente.

**Solución:**
1. **En desarrollo:** Usar localhost:5002/clone directamente
2. **En producción:** 
   - Opción A: Contactar al administrador para pre-clonar voces
   - Opción B: Implementar edge function dedicado
   - Opción C: Usar voces predefinidas

### El selector de voces no aparece

**Causa:**
Frontend no cargó correctamente.

**Solución:**
1. Recargar página: Ctrl+Shift+R
2. Verificar consola (F12): debe ver "🎤 Voice Selector Module cargado"
3. Verificar que `voice-selector.js` y `voice-selector.css` estén cargados

---

## 📊 Comparación de Voces

| Característica | Web Speech API | Voces Predefinidas | Voz Clonada |
|----------------|----------------|-------------------|-------------|
| Calidad | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Personalización | ❌ | ✅ (3 opciones) | ✅ (ilimitada) |
| Latencia | <1 seg | 2-3 seg | 2-3 seg |
| Requiere internet | ❌ | ✅ | ✅ |
| Idiomas | Limitados | 16+ | Mismo que audio |
| Setup | Automático | Listo para usar | Requiere audio |

---

## 🎯 Próximos Pasos

1. **Reiniciar TTS en la VM** con el nuevo servidor
2. **Probar voces predefinidas** en el chat
3. **Clonar una voz personalizada** (en desarrollo local)
4. **Ajustar voces** según preferencias

---

## 📚 Referencias

- [Coqui TTS Documentation](https://docs.coqui.ai/)
- [XTTS v2 Paper](https://arxiv.org/abs/2406.04904)
- [Voice Cloning Best Practices](https://docs.coqui.ai/en/latest/tutorial_for_nervous_beginners.html)

---

**Última actualización:** 12 Oct 2025  
**Versión:** Capibara6 v2.1 (con clonación de voz)  
**Backend:** XTTS v2 + Flask  
**Frontend:** voice-selector.js v1.0

