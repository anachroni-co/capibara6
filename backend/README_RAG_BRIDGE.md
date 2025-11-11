# 🚀 RAG Bridge - Quick Start Guide

## Resumen

Esta integración permite que los modelos de Ollama en **bounty2** accedan al sistema RAG completo en **RAG3** para enriquecer sus respuestas con datos personales del usuario.

## Instalación Rápida en bounty2

```bash
cd /home/elect/capibara6/backend

# 1. Ejecutar script de configuración
./setup_rag_bridge.sh

# 2. Verificar que todo funciona
python3 rag_client.py
python3 ollama_rag_integration.py
```

## Uso Básico

### Opción 1: Cliente Simple

```python
from rag_client import get_rag_context

# Obtener contexto RAG para una consulta
context = get_rag_context("¿Qué he hablado sobre IA?")

# Agregar contexto al prompt de Ollama
full_prompt = f"""
Información del usuario:
{context}

---

Usuario: ¿Qué he hablado sobre IA?
"""
```

### Opción 2: Integración Completa (Recomendado)

```python
from ollama_rag_integration import create_integrated_client
import json

# Cargar configuración
with open("../model_config.json") as f:
    ollama_config = json.load(f)

# Crear cliente integrado
client = create_integrated_client(ollama_config)

# Generar respuesta (usa RAG automáticamente cuando es necesario)
response = client.generate_with_rag(
    prompt="¿Qué he comentado sobre machine learning?",
    model_tier="balanced"
)

print(f"Respuesta: {response['response']}")
print(f"RAG usado: {response['rag_used']}")
```

### Opción 3: Servidor Flask Completo

```bash
# Iniciar servidor de ejemplo
python3 example_rag_bridge_server.py

# En otro terminal, probar
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué he guardado sobre IA?"}'
```

## Arquitectura

```
bounty2 (Ollama)  ──────►  RAG3 (Sistema RAG)
     │                           │
     │    HTTP Request           │
     │    10.154.0.2:8000        │
     │                           │
     ├─ rag_client.py           ├─ Milvus (vectors)
     ├─ ollama_rag_integration  ├─ PostgreSQL (data)
     └─ example_server.py       └─ Nebula (graph)
```

## Endpoints del Servidor de Ejemplo

- `GET /` - Información del servidor
- `GET /api/health` - Health check (Ollama + RAG)
- `POST /api/chat` - Chat con integración RAG
- `POST /api/chat/stream` - Chat con streaming
- `GET /api/rag/status` - Estado de conexión RAG
- `POST /api/rag/search` - Búsqueda directa en RAG
- `GET /api/models` - Listar modelos Ollama

## Ejemplos de Uso

### Ejemplo 1: Chat Normal (Sin RAG)

```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué es machine learning?",
    "model_tier": "fast_response"
  }'
```

Respuesta:
```json
{
  "response": "Machine learning es una rama de la inteligencia artificial...",
  "model": "phi3:mini",
  "rag_used": false,
  "metadata": {...}
}
```

### Ejemplo 2: Chat Personal (Con RAG)

```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué he comentado sobre machine learning?",
    "model_tier": "balanced",
    "use_rag": true
  }'
```

Respuesta:
```json
{
  "response": "Basándome en tus conversaciones anteriores, has comentado sobre...",
  "model": "mistral:latest",
  "rag_used": true,
  "rag_metadata": {
    "confidence": 0.6,
    "context_length": 1234
  }
}
```

### Ejemplo 3: Streaming

```bash
curl -X POST http://localhost:5001/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explícame qué es RAG",
    "model_tier": "balanced"
  }'
```

### Ejemplo 4: Búsqueda RAG Directa

```bash
curl -X POST http://localhost:5001/api/rag/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "IA y embeddings",
    "n_results": 5,
    "use_graph": true
  }'
```

## Configuración Avanzada

### Variables de Entorno

```bash
# .env o .env.rag_bridge
RAG_API_URL=http://10.154.0.2:8000
OLLAMA_ENDPOINT=http://localhost:11434
DEFAULT_MODEL_TIER=balanced
RAG_THRESHOLD=0.3
RAG_CONTEXT_MAX_LENGTH=1500
RAG_TIMEOUT=30
PORT=5001
DEBUG=false
```

### Personalizar Detección RAG

```python
from ollama_rag_integration import OllamaRAGIntegration

# Crear con umbral personalizado
integration = OllamaRAGIntegration(
    rag_threshold=0.4,  # Requiere más confianza
    context_max_length=2000  # Más contexto
)

# Verificar si una consulta usaría RAG
should_use, score = integration.should_use_rag("mi pregunta")
print(f"Usar RAG: {should_use}, Score: {score}")
```

### Agregar Patrones Personalizados

```python
# En ollama_rag_integration.py
OllamaRAGIntegration.RAG_TRIGGERS.extend([
    r"\b(proyecto|trabajo)\b",
    r"mis (notas|apuntes|documentos)"
])
```

## Monitoreo y Logs

```bash
# Ver logs del servidor
tail -f /var/log/capibara6/server.log

# Verificar conectividad
curl http://localhost:5001/api/health

# Verificar estado RAG
curl http://localhost:5001/api/rag/status
```

## Troubleshooting

### Error: "Connection refused to RAG3"

```bash
# Verificar conectividad
ping 10.154.0.2

# Verificar que RAG API está corriendo
curl http://10.154.0.2:8000/health

# Verificar firewall
gcloud compute firewall-rules list | grep rag3
```

### Error: "Ollama not responding"

```bash
# Verificar proceso de Ollama
ps aux | grep ollama

# Reiniciar Ollama
sudo systemctl restart ollama

# Verificar puerto
curl http://localhost:11434/api/tags
```

### RAG siempre retorna contexto vacío

```python
# Reducir umbral de similitud
rag_client.search_rag(
    query="mi consulta",
    n_results=10,  # Más resultados
    use_graph=False  # Desactivar grafo si es lento
)
```

## Performance

- **Latencia VM-to-VM:** ~9ms (red privada GCloud)
- **Búsqueda RAG:** 100-500ms (dependiendo de complejidad)
- **Generación Ollama:** Variable según modelo
  - phi3:mini: 50-200ms
  - mistral: 200-800ms
  - gpt-oss:20b: 1-5s

## Seguridad

- ✅ Comunicación por red privada de GCloud
- ✅ Sin exposición a Internet
- ✅ Firewall de GCloud
- ⚠️ Considera agregar autenticación con API keys para producción

## Más Información

- **Documentación completa:** `OLLAMA_RAG_BRIDGE.md`
- **Configuración de VM:** `web/REAL_VM_SETUP.md`
- **API del sistema RAG:** http://10.154.0.2:8000/docs (si tienes FastAPI docs habilitado)

## Soporte

Si encuentras problemas:

1. Ejecuta el script de diagnóstico: `./setup_rag_bridge.sh`
2. Revisa los logs del servidor
3. Verifica la conectividad de red
4. Consulta la documentación completa

---

*Última actualización: 2025-11-11*
