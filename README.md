# Capibara6 - Sistema de IA con vLLM

## Descripción General

Capibara6 es una plataforma de Inteligencia Artificial conversacional que utiliza múltiples modelos de lenguaje para proporcionar respuestas inteligentes a través de un sistema de enrutamiento semántico y consenso. El sistema ha sido migrado de Ollama a vLLM con endpoints compatibles con OpenAI.

## Arquitectura del Sistema

### Componentes Principales

1. **Backend Principal (vm-bounty2)**
   - Sistema de múltiples modelos con enrutamiento inteligente
   - Sistema de consenso con votación ponderada
   - Integración con RAG y E2B
   
2. **Sistema RAG (vm-rag3)**
   - Milvus (vector database)
   - Nebula Graph (knowledge graph)
   - PostgreSQL (metadata relacional)
   
3. **Servicios Especializados (vm-services)**
   - MCP (Smart Model Controller Protocol)
   - Kyutai TTS (síntesis de voz)
   - Coqui XTTS v2 (mejora de calidad de voz)

### Modelos Activos

1. **phi4:mini** - Modelo rápido para tareas simples (14B params)
2. **qwen2.5-coder:1.5b** - Experto en programación y tareas técnicas
3. **gpt-oss-20b** - Modelo complejo para análisis profundos
4. **mixtral** - Modelo general para tareas creativas

## Migración a vLLM

### Cambios Importantes

- **Ollama API** → **vLLM OpenAI-Compatible API**
  - Endpoints: `/api/generate` → `/v1/chat/completions`
  - Formato: `prompt`-based → `messages`-based (`{"role": "user", "content": "texto"}`)
  - Autenticación: Opcional con "Bearer EMPTY"

- **Actualización de Modelos**
  - `phi3:mini` → `phi4:mini` (de 3.8B a 14B parámetros)
  - `mistral` → `qwen2.5-coder:1.5b` (modelo experto en código)

### Configuración de Endpoints

- **vLLM Endpoint Principal**: `http://34.12.166.76:8000/v1`
- **phi4 Endpoint**: `http://34.12.166.76:8001/v1`
- **qwen2.5-coder Endpoint**: `http://34.12.166.76:8002/v1`
- **RAG3 Endpoint**: `http://10.154.0.2:8000/` (interno)

## Sistema de Consenso

### Configuración

- **Método**: Votación ponderada ('weighted')
- **Pesos**: phi4 (0.7), qwen2.5-coder (0.8), gpt-oss-20b (0.9), mixtral (0.6)
- **Min/Max modelos**: 2/3 para consenso
- **Fallback**: phi4 como modelo de respaldo

## Integración RAG-E2B-TOON

### Sistema RAG
- **MiniRAG**: Búsqueda rápida y ligera
- **FullRAG**: Búsqueda profunda con expansión de queries
- **Vector Store**: Basado en Milvus (VM RAG3)

### Sistema E2B
- **Integración automática**: Detecta cuándo se necesita ejecución de código
- **Ejecución segura**: En entornos sandbox para código propuesto

### Sistema TOON
- **Optimización de tokens**: Reducción de 30-60% en contexto RAG
- **Formateo eficiente**: Mejora la comprensión por LLMs

## Comandos Esenciales

### Iniciar vLLM
```bash
# phi4-mini
vllm serve microsoft/Phi-4-mini --host 0.0.0.0 --port 8001 --api-key EMPTY

# qwen2.5-coder-1.5b  
vllm serve Qwen/Qwen2.5-Coder-1.5B-Instruct --host 0.0.0.0 --port 8002 --api-key EMPTY

# gpt-oss-20b
vllm serve /home/elect/models/gpt-oss-20b --host 0.0.0.0 --port 8000 --api-key EMPTY
```

### Verificar Sistema
```bash
# Verificar conexión con vLLM
curl http://34.12.166.76:8000/v1/models

# Test simple
curl -X POST "http://34.12.166.76:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer EMPTY" \
  -d '{
    "model": "phi4:mini",
    "messages": [{"role": "user", "content": "Hola"}],
    "max_tokens": 50
  }'
```

## Carpetas y Archivos Clave

### Directorios Principales
- `/home/elect/capibara6/` - Directorio principal
- `/home/elect/capibara6/vm-bounty2/` - Backend con modelos
- `/home/elect/capibara6/vm-rag3/` - Sistema RAG
- `/home/elect/models/` - Modelos físicos instalados

### Archivos de Configuración 
- `model_config.json` - Configuración principal de modelos
- `server.js` - API principal Node.js  
- `vm-bounty2/servers/consensus_server.py` - Servidor de consenso
- `backend/ollama_rag_integration.py` - Integración RAG (renombrado a vLLM)

## Seguridad y Monitoreo

### Firewall
- Puertos 8000-8003 abiertos para vLLM
- IP interna RAG3 (10.154.0.2) autorizada para comunicaciones internas
- IP externa 34.12.166.76 para endpoints de servicios

### Monitoreo
- **Grafana**: http://10.154.0.2:3000 (métricas del sistema)
- **Prometheus**: http://10.154.0.2:9090 (recolección de métricas)

## Estado Actual

- ✅ Migración Ollama → vLLM completada
- ✅ Modelos phi3 → phi4 y mistral → qwen2.5-coder actualizados
- ✅ Sistema de consenso con votación ponderada operativo
- ✅ Integración RAG con E2B y TOON completamente funcional
- ✅ Backend principal con enrutamiento semántico operativo
- ✅ Frontend con chat responsive y plantillas integrado
- ✅ Servicios MCP, TTS y otros completamente operativos