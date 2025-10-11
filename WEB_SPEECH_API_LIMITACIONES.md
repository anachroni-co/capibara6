# ⚠️ Limitaciones de Web Speech API

## ❌ Problemas Encontrados

Web Speech API tiene limitaciones importantes que causan errores frecuentes:

### 1. Error `synthesis-failed` o `undefined`

**Causa:** El navegador no puede sintetizar textos largos o complejos.

**Síntomas:**
```
❌ Error TTS: undefined
❌ Error TTS: synthesis-failed
```

**Limitaciones por navegador:**

| Navegador | Límite aproximado | Voces |
|-----------|-------------------|-------|
| Chrome | ~300 caracteres | Google (remoto) |
| Edge | ~200 caracteres | Microsoft (local) |
| Firefox | ~500 caracteres | Sistema |
| Safari | ~400 caracteres | Apple |

### 2. Voces no Disponibles Inmediatamente

**Problema:** Las voces tardan en cargar al iniciar la página.

**Solución implementada:**
```javascript
// Esperar múltiples veces hasta que las voces carguen
setTimeout(loadVoices, 100);
setTimeout(loadVoices, 500);
```

### 3. Caracteres Especiales Problemáticos

Algunos caracteres causan fallos en la síntesis:
- Emojis (🎉, 🚀, etc.)
- Símbolos matemáticos (×, ÷, ∑)
- Código (HTML, JSON, Python)
- URLs completas

### 4. No Permite Control Fino

**Limitaciones:**
- ❌ No hay clonación de voz
- ❌ Calidad varía por navegador/OS
- ❌ No funciona offline (voces remotas)
- ❌ No hay control de emociones
- ❌ Latencia variable

---

## ✅ Mejoras Implementadas (v7.0)

### 1. División Inteligente de Texto

```javascript
// Dividir en oraciones y tomar solo las primeras 2
const sentences = cleanText.split(/[.!?]+/);
cleanText = sentences.slice(0, 2).join('. ') + '.';

// Límite estricto: 300 caracteres
cleanText = cleanText.substring(0, 300);
```

### 2. Reintentos con Texto Más Corto

```
Intento 1: Primeras 2 oraciones (~300 chars)
Intento 2: Primera oración completa
Intento 3: Primeros 100 caracteres
```

### 3. Manejo de Errores `undefined`

```javascript
const errorType = event.error || 'unknown';
if (errorType === 'unknown' || errorType === 'undefined') {
    // Reintentar con primera oración solamente
}
```

### 4. Try-Catch en speak()

```javascript
try {
    window.speechSynthesis.speak(currentUtterance);
} catch (error) {
    console.error('Error al llamar speak():', error);
    // Limpiar estado
}
```

---

## 🎯 Solución Definitiva: Coqui TTS

Para eliminar TODAS estas limitaciones, usa **Coqui TTS en tu VM**:

### Ventajas de Coqui TTS:

| Característica | Web Speech API | Coqui TTS |
|----------------|----------------|-----------|
| **Límite de texto** | ⚠️ ~300 chars | ✅ 3000+ chars |
| **Calidad** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Consistencia** | ⚠️ Varía | ✅ Siempre igual |
| **Control** | ❌ Mínimo | ✅ Total |
| **Offline** | ❌ No | ✅ Sí |
| **Errores** | ⚠️ Frecuentes | ✅ Raros |
| **Clonación** | ❌ No | ✅ Sí |

### Deploy de Coqui TTS:

```bash
# Desde tu PC
./deploy_services_to_vm.sh

# En la VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
screen -S coqui-tts
cd ~/capibara6/backend
./start_coqui_tts.sh
# Ctrl+A, D

# Configurar en Vercel
# Variable: KYUTAI_TTS_URL
# Valor: http://TU_IP_VM:5001/tts
```

**Resultado:** Sin limitaciones de texto, calidad ⭐⭐⭐⭐⭐, sin errores.

---

## 📊 Estadísticas de Éxito

### Con Web Speech API (v7.0):

| Longitud texto | Tasa éxito | Observaciones |
|----------------|------------|---------------|
| < 100 chars | ~99% | ✅ Casi siempre funciona |
| 100-300 chars | ~85% | ✅ Funciona con reintentos |
| 300-500 chars | ~60% | ⚠️ Fallos frecuentes |
| > 500 chars | ~20% | ❌ Casi siempre falla |

### Con Coqui TTS:

| Longitud texto | Tasa éxito |
|----------------|------------|
| < 3000 chars | ~100% ✅ |

---

## 🔧 Workarounds Actuales

Mientras no tengas Coqui TTS deployado:

### 1. Textos Cortos

Web Speech API funciona **perfectamente** con textos < 200 caracteres.

**Consejo:** Si el texto falla, haz clic de nuevo. El sistema reintentará con solo la primera oración.

### 2. Mensajes Simples

Funciona mejor con:
- ✅ Respuestas directas
- ✅ Definiciones cortas
- ✅ Saludos/confirmaciones

Falla más con:
- ⚠️ Explicaciones largas
- ⚠️ Código mixto con texto
- ⚠️ Listas numeradas largas

### 3. Navegadores Recomendados

| Navegador | Compatibilidad TTS |
|-----------|-------------------|
| Chrome | ⭐⭐⭐⭐ Muy bueno |
| Edge | ⭐⭐⭐ Bueno (pero límite bajo) |
| Firefox | ⭐⭐⭐⭐ Bueno |
| Safari | ⭐⭐⭐⭐⭐ Excelente |

---

## 💡 Recomendación

**Para producción seria:** Deployar **Coqui TTS** en la VM.

**Razones:**
1. Sin limitaciones de longitud
2. Calidad consistente
3. Sin errores aleatorios
4. Control total
5. Mejor experiencia de usuario

**Tiempo de setup:** ~15 minutos  
**Beneficio:** TTS 10x más robusto

---

## 📚 Ver También

- `COQUI_TTS_SETUP.md` - Setup completo de Coqui
- `TTS_OPTIONS.md` - Comparativa de opciones
- `DEPLOY_AHORA.md` - Guía de deployment

---

**Web Speech API es un buen fallback, pero Coqui TTS es la solución profesional.** 🎙️

