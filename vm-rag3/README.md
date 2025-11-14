# VM RAG3 - Sistema RAG Completo

**IP Interna**: 10.154.0.2
**Zona**: europe-west2-c
**Proyecto**: mamba-001
**Propósito**: Sistema RAG completo (Milvus, Nebula Graph, Bridge API, Monitoring)

## 📋 Servicios

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **Bridge API** | 8000 | capibara6-api - Gateway principal |
| **Milvus** | 19530 | Vector database (v2.3.10) |
| **Nebula Graph** | 9669 | Knowledge graph (v3.1.0) |
| **PostgreSQL** | 5432 | Base de datos relacional |
| **TimescaleDB** | 5433 | Time-series database |
| **Redis** | 6379 | Cache y message broker |
| **Prometheus** | 9090 | Metrics collection |
| **Grafana** | 3000 | Dashboards y visualización |
| **Jaeger** | 16686 | Distributed tracing |

## 🚀 Inicio Rápido

### Conectar a VM RAG3

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

### Iniciar Todos los Servicios

```bash
./scripts/start-all-services.sh
```

### Verificar Estado

```bash
./scripts/check-services.sh
```

### Detener Servicios

```bash
./scripts/stop-all-services.sh
```

## 📁 Estructura

```
vm-rag3/
├── api/                  # Bridge API (puerto 8000)
│   ├── main.py           # FastAPI application
│   ├── routes/           # API routes
│   │   ├── milvus.py     # Milvus endpoints
│   │   ├── nebula.py     # Nebula Graph endpoints
│   │   └── rag.py        # RAG endpoints
│   └── config/           # API configuration
├── databases/            # Configuraciones de bases de datos
│   ├── milvus/           # Milvus vector database
│   │   ├── config/
│   │   └── schemas/      # Collection schemas
│   ├── nebula/           # Nebula Graph
│   │   ├── config/
│   │   └── schemas/      # Graph schemas
│   ├── postgres/         # PostgreSQL config
│   ├── timescaledb/      # TimescaleDB config
│   └── redis/            # Redis config
├── monitoring/           # Sistema de monitoreo
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alerts/       # Alert rules
│   ├── grafana/
│   │   ├── dashboards/   # Dashboards JSON
│   │   └── datasources/  # Datasource configs
│   └── jaeger/           # Tracing config
├── scripts/              # Scripts de administración
│   ├── start-all-services.sh
│   ├── stop-all-services.sh
│   ├── check-services.sh
│   ├── start-optional-services.sh
│   └── diagnostics/      # Diagnostic tools
├── deployment/           # Docker compose
│   ├── docker-compose.yml
│   ├── docker-compose.monitoring.yml
│   └── .env.example
└── docs/                 # Documentación específica
    ├── SETUP.md
    ├── MONITORING.md
    └── TROUBLESHOOTING.md
```

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env` en `deployment/`:

```bash
# Bridge API
API_HOST=0.0.0.0
API_PORT=8000

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION=capibara6_vectors
MILVUS_DIMENSION=384  # all-MiniLM-L6-v2

# Nebula Graph
NEBULA_METAD_HOST=localhost
NEBULA_METAD_PORT=9559
NEBULA_GRAPHD_HOST=localhost
NEBULA_GRAPHD_PORT=9669
NEBULA_STORAGED_HOST=localhost
NEBULA_STORAGED_PORT=9779
NEBULA_SPACE=capibara6_graph

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=capibara6
POSTGRES_USER=capibara6
POSTGRES_PASSWORD=secure_password

# TimescaleDB
TIMESCALE_HOST=localhost
TIMESCALE_PORT=5433

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Monitoring
GRAFANA_PORT=3000
PROMETHEUS_PORT=9090
JAEGER_PORT=16686
```

### Milvus - Vector Database

**Colección**: `capibara6_vectors`
**Dimensiones**: 384 (all-MiniLM-L6-v2)
**Tipo de índice**: IVF_FLAT
**Métrica**: L2

Schema:

```python
{
    "collection_name": "capibara6_vectors",
    "dimension": 384,
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "nlist": 1024
}
```

### Nebula Graph - Knowledge Graph

**Space**: `capibara6_graph`
**Cluster**: 3 nodos (metad, storaged, graphd)

Schema ejemplo:

```nGQL
CREATE TAG entity (
    name string,
    type string,
    description string,
    created_at timestamp
);

CREATE EDGE relates_to (
    weight double,
    description string
);
```

## 🔧 Funcionalidades

### Bridge API (puerto 8000)

Gateway principal que expone:

- Búsqueda vectorial en Milvus
- Consultas de grafo en Nebula
- Búsqueda híbrida RAG
- Integración con PostgreSQL/TimescaleDB/Redis

Endpoints:

```
# Milvus
POST /api/v1/milvus/search
GET  /api/v1/milvus/collections
POST /api/v1/milvus/insert

# Nebula Graph
POST /api/v1/nebula/query
GET  /api/v1/nebula/vertices
GET  /api/v1/nebula/edges

# RAG
POST /api/v1/rag/search
POST /api/v1/rag/hybrid

# Health
GET  /health
```

### Milvus - Búsqueda Vectorial

```python
from pymilvus import Collection, connections

# Conectar
connections.connect(host="10.154.0.2", port=19530)

# Buscar
collection = Collection("capibara6_vectors")
results = collection.search(
    data=[embedding_vector],
    anns_field="embedding",
    param={"metric_type": "L2", "nprobe": 10},
    limit=10
)
```

### Nebula Graph - Queries

```bash
# Conectar a graphd
nebula-console --addr=10.154.0.2 --port=9669 --user=root --password=nebula

# Usar space
USE capibara6_graph;

# Query ejemplo
MATCH (v:entity)-[r:relates_to]->(connected:entity)
WHERE v.name == "Python"
RETURN v, r, connected
LIMIT 10;
```

### PostgreSQL - Datos Estructurados

```bash
psql -h 10.154.0.2 -p 5432 -U capibara6 -d capibara6
```

### Redis - Cache

```bash
redis-cli -h 10.154.0.2 -p 6379
```

## 📊 Monitoreo

### Grafana Dashboards

Acceder: `http://10.154.0.2:3000`

Dashboards disponibles:
- **Capibara6 - Sistema Completo** (18 paneles)
  - Overview del sistema
  - Métricas RAG (Milvus, Nebula)
  - Router semántico
  - E2B Sandboxes
  - RQ Workers
  - Optimización TOON
  - Recursos del sistema

Credenciales por defecto:
- Usuario: `admin`
- Password: `admin`

### Prometheus Metrics

Acceder: `http://10.154.0.2:9090`

Queries útiles:

```promql
# Latencia p99
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Búsquedas vectoriales
rate(milvus_search_requests_total[5m])

# Queries de grafo
rate(nebula_query_requests_total[5m])

# Errores
rate(http_requests_total{status=~"5.."}[5m])
```

### Jaeger Tracing

Acceder: `http://10.154.0.2:16686`

Ver traces distribuidos de:
- Requests HTTP completos
- Búsquedas en Milvus
- Queries en Nebula Graph
- Interacciones con PostgreSQL/Redis

### Alertas

Ver alertas activas:

```bash
curl http://10.154.0.2:9090/api/v1/alerts
```

Alertas configuradas (30+ reglas):
- Latencia crítica (p99 > 5s)
- CPU/Memoria alta
- Servicios DOWN (Milvus, Nebula, etc.)
- Cluster Nebula unhealthy
- Workers RQ inactivos
- Cache hit rate bajo

## 🐳 Deployment

### Docker Compose

```bash
cd deployment

# Iniciar todo
docker-compose up -d

# Iniciar solo bases de datos
docker-compose up -d postgres timescaledb redis

# Iniciar sistema RAG
docker-compose up -d milvus nebula-graphd capibara6-api

# Iniciar monitoring
docker-compose -f docker-compose.monitoring.yml up -d

# Ver logs
docker-compose logs -f capibara6-api

# Detener
docker-compose down
```

### Servicios Individuales

```bash
# Milvus
docker-compose up -d milvus

# Nebula Graph (cluster completo)
docker-compose up -d nebula-metad nebula-storaged nebula-graphd

# Bridge API
docker-compose up -d capibara6-api

# Monitoring
docker-compose up -d prometheus grafana jaeger
```

## 🔍 Troubleshooting

### Milvus no responde

```bash
# Verificar contenedor
docker ps | grep milvus

# Ver logs
docker logs capibara6-milvus

# Reiniciar
docker restart capibara6-milvus

# Verificar conexión
curl http://10.154.0.2:19530/health
```

### Nebula Graph cluster unhealthy

```bash
# Verificar todos los nodos
docker ps | grep nebula

# Ver estado del cluster
docker exec nebula-graphd nebula-storaged --status

# Reiniciar cluster
docker-compose restart nebula-metad nebula-storaged nebula-graphd

# Verificar en console
nebula-console --addr=10.154.0.2 --port=9669
SHOW HOSTS;
```

### Bridge API errores 500

```bash
# Ver logs
docker logs capibara6-api

# Verificar conexiones a bases de datos
docker exec capibara6-api python -c "
from pymilvus import connections
connections.connect(host='milvus', port=19530)
print('Milvus OK')
"

# Reiniciar
docker restart capibara6-api
```

### Grafana sin datos

```bash
# Verificar Prometheus
curl http://10.154.0.2:9090/-/healthy

# Verificar datasource en Grafana
curl http://10.154.0.2:3000/api/datasources

# Reimportar dashboard
# UI: Dashboard → Import → Upload JSON
```

## 🔧 Mantenimiento

### Backup de Bases de Datos

```bash
# PostgreSQL
pg_dump -h 10.154.0.2 -p 5432 -U capibara6 capibara6 > backup_$(date +%Y%m%d).sql

# Milvus (backup de colección)
python scripts/backup_milvus.py

# Nebula Graph (export space)
nGQL> SUBMIT JOB EXPORT "/path/to/export";
```

### Limpieza de Datos Antiguos

```bash
# Redis - limpiar cache
redis-cli -h 10.154.0.2 FLUSHDB

# TimescaleDB - eliminar datos antiguos
psql -h 10.154.0.2 -p 5433 -c "
SELECT drop_chunks('metrics', INTERVAL '90 days');
"

# Prometheus - ajustar retención (en prometheus.yml)
--storage.tsdb.retention.time=30d
```

### Actualizar Dashboards

```bash
# Copiar dashboard actualizado
cp monitoring/grafana/dashboards/capibara6-dashboard.json /path/to/grafana/

# Reimportar en UI o via API
curl -X POST http://10.154.0.2:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @monitoring/grafana/dashboards/capibara6-dashboard.json
```

## 📚 Documentación Relacionada

- [VM_RAG3_COMPLETE_ANALYSIS.md](../docs/VM_RAG3_COMPLETE_ANALYSIS.md)
- [IMPROVEMENTS_VM_RAG3.md](../docs/IMPROVEMENTS_VM_RAG3.md)
- [MONITORING_README.md](./monitoring/MONITORING_README.md)
- [Frontend RAG Clients](../frontend/src/clients/)

## 🔗 Clientes Frontend

Ver ejemplos de uso en:
- [milvus-client.js](../frontend/src/clients/milvus-client.js)
- [nebula-client.js](../frontend/src/clients/nebula-client.js)
- [rag-client.js](../frontend/src/clients/rag-client.js)

## 🚀 Mejoras Futuras

- [ ] Implementar backup automático de bases de datos
- [ ] Agregar más dashboards Grafana
- [ ] Configurar Alertmanager para notificaciones
- [ ] Implementar auto-scaling de Nebula Graph
- [ ] Agregar más índices a Milvus para mejor performance
- [ ] Implementar rate limiting en Bridge API

---

**Mantenedor**: Capibara6 Team
**Última actualización**: 2025-11-14
**SSH**: `gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"`
