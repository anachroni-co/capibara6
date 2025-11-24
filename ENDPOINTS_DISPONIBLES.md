# 📋 Endpoints Disponibles en el Servidor Integrado

## ✅ Endpoints que SÍ existen

### Chat
- `POST /api/chat` - Chat principal con el modelo
- `POST /api/chat/stream` - Chat con streaming (si está disponible)

### Health Check
- `GET /health` - Verificar estado del servidor
  - **NOTA**: Es `/health`, NO `/api/health`

### AI
- `POST /api/ai/generate` - Generar texto usando CTM y Ollama

### MCP (Model Context Protocol)
- `GET /api/mcp/status` - Estado del conector MCP
- `POST /api/mcp/initialize` - Inicializar MCP
- `GET /api/mcp/tools/list` - Listar herramientas
- `POST /api/mcp/tools/call` - Ejecutar herramienta
- `POST /api/mcp/analyze` - Análisis inteligente

### TTS (Text-to-Speech)
- `POST /api/tts/speak` - Síntesis de voz
- `GET /api/tts/voices` - Lista de voces disponibles
- `POST /api/tts/clone` - Clonación de voz

### Otros
- `POST /api/save-conversation` - Guardar conversación
- `POST /api/save-lead` - Guardar leads
- `GET /api/models` - Información de modelos disponibles

## ❌ Endpoints que NO existen

- `POST /api/ai/classify` - **NO EXISTE**
  - Usar `/health` para verificar conexión en su lugar

## 🔧 Correcciones Aplicadas

1. ✅ `web/config.js` - Eliminado `/api/ai/classify` de los endpoints
2. ✅ `web/chat-page.js` - Actualizado para usar solo `/health` para verificar conexión
3. ✅ Endpoint `/health` corregido (no `/api/health`)

## 🧪 Pruebas

### Verificar endpoints disponibles

```bash
# Health check (debe funcionar)
curl http://localhost:8001/health

# Chat (debe funcionar)
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola"}'

# AI Generate (debe funcionar)
curl -X POST http://localhost:8001/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'
```

### Endpoints que NO funcionan

```bash
# Este NO existe
curl http://localhost:8001/api/ai/classify
# Debe devolver 404

# Este tampoco existe
curl http://localhost:8001/api/health
# Debe devolver 404 (usar /health en su lugar)
```

