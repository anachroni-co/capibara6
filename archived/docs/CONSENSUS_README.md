# 🧠 Sistema de Consenso Capibara6

## ✅ Implementación Completada

Se ha implementado un sistema completo de consenso entre múltiples modelos de IA, incluyendo el modelo OSS-120B con TPU-v5e-64.

### 🎯 Características Implementadas

- ✅ **Modelo OSS-120B** configurado con TPU-v5e-64
- ✅ **Sistema de Consenso** entre múltiples modelos
- ✅ **Plantillas de Prompts** por categoría
- ✅ **Selector de Modelos** en la interfaz
- ✅ **Selector de Plantillas** dinámico
- ✅ **Fallback Automático** al modelo original
- ✅ **Servidor de Consenso** independiente
- ✅ **Configuración Flexible** por modelo

### 📁 Archivos Creados

#### Backend
- `backend/models_config.py` - Configuración de modelos y plantillas
- `backend/consensus_server.py` - Servidor de consenso
- `backend/requirements.txt` - Dependencias actualizadas

#### Frontend
- `web/consensus-integration.js` - Integración del consenso
- `web/chat.css` - Estilos para selectores
- `web/chat.html` - Scripts incluidos

#### Scripts
- `start_consensus.bat` - Script de inicio con consenso

### 🤖 Modelos Configurados

#### 1. Capibara6 (Gemma3-12B)
- **Hardware:** GPU
- **Servidor:** http://34.175.89.158:8080
- **Especialidad:** Respuestas rápidas y código
- **Peso en consenso:** 0.6

#### 2. OSS-120B (Open Source Supervised 120B)
- **Hardware:** TPU-v5e-64
- **Servidor:** http://tpu-server:8080 (configurar URL real)
- **Especialidad:** Análisis complejos y documentación técnica
- **Peso en consenso:** 0.4

### 🎨 Plantillas de Prompts

#### 1. General
- **Descripción:** Conversación general y preguntas abiertas
- **Modelos:** Capibara6, OSS-120B
- **Uso:** Preguntas cotidianas, explicaciones básicas

#### 2. Programación
- **Descripción:** Ayuda con código, debugging y desarrollo
- **Modelos:** Capibara6, OSS-120B
- **Uso:** Generación de código, resolución de bugs

#### 3. Análisis
- **Descripción:** Análisis de datos, investigación y pensamiento crítico
- **Modelos:** OSS-120B (recomendado)
- **Uso:** Análisis complejos, investigación profunda

#### 4. Creativo
- **Descripción:** Escritura creativa, storytelling y contenido
- **Modelos:** Capibara6, OSS-120B
- **Uso:** Contenido creativo, narrativas

#### 5. Técnico
- **Descripción:** Documentación técnica, arquitectura y sistemas
- **Modelos:** OSS-120B (recomendado)
- **Uso:** Documentación, arquitectura de software

### 🚀 Cómo Usar

#### 1. Iniciar el Sistema

```cmd
start_consensus.bat
```

#### 2. Configurar URLs de Modelos

Editar `backend/models_config.py`:

```python
MODELS_CONFIG = {
    'oss-120b': {
        'server_url': 'http://tu-tpu-server:8080/completion',  # URL real del TPU
        # ... resto de configuración
    }
}
```

#### 3. Acceder a la Interfaz

- **Frontend:** http://localhost:8000
- **Login:** http://localhost:8000/login.html
- **Chat:** http://localhost:8000/chat.html
- **Consensus API:** http://localhost:5002

### 🔧 Configuración del Consenso

#### Métodos de Consenso

1. **Weighted (Ponderado)**
   - Capibara6: Peso 0.6
   - OSS-120B: Peso 0.4
   - Selecciona la respuesta del modelo con mayor peso

2. **Simple**
   - Selecciona la primera respuesta exitosa
   - Útil para testing

#### Configuración

```python
CONSENSUS_CONFIG = {
    'enabled': True,
    'min_models': 2,
    'max_models': 3,
    'voting_method': 'weighted',
    'model_weights': {
        'capibara6': 0.6,
        'oss-120b': 0.4
    },
    'fallback_model': 'capibara6',
    'timeout': 30
}
```

### 📊 API del Consenso

#### Endpoints Disponibles

- **POST /api/consensus/query** - Consulta con consenso
- **GET /api/consensus/models** - Información de modelos
- **GET /api/consensus/templates** - Plantillas disponibles
- **GET /api/consensus/config** - Configuración del consenso
- **GET /api/consensus/health** - Health check

#### Ejemplo de Consulta

```javascript
const response = await fetch('http://localhost:5002/api/consensus/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        prompt: 'Explica qué es la inteligencia artificial',
        template: 'general',
        models: ['capibara6', 'oss-120b']
    })
});

const result = await response.json();
console.log(result.response); // Respuesta del consenso
```

### 🎛️ Interfaz de Usuario

#### Selector de Plantillas
- Dropdown con plantillas disponibles
- Cambio dinámico de contexto
- Persistencia de selección

#### Selector de Modelos
- Checkboxes para activar/desactivar modelos
- Información de hardware
- Actualización en tiempo real

#### Indicador de Consenso
- Muestra número de modelos activos
- Información detallada en tooltip
- Estado de conexión

### 🔄 Flujo de Consenso

1. **Usuario envía mensaje**
2. **Sistema selecciona plantilla**
3. **Consulta modelos activos en paralelo**
4. **Aplica método de consenso**
5. **Devuelve respuesta final**
6. **Fallback automático si falla**

### 🛡️ Fallback y Robustez

- **Fallback automático** al modelo original si falla el consenso
- **Timeout configurable** para evitar esperas largas
- **Manejo de errores** por modelo individual
- **Health checks** para verificar conectividad

### 📈 Próximas Mejoras

- [ ] **Streaming de consenso** en tiempo real
- [ ] **Métricas de calidad** por modelo
- [ ] **Aprendizaje automático** de pesos
- [ ] **Más modelos** (GPT, Claude, etc.)
- [ ] **Análisis de sentimientos** en respuestas
- [ ] **Cache inteligente** de respuestas

### 🆘 Solución de Problemas

**Error: "Consensus server unreachable"**
- Verificar que el servidor de consenso esté ejecutándose en puerto 5002
- Comprobar conectividad de red

**Error: "No models available"**
- Verificar configuración en `models_config.py`
- Comprobar URLs de servidores de modelos

**Error: "Template not found"**
- Verificar que la plantilla existe en `PROMPT_TEMPLATES`
- Comprobar configuración de plantillas

---

¡El sistema de consenso está listo para usar! 🎉

**Para configurar el OSS-120B con TPU-v5e-64, actualiza la URL del servidor en `backend/models_config.py`**
