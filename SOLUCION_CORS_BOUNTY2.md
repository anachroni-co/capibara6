# 🔧 Solución CORS en bounty2 (Puerto 5001)

## ❌ Problema

Error de CORS al intentar conectar desde `http://localhost:8000`:

```
Access to fetch at 'http://34.12.166.76:5001/api/health' from origin 'http://localhost:8000' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check: 
It does not have HTTP ok status.
```

## ✅ Solución Aplicada

### 1. Agregado endpoint `/api/health`

El servidor tenía `/health` pero el frontend llama a `/api/health`. Se agregó el endpoint correcto.

### 2. Mejorada configuración CORS

- ✅ Agregado manejo explícito de peticiones OPTIONS (preflight)
- ✅ Configurado `allow_methods` para incluir OPTIONS
- ✅ Configurado `allow_headers` completo
- ✅ Agregado `max_age` para cachear preflight

### 3. Cambios en `backend/capibara6_integrated_server.py`

```python
# Endpoint de health con soporte OPTIONS
@app.route('/health', methods=['GET', 'OPTIONS'])
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    if request.method == 'OPTIONS':
        # Responder correctamente al preflight
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response
    # ... resto del código
```

## 🔄 Próximos Pasos

### 1. Reiniciar el servidor en bounty2

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Detener servidor actual
screen -S capibara6-backend -X quit
# O: kill $(lsof -ti:5001)

# Actualizar código
cd ~/capibara6/backend
git pull  # O copiar el archivo actualizado

# Reiniciar
source venv/bin/activate
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server.py
"
```

### 2. Verificar Firewall en GCloud

```bash
# Ver reglas de firewall existentes
gcloud compute firewall-rules list --project=mamba-001 --filter="name~'5001'"

# Crear regla si no existe
gcloud compute firewall-rules create allow-bounty2-backend-5001 \
  --allow tcp:5001 \
  --source-ranges 0.0.0.0/0 \
  --target-tags bounty2 \
  --description "Backend Capibara6 en puerto 5001"
```

### 3. Verificar que el servidor escucha en 0.0.0.0

```bash
# En bounty2
sudo ss -tulnp | grep 5001
# Debe mostrar: 0.0.0.0:5001, no 127.0.0.1:5001
```

### 4. Probar Preflight Request

```bash
# Desde tu PC local
curl -X OPTIONS http://34.12.166.76:5001/api/health \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v
```

Deberías ver headers CORS en la respuesta:
```
< HTTP/1.1 200 OK
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Methods: GET, POST, OPTIONS
< Access-Control-Allow-Headers: Content-Type, Authorization
```

## 🧪 Verificación Final

### Probar desde el navegador:

```javascript
// En consola del navegador (http://localhost:8000)
fetch('http://34.12.166.76:5001/api/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

Debería funcionar sin errores de CORS.

## 📝 Archivos Modificados

- ✅ `backend/capibara6_integrated_server.py`
  - Agregado endpoint `/api/health`
  - Mejorada configuración CORS
  - Agregado manejo explícito de OPTIONS

## ⚠️ Notas Importantes

1. **El servidor debe reiniciarse** para aplicar los cambios
2. **Firewall debe permitir** conexiones al puerto 5001
3. **El servidor debe escuchar en 0.0.0.0** y no solo en localhost
4. **CORS debe responder correctamente** a peticiones OPTIONS

## ✅ Checklist

- [x] Agregado endpoint `/api/health`
- [x] Mejorada configuración CORS
- [x] Agregado manejo de OPTIONS
- [ ] Reiniciar servidor en bounty2
- [ ] Verificar firewall
- [ ] Probar conexión desde frontend

