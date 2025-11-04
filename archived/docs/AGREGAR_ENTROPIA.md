# 🎯 Cómo Agregar el Monitor de Entropía

## ✅ Archivos Ya Creados

- ✅ `web/entropy-monitor.js` - Funciones de cálculo
- ✅ `web/chat.css` - Estilos para entropía
- ✅ `web/chat.html` - Script incluido

## 📝 Paso Final: Integrar en chat-app.js

### Ubicación: Función `simulateAssistantResponse`

Busca donde se crean las estadísticas del mensaje (cerca del final de la función, donde se muestran las estadísticas).

**Buscar líneas similares a:**
```javascript
streamingMessageDiv.querySelector('.message-stats').innerHTML = `
    <span class="stat-item">
        <i data-lucide="clock"></i>
        ${duration}s
    </span>
    // ... más estadísticas
`;
```

### Código a Agregar:

**ANTES de crear el HTML de estadísticas, agregar:**

```javascript
// Calcular entropía
const entropy = calculateEntropy(accumulatedText, MODEL_CONFIG.defaultParams.temperature);
const entropyHTML = createEntropyHTML(entropy);
```

**DENTRO del HTML de estadísticas, agregar:**

```javascript
streamingMessageDiv.querySelector('.message-stats').innerHTML = `
    <span class="stat-item">
        <i data-lucide="clock"></i>
        ${duration}s
    </span>
    <span class="stat-item">
        <i data-lucide="zap"></i>
        ${tokensGenerated} gen
    </span>
    <span class="stat-item">
        <i data-lucide="arrow-right"></i>
        ${tokensEvaluated} in
    </span>
    <span class="stat-item">
        <i data-lucide="cpu"></i>
        ${tokensPerSecond} tok/s
    </span>
    <span class="stat-item">
        <i data-lucide="terminal"></i>
        ${totalTokens} total
    </span>
    ${entropyHTML}    <!-- ← AGREGAR ESTA LÍNEA -->
    <span class="stat-item">
        <i data-lucide="gauge"></i>
        ${modelName}
    </span>
`;
```

## 🎨 Resultado Visual

El indicador de entropía se mostrará con:

- 🟢 **Verde** (< 1.0): Muy predecible - Respuestas consistentes
- 🔵 **Azul** (1.0-1.5): Normal - Balanceado
- 🟠 **Naranja** (1.5-2.5): Creativo - Respuestas variadas
- 🔴 **Rojo** (> 2.5): Aleatorio - Máxima creatividad

### Ejemplo:
```
⏱️ 2.5s  ⚡ 50 gen  ➡️ 100 in  💻 20 tok/s  🖥️ 150 total  📊 1.45 H  ⚙️ capibara6
```

## 🧪 Probar

1. Recarga el chat
2. Envía un mensaje
3. Observa las estadísticas
4. El valor de entropía aparecerá con color según el nivel

## 📊 Interpretación de Valores

| Rango | Color | Significado | Descripción |
|-------|-------|-------------|-------------|
| 0.0 - 1.0 | 🟢 Verde | Muy Predecible | El modelo está muy seguro, respuestas repetitivas |
| 1.0 - 1.5 | 🔵 Azul | Normal | Balance ideal entre creatividad y coherencia |
| 1.5 - 2.5 | 🟠 Naranja | Creativo | Respuestas más variadas y originales |
| > 2.5 | 🔴 Rojo | Aleatorio | Máxima creatividad, puede perder coherencia |

## 🔧 Ajuste Fino

Si quieres ajustar la sensibilidad, edita en `entropy-monitor.js`:

```javascript
// Línea 47-50: Ajustar umbrales
function getEntropyClass(entropy) {
    if (entropy < 1.0) return 'entropy-low';      // ← Ajustar aquí
    if (entropy < 1.5) return 'entropy-normal';   // ← Ajustar aquí
    if (entropy < 2.5) return 'entropy-medium';   // ← Ajustar aquí
    return 'entropy-high';
}
```

## 💡 Tooltip Informativo

Al pasar el mouse sobre el indicador de entropía, se muestra:
```
Entropía: 1.45 - Predecible

Mide la aleatoriedad/sorpresa en las predicciones del modelo:
• < 1.0: Muy predecible (respuestas consistentes)
• 1.0-1.5: Normal (balanceado)
• 1.5-2.5: Creativo (respuestas variadas)
• > 2.5: Aleatorio (máxima creatividad)
```

## 🚀 Mejora Futura: Entropía Real del Servidor

Cuando el servidor llama.cpp empiece a devolver la entropía real en la respuesta, solo necesitas actualizar:

```javascript
// En simulateAssistantResponse, usar entropía del servidor si está disponible
const serverEntropy = getServerEntropy(result);
const entropy = serverEntropy !== null ? serverEntropy : 
                calculateEntropy(accumulatedText, MODEL_CONFIG.defaultParams.temperature);
```

---

**Estado:** ✅ Listo para integrar
**Impacto:** 📊 Visual + ℹ️ Informativo
**Complejidad:** 🟢 Simple (una línea de código)
