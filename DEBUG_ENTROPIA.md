# 🔍 Debug - Monitor de Entropía

## Paso 1: Verificar que los Scripts Estén Cargados

### Abrir página de test:
```
http://localhost:5500/web/test-entropy-integration.html
```

Deberías ver:
- ✅ calculateEntropy
- ✅ getEntropyClass
- ✅ createEntropyHTML
- ✅ Lucide

Si ves ❌ en alguno, ese script no se cargó correctamente.

---

## Paso 2: Abrir la Consola del Navegador

1. **Abre el chat:** http://localhost:5500/web/chat.html
2. **Presiona F12** para abrir DevTools
3. **Ve a la pestaña "Console"**

### ¿Qué deberías ver?

```
🎯 Monitor de entropía cargado
🎯 Inicializando monitor de entropía...
✅ Contenedor de mensajes encontrado
✅ Monitor de entropía activado
```

### Si NO ves esos mensajes:

**Problema:** Los scripts no se están cargando.

**Solución:**
1. Verifica que los archivos existan:
   - `web/entropy-monitor.js`
   - `web/entropy-auto-inject.js`

2. Verifica en la pestaña "Network" de DevTools que los scripts se carguen sin errores (código 200).

---

## Paso 3: Enviar un Mensaje de Prueba

1. En el chat, escribe: **"Hola"**
2. Envía el mensaje
3. Espera la respuesta

### En la consola deberías ver:

```
📊 Entropía calculada: 1.35 H
✅ Entropía agregada correctamente
```

### Si ves estos mensajes en la consola pero NO ves el indicador en el chat:

**Problema:** El HTML se está generando pero no se está insertando correctamente.

---

## Paso 4: Inspeccionar el HTML del Mensaje

1. **Click derecho** en un mensaje del asistente
2. **Inspeccionar elemento**
3. Busca la clase `.message-stats`

### Estructura esperada:

```html
<div class="message-stats">
    <span class="stat-item">
        <i data-lucide="clock"></i>
        2.3s
    </span>
    <span class="stat-item">
        <i data-lucide="zap"></i>
        45 gen
    </span>
    <!-- AQUÍ DEBERÍA ESTAR -->
    <span class="stat-item stat-entropy entropy-normal">
        <i data-lucide="activity"></i>
        1.35 H
    </span>
    <span class="stat-item">
        <i data-lucide="gauge"></i>
        capibara6
    </span>
</div>
```

---

## Paso 5: Errores Comunes

### ❌ Error: "Cannot read property 'querySelector' of null"

**Causa:** El selector `.message-stats` no existe o tiene otro nombre.

**Solución:** Inspecciona el HTML real del mensaje y verifica el nombre de la clase.

### ❌ Error: "calculateEntropy is not defined"

**Causa:** El script `entropy-monitor.js` no se cargó antes de `entropy-auto-inject.js`.

**Solución:** Verifica el orden de los scripts en `chat.html`:
```html
<script src="entropy-monitor.js"></script>  <!-- PRIMERO -->
<script src="entropy-auto-inject.js"></script>  <!-- DESPUÉS -->
```

### ❌ Error: "Contenedor de mensajes no encontrado"

**Causa:** El ID del contenedor de mensajes no es `messages`.

**Solución:** Busca en `chat.html` cuál es el ID real del contenedor de mensajes.

---

## Paso 6: Solución Manual Temporal

Si el sistema automático no funciona, puedes agregar la entropía manualmente:

### Abrir la consola del navegador y ejecutar:

```javascript
// Calcular entropía de un mensaje
const text = "Hola, ¿cómo estás?";
const entropy = calculateEntropy(text, 0.6);
console.log(`Entropía: ${entropy.toFixed(2)} H`);

// Crear HTML
const html = createEntropyHTML(entropy);
console.log(html);
```

---

## Paso 7: Verificar Archivos

### Ejecuta en la terminal:

```cmd
dir web\entropy*.js
```

Deberías ver:
- `entropy-monitor.js`
- `entropy-auto-inject.js`

---

## 🆘 Si Nada Funciona

### Opción 1: Reinstalar Scripts

```cmd
# Desde la raíz del proyecto
cd web
# Verificar que existan
type entropy-monitor.js
type entropy-auto-inject.js
```

### Opción 2: Verificar en chat.html

Abre `web/chat.html` y verifica que estas líneas estén presentes:

```html
<script src="entropy-monitor.js"></script>
<script src="entropy-auto-inject.js"></script>
```

### Opción 3: Caché del Navegador

A veces el navegador cachea los archivos antiguos:

1. **Ctrl + Shift + Delete** para limpiar caché
2. O **Ctrl + Shift + R** para recargar forzado

---

## 📋 Checklist de Verificación

- [ ] Los archivos .js existen en web/
- [ ] Los scripts están en chat.html en el orden correcto
- [ ] La consola muestra "Monitor de entropía activado"
- [ ] Los mensajes tienen la clase `.message-stats`
- [ ] No hay errores en la consola del navegador
- [ ] El navegador no está usando caché antiguo

---

**Siguiente paso:** Comparte el output de la consola del navegador (F12 → Console) para ver qué está pasando.
