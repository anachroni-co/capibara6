# Integración BB + Capibara6

Arquitectura de dos servidores para separar modelos AI de servicios auxiliares.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                          FRONTEND                                │
│                      (Vercel / Web)                              │
│                   https://capibara6.com                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTPS
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CAPIBARA6 - Backend Servicios                  │
│                        VM 2: 34.175.215.109                      │
│                           Puerto 5001                            │
├─────────────────────────────────────────────────────────────────┤
│  Servidor Integrado (capibara6_integrated_server.py)            │
│  ├─ Semantic Router     → Selección automática de modelo        │
│  ├─ Smart MCP          → Contexto inteligente                   │
│  ├─ Coqui TTS          → Síntesis de voz                        │
│  └─ Consensus Server   → Manejo multi-modelo                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTP
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BB - Backend Modelos                        │
│                   VM 1: 34.175.215.109 (?)                       │
│                    Repositorio: gmarko/BB                        │
├─────────────────────────────────────────────────────────────────┤
│  Modelos AI (llama-server / vllm)                               │
│  ├─ GPT-OSS-20B    → Puerto 8080  (20B params)                  │
│  ├─ Phi-Mini       → Puerto 8081  (3.8B params)                 │
│  └─ Mixtral 8x7B   → Puerto 8082  (~47B params)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Separación de Responsabilidades

### **Capibara6 (Backend Servicios)**
**Responsabilidad**: Orquestación, servicios auxiliares y lógica de negocio

**Componentes**:
- ✅ **Semantic Router** - Selecciona qué modelo usar según la query
- ✅ **Smart MCP** - Añade contexto inteligente a las queries
- ✅ **TOON Format** - Optimización de tokens (30-60% de ahorro vs JSON)
- ✅ **Coqui TTS** - Convierte texto a voz
- ✅ **Consensus Server** - Combina respuestas de múltiples modelos
- ✅ **API Proxies** - Maneja CORS y enrutamiento

**Puerto**: 5001
**Repositorio**: anachroni-co/capibara6

---

### **BB (Backend Modelos)**
**Responsabilidad**: Servir modelos de lenguaje

**Modelos disponibles**:

| Modelo | Puerto | Parámetros | Uso Principal |
|--------|--------|------------|---------------|
| **gpt-oss-20b** | 8080 | 20B | Programación, Matemáticas, Análisis |
| **phi-mini** | 8081 | 3.8B | Facts rápidos, Conversación |
| **mixtral** | 8082 | ~47B | Creatividad, Traducción |

**Repositorio**: gmarko/BB
**Servidor**: llama-server, vllm o similar

---

## 🔄 Flujo de Request

### 1. Usuario hace una query

```
Usuario: "cómo programar en Python"
   ↓
Frontend (Vercel)
   ↓ POST /api/chat
Capibara6 Backend (5001)
```

### 2. Semantic Router selecciona modelo

```python
# En capibara6_integrated_server.py
routing_decision = semantic_router.select_model("cómo programar en Python")

# Resultado:
{
    "model_id": "gpt-oss-20b",
    "route_name": "programming",
    "confidence": 0.9,
    "reasoning": "Query clasificada como 'programming'"
}
```

### 3. Smart MCP añade contexto

```python
enhanced_message = smart_mcp.enhance_message_with_context(query)
# Añade fecha actual, identidad del bot, etc. si es relevante
```

### 4. Request al modelo en BB

```
Capibara6 Backend (5001)
   ↓ POST http://34.175.215.109:8080/completion
BB - gpt-oss-20b (8080)
   ↓ Respuesta generada
Capibara6 Backend (5001)
   ↓ Response JSON
Frontend
   ↓ Display
Usuario
```

---

## 📊 Configuración Actual

### Modelos Activos (en models_config.py)

```python
MODELS_CONFIG = {
    'gpt-oss-20b': {
        'name': 'GPT-OSS-20B',
        'server_url': 'http://34.175.215.109:8080/completion',
        'hardware': 'GPU',
        'status': 'active',
    },

    'phi': {
        'name': 'Phi-3 Mini',
        'server_url': 'http://34.175.215.109:8081/completion',
        'hardware': 'GPU',
        'status': 'active',
    },

    'mixtral': {
        'name': 'Mixtral 8x7B',
        'server_url': 'http://34.175.215.109:8082/completion',
        'hardware': 'GPU',
        'status': 'active',
    }
}
```

### Routing de Semantic Router

```python
model_mapping = {
    "programming": "gpt-oss-20b",      # Código, debugging
    "creative_writing": "mixtral",      # Cuentos, poemas
    "quick_facts": "phi",               # Definiciones rápidas
    "analysis": "gpt-oss-20b",          # Análisis profundo
    "conversation": "phi",              # Chat casual
    "math": "gpt-oss-20b",              # Matemáticas
    "translation": "mixtral",           # Traducción
    "default": "gpt-oss-20b"            # Fallback
}
```

---

## 🚀 Deployment

### **Capibara6 (Backend Servicios)**

```bash
# En VM 2
cd capibara6/backend
pip install -r requirements.txt
python capibara6_integrated_server.py

# Se inicia en puerto 5001
```

**Health check**:
```bash
curl http://localhost:5001/health
```

---

### **BB (Backend Modelos)**

```bash
# En VM 1 (configuración depende del repo BB)
cd BB

# Ejemplo con llama-server
llama-server --model gpt-oss-20b.gguf --port 8080 &
llama-server --model phi-mini.gguf --port 8081 &
llama-server --model mixtral-8x7b.gguf --port 8082 &
```

**Health check**:
```bash
curl http://localhost:8080/health
curl http://localhost:8081/health
curl http://localhost:8082/health
```

---

## 🔧 Configuración de Puertos

### VM 1 - BB (Modelos)
- **8080**: gpt-oss-20b
- **8081**: phi-mini
- **8082**: mixtral

### VM 2 - Capibara6 (Servicios)
- **5001**: Servidor integrado principal
- **5002**: Consensus server (⚠️ conflicto con TTS)
- **5003**: Smart MCP standalone
- **5010**: Smart MCP alternativo

---

## 🔌 API Endpoints

### Capibara6 → BB

**Request a modelo**:
```bash
POST http://34.175.215.109:8080/completion
Content-Type: application/json

{
  "prompt": "texto mejorado con contexto",
  "n_predict": 200,
  "temperature": 0.7,
  "top_p": 0.9,
  "repeat_penalty": 1.2,
  "stream": true
}
```

**Response del modelo**:
```json
{
  "content": "respuesta generada",
  "tokens_predicted": 150,
  "tokens_evaluated": 50
}
```

---

## 📝 Testing

### Test del Semantic Router

```bash
cd backend
python test_semantic_router.py

# Output mostrará qué modelo se selecciona para cada query
```

### Test de integración completa

```bash
# Test routing
curl -X POST http://localhost:5001/api/router/test \
  -H "Content-Type: application/json" \
  -d '{"query": "cómo programar en Python"}'

# Test chat completo
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "escribe un cuento sobre robots"}'
```

---

## 🐛 Troubleshooting

### Error: "Error de conexión con modelo"

**Causa**: BB no está respondiendo en el puerto esperado

**Solución**:
```bash
# Verificar que los modelos estén corriendo
lsof -i :8080
lsof -i :8081
lsof -i :8082

# Ver logs de BB
tail -f /var/log/bb/llama-server.log
```

### Error: "Modelo no configurado"

**Causa**: El Semantic Router seleccionó un modelo que no existe en models_config.py

**Solución**:
1. Verificar que todos los modelos en `semantic_model_router.py` existan en `models_config.py`
2. Verificar que el `status` sea `'active'`

### Performance lento

**Posibles causas**:
- Modelos grandes en CPU en vez de GPU
- Múltiples requests simultáneos sin balanceo
- Contexto muy largo

**Soluciones**:
- Verificar que BB use GPU: `nvidia-smi`
- Implementar cola de requests
- Limitar tokens de contexto

---

## 🔒 Seguridad

### Firewall
```bash
# Solo permitir conexiones desde Capibara6 a BB
# En VM de BB:
sudo ufw allow from 34.175.215.109 to any port 8080
sudo ufw allow from 34.175.215.109 to any port 8081
sudo ufw allow from 34.175.215.109 to any port 8082
```

### Rate Limiting
Implementar en Capibara6 para evitar abuse:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/chat')
@limiter.limit("10 per minute")
def chat():
    # ...
```

---

## 📈 Monitoreo

### Métricas clave

**Capibara6**:
- Requests por minuto
- Latencia de routing (ms)
- Errores de conexión a BB

**BB**:
- Tokens por segundo
- Uso de VRAM/RAM
- Queue length
- Tiempo de generación

### Logs

**Capibara6**:
```bash
tail -f backend/logs/capibara6.log
```

**BB**:
```bash
# Depende de configuración de BB
tail -f /var/log/bb/*.log
```

---

## 🔄 Próximos Pasos

- [ ] Confirmar IPs exactas de VMs
- [ ] Obtener acceso al repositorio BB
- [ ] Documentar configuración exacta de BB
- [ ] Implementar health checks automáticos
- [ ] Agregar failover si un modelo cae
- [ ] Implementar caché de respuestas
- [ ] Agregar métricas con Prometheus

---

## 📚 Referencias

- Repositorio BB: https://github.com/gmarko/BB (privado)
- Repositorio Capibara6: https://github.com/anachroni-co/capibara6
- Semantic Router: `backend/SEMANTIC_ROUTER_README.md`
- TOON Format: `TOON_GUIDE.md`
- Models Config: `backend/models_config.py`

---

**Última actualización**: Noviembre 2025
**Versión**: 1.0.0
