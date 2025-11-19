# ✅ Solución CORS - Resumen Final

## 🔴 Problema

Error de CORS al intentar conectar desde `http://localhost:8000` al backend en `http://34.12.166.76:5001`:

```
Access to fetch at 'http://34.12.166.76:5001/api/ai/classify' from origin 'http://localhost:8000' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check
```

## ✅ Solución Aplicada

Se ha agregado configuración de CORS al archivo `backend/capibara6_integrated_server.py`:

```python
from flask_cors import CORS

CORS(app, origins=[
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://www.capibara6.com",
    "https://capibara6.com",
    "http://34.12.166.76:5001",
    "http://34.12.166.76:8000",
    "http://34.175.136.104:8000"
], supports_credentials=True)
```

## 🔄 Pasos para Aplicar la Solución

### Opción 1: Reiniciar Manualmente (Recomendado)

```bash
# 1. Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# 2. Ir al backend
cd ~/capibara6/backend

# 3. Actualizar código (si usas git)
git pull

# 4. Asegurarse de que flask-cors está instalado
source venv/bin/activate
pip install flask-cors

# 5. Detener servidor actual
screen -S capibara6-backend -X quit
# O si no está en screen:
kill $(lsof -ti:5001)

# 6. Reiniciar servidor
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server.py
"

# 7. Verificar que funciona
sleep 3
curl http://localhost:5001/api/health

# 8. Probar CORS
curl -X OPTIONS http://localhost:5001/api/ai/classify \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

### Opción 2: Usar Script Automatizado

```bash
./scripts/reiniciar_backend_con_cors.sh
```

## ✅ Verificación Final

### Desde tu PC local:

```bash
# 1. Probar health endpoint
curl http://34.12.166.76:5001/api/health

# 2. Probar preflight request (OPTIONS)
curl -X OPTIONS http://34.12.166.76:5001/api/ai/classify \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v
```

Deberías ver headers como:
```
< Access-Control-Allow-Origin: http://localhost:8000
< Access-Control-Allow-Methods: POST, OPTIONS
< Access-Control-Allow-Headers: Content-Type
```

### Desde el Frontend:

El error de CORS debería desaparecer y las peticiones deberían funcionar correctamente.

## 🔍 Troubleshooting

### Si el error persiste:

1. **Verificar que el servidor está usando el archivo correcto**:
   ```bash
   ps aux | grep python | grep -E "(server|integrated)"
   ```

2. **Verificar que flask-cors está instalado**:
   ```bash
   pip show flask-cors
   ```

3. **Ver logs del servidor**:
   ```bash
   screen -r capibara6-backend
   ```

4. **Verificar que el código está actualizado**:
   ```bash
   cd ~/capibara6/backend
   grep -A 5 "CORS(app" capibara6_integrated_server.py
   ```

### Si el servidor usa `server_gptoss.py`:

Ese archivo ya tiene CORS configurado correctamente. Solo necesitas reiniciarlo:

```bash
screen -S capibara6-backend -X quit
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    python3 server_gptoss.py
"
```

## 📝 Archivos Modificados

- ✅ `backend/capibara6_integrated_server.py` - Agregado CORS

## 📚 Documentación Relacionada

- `SOLUCION_CORS.md` - Detalles técnicos
- `COMANDOS_INICIAR_SERVICIOS.md` - Comandos para iniciar servicios
- `scripts/reiniciar_backend_con_cors.sh` - Script automatizado

## 🎯 Estado Actual

- ✅ Código actualizado con CORS
- ⏳ Servidor necesita reiniciarse para aplicar cambios
- ⏳ Verificación pendiente desde frontend

Una vez que reinicies el servidor siguiendo los pasos arriba, el error de CORS debería desaparecer.

