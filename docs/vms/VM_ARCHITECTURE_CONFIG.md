# 🏗️ Arquitectura y Configuración de VMs - Capibara6

## 📋 Resumen de VMs

### 1. **VM: bounty2** (europe-west4-a)
**IP Pública**: `34.12.166.76`  
**Propósito**: Servidor de modelos Ollama  
**Servicios**:
- **Ollama** (puerto 11434): Modelos de IA
  - `gpt-oss-20B`
  - `mixtral`
  - `phi-mini3`
- **Backend Capibara6** (puerto 5001): Servidor integrado con Ollama
- **Servidor BB** (Node.js): Posible puerto 3000 o personalizado

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### 2. **VM: rag3** (europe-west2-c)
**IP Pública**: (pendiente de obtener)  
**Propósito**: Sistema de base de datos RAG  
**Servicios**:
- Base de datos vectorial para RAG
- Sistema de embeddings y búsqueda semántica

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

### 3. **VM: gpt-oss-20b** (europe-southwest1-b)
**IP Pública**: `34.175.136.104`  
**Propósito**: Servicios de TTS, MCP, N8n y Bridge  
**Servicios**:
- **Servidor Principal** (puerto 5000): Capibara6 Main Server
- **Smart MCP Server** (puerto 5003): Contexto inteligente
- **Smart MCP Server** (puerto 5010): Análisis avanzado
- **Llama Server** (puerto 8080): Modelo gpt-oss-20b
- **TTS**: Servicio de síntesis de voz
- **N8n**: Automatización de workflows
- **Bridge**: Servicio de puente entre servicios

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

## 🔌 Arquitectura de Conexiones

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Local/Vercel)                 │
└────────────┬───────────────────────────────────────────────┘
             │
             │ HTTP/HTTPS
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│         VM: gpt-oss-20b (34.175.136.104)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Puerto 5000: Capibara6 Main Server                   │   │
│  │  - /api/chat                                         │   │
│  │  - /api/health                                       │   │
│  │  - /api/save-conversation                           │   │
│  │  - /api/save-lead                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Puerto 5003: Smart MCP Server                         │   │
│  │  - /api/mcp/status                                   │   │
│  │  - /api/mcp/tools/call                               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Puerto 5010: Smart MCP Server (alternativo)           │   │
│  │  - /api/mcp/analyze                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Puerto 8080: Llama Server (gpt-oss-20b)               │   │
│  │  - /completion                                        │   │
│  │  - /health                                            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ TTS, N8n, Bridge                                     │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────┬───────────────────────────────────────────────┘
             │
             │ HTTP (interno)
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│         VM: bounty2 (34.12.166.76)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Puerto 11434: Ollama                                  │   │
│  │  - Modelos: gpt-oss-20B, mixtral, phi-mini3          │   │
│  │  - /api/generate                                      │   │
│  │  - /api/tags                                          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Puerto 5001: Backend Capibara6                        │   │
│  │  - Integración con Ollama                            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────┬───────────────────────────────────────────────┘
             │
             │ HTTP (interno)
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│         VM: rag3 (europe-west2-c)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Base de Datos RAG                                     │   │
│  │  - Vectorial                                         │   │
│  │  - Embeddings                                        │   │
│  │  - Búsqueda semántica                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🌐 Configuración de Red

### Verificar IPs Públicas

```bash
# Bounty2
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# rag3
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# gpt-oss-20b
gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### Verificar IPs Internas

```bash
# Bounty2
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# rag3
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# gpt-oss-20b
gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"
```

### Configurar Red de Alta Velocidad

Para que las VMs se comuniquen entre sí a alta velocidad, deben estar en la misma red VPC o configurar peering de VPC:

```bash
# Verificar red VPC de cada VM
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

### Firewall Rules

Asegúrate de que las siguientes reglas de firewall permitan la comunicación:

```bash
# Permitir comunicación entre VMs (usar IPs internas)
gcloud compute firewall-rules create allow-vm-communication \
  --allow tcp:11434,tcp:5000,tcp:5001,tcp:5003,tcp:5010,tcp:8080 \
  --source-ranges 10.0.0.0/8 \
  --target-tags capibara6-vms \
  --description "Permitir comunicación entre VMs de Capibara6"

# Permitir acceso externo a servicios principales
gcloud compute firewall-rules create allow-capibara6-external \
  --allow tcp:5000,tcp:5003,tcp:5010,tcp:8080 \
  --source-ranges 0.0.0.0/0 \
  --target-tags capibara6-services \
  --description "Permitir acceso externo a servicios Capibara6"
```

## 🔧 Configuración del Frontend (Desarrollo Local)

### Archivo: `web/config.js`

```javascript
const CHATBOT_CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://34.175.136.104:5000'  // VM gpt-oss-20b - Servidor principal
        : 'https://www.capibara6.com',
    ENDPOINTS: {
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        HEALTH: '/api/health',
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        AI_GENERATE: '/api/ai/generate',
        AI_CLASSIFY: '/api/ai/classify'
    }
};
```

### Archivo: `web/mcp-integration.js`

```javascript
serverUrl: window.location.hostname === 'localhost'
    ? 'http://34.175.136.104:5003/api/mcp'  // VM gpt-oss-20b - MCP Server
    : 'https://www.capibara6.com/api/mcp'
```

### Archivo: `web/smart-mcp-integration.js`

```javascript
serverUrl: window.location.hostname === 'localhost'
    ? 'http://34.175.136.104:5010/api/mcp/analyze'  // VM gpt-oss-20b - MCP alternativo
    : 'https://www.capibara6.com/api/mcp/analyze'
```

## 🔧 Configuración del Backend

### Archivo: `backend/env.example` (actualizar con IPs reales)

```bash
# Configuración de Ollama (VM bounty2)
OLLAMA_BASE_URL=http://34.12.166.76:11434
OLLAMA_MODEL=gpt-oss-20B
# O usar IP interna si están en la misma red:
# OLLAMA_BASE_URL=http://[IP_INTERNA_BOUNTY2]:11434

# Configuración de RAG (VM rag3)
RAG_SERVER_URL=http://[IP_RAG3]/api/rag
# O usar IP interna:
# RAG_SERVER_URL=http://[IP_INTERNA_RAG3]/api/rag

# Configuración de modelo principal (VM gpt-oss-20b)
GPT_OSS_URL=http://34.175.136.104:8080
# O usar IP interna:
# GPT_OSS_URL=http://[IP_INTERNA_GPT_OSS_20B]:8080
```

## ✅ Verificación de Servicios

### Script de Verificación Completo

Ver `scripts/verify_vm_connections.sh` para verificación automatizada.

### Verificación Manual

#### 1. Verificar servicios en bounty2 (Ollama)

```bash
# Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Verificar Ollama
curl http://localhost:11434/api/tags

# Verificar backend
curl http://localhost:5001/api/health

# Ver puertos activos
sudo ss -tulnp | grep -E "(11434|5001)"
```

#### 2. Verificar servicios en rag3 (Base de datos)

```bash
# Conectarse a rag3
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Verificar base de datos
# (comandos específicos según el tipo de BD)

# Ver puertos activos
sudo ss -tulnp
```

#### 3. Verificar servicios en gpt-oss-20b (Servicios principales)

```bash
# Conectarse a gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Verificar servidor principal
curl http://localhost:5000/api/health

# Verificar MCP
curl http://localhost:5003/api/mcp/status
curl http://localhost:5010/api/mcp/analyze -X POST -H "Content-Type: application/json" -d '{"query":"test"}'

# Verificar modelo
curl http://localhost:8080/health

# Ver puertos activos
sudo ss -tulnp | grep -E "(5000|5003|5010|8080)"
```

## 🧪 Pruebas de Conectividad

### Desde tu PC Local

```bash
# Probar conexión a gpt-oss-20b
curl http://34.175.136.104:5000/api/health
curl http://34.175.136.104:5003/api/mcp/status
curl http://34.175.136.104:8080/health

# Probar conexión a bounty2 (si tiene IP pública)
curl http://34.12.166.76:11434/api/tags
curl http://34.12.166.76:5001/api/health
```

### Entre VMs (desde dentro de una VM)

```bash
# Desde gpt-oss-20b, probar conexión a bounty2 (usar IP interna)
curl http://[IP_INTERNA_BOUNTY2]:11434/api/tags

# Desde bounty2, probar conexión a rag3 (usar IP interna)
curl http://[IP_INTERNA_RAG3]/api/rag/health
```

## 📝 Próximos Pasos

1. ✅ Obtener IPs públicas e internas de las 3 VMs
2. ✅ Verificar servicios activos en cada VM
3. ✅ Configurar firewall para permitir comunicación entre VMs
4. ✅ Actualizar configuración del frontend
5. ✅ Actualizar configuración del backend
6. ✅ Probar conectividad desde local
7. ✅ Probar conectividad entre VMs
8. ✅ Verificar que el frontend puede obtener respuestas de todos los servicios

## 🚨 Troubleshooting

### Problema: No puedo conectar desde local

**Solución**:
- Verificar que las VMs tengan IPs públicas
- Verificar reglas de firewall
- Verificar que los servicios estén escuchando en `0.0.0.0` y no solo en `localhost`

### Problema: Las VMs no se comunican entre sí

**Solución**:
- Verificar que estén en la misma red VPC o configurar peering
- Usar IPs internas para comunicación entre VMs
- Verificar reglas de firewall internas

### Problema: Servicios no responden

**Solución**:
- Verificar que los servicios estén corriendo: `ps aux | grep [servicio]`
- Verificar logs: `tail -f /var/log/[servicio].log`
- Verificar puertos: `sudo ss -tulnp | grep [puerto]`

