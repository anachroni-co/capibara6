# 🎯 Sistema de Plantillas - Capibara6

## 📋 ¿Qué es?

Un sistema de **10 plantillas diferentes** con configuraciones únicas para encontrar la mejor combinación de parámetros para Gemma 3-12B.

Cada plantilla tiene diferentes valores de:
- `temperature` (creatividad)
- `top_p` (diversidad)
- `repeat_penalty` (anti-repetición)
- `n_predict` (longitud de respuesta)
- Y más...

---

## 🎨 Las 10 Plantillas

### 1. 🛡️ Conservador
**Descripción:** Muy coherente y predecible, evita riesgos

**Parámetros:**
```javascript
n_predict: 150
temperature: 0.5      // Baja creatividad
top_p: 0.75          // Baja diversidad
repeat_penalty: 1.4   // Moderado
```

**Ideal para:**
- Respuestas precisas y cortas
- Información factual
- Cuando necesitas coherencia máxima

---

### 2. ⚖️ Balanceado (Default)
**Descripción:** Equilibrio entre coherencia y creatividad

**Parámetros:**
```javascript
n_predict: 200
temperature: 0.7      // Balanceado
top_p: 0.9           // Buena diversidad
repeat_penalty: 1.5   // Moderado
```

**Ideal para:**
- Uso general
- Conversaciones normales
- Punto de partida recomendado

---

### 3. 🎨 Creativo
**Descripción:** Más diversidad y originalidad en respuestas

**Parámetros:**
```javascript
n_predict: 250
temperature: 0.85     // Alta creatividad
top_p: 0.95          // Máxima diversidad
repeat_penalty: 1.3   // Suave
```

**Ideal para:**
- Generación de ideas
- Respuestas originales
- Contenido creativo

---

### 4. 🎯 Preciso
**Descripción:** Respuestas cortas, directas y exactas

**Parámetros:**
```javascript
n_predict: 100       // Muy corto
temperature: 0.4     // Muy baja
top_p: 0.7          // Baja diversidad
repeat_penalty: 1.6  // Alto
```

**Ideal para:**
- Preguntas simples
- Respuestas de sí/no
- Datos específicos

---

### 5. 💬 Conversacional
**Descripción:** Natural y amigable, como una conversación

**Parámetros:**
```javascript
n_predict: 180
temperature: 0.75     // Moderado-alto
top_p: 0.92          // Alta diversidad
repeat_penalty: 1.4   // Moderado
```

**Ideal para:**
- Chat casual
- Explicaciones amigables
- Tono relajado

---

### 6. 🔧 Técnico
**Descripción:** Para explicaciones técnicas detalladas

**Parámetros:**
```javascript
n_predict: 300       // Largo
temperature: 0.6     // Moderado-bajo
top_p: 0.88         // Moderado
repeat_penalty: 1.5  // Moderado
```

**Ideal para:**
- Tutoriales de código
- Explicaciones técnicas
- Documentación

---

### 7. ⚡ Conciso
**Descripción:** Máxima brevedad, mínimo de palabras

**Parámetros:**
```javascript
n_predict: 80        // Muy corto
temperature: 0.55    // Baja
top_p: 0.8          // Baja-media
repeat_penalty: 1.7  // Alto
```

**Ideal para:**
- Respuestas rápidas
- Definiciones breves
- Tiempo limitado

---

### 8. 📚 Detallado
**Descripción:** Explicaciones completas y exhaustivas

**Parámetros:**
```javascript
n_predict: 400       // Muy largo
temperature: 0.65    // Moderado
top_p: 0.9          // Alta diversidad
repeat_penalty: 1.4  // Moderado
```

**Ideal para:**
- Tutoriales largos
- Explicaciones complejas
- Aprendizaje profundo

---

### 9. 🧪 Experimental
**Descripción:** Configuración única y diferente

**Parámetros:**
```javascript
n_predict: 220
temperature: 0.8      // Alta
top_p: 0.85          // Moderado-alto
repeat_penalty: 1.2   // Bajo (permite más repetición)
presence_penalty: 0.5 // Alto
```

**Ideal para:**
- Probar comportamientos únicos
- Exploración
- Curiosidad

---

### 10. ✨ Gemma Optimizado
**Descripción:** Basado en pruebas reales con Gemma 3-12B

**Parámetros:**
```javascript
n_predict: 200
temperature: 0.7
top_p: 0.9
repeat_penalty: 1.5
presence_penalty: 0.3
frequency_penalty: 0.3
```

**Ideal para:**
- Configuración probada
- Resultados consistentes
- Uso general con Gemma

---

## 🚀 Cómo Usar

### **Paso 1: Selecciona una Plantilla**

En la parte superior del chat, verás un selector con las 10 plantillas:

```
Plantilla: [⚖️ Balanceado ▼]  [📊]
```

1. Haz clic en el selector
2. Elige una plantilla (ej: "🎯 Preciso")
3. Verás la descripción debajo del selector

---

### **Paso 2: Haz la Misma Pregunta**

Usa la **misma pregunta** para cada plantilla. Por ejemplo:

```
Explícame cómo funciona la arquitectura híbrida Transformer-Mamba
```

---

### **Paso 3: Da "Me Gusta" a las Mejores**

Después de cada respuesta:

- Si te gusta la respuesta → Haz clic en "**Me gusta**" ❤️
- El sistema registrará automáticamente que esa plantilla funciona bien

---

### **Paso 4: Ver Estadísticas**

Haz clic en el botón de estadísticas **[📊]** para ver:

```
🏆 Mejores Plantillas:

#1 🎯 Preciso         👍 5 👎 0
#2 ⚖️ Balanceado      👍 3 👎 1
#3 💬 Conversacional   👍 2 👎 0
```

---

## 🧪 Flujo de Prueba Recomendado

### **Pregunta de Prueba:**
```
Explícame cómo funciona la arquitectura híbrida Transformer-Mamba
```

### **Proceso:**

1. **Selecciona:** 🛡️ Conservador
   - Envía la pregunta
   - Lee la respuesta
   - Si te gusta → Clic en "Me gusta"
   - Crea nuevo chat

2. **Selecciona:** ⚖️ Balanceado
   - Envía la MISMA pregunta
   - Lee la respuesta
   - Si te gusta → Clic en "Me gusta"
   - Crea nuevo chat

3. **Repite para todas las 10 plantillas**

4. **Ve estadísticas** (botón 📊)
   - Revisa cuáles tienen más likes
   - Esas son las mejores para Gemma

---

## 📊 Comparación de Plantillas

| Plantilla | n_predict | temp | top_p | repeat | Uso |
|-----------|-----------|------|-------|--------|-----|
| 🛡️ Conservador | 150 | 0.5 | 0.75 | 1.4 | Precisión |
| ⚖️ Balanceado | 200 | 0.7 | 0.9 | 1.5 | General |
| 🎨 Creativo | 250 | 0.85 | 0.95 | 1.3 | Ideas |
| 🎯 Preciso | 100 | 0.4 | 0.7 | 1.6 | Brevedad |
| 💬 Conversacional | 180 | 0.75 | 0.92 | 1.4 | Chat |
| 🔧 Técnico | 300 | 0.6 | 0.88 | 1.5 | Código |
| ⚡ Conciso | 80 | 0.55 | 0.8 | 1.7 | Rapidez |
| 📚 Detallado | 400 | 0.65 | 0.9 | 1.4 | Tutoriales |
| 🧪 Experimental | 220 | 0.8 | 0.85 | 1.2 | Pruebas |
| ✨ Gemma Optimizado | 200 | 0.7 | 0.9 | 1.5 | Probado |

---

## 💡 Ejemplos de Uso

### **Pregunta Técnica:**
```
Pregunta: "Muéstrame un ejemplo de función en Python"

Plantilla recomendada: 🔧 Técnico
Razón: n_predict: 300, bueno para código largo
```

---

### **Pregunta Simple:**
```
Pregunta: "¿Qué es Python?"

Plantilla recomendada: 🎯 Preciso
Razón: n_predict: 100, respuesta corta y directa
```

---

### **Conversación Casual:**
```
Pregunta: "Hola, ¿cómo estás?"

Plantilla recomendada: 💬 Conversacional
Razón: temperature: 0.75, más natural
```

---

## 📈 Sistema de Ratings

### **Cómo Funciona:**

1. **Cada vez que das "Me gusta":**
   - Se incrementa el contador de esa plantilla
   - Se guarda en `localStorage`
   - Se actualiza el ranking

2. **Ver las mejores:**
   - Clic en botón 📊
   - Muestra top 3 plantillas por likes

3. **Historial persistente:**
   - Los ratings se guardan en el navegador
   - No se pierden al cerrar el chat

---

## 🔧 Personalización

### **Crear Nueva Plantilla:**

Edita `web/template-profiles.js`:

```javascript
mi_plantilla: {
    name: "🚀 Mi Plantilla",
    description: "Descripción personalizada",
    systemPrompt: "Tu prompt aquí",
    params: {
        n_predict: 200,
        temperature: 0.7,
        top_p: 0.9,
        repeat_penalty: 1.5,
        presence_penalty: 0.3,
        frequency_penalty: 0.3
    }
}
```

Luego agrégala en `web/chat.html`:
```html
<option value="mi_plantilla">🚀 Mi Plantilla</option>
```

---

## 🎯 Objetivo

**Encontrar la configuración óptima para Gemma 3-12B**

Después de probar las 10 plantillas con las mismas preguntas:
1. Ver estadísticas (botón 📊)
2. Identificar las top 3 con más likes
3. Usar esa configuración como base definitiva
4. Ajustar finamente si es necesario

---

## 📚 Archivos Creados

| Archivo | Descripción |
|---------|-------------|
| `web/template-profiles.js` | ✅ 10 plantillas con parámetros |
| `web/chat.html` | ✅ Selector de plantillas agregado |
| `web/chat.css` | ✅ Estilos para selector |
| `web/chat-app.js` | ✅ Botón "Me gusta" conectado |
| `SISTEMA_PLANTILLAS_README.md` | ✅ Esta guía |

---

## 🧪 Preguntas de Prueba Sugeridas

Usa estas preguntas para probar cada plantilla:

1. **Simple:**
   ```
   ¿Qué es Python?
   ```

2. **Técnica:**
   ```
   Explícame cómo funciona la arquitectura híbrida Transformer-Mamba
   ```

3. **Código:**
   ```
   Muéstrame un ejemplo de función en Python
   ```

4. **Identidad:**
   ```
   ¿Cómo te llamas?
   ```

5. **Cálculo:**
   ```
   Calcula 789 × 456
   ```

---

## 📊 Ejemplo de Flujo

```
1. Seleccionar: 🛡️ Conservador
2. Preguntar: "¿Qué es Python?"
3. Leer respuesta
4. Si gusta → Clic en "Me gusta" ❤️
5. Crear nuevo chat
6. Seleccionar: ⚖️ Balanceado
7. Preguntar: "¿Qué es Python?" (MISMA pregunta)
8. Leer respuesta
9. Si gusta → Clic en "Me gusta" ❤️
10. Repetir para las 10 plantillas
11. Ver estadísticas (📊)
12. Identificar la mejor plantilla
```

---

## 🏆 Después de las Pruebas

Una vez identificada la mejor plantilla:

1. **Úsala como predeterminada:**
   - Edita `template-profiles.js`
   - Cambia la línea: `window.activeTemplate = 'tu_mejor_plantilla';`

2. **O simplemente selecciónala** cada vez que uses el chat
   - El sistema recuerda tu última selección

---

## 📝 Guardar Resultados

Los ratings se guardan automáticamente en:
- `localStorage.templateRatings`

Puedes exportarlos en la consola:
```javascript
console.log(JSON.stringify(window.templateRatings, null, 2));
```

---

## 🚀 Estado del Sistema

```
✅ Plantillas:           10 configuraciones únicas
✅ Sistema de ratings:   Activo (botón "Me gusta")
✅ Estadísticas:         Ver con botón 📊
✅ Persistencia:         localStorage
✅ Selector UI:          Agregado arriba del input
```

---

## 🎯 Próximos Pasos

1. **Recarga el chat** (Ctrl + Shift + R)
2. **Ve el selector** de plantillas arriba del input
3. **Prueba cada plantilla** con la misma pregunta
4. **Da "Me gusta"** a las mejores
5. **Ve estadísticas** (botón 📊)
6. **Identifica la ganadora** 🏆

---

**¡Empieza probando con la pregunta "¿Qué es Python?" en las 10 plantillas!** 🎯

