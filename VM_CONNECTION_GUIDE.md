# 🔌 Guía de Conexión de VMs - Capibara6

Este documento explica cómo verificar y configurar las conexiones entre las 3 VMs de Google Cloud y el frontend local.

## 📋 Arquitectura de VMs

### VM 1: **bounty2** (europe-west4-a)
**Propósito**: Servidor de modelos Ollama
- **Servicios**:
  - Ollama (puerto 11434) - Modelos: gpt-oss-20B, mixtral, phi-mini3
  - Backend Capibara6 (puerto 5001)
  - Backend alternativo (puerto 5000)

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### VM 2: **rag3** (europe-west2-c)
**Propósito**: Sistema de base de datos RAG
- **Servicios**:
  - RAG API (puerto 8000)
  - PostgreSQL (puerto 5432, si aplica)

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

### VM 3: **gpt-oss-20b** (europe-southwest1-b)
**Propósito**: Servicios TTS, MCP, N8n y Bridge
- **Servicios**:
  - Bridge/Main Server (puerto 5000)
  - TTS Server (puerto 5002)
  - MCP Server (puerto 5003)
  - MCP Server alternativo (puerto 5010)
  - N8n (puerto 5678)
  - Modelo (puerto 8080, si aplica)

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

## 🔍 Verificación de IPs

### Obtener IPs de las VMs

```bash
# IP de bounty2
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# IP de rag3
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# IP de gpt-oss-20b
gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

Si no hay IP pública, usar IP interna:
```bash
--format="value(networkInterfaces[0].networkIP)"
```

## 🛠️ Scripts de Verificación

### Script Python (Recomendado)
```bash
python3 verify_all_services.py
```

Este script:
- ✅ Obtiene las IPs de las 3 VMs
- ✅ Verifica servicios activos en cada VM
- ✅ Verifica conectividad entre VMs
- ✅ Genera configuración automática para el frontend

### Script Bash
```bash
./verify_vm_connections.sh
```

## 🔧 Configuración del Frontend

### Para Desarrollo Local

El frontend debe conectarse a las VMs cuando se ejecuta en `localhost`. 

**Archivo: `web/config.js`**

```javascript
const CHATBOT_CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://[IP_BOUNTY2]:5001'  // IP de bounty2
        : 'https://www.capibara6.com',
    // ... resto de configuración
};
```

**Archivo: `web/mcp-integration.js`**

```javascript
serverUrl: window.location.hostname === 'localhost'
    ? 'http://[IP_GPT_OSS_20B]:5003/api/mcp'  // IP de gpt-oss-20b
    : 'https://www.capibara6.com/api/mcp'
```

**Archivo: `web/smart-mcp-integration.js`**

```javascript
serverUrl: window.location.hostname === 'localhost'
    ? 'http://[IP_GPT_OSS_20B]:5010/api/mcp/analyze'  // IP de gpt-oss-20b
    : 'https://www.capibara6.com/api/mcp/analyze'
```

### Configuración Automática

Después de ejecutar `verify_all_services.py`, se genera automáticamente:
- `web/config-vm-auto.js` - Configuración con las IPs detectadas

Incluir este archivo en `chat.html` antes de otros scripts:
```html
<script src="config-vm-auto.js"></script>
```

## 🌐 Verificación de Conectividad entre VMs

### Red de Alta Velocidad en Google Cloud

Las VMs en Google Cloud pueden comunicarse entre sí usando:
1. **IPs internas** (recomendado para mejor rendimiento)
2. **IPs públicas** (si no están en la misma red)

### Verificar Conectividad

Desde cada VM, verificar conectividad a las otras:

```bash
# Desde bounty2
ping [IP_RAG3]
ping [IP_GPT_OSS_20B]

# Desde rag3
ping [IP_BOUNTY2]
ping [IP_GPT_OSS_20B]

# Desde gpt-oss-20b
ping [IP_BOUNTY2]
ping [IP_RAG3]
```

### Configurar Firewall de Google Cloud

Asegúrate de que las reglas de firewall permitan comunicación entre VMs:

```bash
# Permitir comunicación entre VMs en el mismo proyecto
gcloud compute firewall-rules create allow-internal \
  --allow tcp:11434,tcp:5001,tcp:8000,tcp:5002,tcp:5003,tcp:5678 \
  --source-ranges 10.0.0.0/8 \
  --target-tags internal \
  --project mamba-001
```

## 🔍 Verificación de Servicios

### En bounty2 (Ollama)

```bash
# Verificar Ollama
curl http://localhost:11434/api/tags

# Verificar Backend
curl http://localhost:5001/api/health

# Ver procesos activos
ps aux | grep -E "(ollama|python|node)"
sudo netstat -tuln | grep -E "(11434|5001|5000)"
```

### En rag3 (RAG)

```bash
# Verificar RAG API
curl http://localhost:8000/health

# Ver procesos activos
ps aux | grep -E "(python|uvicorn|fastapi)"
sudo netstat -tuln | grep -E "(8000|5432)"
```

### En gpt-oss-20b (Servicios)

```bash
# Verificar Bridge
curl http://localhost:5000/api/health

# Verificar TTS
curl http://localhost:5002/api/tts/voices

# Verificar MCP
curl http://localhost:5003/api/mcp/status

# Verificar N8n
curl http://localhost:5678/healthz

# Ver procesos activos
ps aux | grep -E "(python|node|n8n)"
sudo netstat -tuln | grep -E "(5000|5002|5003|5010|5678)"
```

## 🧪 Prueba desde el Portátil Local

### 1. Verificar que las IPs públicas sean accesibles

```bash
# Desde tu portátil
ping [IP_BOUNTY2]
ping [IP_RAG3]
ping [IP_GPT_OSS_20B]
```

### 2. Verificar servicios HTTP

```bash
# Ollama en bounty2
curl http://[IP_BOUNTY2]:11434/api/tags

# Backend en bounty2
curl http://[IP_BOUNTY2]:5001/api/health

# RAG en rag3
curl http://[IP_RAG3]:8000/health

# Servicios en gpt-oss-20b
curl http://[IP_GPT_OSS_20B]:5000/api/health
curl http://[IP_GPT_OSS_20B]:5003/api/mcp/status
curl http://[IP_GPT_OSS_20B]:5678/healthz
```

### 3. Probar Frontend Local

```bash
# Iniciar servidor web local
cd web
python3 -m http.server 8000

# Abrir en navegador
# http://localhost:8000/chat.html
```

El frontend debería conectarse automáticamente a las VMs si la configuración está correcta.

## 📝 Checklist de Verificación

- [ ] IPs de las 3 VMs obtenidas
- [ ] Servicios verificados en bounty2 (Ollama, Backend)
- [ ] Servicios verificados en rag3 (RAG API)
- [ ] Servicios verificados en gpt-oss-20b (TTS, MCP, N8n, Bridge)
- [ ] Conectividad entre VMs verificada
- [ ] Firewall configurado correctamente
- [ ] Frontend configurado con IPs correctas
- [ ] Prueba desde portátil local exitosa

## 🐛 Troubleshooting

### Problema: No se puede obtener IP de VM

**Solución**:
- Verificar que tienes permisos en el proyecto `mamba-001`
- Verificar que la VM existe y está activa
- Usar `gcloud compute instances list` para ver todas las VMs

### Problema: Servicios no responden

**Solución**:
1. Conectarse a la VM via SSH
2. Verificar que los servicios están corriendo: `ps aux | grep [servicio]`
3. Verificar puertos abiertos: `sudo netstat -tuln`
4. Verificar logs: `journalctl -u [servicio]` o `tail -f [log_file]`

### Problema: Frontend no se conecta

**Solución**:
1. Verificar configuración en `web/config.js`
2. Verificar que las IPs son correctas
3. Verificar CORS en el backend
4. Abrir consola del navegador para ver errores
5. Verificar que los puertos están abiertos en el firewall de Google Cloud

### Problema: Conectividad lenta entre VMs

**Solución**:
- Usar IPs internas en lugar de IPs públicas
- Verificar que las VMs están en la misma región o regiones cercanas
- Configurar red VPC compartida si es necesario

## 📚 Archivos de Configuración

- `web/config.js` - Configuración principal del frontend
- `web/config-vm-auto.js` - Configuración generada automáticamente
- `web/mcp-integration.js` - Integración MCP
- `web/smart-mcp-integration.js` - Integración Smart MCP
- `backend/models_config.py` - Configuración de modelos
- `backend/env.example` - Variables de entorno de ejemplo

## 🆘 Soporte

Si encuentras problemas:
1. Ejecuta `python3 verify_all_services.py` para diagnóstico
2. Revisa los logs en cada VM
3. Verifica la configuración de firewall en Google Cloud
4. Consulta la documentación en `ARCHITECTURE.md` y `DEPLOYMENT_GUIDE.md`

---

**Última actualización**: Noviembre 2025
**Versión**: 1.0.0

