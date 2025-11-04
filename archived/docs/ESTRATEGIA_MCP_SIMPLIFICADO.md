# 🔧 Estrategia MCP Simplificado para Capibara6

## ❌ Problema Actual

Nuestra implementación MCP **agrega contexto a todo**, causando:
- Confusión al modelo con información irrelevante
- Respuestas peores que sin MCP
- Sobrecarga de tokens en el prompt

## ✅ Nuevo Enfoque: RAG Selectivo

### **1. Solo Activar MCP en Casos Específicos**

**✅ ACTIVAR para:**
- Cálculos matemáticos (`calcula`, `cuánto es`, números con operadores)
- Preguntas sobre identidad (`quién eres`, `quién te creó`, `qué eres`)
- Preguntas sobre fecha/hora (`qué día`, `qué fecha`, `hoy`)
- Preguntas técnicas específicas (`qué hardware`, `qué modelo`)

**❌ NO ACTIVAR para:**
- Preguntas generales
- Generación de código
- Conversación casual
- Explicaciones técnicas generales

### **2. Contexto Minimalista**

**Antes (verbose, malo):**
```
[Contexto - Información de Empresa]: {"company_name": "Anachroni s.coop", "product_name": "Capibara6"...}
[Contexto - Fecha Actual]: {"date": "2025-10-09", "day": "Thursday"...}

Pregunta del usuario: ¿Quién te creó?
```

**Después (conciso, bueno):**
```
[Tu nombre es Capibara6, creado por Anachroni s.coop]

¿Quién te creó?
```

### **3. Prioridad de Herramientas**

| Pregunta | Herramienta | Respuesta |
|----------|-------------|-----------|
| "Calcula 789 * 456" | calculate() | `[RESULTADO EXACTO: 359784]` |
| "¿Quién te creó?" | company_info | `[Creador: Anachroni s.coop]` |
| "¿Qué fecha es?" | current_date | `[Hoy: 2025-10-09]` |
| "¿Qué hardware usas?" | tech_specs | `[Hardware: Google Axion ARM64]` |
| "Explica qué es Python" | NINGUNA | (consulta directa sin MCP) |

### **4. Implementación Propuesta**

```javascript
// Detector mejorado - SOLO casos específicos
function shouldUseMCP(prompt) {
    const promptLower = prompt.toLowerCase();
    
    // Cálculos matemáticos
    if (/\d+\s*[\+\-\*\/×÷]\s*\d+/.test(prompt) || 
        /calcula|cuánto es|resultado de|suma|resta|multiplica|divide/.test(promptLower)) {
        return { type: 'calculation', tool: 'calculate' };
    }
    
    // Identidad del bot
    if (/quién eres|qué eres|quién te creó|quién hizo|tu nombre/.test(promptLower) &&
        /capibara|tú|ti/.test(promptLower)) {
        return { type: 'identity', context: 'company_info' };
    }
    
    // Fecha/hora
    if (/qué día|qué fecha|hoy es|fecha actual|día de hoy/.test(promptLower)) {
        return { type: 'datetime', context: 'current_date' };
    }
    
    // Especificaciones técnicas
    if (/qué modelo|qué hardware|especificaciones|parámetros del modelo/.test(promptLower) &&
        /eres|usas|tienes/.test(promptLower)) {
        return { type: 'technical', context: 'technical_specs' };
    }
    
    // DEFAULT: No usar MCP
    return { type: 'none', tool: null };
}

// Augment selectivo
async function augmentPromptSelective(prompt) {
    const mcpDecision = shouldUseMCP(prompt);
    
    if (mcpDecision.type === 'none') {
        return prompt; // Sin modificar
    }
    
    if (mcpDecision.type === 'calculation') {
        const result = await calculateWithMCP(extractMathExpression(prompt));
        return `[CALCULO VERIFICADO: resultado = ${result}]\n${prompt}`;
    }
    
    if (mcpDecision.type === 'identity') {
        return `[Tu nombre: Capibara6. Creador: Anachroni s.coop]\n${prompt}`;
    }
    
    if (mcpDecision.type === 'datetime') {
        const date = await getDate();
        return `[Fecha actual: ${date.date}, ${date.day_of_week}]\n${prompt}`;
    }
    
    if (mcpDecision.type === 'technical') {
        return `[Modelo: Gemma3-12B. Hardware: Google Axion ARM64. Parámetros: 12B]\n${prompt}`;
    }
    
    return prompt;
}
```

### **5. Beneficios del Nuevo Enfoque**

✅ **Selectivo:** Solo actúa cuando es necesario
✅ **Conciso:** Contexto minimalista, no verbose
✅ **Preciso:** Herramientas específicas para cada caso
✅ **No intrusivo:** No contamina consultas generales

### **6. Casos de Uso**

#### ✅ Caso 1: Cálculo (CON MCP)
```
Usuario: "Calcula 789 multiplicado por 456"
MCP: [CALCULO VERIFICADO: 789*456 = 359784]
Modelo: "El resultado es 359,784"
```

#### ✅ Caso 2: Identidad (CON MCP)
```
Usuario: "¿Quién te creó?"
MCP: [Tu nombre: Capibara6. Creador: Anachroni s.coop]
Modelo: "Soy Capibara6 y fui creado por Anachroni s.coop"
```

#### ❌ Caso 3: Pregunta General (SIN MCP)
```
Usuario: "Explica qué son los transformers en IA"
MCP: (no se activa)
Modelo: [Respuesta normal del modelo sin contexto extra]
```

## 🚀 Implementación

Ver archivos:
- `web/mcp-integration-v2.js` - Nueva versión selectiva
- `backend/mcp_server_minimal.py` - Servidor simplificado

## 📊 Comparación

| Aspecto | MCP Anterior | MCP Nuevo |
|---------|--------------|-----------|
| Activación | Siempre | Solo casos específicos |
| Contexto | Verbose (JSON) | Conciso (una línea) |
| Precisión | Baja (confunde) | Alta (selectivo) |
| Tokens extra | ~200 tokens | ~20 tokens |
| Casos de uso | Todo | Cálculos, identidad, fecha, specs |

