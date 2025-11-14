# 🔍 Verificación del Servidor MCP

## 📍 Ubicación Correcta del MCP Server

Según la arquitectura del proyecto:

### ✅ **El MCP Server DEBE estar en la VM `gpt-oss-20b`**

**VM**: `gpt-oss-20b` (`34.175.136.104`)  
**Zona**: europe-southwest1-b  
**Puerto Principal**: 5003  
**Puerto Alternativo**: 5010 (configurado actualmente)

### ❌ **NO debe estar en `bounty2`**

La VM `bounty2` es exclusivamente para:
- Backend Flask integrado (puerto 5001)
- Ollama con modelos de IA (puerto 11434)

## 🏗️ Arquitectura Actual

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (localhost:8000)                 │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
               │              │              │
     ┌─────────▼─────────┐   │   ┌──────────▼───────────┐
     │   bounty2         │   │   │   rag3               │
     │   34.12.166.76    │   │   │   34.105.131.8       │
     │                   │   │   │                      │
     │ • Backend: 5001   │   │   │ • RAG: 8000          │
     │ • Ollama: 11434   │   │   └──────────────────────┘
     └───────────────────┘   │
                             │
                  ┌──────────▼───────────┐
                  │   gpt-oss-20b        │
                  │   34.175.136.104     │
                  │                      │
                  │ • Main: 5000         │
                  │ • MCP: 5003 ⭐       │
                  │ • MCP Alt: 5010 ⭐   │
                  │ • N8n: 5678          │
                  │ • TTS: 8080          │
                  └──────────────────────┘
```

## 📝 Archivos de Configuración

### 1. Frontend: `web/smart-mcp-integration.js`

```javascript
const SMART_MCP_CONFIG = {
    serverUrl: window.location.hostname === 'localhost' 
        ? 'http://34.175.136.104:5010/api/mcp/analyze'  // ✅ VM gpt-oss-20b
        : 'https://www.capibara6.com/api/mcp/analyze',
    enabled: true,
    timeout: 5000
};
```

### 2. Backend: Archivo del servidor MCP

**Ubicación**: En la VM `gpt-oss-20b`
**Archivo**: `backend/smart_mcp_server.py`
**Puerto**: 5010 (configurado actualmente)

## 🚀 Iniciar el Servidor MCP

### Opción 1: Conectarse y verificar manualmente

```bash
# 1. Conectarse a la VM gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# 2. Verificar si el servidor MCP ya está corriendo
ps aux | grep smart_mcp_server
# O también:
sudo netstat -tulpn | grep :5010

# 3. Si NO está corriendo, navegar al directorio del proyecto
cd /path/to/capibara6/backend

# 4. Iniciar el servidor MCP con screen
screen -S smart-mcp
python3 smart_mcp_server.py --port 5010
# Presionar Ctrl+A, D para desconectar sin cerrar

# 5. Verificar que esté corriendo
curl http://localhost:5010/health
```

### Opción 2: Script automatizado

```bash
# 1. Conectarse a la VM
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# 2. Ejecutar script de inicio
screen -dmS smart-mcp bash -c "
    cd /path/to/capibara6/backend && 
    source venv/bin/activate 2>/dev/null || true &&
    python3 smart_mcp_server.py --port 5010
"

# 3. Verificar logs
screen -r smart-mcp
```

## 🧪 Verificar Conexión desde Local

### Test 1: Health Check

```bash
# Desde tu máquina local
curl http://34.175.136.104:5010/health
```

**Respuesta esperada**:
```json
{
  "status": "healthy",
  "service": "smart-mcp",
  "version": "2.0"
}
```

### Test 2: Analyze Endpoint

```bash
curl -X POST http://34.175.136.104:5010/api/mcp/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "¿Qué es Python?"}'
```

### Test 3: Desde el Frontend

Abre la consola del navegador en `http://localhost:8000/chat.html`:

```javascript
// Verificar configuración
console.log(SMART_MCP_CONFIG);

// Test de salud
await fetch('http://34.175.136.104:5010/health')
  .then(r => r.json())
  .then(console.log);

// Test de análisis
await fetch('http://34.175.136.104:5010/api/mcp/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'test'})
}).then(r => r.json()).then(console.log);
```

## 🔐 Verificar Firewall

El puerto 5010 debe estar abierto en el firewall de GCloud:

```bash
# Ver reglas de firewall
gcloud compute firewall-rules list --project=mamba-001 | grep 5010

# Si no existe, crear regla
gcloud compute firewall-rules create allow-smart-mcp-5010 \
  --project=mamba-001 \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5010 \
  --source-ranges=0.0.0.0/0 \
  --description="Smart MCP Server en gpt-oss-20b"
```

## 📊 Diagnóstico de Problemas

### Problema 1: "Connection Refused"

**Causa**: El servidor MCP no está corriendo en `gpt-oss-20b`

**Solución**:
```bash
# Conectarse a gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Verificar proceso
ps aux | grep smart_mcp_server

# Si no está corriendo, iniciarlo
cd /path/to/capibara6/backend
screen -S smart-mcp
python3 smart_mcp_server.py --port 5010
```

### Problema 2: "404 Not Found"

**Causa**: El endpoint no existe o la URL es incorrecta

**Solución**:
- Verificar que el archivo `smart_mcp_server.py` exista en `gpt-oss-20b`
- Verificar que los endpoints estén correctamente configurados
- El endpoint correcto es: `/api/mcp/analyze` (no solo `/analyze`)

### Problema 3: Timeout

**Causa**: Firewall bloqueando el puerto o servidor lento

**Solución**:
```bash
# Verificar firewall
gcloud compute firewall-rules list --project=mamba-001

# Verificar que el puerto esté escuchando
sudo netstat -tulpn | grep :5010

# Verificar logs del servidor
screen -r smart-mcp
```

### Problema 4: CORS Error

**Causa**: El servidor MCP no tiene CORS configurado

**Solución**: Verificar que `smart_mcp_server.py` tenga:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:8000', 'https://www.capibara6.com'])
```

## 📋 Checklist de Verificación

### En la VM `gpt-oss-20b`:
- [ ] Servidor MCP corriendo en puerto 5010
- [ ] Proceso visible con `ps aux | grep smart_mcp`
- [ ] Puerto escuchando: `netstat -tulpn | grep :5010`
- [ ] Health endpoint responde: `curl http://localhost:5010/health`

### Firewall de GCloud:
- [ ] Regla para puerto 5010 existe
- [ ] Regla permite tráfico desde `0.0.0.0/0` o tu IP

### Desde Local:
- [ ] `curl http://34.175.136.104:5010/health` responde
- [ ] Frontend puede conectarse (sin CORS errors)
- [ ] Endpoint de análisis funciona

### En el Frontend:
- [ ] `SMART_MCP_CONFIG.serverUrl` apunta a `34.175.136.104:5010`
- [ ] `SMART_MCP_CONFIG.enabled` es `true`
- [ ] No hay errores en la consola del navegador

## 🎯 Resumen

| Aspecto | Valor Correcto |
|---------|---------------|
| **VM Correcta** | `gpt-oss-20b` ❌ NO `bounty2` |
| **IP** | `34.175.136.104` |
| **Puerto** | `5010` (alternativo: 5003) |
| **Endpoint Health** | `http://34.175.136.104:5010/health` |
| **Endpoint Analyze** | `http://34.175.136.104:5010/api/mcp/analyze` |
| **Archivo Backend** | `backend/smart_mcp_server.py` |
| **Screen Session** | `smart-mcp` |

## 🚀 Próximos Pasos

1. **Conectarse a `gpt-oss-20b`**:
   ```bash
   gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
   ```

2. **Verificar si MCP está corriendo**:
   ```bash
   ps aux | grep smart_mcp_server
   sudo netstat -tulpn | grep :5010
   ```

3. **Si NO está corriendo, iniciarlo**:
   ```bash
   cd /path/to/capibara6/backend
   screen -S smart-mcp
   python3 smart_mcp_server.py --port 5010
   # Ctrl+A, D para desconectar
   ```

4. **Verificar desde local**:
   ```bash
   curl http://34.175.136.104:5010/health
   ```

5. **Probar desde el frontend**:
   - Abrir `http://localhost:8000/chat.html`
   - Verificar consola para errores de MCP

