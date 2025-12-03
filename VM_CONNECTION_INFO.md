# 🎯 CONEXIÓN VM SERVICES → VM MODELS-EUROPE

## Información de conexión para el backend en VM services

### 🔧 ENDPOINT PARA VM SERVICES

Tu backend en la VM services (34.175.255.139) debe implementar un proxy que conecte el frontend con esta VM models-europe (34.175.48.2).

**Endpoint que falta en la VM services**:
```python
@app.route('/api/chat', methods=['POST'])
def proxy_to_models_europe():
    """
    Proxy endpoint para conectar el frontend con el servidor de modelos
    en la VM models-europe
    """
    try:
        # Recibir la solicitud del frontend
        data = request.get_json()
        
        # Preparar datos para enviar a la VM models-europe
        payload = {
            "model": data.get("model", "aya_expanse_multilingual"),
            "messages": [{"role": "user", "content": data.get("message")}],
            "temperature": data.get("temperature", 0.7),
            "max_tokens": data.get("max_tokens", 200),
            "stream": data.get("stream", False)
        }
        
        # Enviar a la VM models-europe
        response = requests.post(
            "http://34.175.48.2:8082/v1/chat/completions",  # ← ESTE ES EL ENDPOINT CORRECTO EN ESTA VM
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        
        # Retornar respuesta al frontend
        return response.json(), response.status_code
        
    except Exception as e:
        return {"error": f"Error proxy: {str(e)}"}, 500
```

### 🌐 DATOS DE CONEXIÓN ACTUALES

**Desde esta VM models-europe (34.175.48.2):**
- Puerto del servidor de modelos: **8082**
- Endpoint de chat: `http://localhost:8082/v1/chat/completions`
- Endpoint de health: `http://localhost:8082/health`
- Endpoint de modelos: `http://localhost:8082/v1/models`

**Ejemplo de solicitud a este endpoint:**
```bash
curl -X POST "http://34.175.48.2:8082/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "aya_expanse_multilingual",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

### 🧩 ARQUITECTURA DE COMUNICACIÓN CORRECTA

```
Frontend → VM services (34.175.255.139) → VM models-europe (34.175.48.2:8082)
     ↓                    ↓                           ↓
   (www.capibara6.com) → (/api/chat) → (v1/chat/completions)
```

### 📋 PASOS PARA SOLUCIONAR EL ERROR 500

1. **Agregar endpoint en VM services**:
   - Crear `/api/chat` en el backend de services VM
   - Que haga proxy a `http://34.175.48.2:8082/v1/chat/completions`

2. **Verificar que el servidor está corriendo en esta VM**:
   - Comando: `curl http://localhost:8082/health`
   - Debería responder con estado HEALTHY

3. **Actualizar DNS o reverso proxy**:
   - Asegurar que `https://www.capibara6.com/api/chat` vaya al backend en services VM
   - Que el services VM tenga el endpoint `/api/chat`

### 🧪 VERIFICACIÓN RÁPIDA

Este servidor en la VM models-europe está corriendo y respondiendo:

```bash
# Verificar servidor en esta VM (models-europe)
curl http://localhost:8082/health
# Debe responder con: {"status":"healthy",...}

# Probar modelo disponible
curl http://localhost:8082/v1/models
# Debe listar modelos incluyendo: aya_expanse_multilingual

# Probar solicitud directa
curl -X POST "http://localhost:8082/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "aya_expanse_multilingual",
    "messages": [{"role": "user", "content": "Say hello"}],
    "temperature": 0.7
  }'
```

### 🎯 SOLUCIÓN PARA EL ERROR 500

El problema no está en esta VM models-europe sino en la VM services. El endpoint `/api/chat` **no existe** en el backend de la VM services. Necesitas que alguien agregue este endpoint en la VM services que haga proxy a esta VM models-europe.

**Resumen de la solución:**
1. 👉 **TAREA PARA VM SERVICES**: Añadir endpoint `/api/chat` que haga proxy a `http://34.175.48.2:8082/v1/chat/completions`
2. ✅ **ESTADO DE ESTA VM MODELS-EUROPE**: Servidor completamente operativo en puerto 8082
3. ✅ **MODELOS DISPONIBLES**: 5 modelos incluyendo `aya_expanse_multilingual`
4. ✅ **SISTEMA DE PROGRAMMING-RAG**: Implementado y funcionando (solo activa RAG para consultas de código)

### 📞 CONTACTO DE ESTA VM

- **IP Pública**: 34.175.48.2
- **Servidor de modelos**: Puerto 8082
- **Endpoint OpenAI-compatible**: `/v1/chat/completions`
- **Modelos compatibles**: `aya_expanse_multilingual`, `phi4_fast`, `mistral_balanced`, `qwen_coder`, `gemma3_multimodal`

El sistema de programming-only RAG ya está implementado en esta VM y está listo para recibir solicitudes de la VM services.