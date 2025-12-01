# Arquitectura Capibara6 - VMs en Google Cloud

**Actualizado:** 2025-11-27
**Red VPC:** default (10.204.0.0/24)
**Zona:** europe-southwest1-b
**Latencia entre VMs:** < 1ms

---

## 🌐 Topología de Red

```
┌────────────────────────────────────────────────────────────────────┐
│                    VPC: default (10.204.0.0/24)                     │
│                  Zona: europe-southwest1-b                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐      ┌──────────────────┐      ┌───────────┐│
│  │   services      │      │  models-europe   │      │rag-europe ││
│  │   10.204.0.5    │◄────►│   10.204.0.9     │◄────►│10.204.0.10││
│  │ 34.175.255.139  │      │  34.175.48.2     │      │34.175.    ││
│  └─────────────────┘      └──────────────────┘      │110.120    ││
│         │                          │                 └───────────┘│
│    SERVICIOS                   MODELOS                  DATOS      │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ VM 1: services (10.204.0.5)

**Rol:** Servicios de soporte y gateway
**IP Externa:** 34.175.255.139

### Servicios Activos

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| 80/443 | Nginx | Proxy reverso y servidor web |
| 5000 | Flask API | Backend para emails y MCP connector |
| 5001 | Coqui TTS | Text-to-Speech |
| 5003 | MCP Server | Model Context Protocol |
| 5678 | n8n | Workflow Automation |

### Configuración Nginx

```nginx
/api/ → capibara6_api:8000
/n8n/ → n8n:5678
/webhook/ → n8n webhooks
```

---

## 🤖 VM 2: models-europe (10.204.0.9)

**Rol:** Motor de IA - Servidor de modelos con vLLM
**IP Externa:** 34.175.48.2

### Servicios Activos

#### 1. vLLM Multi-Model Server (Puerto 8082) - **PRINCIPAL**

**Arquitectura:**
- Sistema de consenso y routing de modelos
- Lazy loading automático (max 3 modelos cargados)
- Auto-unload después de 300s de inactividad
- Compatible con OpenAI API

**Modelos Disponibles:**

| Modelo | Estado | Dominio | Descripción |
|--------|--------|---------|-------------|
| `phi4_fast` | ✅ Cargado | General | Respuestas rápidas y simples |
| `mistral_balanced` | ✅ Cargado | Technical | Tareas técnicas intermedias |
| `qwen_coder` | ✅ Cargado | Coding | Especializado en código |
| `gptoss_complex` | ⏳ Disponible | Expert | Razonamiento complejo (20B) |

**Endpoints:**

```bash
# Health & Stats
GET  /health              # Health check
GET  /stats               # Estadísticas y modelos cargados

# OpenAI Compatible
GET  /v1/models           # Lista de modelos
POST /v1/chat/completions # Chat completion
POST /v1/completions      # Text completion

# Ollama Compatible
POST /api/generate        # Generate text
```

**Ejemplo de uso:**

```bash
# Listar modelos
curl http://10.204.0.9:8082/v1/models

# Chat completion
curl http://10.204.0.9:8082/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi4_fast",
    "messages": [{"role": "user", "content": "Hola"}]
  }'
```

#### 2. Ollama (Puerto 11434) - **ALTERNATIVO**

**Modelos:**
- `gpt-oss:20b` (13.8 GB, MXFP4)
- `mistral:latest` (4.4 GB, Q4_K_M)
- `phi3:mini` (2.2 GB, Q4_0)

**Uso:**
```bash
curl http://10.204.0.9:11434/api/generate \
  -d '{"model": "gpt-oss:20b", "prompt": "Hola"}'
```

### Conexión con rag-europe

models-europe se conecta con rag-europe para:
- Consultar bases de datos vectoriales (Milvus)
- Buscar en grafos de conocimiento (Nebula)
- Recuperar contexto de PostgreSQL
- Cache en Redis

```
models-europe → Bridge API (10.204.0.10:8000)
               → /api/v1/rag/hybrid-search
               → /api/v1/milvus/search
               → /api/v1/nebula/query
```

---

## 🗄️ VM 3: rag-europe (10.204.0.10)

**Rol:** Bridge API + Sistema de bases de datos
**IP Externa:** 34.175.110.120

### Servicios Activos

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| 8000 | Bridge API | Gateway unificado para DBs |
| 7001 | Nebula Studio | UI de Nebula Graph |
| 9669 | Nebula Graph | Base de datos de grafos |
| 19530 | Milvus | Base de datos vectorial |
| 5432 | PostgreSQL | Base de datos relacional |
| 6379 | Redis | Cache en memoria |

### Bridge API (Puerto 8000)

**Endpoints:**

```bash
# Health
GET  /health              # Health check básico
GET  /health/detailed     # Estado de todas las conexiones

# Milvus (Vector DB)
POST /api/v1/milvus/search      # Búsqueda vectorial
GET  /api/v1/milvus/collections # Listar colecciones

# Nebula Graph
POST /api/v1/nebula/query       # Consultas nGQL
GET  /api/v1/nebula/spaces      # Listar espacios

# PostgreSQL
POST /api/v1/postgres/query     # Consultas SQL
GET  /api/v1/postgres/tables    # Listar tablas

# Redis
GET  /api/v1/redis/get          # Obtener valor
POST /api/v1/redis/set          # Establecer valor

# RAG Híbrido
POST /api/v1/rag/hybrid-search  # Búsqueda híbrida
```

**Estado de Conexiones:**

```json
{
  "milvus":    { "status": "connected", "host": "localhost:19530" },
  "nebula":    { "status": "connected", "host": "localhost:9669" },
  "postgres":  { "status": "connected", "host": "localhost:5432" },
  "redis":     { "status": "connected", "host": "localhost:6379" }
}
```

---

## 🔄 Flujo de Datos

```
Usuario/Cliente
      ↓
┌─────────────────────────────────────────┐
│ services (10.204.0.5)                   │
│ ├─ Nginx (80/443) → Proxy               │
│ ├─ Flask API (5000) → Backend           │
│ ├─ TTS (5001) → Texto a voz             │
│ ├─ MCP (5003) → Context Protocol        │
│ └─ n8n (5678) → Workflows               │
└─────────────────────────────────────────┘
      ↓ (peticiones de IA)
┌─────────────────────────────────────────┐
│ models-europe (10.204.0.9)              │
│ ┌─────────────────────────────────────┐ │
│ │ vLLM Server (8082) - PRINCIPAL      │ │
│ │ ├─ Router/Consenso                  │ │
│ │ ├─ phi4_fast (rápido)               │ │
│ │ ├─ mistral_balanced (balanceado)    │ │
│ │ ├─ qwen_coder (código)              │ │
│ │ └─ gptoss_complex (experto)         │ │
│ └─────────────────────────────────────┘ │
│ Ollama (11434) - Alternativo            │
└─────────────────────────────────────────┘
      ↓ (necesita contexto/datos)
┌─────────────────────────────────────────┐
│ rag-europe (10.204.0.10)                │
│ ┌─────────────────────────────────────┐ │
│ │ Bridge API (8000)                   │ │
│ └─────────────────────────────────────┘ │
│      ↓           ↓           ↓          │
│  ┌────────┐ ┌────────┐ ┌─────────┐     │
│  │ Milvus │ │ Nebula │ │Postgres │     │
│  │(vector)│ │(grafos)│ │  (SQL)  │     │
│  └────────┘ └────────┘ └─────────┘     │
│                ↓                        │
│          ┌─────────┐                    │
│          │  Redis  │                    │
│          │ (cache) │                    │
│          └─────────┘                    │
└─────────────────────────────────────────┘
```

---

## 📡 Conectividad Verificada

```bash
# Ping entre VMs
services → models-europe:  0.5ms (0% packet loss) ✅
services → rag-europe:     0.5ms (0% packet loss) ✅

# APIs accesibles
vLLM Server (10.204.0.9:8082):     ✅ 4 modelos
Ollama (10.204.0.9:11434):         ✅ 3 modelos
Bridge API (10.204.0.10:8000):     ✅ 4 DBs conectadas
```

---

## 🚀 Scripts de Conexión SSH

```bash
# Conectar a services (actual)
# Ya estás aquí

# Conectar a models-europe
./ssh-models-europe.sh
# o
gcloud compute ssh models-europe --zone=europe-southwest1-b

# Conectar a rag-europe
./ssh-rag-europe.sh
# o
gcloud compute ssh rag-europe --zone=europe-southwest1-b
```

---

## 📝 Archivos de Configuración

### Ubicaciones

```
/home/elect/capibara6/
├── backend/
│   ├── .env.production          # Configuración de producción
│   └── config/
│       └── vm_endpoints.py      # Gestión de endpoints
├── web/
│   └── config.js                # Configuración frontend
├── proxy-cors.js                # Proxy CORS para desarrollo
├── ssh-models-europe.sh         # Script SSH models
├── ssh-rag-europe.sh            # Script SSH rag
└── ARQUITECTURA_VMS.md          # Este archivo
```

### Variables de Entorno Importantes

```bash
# vLLM Server
VLLM_URL=http://10.204.0.9:8082
VLLM_MODELS=phi4_fast,mistral_balanced,qwen_coder,gptoss_complex

# Ollama (alternativo)
OLLAMA_URL=http://10.204.0.9:11434

# Bridge API
BRIDGE_API_URL=http://10.204.0.10:8000
RAG_API_URL=http://10.204.0.10:8000
```

---

## 🔒 Seguridad

### Recomendaciones

1. **Usar IPs internas** para comunicación entre VMs (ya configurado)
2. **Limitar reglas de firewall** por VM específica
3. **Habilitar HTTPS** en producción (certificados SSL)
4. **Implementar autenticación** en APIs públicas

### Reglas de Firewall Actuales

Todas las VMs comparten reglas globales. Considerar crear reglas específicas:

```bash
# Ejemplo: Regla específica para vLLM
gcloud compute firewall-rules create allow-vllm \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:8082 \
  --source-ranges=10.204.0.0/24 \  # Solo VPC interna
  --target-tags=models-vm
```

---

## 📊 Monitoreo

### Health Checks

```bash
# services
curl http://10.204.0.5:5000/health

# models-europe (vLLM)
curl http://10.204.0.9:8082/health
curl http://10.204.0.9:8082/stats

# models-europe (Ollama)
curl http://10.204.0.9:11434/api/version

# rag-europe
curl http://10.204.0.10:8000/health
curl http://10.204.0.10:8000/health/detailed
```

### Logs

```bash
# Ver logs de servicios
sudo journalctl -u flask-app -f
sudo journalctl -u coqui-tts -f
sudo journalctl -u n8n -f
```

---

**Última actualización:** 2025-11-27
**Mantenido por:** Anachroni s.coop
