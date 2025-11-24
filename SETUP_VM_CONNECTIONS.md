# 🚀 Guía de Configuración de Conexiones entre VMs

## 📋 Resumen Ejecutivo

Este proyecto está distribuido en 3 VMs de Google Cloud:
1. **bounty2** (europe-west4-a): Ollama con modelos de IA
2. **rag3** (europe-west2-c): Sistema de base de datos RAG
3. **gpt-oss-20b** (europe-southwest1-b): Servicios TTS, MCP, N8n, Bridge

## 🔍 Paso 1: Obtener IPs de las VMs

Ejecuta estos comandos para obtener las IPs públicas e internas:

```bash
# IPs públicas
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="get(networkInterfaces[0].accessConfigs[0].natIP)"

# IPs internas (para comunicación entre VMs)
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="get(networkInterfaces[0].networkIP)"
gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="get(networkInterfaces[0].networkIP)"
gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="get(networkInterfaces[0].networkIP)"

# Verificar redes (VPC)
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="get(networkInterfaces[0].network)"
gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="get(networkInterfaces[0].network)"
gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="get(networkInterfaces[0].network)"
```

**O usa el script automatizado**:
```bash
bash get_vm_ips.sh
```

## 🔧 Paso 2: Verificar Servicios en Cada VM

### En bounty2 (Ollama y Backend)

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Una vez dentro de la VM:
# Ver puertos abiertos
sudo ss -tulnp | grep LISTEN

# Verificar Ollama
curl http://localhost:11434/api/tags

# Verificar Backend Capibara6
curl http://localhost:5001/health

# Ver procesos corriendo
ps aux | grep -E "(ollama|python|node)" | grep -v grep
```

### En rag3 (Base de datos)

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Una vez dentro de la VM:
# Ver puertos abiertos
sudo ss -tulnp | grep LISTEN

# Verificar servicios de base de datos
ps aux | grep -E "(postgres|mongodb|redis|rag)" | grep -v grep
```

### En gpt-oss-20b (Servicios TTS, MCP, etc.)

```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Una vez dentro de la VM:
# Ver puertos abiertos
sudo ss -tulnp | grep LISTEN

# Verificar servicios
curl http://localhost:5000/health
curl http://localhost:5003/health
curl http://localhost:5010/health
curl http://localhost:8080/health

# Ver procesos
ps aux | grep -E "(python|node|n8n|tts)" | grep -v grep
```

## 🌐 Paso 3: Configurar Red de Alta Velocidad

Para que las VMs se comuniquen a alta velocidad, deben estar en la misma VPC o tener VPC Peering configurado.

### Verificar si están en la misma red

Si las 3 VMs muestran la misma red en el paso 1, ya están conectadas. Si no:

### Opción A: Crear VPC Peering (si están en diferentes VPCs)

```bash
# Crear peering entre VPCs (ejemplo)
gcloud compute networks peerings create bounty2-to-rag3 \
    --network=bounty2-network \
    --peer-network=rag3-network \
    --project=mamba-001
```

### Opción B: Mover VMs a la misma VPC

```bash
# Esto requiere recrear las VMs o cambiar su interfaz de red
# Consulta la documentación de Google Cloud para más detalles
```

## 🔥 Paso 4: Configurar Firewall

### Permitir comunicación interna entre VMs

```bash
# Crear regla de firewall para comunicación interna
gcloud compute firewall-rules create allow-internal-vm-communication \
    --allow tcp:5000,tcp:5001,tcp:5003,tcp:5010,tcp:8080,tcp:11434 \
    --source-ranges 10.0.0.0/8 \
    --target-tags bounty2,rag3,gpt-oss-20b \
    --project=mamba-001 \
    --description="Permitir comunicación interna entre VMs de Capibara6"
```

### Permitir acceso externo a bounty2 (para frontend)

```bash
# Permitir acceso desde Internet al backend en bounty2
gcloud compute firewall-rules create allow-bounty2-backend \
    --allow tcp:5001 \
    --source-ranges 0.0.0.0/0 \
    --target-tags bounty2 \
    --project=mamba-001 \
    --description="Permitir acceso externo al backend de Capibara6"
```

## 💻 Paso 5: Configurar Frontend Local

### Opción A: Usar configuración de VMs (Recomendado)

1. Edita `web/config-local-vm.js` y actualiza las IPs:
```javascript
const VM_IPS = {
    BOUNTY2: '34.12.166.76',  // IP pública de bounty2
    RAG3: '[IP_RAG3]',
    GPT_OSS_20B: '34.175.136.104',  // IP pública de gpt-oss-20b
};
```

2. Incluye el script en tu HTML antes de otros scripts:
```html
<script src="config-local-vm.js"></script>
<script src="config.js"></script>
<script src="chat-app.js"></script>
```

### Opción B: Configurar manualmente

Edita `web/config.js` y actualiza:
```javascript
BACKEND_URL: window.location.hostname === 'localhost'
    ? 'http://[IP_BOUNTY2]:5001'  // IP pública de bounty2
    : 'https://www.capibara6.com',
```

## ⚙️ Paso 6: Configurar Backend

### En VM bounty2

Crea/edita `backend/.env`:
```bash
# Ollama (local en bounty2)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:20b

# RAG (en rag3 - usar IP interna para velocidad)
RAG_URL=http://[IP_INTERNA_RAG3]:[PUERTO_RAG]

# Servicios (en gpt-oss-20b - usar IP interna)
SERVICES_URL=http://[IP_INTERNA_GPT-OSS-20B]:5000
MCP_URL=http://[IP_INTERNA_GPT-OSS-20B]:5003
```

## ✅ Paso 7: Verificar Conexiones

### Desde tu portátil local

```bash
# Verificar backend en bounty2
curl http://[IP_BOUNTY2]:5001/health

# Verificar Ollama en bounty2
curl http://[IP_BOUNTY2]:11434/api/tags

# Verificar servicios en gpt-oss-20b
curl http://[IP_GPT-OSS-20B]:5000/health
```

### Desde dentro de bounty2 (verificar comunicación interna)

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Probar conexión a rag3
curl http://[IP_INTERNA_RAG3]:[PUERTO]/health

# Probar conexión a gpt-oss-20b
curl http://[IP_INTERNA_GPT-OSS-20B]:5000/health
curl http://[IP_INTERNA_GPT-OSS-20B]:5003/health
```

## 🧪 Paso 8: Probar Frontend Local

1. Inicia un servidor HTTP local:
```bash
cd web
python3 -m http.server 8000
```

2. Abre en el navegador: `http://localhost:8000/chat.html`

3. Verifica en la consola del navegador que las peticiones se hagan a la IP correcta de bounty2

4. Prueba enviar un mensaje y verifica que:
   - Se conecta al backend en bounty2
   - El backend se conecta a Ollama
   - Se obtiene una respuesta

## 📊 Checklist Final

- [ ] IPs públicas obtenidas de las 3 VMs
- [ ] IPs internas obtenidas de las 3 VMs
- [ ] Verificadas las redes (VPC) de las VMs
- [ ] Servicios verificados en cada VM
- [ ] Firewall configurado para comunicación interna
- [ ] Firewall configurado para acceso externo a bounty2:5001
- [ ] Frontend configurado con IP de bounty2
- [ ] Backend configurado con IPs internas
- [ ] Conexiones verificadas desde portátil local
- [ ] Conexiones verificadas entre VMs
- [ ] Frontend probado localmente

## 🐛 Troubleshooting

### Error: "Connection refused"
- Verifica que el servicio esté corriendo en la VM
- Verifica que el puerto esté abierto en el firewall
- Verifica que la IP sea correcta

### Error: "Timeout"
- Verifica que las VMs estén en la misma red o tengan VPC Peering
- Verifica que el firewall permita el tráfico
- Verifica que el servicio esté respondiendo

### Error: CORS en el navegador
- Verifica que el backend tenga CORS configurado
- Verifica que estés usando la IP pública correcta
- Considera usar los proxies de Vercel en producción

## 📚 Archivos de Referencia

- `VM_CONNECTION_CONFIG.md` - Documentación detallada de configuración
- `web/config-local-vm.js` - Configuración para desarrollo local
- `web/config.js` - Configuración principal del frontend
- `backend/.env.example` - Ejemplo de variables de entorno
- `get_vm_ips.sh` - Script para obtener IPs
- `verify_vm_services.sh` - Script para verificar servicios

