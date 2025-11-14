# 🚀 Configuración de Conexión a VMs Reales

Este documento explica cómo obtener las IPs reales de las VMs y configurar la conexión desde el frontend local.

## 🔍 VMs Disponibles

### bounty2 - `europe-west4-a` (VM ACTUAL donde están los modelos)
**Servicios activos detectados:**
- **Ollama**: `ollama serve` (puerto por defecto 11434)
- **Backend Capibara6**: `capibara6_integrated_server_ollama.py` (posiblemente puerto 5001 u otro)
- **Servidor BB**: `node server.js` 
- **Otro servidor**: `python -m main` (posiblemente MCP)
- **Web server**: `python -m http.server 8080` (solo para desarrollo)

**Comandos útiles para identificar puertos:**
```bash
# Ver qué puertos están escuchando
sudo netstat -tuln | grep LISTEN

# Ver qué puertos están usando los procesos específicos
sudo lsof -i -c "ollama"     # Ollama
sudo lsof -i -c "python"     # Python servers
sudo lsof -i -c "node"       # Node server
```

## 📋 Pasos para Obtener IPs Reales

### 1. Obtener IP de la VM bounty2 (backend de servicios)
```bash
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### 2. Obtener IP de la VM gpt-oss-20b (modelo)
```bash
gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

## 🔄 Actualización de Configuración

Una vez que tengas las IPs reales, actualiza los archivos siguientes:

### Archivo `web/config.js`:
```javascript
BACKEND_URL: window.location.hostname === 'localhost'
    ? 'http://[IP_BOUNTY2_REAL]:5001'  // VM bounty2 en europe-west4-a
    : 'https://www.capibara6.com'
```

### Archivo `web/mcp-integration.js`:
```javascript
serverUrl: window.location.hostname === 'localhost'
    ? 'http://[IP_BOUNTY2_REAL]:5001/api/mcp'  // MCP en VM bounty2
    : 'https://www.capibara6.com/api/mcp'
```

### Archivo `web/smart-mcp-integration.js`:
```javascript
serverUrl: window.location.hostname === 'localhost'
    ? 'http://[IP_BOUNTY2_REAL]:5001/api/mcp/analyze'  // MCP en VM bounty2
    : 'https://www.capibara6.com/api/mcp/analyze'
```

## ⚙️ Comandos Útiles para Verificar Servicios

### Conectarse a la VM bounty2 (backend):
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

Luego verificar servicios:
```bash
# Verificar si el backend está corriendo
curl http://localhost:5001/health

# Verificar MCP
curl http://localhost:5001/api/mcp/status

# Verificar procesos
ps aux | grep -E "(python|server)"
```

### Conectarse a la VM gpt-oss-20b (modelos):
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

Luego verificar servicios:
```bash
# Verificar si el modelo está corriendo
curl http://localhost:8080/health

# Verificar puertos abiertos
netstat -tuln | grep -E "(8080|8081|8082)"

# Verificar procesos del modelo
ps aux | grep -E "(llama|vllm|model)"
```

## 🧪 Prueba de Conexión

Después de configurar las IPs reales, puedes usar `web/test-vm-connection.html` para verificar la conectividad.

## 🚨 Consideraciones de Seguridad

- Asegúrate de que los puertos necesarios estén abiertos en los firewalls
- Considera usar VPN o IP internas si es posible para mayor seguridad
- No subas credenciales o IPs a repositorios públicos

## 📞 Soporte

Si necesitas ayuda con la configuración, revisa:
- `BB_INTEGRATION.md` - Documentación de la arquitectura de dos servidores
- `ARCHITECTURE.md` - Documentación general de la arquitectura
- `DEPLOYMENT_GUIDE.md` - Guía de despliegue