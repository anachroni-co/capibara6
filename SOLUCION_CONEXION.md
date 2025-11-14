# 🔧 Solución al Error ERR_CONNECTION_REFUSED

## ❌ Problema Actual

```
ERR_CONNECTION_REFUSED en http://34.12.166.76:5001/api/health
```

El frontend no puede conectarse al backend en bounty2.

## 🔍 Diagnóstico Paso a Paso

### Paso 1: Verificar Servicios en bounty2

Conéctate a bounty2 y ejecuta el script de verificación:

```bash
# Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Una vez dentro, ejecutar:
cd /ruta/al/proyecto
chmod +x check_bounty2_services.sh
./check_bounty2_services.sh
```

O manualmente:

```bash
# Ver procesos corriendo
ps aux | grep -E "(python|ollama|node)"

# Ver puertos abiertos
sudo netstat -tuln | grep -E "(5001|5000|11434)"
# O
sudo ss -tuln | grep -E "(5001|5000|11434)"

# Probar servicios localmente
curl http://localhost:5001/api/health
curl http://localhost:5000/api/health
curl http://localhost:11434/api/tags
```

### Paso 2: Iniciar el Servicio si No Está Corriendo

Si el servicio no está corriendo, inícialo:

```bash
# Opción 1: Backend integrado con Ollama
cd /ruta/al/proyecto/backend
python3 capibara6_integrated_server.py

# Opción 2: Servidor básico
python3 server.py

# Opción 3: Con gunicorn (producción)
gunicorn -w 4 -b 0.0.0.0:5001 capibara6_integrated_server:app
```

**IMPORTANTE**: Asegúrate de que el servidor escuche en `0.0.0.0` y no solo en `127.0.0.1`:

```python
# ✅ CORRECTO
app.run(host='0.0.0.0', port=5001)

# ❌ INCORRECTO (solo acepta conexiones locales)
app.run(host='127.0.0.1', port=5001)
```

### Paso 3: Verificar Firewall de Google Cloud

El firewall debe permitir conexiones desde tu IP al puerto 5001:

```bash
# Ver reglas de firewall actuales
gcloud compute firewall-rules list --project=mamba-001 --filter="name~allow"

# Crear regla para permitir acceso desde tu IP
# Reemplaza TU_IP_LOCAL con tu IP pública actual
gcloud compute firewall-rules create allow-backend-dev-5001 \
  --allow tcp:5001 \
  --source-ranges TU_IP_LOCAL/32 \
  --target-tags allow-external \
  --project mamba-001 \
  --description "Permitir acceso al backend desde desarrollo local"

# O permitir desde cualquier IP (menos seguro, solo para desarrollo)
gcloud compute firewall-rules create allow-backend-dev-5001-any \
  --allow tcp:5001 \
  --source-ranges 0.0.0.0/0 \
  --target-tags allow-external \
  --project mamba-001 \
  --description "Permitir acceso al backend desde cualquier IP (solo desarrollo)"
```

**Obtener tu IP pública**:
```bash
curl ifconfig.me
# O
curl ipinfo.io/ip
```

### Paso 4: Verificar IP Correcta de bounty2

```bash
# Obtener IP pública actual
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# Si la IP es diferente, actualiza web/config.js
```

### Paso 5: Probar Conexión desde tu Portátil

```bash
# Probar conectividad básica
ping 34.12.166.76

# Probar puerto 5001
curl -v http://34.12.166.76:5001/api/health

# Si no funciona, probar otros puertos
curl http://34.12.166.76:5000/api/health
curl http://34.12.166.76:11434/api/tags
```

## 🚀 Solución Rápida: Usar Ollama Directamente

Si el backend en 5001 no está disponible, puedes configurar el frontend para usar Ollama directamente:

En `web/config.js`, cambiar temporalmente:

```javascript
BACKEND_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? `http://${VM_IPS.BOUNTY2}:11434`  // Usar Ollama directamente
    : 'https://www.capibara6.com',
```

Y usar el endpoint de Ollama:
```javascript
// En lugar de /api/chat, usar /api/generate de Ollama
```

## 📋 Checklist de Verificación

- [ ] Servicio corriendo en bounty2 (puerto 5001 o 5000)
- [ ] Servicio escuchando en `0.0.0.0` (no solo `127.0.0.1`)
- [ ] Firewall configurado para permitir tu IP
- [ ] IP de bounty2 correcta en `web/config.js`
- [ ] Conectividad desde portátil verificada con `curl`
- [ ] CORS configurado en el backend

## 🆘 Si Nada Funciona

### Opción 1: Usar Proxy Local

Crear un proxy local que redirija las peticiones:

```bash
# En tu portátil, crear proxy_local.py
cat > proxy_local.py << 'EOF'
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BACKEND_URL = "http://34.12.166.76:5001"

@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
                params=request.args
            )
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
EOF

python3 proxy_local.py
```

Luego cambiar `web/config.js`:
```javascript
BACKEND_URL: 'http://localhost:5001'  // Proxy local
```

### Opción 2: Usar SSH Tunnel

```bash
# Crear túnel SSH
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001" \
  --ssh-flag="-L 5001:localhost:5001" -N

# Luego usar localhost en el frontend
BACKEND_URL: 'http://localhost:5001'
```

## 📝 Próximos Pasos

1. **Conectarse a bounty2** y verificar servicios
2. **Iniciar el servicio** si no está corriendo
3. **Configurar firewall** si es necesario
4. **Probar conexión** desde el portátil con `curl`
5. **Actualizar configuración** del frontend si es necesario

---

**Última actualización**: Noviembre 2025

