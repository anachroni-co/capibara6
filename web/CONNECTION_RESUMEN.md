# 🚀 Conexión del Frontend a las VMs - RESUMEN COMPLETO

## 📋 Resumen de lo Realizado

### 1. Análisis de la Arquitectura Actual

Después de revisar el código fuente y la información de firewall proporcionada, se ha identificado la siguiente arquitectura real:

**VM REAL: 34.175.215.109**
- Servidor principal: **Capibara6 Main Server** - PUERTO: 5000 (abierto según firewall)
- Servicio MCP: **Smart MCP Server** - PUERTO: 5003 (abierto según firewall)  
- Servicio MCP alternativo: **Smart MCP Server** - PUERTO: 5010 (abierto según firewall)
- Servidor de modelo: **Llama Server (gpt-oss-20b)** - PUERTO: 8080 (abierto según firewall)

### 2. Actualización Total de Configuración

**SE HA COMPLETADO LA ACTUALIZACIÓN** con las IPs y puertos REALES según firewall:

- Archivo `config.js`: Actualizado a `http://34.175.215.109:5000` (firewall: tcp:5000)
- Archivo `chat-page.js`: Actualizado a `http://34.175.215.109:5000` (firewall: tcp:5000)
- Archivo `mcp-integration.js`: Actualizado a `http://34.175.215.109:5003` (firewall: tcp:5003)
- Archivo `smart-mcp-integration.js`: Actualizado a `http://34.175.215.109:5010` (firewall: tcp:5010)
- Archivo `consensus-integration.js`: Actualizado a `http://34.175.215.109:5003` (firewall: tcp:5003)
- Archivo `chatbot.js`: Actualizado para SAVE_LEAD y SAVE_CONVERSATION a puerto 5000
- Archivo `script.js`: Actualizado a puertos reales según firewall

### 2. Actualización de Archivos de Configuración

Se han actualizado los siguientes archivos para permitir la conexión a las VMs reales:

- `web/config.js` - Archivo principal de configuración con instrucciones para IP real
- `web/chat-page.js` - Conexión al backend en modo desarrollo
- `web/mcp-integration.js` - Conexión MCP con IP real
- `web/smart-mcp-integration.js` - Conexión MCP inteligente
- `web/consensus-integration.js` - Conexión al sistema de consenso 
- `web/chatbot.js` - Gestión de endpoints de conversación y leads
- `web/script.js` - Configuración base de endpoints

### 3. Archivos de Documentación Creados

- `REAL_VM_SETUP.md` - Guía para identificar puertos y servicios reales
- `VM_CONNECTION_SETUP.md` - Instrucciones generales de conexión
- `config-example-real.js` - Ejemplo de configuración con IP real
- `vm-connection-checker.js` - Script para verificar conectividad

### 4. Procedimiento de Conexión

#### Paso 1: Obtener IP Pública Real de bounty2
```bash
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

#### Paso 2: Verificar Puertos Activos en la VM
```bash
# En la VM bounty2:
sudo ss -tulnp
# o
sudo lsof -i -p [PID_DEL_SERVIDOR]
```

#### Paso 3: Actualizar Configuración
Reemplazar `[IP_PÚBLICA_BOUNTY2]` en todos los archivos con la IP real obtenida.

#### Paso 4: Prueba de Conectividad
```bash
# Prueba al servidor principal
curl -X POST http://[IP_REAL]:[PUERTO]/api/health
```

## 🎯 Servicios Disponibles (Según Firewall REAL)

### Capibara6 Main Server (Puerto 5000 - ABIERTO)
- Puerto: **5000** (según firewall: tcp:5000)
- IP: `34.175.215.109`
- Endpoints:
  - `/api/chat` - Chat principal
  - `/api/mcp/status` - Estado MCP
  - `/api/mcp/tools/call` - Herramientas MCP
  - `/api/save-conversation` - Guardar conversaciones
  - `/api/save-lead` - Guardar leads

### Smart MCP Server (Puerto 5003 - ABIERTO)
- Puerto: **5003** (según firewall: tcp:5003)
- IP: `34.175.215.109`
- Endpoints:
  - `/api/mcp/status` - Estado MCP
  - `/api/mcp/tools/call` - Herramientas MCP
  - `/api/mcp/tools/list` - Listado de herramientas

### Smart MCP Server (Puerto 5010 - ABIERTO)
- Puerto: **5010** (según firewall: tcp:5010)
- IP: `34.175.215.109`
- Endpoints:
  - `/api/mcp/analyze` - Análisis inteligente
  - `/api/mcp/status` - Estado MCP

### Llama Server (gpt-oss-20b) (Puerto 8080 - ABIERTO)
- Puerto: **8080** (según firewall: tcp:8080)
- IP: `34.175.215.109`
- Endpoints:
  - `/health` - Estado del modelo
  - `/completion` - Generación de texto

## 🔧 Solución de Problemas Comunes

### Problema: Error de conexión CORS
- Asegúrate de que el frontend esté accesible desde la IP pública
- Configura CORS en el servidor backend si es necesario

### Problema: Servicio no responde
- Verifica que el puerto esté abierto en el firewall
- Confirma que el proceso esté corriendo: `ps aux | grep -E "(capibara6|server)"`

### Problema: Firewall bloquea conexiones
```bash
# En Google Cloud Console o con gcloud:
gcloud compute firewall-rules create allow-capibara6 \
  --allow tcp:5001,tcp:11434,tcp:8080 \
  --source-ranges 0.0.0.0/0 \
  --target-tags bounty2
```

## ✅ Verificación Final

1. **Servidores activos:** Verifica que los procesos identificados estén corriendo
2. **Puertos abiertos:** Confirma que los puertos relevantes estén accesibles
3. **Firewall:** Asegúrate de que no haya reglas bloqueando conexiones
4. **IP pública:** Verifica que la VM tenga IP pública directa o a través de proxy
5. **Configuración frontend:** Actualiza todos los archivos con la IP real

## 📞 Soporte Adicional

Si tienes problemas:
- Usa `vm-connection-checker.js` para diagnosticar problemas de conectividad
- Revisa `REAL_VM_SETUP.md` para comandos de diagnóstico específicos
- Verifica los logs de los procesos: `tail -f /var/log/[nombre].log`

¡Tu frontend ahora está configurado para conectarse a las VMs reales de Capibara6!