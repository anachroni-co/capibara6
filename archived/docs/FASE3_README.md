# FASE 3: E2B Integration - Ejecución de Código en Sandboxes

## 🎯 Objetivo

Implementar el sistema de ejecución de código E2B que permite:
- **Ejecución segura** de código en sandboxes aislados
- **Detección automática** de bloques de código en respuestas
- **Loop multi-round** con corrección automática (máximo 3 intentos)
- **Mapeo de errores** comunes y estrategias de corrección
- **Feedback loop** hacia ACE para aprendizaje continuo

## 📋 Componentes Implementados

### 1. 🏗️ E2B Manager (`backend/execution/e2b_manager.py`)

**E2BSandbox** - Sandbox individual con límites de recursos:
- Integración con E2B SDK real
- Límites de memoria, CPU y timeout
- Gestión de ciclo de vida del sandbox
- Fallback a simulación si E2B no está disponible

**E2BManager** - Gestión de múltiples sandboxes:
- Pool de sandboxes concurrentes (máximo 5)
- Ejecución paralela de múltiples códigos
- Estadísticas de ejecución y performance
- Limpieza automática de recursos

**Características:**
- **Lenguajes soportados**: Python, JavaScript, SQL, Bash
- **Límites configurables**: Timeout (30s), Memoria (512MB), CPU (50%)
- **Pool management**: Máximo 5 sandboxes concurrentes
- **Error handling**: Manejo robusto de errores con fallback

### 2. 🔍 Code Detector (`backend/execution/code_detector.py`)

**CodeBlock** - Representación de bloque de código:
- Análisis de complejidad automático
- Detección de candidatos para ejecución
- Metadata de posición y contexto
- Scoring de complejidad (0-1)

**CodeDetector** - Detección inteligente de código:
- **Markdown blocks**: ```python, ```javascript, ```sql
- **Inline code**: `código` entre backticks
- **Heuristic detection**: Código sin markdown
- **Language detection**: Automática basada en contexto

**Características:**
- **Detección multi-formato**: Markdown, inline, heurística
- **Análisis de complejidad**: Basado en patrones de código
- **Filtrado inteligente**: Solo ejecuta código relevante
- **Context extraction**: Contexto alrededor del código

### 3. 🔄 Execution Loop (`backend/execution/execution_loop.py`)

**ExecutionAttempt** - Representa un intento de ejecución:
- Tracking de intentos y correcciones
- Metadata de cada intento
- Resultados y errores

**ExecutionLoop** - Loop multi-round con corrección:
- **Máximo 3 intentos** por ejecución
- **Corrección automática** basada en errores
- **Estrategias predefinidas** para errores comunes
- **Integración con modelo LLM** para correcciones avanzadas

**Estrategias de corrección:**
- **SyntaxError**: Paréntesis faltantes, comillas no cerradas
- **NameError**: Variables no definidas, errores tipográficos
- **TypeError**: Conversión de tipos, operadores inapropiados
- **IndentationError**: Normalización de indentación
- **ImportError**: Importaciones alternativas
- **AttributeError**: Verificaciones de None, nombres de atributos

### 4. 🗺️ Error Mapping (`backend/execution/error_mapping.py`)

**ErrorPattern** - Patrón de error con estrategias:
- Categorización por tipo y severidad
- Múltiples estrategias de corrección
- Tracking de éxito de correcciones
- Condiciones de aplicación

**ErrorMapper** - Mapeo inteligente de errores:
- **8 categorías principales**: Syntax, Runtime, Logic, Import, Type, Resource, Security
- **4 niveles de severidad**: Low, Medium, High, Critical
- **Estrategias contextuales**: Basadas en lenguaje y código
- **Learning system**: Mejora con cada corrección

**Patrones implementados:**
- SyntaxError, NameError, TypeError, IndentationError
- ImportError, AttributeError, IndexError, KeyError
- Estrategias específicas por lenguaje y contexto

### 5. 🔄 Feedback Loop (`backend/execution/feedback_loop.py`)

**ExecutionFeedback** - Feedback estructurado para ACE:
- Análisis completo de ejecución
- Metadata de intentos y correcciones
- Scoring de complejidad y éxito
- Contexto e intención del usuario

**FeedbackLoop** - Envío de feedback a ACE:
- **Integración con ACE Curator** para aprendizaje
- **Batch processing** de múltiples feedbacks
- **Insights generation** basados en estadísticas
- **Queue management** para procesamiento asíncrono

**Características:**
- **Feedback estructurado**: Formato estándar para ACE
- **Batch processing**: Múltiples feedbacks en lote
- **Insights automáticos**: Análisis de performance y errores
- **Queue system**: Procesamiento asíncrono

### 6. 🔗 E2B Integration (`backend/execution/e2b_integration.py`)

**E2BIntegration** - Integración completa del sistema:
- **Pipeline completo**: Detección → Ejecución → Corrección → Feedback
- **Configuración cloud**: Integración con Google Cloud
- **Métricas consolidadas**: Estadísticas de todo el pipeline
- **Insights avanzados**: Recomendaciones automáticas

**Características:**
- **Pipeline automatizado**: Detección y ejecución automática
- **Configuración cloud**: API keys y endpoints
- **Métricas integradas**: Performance de todo el sistema
- **Insights inteligentes**: Recomendaciones basadas en datos

## 🚀 Configuración y Uso

### Configuración de Cloud (`backend/config/cloud_config.py`)

```python
# Configuración automática desde variables de entorno
E2B_API_KEY=e2b_01ea80c0f5c76ebcac24d99e9136e2975787b918
GCP_PROJECT_ID=mamba-001
GCP_ZONE=europe-southwest1-b
GCP_VM_NAME=gpt-oss-20b
```

### Uso Básico

```python
from backend.execution.e2b_integration import E2BIntegration

# Crear integración
integration = E2BIntegration()

# Procesar respuesta con código
result = await integration.process_response_with_code(
    response="Aquí tienes código Python:\n```python\nprint('Hello!')\n```",
    query="Show me Python code",
    context="Programming help",
    user_intent="Learn Python"
)

# Ejecutar código directamente
direct_result = await integration.execute_code_directly(
    code="print('Hello, World!')",
    language="python"
)
```

### Integración con ACE

```python
from backend.ace.curator import ACECurator
from backend.execution.e2b_integration import E2BIntegration

# Crear componentes
ace_curator = ACECurator()
e2b_integration = E2BIntegration(ace_curator=ace_curator)

# El feedback se envía automáticamente al ACE
result = await e2b_integration.process_response_with_code(
    response="Código con errores...",
    query="Fix this code",
    context="Debugging help"
)
```

## 📊 Métricas y Monitoreo

### Métricas de E2B Manager
- Total de ejecuciones
- Ejecuciones exitosas/fallidas
- Tiempo promedio de ejecución
- Uso por lenguaje
- Tipos de errores más comunes

### Métricas de Code Detector
- Bloques de código detectados
- Candidatos para ejecución
- Lenguajes detectados
- Complejidad promedio

### Métricas de Execution Loop
- Loops completados
- Intentos promedio por loop
- Correcciones aplicadas
- Tasa de éxito por intento

### Métricas de Error Mapping
- Errores mapeados por categoría
- Estrategias de corrección exitosas
- Tasa de éxito por tipo de error
- Errores más comunes

### Métricas de Feedback Loop
- Feedback enviado al ACE
- Tasa de éxito de feedback
- Insights generados
- Recomendaciones aplicadas

## 🔧 Configuración Avanzada

### Límites de Recursos
```python
e2b_config = {
    'timeout': 30,              # Segundos
    'memory_limit_mb': 512,     # MB
    'cpu_limit_percent': 50,    # Porcentaje
    'max_concurrent_sandboxes': 5
}
```

### Estrategias de Corrección
```python
# Personalizar estrategias
error_mapper = ErrorMapper()
custom_pattern = ErrorPattern(
    error_type="CustomError",
    category=ErrorCategory.RUNTIME,
    severity=ErrorSeverity.MEDIUM,
    patterns=["custom error pattern"],
    correction_strategies=[...]
)
error_mapper.add_custom_pattern(custom_pattern)
```

### Configuración de Feedback
```python
# Configurar feedback loop
feedback_loop = FeedbackLoop(ace_curator)
feedback_loop.set_sampling_rate(0.1)  # 10% sampling
```

## 🧪 Testing

### Tests Unitarios
```bash
# Ejecutar tests de FASE 3
python backend/test_fase3.py

# Test específico de E2B real
python backend/test_e2b_real.py
```

### Tests de Integración
```python
# Test completo del pipeline
async def test_full_pipeline():
    integration = E2BIntegration()
    
    result = await integration.process_response_with_code(
        response="Código con errores...",
        query="Fix this code",
        context="Debugging"
    )
    
    assert result['success']
    assert len(result['execution_results']) > 0
```

## 📁 Estructura de Archivos

```
backend/execution/
├── __init__.py              # Inicialización del módulo
├── e2b_manager.py           # Gestión de sandboxes E2B
├── code_detector.py         # Detección de código
├── execution_loop.py        # Loop multi-round
├── error_mapping.py         # Mapeo de errores
├── feedback_loop.py         # Feedback a ACE
└── e2b_integration.py       # Integración completa

backend/config/
└── cloud_config.py          # Configuración cloud

backend/test_fase3.py        # Tests de FASE 3
backend/test_e2b_real.py     # Tests E2B real
```

## 🎯 Próximos Pasos (FASE 4)

1. **Persistent Agent Memory** - Memoria persistente de agentes
2. **Agent Graduation System** - Sistema de graduación (85% success)
3. **Domain Specialization** - Especialización por dominios
4. **Agent Collaboration** - Colaboración entre agentes

## 📊 Estado Actual

✅ **Completado:**
- E2B Manager con SDK real
- Code Detector multi-formato
- Execution Loop con corrección automática
- Error Mapping con 8 categorías
- Feedback Loop hacia ACE
- Integración completa del pipeline
- Configuración cloud con Google Cloud
- Tests completos y documentación

🔄 **En Progreso:**
- Optimizaciones de performance
- Integración con modelos reales en Google Cloud
- Población de estrategias de corrección

📋 **Pendiente:**
- Persistent Agent Memory (FASE 4)
- Agent Graduation System (FASE 4)
- Domain Specialization (FASE 4)
- Metadata System (FASE 5)

## 🤝 Contribución

Para contribuir al sistema E2B:

1. Fork del repositorio
2. Crear branch para feature
3. Implementar cambios con tests
4. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

**FASE 3 completada exitosamente** 🎉

El sistema E2B está listo para la integración con Persistent Agent Memory en la FASE 4.
