# 🔧 Solución a Errores del Frontend

## ❌ Errores Detectados

1. **Error CORS**: `Access to fetch at 'http://34.12.166.76:5001/api/ai/classify' blocked by CORS policy`
2. **ERR_CONNECTION_REFUSED**: `http://34.175.136.104:5010/health` no responde
3. **Failed to fetch**: Backend no disponible o CORS mal configurado

## ✅ Soluciones

### Problema 1: Error CORS en `/api/ai/classify`

**Causa**: El frontend intenta usar `/api/ai/classify` que puede no existir o tener problemas CORS.

**Solución**: Ya actualicé `chat-page.js` para usar `/api/health` directamente. El código ahora usa:
- `/api/health` en lugar de `/api/ai/classify`
- Modo CORS correcto
- Timeout configurado

### Problema 2: Backend no responde (ERR_CONNECTION_REFUSED)

**Causa**: El servicio en `34.12.166.76:5001` no está corriendo o no está accesible.

**Solución**: Iniciar el backend en bounty2:

```bash
# Conectarse a bounty2
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001

# Una vez dentro:
cd ~/capibara6/backend
# O la ruta donde tengas el proyecto

# Iniciar backend
screen -dmS backend python3 capibara6_integrated_server.py
# O
screen -dmS backend python3 server.py

# IMPORTANTE: Verificar que escucha en 0.0.0.0
# Si el código tiene app.run(host='127.0.0.1'), cambiarlo a:
# app.run(host='0.0.0.0', port=5001)
```

### Problema 3: MCP Server no responde (puerto 5010)

**Causa**: El servicio MCP en `34.175.136.104:5010` no está corriendo.

**Solución**: Iniciar servicios en gpt-oss-20b:

```bash
# Conectarse a gpt-oss-20b
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001

# Una vez dentro:
cd ~/capibara6
./check_and_start_gpt_oss_20b.sh
```

O manualmente:

```bash
cd backend
screen -dmS mcp python3 smart_mcp_server.py
# Verificar que escucha en 0.0.0.0:5010
```

### Problema 4: Configuración CORS en Backend

**Verificar** que el backend tiene CORS configurado correctamente:

En `backend/server.py` o `backend/capibara6_integrated_server.py`:

```python
from flask_cors import CORS

app = Flask(__name__)
# CORS permitiendo localhost:8000
CORS(app, origins=[
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://www.capibara6.com"
])
```

## 🔍 Verificación Paso a Paso

### 1. Verificar que el Backend está Corriendo

```bash
# Desde tu portátil
curl http://34.12.166.76:5001/api/health

# Si no responde, conectarse a bounty2 y verificar:
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="curl http://localhost:5001/api/health"
```

### 2. Verificar CORS en el Backend

El backend debe tener CORS configurado para permitir `http://localhost:8000`. Verifica en el código del backend.

### 3. Verificar Servicios en gpt-oss-20b

```bash
# Desde tu portátil
curl http://34.175.136.104:5003/health
curl http://34.175.136.104:5010/health
curl http://34.175.136.104:5678/healthz

# Si no responden, iniciar servicios en gpt-oss-20b
```

## 🚀 Solución Rápida: Usar Proxy Local

Si los problemas de CORS persisten, puedes usar un proxy local:

```bash
# En tu portátil, crear proxy_local.py
cat > proxy_local.py << 'EOF'
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BACKEND_URL = "http://34.12.166.76:5001"

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    url = f"{BACKEND_URL}/api/{path}"
    try:
        if request.method == 'GET':
            resp = requests.get(url, params=request.args)
        else:
            resp = requests.request(
                method=request.method,
                url=url,
                headers={key: value for (key, value) in request.headers if key != 'Host'},
                data=request.get_data(),
                params=request.args,
                json=request.json if request.is_json else None
            )
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = {name: value for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers}
        return (resp.content, resp.status_code, headers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
EOF

python3 proxy_local.py
```

Luego cambiar `web/config.js`:
```javascript
BACKEND_URL: 'http://localhost:5001'  // Proxy local
```

## 📝 Checklist

- [ ] Backend corriendo en bounty2 (puerto 5001)
- [ ] Backend escuchando en 0.0.0.0 (no solo 127.0.0.1)
- [ ] CORS configurado para permitir localhost:8000
- [ ] MCP Server corriendo en gpt-oss-20b (puerto 5003 o 5010)
- [ ] Firewall configurado para permitir tu IP
- [ ] Frontend usando `/api/health` en lugar de `/api/ai/classify`

---

**Última actualización**: Noviembre 2025

