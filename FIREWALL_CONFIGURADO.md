# ✅ Configuración de Firewall - Capibara6

## 🔒 Reglas de Firewall Configuradas

Se han configurado las siguientes reglas de firewall en el proyecto `mamba-001`:

### 1. Regla Interna (Comunicación entre VMs)

**Nombre**: `allow-capibara6-internal`

- **Red**: `default`
- **Puertos permitidos**: 11434, 5000, 5001, 5002, 5003, 5010, 5678, 8000
- **Origen**: `10.0.0.0/8` (red interna de GCloud)
- **Descripción**: Permite comunicación interna entre VMs de Capibara6

Esta regla permite que las VMs se comuniquen entre sí usando sus IPs internas.

### 2. Regla Externa (Acceso desde Desarrollo Local)

**Nombre**: `allow-capibara6-external-dev`

- **Red**: `default`
- **Puertos permitidos**: 11434, 5000, 5001, 5002, 5003, 5010, 5678, 8000
- **Origen**: `83.56.2.137/32` (tu IP pública actual)
- **Descripción**: Permite acceso a servicios Capibara6 desde desarrollo local

Esta regla permite que tu portátil se conecte a los servicios usando las IPs externas.

## 📋 Puertos Configurados

| Puerto | Servicio | VM |
|--------|----------|----|
| 11434 | Ollama | Bounty2 |
| 5000 | Bridge | gpt-oss-20b |
| 5001 | Backend Flask | Bounty2 |
| 5002 | TTS | gpt-oss-20b |
| 5003 | MCP Server | gpt-oss-20b |
| 5010 | MCP Server Alt | gpt-oss-20b |
| 5678 | N8n | gpt-oss-20b |
| 8000 | RAG API | rag3 |

## ✅ Verificar Reglas

Para verificar que las reglas están creadas correctamente:

```bash
gcloud compute firewall-rules list \
  --project=mamba-001 \
  --filter="name~allow-capibara6" \
  --format="table(name,network,direction,sourceRanges.list():label=SOURCE_RANGES,allowed[].map().firewall_rule().list():label=ALLOW)"
```

## 🔄 Actualizar IP Externa

Si tu IP pública cambia (por ejemplo, al cambiar de red WiFi), necesitas actualizar la regla externa:

```bash
# Eliminar regla antigua
gcloud compute firewall-rules delete allow-capibara6-external-dev --project=mamba-001 --quiet

# Obtener nueva IP
NUEVA_IP=$(curl -s https://api.ipify.org)

# Crear nueva regla
gcloud compute firewall-rules create allow-capibara6-external-dev \
  --project=mamba-001 \
  --network=default \
  --allow=tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=$NUEVA_IP/32 \
  --description="Permitir acceso a servicios Capibara6 desde desarrollo local" \
  --direction=INGRESS \
  --priority=1000
```

O usar el script automático:

```bash
bash scripts/configure_firewall_auto.sh
```

## 🧪 Probar Conexiones

Ahora puedes probar las conexiones:

```bash
bash scripts/verify_all_services.sh
```

O manualmente:

```bash
# Ollama (debería funcionar)
curl http://34.12.166.76:11434/api/tags

# Backend Flask (verificar que el servicio esté corriendo)
curl http://34.12.166.76:5001/api/health

# TTS
curl http://34.175.136.104:5002/api/tts/voices

# MCP
curl http://34.175.136.104:5003/api/mcp/status

# N8n
curl http://34.175.136.104:5678/healthz

# Bridge
curl http://34.175.136.104:5000/api/health
```

## ⚠️ Notas Importantes

1. **IP Pública Dinámica**: Si tu IP cambia, actualiza la regla externa.

2. **Servicios deben estar corriendo**: El firewall solo permite el tráfico, pero los servicios deben estar activos en cada VM.

3. **Servicios deben escuchar en 0.0.0.0**: Los servicios deben estar configurados para escuchar en `0.0.0.0` y no solo en `127.0.0.1`.

4. **Verificar servicios en VMs**: Asegúrate de que los servicios están corriendo ejecutando `bash scripts/check_services_on_vm.sh` en cada VM.

## 🎯 Próximos Pasos

1. ✅ Firewall configurado
2. ⏭️ Verificar que los servicios están corriendo en cada VM
3. ⏭️ Probar las conexiones desde tu portátil
4. ⏭️ Si algún servicio no responde, verificar que está escuchando en `0.0.0.0`

---

**Última actualización**: Noviembre 2025
**IP pública configurada**: 83.56.2.137

