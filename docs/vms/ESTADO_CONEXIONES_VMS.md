# 📊 Estado de Conexiones VMs - Capibara6

**Fecha**: $(date)

## ✅ Servicios Verificados

### VM: bounty2 (34.12.166.76) - europe-west4-a
**Estado**: ✅ **FUNCIONANDO**

- ✅ **Ollama** (puerto 11434): **ACTIVO**
  - Modelos disponibles:
    - `gpt-oss:20b` (20.9B, MXFP4)
    - `mistral:latest` (7.2B, Q4_K_M)
    - `phi3:mini` (3.8B, Q4_0)
  - Endpoint: `http://34.12.166.76:11434/api/tags` ✅ Responde correctamente

- ⏳ **Backend Capibara6** (puerto 5001): Pendiente verificación

### VM: gpt-oss-20b (34.175.136.104) - europe-southwest1-b
**Estado**: ⚠️ **VERIFICACIÓN PENDIENTE**

- ⏳ **Servidor Principal** (puerto 5000): No responde desde local
  - Posibles causas:
    - Servicio no está corriendo
    - Firewall bloquea conexiones externas
    - Servicio escucha solo en localhost

- ⏳ **MCP Server** (puerto 5003): No responde desde local
- ⏳ **MCP Server Alternativo** (puerto 5010): No responde desde local
- ⏳ **Llama Server** (puerto 8080): No responde desde local

**Acción requerida**: Conectarse a la VM y verificar que los servicios estén corriendo y escuchando en `0.0.0.0`

### VM: rag3 - europe-west2-c
**Estado**: ⏳ **IP PENDIENTE**

- ⏳ IP pública: Pendiente de obtener
- ⏳ Servicios: Pendiente verificación

## 🔧 Configuración Actualizada

### Frontend (`web/config.js`)
✅ **CONFIGURADO**
- Desarrollo local: `http://34.175.136.104:5000`
- Configuración de todas las VMs documentada

### Backend (`backend/env.example`)
✅ **ACTUALIZADO**
- `OLLAMA_BASE_URL=http://34.12.166.76:11434`
- Documentación de IPs internas vs públicas

## 📋 Próximos Pasos

### 1. Verificar Servicios en gpt-oss-20b

Conectarse a la VM y verificar:

```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Verificar servicios activos
sudo ss -tulnp | grep -E "(5000|5003|5010|8080)"

# Verificar procesos
ps aux | grep -E "(python|server|mcp)"

# Probar servicios localmente en la VM
curl http://localhost:5000/api/health
curl http://localhost:5003/api/mcp/status
curl http://localhost:8080/health
```

### 2. Verificar Firewall

Asegurarse de que los puertos estén abiertos:

```bash
# Ver reglas de firewall existentes
gcloud compute firewall-rules list --project=mamba-001

# Crear regla si no existe (ejemplo)
gcloud compute firewall-rules create allow-capibara6-services \
  --allow tcp:5000,tcp:5003,tcp:5010,tcp:8080 \
  --source-ranges 0.0.0.0/0 \
  --target-tags capibara6-services \
  --description "Servicios Capibara6"
```

### 3. Verificar que Servicios Escuchen en 0.0.0.0

Los servicios deben escuchar en `0.0.0.0` y no solo en `localhost` o `127.0.0.1`:

```bash
# En la VM, verificar qué IP está escuchando
sudo ss -tulnp | grep LISTEN
```

Si un servicio escucha solo en `127.0.0.1`, debe cambiarse a `0.0.0.0` en la configuración.

### 4. Obtener IP de rag3

```bash
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"
```

### 5. Configurar Red de Alta Velocidad

Verificar si las VMs están en la misma red VPC:

```bash
# Verificar red de cada VM
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].network)"

gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].network)"
```

Si están en redes diferentes, considerar:
- Mover VMs a la misma red VPC
- Configurar VPC Peering
- Usar IPs internas para comunicación entre VMs

## 🧪 Scripts de Verificación

### Script Simple de Conectividad
```bash
./scripts/test_vm_connectivity.sh
```

### Script Completo de Verificación
```bash
./scripts/verify_vm_connections.sh
```

## 📝 Resumen de Configuración para Desarrollo Local

### Frontend
- Servidor Principal: `http://34.175.136.104:5000`
- MCP Server: `http://34.175.136.104:5003`
- Modelo: `http://34.175.136.104:8080`

### Backend
- Ollama: `http://34.12.166.76:11434`
- Modelos disponibles: `gpt-oss:20b`, `mistral`, `phi3:mini`

### Para Probar Frontend Localmente

```bash
cd web
python3 -m http.server 8000
# Abrir: http://localhost:8000
```

El frontend debería conectarse automáticamente a `http://34.175.136.104:5000` cuando se ejecuta desde localhost.

## ⚠️ Problemas Conocidos

1. **Servicios en gpt-oss-20b no responden desde local**
   - **Causa probable**: Servicios no están corriendo o firewall bloquea conexiones
   - **Solución**: Verificar servicios en la VM y configurar firewall

2. **IP de rag3 pendiente**
   - **Solución**: Ejecutar comando para obtener IP pública

3. **Red de alta velocidad no configurada**
   - **Solución**: Verificar redes VPC y configurar peering si es necesario

## ✅ Checklist de Completitud

- [x] IPs de bounty2 y gpt-oss-20b obtenidas
- [x] Ollama verificado y funcionando
- [x] Frontend configurado
- [x] Backend configurado para Ollama
- [ ] Servicios en gpt-oss-20b verificados
- [ ] IP de rag3 obtenida
- [ ] Firewall configurado
- [ ] Red de alta velocidad configurada
- [ ] Conexiones probadas desde local

