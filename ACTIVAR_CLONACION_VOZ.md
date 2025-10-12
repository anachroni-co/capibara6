# ⚡ Activar Clonación de Voz - Guía Rápida

## ✅ ¿Qué se ha agregado?

1. **3 voces predefinidas** (Sofía, Ana, Carlos)
2. **Clonación de voz personalizada** desde audio
3. **Selector visual** en el chat
4. **Preview de voces** antes de usar

---

## 🚀 Paso 1: Reiniciar TTS en la VM (10 min)

### 1.1. Conectar a la VM

```bash
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

### 1.2. Detener TTS Actual

```bash
# Ver screens
screen -ls

# Conectar al screen de TTS (ajustar nombre si es diferente)
screen -r coqui-tts

# Detener: Ctrl+C
# Salir: Ctrl+D
```

### 1.3. Iniciar Nuevo TTS con Clonación

```bash
cd ~/capibara6/backend
screen -S coqui-xtts
./start_coqui_tts_py311.sh
```

**Espera a ver:**
```
🎙️  COQUI TTS SERVER - Capibara6
📦 Modelo: XTTS v2 (Máxima Calidad + Clonación)
✨ Características: Clonación de voz + 3 voces predefinidas
👥 Voces predefinidas: sofia, ana, carlos
✅ Modelo cargado exitosamente
* Running on http://0.0.0.0:5002
```

**Salir del screen:** Presiona `Ctrl+A`, luego `D`

### 1.4. Verificar

```bash
curl http://localhost:5002/health
```

**Debe responder:**
```json
{
  "status": "healthy",
  "model": "xtts_v2",
  "features": ["voice_cloning", "multilingual", "custom_voices"],
  "predefined_voices": 3
}
```

✅ **¡Listo! TTS con clonación activado**

---

## 🎨 Paso 2: Probar en el Chat (2 min)

### 2.1. Abrir el Chat

```
https://www.capibara6.com/chat.html
```

### 2.2. Forzar Recarga

Presiona: **Ctrl+Shift+R** (Windows/Linux) o **Cmd+Shift+R** (Mac)

### 2.3. Buscar el Selector de Voces

Deberías ver un nuevo panel arriba del chat:

```
┌─────────────────────────────────────────┐
│ 🎤 Seleccionar Voz              [▼]     │
└─────────────────────────────────────────┘
```

### 2.4. Abrir el Panel

Haz clic en "🎤 Seleccionar Voz" para expandir.

### 2.5. Probar Voces Predefinidas

1. Verás 3 voces:
   - 👩 **Sofía** (Profesional)
   - 👧 **Ana** (Amigable)
   - 👨 **Carlos** (Clara)

2. Haz clic en el botón ▶️ de cada voz para probarla

3. Selecciona tu favorita (radio button)

### 2.6. Probar en el Chat

1. Escribe: "¿Qué es inteligencia artificial?"
2. Espera la respuesta
3. Haz clic en el botón 🔊 del mensaje
4. **¡Debería sonar con la voz seleccionada!**

---

## 🎭 Paso 3: Clonar tu Propia Voz (Opcional)

### 3.1. Grabar un Audio

**Requisitos:**
- 5-10 segundos de duración
- Hablar claramente en español
- Sin ruido de fondo
- Formato: WAV o MP3

**Ejemplo de texto:**
```
"Hola, mi nombre es [tu nombre]. Esta es una muestra de mi voz 
para usar en el asistente de Capibara6."
```

### 3.2. Subir el Audio

**⚠️ Importante:** La clonación solo funciona en desarrollo local por ahora.

#### Opción A: En Desarrollo Local

1. Asegúrate de que el TTS esté corriendo en localhost:5002
2. Abrir http://localhost/chat.html (o usar tu servidor local)
3. En el selector de voces, ir a "🎭 Clonar Voz Personalizada"
4. Arrastrar el archivo de audio o hacer clic para seleccionar
5. Esperar ~5-10 segundos
6. La voz aparecerá en "Voces Clonadas"

#### Opción B: En Producción

La clonación en producción requiere configuración adicional. Por ahora:
- Usa las 3 voces predefinidas
- O contacta al administrador para pre-clonar voces

### 3.3. Usar la Voz Clonada

1. Seleccionar la voz clonada en el panel
2. Probarla con el botón ▶️
3. Usar en el chat con el botón 🔊

---

## 🔍 Verificación Completa

### Backend (VM)

```bash
# Conectar
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Verificar servicios
cd ~/capibara6/backend
chmod +x verificar_servicios.sh
./verificar_servicios.sh
```

**Debe mostrar:**
```
✓ Gemma 3-12B (puerto 8080)... ACTIVO
✓ Smart MCP (puerto 5010)... ACTIVO
✓ Coqui TTS (puerto 5002)... ACTIVO
```

### Frontend (Consola del Navegador)

Presiona **F12** → Consola

**Debe mostrar:**
```javascript
🎤 Voice Selector Module cargado
✅ Funciones disponibles: initVoiceSelector, getSelectedVoice, testVoice
🎤 Inicializando selector de voces...
📋 Voces disponibles: {predefined: {...}, custom: {...}}
✅ Selector de voces inicializado
```

### Probar Endpoints

Desde tu PC:

```bash
# Voces disponibles
curl https://www.capibara6.com/api/tts-voices

# Debe devolver:
{
  "status": "success",
  "voices": {
    "predefined": {
      "sofia": {...},
      "ana": {...},
      "carlos": {...}
    }
  }
}
```

---

## 🎉 ¡Listo!

Ahora tienes:

- ✅ **3 voces predefinidas** listas para usar
- ✅ **Selector visual** en el chat
- ✅ **Preview de voces** antes de usar
- ✅ **Clonación de voz** (en desarrollo local)

---

## 📊 Comparación de Voces

| Voz | Género | Estilo | Ideal Para |
|-----|--------|--------|-----------|
| Sofía | Femenina | Profesional | Tutoriales, explicaciones técnicas |
| Ana | Femenina | Amigable | Conversación casual, historias |
| Carlos | Masculina | Clara | Narración, presentaciones |

---

## 💡 Tips

### Cambiar Voz en Medio de una Conversación

1. Abrir el selector de voces
2. Elegir otra voz
3. Los siguientes mensajes con 🔊 usarán la nueva voz

### Probar Voces sin Escribir

1. Abrir el selector de voces
2. Hacer clic en ▶️ de cualquier voz
3. Escuchar la frase de demostración

### Grabar Audio de Calidad

✅ **Bueno:**
- Hablar naturalmente
- Ambiente silencioso
- Micrófono cerca (20-30 cm)
- 5-10 segundos

❌ **Evitar:**
- Gritar o susurrar
- Ruido de fondo
- Música
- Audio muy corto (<3 seg)

---

## 🐛 Troubleshooting

### El selector no aparece

1. Recargar: Ctrl+Shift+R
2. Verificar consola (F12)
3. Debe ver: "🎤 Voice Selector Module cargado"

### Las voces no suenan

1. Verificar que TTS esté corriendo en la VM
2. `curl http://localhost:5002/health` (desde la VM)
3. Verificar logs: `screen -r coqui-xtts`

### El audio suena mal

1. Esperar a que termine de cargar (primera vez: ~30 seg)
2. Probar con texto más corto
3. Verificar conexión a internet

---

## 📚 Documentación Completa

Lee `CLONACION_VOZ_README.md` para:
- Arquitectura detallada
- API endpoints
- Consejos avanzados
- Troubleshooting completo

---

**¿Preguntas?** Revisa la documentación o verifica los logs del servidor.

**Última actualización:** 12 Oct 2025  
**Versión:** Capibara6 v2.1 con clonación de voz  
**Tiempo estimado:** 15 minutos

