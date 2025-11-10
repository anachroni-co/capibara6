# 🚀 Guía de Deployment - Capibara6 + Backend BB

Guía paso a paso para desplegar el sistema completo con integración BB.

---

## 📋 Prerequisitos

### Backend BB (VM 1)
- Servidor con GPU para servir modelos
- Modelos descargados y configurados:
  - **gpt-oss-20b** en puerto 8080
  - **phi-mini** en puerto 8081
  - **mixtral-8x7b** en puerto 8082
- llama-server, vllm o similar instalado

### Backend Capibara6 (VM 2 o misma VM)
- Python 3.9+
- pip instalado
- Acceso de red a Backend BB

---

## 🔧 Instalación Backend Capibara6

### 1. Clonar repositorio

```bash
git clone https://github.com/anachroni-co/capibara6.git
cd capibara6/backend
```

### 2. Instalar dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar que semantic-router esté instalado
pip list | grep semantic-router

# Si no está, instalar manualmente
pip install semantic-router fastembed
```

### 3. Configurar IPs y puertos

Edita `backend/models_config.py` con las IPs correctas:

```python
MODELS_CONFIG = {
    'gpt-oss-20b': {
        'server_url': 'http://TU_IP_BB:8080/completion',  # <-- Cambiar
    },
    'phi': {
        'server_url': 'http://TU_IP_BB:8081/completion',  # <-- Cambiar
    },
    'mixtral': {
        'server_url': 'http://TU_IP_BB:8082/completion',  # <-- Cambiar
    },
}
```

También en `backend/capibara6_integrated_server.py`:

```python
GPTOSS_API_URL = 'http://TU_IP_BB:8080/completion'  # <-- Cambiar
GPTOSS_HEALTH_URL = 'http://TU_IP_BB:8080/health'   # <-- Cambiar
```

---

## 🧪 Testing

### 1. Probar conexión con BB

```bash
cd backend
python test_bb_connection.py
```

Deberías ver:
```
✅ Conexión exitosa con gpt-oss-20b
✅ Conexión exitosa con phi
✅ Conexión exitosa con mixtral
```

Si falla, verifica:
- Backend BB está corriendo
- IPs y puertos son correctos
- Firewall permite conexiones

### 2. Probar Semantic Router

```bash
python test_semantic_router.py --interactive
```

Prueba con queries como:
- "cómo programar en Python" → debería usar gpt-oss-20b
- "escribe un cuento" → debería usar mixtral
- "qué es la fotosíntesis" → debería usar phi

---

## 🚀 Arrancar Servidor

### Desarrollo (local)

```bash
cd backend
python capibara6_integrated_server.py
```

Deberías ver:
```
============================================================
🚀 Iniciando Servidor Integrado Capibara6...
============================================================
📡 VM GPT-OSS-20B: http://TU_IP:8080/completion
🧠 Smart MCP: Activo
🎯 Semantic Router: ✅ Activo
🤖 Models Config: ✅ Activo
🌐 Puerto: 5001
✅ Conexión con VM GPT-OSS-20B: OK

📋 Semantic Router configurado:
   • Rutas: 7 (programming, creative_writing...)
   • Modelos: 3
============================================================
```

### Producción (con gunicorn)

```bash
cd backend

# Con 4 workers
gunicorn -w 4 -b 0.0.0.0:5001 capibara6_integrated_server:app

# Con logs
gunicorn -w 4 -b 0.0.0.0:5001 \
  --access-logfile access.log \
  --error-logfile error.log \
  capibara6_integrated_server:app
```

### Con systemd (recomendado)

Crea `/etc/systemd/system/capibara6.service`:

```ini
[Unit]
Description=Capibara6 Backend Server
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/a/capibara6/backend
Environment="PATH=/ruta/a/venv/bin"
ExecStart=/ruta/a/venv/bin/gunicorn -w 4 -b 0.0.0.0:5001 capibara6_integrated_server:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable capibara6
sudo systemctl start capibara6
sudo systemctl status capibara6
```

---

## 🔍 Verificación

### 1. Health check

```bash
curl http://localhost:5001/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "server": "Capibara6 Integrated Server",
  "components": {
    "gpt_oss_proxy": "✅ Activo",
    "smart_mcp": "✅ Activo",
    "coqui_tts": "✅ Activo"
  },
  "vm_status": {"status": "ok"}
}
```

### 2. Probar routing

```bash
curl -X POST http://localhost:5001/api/router/test \
  -H "Content-Type: application/json" \
  -d '{"query": "escribe un cuento sobre robots"}'
```

Respuesta esperada:
```json
{
  "query": "escribe un cuento sobre robots",
  "decision": {
    "model_id": "mixtral",
    "route_name": "creative_writing",
    "confidence": 0.9,
    "fallback": false
  }
}
```

### 3. Probar chat completo

```bash
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "explica qué es Python",
    "use_semantic_router": true
  }'
```

---

## 📊 Monitoreo

### Ver logs en tiempo real

```bash
# Si usas systemd
sudo journalctl -u capibara6 -f

# Si ejecutas directo
tail -f logs/capibara6.log
```

### Métricas importantes

- Requests por minuto
- Latencia promedio
- Errores de conexión con BB
- Uso de memoria del semantic router

---

## 🐛 Troubleshooting

### Error: "No se puede conectar con BB"

**Síntomas:**
```
❌ Error de conexión: Connection refused
```

**Soluciones:**
1. Verifica que BB esté corriendo:
   ```bash
   ssh usuario@IP_BB
   lsof -i :8080
   lsof -i :8081
   lsof -i :8082
   ```

2. Verifica conectividad:
   ```bash
   ping IP_BB
   curl http://IP_BB:8080/health
   ```

3. Verifica firewall:
   ```bash
   # En servidor BB, permitir conexiones
   sudo ufw allow from IP_CAPIBARA6 to any port 8080
   sudo ufw allow from IP_CAPIBARA6 to any port 8081
   sudo ufw allow from IP_CAPIBARA6 to any port 8082
   ```

### Error: "Semantic Router no disponible"

**Síntomas:**
```
⚠️ Semantic Router no disponible: No module named 'semantic_router'
```

**Soluciones:**
```bash
pip install semantic-router fastembed
```

### Error: "ModuleNotFoundError: No module named 'fastembed'"

**Síntomas:**
```
❌ Error inicializando router: No module named 'fastembed'
```

**Soluciones:**
```bash
pip install fastembed
```

### Semantic Router siempre usa modelo por defecto

**Síntomas:**
- Todas las queries van a gpt-oss-20b
- No se detectan rutas específicas

**Soluciones:**
1. Verifica que FastEmbed esté instalado:
   ```bash
   python -c "import fastembed; print('OK')"
   ```

2. Descarga manual de modelos de embeddings:
   ```bash
   python -c "from semantic_router.encoders import FastEmbedEncoder; FastEmbedEncoder()"
   ```

3. Revisa logs del router:
   ```bash
   python test_semantic_router.py --interactive
   ```

### Puerto 5001 ya en uso

**Síntomas:**
```
OSError: [Errno 98] Address already in use
```

**Soluciones:**
```bash
# Ver qué proceso usa el puerto
lsof -i :5001

# Matar el proceso
kill -9 PID

# O cambiar puerto en capibara6_integrated_server.py
app.run(host='0.0.0.0', port=5002)  # <-- Cambiar aquí
```

---

## 🔒 Seguridad

### 1. Firewall

Solo permitir conexiones desde IPs conocidas:

```bash
# En Backend Capibara6
sudo ufw allow from FRONTEND_IP to any port 5001

# En Backend BB
sudo ufw allow from CAPIBARA6_IP to any port 8080
sudo ufw allow from CAPIBARA6_IP to any port 8081
sudo ufw allow from CAPIBARA6_IP to any port 8082
```

### 2. Rate Limiting

Instalar flask-limiter:

```bash
pip install flask-limiter
```

En `capibara6_integrated_server.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/chat')
@limiter.limit("10 per minute")
def chat_proxy():
    # ...
```

### 3. HTTPS

Usar nginx como reverse proxy con SSL:

```nginx
server {
    listen 443 ssl;
    server_name api.capibara6.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📈 Optimizaciones

### 1. Caché de respuestas

Instalar Redis para cachear respuestas frecuentes:

```bash
pip install redis
```

### 2. Balanceo de carga

Si tienes múltiples instancias de BB, usar nginx:

```nginx
upstream bb_backends {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080;
}
```

### 3. Conexión persistente

Usar `requests.Session()` para reutilizar conexiones HTTP.

---

## 📚 Recursos

- **Documentación BB**: Consultar repositorio gmarko/BB
- **Semantic Router**: [backend/SEMANTIC_ROUTER_README.md](backend/SEMANTIC_ROUTER_README.md)
- **Arquitectura**: [BB_INTEGRATION.md](BB_INTEGRATION.md)
- **Models Config**: [backend/models_config.py](backend/models_config.py)

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa logs: `journalctl -u capibara6 -f`
2. Ejecuta tests: `python test_bb_connection.py`
3. Verifica configuración: `python -c "from models_config import *; print(get_system_info())"`
4. Consulta documentación en `backend/SEMANTIC_ROUTER_README.md`

---

**Última actualización**: Noviembre 2025
**Versión**: 1.0.0
