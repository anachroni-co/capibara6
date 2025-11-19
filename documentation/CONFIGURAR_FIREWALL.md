# 🔒 Configuración de Firewall para Capibara6

Este documento explica cómo configurar las reglas de firewall en Google Cloud para permitir el acceso a los servicios de Capibara6.

## 📋 Puertos que Necesitan Estar Abiertos

| Servicio | VM | Puerto | Descripción |
|----------|----|--------|-------------|
| Ollama | Bounty2 | 11434 | API de Ollama |
| Backend Flask | Bounty2 | 5001 | Servidor backend principal |
| Bridge | gpt-oss-20b | 5000 | Servicio Bridge |
| TTS | gpt-oss-20b | 5002 | Text-to-Speech |
| MCP | gpt-oss-20b | 5003 | MCP Server |
| MCP Alt | gpt-oss-20b | 5010 | MCP Server alternativo |
| N8n | gpt-oss-20b | 5678 | Automatización N8n |
| RAG API | rag3 | 8000 | API de RAG |

## 🚀 Opción 1: Configuración Automática (Recomendada)

Ejecuta el script automático:

```bash
bash scripts/configure_firewall_auto.sh
```

Este script:
- Detecta tu IP pública automáticamente
- Crea reglas para comunicación interna entre VMs
- Crea reglas para acceso externo desde tu IP
- Configura todos los puertos necesarios

## 🔧 Opción 2: Configuración Manual

### Paso 1: Obtener tu IP Pública

```bash
curl https://api.ipify.org
```

Anota esta IP, la necesitarás para la regla externa.

### Paso 2: Obtener el Nombre de la Red VPC

```bash
gcloud compute networks list --project=mamba-001
```

Anota el nombre de la red (probablemente `default` o similar).

### Paso 3: Crear Regla para Comunicación Interna

Esta regla permite que las VMs se comuniquen entre sí usando IPs internas:

```bash
gcloud compute firewall-rules create allow-capibara6-internal \
  --project=mamba-001 \
  --network=default \
  --allow=tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=10.0.0.0/8 \
  --description="Permitir comunicación interna entre VMs de Capibara6" \
  --direction=INGRESS \
  --priority=1000
```

**Nota**: Reemplaza `default` con el nombre de tu red VPC si es diferente.

### Paso 4: Crear Regla para Acceso Externo

Esta regla permite acceso desde tu portátil (desarrollo local):

```bash
# Reemplaza TU_IP_PUBLICA con tu IP pública obtenida en el Paso 1
gcloud compute firewall-rules create allow-capibara6-external-dev \
  --project=mamba-001 \
  --network=default \
  --allow=tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=TU_IP_PUBLICA/32 \
  --description="Permitir acceso a servicios Capibara6 desde desarrollo local" \
  --direction=INGRESS \
  --priority=1000
```

**Ejemplo**:
```bash
gcloud compute firewall-rules create allow-capibara6-external-dev \
  --project=mamba-001 \
  --network=default \
  --allow=tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=123.45.67.89/32 \
  --description="Permitir acceso a servicios Capibara6 desde desarrollo local" \
  --direction=INGRESS \
  --priority=1000
```

## ✅ Verificar Reglas Creadas

Para ver todas las reglas de firewall relacionadas con Capibara6:

```bash
gcloud compute firewall-rules list \
  --project=mamba-001 \
  --filter="name~allow-capibara6" \
  --format="table(name,network,direction,priority,sourceRanges.list():label=SOURCE_RANGES,allowed[].map().firewall_rule().list():label=ALLOW)"
```

## 🔍 Ver Detalles de una Regla Específica

```bash
gcloud compute firewall-rules describe allow-capibara6-internal --project=mamba-001
gcloud compute firewall-rules describe allow-capibara6-external-dev --project=mamba-001
```

## 🗑️ Eliminar Reglas (si es necesario)

Si necesitas eliminar una regla:

```bash
# Eliminar regla interna
gcloud compute firewall-rules delete allow-capibara6-internal --project=mamba-001 --quiet

# Eliminar regla externa
gcloud compute firewall-rules delete allow-capibara6-external-dev --project=mamba-001 --quiet
```

## 📝 Comandos Completos (Copia y Pega)

Si tu IP pública es, por ejemplo, `123.45.67.89` y tu red es `default`:

```bash
# 1. Regla interna
gcloud compute firewall-rules create allow-capibara6-internal \
  --project=mamba-001 \
  --network=default \
  --allow=tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=10.0.0.0/8 \
  --description="Permitir comunicación interna entre VMs de Capibara6" \
  --direction=INGRESS \
  --priority=1000

# 2. Regla externa (reemplaza 123.45.67.89 con tu IP)
gcloud compute firewall-rules create allow-capibara6-external-dev \
  --project=mamba-001 \
  --network=default \
  --allow=tcp:11434,tcp:5000,tcp:5001,tcp:5002,tcp:5003,tcp:5010,tcp:5678,tcp:8000 \
  --source-ranges=123.45.67.89/32 \
  --description="Permitir acceso a servicios Capibara6 desde desarrollo local" \
  --direction=INGRESS \
  --priority=1000
```

## ⚠️ Notas Importantes

1. **IP Pública Dinámica**: Si tu IP pública cambia (por ejemplo, al cambiar de red), necesitarás actualizar la regla externa o crear una nueva.

2. **Múltiples IPs**: Si trabajas desde diferentes ubicaciones, puedes crear múltiples reglas o usar un rango de IPs.

3. **Seguridad**: Las reglas externas solo permiten acceso desde tu IP específica. Esto es seguro para desarrollo, pero para producción considera usar un VPN o Cloud Load Balancer.

4. **Prioridad**: Las reglas tienen prioridad 1000. Si tienes otras reglas con mayor prioridad que bloquean estos puertos, ajusta la prioridad.

## 🧪 Probar las Conexiones

Después de configurar el firewall, prueba las conexiones:

```bash
bash scripts/verify_all_services.sh
```

O manualmente:

```bash
# Ollama
curl http://34.12.166.76:11434/api/tags

# Backend Flask
curl http://34.12.166.76:5001/api/health

# TTS
curl http://34.175.136.104:5002/api/tts/voices

# MCP
curl http://34.175.136.104:5003/api/mcp/status

# N8n
curl http://34.175.136.104:5678/healthz
```

## 🐛 Troubleshooting

### Problema: Las reglas no se aplican

1. Verifica que estás usando el proyecto correcto:
   ```bash
   gcloud config set project mamba-001
   ```

2. Verifica que la red VPC es correcta:
   ```bash
   gcloud compute networks list --project=mamba-001
   ```

3. Verifica que las VMs están en la misma red:
   ```bash
   gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001 --format="value(networkInterfaces[0].network)"
   ```

### Problema: No puedo conectarme desde mi portátil

1. Verifica tu IP pública actual:
   ```bash
   curl https://api.ipify.org
   ```

2. Verifica que la regla externa incluye tu IP:
   ```bash
   gcloud compute firewall-rules describe allow-capibara6-external-dev --project=mamba-001
   ```

3. Verifica que los servicios están escuchando en `0.0.0.0` y no solo en `127.0.0.1`

### Problema: Las VMs no pueden comunicarse entre sí

1. Verifica que están en la misma red VPC
2. Verifica que la regla interna está creada y activa
3. Verifica que estás usando IPs internas para comunicación entre VMs

---

**Última actualización**: Noviembre 2025

