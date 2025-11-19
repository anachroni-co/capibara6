# ✅ Configuración Final de VMs - Capibara6

## 📋 Resumen de la Arquitectura

### VMs Configuradas

1. **bounty2** (europe-west4-a)
   - IP Pública: `34.12.166.76`
   - Servicios: Ollama (puerto 11434) con modelos gpt-oss-20B, mixtral, phi-mini3
   - Backend Capibara6 integrado (puerto 5001)

2. **rag3** (europe-west2-c)
   - IP Pública: Pendiente de obtener
   - Servicios: Base de datos RAG (vectorial, embeddings)

3. **gpt-oss-20b** (europe-southwest1-b)
   - IP Pública: `34.175.136.104`
   - Servicios:
     - Puerto 5000: Servidor principal Capibara6
     - Puerto 5003: Smart MCP Server
     - Puerto 5010: Smart MCP Server (alternativo)
     - Puerto 8080: Llama Server (modelo gpt-oss-20b)
     - TTS, N8n, Bridge

## ✅ Cambios Realizados

### 1. Configuración del Frontend

**Archivo actualizado**: `web/config.js`
- ✅ Configurado para conectarse a `34.175.136.104:5000` en desarrollo local
- ✅ Agregada configuración completa de todas las VMs
- ✅ Documentación de servicios por VM

**Archivos ya configurados**:
- ✅ `web/mcp-integration.js` → `34.175.136.104:5003`
- ✅ `web/smart-mcp-integration.js` → `34.175.136.104:5010`

### 2. Documentación Creada

- ✅ `VM_ARCHITECTURE_CONFIG.md` - Documentación completa de arquitectura
- ✅ `scripts/verify_vm_connections.sh` - Script de verificación automatizada

## 🔧 Próximos Pasos para Completar la Configuración

### Paso 1: Obtener IP de rag3

```bash
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### Paso 2: Verificar Servicios en Cada VM

#### En bounty2 (Ollama)
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Verificar Ollama
curl http://localhost:11434/api/tags

# Verificar backend
curl http://localhost:5001/api/health

# Ver puertos activos
sudo ss -tulnp | grep -E "(11434|5001)"
```

#### En rag3 (Base de datos)
```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Ver puertos activos
sudo ss -tulnp

# Verificar servicio de base de datos
# (comandos específicos según el tipo de BD)
```

#### En gpt-oss-20b (Servicios principales)
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Verificar servidor principal
curl http://localhost:5000/api/health

# Verificar MCP
curl http://localhost:5003/api/mcp/status
curl -X POST http://localhost:5010/api/mcp/analyze \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}'

# Verificar modelo
curl http://localhost:8080/health

# Ver puertos activos
sudo ss -tulnp | grep -E "(5000|5003|5010|8080)"
```

### Paso 3: Configurar Red de Alta Velocidad

Para que las VMs se comuniquen entre sí a alta velocidad:

1. **Verificar red VPC de cada VM**:
```bash
# Verificar si están en la misma red
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].network)"

gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].network)"

gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].network)"
```

2. **Si están en redes diferentes**, configurar VPC Peering o mover las VMs a la misma red.

3. **Configurar firewall para comunicación interna**:
```bash
# Permitir comunicación entre VMs usando IPs internas
gcloud compute firewall-rules create allow-vm-internal-communication \
  --allow tcp:11434,tcp:5000,tcp:5001,tcp:5003,tcp:5010,tcp:8080 \
  --source-ranges 10.0.0.0/8 \
  --target-tags capibara6-vms \
  --description "Comunicación interna entre VMs de Capibara6"
```

### Paso 4: Actualizar Configuración del Backend

**Archivo**: `backend/.env` (crear desde `backend/env.example`)

```bash
# Configuración de Ollama (VM bounty2)
OLLAMA_BASE_URL=http://34.12.166.76:11434
# O usar IP interna si están en la misma red:
# OLLAMA_BASE_URL=http://[IP_INTERNA_BOUNTY2]:11434
OLLAMA_MODEL=gpt-oss-20B

# Configuración de RAG (VM rag3)
RAG_SERVER_URL=http://[IP_RAG3]/api/rag
# O usar IP interna:
# RAG_SERVER_URL=http://[IP_INTERNA_RAG3]/api/rag

# Configuración de modelo principal (VM gpt-oss-20b)
GPT_OSS_URL=http://34.175.136.104:8080
# O usar IP interna:
# GPT_OSS_URL=http://[IP_INTERNA_GPT_OSS_20B]:8080
```

### Paso 5: Probar Conexión desde Local

```bash
# Probar conexión a servidor principal
curl http://34.175.136.104:5000/api/health

# Probar conexión a MCP
curl http://34.175.136.104:5003/api/mcp/status

# Probar conexión a modelo
curl http://34.175.136.104:8080/health

# Probar conexión a Ollama (si tiene acceso público)
curl http://34.12.166.76:11434/api/tags
```

### Paso 6: Ejecutar Frontend Localmente

```bash
# Desde el directorio web
cd web
python3 -m http.server 8000

# Abrir en navegador
# http://localhost:8000
```

El frontend debería conectarse automáticamente a `http://34.175.136.104:5000` cuando se ejecuta desde localhost.

## 🧪 Script de Verificación

Ejecutar el script de verificación automatizada:

```bash
# Dar permisos de ejecución (si no se hizo antes)
chmod +x scripts/verify_vm_connections.sh

# Ejecutar verificación
./scripts/verify_vm_connections.sh
```

Este script:
- ✅ Obtiene las IPs públicas e internas de las 3 VMs
- ✅ Verifica conectividad a los servicios principales
- ✅ Verifica servicios activos en cada VM
- ✅ Muestra resumen de configuración

## 📝 Checklist Final

- [x] Documentación de arquitectura creada
- [x] Configuración del frontend actualizada
- [ ] IP de rag3 obtenida
- [ ] Servicios verificados en cada VM
- [ ] Red de alta velocidad configurada (VPC/Peering)
- [ ] Firewall configurado para comunicación entre VMs
- [ ] Configuración del backend actualizada con IPs reales
- [ ] Conexión desde local probada
- [ ] Frontend probado localmente con todas las conexiones

## 🚨 Troubleshooting

### Problema: No puedo conectar desde local a las VMs

**Solución**:
1. Verificar que las VMs tengan IPs públicas asignadas
2. Verificar reglas de firewall en GCloud
3. Verificar que los servicios estén escuchando en `0.0.0.0` y no solo en `localhost`

### Problema: Las VMs no se comunican entre sí

**Solución**:
1. Verificar que estén en la misma red VPC o configurar peering
2. Usar IPs internas para comunicación entre VMs
3. Verificar reglas de firewall internas

### Problema: Servicios no responden

**Solución**:
1. Verificar que los servicios estén corriendo: `ps aux | grep [servicio]`
2. Verificar logs: `tail -f /var/log/[servicio].log` o `journalctl -u [servicio]`
3. Verificar puertos: `sudo ss -tulnp | grep [puerto]`

## 📞 Comandos SSH Rápidos

```bash
# Conectar a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Conectar a rag3
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Conectar a gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

## ✅ Estado Actual

- ✅ Arquitectura documentada
- ✅ Frontend configurado para desarrollo local
- ✅ Scripts de verificación creados
- ⏳ Pendiente: Verificar servicios activos en cada VM
- ⏳ Pendiente: Configurar red de alta velocidad
- ⏳ Pendiente: Obtener IP de rag3
- ⏳ Pendiente: Probar conexiones completas

