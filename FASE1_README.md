# FASE 1: Componentes Core - Sistema de Agentes IA Avanzado Capibara6

## 🎯 Objetivo

Implementar los componentes fundamentales del sistema de agentes IA avanzado, incluyendo routing inteligente, Context-Aware Generation (CAG) y RAG jerárquico.

## 📋 Componentes Implementados

### 1. 🛣️ Router Inteligente (`backend/core/router.py`)

**RouterModel20B** - Decide cuándo escalar de modelo 20B a 120B basado en:
- **Complejidad de query** (longitud, términos técnicos, estructura sintáctica)
- **Confianza de dominio** (similitud con dominios conocidos)
- **Umbrales configurables** (complejidad: 0.7, confianza: 0.6)

**Características:**
- Análisis semántico con embeddings
- Dominios predefinidos (programming, science, business, general)
- Logging detallado de decisiones
- Sistema de umbrales adaptativos

### 2. 🧠 Sistema de Embeddings (`backend/core/embeddings.py`)

**EmbeddingModel** - Modelo de embeddings con:
- Soporte para sentence-transformers (all-MiniLM-L6-v2)
- Caché persistente de embeddings
- Funciones de similitud y clustering
- Optimizaciones para producción

**DomainEmbeddingAnalyzer** - Análisis especializado:
- Detección de dominios (programming, data_science, web_development, etc.)
- Cálculo de confianza de dominio
- Análisis de similitud semántica

### 3. ⚙️ Sistema de Umbrales (`backend/core/thresholds.py`)

**ThresholdManager** - Gestión de umbrales:
- Configuración persistente en JSON
- Validación de valores
- Actualización dinámica

**AdaptiveThresholds** - Umbrales adaptativos:
- Ajuste automático basado en performance
- Análisis de métricas históricas
- Optimización continua

### 4. 📚 CAG - Context-Aware Generation

#### StaticCache (`backend/core/cag/static_cache.py`)
- Base de conocimiento pre-cargada
- Índices por categoría, tags y contenido
- Recuperación rápida con límites de tokens
- Caché persistente

#### DynamicContext (`backend/core/cag/dynamic_context.py`)
- Contexto evolutivo basado en conversaciones
- Proveedores de contexto registrables
- Filtros de relevancia y recencia
- TTL configurable

#### AwarenessGate (`backend/core/cag/awareness_gate.py`)
- Decisión inteligente de fuentes de contexto
- Análisis de patrones de query
- Asignación de presupuesto de tokens
- Estrategias de expansión

#### MiniCAG (`backend/core/cag/mini_cag.py`)
- Optimizado para modelo 20B (8K tokens)
- Límites específicos por fuente
- Decisión de escalación a FullCAG
- Métricas de performance

#### FullCAG (`backend/core/cag/full_cag.py`)
- Optimizado para modelo 120B (32K tokens)
- Integración completa con RAG
- Truncamiento inteligente
- Análisis de complejidad

### 5. 🔍 RAG Jerárquico

#### VectorStore (`backend/core/rag/vector_store.py`)
- Wrapper unificado para FAISS/ChromaDB
- Implementación básica como fallback
- Gestión de documentos y metadata
- Búsqueda con filtros

#### MiniRAG (`backend/core/rag/mini_rag.py`)
- Búsqueda rápida con timeout <50ms
- Caché de queries recientes
- Optimizado para latencia
- Métricas de performance

#### FullRAG (`backend/core/rag/full_rag.py`)
- Búsqueda profunda guiada
- Expansión de queries (sinónimos, conceptos, contexto)
- Ranking inteligente de resultados
- Integración con MiniRAG

#### GuidedSearch (`backend/core/rag/guided_search.py`)
- Coordinación entre MiniRAG y FullRAG
- Criterios de expansión automática
- Combinación inteligente de resultados
- Estrategias de búsqueda

### 6. 📊 Sistema de Logging (`backend/utils/logging_config.py`)

**Capibara6Logger** - Logging centralizado:
- Loggers específicos por componente
- Rotación automática de archivos
- Logging estructurado (JSON)
- Métricas de logging

## 🚀 Uso del Sistema

### Instalación

```bash
# Instalar dependencias
pip install -r backend/requirements.txt

# Crear directorios necesarios
mkdir -p backend/data/{knowledge_base,vector_store,logs,playbooks}
```

### Población de Datos

```bash
# Poblar RAG con 10K documentos de muestra
python backend/scripts/populate_rag.py --count 10000

# Crear conocimiento base de ejemplo
python backend/core/cag/static_cache.py
```

### Inicio del Sistema

```bash
# Iniciar sistema completo
python backend/start_system.py

# Ejecutar tests de FASE 1
python backend/test_fase1.py
```

### Uso Programático

```python
from backend.start_system import Capibara6System

# Crear e iniciar sistema
system = Capibara6System()
system.start()

# Procesar query
response = system.process_query("¿Qué es Python?")
print(f"Modelo usado: {response['model_used']}")
print(f"Latencia: {response['total_latency_ms']:.1f}ms")
print(f"Contexto: {response['context']}")

# Detener sistema
system.stop()
```

## 📈 Métricas y Monitoreo

### Métricas de Router
- Decisiones de escalación (20B vs 120B)
- Complejidad promedio de queries
- Confianza de dominio
- Latencia de decisión

### Métricas de CAG
- Tokens utilizados por fuente
- Latencia de generación de contexto
- Uso de fuentes (static, dynamic, RAG)
- Efectividad de escalación

### Métricas de RAG
- Latencia de búsqueda (MiniRAG <50ms)
- Tasa de expansión a FullRAG
- Relevancia de resultados
- Hit rate de caché

## 🔧 Configuración

### Umbrales de Router
```json
{
  "complexity_threshold": 0.7,
  "domain_confidence_threshold": 0.6,
  "max_latency_20b_ms": 2000,
  "max_latency_120b_ms": 10000
}
```

### Límites de Tokens CAG
- **MiniCAG**: 8K tokens total
  - Static Cache: 40% (3.2K)
  - Dynamic Context: 30% (2.4K)
  - RAG: 30% (2.4K)

- **FullCAG**: 32K tokens total
  - Static Cache: 25% (8K)
  - Dynamic Context: 20% (6.4K)
  - MiniRAG: 20% (6.4K)
  - FullRAG: 35% (11.2K)

## 🧪 Testing

### Tests Unitarios
```bash
# Ejecutar tests específicos
python -m pytest backend/tests/test_router.py -v
python -m pytest backend/tests/test_cag.py -v
python -m pytest backend/tests/test_rag.py -v
```

### Tests de Integración
```bash
# Test completo de FASE 1
python backend/test_fase1.py
```

### Benchmarks
- **Router**: <10ms decisión
- **MiniRAG**: <50ms búsqueda
- **FullRAG**: <200ms búsqueda profunda
- **MiniCAG**: <100ms generación contexto
- **FullCAG**: <300ms generación contexto

## 📁 Estructura de Archivos

```
backend/
├── core/
│   ├── router.py              # Router inteligente
│   ├── embeddings.py          # Modelo de embeddings
│   ├── thresholds.py          # Sistema de umbrales
│   ├── cag/                   # Context-Aware Generation
│   │   ├── static_cache.py
│   │   ├── dynamic_context.py
│   │   ├── awareness_gate.py
│   │   ├── mini_cag.py
│   │   └── full_cag.py
│   └── rag/                   # RAG jerárquico
│       ├── vector_store.py
│       ├── mini_rag.py
│       ├── full_rag.py
│       └── guided_search.py
├── utils/
│   └── logging_config.py      # Sistema de logging
├── scripts/
│   └── populate_rag.py        # Población de datos
├── data/                      # Datos del sistema
│   ├── knowledge_base/        # Conocimiento estático
│   ├── vector_store/          # Índices vectoriales
│   ├── logs/                  # Archivos de log
│   └── playbooks/             # Playbooks ACE (FASE 2)
├── start_system.py            # Sistema principal
├── test_fase1.py              # Tests de FASE 1
└── requirements.txt           # Dependencias
```

## 🎯 Próximos Pasos (FASE 2)

1. **ACE Framework** - Sistema de evolución adaptativa
2. **E2B Integration** - Ejecución de código en sandboxes
3. **Persistent Agents** - Agentes con memoria y especialización
4. **Metadata System** - Captura y análisis de métricas

## 📊 Estado Actual

✅ **Completado:**
- Router inteligente con embeddings
- Sistema CAG completo (Static, Dynamic, Awareness, Mini, Full)
- RAG jerárquico (VectorStore, MiniRAG, FullRAG, GuidedSearch)
- Sistema de logging centralizado
- Tests y documentación

🔄 **En Progreso:**
- Optimizaciones de performance
- Integración con modelos reales
- Población de datos de producción

📋 **Pendiente:**
- ACE Framework (FASE 2)
- E2B Integration (FASE 3)
- Agentes Persistentes (FASE 4)

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear branch para feature
3. Implementar cambios con tests
4. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

**FASE 1 completada exitosamente** 🎉

El sistema de componentes core está listo para la integración con el ACE Framework en la FASE 2.
