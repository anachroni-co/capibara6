# 🚀 Guía de Configuración de VMs - Capibara6

Esta guía explica cómo configurar y verificar las conexiones entre las 3 VMs de Google Cloud.

## 📋 VMs del Sistema

### 1. **Bounty2** (`europe-west4-a`)
- **Servicios**: Ollama con modelos gpt-oss-20B, mixtral, phi-mini3
- **Puertos**:
  - `11434`: Ollama API
  - `5001`: Backend Flask (servidor integrado)

### 2. **rag3** (`europe-west2-c`)
- **Servicios**: Sistema de base de datos RAG
- **Puertos**:
  - `8000`: RAG API
  - `5432`: PostgreSQL (si aplica)
  - `6379`: Redis (si aplica)

### 3. **gpt-oss-20b** (`europe-southwest1-b`)
- **Servicios**: TTS, MCP, N8n, Bridge
- **Puertos**:
  - `5000`: Bridge/Backend principal
  - `5002`: TTS (Text-to-Speech)
  - `5003`: MCP Server
  - `5010`: MCP Server (alternativo)
  - `5678`: N8n

## 🔍 Paso 1: Obtener IPs de las VMs

Ejecuta estos comandos para obtener las IPs externas e internas:

```bash
# Bounty2
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# rag3
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# gpt-oss-20b
gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"
```

O usa el script automatizado:

```bash
python3 scripts/get_vm_info.py
```

Esto generará un archivo `vm_config.json` con toda la información.

## 🌐 Paso 2: Verificar Red VPC

Para comunicación de alta velocidad, todas las VMs deben estar en la misma red VPC.

### Verificar red actual:

```bash
# Ver red de cada VM
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

### Si están en diferentes redes:

1. **Opción 1: Mover VMs a la misma red** (recomendado)
   ```bash
   # Crear una nueva red VPC si no existe
   gcloud compute networks create capibara6-vpc \
     --project=mamba-001 \
     --subnet-mode=auto
   
   # Mover cada VM a la nueva red (requiere detener la VM)
   gcloud compute instances stop bounty2 --zone=europe-west4-a --project=mamba-001
   gcloud compute instances set-network-interface bounty2 \
     --zone=europe-west4-a \
     --project=mamba-001 \
     --network=capibara6-vpc \
     --network-tier=PREMIUM
   gcloud compute instances start bounty2 --zone=europe-west4-a --project=mamba-001
   ```

2. **Opción 2: Configurar VPC Peering** (si las VMs deben quedarse en diferentes redes)
   ```bash
   # Crear peering entre redes
   gcloud compute networks peerings create peer-rag3-to-bounty2 \
     --network=RED_BOUNTY2 \
     --peer-network=RED_RAG3 \
     --project=mamba-001
   ```

## 🔒 Paso 3: Configurar Firewall Rules

Las VMs necesitan poder comunicarse entre sí. Configura reglas de firewall:

```bash
# Permitir comunicación interna entre VMs (usando IPs internas)
gcloud compute firewall-rules create allow-internal-vm-communication \
  --project=mamba-001 \
  --network=TU_RED_VPC \
  --allow tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=10.0.0.0/8 \
  --description="Permitir comunicación entre VMs de Capibara6"

# Permitir acceso externo desde tu IP (para desarrollo local)
gcloud compute firewall-rules create allow-external-development \
  --project=mamba-001 \
  --network=TU_RED_VPC \
  --allow tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=TU_IP_PUBLICA/32 \
  --description="Permitir acceso desde desarrollo local"
```

## ✅ Paso 4: Verificar Servicios en cada VM

Conecta a cada VM y ejecuta el script de verificación:

```bash
# En Bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
bash scripts/check_services_on_vm.sh

# En rag3
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
bash scripts/check_services_on_vm.sh

# En gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
bash scripts/check_services_on_vm.sh
```

## 🔧 Paso 5: Actualizar Configuraciones

### Backend

1. **Actualizar `backend/config/vm_endpoints.py`** o crear archivo `.env`:

```bash
# En cada VM, crear/actualizar .env
# Bounty2
OLLAMA_ENDPOINT=http://IP_INTERNA_BOUNTY2:11434
BOUNTY2_BACKEND_ENDPOINT=http://IP_INTERNA_BOUNTY2:5001

# rag3 (si hay backend aquí)
RAG_API_ENDPOINT=http://IP_INTERNA_RAG3:8000

# gpt-oss-20b
TTS_ENDPOINT=http://IP_INTERNA_GPTOSS:5002
MCP_ENDPOINT=http://IP_INTERNA_GPTOSS:5003
MCP_ALT_ENDPOINT=http://IP_INTERNA_GPTOSS:5010
N8N_ENDPOINT=http://IP_INTERNA_GPTOSS:5678
BRIDGE_ENDPOINT=http://IP_INTERNA_GPTOSS:5000
```

2. **Actualizar `backend/rag_client.py`**:

```python
# Cambiar la IP hardcodeada por la IP interna de rag3
self.base_url = base_url or os.getenv(
    "RAG_API_URL",
    "http://IP_INTERNA_RAG3:8000"  # Actualizar esta IP
)
```

3. **Actualizar `backend/ollama_client.py`**:

```python
# Asegurar que apunta a Bounty2
self.endpoint = config.get("api_settings", {}).get(
    "ollama_endpoint",
    os.getenv("OLLAMA_ENDPOINT", "http://IP_INTERNA_BOUNTY2:11434")
)
```

### Frontend

Actualizar `web/config.js` para desarrollo local:

```javascript
const CHATBOT_CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://IP_EXTERNA_BOUNTY2:5001'  // IP externa de Bounty2 para acceso desde local
        : 'https://www.capibara6.com',
    // ... resto de configuración
};
```

## 🧪 Paso 6: Probar Conexiones

### Desde tu portátil (desarrollo local):

```bash
# Verificar Ollama en Bounty2
curl http://IP_EXTERNA_BOUNTY2:11434/api/tags

# Verificar Backend en Bounty2
curl http://IP_EXTERNA_BOUNTY2:5001/api/health

# Verificar RAG API en rag3
curl http://IP_EXTERNA_RAG3:8000/health

# Verificar TTS en gpt-oss-20b
curl http://IP_EXTERNA_GPTOSS:5002/api/tts/voices

# Verificar MCP en gpt-oss-20b
curl http://IP_EXTERNA_GPTOSS:5003/api/mcp/status
```

### Desde dentro de las VMs (usando IPs internas):

```bash
# Desde Bounty2, verificar RAG en rag3
curl http://IP_INTERNA_RAG3:8000/health

# Desde cualquier VM, verificar Ollama en Bounty2
curl http://IP_INTERNA_BOUNTY2:11434/api/tags
```

## 📊 Resumen de Endpoints

Una vez configurado, los endpoints deberían ser:

| Servicio | VM | IP Interna | IP Externa | Puerto |
|----------|----|-----------|------------|--------|
| Ollama | Bounty2 | `10.x.x.x` | `34.x.x.x` | 11434 |
| Backend | Bounty2 | `10.x.x.x` | `34.x.x.x` | 5001 |
| RAG API | rag3 | `10.x.x.x` | `34.x.x.x` | 8000 |
| TTS | gpt-oss-20b | `10.x.x.x` | `34.x.x.x` | 5002 |
| MCP | gpt-oss-20b | `10.x.x.x` | `34.x.x.x` | 5003 |
| N8n | gpt-oss-20b | `10.x.x.x` | `34.x.x.x` | 5678 |
| Bridge | gpt-oss-20b | `10.x.x.x` | `34.x.x.x` | 5000 |

**Nota**: Usa IPs internas para comunicación entre VMs (más rápido y sin costo). Usa IPs externas solo para acceso desde fuera de GCloud.

## 🐛 Troubleshooting

### Problema: No puedo conectarme entre VMs

1. Verificar que están en la misma VPC
2. Verificar reglas de firewall
3. Verificar que los servicios están corriendo (`check_services_on_vm.sh`)
4. Verificar conectividad: `ping IP_INTERNA` desde una VM a otra

### Problema: Puerto cerrado desde fuera

1. Verificar firewall rules de GCloud
2. Verificar que el servicio está escuchando en `0.0.0.0` y no solo `127.0.0.1`
3. Verificar que el puerto está abierto en el firewall de la VM

### Problema: Latencia alta

1. Asegurar que las VMs están en la misma región o zonas cercanas
2. Usar IPs internas en lugar de externas
3. Verificar que están en la misma VPC

## 📝 Checklist Final

- [ ] IPs obtenidas y guardadas en `vm_config.json`
- [ ] VMs verificadas en la misma VPC (o peering configurado)
- [ ] Firewall rules configuradas
- [ ] Servicios verificados corriendo en cada VM
- [ ] Configuraciones del backend actualizadas
- [ ] Configuración del frontend actualizada para desarrollo local
- [ ] Conexiones probadas desde portátil
- [ ] Conexiones probadas entre VMs

---

**Última actualización**: Noviembre 2025

