# ⚠️ INSTRUCCIONES URGENTES - Limpia el Caché YA

## 🎯 El Problema

Tu navegador está mostrando código VIEJO (en caché). El código está actualizado pero el navegador no lo sabe.

---

## ✅ SOLUCIÓN (Sigue estos pasos EXACTAMENTE)

### **Paso 1: Cierra TODAS las pestañas del chat**
Cierra todas las pestañas que tengan `localhost:8000/chat.html` o `localhost:5500`

### **Paso 2: Limpia el caché**

#### **Windows (Chrome/Edge):**

1. Presiona estas 3 teclas al mismo tiempo:
   ```
   Ctrl + Shift + Delete
   ```

2. Se abrirá una ventana. Configura:
   - **Intervalo:** "Última hora"
   - **Marca SOLO:** ☑ "Archivos e imágenes almacenados en caché"
   - **NO marques:** Contraseñas, historial, etc.

3. Clic en: **"Borrar datos"**

4. Espera 2 segundos

### **Paso 3: Abre en Modo Incógnito**

1. Presiona:
   ```
   Ctrl + Shift + N
   ```

2. En la ventana incógnita, abre:
   ```
   http://localhost:8000/chat.html
   ```

3. Presiona `F12` para abrir la consola

4. Busca esta línea:
   ```
   ✓ Rating System: function
   ```

### **Paso 4: Verifica**

En el chat deberías ver:
- ✅ Botón **"Evaluar"** ⭐ (NO "Me gusta")
- ✅ Selector de plantillas arriba del input

---

## 🚨 Si AÚN No Funciona

### **Opción A: Deshabilitar Caché Permanentemente**

1. F12 (abrir DevTools)
2. Pestaña **"Network"**
3. Marca: **☑ "Disable cache"**
4. **DEJA DevTools ABIERTO**
5. Recarga: `Ctrl + R`

### **Opción B: Usar Python Server en Otro Puerto**

Si Live Server tiene caché persistente:

```cmd
# Detener Live Server
# Luego usa Python en puerto diferente:
cd web
python -m http.server 8001
```

Abre: `http://localhost:8001/chat.html`

---

## 📋 Checklist

Después de limpiar caché, verifica:

- [ ] ❌ Cerré TODAS las pestañas del chat
- [ ] ❌ Borré caché (Ctrl + Shift + Delete)
- [ ] ❌ Abrí en modo incógnito (Ctrl + Shift + N)
- [ ] ❌ Abrí http://localhost:8000/chat.html
- [ ] ❌ Presioné F12 y busqué "✓ Rating System: function"
- [ ] ❌ Veo el botón **"Evaluar"** ⭐ (NO "Me gusta")
- [ ] ❌ Veo selector de plantillas arriba del input

---

## 🔍 En la Consola Debes Ver

```
🔍 Verificando módulos cargados...
✓ Lucide: object
✓ Marked: object
✓ Template Profiles: object
✓ Rating System: function      ← ✅ DEBE DECIR "function"
✓ Smart MCP: function
✅ Iconos de Lucide inicializados

📊 Sistema de evaluación detallado cargado
✅ Funciones exportadas: {showRatingModal: 'function', ...}
```

---

## 📸 Comparte Screenshot

Si sigue sin funcionar, comparte screenshot de:

1. **La página del chat** (completa)
2. **La consola (F12)** mostrando los logs de verificación

---

**IMPORTANTE: Usa MODO INCÓGNITO (Ctrl+Shift+N) para evitar el caché completamente.** 🚨

