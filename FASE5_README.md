# FASE 5: Metadata System - Sistema Completo de Captura y Procesamiento de Métricas

## 🎯 Objetivo

Implementar el sistema completo de metadata que incluye:
- **Captura completa** de métricas de todos los componentes del sistema
- **TimescaleDB** con esquemas optimizados y compresión automática
- **Pipeline de agregación** diaria con métricas derivadas
- **Detección de anomalías** automática con alertas
- **Reportes semanales** y dashboards de monitoreo
- **Integración completa** con todos los componentes del sistema

## 📋 Componentes Implementados

### 1. 📊 Metrics Collector (`backend/metadata/metrics_collector.py`)

**Sistema de Recolección de Métricas:**
- **8 tipos de métricas**: Routing, Memory, Attention, Compute, Execution, Agent Evolution, RAG, System
- **Buffer circular** con límite configurable (10,000 métricas por defecto)
- **Flush automático** cada 30 segundos
- **Threading asíncrono** para no bloquear el sistema principal
- **Manejo de errores** robusto con estadísticas

**Tipos de Métricas Implementadas:**
- **RoutingMetrics**: Complejidad, confianza, modelo seleccionado, tiempo de routing
- **MemoryMetrics**: Operaciones de memoria, compresión, cache hits, importancia
- **AttentionMetrics**: Patrones de atención, entropía, diversidad, tiempo de cómputo
- **ComputeMetrics**: Utilización GPU/CPU, throughput, latencia, tokens procesados
- **ExecutionMetrics**: Ejecución E2B, correcciones, errores, tiempo de ejecución
- **AgentEvolutionMetrics**: Evolución de agentes, graduación, expertise, colaboraciones
- **RAGMetrics**: Retrieval, relevancia, documentos, tiempo de búsqueda
- **SystemMetrics**: CPU, memoria, disco, conexiones, throughput del sistema

**Características:**
- **Buffer thread-safe** con queue.Queue
- **Flush worker** en thread separado
- **Estadísticas detalladas** de recolección
- **Manejo de overflow** del buffer
- **Métricas compuestas** y simples

### 2. 🔗 Metrics Integration (`backend/metadata/metrics_integration.py`)

**Integración con Todos los Componentes:**
- **Context managers** para tracking automático
- **Decoradores** para métricas de funciones
- **Integración transparente** con el código existente
- **Tracking automático** de tiempo y recursos

**Integraciones Implementadas:**
- **Routing**: Tracking de decisiones de routing con contexto
- **Memory**: Operaciones de lectura/escritura con cache hits
- **Compute**: Inferencia de modelos con métricas de GPU/CPU
- **Execution**: Ejecución E2B con correcciones y errores
- **Agent Evolution**: Creación, entrenamiento, graduación de agentes
- **RAG**: Retrieval con relevancia y tiempo de búsqueda
- **System**: Métricas del sistema operativo y aplicación

**Context Managers:**
```python
# Tracking de routing
with integration.track_routing("query_001", "Python optimization", "optimization"):
    # Código de routing
    pass

# Tracking de memoria
with integration.track_memory_read("agent_001", "knowledge") as cache_hit:
    # Código de lectura de memoria
    pass

# Tracking de cómputo
with integration.track_model_inference("120B", batch_size=1) as (tokens, seq_len):
    # Código de inferencia
    pass
```

### 3. 🗄️ TimescaleDB Manager (`backend/metadata/timescaledb_manager.py`)

**Gestión Completa de TimescaleDB:**
- **7 tablas de métricas** con esquemas optimizados
- **Hypertables** para escalabilidad temporal
- **Compresión automática** configurable por tabla
- **Índices optimizados** para consultas rápidas
- **Políticas de retención** automáticas

**Esquemas de Tablas:**
```sql
-- Routing Metrics
CREATE TABLE metrics.routing_metrics (
    time TIMESTAMPTZ NOT NULL,
    query_id TEXT,
    complexity_score REAL,
    confidence_score REAL,
    model_selected TEXT,
    routing_time_ms INTEGER,
    -- ... más campos
);

-- Memory Metrics
CREATE TABLE metrics.memory_metrics (
    time TIMESTAMPTZ NOT NULL,
    agent_id TEXT,
    memory_type TEXT,
    memory_operation TEXT,
    memory_size_bytes BIGINT,
    -- ... más campos
);

-- Compute Metrics
CREATE TABLE metrics.compute_metrics (
    time TIMESTAMPTZ NOT NULL,
    model_id TEXT,
    operation_type TEXT,
    gpu_utilization_percent REAL,
    throughput_tokens_per_sec REAL,
    -- ... más campos
);
```

**Políticas de Compresión:**
- **Routing/Memory/Compute/Execution/RAG**: 30 días
- **System Metrics**: 7 días (más frecuente)
- **Compresión automática** con TimescaleDB
- **Retención configurable** por tipo de métrica

**Características:**
- **Conexión automática** con reintentos
- **Verificación de extensión** TimescaleDB
- **Creación automática** de hypertables
- **Inserción en lote** para eficiencia
- **Consultas optimizadas** con índices

### 4. 🔄 Metrics Pipeline (`backend/metadata/metrics_pipeline.py`)

**Pipeline de Procesamiento de Métricas:**
- **Agregación diaria** automática
- **Métricas derivadas** calculadas
- **Detección de anomalías** en tiempo real
- **Reportes automáticos** generados

**Agregaciones Implementadas:**
- **Por tabla**: Routing, Memory, Compute, Execution, RAG, System
- **Por tiempo**: 1 hora, 1 día, 1 semana
- **Por métrica**: avg, sum, min, max, count, p50, p95, p99
- **Por grupo**: modelo, agente, dominio, tipo de operación

**Métricas Derivadas:**
- **System Health Score**: 100 - (CPU + Memory + Error Rate) / 3
- **Agent Efficiency Score**: Success Rate × (1000 / Execution Time)
- **Routing Accuracy Score**: Confidence × (1 - |Complexity - 0.7|)

**Detección de Anomalías:**
- **Spikes**: Valores por encima del umbral
- **Drops**: Valores por debajo del umbral
- **Trend Changes**: Cambios en tendencias
- **Outliers**: Valores atípicos estadísticamente

**Configuración de Anomalías:**
```python
anomaly_configs = {
    'system_metrics.cpu_usage_percent.avg': {
        'threshold': 80.0,
        'anomaly_type': 'spike',
        'severity': 'high'
    },
    'system_metrics.memory_usage_percent.avg': {
        'threshold': 90.0,
        'anomaly_type': 'spike',
        'severity': 'critical'
    }
}
```

### 5. 🏗️ Metadata System (`backend/metadata/metadata_system.py`)

**Sistema Completo de Metadata:**
- **Integración unificada** de todos los componentes
- **API centralizada** para tracking de métricas
- **Health checks** automáticos
- **Gestión de estado** del sistema
- **Instancia global** para uso en toda la aplicación

**API Principal:**
```python
# Inicializar sistema
metadata_system = MetadataSystem()
await metadata_system.initialize()
await metadata_system.start()

# Tracking de métricas
metadata_system.track_routing_decision(
    "query_001", 0.8, 0.9, "120B", 50, "python"
)

metadata_system.track_memory_operation(
    "agent_001", "knowledge", "write", 1024, 256, 10
)

metadata_system.track_compute_operation(
    "120B", "inference", 1, 1000, 1000, 2000, 85.0, 8000.0
)

# Health check
health = await metadata_system.health_check()

# Estadísticas
stats = metadata_system.get_system_stats()
```

**Sistema Global:**
```python
# Inicializar sistema global
metadata_system = initialize_metadata_system()
await start_metadata_system()

# Usar en cualquier parte de la aplicación
global_system = get_metadata_system()
global_system.track_system_metrics(cpu_usage_percent=25.0)

# Detener sistema
await stop_metadata_system()
```

## 🚀 Configuración y Uso

### Configuración de TimescaleDB

```bash
# Instalar TimescaleDB
sudo apt-get install timescaledb-2-postgresql-14

# Crear base de datos
createdb capibara6_metrics

# Conectar y configurar
psql capibara6_metrics
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

### Variables de Entorno

```bash
# TimescaleDB
export TIMESCALEDB_HOST=localhost
export TIMESCALEDB_PORT=5432
export TIMESCALEDB_DATABASE=capibara6_metrics
export TIMESCALEDB_USERNAME=postgres
export TIMESCALEDB_PASSWORD=password

# Metrics Collector
export METRICS_BUFFER_SIZE=10000
export METRICS_FLUSH_INTERVAL=30
export ENABLE_SYSTEM_METRICS=true
```

### Uso Básico

```python
from backend.metadata.metadata_system import initialize_metadata_system, start_metadata_system

# Inicializar sistema
metadata_system = initialize_metadata_system()
await start_metadata_system()

# El sistema está listo para usar
```

### Integración con Componentes Existentes

```python
# En el router
from backend.metadata.metadata_system import get_metadata_system

def route_query(query, complexity, confidence):
    metadata_system = get_metadata_system()
    
    start_time = time.time()
    model = select_model(complexity, confidence)
    routing_time = int((time.time() - start_time) * 1000)
    
    # Track métricas
    metadata_system.track_routing_decision(
        query_id=generate_id(),
        complexity_score=complexity,
        confidence_score=confidence,
        model_selected=model,
        routing_time_ms=routing_time
    )
    
    return model

# En el agente
def process_query(agent_id, query):
    metadata_system = get_metadata_system()
    
    # Track evolución del agente
    metadata_system.track_agent_evolution(
        agent_id=agent_id,
        domain="python",
        evolution_event="interaction",
        interactions_count=1,
        success_rate=0.8,
        graduation_score=0.7
    )
```

## 📊 Métricas y Monitoreo

### Métricas de Routing
- Tiempo de routing (p50, p95, p99)
- Complejidad promedio por dominio
- Confianza promedio por modelo
- Distribución de modelos seleccionados
- Tasa de éxito de routing

### Métricas de Memoria
- Operaciones de memoria por agente
- Tasa de cache hit por tipo
- Compresión de memoria por agente
- Utilización de memoria por dominio
- Tiempo de operaciones de memoria

### Métricas de Cómputo
- Utilización GPU/CPU por modelo
- Throughput de tokens por segundo
- Latencia de inferencia (p50, p95, p99)
- Memoria GPU utilizada
- Eficiencia de cómputo

### Métricas de Ejecución E2B
- Tasa de éxito por lenguaje
- Tiempo de ejecución promedio
- Correcciones aplicadas por agente
- Errores más comunes
- Utilización de recursos

### Métricas de Evolución de Agentes
- Tasa de graduación por dominio
- Score de graduación promedio
- Interacciones por agente
- Expertise por dominio
- Colaboraciones exitosas

### Métricas de RAG
- Tiempo de retrieval por tipo
- Relevancia de documentos
- Estrategias de búsqueda más efectivas
- Contexto generado por query
- Eficiencia de búsqueda

### Métricas del Sistema
- CPU, memoria, disco utilizados
- Conexiones activas
- Throughput de requests
- Tasa de errores
- Tiempo de respuesta promedio

## 🔧 Configuración Avanzada

### Personalización de Agregaciones

```python
# Configurar agregaciones personalizadas
aggregator = MetricsAggregator(timescaledb_manager)

# Agregar nueva configuración
aggregator.aggregation_configs['custom_metrics'] = {
    'aggregations': ['avg', 'p95', 'p99'],
    'group_by': ['custom_field'],
    'time_buckets': ['1 hour', '1 day'],
    'metrics': ['custom_metric']
}
```

### Configuración de Anomalías

```python
# Personalizar detección de anomalías
anomaly_configs = {
    'custom_metric.avg': {
        'threshold': 100.0,
        'anomaly_type': 'spike',
        'severity': 'medium'
    }
}

# Agregar al pipeline
pipeline.aggregator.anomaly_configs.update(anomaly_configs)
```

### Políticas de Compresión

```python
# Configurar compresión personalizada
timescaledb_manager.compression_policies = {
    'routing_metrics': 15,  # 15 días
    'memory_metrics': 45,   # 45 días
    'system_metrics': 3     # 3 días
}
```

## 🧪 Testing

### Tests Unitarios
```bash
# Ejecutar tests de FASE 5
python backend/test_fase5.py
```

### Tests Específicos
```python
# Test de collector
python -c "from backend.test_fase5 import test_metrics_collector; test_metrics_collector()"

# Test de integración
python -c "from backend.test_fase5 import test_metrics_integration; test_metrics_integration()"

# Test de pipeline
python -c "import asyncio; from backend.test_fase5 import test_metrics_pipeline; asyncio.run(test_metrics_pipeline())"
```

### Tests de Integración
```python
# Test completo del sistema
metadata_system = MetadataSystem()
await metadata_system.initialize()
await metadata_system.start()

# Simular métricas
metadata_system.track_routing_decision("test_001", 0.8, 0.9, "120B", 50)
metadata_system.track_system_metrics(cpu_usage_percent=25.0)

# Verificar health
health = await metadata_system.health_check()
assert health['status'] == 'healthy'
```

## 📁 Estructura de Archivos

```
backend/metadata/
├── __init__.py              # Inicialización del módulo
├── metrics_collector.py     # Recolección de métricas
├── metrics_integration.py   # Integración con componentes
├── timescaledb_manager.py   # Gestión de TimescaleDB
├── metrics_pipeline.py      # Pipeline de procesamiento
└── metadata_system.py       # Sistema completo

backend/test_fase5.py        # Tests completos de FASE 5
```

## 🎯 Próximos Pasos (FASE 6)

1. **Fine-tuning Pipeline** - Consolidación de playbooks y datasets
2. **LoRA/QLoRA** - Configuración de fine-tuning eficiente
3. **Distributed Training** - Entrenamiento distribuido en TPU
4. **Evaluation Benchmarks** - HumanEval, MMLU, AppWorld
5. **A/B Testing Framework** - Testing y rollback automático

## 📊 Estado Actual

✅ **Completado:**
- Metrics Collector con 8 tipos de métricas
- Metrics Integration con context managers
- TimescaleDB Manager con 7 tablas optimizadas
- Metrics Pipeline con agregación y anomalías
- Metadata System completo con API unificada
- Tests completos y documentación

🔄 **En Progreso:**
- Configuración de TimescaleDB en producción
- Dashboards de Grafana
- Alertas automáticas

📋 **Pendiente:**
- Fine-tuning Pipeline (FASE 6)
- Evaluation Benchmarks (FASE 6)
- Advanced Optimizations (FASE 7)
- Production Deployment (FASE 8)

## 🤝 Contribución

Para contribuir al sistema de metadata:

1. Fork del repositorio
2. Crear branch para feature
3. Implementar cambios con tests
4. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

**FASE 5 completada exitosamente** 🎉

El sistema de metadata está listo para la integración con el Fine-tuning Pipeline en la FASE 6.
