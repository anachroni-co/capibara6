# 🔍 Debug: Mensaje Sin Texto

## 🎯 Problema Reportado

A la tercera o cuarta pregunta aparece "⚠️ Mensaje sin texto" - la respuesta está vacía.

---

## ✅ Logs de Debug Agregados

He agregado logs específicos para rastrear dónde se pierde el texto:

### **1. Contenido Original (antes de filtros)**
```javascript
console.log('📥 Contenido original:', data.content.substring(0, 50) + '...');
```

### **2. Después de Filtros**
```javascript
console.log('🧹 Después de filtros:', cleanContent.length, 'chars');
```

### **3. Contenido Eliminado**
```javascript
console.warn('⚠️ Contenido eliminado por filtros:', data.content.substring(0, 100));
```

### **4. Texto Acumulado Final**
```javascript
console.log('📊 Texto acumulado final:', accumulatedText.length, 'chars');
if (accumulatedText.length === 0) {
    console.error('❌ ERROR: No se acumuló ningún texto');
}
```

---

## 🔧 Filtros Ajustados

### **Problema: Filtros Demasiado Amplios**

**❌ Antes:**
```javascript
.replace(/Responde de forma clara.*/gi, '')  // Elimina TODA la línea
.replace(/Microsoft/g, 'Anachroni s.coop')   // Rompe contextos como "Microsoft Azure"
```

**✅ Ahora:**
```javascript
.replace(/^Responde de forma clara.*/gim, '')  // Solo si EMPIEZA la línea
// .replace(/\bMicrosoft\b/g, ...)  // DESHABILITADO - puede romper contextos válidos
```

### **Cambios Realizados:**

1. **Instrucciones:** Añadido `^` para que solo elimine si **empieza** la línea
2. **Microsoft/OpenAI:** **DESHABILITADOS** temporalmente (pueden aparecer en contextos válidos)
3. **Filtros de nombres:** Usamos `\b` (word boundary) para no romper palabras

---

## 🧪 Cómo Diagnosticar el Problema

### **Paso 1: Recarga y Abre Consola**
```
Ctrl + Shift + R
F12 → Pestaña "Console"
```

### **Paso 2: Haz 3-4 Preguntas**

1. Primera pregunta: "Hola"
2. Segunda pregunta: "¿Qué es Python?"
3. Tercera pregunta: "Explícame Transformer"
4. Cuarta pregunta: (cuando falla)

### **Paso 3: Observa los Logs**

En la respuesta que falla, busca:

```
📥 Contenido original: [texto aquí]...
🧹 Después de filtros: X chars
```

**Si "Después de filtros" = 0:**
→ Los filtros eliminaron todo
→ Comparte el "Contenido original" para ver qué filtro lo eliminó

**Si no aparece "📥 Contenido original":**
→ El modelo no está generando nada
→ Problema con el servidor o parámetros

---

## 📊 Posibles Causas

### **Causa 1: Filtros Demasiado Agresivos**

**Síntoma:**
```
📥 Contenido original: Google Cloud TPU ofrece...
🧹 Después de filtros: 0 chars
⚠️ Contenido eliminado por filtros: Google Cloud TPU...
```

**Solución:**
- Identificar qué filtro lo eliminó
- Deshabilitarlo o hacerlo más específico

---

### **Causa 2: Modelo Genera Solo Basura**

**Síntoma:**
```
📥 Contenido original: \textbackslash höherhöher...
🧹 Después de filtros: 0 chars
⚠️ Contenido eliminado por filtros: \textbackslash höher...
```

**Solución:**
- Ajustar parámetros de la plantilla
- Reducir penalties si son muy altas

---

### **Causa 3: Modelo No Genera Nada**

**Síntoma:**
```
(No aparece "📥 Contenido original")
📊 Texto acumulado final: 0 chars
❌ ERROR: No se acumuló ningún texto
```

**Solución:**
- Verificar conexión con servidor
- Revisar parámetros (n_predict muy bajo, etc.)

---

### **Causa 4: El Historial Confunde al Modelo**

**Síntoma:**
- Primeras 2-3 preguntas funcionan
- A partir de la 4ta falla

**Solución:**
- El contexto acumulado está confundiendo al modelo
- Crear nuevo chat más frecuentemente
- Reducir n_predict

---

## 🔧 Soluciones Aplicadas

### **1. Filtros Más Específicos**

```javascript
// ❌ Antes: Elimina en cualquier parte
.replace(/Responde de forma.*/gi, '')

// ✅ Ahora: Solo si empieza la línea
.replace(/^Responde de forma.*/gim, '')
```

### **2. Filtros de Nombres Deshabilitados**

```javascript
// ❌ Antes: Reemplazaba "Microsoft" siempre
.replace(/Microsoft/g, 'Anachroni s.coop')

// ✅ Ahora: Deshabilitado (comentado)
// .replace(/\bMicrosoft\b/g, 'Anachroni s.coop')
```

**Razón:** Rompía contextos válidos como:
- "Google Cloud TPU..."
- "Microsoft Azure..."
- "OpenAI GPT..."

### **3. Logs de Debug**

```javascript
// Ver contenido antes de filtros
console.log('📥 Contenido original:', data.content);

// Ver contenido después de filtros
console.log('🧹 Después de filtros:', cleanContent.length);

// Alertar si se eliminó todo
if (cleanContent.length === 0) {
    console.warn('⚠️ Contenido eliminado por filtros:', data.content);
}
```

---

## 🚀 Qué Hacer Ahora

1. **Recarga el chat:**
   ```
   Ctrl + Shift + R
   ```

2. **Haz 4 preguntas seguidas:**
   ```
   1. Hola
   2. ¿Qué es Python?
   3. Explícame Transformer
   4. ¿Cómo funciona Mamba?
   ```

3. **Cuando aparezca "⚠️ Mensaje sin texto":**
   
   **Comparte estos logs de la consola:**
   ```
   📥 Contenido original: [...]
   🧹 Después de filtros: X chars
   ⚠️ Contenido eliminado por filtros: [...]
   📊 Texto acumulado final: 0 chars
   ```

4. **Con esos logs podré identificar:**
   - ✅ Qué filtro está eliminando el texto
   - ✅ Si el modelo genera basura o texto válido
   - ✅ Qué filtro deshabilitar/ajustar

---

## 📊 Estado Actual

```
✅ Logs de debug:        4 puntos de tracking
✅ Filtros ajustados:    Más específicos (con ^ y \b)
✅ Microsoft/OpenAI:     Deshabilitados temporalmente
✅ Instrucciones:        Solo si empiezan línea (^)
✅ Listo para debug:     Siguiente vez que falle, tendremos los logs
```

---

## 📝 Próximos Pasos

1. **Prueba 3-4 preguntas**
2. **Cuando falle, comparte los logs**
3. **Identificaré el filtro problemático**
4. **Lo ajustaremos**

---

**Recarga el chat y prueba hacer 4 preguntas. Cuando aparezca "Mensaje sin texto", comparte los logs de la consola.** 🔍

