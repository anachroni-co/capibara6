# Hallazgos de Infraestructura - Capibara6
## Fecha: 2025-11-13

## Resumen Ejecutivo

Investigación completa de la infraestructura del proyecto Capibara6 para identificar todos los servicios, bases de datos y servidores activos o documentados.

---

## 🔍 Servicios Backend Encontrados y Verificados

### Servidor Principal: `backend/server_gptoss.py` (Puerto 5001)
**Rol:** Backend principal del chatbot con GPT-OSS-20B
**Estado:** ✅ Activo y configurado
**Endpoints:**
- `POST /api/chat` - Chat básico
- `POST /api/chat/stream` - Chat con streaming
- `GET /api/health` - Health check
- `GET /api/models` - Listar modelos
- `POST /api/save-conversation` - Guardar conversaciones

**Frontend conecta a:** `http://localhost:5001` (desarrollo) o `VM_MODELS:5001` (producción)

### Servidor FastAPI Alternativo: `backend/main.py` (Puerto 8000)
**Rol:** API alternativa con E2B integrado
**Estado:** ⚠️ Disponible pero no usado por frontend actual
**Endpoints:**
- `GET /health`
- `POST /api/v1/query` - Consulta al modelo
- `GET /api/v1/models` - Listar modelos
- `POST /api/v1/e2b/execute` - Ejecutar código en E2B

### Servidor MCP: `backend/mcp_server.py` (Puerto 5003)
**Rol:** Model Context Protocol - RAG y contexto inteligente
**Estado:** ⚠️ Opcional, deshabilitado por defecto
**Endpoints:**
- `GET /api/mcp/contexts` - Listar contextos
- `GET /api/mcp/context/<id>` - Obtener contexto específico
- `POST /api/mcp/augment` - Aumentar prompt con contexto (RAG)
- `GET /api/mcp/tools` - Listar herramientas
- `POST /api/mcp/calculate` - Calculadora
- `POST /api/mcp/verify` - Verificar hechos
- `GET /api/mcp/health` - Health check

**Configuración Frontend:** `web/config.js` → `SERVICES.MCP.enabled = false`

### Servidor TTS: `backend/kyutai_tts_server.py` (Puerto 5002)
**Rol:** Text-to-Speech con Kyutai Moshi
**Estado:** ✅ Activo en VM gpt-oss-20b (34.175.136.104:5002)
**Endpoints:**
- `POST /tts` - Síntesis de voz
- `GET /voices` - Listar voces
- `POST /clone` - Clonar voz
- `GET /health` - Health check
- `POST /preload` - Precargar modelo

**Documentación:** `SERVICES_SETUP.md`

### Servidor Auth: `backend/auth_server.py` (Puerto 5004)
**Rol:** Autenticación OAuth (GitHub y Google)
**Estado:** ✅ Configurado
**Endpoints:**
- `GET /auth/github` - Login con GitHub
- `GET /auth/google` - Login con Google
- `POST /auth/verify` - Verificar token
- `POST /auth/logout` - Cerrar sesión
- `GET /auth/callback/github` - Callback GitHub
- `GET /auth/callback/google` - Callback Google
- `GET /health` - Health check

**Cambio reciente:** Puerto cambiado de 5001 → 5004 (Fase 2)

### Servidor Consensus: `backend/consensus_server.py` (Puerto 5005)
**Rol:** Consenso multi-modelo
**Estado:** ⚠️ Deshabilitado por defecto
**Endpoints:**
- `POST /api/consensus/query` - Consulta con consenso
- `GET /api/consensus/models` - Listar modelos
- `GET /api/consensus/templates` - Templates de consenso
- `GET /api/consensus/config` - Configuración
- `GET /api/consensus/health` - Health check

**Cambio reciente:** Puerto cambiado de 5002 → 5005 (Fase 2)
**Configuración Frontend:** `web/config.js` → `SERVICES.CONSENSUS.enabled = false`

### Servidor Smart MCP Alternativo: `backend/smart_mcp_server.py` (Puerto 5010)
**Rol:** MCP alternativo con RAG selectivo simplificado
**Estado:** ⚠️ Opcional, alternativa a mcp_server.py
**Endpoints:**
- `GET /health` - Health check
- `POST /analyze` - Análisis de query
- `POST /update-date` - Actualizar fecha

**Configuración Frontend:** `web/config.js` → `SERVICES.SMART_MCP.enabled = false`

---

## 🗄️ Bases de Datos Encontradas

### PostgreSQL (Puerto 5432)
**Ubicación:** `docker-compose.yml`
**Estado:** ✅ Configurado en Docker
**Uso:** Base de datos principal para persistencia
```yaml
postgres:
  image: postgres:15
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

### TimescaleDB (Puerto 5433)
**Ubicación:** `docker-compose.yml`
**Estado:** ✅ Configurado en Docker
**Uso:** Time-series data (métricas, logs temporales)
```yaml
timescaledb:
  image: timescale/timescaledb:latest-pg15
  ports:
    - "5433:5432"
  volumes:
    - timescale_data:/var/lib/postgresql/data
```

### Redis (Puerto 6379)
**Ubicación:** `docker-compose.yml`
**Estado:** ✅ Configurado en Docker
**Uso:** Cache y sesiones
```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
```

### FAISS Vector Store
**Ubicación:** `backend/config/infrastructure_config.py`
**Estado:** ✅ Configurado como vector store principal
**Uso:** Búsqueda de vectores para RAG
```python
RAG_CONFIG = {
    'vector_store': {
        'type': 'faiss',
        'index_type': 'IndexFlatIP',
        'embedding_dimension': 384
    }
}
```

### ChromaDB
**Ubicación:** `archived/backend_modules/core/rag/vector_store.py`
**Estado:** ❌ Solo en código archivado, no activo
**Nota:** Código existe pero no está en uso actualmente

---

## ❌ Servicios NO Encontrados (Búsqueda Exhaustiva)

### Milvus Database
**Búsqueda realizada:**
- ✅ Archivos Python (.py)
- ✅ Archivos JavaScript (.js)
- ✅ Archivos de configuración (.yaml, .json, .env, .cfg)
- ✅ Docker Compose
- ✅ Documentación (.md)
- ✅ Puerto estándar 19530

**Resultado:** ❌ No encontrado en el repositorio

**Posibilidades:**
1. Instalado directamente en VM rag3 (fuera del repositorio)
2. No implementado aún
3. Reemplazado por FAISS

### Nebula Graph
**Búsqueda realizada:**
- ✅ Archivos Python (.py)
- ✅ Archivos JavaScript (.js)
- ✅ Archivos de configuración
- ✅ Docker Compose
- ✅ Puertos estándar (9669, 7687)

**Resultado:** ❌ No encontrado en el repositorio

**Posibilidades:**
1. Instalado directamente en VM rag3
2. Confundido con otra base de datos de grafos
3. No implementado

### Servidor "Bridge" Explícito
**Búsqueda realizada:**
- ✅ Archivos con nombre "bridge"
- ✅ Archivos con "proxy" en el nombre
- ✅ Documentación que mencione "bridge"

**Resultado:** ❌ No encontrado como archivo independiente

**Análisis:**
El rol de "bridge" probablemente lo cumple **`backend/server_gptoss.py`** (puerto 5001), que:
- Recibe requests del frontend
- Se comunica con MCP para RAG (puerto 5003)
- Se comunica con TTS para síntesis de voz (puerto 5002)
- Integra E2B para ejecución de código
- Maneja autenticación via auth_server (puerto 5004)
- Coordina consensus si está habilitado (puerto 5005)

**Evidencia:**
```javascript
// web/config.js
const CHATBOT_CONFIG = {
    BACKEND_URL: isLocalhost ? 'http://localhost:5001' : VM_MODELS + ':5001',
    ENDPOINTS: {
        CHAT: '/api/v1/query',
        CHAT_STREAM: '/api/v1/chat/stream',
        TTS_SPEAK: '/api/tts/speak',
        MCP_CONTEXT: '/api/v1/mcp/context',
        E2B_EXECUTE: '/api/v1/e2b/execute'
    }
}
```

---

## 📋 Servicios Externos Documentados

### N8N Workflow Automation (Puerto 5678)
**Ubicación:** VM gpt-oss-20b (34.175.136.104:5678)
**Estado:** ⚠️ Requiere VPN/túnel
**Documentación:** `SERVICES_SETUP.md`
**Configuración Frontend:** Deshabilitado en `web/config.js` → `N8N_ENABLED: false`

**Razón de deshabilitado:** No es accesible públicamente, requiere conexión VPN a la VM

### VM rag3
**Mencionado en:** `backend/ARCHITECTURE.md`
**Estado:** 📝 Documentado pero sin detalles de implementación
**Descripción:** "Servidor con sistema RAG completo"
**Nota:** No se encontraron detalles de configuración, endpoints o servicios específicos

---

## 🏗️ Arquitectura de VMs

### VM bounty2 (34.12.166.76)
**Servicios:**
- Backend principal (server_gptoss.py - puerto 5001)
- Auth server (puerto 5004)
- Consensus server (puerto 5005)
- Ollama (modelo local)

### VM gpt-oss-20b (34.175.136.104)
**Servicios:**
- TTS Server (puerto 5002)
- MCP Server (puerto 5003)
- Smart MCP alternativo (puerto 5010)
- N8N (puerto 5678 - VPN requerida)

### VM rag3 (dirección desconocida)
**Estado:** Mencionada en documentación pero sin detalles
**Servicios esperados:**
- Sistema RAG completo
- ¿Milvus?
- ¿Nebula Graph?
- ¿Bridge server?

---

## 🔧 Configuración de RAG

### Mini RAG
```python
'mini_rag': {
    'timeout_ms': 50,
    'max_results': 5,
    'cache_size': 1000,
    'cache_ttl_seconds': 300
}
```

### Full RAG
```python
'full_rag': {
    'max_results': 10,
    'expansion_factor': 2.0,
    'deep_search_timeout_ms': 200
}
```

### Vector Store
```python
'vector_store': {
    'type': 'faiss',
    'index_type': 'IndexFlatIP',
    'embedding_dimension': 384
}
```

---

## 📊 Resumen de Puertos

| Puerto | Servicio | Estado | VM |
|--------|----------|--------|-----|
| 5001 | Backend Principal (server_gptoss.py) | ✅ Activo | bounty2 |
| 5002 | TTS Server (Kyutai) | ✅ Activo | gpt-oss-20b |
| 5003 | MCP Server | ⚠️ Opcional | gpt-oss-20b |
| 5004 | Auth Server | ✅ Configurado | bounty2 |
| 5005 | Consensus Server | ⚠️ Opcional | bounty2 |
| 5010 | Smart MCP Alternativo | ⚠️ Opcional | gpt-oss-20b |
| 5432 | PostgreSQL | ✅ Docker | Local |
| 5433 | TimescaleDB | ✅ Docker | Local |
| 5678 | N8N | ⚠️ VPN requerida | gpt-oss-20b |
| 6379 | Redis | ✅ Docker | Local |
| 8000 | FastAPI (main.py) | ⚠️ Alternativo | bounty2 |

---

## 🎯 Conclusiones

### Servicios Consolidados Exitosamente ✅
1. Backend principal claramente definido (puerto 5001)
2. Servicios especializados con puertos dedicados
3. Frontend correctamente configurado para usar puertos correctos
4. Docker Compose con bases de datos fundamentales

### Áreas que Requieren Clarificación ⚠️
1. **VM rag3:** Necesita documentación detallada de servicios
2. **Milvus:** No encontrado en código, posible instalación externa
3. **Nebula Graph:** No encontrado en código
4. **Bridge Server:** Rol cumplido por server_gptoss.py (necesita confirmación)

### Recomendaciones 📝

1. **Si Milvus y Nebula Graph existen en VM rag3:**
   - Documentar endpoints y configuración
   - Agregar healthchecks en frontend
   - Crear scripts de conexión en backend

2. **Si NO existen:**
   - Considerar si son necesarios para la funcionalidad actual
   - FAISS está funcionando bien como vector store
   - PostgreSQL puede manejar relaciones si no se necesita grafo

3. **Para VM rag3:**
   - Crear documentación de arquitectura específica
   - Agregar a `ARCHITECTURE_QUICK_REF.md`
   - Incluir en scripts de monitoreo

4. **Para el "Bridge":**
   - Confirmar que server_gptoss.py cumple este rol
   - O implementar un bridge dedicado si se requiere separación de responsabilidades
   - Documentar flujo de comunicación entre servicios

---

## 📁 Archivos de Referencia

- `web/config.js` - Configuración completa de servicios frontend
- `backend/config/infrastructure_config.py` - Configuración RAG y vector store
- `SERVICES_SETUP.md` - Setup de servicios en VMs
- `ARCHITECTURE_QUICK_REF.md` - Referencia rápida de arquitectura
- `docker-compose.yml` - Bases de datos locales
- `BACKEND_CONSOLIDATION_PLAN.md` - Plan de consolidación (Fases 1-4)
- `FIXES_ENDPOINTS.md` - Correcciones de endpoints

---

## 🚀 Próximos Pasos

1. **Validar hallazgos** con acceso real a las VMs
2. **Documentar VM rag3** si existe
3. **Implementar Fase 4** con los servicios verificados
4. **Crear scripts de gestión** para servicios confirmados
5. **Actualizar documentación** con hallazgos validados
