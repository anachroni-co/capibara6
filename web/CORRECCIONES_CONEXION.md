# 🔧 Correcciones de Conexión - Errores Detectados

## ❌ Problemas Encontrados

### 1. **Smart MCP intenta conectar a localhost:5010**
**Error**: `GET http://localhost:5010/health net::ERR_CONNECTION_REFUSED`

**Causa**: El código estaba intentando conectar a `localhost:5010` en lugar de la IP de la VM `gpt-oss-20b` (34.175.136.104:5010).

**Solución**: ✅ **CORREGIDO** en `smart-mcp-integration.js`
- Ahora usa la IP de la VM desde `CHATBOT_CONFIG.SERVICE_URLS.MCP`
- Si no está disponible, usa el fallback `34.175.136.104:5010`

### 2. **RAG_API es null**
**Error**: `RAG_API: null` en la configuración

**Causa**: `RAG3_EXTERNAL` está vacío en `config.js`

**Solución**: ⚠️ **PENDIENTE** - Necesitas obtener la IP externa de rag3:
```bash
gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
```

Luego actualiza `config.js`:
```javascript
RAG3_EXTERNAL: 'IP_OBTENIDA',  // IP externa de rag3
```

### 3. **Backend Flask no responde (34.12.166.76:5001)**
**Error**: `GET http://34.12.166.76:5001/api/health net::ERR_CONNECTION_REFUSED`

**Causa**: El servicio Flask en Bounty2 no está corriendo o no está escuchando en el puerto 5001.

**Solución**: ⚠️ **VERIFICAR EN LA VM**
1. Conectar a Bounty2:
   ```bash
   gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
   ```

2. Verificar si el servicio está corriendo:
   ```bash
   # Ver procesos en puerto 5001
   sudo lsof -i :5001
   # O
   sudo netstat -tlnp | grep 5001
   ```

3. Verificar servicios en screen:
   ```bash
   screen -ls
   ```

4. Si no está corriendo, iniciarlo según la documentación del proyecto.

## ✅ Cambios Realizados

### `web/smart-mcp-integration.js`
- ✅ Corregida la función `checkSmartMCPHealth()` para usar la IP correcta de la VM
- ✅ Ahora extrae la IP desde `CHATBOT_CONFIG.SERVICE_URLS.MCP`
- ✅ Fallback a IP hardcodeada si no está disponible

## 📋 Próximos Pasos

1. **Obtener IP de rag3**:
   ```bash
   cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC
   python3 scripts/get_vm_info.py
   ```
   Esto debería generar `vm_config.json` con todas las IPs.

2. **Actualizar config.js con IP de rag3**:
   ```javascript
   RAG3_EXTERNAL: 'IP_DE_RAG3',
   ```

3. **Verificar servicios en Bounty2**:
   - Conectar a la VM
   - Verificar que el backend Flask esté corriendo en puerto 5001
   - Reiniciar si es necesario

4. **Verificar firewall**:
   - Asegurarse de que los puertos estén abiertos:
     - 5001 (Backend Flask en Bounty2)
     - 5010 (Smart MCP en gpt-oss-20b)
     - 8000 (RAG API en rag3)

## 🔍 Verificación

Después de las correcciones, deberías ver en la consola:
- ✅ `🔍 Verificando Smart MCP en: http://34.175.136.104:5010/health`
- ✅ `RAG_API: 'http://IP_RAG3:8000'` (en lugar de null)
- ✅ Conexión exitosa al backend (si está corriendo)

## 📝 Notas

- El error de conexión al backend Flask es un problema del servicio en la VM, no de la configuración del frontend.
- El frontend está correctamente configurado para conectarse a `34.12.166.76:5001`.
- Si el servicio no está corriendo, necesitas iniciarlo en la VM.

