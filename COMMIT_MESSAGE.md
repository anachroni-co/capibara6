# Commit de actualizaciones del sistema Capibara6

## Resumen de cambios:

### 1. Migración de Ollama a vLLM
- Actualizado `model_config.json` para usar vLLM endpoints en lugar de Ollama
- Renombrado `OllamaClient` a `VLLMClient` en `ollama_client.js`
- Actualizado formato de requests de Ollama a OpenAI-compatible para vLLM
- Actualizado streaming API para usar formato de eventos SSE de vLLM

### 2. Actualización de modelos
- Reemplazado `phi3:mini` con `phi4:mini` (upgrade de 3.8B a 14B parametros)
- Reemplazado `mistral` con `qwen2.5-coder:1.5b` (nuevo modelo experto en código)
- Mantenido `gpt-oss:20b` como modelo complejo
- Actualizado `models_config.py` con nuevas configuraciones vLLM

### 3. Integración de RAG con E2B
- Actualizado `ollama_rag_integration.py` para usar `VLLMClient` en lugar de `OllamaClient`
- Añadida detección automática de necesidad de E2B en consultas de código
- Implementado sistema de detección de palabras clave para ejecución de código
- Integración con TOON para optimización de tokens en contextos RAG

### 4. Servidor de consenso actualizado
- Actualizado `consensus_server.py` para usar nuevas configuraciones de modelos
- Actualizado formato de API para usar endpoints vLLM
- Ajustada lógica de consenso para nuevos modelos
- Corregido import path para `models_config.py`

### 5. Router semántico mejorado
- Actualizados mapeos de rutas a nuevos modelos (phi4, qwen2.5-coder, etc.)
- Ajustada clasificación de tareas para nuevos modelos
- Integración con sistema E2B para ejecución de código cuando se detecta

### 6. Sistema de monitoreo actualizado
- Actualizados endpoints para usar vLLM en lugar de Ollama
- Ajustados health checks para nuevos endpoints
- Actualizadas configuraciones de timeout y parámetros

## Archivos modificados:
- model_config.json
- ollama_client.js → Ahora VLLMClient
- server.js
- backend/ollama_client.py → Ahora VLLMClient
- backend/ollama_rag_integration.py → Actualizado para vLLM
- backend/models_config.py
- vm-bounty2/servers/server_gptoss.py
- vm-bounty2/config/models_config.py
- vm-bounty2/servers/consensus_server.py
- backend/semantic_model_router.py

## Nuevo funcionamiento:
- El sistema ahora usa vLLM con endpoints OpenAI-compatible
- phi4:mini como modelo rápido (reemplaza phi3)
- qwen2.5-coder:1.5b como modelo experto en código (reemplaza mistral)
- Integración automática con E2B para consultas de código
- Sistema RAG completamente funcional con optimización TOON
- Sistema de consenso operativo con nuevos modelos