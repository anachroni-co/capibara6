# ✅ Resumen Final - Solución de Errores de Conexión

## 🔴 Errores Detectados

1. **Backend en bounty2** (puerto 5001): `ERR_CONNECTION_REFUSED`
2. **Smart MCP en gpt-oss-20b** (puerto 5010): `ERR_CONNECTION_REFUSED`

## ✅ Solución

Los servicios **NO están corriendo** en las VMs. Necesitas iniciarlos manualmente.

### Pasos Rápidos:

#### 1. Iniciar Backend en bounty2

```bash
# Conectarse
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Dentro de la VM:
cd ~/capibara6/backend
source venv/bin/activate
screen -dmS capibara6-backend bash -c "
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server_ollama.py
"
```

#### 2. Iniciar Smart MCP en gpt-oss-20b

```bash
# Conectarse
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Dentro de la VM:
cd ~/capibara6/backend
source venv/bin/activate
screen -dmS smart-mcp bash -c "
    export PORT=5010
    python3 smart_mcp_server.py
"
```

#### 3. Verificar

```bash
# Desde tu PC local:
curl http://34.12.166.76:5001/api/health
curl http://34.175.136.104:5010/health
```

Si ambos responden, el frontend funcionará correctamente.

## 📚 Documentación Completa

- **Comandos detallados**: `COMANDOS_INICIAR_SERVICIOS.md`
- **Solución de errores**: `SOLUCION_ERRORES_CONEXION.md`
- **Instrucciones**: `INSTRUCCIONES_INICIO_SERVICIOS.md`

## ⚡ Scripts Disponibles

- `scripts/iniciar_servicios_rapido.sh` - Script automatizado (puede tardar)
- `scripts/start_bounty2_services.sh` - Solo para bounty2
- `scripts/check_bounty2_status.sh` - Verificar estado

## 🎯 Estado Actual

- ✅ Configuración del frontend: **COMPLETA**
- ✅ Documentación: **COMPLETA**
- ✅ Scripts creados: **COMPLETOS**
- ⏳ Servicios en VMs: **PENDIENTE DE INICIAR** (debes hacerlo manualmente)

Una vez que inicies los servicios siguiendo los comandos arriba, todo debería funcionar correctamente.

