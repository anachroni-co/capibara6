# 🔗 Configuración de Conexiones entre VMs - Capibara6

## 📋 Arquitectura de las 3 VMs

### VM 1: **bounty2** (europe-west4-a)
**Propósito**: Ollama con modelos de IA
**Servicios**:
- **Ollama**: Puerto 11434 (modelos: gpt-oss-20B, mixtral, phi-mini3)
- **Backend Capibara6**: Puerto 5001 (servidor integrado con Ollama)
- **Servidor BB**: Puerto variable (Node.js)
- **Servidor HTTP simple**: Puerto 8000 (desarrollo)

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### VM 2: **rag3** (europe-west2-c)
**Propósito**: Sistema de base de datos RAG
**Servicios**:
- Base de datos RAG (puerto a verificar)
- API RAG (puerto a verificar)

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

### VM 3: **gpt-oss-20b** (europe-southwest1-b)
**Propósito**: Servicios auxiliares (TTS, MCP, N8n, Bridge)
**Servicios**:
- **Servidor Principal**: Puerto 5000 (server.py)
- **Servidor Llama**: Puerto 8080 (modelo gpt-oss-20b)
- **MCP Server**: Puerto 5003 o 5010
- **TTS**: Puerto a verificar
- **N8n**: Puerto 5678 (típico)
- **Bridge**: Puerto a verificar

**Comando SSH**:
```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

## 🔌 Flujo de Conexiones

```
Frontend (Local/Vercel)
    ↓
VM bounty2:5001 (Backend Capibara6)
    ↓
VM bounty2:11434 (Ollama - modelos)
    ↓
VM rag3 (Base de datos RAG) [opcional]
    ↓
VM gpt-oss-20b:5000 (Servicios TTS, MCP, etc.)
```

## 🌐 Configuración de Red

### IPs Públicas (a obtener)
- **bounty2**: `[OBTENER IP]`
- **rag3**: `[OBTENER IP]`
- **gpt-oss-20b**: `[OBTENER IP]`

### IPs Internas (para comunicación entre VMs)
- **bounty2**: `[OBTENER IP INTERNA]`
- **rag3**: `[OBTENER IP INTERNA]`
- **gpt-oss-20b**: `[OBTENER IP INTERNA]`

### Red de Alta Velocidad
Para que las VMs se comuniquen a alta velocidad, deben estar en la misma **VPC (Virtual Private Cloud)** de Google Cloud.

**Verificar VPC compartida**:
```bash
# Verificar la red de cada VM
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="value(networkInterfaces[0].network)"
gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="value(networkInterfaces[0].network)"
gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="value(networkInterfaces[0].network)"
```

Si las VMs están en diferentes VPCs, necesitarás:
1. Crear una VPC compartida, o
2. Configurar VPC Peering, o
3. Usar Cloud VPN para conectar las VPCs

## 📝 Configuración del Frontend

### Para Desarrollo Local

El frontend debe conectarse a la VM **bounty2** en el puerto **5001**:

```javascript
// web/config.js
const CHATBOT_CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://[IP_BOUNTY2]:5001'  // IP pública de bounty2
        : 'https://www.capibara6.com',
    // ...
};
```

### Para Producción (Vercel)

El frontend en Vercel debe usar los proxies de Vercel (`/api/*`) que redirigen a las VMs.

## 🔧 Configuración del Backend

### En VM bounty2

El backend debe conectarse a:
- **Ollama local**: `http://localhost:11434` (mismo servidor)
- **RAG (rag3)**: `http://[IP_INTERNA_RAG3]:[PUERTO]` (usar IP interna para velocidad)
- **Servicios (gpt-oss-20b)**: `http://[IP_INTERNA_GPT-OSS-20B]:5000` (usar IP interna)

### Variables de Entorno

En `backend/.env`:
```bash
# Ollama (local en bounty2)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:20b

# RAG (en rag3)
RAG_URL=http://[IP_INTERNA_RAG3]:[PUERTO]

# Servicios (en gpt-oss-20b)
SERVICES_URL=http://[IP_INTERNA_GPT-OSS-20B]:5000
MCP_URL=http://[IP_INTERNA_GPT-OSS-20B]:5003
```

## 🔥 Configuración de Firewall

### Reglas de Firewall Necesarias

1. **bounty2** debe permitir:
   - Puerto 5001 desde Internet (para frontend)
   - Puerto 11434 desde IPs internas (para otros servicios)

2. **rag3** debe permitir:
   - Puerto de RAG desde IPs internas de otras VMs

3. **gpt-oss-20b** debe permitir:
   - Puerto 5000 desde IPs internas
   - Puerto 5003/5010 desde IPs internas
   - Puerto 8080 desde IPs internas

**Comandos para crear reglas de firewall**:
```bash
# Permitir comunicación interna entre VMs
gcloud compute firewall-rules create allow-internal-vm-communication \
    --allow tcp:5000,tcp:5001,tcp:5003,tcp:5010,tcp:8080,tcp:11434 \
    --source-ranges 10.0.0.0/8 \
    --target-tags bounty2,rag3,gpt-oss-20b \
    --project=mamba-001

# Permitir acceso externo a bounty2 (backend)
gcloud compute firewall-rules create allow-bounty2-backend \
    --allow tcp:5001 \
    --source-ranges 0.0.0.0/0 \
    --target-tags bounty2 \
    --project=mamba-001
```

## ✅ Checklist de Verificación

- [ ] Obtener IPs públicas de las 3 VMs
- [ ] Obtener IPs internas de las 3 VMs
- [ ] Verificar que las VMs estén en la misma VPC o configurar VPC Peering
- [ ] Verificar servicios corriendo en cada VM
- [ ] Configurar firewall para permitir comunicación interna
- [ ] Configurar firewall para permitir acceso externo a bounty2:5001
- [ ] Actualizar `web/config.js` con IP de bounty2
- [ ] Actualizar `backend/.env` con IPs internas
- [ ] Probar conexión desde frontend local a bounty2:5001
- [ ] Probar conexión desde bounty2 a rag3
- [ ] Probar conexión desde bounty2 a gpt-oss-20b

## 🧪 Scripts de Prueba

### Probar conexión desde local a bounty2
```bash
curl http://[IP_BOUNTY2]:5001/health
```

### Probar Ollama en bounty2
```bash
curl http://[IP_BOUNTY2]:11434/api/tags
```

### Probar servicios en gpt-oss-20b (desde bounty2)
```bash
# Desde dentro de bounty2
curl http://[IP_INTERNA_GPT-OSS-20B]:5000/health
curl http://[IP_INTERNA_GPT-OSS-20B]:5003/health
```

## 📚 Referencias

- [Google Cloud VPC Peering](https://cloud.google.com/vpc/docs/vpc-peering)
- [Google Cloud Firewall Rules](https://cloud.google.com/vpc/docs/firewalls)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)

