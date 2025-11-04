# 🔊 Opciones de TTS para Capibara6

## 📊 Comparativa Completa

| Opción | Calidad | Latencia | Setup | Costo | Estado |
|--------|---------|----------|-------|-------|--------|
| **Coqui TTS** | ⭐⭐⭐⭐⭐ | ~1s | Medio | Gratis | ✅ **RECOMENDADO** |
| Web Speech API | ⭐⭐⭐ | ~0s | Fácil | Gratis | ✅ Funciona |
| Google Chirp 3 | ⭐⭐⭐⭐⭐ | ~1s | Fácil | $16/millón | ⚠️ Requiere pago |
| Kyutai/Moshi | ❓ | ❓ | Difícil | Gratis | ❌ API no disponible |

---

## 🥇 Opción 1: Coqui TTS (RECOMENDADA)

### Por qué es la mejor:

✅ **Calidad excepcional en español**  
✅ **Open source y gratuito**  
✅ **Control total** (velocidad, tono, clonación de voz)  
✅ **Funciona offline**  
✅ **Sin límites de uso**  

### Implementación:

```bash
# En la VM
screen -S coqui-tts
cd ~/capibara6/backend
./start_coqui_tts.sh
# Ctrl+A, D
```

**Documentación:** `COQUI_TTS_SETUP.md`

---

## 🥈 Opción 2: Web Speech API (Fallback actual)

### Ventajas:

✅ **Latencia cero** (corre en el navegador)  
✅ **Sin setup** (funciona automáticamente)  
✅ **Gratis**  
✅ **Compatible** con Chrome, Firefox, Edge, Safari  

### Desventajas:

⚠️ Calidad varía por navegador  
⚠️ Requiere internet  
⚠️ Sin control sobre la voz  

### Estado actual:

Ya está **activo** en el frontend. El botón "Escuchar" 🔊 usa Web Speech API si el servidor TTS no responde.

---

## 🥉 Opción 3: Google Chirp 3 HD

### Ventajas:

✅ **Calidad excelente**  
✅ **Fácil setup**  
✅ **Múltiples idiomas**  

### Desventajas:

❌ **Costo:** $16 por millón de caracteres  
❌ **Requiere cuenta GCP**  
❌ **Sin privacidad** (audio procesado en Google Cloud)  

### No recomendado porque:

Coqui TTS ofrece calidad similar **gratis** y con **más control**.

---

## ❌ Opción 4: Kyutai/Moshi (No disponible)

### Estado:

La API de `moshi` para TTS **no está públicamente disponible**. El paquete PyPI solo incluye STT (Speech-to-Text).

**Documentación:** `KYUTAI_TTS_PENDIENTE.md`

---

## 🎯 Recomendación Final

### Para Capibara6:

```
1. Usar Coqui TTS en la VM        ← ✅ MEJOR OPCIÓN
2. Fallback automático a Web Speech API
```

**Razones:**
- Español de alta calidad
- Sin costos
- Control total
- Open source
- Posibilidad de clonar voces en el futuro

---

## 🚀 Cómo Cambiar de TTS

### Actualmente usando: Web Speech API (fallback)

### Cambiar a Coqui TTS:

```bash
# 1. Deploy files
./deploy_services_to_vm.sh

# 2. En la VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# 3. Iniciar Coqui TTS
screen -S coqui-tts
cd ~/capibara6/backend
./start_coqui_tts.sh

# 4. Verificar
curl http://localhost:5001/health

# 5. Configurar en Vercel (si no está)
# Variable: KYUTAI_TTS_URL
# Valor: http://TU_IP_VM:5001/tts
```

**Frontend:** No requiere cambios, ya está preparado para usar cualquier backend TTS.

---

## 📈 Roadmap TTS

### Implementado:

- [x] Web Speech API (fallback)
- [x] Proxy JavaScript ligero en Vercel
- [x] Coqui TTS server con VITS
- [x] Scripts de inicio automatizados
- [x] Documentación completa

### Futuro:

- [ ] Clonación de voz con XTTS v2
- [ ] Múltiples voces seleccionables
- [ ] Control de velocidad desde UI
- [ ] Cache de audio generado
- [ ] Streaming de audio real-time

---

## 🎙️ Modelos de Voz Disponibles

### Con Coqui TTS:

```python
# 1. VITS CSS10 (actual) - Balance perfecto
'tts_models/es/css10/vits'

# 2. XTTS v2 - Clonación de voz
'tts_models/multilingual/multi-dataset/xtts_v2'

# 3. Tacotron2 - Más rápido
'tts_models/es/mai/tacotron2-DDC'
```

Cambiar en: `backend/coqui_tts_server.py` → `COQUI_CONFIG['model_name']`

---

## 📚 Documentación

| Archivo | Contenido |
|---------|-----------|
| `COQUI_TTS_SETUP.md` | Setup completo de Coqui TTS |
| `KYUTAI_TTS_PENDIENTE.md` | Estado de Kyutai (no disponible) |
| `TTS_OPTIONS.md` | Este archivo - comparativa |
| `ERRORES_VERCEL_SOLUCIONADOS.md` | Errores de deploy resueltos |

---

**Recomendación:** Implementa Coqui TTS para obtener la mejor calidad en español. 🎙️✨

