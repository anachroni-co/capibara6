# 🔧 Solución de Error CORS

## ❌ Error Detectado

```
Access to fetch at 'http://34.12.166.76:5001/api/ai/classify' from origin 'http://localhost:8000' 
has been blocked by CORS policy: Response to preflight request doesn't pass access control check: 
It does not have HTTP ok status.
```

## ✅ Solución Aplicada

Se ha agregado configuración de CORS al archivo `backend/capibara6_integrated_server.py`:

```python
from flask_cors import CORS

# Configurar CORS
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

## 🔄 Próximos Pasos

1. **Reiniciar el servidor en bounty2** para que los cambios surtan efecto:

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Detener el servidor actual
screen -S capibara6-backend -X quit
# O matar el proceso
kill $(lsof -ti:5001)

# Reiniciar con el código actualizado
cd ~/capibara6/backend
source venv/bin/activate
screen -dmS capibara6-backend bash -c "
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server.py
"
```

2. **Verificar que funciona**:

```bash
# Desde tu PC local
curl -X OPTIONS http://34.12.166.76:5001/api/ai/classify \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

Debería responder con headers CORS correctos.

3. **Probar desde el frontend**: El error de CORS debería desaparecer.

## 📝 Nota

Si el servidor está usando `server_gptoss.py` en lugar de `capibara6_integrated_server.py`, ese archivo ya tiene CORS configurado correctamente. Verifica qué servidor está corriendo:

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
ps aux | grep python | grep -E "(server|integrated)"
```

