# VM Services - Servicios Auxiliares

**IP Externa**: 34.175.136.104
**Zona**: Google Cloud
**Propósito**: Servicios auxiliares (TTS, MCP, N8N)

## 📋 Servicios

| Servicio | Puerto | Descripción | Script |
|----------|--------|-------------|--------|
| **TTS (Kyutai)** | 5002 | Text-to-Speech | `tts/kyutai_tts_server.py` |
| **MCP** | 5003 | Model Context Protocol | `mcp/smart_mcp_server.py` |
| **N8N** | 5678 | Workflow Automation | Requiere VPN/túnel |

## 🚀 Inicio Rápido

### Iniciar TTS Server

```bash
python3 tts/kyutai_tts_server.py
```

### Iniciar MCP Server

```bash
# Versión Smart MCP v2.0 (recomendado)
python3 mcp/smart_mcp_server.py

# Versión MCP v1.0 (legacy)
python3 mcp/mcp_server.py
```

### Iniciar Todos los Servicios

```bash
./scripts/start-all-services.sh
```

### Detener Todos los Servicios

```bash
./scripts/stop-all-services.sh
```

## 📁 Estructura

```
vm-services/
├── tts/                  # Text-to-Speech
│   ├── kyutai_tts_server.py  # Servidor Kyutai TTS (puerto 5002)
│   ├── coqui_tts_server.py   # Servidor Coqui TTS (alternativo)
│   ├── config/           # Configuración TTS
│   └── api/              # API endpoints TTS
├── mcp/                  # Model Context Protocol
│   ├── smart_mcp_server.py  # Smart MCP v2.0 (puerto 5003)
│   ├── mcp_server.py     # MCP v1.0 (legacy)
│   ├── config/           # Configuración MCP
│   └── api/              # API endpoints MCP
├── n8n/                  # Workflow Automation
│   ├── config/           # Configuración N8N
│   └── workflows/        # Workflows guardados
├── scripts/              # Scripts de gestión
│   ├── start-all-services.sh
│   ├── stop-all-services.sh
│   └── check-services.sh
└── deployment/           # Deploy configs
    ├── docker-compose.yml
    ├── Dockerfile.tts
    └── Dockerfile.mcp
```

## ⚙️ Configuración

### TTS - Kyutai

Variables de entorno:

```bash
# Servidor
TTS_HOST=0.0.0.0
TTS_PORT=5002

# Modelo
TTS_MODEL_NAME=kyutai-moshi
TTS_VOICES_PATH=/path/to/voices
```

Endpoints:

```
POST /tts           # Generar audio desde texto
GET  /voices        # Listar voces disponibles
POST /clone         # Clonar voz
GET  /health        # Health check
POST /preload       # Precargar modelo
```

Uso desde frontend:

```javascript
const ttsClient = new TTSClient({
    url: 'http://34.175.136.104:5002'
});

const audio = await ttsClient.speak("Hola mundo", {
    voice: 'default',
    speed: 1.0
});
```

### MCP - Model Context Protocol

Variables de entorno:

```bash
# Servidor
MCP_HOST=0.0.0.0
MCP_PORT=5003

# Configuración
MCP_ENABLED=false  # Deshabilitado por defecto
MCP_TIMEOUT=2000   # 2 segundos
```

Endpoints (Smart MCP v2.0):

```
POST /api/mcp/augment   # Aumentar query con contexto
GET  /api/mcp/health    # Health check
POST /api/mcp/analyze   # Analizar query
```

Uso desde frontend:

```javascript
const smartMCP = new SmartMCPClient({
    url: 'http://34.175.136.104:5003'
});

const result = await smartMCP.analyze("¿Qué es Python?");
// {
//   needsContext: false,
//   prompt: "¿Qué es Python?",
//   lightweight: true
// }
```

**Filosofía Smart MCP v2.0**:
- Solo agrega contexto cuando es REALMENTE necesario
- Detecta queries que requieren contexto adicional
- Evita sobrecarga de tokens innecesaria
- Fallback automático si no está disponible

### N8N - Workflow Automation

Variables de entorno:

```bash
# Servidor
N8N_HOST=0.0.0.0
N8N_PORT=5678

# Seguridad
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_password
```

**⚠️ Nota**: N8N requiere VPN o túnel SSH para acceso remoto:

```bash
# Túnel SSH desde local
ssh -L 5678:localhost:5678 user@34.175.136.104
```

## 🔧 Funcionalidades

### TTS - Text-to-Speech

**Síntesis de voz de alta calidad** con modelo Kyutai Moshi:

```python
from tts.kyutai_tts_server import TTS

tts = TTS()
audio = tts.synthesize("Hola, soy Capibara6")
# → Devuelve archivo de audio WAV
```

**Clonación de voz**:

```python
# Clonar voz desde muestra de audio
cloned_voice = tts.clone_voice("sample.wav", voice_name="custom")

# Usar voz clonada
audio = tts.synthesize("Texto personalizado", voice="custom")
```

### MCP - Análisis Inteligente

**Smart MCP v2.0** analiza queries y solo agrega contexto cuando es necesario:

```python
from mcp.smart_mcp_server import SmartMCP

mcp = SmartMCP()
result = mcp.analyze_query("¿Qué es Python?")

# Query simple → No agrega contexto
# {
#   "needsContext": False,
#   "prompt": "¿Qué es Python?",
#   "lightweight": True
# }

result = mcp.analyze_query("¿Cómo se compara Python con Java en el contexto de ML?")

# Query compleja → Agrega contexto
# {
#   "needsContext": True,
#   "prompt": "Context: [ML frameworks, Python vs Java]...\n¿Cómo se compara...",
#   "lightweight": False
# }
```

### N8N - Workflows

**Automatización de tareas** con workflows visuales:

- Integración con APIs externas
- Procesamiento de datos
- Notificaciones automatizadas
- Pipelines de ML

## 📊 Monitoreo

### Health Check de Todos los Servicios

```bash
./scripts/check-services.sh
```

### Health Check Individual

```bash
# TTS
curl http://34.175.136.104:5002/health

# MCP
curl http://34.175.136.104:5003/api/mcp/health

# N8N (requiere túnel)
curl http://localhost:5678/healthz
```

## 🐳 Deployment

### Docker Compose

```bash
cd deployment
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Individual

```bash
# TTS
docker build -f Dockerfile.tts -t capibara6-tts .
docker run -p 5002:5002 capibara6-tts

# MCP
docker build -f Dockerfile.mcp -t capibara6-mcp .
docker run -p 5003:5003 capibara6-mcp
```

## 🔍 Troubleshooting

### TTS no genera audio

```bash
# Verificar modelo cargado
curl http://34.175.136.104:5002/health

# Ver logs
tail -f logs/tts.log

# Verificar espacio en disco
df -h
```

### MCP no responde

```bash
# Verificar si está habilitado
grep MCP_ENABLED .env

# Verificar timeout
# Smart MCP tiene timeout de 2 segundos
curl -m 3 http://34.175.136.104:5003/api/mcp/health
```

### N8N no accesible

```bash
# Crear túnel SSH
ssh -L 5678:localhost:5678 user@34.175.136.104

# Verificar en navegador
open http://localhost:5678
```

## 📚 Documentación Relacionada

- [Smart MCP Integration](../frontend/src/integrations/smart-mcp-integration.js)
- [TTS Integration](../frontend/src/integrations/tts-integration.js)

## 🔗 API Examples

### TTS API

```bash
# Generar audio
curl -X POST http://34.175.136.104:5002/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hola mundo",
    "voice": "default",
    "speed": 1.0
  }' \
  --output audio.wav

# Listar voces
curl http://34.175.136.104:5002/voices
```

### MCP API

```bash
# Analizar query
curl -X POST http://34.175.136.104:5003/api/mcp/augment \
  -H "Content-Type: application/json" \
  -d '{"query": "¿Qué es Python?"}'
```

## 🧪 Tests

```bash
# Test TTS
python3 -m pytest tests/test_tts.py

# Test MCP
python3 -m pytest tests/test_mcp.py
```

## 🚀 Mejoras Futuras

- [ ] Agregar más voces a TTS
- [ ] Mejorar detección de contexto en MCP
- [ ] Integrar N8N con workflows predefinidos
- [ ] Agregar caché de audio generado
- [ ] Implementar rate limiting

---

**Mantenedor**: Capibara6 Team
**Última actualización**: 2025-11-14
