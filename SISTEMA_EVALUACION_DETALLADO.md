# 📊 Sistema de Evaluación Detallado

## 🎯 ¿Qué es?

Un sistema completo de **evaluación por criterios** que te permite puntuar cada aspecto de las respuestas (1-5 estrellas) y obtener **recomendaciones automáticas** sobre qué parámetros ajustar.

---

## ⭐ Los 6 Criterios de Evaluación

| # | Criterio | Pregunta | Afecta Parámetros |
|---|----------|----------|-------------------|
| 1 | **Coherencia** ✓ | ¿Tiene sentido y es lógica? | `temperature`, `top_p` |
| 2 | **Longitud** 📏 | ¿Ni muy corta ni muy larga? | `n_predict` |
| 3 | **Formato** 📐 | ¿Usa párrafos, listas, negrita? | `systemPrompt` |
| 4 | **Precisión** 🎯 | ¿Información correcta? | `temperature`, `repeat_penalty` |
| 5 | **Limpieza** ✨ | ¿Sin basura (LaTeX, HTML)? | `repeat_penalty`, `presence_penalty`, `frequency_penalty` |
| 6 | **Naturalidad** 💬 | ¿Suena natural? | `temperature`, `top_p`, `repeat_penalty` |

---

## 🚀 Cómo Usar

### **Paso 1: Selecciona Plantilla y Pregunta**

1. Selecciona una plantilla (ej: "🛡️ Conservador")
2. Haz una pregunta (ej: "¿Qué es Python?")
3. Lee la respuesta

### **Paso 2: Abre el Modal de Evaluación**

Clic en el botón **"Me gusta" ❤️** de la respuesta

Se abrirá un modal con 6 criterios para evaluar:

```
┌──────────────────────────────────────┐
│ 📊 Evaluar Respuesta                 │
│ 🛡️ Conservador                       │
├──────────────────────────────────────┤
│                                      │
│ ✓ Coherencia                         │
│ ¿La respuesta tiene sentido?         │
│ ☆ ☆ ☆ ☆ ☆  (1-5 estrellas)         │
│ Afecta: temperature, top_p           │
│                                      │
│ 📏 Longitud                          │
│ ¿La longitud es adecuada?            │
│ ☆ ☆ ☆ ☆ ☆                           │
│ Afecta: n_predict                    │
│                                      │
│ [... 4 criterios más ...]           │
│                                      │
│ Notas adicionales:                   │
│ ┌────────────────────────────┐      │
│ │ Ej: Se repite mucho...     │      │
│ └────────────────────────────┘      │
│                                      │
│ [Cancelar] [Guardar Evaluación]     │
└──────────────────────────────────────┘
```

### **Paso 3: Puntúa Cada Criterio**

Haz clic en las estrellas (1-5) para cada criterio:

- ⭐ = 1/5 (Muy malo)
- ⭐⭐ = 2/5 (Malo)
- ⭐⭐⭐ = 3/5 (Aceptable)
- ⭐⭐⭐⭐ = 4/5 (Bueno)
- ⭐⭐⭐⭐⭐ = 5/5 (Excelente)

**Ejemplo:**
```
✓ Coherencia:    ⭐⭐⭐⭐⭐ (5/5) - Muy coherente
📏 Longitud:     ⭐⭐⭐ (3/5) - Un poco larga
📐 Formato:      ⭐⭐⭐⭐ (4/5) - Buen formato
🎯 Precisión:    ⭐⭐⭐⭐⭐ (5/5) - Muy precisa
✨ Limpieza:     ⭐⭐ (2/5) - Genera LaTeX
💬 Naturalidad:  ⭐⭐⭐⭐ (4/5) - Suena natural
```

### **Paso 4: Agrega Notas (Opcional)**

Escribe observaciones específicas:

```
Notas: Se repite mucho al final. Genera código LaTeX innecesario.
```

### **Paso 5: Guardar**

Clic en **"Guardar Evaluación"**

Verás una notificación:
```
✅ Evaluación guardada
   Promedio: 4.2/5
```

---

## 📊 Ver Estadísticas Detalladas

### **Clic en el Botón [📊]**

Se abrirá un modal con:

```
┌──────────────────────────────────────────────┐
│ 📊 Estadísticas Detalladas                   │
├──────────────────────────────────────────────┤
│                                              │
│ #1 🎯 Preciso                    4.5/5      │
│ ├─ Coherencia:     ████████░░ 4.8/5        │
│ ├─ Longitud:       ██████████ 5.0/5        │
│ ├─ Formato:        ███████░░░ 4.2/5        │
│ ├─ Precisión:      ████████░░ 4.6/5        │
│ ├─ Limpieza:       ███████░░░ 4.0/5        │
│ └─ Naturalidad:    ████████░░ 4.5/5        │
│                                              │
│ 💡 Recomendaciones:                          │
│ ✅ Coherencia excelente (4.8/5) - Mantener   │
│ ✅ Longitud excelente (5.0/5) - Mantener     │
│                                              │
│ Total de evaluaciones: 3                     │
│                                              │
│ #2 ⚖️ Balanceado                 3.8/5      │
│ [... similar ...]                            │
│                                              │
│ #3 💬 Conversacional             3.2/5      │
│ [... similar ...]                            │
│                                              │
│ [📥 Exportar Resultados] [🗑️ Borrar Todo]   │
└──────────────────────────────────────────────┘
```

---

## 💡 Recomendaciones Automáticas

El sistema genera recomendaciones automáticas basadas en tus evaluaciones:

### **Si un Criterio Puntúa Bajo (<3)**

```
⚠️ Limpieza baja (2.3/5) - Ajustar: repeat_penalty, presence_penalty, frequency_penalty

ACCIÓN SUGERIDA:
- ⬆️ Aumentar repeat_penalty de 1.5 a 1.8
- ⬆️ Aumentar presence_penalty de 0.3 a 0.5
```

### **Si un Criterio Puntúa Alto (≥4.5)**

```
✅ Coherencia excelente (4.8/5) - Mantener configuración

ACCIÓN SUGERIDA:
- ✅ Mantener temperature en 0.7
- ✅ Mantener top_p en 0.9
```

---

## 📋 Ejemplo de Flujo Completo

### **Plantilla: 🛡️ Conservador**

**1. Pregunta:**
```
¿Qué es Python?
```

**2. Respuesta recibida:**
```
Python es un lenguaje de programación de alto nivel conocido por su sintaxis clara y legible.
```

**3. Evaluación (Clic en botón ⭐ "Evaluar"):**

| Criterio | Puntuación | Razón |
|----------|------------|-------|
| Coherencia | ⭐⭐⭐⭐⭐ 5/5 | Muy coherente |
| Longitud | ⭐⭐ 2/5 | Demasiado corta |
| Formato | ⭐⭐⭐ 3/5 | Sin listas |
| Precisión | ⭐⭐⭐⭐⭐ 5/5 | Info correcta |
| Limpieza | ⭐⭐⭐⭐⭐ 5/5 | Sin basura |
| Naturalidad | ⭐⭐⭐⭐ 4/5 | Suena bien |

**Promedio:** 4.0/5

**Notas:** "Muy corta, debería dar más detalles."

**4. Recomendación Automática:**
```
⚠️ Longitud baja (2/5) - Ajustar: n_predict

SUGERENCIA: Aumentar n_predict de 150 a 200
```

---

## 📊 Exportar Resultados

### **Clic en "📥 Exportar Resultados"**

Descarga un archivo JSON con todos los datos:

```json
{
  "conservador": {
    "templateName": "🛡️ Conservador",
    "totalEvaluations": 3,
    "averageScores": {
      "coherencia": "4.67",
      "longitud": "2.33",
      "formato": "3.00",
      "precision": "4.67",
      "limpieza": "5.00",
      "naturalidad": "4.00"
    },
    "allRatings": [
      {
        "timestamp": "2025-10-09T22:30:00",
        "scores": {
          "coherencia": 5,
          "longitud": 2,
          "formato": 3,
          "precision": 5,
          "limpieza": 5,
          "naturalidad": 4
        },
        "notes": "Muy corta, debería dar más detalles",
        "totalScore": 4.0
      }
    ],
    "recommendations": [
      {
        "criterion": "longitud",
        "score": 2.33,
        "action": "increase",
        "params": ["n_predict"],
        "message": "⚠️ Longitud baja (2.33/5) - Ajustar: n_predict"
      }
    ]
  }
}
```

Puedes usar estos datos para:
- 📊 Analizar tendencias
- 📈 Comparar plantillas
- 🔧 Ajustar configuraciones

---

## 🔧 Interpretación de Resultados

### **Criterio: Coherencia (Baja)**
```
Puntuación: ⭐⭐ (2/5)
Afecta: temperature, top_p

ACCIÓN:
⬇️ Reducir temperature (más coherente)
⬇️ Reducir top_p (menos diversidad aleatoria)

Ejemplo:
temperature: 0.7 → 0.6
top_p: 0.9 → 0.85
```

### **Criterio: Longitud (Muy Corta)**
```
Puntuación: ⭐⭐ (2/5)
Afecta: n_predict

ACCIÓN:
⬆️ Aumentar n_predict

Ejemplo:
n_predict: 150 → 250
```

### **Criterio: Limpieza (Baja)**
```
Puntuación: ⭐⭐ (2/5)
Afecta: repeat_penalty, presence_penalty, frequency_penalty

ACCIÓN:
⬆️ Aumentar penalties para evitar basura

Ejemplo:
repeat_penalty: 1.5 → 1.8
presence_penalty: 0.3 → 0.5
frequency_penalty: 0.3 → 0.5
```

---

## 🎯 Encontrar la Mejor Configuración

### **Opción 1: Usar la Plantilla Ganadora Directamente**

1. Probar las 10 plantillas
2. Evaluar cada una
3. Ver estadísticas (📊)
4. Usar la #1 del ranking

### **Opción 2: Crear Configuración Híbrida Óptima**

Tomar lo mejor de cada plantilla:

```javascript
// Ejemplo de configuración híbrida óptima
{
    systemPrompt: "Del Técnico",           // Si tuvo mejor Formato
    n_predict: 200,                        // Del Preciso (mejor Longitud)
    temperature: 0.7,                      // Del Balanceado (mejor Coherencia)
    top_p: 0.9,                           // Del Conversacional (mejor Naturalidad)
    repeat_penalty: 1.8,                   // Del Conservador (mejor Limpieza)
    presence_penalty: 0.3,
    frequency_penalty: 0.3
}
```

---

## 📋 Guía de Evaluación

### **¿Cómo Puntuar Cada Criterio?**

#### **1. Coherencia** ✓

| Puntuación | Descripción | Ejemplo |
|------------|-------------|---------|
| ⭐ 1/5 | Incoherente, sin sentido | "höherhöher \textbackslash..." |
| ⭐⭐ 2/5 | Poco coherente | Mezcla ideas sin conexión |
| ⭐⭐⭐ 3/5 | Aceptable | Se entiende pero confuso |
| ⭐⭐⭐⭐ 4/5 | Coherente | Lógico y claro |
| ⭐⭐⭐⭐⭐ 5/5 | Muy coherente | Perfecto sentido |

#### **2. Longitud** 📏

| Puntuación | Descripción | Ejemplo |
|------------|-------------|---------|
| ⭐ 1/5 | Muy corta/larga | 1 palabra o 1000 palabras |
| ⭐⭐ 2/5 | Corta/larga | 10 palabras o 500 palabras |
| ⭐⭐⭐ 3/5 | Aceptable | Suficiente pero mejorable |
| ⭐⭐⭐⭐ 4/5 | Adecuada | Longitud apropiada |
| ⭐⭐⭐⭐⭐ 5/5 | Perfecta | Exactamente lo necesario |

#### **3. Formato** 📐

| Puntuación | Descripción | Ejemplo |
|------------|-------------|---------|
| ⭐ 1/5 | Sin formato | Muro de texto |
| ⭐⭐ 2/5 | Poco formato | Algunos saltos de línea |
| ⭐⭐⭐ 3/5 | Formato básico | Párrafos separados |
| ⭐⭐⭐⭐ 4/5 | Buen formato | Listas, párrafos, negrita |
| ⭐⭐⭐⭐⭐ 5/5 | Formato perfecto | Estructura completa |

#### **4. Precisión** 🎯

| Puntuación | Descripción | Ejemplo |
|------------|-------------|---------|
| ⭐ 1/5 | Info incorrecta | Alucinaciones graves |
| ⭐⭐ 2/5 | Parcialmente incorrecta | Mezcla verdades y mentiras |
| ⭐⭐⭐ 3/5 | Mayormente correcta | Info correcta pero vaga |
| ⭐⭐⭐⭐ 4/5 | Precisa | Info correcta y específica |
| ⭐⭐⭐⭐⭐ 5/5 | Muy precisa | 100% correcto y detallado |

#### **5. Limpieza** ✨

| Puntuación | Descripción | Ejemplo |
|------------|-------------|---------|
| ⭐ 1/5 | Mucha basura | LaTeX, HTML, repeticiones |
| ⭐⭐ 2/5 | Algo de basura | Tags ocasionales |
| ⭐⭐⭐ 3/5 | Mayormente limpio | Pequeños artefactos |
| ⭐⭐⭐⭐ 4/5 | Limpio | Sin basura significativa |
| ⭐⭐⭐⭐⭐ 5/5 | Perfectamente limpio | Cero artefactos |

#### **6. Naturalidad** 💬

| Puntuación | Descripción | Ejemplo |
|------------|-------------|---------|
| ⭐ 1/5 | Robótico | "Soy Bing creado por..." |
| ⭐⭐ 2/5 | Poco natural | Formal y rígido |
| ⭐⭐⭐ 3/5 | Aceptable | Se entiende |
| ⭐⭐⭐⭐ 4/5 | Natural | Como humano |
| ⭐⭐⭐⭐⭐ 5/5 | Muy natural | Conversación fluida |

---

## 🏆 Ranking y Recomendaciones

Después de evaluar las 10 plantillas, el sistema te muestra:

### **Top 3 Plantillas**

```
#1 🎯 Preciso              4.7/5
   ├─ Coherencia:    ████████░░ 4.8/5
   ├─ Longitud:      ██████████ 5.0/5
   ├─ Formato:       ███████░░░ 4.2/5
   ├─ Precisión:     █████████░ 4.9/5
   ├─ Limpieza:      ████████░░ 4.5/5
   └─ Naturalidad:   ███████░░░ 4.1/5
   
   💡 Recomendaciones:
   ✅ Coherencia excelente (4.8/5) - Mantener
   ✅ Longitud excelente (5.0/5) - Mantener
   ⚠️ Formato bajo (4.2/5) - Mejorar systemPrompt
   
   Total de evaluaciones: 3

#2 ⚖️ Balanceado           4.3/5
   [... similar ...]

#3 💬 Conversacional        3.9/5
   [... similar ...]
```

---

## 📥 Exportar y Analizar

### **Exportar Resultados:**

1. Clic en "📥 Exportar Resultados"
2. Se descarga: `capibara6-ratings-2025-10-09.json`
3. Abre el archivo para análisis detallado

### **Formato del JSON:**

```json
{
  "plantilla": {
    "templateName": "Nombre",
    "totalEvaluations": 3,
    "averageScores": {
      "coherencia": "4.67",
      "longitud": "5.00",
      ...
    },
    "allRatings": [...],
    "recommendations": [...]
  }
}
```

---

## 🔄 Flujo Completo de Pruebas

```
1. Selecciona Plantilla #1
        ↓
2. Haz Pregunta
        ↓
3. Lee Respuesta
        ↓
4. Clic en "Me gusta" ❤️
        ↓
5. Evalúa 6 Criterios (⭐⭐⭐⭐⭐)
        ↓
6. Agrega Notas (opcional)
        ↓
7. Guardar Evaluación
        ↓
8. Nuevo Chat
        ↓
9. Repite para Plantillas #2-#10
        ↓
10. Ver Estadísticas (📊)
        ↓
11. Identificar Ganadora (#1)
        ↓
12. Exportar Resultados (📥)
        ↓
13. Usar Configuración Óptima
```

---

## 🎯 Beneficios vs "Me Gusta" Simple

| Feature | "Me Gusta" Simple | Evaluación Detallada |
|---------|-------------------|---------------------|
| **Granularidad** | ❌ Solo sí/no | ✅ 6 criterios de 1-5 |
| **Insights** | ❌ No sabes qué falló | ✅ Sabes exactamente qué arreglar |
| **Recomendaciones** | ❌ Ninguna | ✅ Automáticas y específicas |
| **Parámetros** | ❌ No sabes cuál ajustar | ✅ Te dice qué parámetro modificar |
| **Tracking** | ❌ Solo contador | ✅ Historial completo |
| **Exportar** | ❌ No | ✅ JSON descargable |

---

## 📚 Archivos del Sistema

| Archivo | Descripción |
|---------|-------------|
| `web/rating-system.js` | ✅ Sistema completo de evaluación |
| `web/template-profiles.js` | ✅ 10 plantillas |
| `web/chat.html` | ✅ Modal de evaluación |
| `web/chat.css` | ✅ Estilos del modal (480 líneas) |
| `web/chat-app.js` | ✅ Conectado con "Me gusta" |

---

## 🚀 Estado del Sistema

```
✅ Evaluación detallada:  6 criterios (1-5 estrellas)
✅ Recomendaciones:       Automáticas basadas en puntuaciones
✅ Exportar:              JSON descargable
✅ Ranking:               Top 3 mejores plantillas
✅ Historial:             Todas las evaluaciones guardadas
✅ UI:                    Modal profesional con barras de progreso
```

---

## 🧪 Prueba Ahora

1. **Recarga el chat:**
   ```
   Ctrl + Shift + R
   ```

2. **Selecciona una plantilla:**
   ```
   🛡️ Conservador
   ```

3. **Haz una pregunta:**
   ```
   ¿Qué es Python?
   ```

4. **Clic en "Me gusta" ❤️**

5. **Evalúa los 6 criterios** con estrellas

6. **Agrega notas** sobre qué mejorar

7. **Guardar**

8. **Repite con las 10 plantillas**

9. **Ver estadísticas** (botón 📊)

---

**¡Ahora tienes evaluación detallada en lugar de solo "me gusta"!** 🎯

