# ✅ Solución Completa CORS - bounty2

## ❌ Problema Original

```
Access to fetch at 'http://34.12.166.76:5001/api/health' from origin 'http://localhost:8000' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check
```

## ✅ Soluciones Aplicadas

### 1. Agregado Endpoint `/api/health`

El servidor tenía `/health` pero el frontend llama a `/api/health`. Se agregó el endpoint correcto.

### 2. Agregado Endpoint `/api/ai/classify`

El frontend intenta usar este endpoint pero no existía. Se agregó.

### 3. Middleware CORS Global

Se agregó un middleware `@app.before_request` que maneja todas las peticiones OPTIONS (preflight) antes de que lleguen a los endpoints.

### 4. Configuración CORS Mejorada

```python
CORS(app, 
     origins=[...],
     allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'Accept', 'Origin', 'X-Requested-With'],
     max_age=3600)
```

## 🔄 Cambios en `backend/capibara6_integrated_server.py`

1. ✅ Configuración CORS mejorada con `allow_methods` y `allow_headers`
2. ✅ Middleware `handle_preflight()` para manejar OPTIONS globalmente
3. ✅ Endpoint `/api/health` agregado
4. ✅ Endpoint `/api/ai/classify` agregado
5. ✅ Ambos endpoints soportan OPTIONS

## 🚀 Pasos para Aplicar

### Opción 1: Script Automatizado (Recomendado)

```bash
./scripts/fix_cors_bounty2.sh
```

Este script:
- ✅ Verifica y crea regla de firewall
- ✅ Reinicia el servidor con código actualizado
- ✅ Verifica que responde correctamente
- ✅ Prueba preflight request

### Opción 2: Manual

```bash
# 1. Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# 2. Detener servidor actual
screen -S capibara6-backend -X quit
# O: kill $(lsof -ti:5001)

# 3. Actualizar código
cd ~/capibara6/backend
git pull  # O copiar archivo actualizado

# 4. Verificar flask-cors instalado
source venv/bin/activate
pip install flask-cors

# 5. Reiniciar servidor
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server.py
"

# 6. Verificar
sleep 3
curl http://localhost:5001/api/health
curl -X OPTIONS http://localhost:5001/api/health \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: GET" \
  -v
```

### 3. Verificar Firewall

```bash
# Ver reglas existentes
gcloud compute firewall-rules list --project=mamba-001 --filter="name~'5001'"

# Crear si no existe
gcloud compute firewall-rules create allow-bounty2-backend-5001 \
  --allow tcp:5001 \
  --source-ranges 0.0.0.0/0 \
  --target-tags bounty2 \
  --description "Backend Capibara6 puerto 5001"
```

## ✅ Verificación Final

### Desde tu PC local:

```bash
# 1. Probar health endpoint
curl http://34.12.166.76:5001/api/health

# 2. Probar preflight (OPTIONS)
curl -X OPTIONS http://34.12.166.76:5001/api/health \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v
```

Deberías ver:
```
< HTTP/1.1 200 OK
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Methods: GET,PUT,POST,DELETE,OPTIONS
< Access-Control-Allow-Headers: Content-Type,Authorization,Accept,Origin,X-Requested-With
```

### Desde el Frontend:

El error de CORS debería desaparecer y las peticiones deberían funcionar.

## 📝 Archivos Modificados

- ✅ `backend/capibara6_integrated_server.py`
  - Configuración CORS mejorada
  - Middleware para OPTIONS
  - Endpoint `/api/health` agregado
  - Endpoint `/api/ai/classify` agregado

## ⚠️ Importante

1. **El servidor DEBE reiniciarse** para aplicar los cambios
2. **Firewall debe permitir** conexiones al puerto 5001
3. **El servidor debe escuchar en 0.0.0.0** (ya configurado en el código)
4. **flask-cors debe estar instalado** (ya está en requirements.txt)

## 🎯 Estado Actual

- ✅ Código actualizado con CORS completo
- ✅ Endpoints agregados
- ✅ Middleware para OPTIONS
- ⏳ Servidor necesita reiniciarse en bounty2
- ⏳ Firewall necesita verificación

Una vez que reinicies el servidor siguiendo los pasos arriba, el error de CORS debería desaparecer completamente.

