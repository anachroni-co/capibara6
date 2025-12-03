# Configuración Actualizada de la Arquitectura Capibara6

## 🖥️ VM models-europe (34.175.48.2 / 10.204.0.9)

### Servicios Activos

#### 1. vLLM Multi-Model Server (Puerto 8080) - **PRINCIPAL**
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
| `gemma3_multimodal` | ✅ Cargado | Complex Reasoning | Análisis complejo y multimodal |
| `aya_expanse_multilingual` | ✅ Cargado | Multilingual | Multilingüe y razonamiento complejo |

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
curl http://10.204.0.9:8080/v1/models

# Chat completion
curl http://10.204.0.9:8080/v1/chat/completions \
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

## 🔄 Flujo de Datos Actualizado

```
Usuario/Cliente
      ↓
┌─────────────────────────────────────────┐
│ services (10.204.0.5)                   │
│ ├─ Nginx (80/443) → Proxy               │
│ ├─ Flask API (5000) → Backend           │
│ ├─ TTS (5001/5002) → Texto a voz        │
│ ├─ MCP (5003) → Context Protocol        │
│ └─ n8n (5678) → Workflows               │
└─────────────────────────────────────────┘
      ↓ (peticiones de IA)
┌─────────────────────────────────────────┐
│ models-europe (10.204.0.9)              │
│ ┌─────────────────────────────────────┐ │
│ │ vLLM Server (8080) - PRINCIPAL      │ │
│ │ ├─ Router/Consenso                  │ │
│ │ ├─ phi4_fast (rápido)               │ │
│ │ ├─ mistral_balanced (balanceado)    │ │
│ │ ├─ qwen_coder (código)              │ │
│ │ ├─ gemma3_multimodal (análisis)     │ │
│ │ └─ aya_expanse_multilingual (multi) │ │
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

## 🔧 Variables de Entorno Actualizadas

### Backend

```bash
# vLLM Server (PRINCIPAL)
VLLM_URL=http://10.204.0.9:8080/v1/chat/completions
VLLM_COMPLETIONS_URL=http://10.204.0.9:8080/v1/completions
VLLM_MODELS_URL=http://10.204.0.9:8080/v1/models
VLLM_HEALTH_URL=http://10.204.0.9:8080/health

# Ollama (FALLBACK)
OLLAMA_URL=http://10.204.0.9:11434/api/generate
```

### Vercel (Frontend Proxy)

```bash
# vLLM Principal
VLLM_URL=http://34.175.48.2:8080/v1/chat/completions

# Ollama Fallback
OLLAMA_URL=http://34.175.48.2:11434/api/generate
```

---

## 📡 Endpoints Actualizados

### vLLM (Puerto 8080)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/v1/models` | GET | Listar modelos disponibles |
| `/v1/chat/completions` | POST | Completions de chat (OpenAI compatible) |
| `/v1/completions` | POST | Completions de texto (OpenAI compatible) |
| `/health` | GET | Health check del servidor |
| `/stats` | GET | Estadísticas del servidor |

### Ollama (Puerto 11434)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/generate` | POST | Generación de texto |
| `/api/chat` | POST | Chat completions |
| `/api/tags` | GET | Model tags |

---

## 🧪 Pruebas de Conexión

### Verificar vLLM:

```bash
# Health check
curl http://10.204.0.9:8080/health

# Listar modelos
curl http://10.204.0.9:8080/v1/models

# Test de completions
curl http://10.204.0.9:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi4_fast",
    "messages": [{"role": "user", "content": "Hola, ¿cómo estás?"}],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

### Verificar Ollama:

```bash
# Listar modelos
curl http://10.204.0.9:11434/api/tags

# Test de completions
curl http://10.204.0.9:11434/api/generate \
  -d '{"model": "gpt-oss:20b", "prompt": "Hola", "stream": false}'
```