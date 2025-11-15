# VM Bounty2 - Modelos de IA

**IP Externa**: 34.12.166.76
**Zona**: Google Cloud
**Propósito**: Servidor principal de modelos de IA (Ollama, GPT-OSS-20B)

## 📋 Servicios

| Servicio | Puerto | Descripción | Script |
|----------|--------|-------------|--------|
| **Backend Principal** | 5001 | GPT-OSS-20B API | `servers/server_gptoss.py` |
| **Auth Server** | 5004 | OAuth (GitHub, Google) | `servers/auth_server.py` |
| **Consensus Server** | 5005 | Multi-modelo consensus | `servers/consensus_server.py` |

## 🚀 Inicio Rápido

### Iniciar Backend Principal

```bash
# Opción 1: Script de inicio
python3 scripts/start_gptoss_server.py

# Opción 2: Directamente
python3 servers/server_gptoss.py
```

### Iniciar Auth Server

```bash
python3 servers/auth_server.py
```

### Iniciar Consensus Server

```bash
python3 servers/consensus_server.py
```

### Iniciar Todos los Servicios

```bash
python3 scripts/start_system.py
```

## 📁 Estructura

```
vm-bounty2/
├── servers/              # Servidores principales
│   ├── server_gptoss.py  # Backend GPT-OSS-20B (puerto 5001)
│   ├── auth_server.py    # Auth OAuth (puerto 5004)
│   └── consensus_server.py  # Consensus (puerto 5005)
├── config/               # Configuraciones
│   ├── models_config.py  # Configuración de modelos
│   ├── gpt_oss_optimized_config.py  # Optimizaciones
│   └── production_config.py  # Configuración de producción
├── core/                 # Lógica de negocio
│   ├── router/           # Router semántico
│   ├── execution/        # E2B execution
│   ├── integration/      # Integraciones
│   ├── backend/          # Backend core
│   └── utils/            # Utilidades
├── scripts/              # Scripts de gestión
│   ├── start_gptoss_server.py
│   ├── start_system.py
│   └── start_integrated_server.py
├── deployment/           # Deploy configs
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── k8s/              # Kubernetes configs
├── api/                  # API endpoints
│   └── consensus/
└── tests/                # Tests

```

## ⚙️ Configuración

### Variables de Entorno

```bash
# Modelo
MODEL_NAME=gpt-oss-20b
MODEL_PATH=/path/to/model

# Servidor
HOST=0.0.0.0
PORT=5001

# OAuth
GITHUB_CLIENT_ID=your_id
GITHUB_CLIENT_SECRET=your_secret
GOOGLE_CLIENT_ID=your_id
GOOGLE_CLIENT_SECRET=your_secret

# E2B
E2B_API_KEY=your_key
```

### Modelos Disponibles

- **phi3:mini** - Queries simples
- **llama2** - Queries moderadas
- **gpt-oss-20b** - Queries complejas

## 🔧 Funcionalidades

### Router Semántico

Enruta queries automáticamente al modelo apropiado basado en:
- Complejidad de la consulta
- Embeddings (all-MiniLM-L6-v2)
- Confidence score

```python
from core.router import semantic_router

result = semantic_router.route_query("¿Cómo funciona Python?")
# → Devuelve modelo seleccionado + confidence
```

### E2B Sandboxes

Ejecución segura de código Python:

```python
from core.execution import e2b_client

result = e2b_client.execute("print('Hello')")
# → Ejecuta código en sandbox aislado
```

### Consensus Multi-Modelo

Combina respuestas de múltiples modelos:

```python
from core.consensus import consensus_engine

result = consensus_engine.query("Explica IA")
# → Consulta phi3, llama2, gpt-oss-20b y combina respuestas
```

## 📊 Monitoreo

### Health Check

```bash
curl http://34.12.166.76:5001/health
```

### Métricas

```bash
curl http://34.12.166.76:5001/metrics
```

## 🐳 Deployment

### Docker

```bash
cd deployment
docker-compose up -d
```

### Kubernetes

```bash
cd deployment/k8s
kubectl apply -f .
```

## 🔍 Troubleshooting

### Servidor no inicia

```bash
# Verificar puerto disponible
lsof -i :5001

# Ver logs
tail -f logs/server.log
```

### Modelo no responde

```bash
# Verificar memoria
free -h

# Verificar proceso
ps aux | grep gptoss
```

## 📚 Documentación Relacionada

- [BACKEND_CONSOLIDATION_PLAN.md](../docs/BACKEND_CONSOLIDATION_PLAN.md)
- [INFRASTRUCTURE_FINDINGS.md](../docs/INFRASTRUCTURE_FINDINGS.md)

## 🔗 Endpoints

### Backend Principal (5001)

```
POST /api/v1/query
POST /api/v1/chat/stream
GET  /api/v1/models
POST /api/v1/e2b/execute
GET  /health
```

### Auth Server (5004)

```
GET  /auth/github
GET  /auth/google
POST /auth/verify
GET  /auth/callback/github
GET  /auth/callback/google
GET  /health
```

### Consensus Server (5005)

```
POST /api/consensus/query
GET  /api/consensus/models
GET  /health
```

---

**Mantenedor**: Capibara6 Team
**Última actualización**: 2025-11-14
