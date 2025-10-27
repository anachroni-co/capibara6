# FASE 2: ACE Framework - Adaptive Context Evolution

## 🎯 Objetivo

Implementar el ACE Framework que permite al sistema evolucionar y mejorar continuamente a través de:
- **Generación de contexto evolutivo** basado en playbooks
- **Auto-reflexión** sobre la calidad de las respuestas
- **Curaduría automática** de patrones y conocimiento
- **Integración** con el sistema CAG DynamicContext

## 📋 Componentes Implementados

### 1. 📚 Sistema de Playbooks (`backend/ace/playbook.py`)

**PlaybookPattern** - Representa patrones de conocimiento:
- Patrones de query reutilizables
- Templates de contexto efectivos
- Sistema de feedback (helpful/harmful)
- Cálculo de tasa de éxito
- Filtrado por valor

**Playbook** - Contenedor de patrones por dominio:
- Gestión de patrones por dominio (python, sql, javascript, etc.)
- Búsqueda de patrones relevantes
- Tracking de respuestas exitosas/fallidas
- Estadísticas de performance
- Serialización JSON

**PlaybookManager** - Gestión de múltiples playbooks:
- Carga/guardado automático
- Búsqueda por dominio
- Estadísticas consolidadas
- Persistencia en archivos JSON

### 2. 🧠 ACE Generator (`backend/ace/generator.py`)

**ACEGenerator** - Genera contexto evolutivo:
- Detección automática de dominio
- Búsqueda de patrones relevantes
- Construcción de contexto personalizado
- Límites de tokens configurables
- Integración con historial de conversaciones

**Características:**
- **Detección de dominio**: Python, SQL, JavaScript, Debug, ML, API, General
- **Similitud de patrones**: Algoritmo de similitud basado en palabras clave
- **Límites de contexto**: 4K tokens por defecto, configurable
- **Templates dinámicos**: Personalización basada en tipo de respuesta
- **Estadísticas**: Tracking de generaciones y performance

### 3. 🔍 ACE Reflector (`backend/ace/reflector.py`)

**ACEReflector** - Auto-reflexión sobre respuestas:
- Análisis de calidad multi-dimensional
- Detección de alucinaciones y errores factuales
- Scoring automático (0-10)
- Extracción de patrones exitosos
- Sampling configurable (10% por defecto)

**Dimensiones de análisis:**
- **Precisión y completitud** (0-10)
- **Relevancia** (0-10)
- **Claridad** (0-10)
- **Utilidad** (0-10)
- **Corrección factual** (0-10)

**Prompts especializados:**
- Reflexión general
- Análisis de dominio específico
- Extracción de patrones
- Formato JSON estructurado

### 4. 🎨 ACE Curator (`backend/ace/curator.py`)

**ACECurator** - Curaduría automática de conocimiento:
- Actualización de playbooks basada en reflexiones
- Filtrado de patrones de bajo valor
- Persistencia automática (cada N interacciones)
- Limpieza de patrones antiguos
- Procesamiento de feedback de ejecución

**Características:**
- **Umbral de filtrado**: 0.5 por defecto (50% tasa de éxito)
- **Límite de patrones**: 1000 por dominio
- **Persistencia**: Cada 100 interacciones
- **Limpieza**: Patrones >30 días de antigüedad
- **Feedback de ejecución**: Integración con E2B

### 5. 🔗 ACE Integration (`backend/ace/integration.py`)

**ACEIntegration** - Integración completa del framework:
- Ciclo completo: Generación → Reflexión → Curaduría
- Integración con CAG DynamicContext
- Procesamiento síncrono y asíncrono
- Estadísticas consolidadas
- Manejo de errores robusto

**ACEBackgroundProcessor** - Procesamiento background:
- Integración con RQ (Redis Queue)
- Encolado de reflexiones y curaduría
- Procesamiento asíncrono
- Fallback síncrono si RQ no está disponible
- Monitoreo de colas

## 🚀 Uso del Sistema

### Instalación

```bash
# Las dependencias ya están en requirements.txt
pip install -r backend/requirements.txt

# Crear directorios necesarios
mkdir -p backend/data/playbooks
```

### Uso Básico

```python
from backend.ace.integration import ACEIntegration

# Crear integración ACE
ace = ACEIntegration()

# Generar contexto evolutivo
context_result = ace.get_ace_context(
    query="How to create a Python function?",
    domain="python"
)

# Procesar query completa con ciclo ACE
result = ace.process_query_with_ace(
    query="How to create a Python function?",
    response="Use the 'def' keyword followed by the function name...",
    context="Python function context",
    domain="python"
)
```

### Integración con CAG

```python
from backend.ace.integration import ACEIntegration
from backend.core.cag.dynamic_context import DynamicContext

# Crear componentes
ace = ACEIntegration()
dynamic_context = DynamicContext()

# Integrar ACE como proveedor de contexto
ace.integrate_with_dynamic_context(dynamic_context)

# Ahora DynamicContext usará ACE para generar contexto
```

### Procesamiento Background

```python
from backend.ace.integration import ACEBackgroundProcessor

# Crear procesador background
processor = ACEBackgroundProcessor()

# Encolar reflexión
job_id = processor.enqueue_reflection(
    query="How to create a Python function?",
    response="Use the 'def' keyword...",
    domain="python"
)

# Encolar curaduría
curation_job_id = processor.enqueue_curation(
    reflection_result=reflection_data,
    query="How to create a Python function?",
    response="Use the 'def' keyword...",
    domain="python"
)
```

## 📊 Métricas y Monitoreo

### Métricas de Generación
- Total de generaciones
- Generaciones exitosas
- Patrones utilizados
- Longitud promedio de contexto
- Tiempo de generación

### Métricas de Reflexión
- Total de reflexiones
- Reflexiones exitosas
- Patrones extraídos
- Score promedio de calidad
- Tasa de alucinaciones

### Métricas de Curaduría
- Total de interacciones
- Patrones agregados/removidos
- Playbooks actualizados
- Curadurías exitosas/fallidas
- Tiempo de procesamiento

### Métricas de Integración
- Queries procesadas
- Contexto ACE generado
- Reflexiones realizadas
- Playbooks actualizados
- Calidad promedio del contexto

## 🔧 Configuración

### Configuración del Generador
```python
generator = ACEGenerator(
    playbooks_dir="backend/data/playbooks",
    max_context_tokens=4000,
    similarity_threshold=0.3
)
```

### Configuración del Reflector
```python
reflector = ACEReflector(
    model_client=None,  # Cliente LLM
    reflection_threshold=0.7,
    sampling_rate=0.1  # 10% sampling
)
```

### Configuración del Curator
```python
curator = ACECurator(
    playbooks_dir="backend/data/playbooks",
    persistence_interval=100,
    filtering_threshold=0.5,
    max_patterns_per_domain=1000
)
```

## 🧪 Testing

### Tests Unitarios
```bash
# Ejecutar tests de FASE 2
python backend/test_fase2.py
```

### Tests Específicos
```python
# Test de playbooks
from backend.ace.playbook import PlaybookManager
manager = PlaybookManager()
playbook = manager.create_playbook("python")

# Test de generador
from backend.ace.generator import ACEGenerator
generator = ACEGenerator()
result = generator.generate_context("How to create a Python function?")

# Test de reflector
from backend.ace.reflector import ACEReflector
reflector = ACEReflector()
reflection = reflector.reflect("query", "response", domain="python")
```

## 📁 Estructura de Archivos

```
backend/ace/
├── __init__.py              # Inicialización del módulo
├── playbook.py              # Sistema de playbooks
├── generator.py             # ACE Generator
├── reflector.py             # ACE Reflector
├── curator.py               # ACE Curator
└── integration.py           # Integración completa

backend/data/playbooks/      # Playbooks JSON
├── playbook_<id>.json       # Playbooks por dominio
└── ...

backend/test_fase2.py        # Tests de FASE 2
```

## 🎯 Próximos Pasos (FASE 3)

1. **E2B Integration** - Ejecución de código en sandboxes
2. **Code Detection** - Detección automática de código en respuestas
3. **Execution Loop** - Loop multi-round con corrección automática
4. **Error Mapping** - Mapeo de errores comunes y estrategias de corrección

## 📊 Estado Actual

✅ **Completado:**
- Sistema de playbooks completo
- ACE Generator con detección de dominio
- ACE Reflector con análisis multi-dimensional
- ACE Curator con filtrado automático
- Integración completa con CAG
- Procesamiento background con RQ
- Tests completos y documentación

🔄 **En Progreso:**
- Optimizaciones de performance
- Integración con modelos reales
- Población de playbooks de producción

📋 **Pendiente:**
- E2B Integration (FASE 3)
- Agentes Persistentes (FASE 4)
- Sistema de Metadata (FASE 5)

## 🤝 Contribución

Para contribuir al ACE Framework:

1. Fork del repositorio
2. Crear branch para feature
3. Implementar cambios con tests
4. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

**FASE 2 completada exitosamente** 🎉

El ACE Framework está listo para la integración con E2B en la FASE 3.
