# FASE 4: Persistent Agent Memory - Sistema de Agentes Persistentes

## 🎯 Objetivo

Implementar el sistema completo de agentes persistentes que incluye:
- **Memoria persistente** con compresión inteligente (128K tokens)
- **Sistema de graduación** con criterios de 85% success rate
- **Especialización por dominios** (Python/SQL/Debug/ML/API)
- **Colaboración entre agentes** para resolución de problemas complejos
- **Base de datos completa** con esquemas optimizados

## 📋 Componentes Implementados

### 1. 🗄️ Database Manager (`backend/agents/database.py`)

**Esquema de Base de Datos Completo:**
- **Agentes**: Información básica, estado, métricas de graduación
- **Memorias**: Contenido, tipo, importancia, acceso
- **Interacciones**: Queries, respuestas, calidad, tiempo de ejecución
- **Graduaciones**: Registro de agentes graduados con métricas
- **Colaboraciones**: Interacciones entre agentes

**Características:**
- **SQLite/PostgreSQL** compatible
- **Índices optimizados** para consultas rápidas
- **Relaciones foreign key** para integridad
- **Metadata JSON** para flexibilidad
- **Estadísticas automáticas** de la base de datos

**Tablas principales:**
```sql
agents (id, domain, status, created_at, last_updated, total_interactions, success_rate, graduation_score, memory_tokens, max_memory_tokens, metadata)
agent_memories (id, agent_id, memory_type, content, tokens, importance_score, created_at, last_accessed, access_count, metadata)
agent_interactions (id, agent_id, query, response, success, quality_score, execution_time_ms, corrections_applied, context_used, created_at, metadata)
agent_graduations (id, agent_id, graduation_date, final_score, interactions_count, success_rate, memory_compression_ratio, playbook_contributions, metadata)
agent_collaborations (id, primary_agent_id, secondary_agent_id, collaboration_type, success, quality_score, created_at, metadata)
```

### 2. 🧠 Memory Manager (`backend/agents/memory_manager.py`)

**MemoryCompressor** - Compresión inteligente de memoria:
- **Compresión por tipo**: Conversación, conocimiento, habilidades, experiencia, patrones
- **Estrategias específicas** para cada tipo de memoria
- **Límite de 128K tokens** con compresión automática
- **Preservación de información crítica** durante compresión

**MemoryManager** - Gestión completa de memoria:
- **Cache inteligente** para acceso rápido
- **Búsqueda por relevancia** basada en contenido
- **Tracking de acceso** y importancia
- **Compresión automática** cuando se excede el límite

**Tipos de memoria:**
- **CONVERSATION**: Diálogos y interacciones
- **KNOWLEDGE**: Conocimiento factual y conceptos
- **SKILL**: Habilidades y técnicas
- **EXPERIENCE**: Experiencias y lecciones aprendidas
- **PATTERN**: Patrones y soluciones reutilizables

**Estrategias de compresión:**
- **Conversación**: Extracción de puntos clave
- **Conocimiento**: Filtrado de oraciones importantes
- **Habilidades**: Resumen de pasos y técnicas
- **Experiencia**: Extracción de resultados y lecciones
- **Patrones**: Identificación de patrones y ejemplos

### 3. 🎓 Graduation System (`backend/agents/graduation_system.py`)

**GraduationCriteria** - Criterios de graduación:
- **85% success rate** mínimo
- **100 interacciones** mínimo
- **7.0 quality score** promedio
- **30% memory utilization** mínimo
- **30 días máximo** para graduarse
- **80% domain expertise** mínimo

**GraduationEvaluator** - Evaluación de agentes:
- **Cálculo de métricas** completas del agente
- **Evaluación de criterios** automática
- **Score de graduación** ponderado
- **Recomendaciones** para mejora
- **Estadísticas de evaluación** detalladas

**GraduationSystem** - Sistema completo:
- **Evaluación masiva** de todos los agentes
- **Graduación automática** cuando se cumplen criterios
- **Creación de playbooks** basados en experiencias
- **Registro de graduaciones** con métricas completas

**Métricas de graduación:**
- Success rate, quality score, domain expertise
- Memory utilization, time efficiency
- Interaction count, collaboration success
- Playbook contributions, knowledge extraction

### 4. 🌐 Domain System (`backend/agents/domain_system.py`)

**DomainManager** - Gestión de dominios:
- **6 dominios especializados**: Python, SQL, JavaScript, Debug, ML, API
- **Prompts específicos** por dominio y tipo
- **Cálculo de expertise** basado en interacciones
- **Detección automática** de dominio por contenido
- **Estadísticas por dominio** detalladas

**CollaborationManager** - Colaboración entre agentes:
- **5 tipos de colaboración**: Knowledge sharing, problem solving, code review, mentoring, pair programming
- **Búsqueda inteligente** de colaboradores
- **Gestión de solicitudes** de colaboración
- **Tracking de resultados** y calidad
- **Estadísticas de colaboración** completas

**Dominios implementados:**
- **Python**: Sintaxis, OOP, librerías, frameworks, testing
- **SQL**: Optimización, diseño, performance, administración
- **JavaScript**: ES6+, Node.js, frameworks, async programming
- **Debug**: Análisis sistemático, herramientas, profiling
- **ML**: Algoritmos, preprocessing, evaluación, deployment
- **API**: RESTful design, documentación, seguridad, microservicios

**Prompts por dominio:**
- **System prompt**: Especialización y capacidades
- **Generation prompt**: Generación de soluciones
- **Review prompt**: Revisión y análisis de código

### 5. 🤖 Agent System (`backend/agents/agent_system.py`)

**PersistentAgent** - Agente individual:
- **Procesamiento de queries** con contexto enriquecido
- **Generación de respuestas** usando prompts del dominio
- **Evaluación de calidad** automática
- **Gestión de memoria** automática
- **Colaboración opcional** con otros agentes
- **Tracking de estadísticas** detalladas

**AgentSystem** - Sistema completo:
- **Creación y gestión** de agentes
- **Carga desde base de datos** automática
- **Evaluación de graduaciones** masiva
- **Estadísticas consolidadas** del sistema
- **Integración completa** de todos los componentes

**Características del agente:**
- **Memoria persistente** con compresión inteligente
- **Especialización por dominio** con prompts específicos
- **Colaboración inteligente** con otros agentes
- **Evaluación de calidad** automática
- **Tracking de métricas** para graduación
- **Gestión de contexto** enriquecido

## 🚀 Configuración y Uso

### Configuración de Base de Datos

```python
from backend.agents.database import DatabaseManager

# Crear manager de base de datos
db_manager = DatabaseManager("backend/data/agents.db")

# La base de datos se inicializa automáticamente con el esquema completo
```

### Creación de Agentes

```python
from backend.agents.agent_system import AgentSystem
from backend.agents.domain_system import DomainType

# Crear sistema de agentes
agent_system = AgentSystem()

# Crear agente especializado
python_agent = agent_system.create_agent(DomainType.PYTHON, "python_expert_001")
sql_agent = agent_system.create_agent(DomainType.SQL, "sql_expert_001")
ml_agent = agent_system.create_agent(DomainType.ML, "ml_expert_001")
```

### Procesamiento de Queries

```python
# Procesar query simple
result = python_agent.process_query(
    query="How to create a Python decorator?",
    context="Learning advanced Python concepts",
    user_intent="Understand decorators"
)

print(f"Response: {result['response']}")
print(f"Quality: {result['quality_score']}")
print(f"Success: {result['success']}")

# Procesar query con colaboración
result_with_collab = python_agent.process_query(
    query="Complex Python optimization problem",
    context="Performance optimization",
    user_intent="Learn optimization techniques",
    require_collaboration=True
)
```

### Evaluación de Graduación

```python
# Evaluar todos los agentes
evaluation_results = agent_system.evaluate_graduations()

for result in evaluation_results:
    if result['eligible']:
        print(f"Agent {result['agent_id']} is ready for graduation!")
        print(f"Score: {result['graduation_score']:.2f}")
        
        # Graduar agente
        success = agent_system.graduate_agent(result['agent_id'])
        print(f"Graduation successful: {success}")
```

### Gestión de Memoria

```python
from backend.agents.memory_manager import MemoryManager, MemoryType

# Obtener memorias del agente
memories = python_agent.get_memories(MemoryType.KNOWLEDGE, limit=10)

for memory in memories:
    print(f"Memory: {memory.content[:100]}...")
    print(f"Importance: {memory.importance_score}")
    print(f"Access count: {memory.access_count}")

# Obtener memorias relevantes
relevant = python_agent.memory_manager.get_relevant_memories(
    python_agent.agent_id, "Python functions", limit=5
)
```

### Colaboración entre Agentes

```python
from backend.agents.domain_system import CollaborationType

# Solicitar colaboración
collaboration_request = agent_system.collaboration_manager.request_collaboration(
    requester_agent_id="python_expert_001",
    query="How to optimize database queries in Python?",
    context="Performance optimization",
    collaboration_type=CollaborationType.KNOWLEDGE_SHARING,
    target_domain=DomainType.SQL
)

if collaboration_request:
    print(f"Collaboration requested with {collaboration_request.target_agent_id}")
```

## 📊 Métricas y Monitoreo

### Métricas de Agentes
- Total de interacciones
- Tasa de éxito
- Score de graduación
- Utilización de memoria
- Expertise por dominio
- Colaboraciones exitosas

### Métricas de Memoria
- Total de memorias
- Tokens utilizados
- Compresiones realizadas
- Tokens ahorrados
- Memorias pruned/merged
- Cache hit rate

### Métricas de Graduación
- Agentes evaluados
- Agentes elegibles
- Agentes graduados
- Score promedio de graduación
- Criterios más/menos cumplidos
- Playbooks creados

### Métricas de Dominio
- Agentes por dominio
- Expertise promedio por dominio
- Colaboraciones por dominio
- Prompts más utilizados
- Dominios más activos

### Métricas de Colaboración
- Solicitudes de colaboración
- Colaboraciones completadas
- Tasa de éxito de colaboraciones
- Score promedio de calidad
- Tipos de colaboración más exitosos

## 🔧 Configuración Avanzada

### Criterios de Graduación Personalizados

```python
from backend.agents.graduation_system import GraduationCriteria

# Personalizar criterios
custom_criteria = GraduationCriteria(
    min_success_rate=0.90,  # 90% en lugar de 85%
    min_interactions=150,   # 150 en lugar de 100
    min_quality_score=8.0,  # 8.0 en lugar de 7.0
    min_memory_utilization=0.4,  # 40% en lugar de 30%
    max_graduation_time_days=45,  # 45 días en lugar de 30
    min_domain_expertise=0.85  # 85% en lugar de 80%
)

# Usar criterios personalizados
graduation_system = GraduationSystem(db_manager, memory_manager, custom_criteria)
```

### Configuración de Memoria

```python
from backend.agents.memory_manager import MemoryManager

# Configurar límite de memoria personalizado
memory_manager = MemoryManager(db_manager, max_tokens=256000)  # 256K tokens

# Configurar cache
memory_manager.clear_cache()  # Limpiar cache
memory_manager.clear_cache("agent_id")  # Limpiar cache específico
```

### Prompts Personalizados por Dominio

```python
from backend.agents.domain_system import DomainManager, DomainType

# Agregar prompt personalizado
domain_manager = DomainManager(db_manager)
domain_manager.domain_prompts[DomainType.PYTHON]['custom_prompt'] = """
Custom prompt for Python agent:
- Focus on clean code
- Emphasize testing
- Include performance considerations
"""
```

## 🧪 Testing

### Tests Unitarios
```bash
# Ejecutar tests de FASE 4
python backend/test_fase4.py
```

### Tests Específicos
```python
# Test de base de datos
python -c "from backend.test_fase4 import test_database_manager; test_database_manager()"

# Test de memoria
python -c "from backend.test_fase4 import test_memory_manager; test_memory_manager()"

# Test de graduación
python -c "from backend.test_fase4 import test_graduation_system; test_graduation_system()"
```

### Tests de Integración
```python
# Test completo del sistema
agent_system = AgentSystem()
agent = agent_system.create_agent(DomainType.PYTHON)

# Simular muchas interacciones
for i in range(200):
    result = agent.process_query(f"Python question {i}")
    assert result['success']

# Evaluar graduación
evaluation = agent_system.evaluate_graduations()
assert len(evaluation) > 0
```

## 📁 Estructura de Archivos

```
backend/agents/
├── __init__.py              # Inicialización del módulo
├── database.py              # Esquema y gestión de base de datos
├── memory_manager.py        # Gestión de memoria con compresión
├── graduation_system.py     # Sistema de graduación de agentes
├── domain_system.py         # Dominios y colaboración
└── agent_system.py          # Sistema completo de agentes

backend/data/
└── agents.db                # Base de datos SQLite de agentes

backend/test_fase4.py        # Tests completos de FASE 4
```

## 🎯 Próximos Pasos (FASE 5)

1. **Metadata System** - Captura completa de métricas
2. **TimescaleDB** - Base de datos de series temporales
3. **Grafana Dashboards** - Visualización de métricas
4. **Pipeline de Agregación** - Procesamiento de datos
5. **Detección de Anomalías** - Monitoreo automático

## 📊 Estado Actual

✅ **Completado:**
- Database Manager con esquema completo
- Memory Manager con compresión inteligente
- Graduation System con criterios de 85%
- Domain System con 6 dominios especializados
- Collaboration Manager con 5 tipos de colaboración
- Agent System completo con integración
- Tests completos y documentación

🔄 **En Progreso:**
- Optimizaciones de performance
- Integración con modelos reales
- Población de datos de prueba

📋 **Pendiente:**
- Metadata System (FASE 5)
- TimescaleDB Setup (FASE 5)
- Grafana Dashboards (FASE 5)
- Fine-tuning Pipeline (FASE 6)

## 🤝 Contribución

Para contribuir al sistema de agentes:

1. Fork del repositorio
2. Crear branch para feature
3. Implementar cambios con tests
4. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

**FASE 4 completada exitosamente** 🎉

El sistema de agentes persistentes está listo para la integración con el Metadata System en la FASE 5.
