# 🎯 Smart MCP v2.0 - Selective RAG para Capibara6

## 📚 ¿Qué Aprendimos del MCP Real?

Después de investigar las implementaciones reales del **Model Context Protocol** de Anthropic y Google Cloud, descubrimos que nuestro enfoque inicial tenía problemas:

### ❌ Problemas de la Versión Anterior (MCP v1)
1. **Agregaba contexto a TODAS las consultas** → Sobrecarga innecesaria
2. **Formato muy verbose** → Confundía al modelo
3. **No era selectivo** → Contexto irrelevante empeoraba las respuestas

### ✅ Enfoque Correcto (Smart MCP v2.0)
Implementamos un **Selective RAG (Retrieval-Augmented Generation)** que:
- ✨ **Solo agrega contexto cuando es REALMENTE necesario**
- 🎯 **Detecta automáticamente el tipo de consulta**
- ⚡ **Es ligero y rápido (timeout 2s)**
- 🔄 **Fallback automático si falla**

---

## 🏗️ Arquitectura

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │ "¿Quién eres?"
       ▼
┌─────────────────────────┐
│  Smart MCP Analyzer     │  ← Detecta si necesita contexto
│  (smart-mcp-integration)│
└──────┬──────────────────┘
       │
       ├─ SÍ necesita contexto ─────┐
       │                             ▼
       │                    ┌────────────────┐
       │                    │ Knowledge Base │
       │                    │  • Identidad   │
       │                    │  • Fecha       │
       │                    │  • Cálculos    │
       │                    └────────────────┘
       │                             │
       │                             ▼
       │                  "Capibara6, creado por Anachroni"
       │                             │
       ├─ NO necesita contexto ──────┤
       │                             │
       ▼                             ▼
┌──────────────────────────────────────────┐
│  Capibara6 (Gemma 3-12B)                 │
│  + Contexto solo si es necesario         │
└──────────────────────────────────────────┘
```

---

## 🔍 Detección Inteligente de Contexto

### 1️⃣ Contexto de Identidad
**Cuándo se activa:**
- "¿Quién eres?"
- "¿Cómo te llamas?"
- "¿Quién te creó?"
- Menciones a "Capibara"

**Contexto agregado:**
```
[INFO VERIFICADA]
Nombre: Capibara6 Consensus
Estado: Beta (en pruebas)
Creador: Anachroni s.coop
Web: http://www.anachroni.co
Contacto: info@anachroni.co
Tipo: Modelo de lenguaje basado en Gemma 3-12B
Hardware: Google Cloud TPU v5e-64
```

### 2️⃣ Contexto de Fecha/Tiempo
**Cuándo se activa:**
- "¿Qué día es hoy?"
- "¿Qué fecha es?"
- "¿Cuándo estamos?"

**Contexto agregado:**
```
[FECHA ACTUAL]
Hoy es jueves, 9 de octubre de 2025
```

### 3️⃣ Cálculos Matemáticos
**Cuándo se activa:**
- "Calcula 789 × 456"
- "¿Cuánto es 25 + 17?"
- Detecta operaciones: `+`, `-`, `*`, `×`, `/`, `÷`

**Contexto agregado:**
```
[CÁLCULO]
789 × 456 = 359784

Pregunta: Calcula 789 × 456
```

---

## 🚀 Uso

### Inicio Rápido

1. **Iniciar el servidor Smart MCP:**
```bash
# Windows
start_smart_mcp.bat

# Linux/Mac
python backend/smart_mcp_server.py
```

2. **El servidor corre en:** `http://localhost:5003`

3. **Verificar estado:**
```bash
curl http://localhost:5003/health
```

Respuesta:
```json
{
  "status": "healthy",
  "service": "smart-mcp-capibara6",
  "version": "2.0",
  "approach": "selective-rag"
}
```

### Integración Frontend

El frontend automáticamente:
- ✅ Verifica si el servidor MCP está activo
- ✅ Analiza cada consulta antes de enviarla
- ✅ Agrega contexto solo si es necesario
- ✅ Usa fallback si el servidor no responde

**Indicador Visual:**
- 🟢 Verde: Smart MCP activo
- ⚫ Gris: No disponible (funciona en modo directo)

### Control Manual

```javascript
// Deshabilitar Smart MCP
toggleSmartMCP(false);

// Habilitar Smart MCP
toggleSmartMCP(true);

// Verificar estado
checkSmartMCPHealth();
```

---

## 📊 Comparación de Rendimiento

### Antes (MCP v1)
```
Usuario: "Hola, ¿cómo estás?"

Prompt enviado al modelo:
[EMPRESA] Creado por Anachroni s.coop, una cooperativa...
[IDENTIDAD] Eres Capibara6, un modelo avanzado...
[FECHA] Hoy es jueves 9 de octubre de 2025...
[HERRAMIENTAS] Puedes usar: calculadora, búsqueda...

Pregunta: Hola, ¿cómo estás?

Resultado: ❌ Respuesta confusa con información irrelevante
```

### Ahora (Smart MCP v2.0)
```
Usuario: "Hola, ¿cómo estás?"

Análisis: ❌ No necesita contexto adicional

Prompt enviado:
Hola, ¿cómo estás?

Resultado: ✅ Respuesta natural y directa
```

```
Usuario: "¿Quién eres?"

Análisis: ✅ Necesita contexto de identidad

Prompt enviado:
[INFO VERIFICADA]
Nombre: Capibara6 Consensus
Estado: Beta (en pruebas)
Creador: Anachroni s.coop
Web: http://www.anachroni.co
Contacto: info@anachroni.co
Tipo: Modelo basado en Gemma 3-12B
Hardware: Google Cloud TPU v5e-64

Pregunta: ¿Quién eres?

Resultado: ✅ Respuesta precisa con información correcta
```

---

## 🛠️ Personalización

### Agregar Nuevos Contextos

Edita `backend/smart_mcp_server.py`:

```python
CONTEXT_TRIGGERS = {
    "mi_contexto": {
        "patterns": [
            r'\bpalabra_clave\b',
            r'\bexpresión_regular\b'
        ],
        "context": lambda: """[MI CONTEXTO]
Información relevante aquí
"""
    }
}
```

### Actualizar la Fecha

```bash
curl -X POST http://localhost:5003/update-date \
  -H "Content-Type: application/json" \
  -d '{"date": "10 de octubre de 2025", "day": "viernes"}'
```

---

## 🔬 Casos de Prueba

### ✅ Casos que Funcionan Bien

1. **Identidad:**
   - "¿Quién eres?" → Agrega contexto ✅
   - "Hola" → No agrega contexto ✅

2. **Fecha:**
   - "¿Qué día es hoy?" → Agrega contexto ✅
   - "Me gustan los martes" → No agrega contexto ✅

3. **Cálculos:**
   - "Calcula 25 + 17" → Agrega resultado ✅
   - "Dame 25 razones" → No agrega contexto ✅

### 🧪 Pruebas Sugeridas

```javascript
// Test 1: Pregunta simple (sin contexto)
"Explícame qué es Python"

// Test 2: Pregunta de identidad (con contexto)
"¿Cómo te llamas?"

// Test 3: Cálculo (con resultado)
"¿Cuánto es 789 multiplicado por 456?"

// Test 4: Fecha (con contexto)
"¿Qué fecha es hoy?"

// Test 5: Mezcla (con contexto de identidad)
"Hola, ¿quién eres y qué puedes hacer?"
```

---

## 📈 Métricas

El Smart MCP registra automáticamente:

```javascript
{
  "needsContext": true,
  "contextsAdded": 1,
  "lightweight": true,
  "responseTime": "45ms"
}
```

---

## 🔐 Seguridad

- ✅ **No expone información sensible** (solo contexto público)
- ✅ **Timeout de 2 segundos** (no bloquea el sistema)
- ✅ **Fallback automático** si falla
- ✅ **CORS configurado** solo para dominios permitidos

---

## 🎯 Próximos Pasos

### Fase 1: Estable (Actual)
- [x] Detección de identidad
- [x] Detección de fecha
- [x] Cálculos básicos
- [x] Fallback automático

### Fase 2: Expandir Contextos
- [ ] Contexto de empresa (Anachroni s.coop)
- [ ] FAQ frecuentes
- [ ] Documentación técnica

### Fase 3: RAG Avanzado
- [ ] Integración con bases de datos vectoriales
- [ ] Búsqueda semántica en documentos
- [ ] Caché de contextos frecuentes

---

## 📚 Referencias

- [Google Cloud - Model Context Protocol](https://cloud.google.com/discover/what-is-model-context-protocol)
- [Xataka - ¿Qué es MCP?](https://www.xataka.com/basics/mcp-model-context-protocol)
- [NeuralTrust - MCP Guide](https://neuraltrust.ai/es/blog/what-is-model-context-protocol)

---

## 🆘 Troubleshooting

### Problema: MCP no se activa
**Solución:**
```bash
# Verificar que el servidor esté corriendo
curl http://localhost:5003/health

# Reiniciar servidor
start_smart_mcp.bat
```

### Problema: Contexto no se agrega cuando debería
**Solución:**
```javascript
// Verificar en consola del navegador
console.log('MCP habilitado:', SMART_MCP_CONFIG.enabled);

// Forzar activación
toggleSmartMCP(true);
```

### Problema: Respuestas siguen siendo malas
**Causa probable:** El modelo base necesita ajuste de parámetros
**Solución:** Revisar `MODEL_CONFIG.defaultParams` en `chat-app.js`

---

**Smart MCP v2.0** - Contexto inteligente para Capibara6 🎯

