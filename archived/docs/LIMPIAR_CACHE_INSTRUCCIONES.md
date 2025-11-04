# 🧹 Instrucciones: Limpiar Caché del Navegador

## 🎯 Problema

El navegador está mostrando una versión antigua del código (caché):
- ❌ Muestra "Me gusta" en vez de "Evaluar"
- ❌ No abre el modal de evaluación
- ❌ No se ve el icono de estrella

---

## ✅ Solución: Vaciar Caché Completo

### **Método 1: Vaciar Caché y Recarga Forzada (Recomendado)**

#### **En Chrome/Edge:**

1. **Presiona F12** (abre DevTools)
2. **Haz clic derecho en el botón de recargar** (al lado de la URL)
3. **Selecciona:** "Vaciar caché y recargar de forma forzada"

**Atajo de teclado:**
```
Ctrl + Shift + R  (Windows/Linux)
Cmd + Shift + R   (Mac)
```

---

### **Método 2: Limpiar Caché Manualmente**

#### **En Chrome/Edge:**

1. Presiona: `Ctrl + Shift + Delete`
2. En "Intervalo de tiempo" selecciona: **"Última hora"**
3. Marca: **"Archivos e imágenes almacenados en caché"**
4. Clic en: **"Borrar datos"**
5. Recarga la página: `Ctrl + R`

---

### **Método 3: Modo Incógnito (Prueba Rápida)**

1. Presiona: `Ctrl + Shift + N` (Chrome/Edge)
2. Abre: `http://localhost:8000/chat.html`
3. Si funciona aquí → El problema era el caché

---

### **Método 4: Deshabilitar Caché en DevTools**

1. Presiona `F12` (abre DevTools)
2. Ve a la pestaña **"Network"** (Red)
3. Marca: **"Disable cache"** (Deshabilitar caché)
4. **Mantén DevTools abierto** mientras trabajas
5. Recarga: `Ctrl + R`

---

## 🔍 Verificar que se Actualizó

Después de limpiar caché, abre la consola (F12) y busca:

### **✅ Deberías Ver:**

```
🔍 Verificando módulos cargados...
✓ Lucide: object
✓ Marked: object
✓ Template Profiles: object
✓ Rating System: function      ← ✅ IMPORTANTE
✓ Smart MCP: function
✅ Iconos de Lucide inicializados

📊 Sistema de evaluación detallado cargado
✅ Funciones exportadas: {showRatingModal: 'function', ...}

📋 Sistema de plantillas cargado
🎯 Plantilla activa: balanceado
```

### **❌ Si Ves Errores:**

```
✓ Rating System: undefined     ← ❌ No se cargó
```

**Solución:**
- El archivo `rating-system.js` no se está cargando
- Verifica que exista en `web/rating-system.js`
- Recarga con `Ctrl + Shift + R`

---

## 📋 Checklist de Verificación

Después de limpiar caché:

- [ ] ✅ El botón dice "**Evaluar**" (no "Me gusta")
- [ ] ✅ El icono es una **estrella** ⭐ (no corazón ❤️)
- [ ] ✅ Arriba del input hay un **selector de plantillas**
- [ ] ✅ En consola aparece "✓ Rating System: function"
- [ ] ✅ Al hacer clic en "Evaluar" se abre un **modal**

---

## 🚀 Pasos Completos

### **1. Vaciar Caché:**
```
Ctrl + Shift + Delete
→ Marcar "Archivos e imágenes almacenados en caché"
→ Borrar datos
```

### **2. Cerrar Todas las Pestañas del Chat:**
```
Cerrar todas las pestañas de localhost:8000/chat.html
```

### **3. Abrir Nueva Ventana en Modo Incógnito:**
```
Ctrl + Shift + N
```

### **4. Abrir el Chat:**
```
http://localhost:8000/chat.html
```

### **5. Abrir Consola (F12) y Verificar:**
```
Buscar: "✓ Rating System: function"
```

### **6. Hacer una Pregunta:**
```
¿Qué es Python?
```

### **7. Verificar el Botón:**
```
Debería decir: "Evaluar" ⭐
NO: "Me gusta" ❤️
```

### **8. Hacer Clic en "Evaluar":**
```
Debería abrir modal con 6 criterios
```

---

## 🔧 Si Aún No Funciona

### **Opción 1: Verificar Archivos**

En consola (F12):
```javascript
// Verificar que rating-system.js se cargó
console.log(window.showRatingModal);  // Debería mostrar: ƒ showRatingModal()

// Si es undefined:
// El archivo no se cargó o tiene errores
```

### **Opción 2: Ver Errores de Red**

1. F12 → Pestaña "**Network**" (Red)
2. Recarga la página
3. Busca archivos con estado **404** o **error**
4. Si `rating-system.js` está en rojo → no se encuentra el archivo

### **Opción 3: Ver Errores de JavaScript**

1. F12 → Pestaña "**Console**"
2. Busca mensajes en **rojo**
3. Si hay errores de sintaxis en `rating-system.js` → copiar y pegar aquí

---

## 📊 Estado de los Archivos

```
✅ chat-app.js:          Botón cambiado a "Evaluar" ⭐
✅ rating-system.js:     Sistema completo implementado
✅ chat.html:            Script incluido con ?v=2.0
✅ chat.css:             Estilos del modal agregados
✅ Versión:              2.0 (fuerza recarga de caché)
```

---

## 🚨 IMPORTANTE

Debes hacer una **recarga completa sin caché**:

```
Ctrl + Shift + Delete → Borrar caché
Ctrl + Shift + R → Recarga forzada
```

O usa **modo incógnito**:
```
Ctrl + Shift + N
```

---

**Después de limpiar caché, comparte qué ves en la consola al cargar la página (especialmente la línea "✓ Rating System:")** 🔍

