# 📋 Resumen: Configuración de VMs de Capibara6

## ✅ Lo que se ha hecho

1. **Scripts de diagnóstico creados**:
   - `scripts/get_vm_info.py` - Obtiene IPs y configuración de VMs
   - `scripts/verify_vm_connections.sh` - Verifica conexiones entre VMs
   - `scripts/check_services_on_vm.sh` - Verifica servicios en una VM específica
   - `scripts/setup_vm_connections.sh` - Configuración automática de conexiones

2. **Configuraciones actualizadas**:
   - `web/config.js` - Actualizado para desarrollo local con IPs de VMs
   - `backend/rag_client.py` - Mejorado para usar variables de entorno
   - `backend/config/vm_endpoints.py` - Nuevo módulo para gestión de endpoints

3. **Documentación creada**:
   - `VM_SETUP_GUIDE.md` - Guía completa de configuración
   - `RESUMEN_CONFIGURACION_VMS.md` - Este archivo

## 🎯 Próximos pasos (en orden)

### Paso 1: Obtener IPs de las VMs

Ejecuta desde tu terminal:

```bash
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/NxnaC
python3 scripts/get_vm_info.py
```

Esto generará `vm_config.json` con todas las IPs.

**Alternativa manual**:
```bash
# Bounty2
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# rag3
gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# gpt-oss-20b
gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### Paso 2: Actualizar configuración del frontend

Edita `web/config.js` y actualiza las IPs en `VM_IPS`:

```javascript
const VM_IPS = {
    BOUNTY2_EXTERNAL: 'TU_IP_BOUNTY2',      // IP externa de Bounty2
    GPTOSS_EXTERNAL: 'TU_IP_GPTOSS',        // IP externa de gpt-oss-20b
    RAG3_EXTERNAL: 'TU_IP_RAG3',            // IP externa de rag3
};
```

### Paso 3: Verificar servicios en cada VM

Conecta a cada VM y ejecuta el script de verificación:

```bash
# Bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
cd /ruta/al/repositorio
bash scripts/check_services_on_vm.sh

# rag3
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
cd /ruta/al/repositorio
bash scripts/check_services_on_vm.sh

# gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
cd /ruta/al/repositorio
bash scripts/check_services_on_vm.sh
```

### Paso 4: Verificar red VPC

Asegúrate de que todas las VMs están en la misma red VPC para comunicación de alta velocidad:

```bash
# Verificar redes
gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="value(networkInterfaces[0].network)"
gcloud compute instances describe rag3 --zone=europe-west2-c --project=mamba-001 --format="value(networkInterfaces[0].network)"
gcloud compute instances describe gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --format="value(networkInterfaces[0].network)"
```

Si están en diferentes redes, consulta `VM_SETUP_GUIDE.md` para moverlas a la misma VPC.

### Paso 5: Configurar firewall rules

Ejecuta el script de configuración:

```bash
bash scripts/setup_vm_connections.sh
```

O manualmente:

```bash
# Obtener nombre de la red VPC (reemplaza NETWORK_NAME)
NETWORK_NAME=$(gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="value(networkInterfaces[0].network)" | awk -F'/' '{print $NF}')

# Crear regla de firewall
gcloud compute firewall-rules create allow-internal-vm-communication \
  --project=mamba-001 \
  --network=$NETWORK_NAME \
  --allow tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=10.0.0.0/8 \
  --description="Permitir comunicación entre VMs de Capibara6"
```

### Paso 6: Configurar variables de entorno en backend

En cada VM, crea/actualiza `.env`:

**En Bounty2**:
```bash
OLLAMA_ENDPOINT=http://IP_INTERNA_BOUNTY2:11434
BOUNTY2_BACKEND_ENDPOINT=http://IP_INTERNA_BOUNTY2:5001
```

**En rag3** (si hay backend):
```bash
RAG_API_ENDPOINT=http://IP_INTERNA_RAG3:8000
```

**En gpt-oss-20b**:
```bash
TTS_ENDPOINT=http://IP_INTERNA_GPTOSS:5002
MCP_ENDPOINT=http://IP_INTERNA_GPTOSS:5003
MCP_ALT_ENDPOINT=http://IP_INTERNA_GPTOSS:5010
N8N_ENDPOINT=http://IP_INTERNA_GPTOSS:5678
BRIDGE_ENDPOINT=http://IP_INTERNA_GPTOSS:5000
```

### Paso 7: Probar conexiones

**Desde tu portátil (desarrollo local)**:

```bash
# Verificar Ollama
curl http://IP_EXTERNA_BOUNTY2:11434/api/tags

# Verificar Backend
curl http://IP_EXTERNA_BOUNTY2:5001/api/health

# Verificar RAG API
curl http://IP_EXTERNA_RAG3:8000/health

# Verificar TTS
curl http://IP_EXTERNA_GPTOSS:5002/api/tts/voices

# Verificar MCP
curl http://IP_EXTERNA_GPTOSS:5003/api/mcp/status
```

**Desde dentro de las VMs** (usando IPs internas):

```bash
# Desde Bounty2, verificar RAG en rag3
curl http://IP_INTERNA_RAG3:8000/health

# Desde cualquier VM, verificar Ollama en Bounty2
curl http://IP_INTERNA_BOUNTY2:11434/api/tags
```

### Paso 8: Probar frontend local

```bash
cd web
python3 -m http.server 8000
```

Abre `http://localhost:8000` en tu navegador y verifica que se conecta correctamente a los servicios.

## 📊 Arquitectura de Servicios

```
┌─────────────────────────────────────────────────────────────┐
│                    TU PORTÁTIL (Local)                      │
│                  Frontend (localhost:8000)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP (IPs externas)
                       │
        ┌──────────────┼──────────────┐
        │              │               │
        ▼              ▼               ▼
┌──────────────┐ ┌──────────┐ ┌──────────────────┐
│   Bounty2    │ │   rag3   │ │  gpt-oss-20b     │
│              │ │          │ │                  │
│ Ollama:11434 │ │ RAG:8000 │ │ TTS:5002         │
│ Backend:5001 │ │          │ │ MCP:5003,5010    │
│              │ │          │ │ N8n:5678         │
│              │ │          │ │ Bridge:5000      │
└──────┬───────┘ └────┬─────┘ └──────────────────┘
       │              │               │
       │              │               │
       └──────────────┼───────────────┘
                      │
              HTTP (IPs internas)
              Comunicación entre VMs
```

## 🔍 Verificación de Estado

Para verificar que todo está conectado correctamente:

1. **Ejecuta el script de diagnóstico**:
   ```bash
   python3 scripts/get_vm_info.py
   ```

2. **Revisa el archivo generado**:
   ```bash
   cat vm_config.json
   ```

3. **Verifica servicios en cada VM**:
   ```bash
   # En cada VM
   bash scripts/check_services_on_vm.sh
   ```

4. **Prueba conexiones**:
   ```bash
   # Desde tu portátil
   bash scripts/verify_vm_connections.sh
   ```

## 📝 Archivos Importantes

- `VM_SETUP_GUIDE.md` - Guía completa de configuración
- `vm_config.json` - Configuración de VMs (generado automáticamente)
- `web/config.js` - Configuración del frontend
- `backend/config/vm_endpoints.py` - Gestión de endpoints en backend
- `backend/rag_client.py` - Cliente RAG (actualizado)
- `scripts/get_vm_info.py` - Script para obtener IPs
- `scripts/check_services_on_vm.sh` - Verificar servicios en VM
- `scripts/setup_vm_connections.sh` - Configuración automática

## ⚠️ Notas Importantes

1. **IPs Internas vs Externas**:
   - Usa IPs **internas** para comunicación entre VMs (más rápido, sin costo)
   - Usa IPs **externas** solo para acceso desde fuera de GCloud (tu portátil)

2. **Red VPC**:
   - Todas las VMs deben estar en la misma VPC para mejor rendimiento
   - Si están en diferentes VPCs, configura VPC Peering

3. **Firewall Rules**:
   - Las reglas de firewall deben permitir comunicación entre VMs
   - Para desarrollo local, necesitas permitir acceso desde tu IP pública

4. **Puertos**:
   - Asegúrate de que los servicios están escuchando en `0.0.0.0` y no solo `127.0.0.1`
   - Verifica que los puertos están abiertos en el firewall de GCloud

## 🆘 Troubleshooting

Si encuentras problemas:

1. Revisa `VM_SETUP_GUIDE.md` sección "Troubleshooting"
2. Verifica logs de servicios en cada VM
3. Verifica reglas de firewall: `gcloud compute firewall-rules list --project=mamba-001`
4. Verifica conectividad: `ping IP_INTERNA` desde una VM a otra

---

**Última actualización**: Noviembre 2025

