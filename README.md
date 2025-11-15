# 🦫 Capibara6 - Sistema de IA Distribuido

**Versión**: 2.0 (Reorganizado por VMs)
**Estado**: ✅ Operativo
**Última actualización**: 2025-11-14

Sistema de IA distribuido en 3 VMs de Google Cloud con:
- Múltiples modelos de IA (GPT-OSS-20B, phi3, llama2)
- Sistema RAG (Milvus + Nebula Graph)
- Servicios auxiliares (TTS, MCP, N8N)
- Monitorización completa (Prometheus, Grafana, Jaeger)

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│              Chat | RAG | TTS | OAuth                │
└────────────┬─────────────────────────────────────────┘
             │
    ┌────────┴────────┬──────────────┬────────────┐
    ↓                 ↓              ↓            ↓
┌─────────┐    ┌─────────┐    ┌──────────┐   ┌────────┐
│ Bounty2 │    │Services │    │  RAG3    │   │Frontend│
│(Modelos)│    │(TTS/MCP)│    │(Milvus+) │   │  (Web) │
│  :5001  │    │:5002/03 │    │  :8000   │   │        │
└─────────┘    └─────────┘    └──────────┘   └────────┘
```

## 📂 Estructura del Proyecto

```
capibara6/
├── vm-bounty2/          # 🤖 VM de Modelos de IA
│   ├── servers/         # Backend GPT-OSS-20B, Auth, Consensus
│   ├── config/          # Configuraciones de modelos
│   ├── core/            # Router semántico, E2B execution
│   └── deployment/      # Docker, K8s
│
├── vm-services/         # 🔧 VM de Servicios
│   ├── tts/             # Text-to-Speech (Kyutai)
│   ├── mcp/             # Model Context Protocol
│   ├── n8n/             # Workflow automation
│   └── deployment/      # Docker configs
│
├── vm-rag3/             # 🗄️ VM RAG (Vector + Graph)
│   ├── api/             # Bridge API (capibara6-api)
│   ├── databases/       # Milvus, Nebula, PostgreSQL, Redis
│   ├── monitoring/      # Prometheus, Grafana, Jaeger
│   └── scripts/         # Scripts de administración
│
├── frontend/            # 🌐 Aplicación Web
│   ├── public/          # HTML files
│   ├── src/             # JavaScript (clients, components, integrations)
│   ├── styles/          # CSS
│   └── deployment/      # Nginx, Docker
│
├── docs/                # 📚 Documentación
│   ├── ARCHITECTURE.md
│   ├── PLAN_REORGANIZACION.md
│   └── ...
│
└── scripts/             # 🔨 Scripts globales
```

## 🚀 Inicio Rápido

### Frontend Local

```bash
cd frontend/public
python3 -m http.server 8080
# Abrir: http://localhost:8080/chat.html
```

### Conectar a VMs

```bash
# VM Bounty2 (Modelos)
gcloud compute ssh bounty2

# VM Services (TTS, MCP)
gcloud compute ssh gpt-oss-20b

# VM RAG3 (Sistema RAG)
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

### Verificar Estado de Servicios

```bash
# VM Bounty2
curl http://34.12.166.76:5001/health      # Backend
curl http://34.12.166.76:5004/health      # Auth
curl http://34.12.166.76:5005/health      # Consensus

# VM Services
curl http://34.175.136.104:5002/health    # TTS
curl http://34.175.136.104:5003/api/mcp/health  # MCP

# VM RAG3 (desde dentro de la VM)
curl http://10.154.0.2:8000/health        # Bridge API
curl http://10.154.0.2:19530              # Milvus
curl http://10.154.0.2:9669               # Nebula Graph
```

## 📋 Servicios por VM

### VM Bounty2 (34.12.166.76)

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Backend Principal | 5001 | GPT-OSS-20B API |
| Auth Server | 5004 | OAuth (GitHub, Google) |
| Consensus Server | 5005 | Multi-modelo |

[Ver documentación completa →](vm-bounty2/README.md)

### VM Services (34.175.136.104)

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| TTS (Kyutai) | 5002 | Text-to-Speech |
| MCP | 5003 | Context Protocol |
| N8N | 5678 | Workflows (requiere VPN) |

[Ver documentación completa →](vm-services/README.md)

### VM RAG3 (10.154.0.2 - IP interna)

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| Bridge API | 8000 | capibara6-api Gateway |
| Milvus | 19530 | Vector database |
| Nebula Graph | 9669 | Knowledge graph |
| PostgreSQL | 5432 | BD relacional |
| TimescaleDB | 5433 | Time-series |
| Redis | 6379 | Cache |
| Prometheus | 9090 | Métricas |
| Grafana | 3000 | Dashboards |
| Jaeger | 16686 | Tracing |

[Ver documentación completa →](vm-rag3/README.md)

## 🎯 Características Principales

### 🤖 Múltiples Modelos de IA

- **GPT-OSS-20B** (20.9B parámetros) - Queries complejas
- **llama2** - Queries moderadas
- **phi3:mini** - Queries simples
- **Router semántico** - Selección automática

### 🔍 Sistema RAG Avanzado

- **Milvus** (v2.3.10) - Búsqueda vectorial semántica
- **Nebula Graph** (v3.1.0) - Knowledge graph de 3 nodos
- **Búsqueda híbrida** - Combina vector (70%) + grafo (30%)
- **Optimización TOON** - Ahorro de 30-60% de tokens

### 🎙️ Text-to-Speech

- **Kyutai Moshi** - Síntesis de voz de alta calidad
- **Clonación de voz** - Voces personalizadas
- **API REST** - Integración fácil

### 🧠 Smart MCP v2.0

- **Contexto selectivo** - Solo cuando es necesario
- **Análisis de queries** - Detecta complejidad
- **Fallback automático** - Si no está disponible

### 🔐 Autenticación

- **OAuth 2.0** - GitHub y Google
- **JWT tokens** - Seguridad robusta
- **Session management** - Refresh tokens

### 📊 Monitorización Completa

- **18 dashboards Grafana** - Métricas en tiempo real
- **30+ alertas Prometheus** - Proactivas
- **Distributed tracing** - Jaeger para debugging
- **Logs centralizados** - Fácil troubleshooting

## 🛠️ Desarrollo

### Requisitos

- Python 3.9+
- Node.js 18+ (opcional, para frontend moderno)
- Docker & Docker Compose
- Google Cloud SDK (para VMs)

### Setup Local

```bash
# Clonar repositorio
git clone https://github.com/anacronic-io/capibara6.git
cd capibara6

# Instalar dependencias
pip install -r requirements.txt

# Copiar .env ejemplo
cp .env.example .env

# Editar configuración
nano .env
```

### Iniciar Servicios (Development)

```bash
# VM Bounty2
cd vm-bounty2
python3 scripts/start_system.py

# VM Services
cd vm-services
./scripts/start-all-services.sh

# VM RAG3
cd vm-rag3
./scripts/start-all-services.sh

# Frontend
cd frontend/public
python3 -m http.server 8080
```

## 🐳 Deployment

### Docker Compose

```bash
# Deploy VM Bounty2
cd vm-bounty2/deployment
docker-compose up -d

# Deploy VM Services
cd vm-services/deployment
docker-compose up -d

# Deploy VM RAG3
cd vm-rag3/deployment
docker-compose up -d
docker-compose -f docker-compose.monitoring.yml up -d

# Deploy Frontend
cd frontend/deployment
docker-compose up -d
```

### Kubernetes (Opcional)

```bash
cd vm-bounty2/deployment/k8s
kubectl apply -f .
```

## 📚 Documentación

### Principales

- [Arquitectura del Sistema](docs/ARCHITECTURE.md)
- [Plan de Reorganización](docs/PLAN_REORGANIZACION.md)
- [Mejoras VM RAG3](docs/IMPROVEMENTS_VM_RAG3.md)
- [Infrastructure Findings](docs/INFRASTRUCTURE_FINDINGS.md)

### Por VM

- [VM Bounty2 (Modelos)](vm-bounty2/README.md)
- [VM Services (TTS, MCP)](vm-services/README.md)
- [VM RAG3 (RAG System)](vm-rag3/README.md)
- [Frontend (Web App)](frontend/README.md)

### Troubleshooting

- [Solución Errores 404](docs/SOLUCIÓN_ERRORES_404.md)
- [Actualizar Servidor Web](docs/ACTUALIZAR_SERVIDOR_WEB.md)
- [VM RAG3 Analysis](docs/VM_RAG3_COMPLETE_ANALYSIS.md)

## 🧪 Tests

```bash
# Tests unitarios
pytest

# Tests de integración
pytest tests/integration

# Tests E2E
pytest tests/e2e

# Linting
flake8 vm-bounty2/ vm-services/ vm-rag3/
eslint frontend/src/
```

## 📊 Métricas y Monitoreo

### Grafana Dashboards

Acceder: http://10.154.0.2:3000

- **Sistema Completo** - Overview general
- **RAG Metrics** - Milvus, Nebula, Bridge API
- **Modelos** - Router, Consensus, E2B
- **Recursos** - CPU, Memoria, Disco, Network

### Prometheus

Acceder: http://10.154.0.2:9090

- Ver métricas en tiempo real
- Explorar queries PromQL
- Verificar alertas activas

### Jaeger Tracing

Acceder: http://10.154.0.2:16686

- Traces distribuidos
- Performance debugging
- Dependencias entre servicios

## 🤝 Contribuir

1. Fork del repositorio
2. Crear branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📝 Changelog

### v2.0 (2025-11-14) - Reorganización por VMs

- ✅ Reorganización completa en 4 carpetas principales
- ✅ Documentación actualizada por VM
- ✅ README.md para cada VM
- ✅ Arquitectura documentada
- ✅ Scripts de gestión organizados

### v1.0 (2025-01-XX) - Versión Inicial

- Integración con GPT-OSS-20B
- Sistema RAG básico
- Frontend funcional
- Auth OAuth

## 🔮 Roadmap

### Q1 2025
- [ ] Migrar frontend a React/Vue
- [ ] Auto-scaling de servicios
- [ ] Agregar más modelos (Mixtral, Qwen)
- [ ] Mejorar cache de embeddings

### Q2 2025
- [ ] Multi-tenancy
- [ ] API pública con rate limiting
- [ ] Mobile app
- [ ] Fine-tuning de modelos propios

## 📄 Licencia

Este proyecto es propiedad de **Anachroni s.coop**.

## 👥 Equipo

**Mantenedor**: Capibara6 Team
**Contacto**: marco@anachroni.co
**Organización**: Anachroni s.coop

---

**URLs Útiles**:
- Backend: http://34.12.166.76:5001
- TTS: http://34.175.136.104:5002
- MCP: http://34.175.136.104:5003
- Grafana: http://10.154.0.2:3000
- Prometheus: http://10.154.0.2:9090

**¿Problemas?** Ver [docs/TROUBLESHOOTING.md](docs/SOLUCIÓN_ERRORES_404.md)
