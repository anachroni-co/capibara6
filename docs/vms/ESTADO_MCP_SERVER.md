# 🔍 Estado Actual del MCP Server

## ❌ Diagnóstico: MCP Server NO está corriendo

### Test de Conectividad

```bash
curl -m 5 http://34.175.136.104:5010/health
# Resultado: Failed to connect - Couldn't connect to server
```

**Conclusión**: El servidor MCP no está activo en la VM `gpt-oss-20b`.

## 📍 Ubicación Correcta

### ✅ Donde DEBE estar el MCP Server:

- **VM**: `gpt-oss-20b`
- **IP**: `34.175.136.104`
- **Zona**: europe-southwest1-b
- **Puerto**: 5010 (o 5003)
- **Archivo**: `backend/smart_mcp_server.py`

### ❌ Donde NO debe estar:

- **NO** en la VM `bounty2` (34.12.166.76)
- La VM `bounty2` es solo para Backend Flask y Ollama

## 🏗️ Arquitectura del Sistema

```
Frontend (localhost:8000)
    ↓
┌─────────────────────────────────────────┐
│         VMs en GCloud                   │
├─────────────────────────────────────────┤
│                                         │
│  bounty2 (34.12.166.76)                 │
│  ├─ Backend Flask: 5001                 │
│  └─ Ollama: 11434                       │
│                                         │
│  gpt-oss-20b (34.175.136.104) ⚠️        │
│  ├─ Main Server: 5000                   │
│  ├─ MCP: 5010 ❌ NO ACTIVO              │
│  ├─ N8n: 5678                           │
│  └─ TTS: 8080                           │
│                                         │
│  rag3 (34.105.131.8)                    │
│  └─ RAG: 8000                           │
│                                         │
└─────────────────────────────────────────┘
```

## 🚀 Solución: Iniciar el MCP Server

### Paso 1: Conectarse a la VM gpt-oss-20b

```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

### Paso 2: Verificar el estado actual

```bash
# Verificar si el proceso está corriendo
ps aux | grep smart_mcp_server

# Verificar si el puerto está en uso
sudo netstat -tulpn | grep :5010

# Verificar si el archivo existe
find /home -name "smart_mcp_server.py" 2>/dev/null
# O si está en un directorio específico:
ls -la /path/to/capibara6/backend/smart_mcp_server.py
```

### Paso 3: Navegar al directorio del proyecto

```bash
# Encuentra el directorio del proyecto
find ~ -name "capibara6" -type d 2>/dev/null

# Navegar al directorio (ajusta la ruta según corresponda)
cd /home/[usuario]/capibara6/backend
# O:
cd /opt/capibara6/backend
# O:
cd ~/capibara6/backend
```

### Paso 4: Iniciar el servidor MCP

#### Opción A: Con Screen (Recomendado)

```bash
# Iniciar una sesión de screen
screen -S smart-mcp

# Activar entorno virtual si existe
source ../venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null || true

# Iniciar el servidor MCP
python3 smart_mcp_server.py --port 5010

# Presionar Ctrl+A, luego D para desconectar sin cerrar
```

#### Opción B: Con nohup

```bash
# Activar entorno virtual si existe
source venv/bin/activate 2>/dev/null || true

# Iniciar en background
nohup python3 smart_mcp_server.py --port 5010 > /tmp/mcp.log 2>&1 &

# Ver el proceso
ps aux | grep smart_mcp_server

# Ver logs
tail -f /tmp/mcp.log
```

#### Opción C: Script automatizado

```bash
# Crear script de inicio rápido
cat > start_mcp.sh << 'EOF'
#!/bin/bash
cd /path/to/capibara6/backend
source venv/bin/activate 2>/dev/null || true
python3 smart_mcp_server.py --port 5010
EOF

chmod +x start_mcp.sh

# Ejecutar con screen
screen -dmS smart-mcp bash -c "./start_mcp.sh"
```

### Paso 5: Verificar que esté corriendo

```bash
# Verificar proceso
ps aux | grep smart_mcp_server

# Verificar puerto
sudo netstat -tulpn | grep :5010

# Test local desde la VM
curl http://localhost:5010/health

# Debería responder algo como:
# {"status": "healthy", "service": "smart-mcp"}
```

### Paso 6: Verificar desde tu máquina local

```bash
# Test desde tu PC
curl http://34.175.136.104:5010/health
```

## 🔐 Verificar Firewall

Si el servidor está corriendo pero no responde desde fuera:

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

## 📝 Verificar Configuración del Frontend

Asegúrate de que el frontend esté configurado correctamente:

### En `web/smart-mcp-integration.js`:

```javascript
const SMART_MCP_CONFIG = {
    serverUrl: window.location.hostname === 'localhost' 
        ? 'http://34.175.136.104:5010/api/mcp/analyze'  // ✅ Correcto
        : 'https://www.capibara6.com/api/mcp/analyze',
    enabled: true,
    timeout: 5000
};
```

## 🧪 Test Completo

Una vez iniciado el servidor:

### 1. Test desde la VM (SSH en gpt-oss-20b):

```bash
# Health check
curl http://localhost:5010/health

# Analyze endpoint
curl -X POST http://localhost:5010/api/mcp/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### 2. Test desde tu PC local:

```bash
# Health check
curl http://34.175.136.104:5010/health

# Analyze endpoint
curl -X POST http://34.175.136.104:5010/api/mcp/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### 3. Test desde el frontend:

Abre `http://localhost:8000/chat.html` y en la consola:

```javascript
// Verificar configuración
console.log(SMART_MCP_CONFIG);

// Test de salud
fetch('http://34.175.136.104:5010/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

// Test de análisis
fetch('http://34.175.136.104:5010/api/mcp/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'test'})
})
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

## 📊 Checklist de Verificación

### En la VM gpt-oss-20b:
- [ ] Conectado por SSH a gpt-oss-20b
- [ ] Encontrado el archivo `smart_mcp_server.py`
- [ ] Servidor MCP iniciado en puerto 5010
- [ ] Proceso visible: `ps aux | grep smart_mcp_server`
- [ ] Puerto escuchando: `netstat -tulpn | grep :5010`
- [ ] Test local exitoso: `curl http://localhost:5010/health`

### Firewall:
- [ ] Regla de firewall para puerto 5010 existe
- [ ] Regla permite tráfico desde 0.0.0.0/0

### Desde Local:
- [ ] `curl http://34.175.136.104:5010/health` responde
- [ ] Endpoint de análisis funciona

### Frontend:
- [ ] Configuración apunta a `34.175.136.104:5010`
- [ ] No hay errores de conexión en consola
- [ ] MCP está habilitado (`SMART_MCP_CONFIG.enabled = true`)

## ⚠️ Notas Importantes

1. **Ubicación**: El MCP **DEBE** estar en `gpt-oss-20b`, NO en `bounty2`
2. **Puerto**: Por defecto 5010, alternativo 5003
3. **Firewall**: Debe permitir tráfico en el puerto 5010
4. **Screen**: Usa screen para mantener el servidor corriendo después de desconectarte
5. **Logs**: Revisa logs si hay errores: `screen -r smart-mcp` o `tail -f /tmp/mcp.log`

## 🎯 Resumen

**Problema Actual**: MCP Server NO está corriendo en gpt-oss-20b

**Solución**:
1. SSH a `gpt-oss-20b`
2. Navegar a directorio del proyecto
3. Iniciar `python3 smart_mcp_server.py --port 5010`
4. Verificar firewall
5. Test de conectividad

**Resultado Esperado**: 
- `curl http://34.175.136.104:5010/health` responde con éxito
- Frontend puede conectarse sin errores
- MCP proporciona contexto inteligente para las respuestas

