# 🔧 Troubleshooting: Selector de Voz No Aparece

## ✅ Pasos para Activar el Selector de Voz

### 1. Esperar Deploy de Vercel (2 minutos)

El código ya está pusheado. Vercel está deployando ahora.

**Verificar deploy:**
- Ir a: https://vercel.com/dashboard
- Ver que el último deploy esté "Ready"

### 2. Limpiar Caché del Navegador

El problema más común es la caché:

#### Opción A: Recarga Forzada (Recomendado)
```
Ctrl + Shift + R   (Windows/Linux)
Cmd + Shift + R    (Mac)
```

#### Opción B: Limpiar Caché Completa
1. F12 → Application → Storage
2. Click en "Clear site data"
3. Recargar página

#### Opción C: Modo Incógnito
```
Ctrl + Shift + N   (Chrome)
```
Probar en ventana incógnita

### 3. Verificar en Consola (F12)

Deberías ver estos mensajes:

```javascript
✅ Correctos:
🎤 Voice Selector Module cargado
✅ Funciones disponibles: initVoiceSelector, getSelectedVoice, testVoice
🎤 Inicializando selector de voces...
✅ Selector de voces inicializado

❌ Errores:
Failed to load resource: voice-selector.js
Failed to load resource: voice-selector.css
```

### 4. Verificar que los Archivos Existan

En consola del navegador:

```javascript
// Verificar que el módulo se cargó
typeof initVoiceSelector
// Debería mostrar: "function"

// Verificar versión
window.location.href
// Debería incluir: ?v=1.0 en los scripts
```

### 5. Si Aún No Aparece

#### Verificar Ruta de Archivos

Abrir estas URLs directamente:
```
https://www.capibara6.com/voice-selector.js?v=1.0
https://www.capibara6.com/voice-selector.css?v=1.0
```

**Si devuelven 404:** Los archivos no se deployaron correctamente.

**Solución:**
```bash
# En tu PC local
git status
git add web/voice-selector.js web/voice-selector.css
git commit -m "Asegurar que archivos de voz se incluyan en deploy"
git push
```

#### Verificar Orden de Carga

El selector debe cargarse **DESPUÉS** de TTS pero **ANTES** de chat-app.js:

```html
<script src="tts-integration.js?v=8.0"></script>
<script src="voice-selector.js?v=1.0"></script>  ← Aquí
<script src="chat-app.js?v=8.0"></script>
```

---

## 🎯 Ubicación Esperada del Selector

El selector debe aparecer **arriba de los mensajes del chat**:

```
┌────────────────────────────────────┐
│  Capibara6 Chat                    │
├────────────────────────────────────┤
│  🎤 Seleccionar Voz         [▼]    │ ← AQUÍ
├────────────────────────────────────┤
│  [Mensajes del chat]               │
│                                    │
└────────────────────────────────────┘
```

**Si no está ahí:**
1. El JavaScript no se ejecutó
2. O `chat-container` no existe

---

## 🐛 Errores Comunes

### Error 1: "initVoiceSelector is not a function"

**Causa:** El script no se cargó o se cargó en orden incorrecto.

**Solución:**
```javascript
// En consola, verificar:
console.log(typeof initVoiceSelector);
// Debería ser "function"

// Si es "undefined", recargar con Ctrl+Shift+R
```

### Error 2: "Cannot read property 'insertBefore' of null"

**Causa:** El selector intenta insertarse antes de que el DOM esté listo.

**Solución:** Ya está solucionado con el `setTimeout` de 1 segundo en `chat-app.js`.

### Error 3: Panel aparece pero está vacío

**Causa:** No puede cargar voces del servidor.

**Solución:**
1. Verificar que TTS esté corriendo en la VM
2. Ver consola: debe mostrar error de fetch
3. Esperar a que TTS esté activo

### Error 4: CSS no se aplica (botones sin estilo)

**Causa:** `voice-selector.css` no se cargó.

**Solución:**
```javascript
// Verificar en consola:
document.styleSheets
// Buscar: voice-selector.css

// Si no está, forzar recarga: Ctrl+Shift+R
```

---

## ✅ Checklist de Verificación

- [ ] Deploy de Vercel completado (verde)
- [ ] Caché del navegador limpiada (Ctrl+Shift+R)
- [ ] Consola sin errores (F12)
- [ ] `voice-selector.js` y `.css` accesibles
- [ ] `typeof initVoiceSelector === "function"`
- [ ] Panel visible arriba del chat

---

## 🚀 Solución Rápida (90% de los casos)

```bash
# 1. En tu PC: Verificar que todo está pusheado
git status

# 2. Si hay cambios sin commit:
git add web/voice-selector.js web/voice-selector.css web/chat.html
git commit -m "Fix selector de voz"
git push

# 3. Esperar 2 minutos

# 4. En el navegador:
# Ctrl + Shift + R (recarga forzada)
```

---

## 📞 Si Nada Funciona

Ejecuta esto en la consola del navegador y envíame el resultado:

```javascript
console.log({
  voiceSelectorJsLoaded: typeof initVoiceSelector,
  chatContainer: !!document.querySelector('.chat-container'),
  chatMessages: !!document.querySelector('.chat-messages'),
  allScripts: [...document.scripts].map(s => s.src),
  allStyles: [...document.styleSheets].map(s => s.href)
});
```

---

**Última actualización:** 12 Oct 2025  
**Tiempo estimado de solución:** 2-5 minutos

