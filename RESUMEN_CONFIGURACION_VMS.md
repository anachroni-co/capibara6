# 📋 Resumen de Configuración de VMs - Capibara6

## ✅ Configuración Completada

### 1. Scripts de Verificación Creados

- ✅ `verify_vm_connections.sh` - Script bash para verificar conexiones
- ✅ `verify_all_services.py` - Script Python completo con verificación de servicios
- ✅ `check_services_from_local.sh` - Script bash para verificar desde local
- ✅ `check_services_simple.py` - Script Python simple para verificación rápida
- ✅ `get_vm_ips.sh` - Script para obtener IPs de las VMs

### 2. Configuración del Frontend Actualizada

- ✅ `web/config.js` - Actualizado con configuración para desarrollo local
  - Detecta automáticamente si está en localhost
  - Conecta a las VMs correctas según el entorno
  - Incluye URLs para todos los servicios (Ollama, RAG, TTS, MCP, N8n, Bridge)

- ✅ `web/chat-app.js` - Actualizado para usar la configuración centralizada

### 3. IPs Configuradas

Según la documentación existente:

| VM | IP | Zona | Servicios |
|---|---|---|---|
| **bounty2** | `34.12.166.76` | europe-west4-a | Ollama (11434), Backend (5001) |
| **rag3** | *Por determinar* | europe-west2-c | RAG API (8000) |
| **gpt-oss-20b** | `34.175.136.104` | europe-southwest1-b | TTS (5002), MCP (5003/5010), N8n (5678), Bridge (5000) |

### 4. Archivos de Configuración de Servicios

Los siguientes archivos ya tienen IPs configuradas:

- ✅ `web/mcp-integration.js` - Usa `34.175.136.104:5003` (gpt-oss-20b)
- ✅ `web/smart-mcp-integration.js` - Usa `34.175.136.104:5010` (gpt-oss-20b)

## 🔧 Cómo Usar

### Desarrollo Local

1. **Iniciar servidor web local**:
```bash
cd web
python3 -m http.server 8000
```

2. **Abrir en navegador**:
```
http://localhost:8000/chat.html
```

3. **El frontend se conectará automáticamente a**:
   - Backend: `http://34.12.166.76:5001` (bounty2)
   - MCP: `http://34.175.136.104:5003` (gpt-oss-20b)
   - TTS: `http://34.175.136.104:5002` (gpt-oss-20b)
   - N8n: `http://34.175.136.104:5678` (gpt-oss-20b)

### Verificar Servicios

Ejecutar desde el portátil:
```bash
python3 check_services_simple.py
```

O desde las VMs directamente:
```bash
# En bounty2
curl http://localhost:11434/api/tags
curl http://localhost:5001/api/health

# En gpt-oss-20b
curl http://localhost:5000/api/health
curl http://localhost:5003/api/mcp/status
curl http://localhost:5678/healthz
```

## 📝 Próximos Pasos

### 1. Obtener IP de rag3

Ejecutar desde tu portátil:
```bash
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

Luego actualizar en `web/config.js`:
```javascript
RAG3: 'IP_OBTENIDA',
```

### 2. Verificar Servicios en Cada VM

**En bounty2**:
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Verificar Ollama
curl http://localhost:11434/api/tags
ps aux | grep ollama

# Verificar Backend
curl http://localhost:5001/api/health
ps aux | grep python
```

**En rag3**:
```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Verificar RAG API
curl http://localhost:8000/health
ps aux | grep python
```

**En gpt-oss-20b**:
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Verificar servicios
curl http://localhost:5000/api/health  # Bridge
curl http://localhost:5002/api/tts/voices  # TTS
curl http://localhost:5003/api/mcp/status  # MCP
curl http://localhost:5678/healthz  # N8n
```

### 3. Configurar Firewall de Google Cloud

Asegurar que los puertos necesarios estén abiertos:

```bash
# Permitir comunicación desde tu IP local a las VMs
gcloud compute firewall-rules create allow-local-dev \
  --allow tcp:11434,tcp:5001,tcp:5000,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges TU_IP_LOCAL/32 \
  --target-tags allow-external \
  --project mamba-001
```

### 4. Verificar Conectividad entre VMs

Las VMs deben poder comunicarse entre sí. Verificar desde cada VM:

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

### 5. Probar Conexión Completa

1. Iniciar frontend local: `python3 -m http.server 8000` en `web/`
2. Abrir `http://localhost:8000/chat.html`
3. Abrir consola del navegador (F12)
4. Verificar que se conecta a los servicios correctos
5. Enviar un mensaje de prueba

## 🐛 Troubleshooting

### Problema: Frontend no se conecta

**Solución**:
1. Verificar que las IPs en `web/config.js` son correctas
2. Verificar que los servicios están corriendo en las VMs
3. Verificar firewall de Google Cloud
4. Revisar consola del navegador para errores CORS

### Problema: CORS Error

**Solución**:
- Los servicios deben tener CORS configurado para permitir `http://localhost:8000`
- O usar un proxy local (como se hace en algunos archivos)

### Problema: Timeout en conexiones

**Solución**:
1. Verificar conectividad de red desde tu portátil
2. Verificar que los puertos están abiertos en firewall
3. Verificar que los servicios están activos en las VMs

## 📚 Documentación Relacionada

- `VM_CONNECTION_GUIDE.md` - Guía completa de conexión
- `ARCHITECTURE.md` - Arquitectura general del sistema
- `DEPLOYMENT_GUIDE.md` - Guía de despliegue
- `SERVICIOS.md` - Documentación de servicios

---

**Última actualización**: Noviembre 2025
**Estado**: ✅ Configuración básica completada - Pendiente verificación de servicios activos

