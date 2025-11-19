# 🚀 Instrucciones para Iniciar Servicios

## ⚡ Inicio Rápido

Ejecuta el script automatizado:

```bash
./scripts/start_all_services.sh
```

Este script iniciará automáticamente:
- ✅ Backend en bounty2 (puerto 5001)
- ✅ Smart MCP en gpt-oss-20b (puerto 5010)
- ✅ N8n en gpt-oss-20b (puerto 5678) - si está disponible

## 🔧 Inicio Manual

### 1. Backend en bounty2 (Puerto 5001)

```bash
# Conectarse a bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Ir al backend
cd ~/capibara6/backend

# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor en screen
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server_ollama.py
"

# Verificar
sleep 3
curl http://localhost:5001/api/health

# Ver logs
screen -r capibara6-backend
```

### 2. Smart MCP en gpt-oss-20b (Puerto 5010)

```bash
# Conectarse a gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Ir al backend
cd ~/capibara6/backend

# Activar entorno virtual
source venv/bin/activate

# Iniciar Smart MCP en screen
screen -dmS smart-mcp bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5010
    python3 smart_mcp_server.py
"

# Verificar
sleep 3
curl http://localhost:5010/health

# Ver logs
screen -r smart-mcp
```

### 3. N8n en gpt-oss-20b (Puerto 5678)

```bash
# Conectarse a gpt-oss-20b
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Si N8n está instalado globalmente
screen -dmS n8n bash -c "n8n start"

# O si está en Docker
docker-compose up -d n8n

# Verificar
curl http://localhost:5678/healthz
```

## 🔍 Verificar Estado

### Desde tu PC local:

```bash
# Backend en bounty2
curl http://34.12.166.76:5001/api/health

# Smart MCP en gpt-oss-20b
curl http://34.175.136.104:5010/health

# N8n en gpt-oss-20b
curl http://34.175.136.104:5678/healthz
```

### Desde dentro de las VMs:

```bash
# Ver screens activos
screen -ls

# Ver procesos en puertos
sudo ss -tulnp | grep -E "(5001|5010|5678)"

# Ver logs de un screen
screen -r [nombre-del-screen]
```

## 🛑 Detener Servicios

### Detener Backend en bounty2:

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
screen -S capibara6-backend -X quit
# O matar el proceso directamente
kill $(lsof -ti:5001)
```

### Detener Smart MCP en gpt-oss-20b:

```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
screen -S smart-mcp -X quit
# O matar el proceso directamente
kill $(lsof -ti:5010)
```

### Detener N8n:

```bash
screen -S n8n -X quit
# O si está en Docker
docker-compose stop n8n
```

## 🔥 Verificar Firewall

Si los servicios no responden desde fuera, verifica el firewall:

```bash
# Ver reglas existentes
gcloud compute firewall-rules list --project=mamba-001

# Crear reglas si no existen
gcloud compute firewall-rules create allow-bounty2-backend \
  --allow tcp:5001 \
  --source-ranges 0.0.0.0/0 \
  --target-tags bounty2

gcloud compute firewall-rules create allow-gptoss-mcp \
  --allow tcp:5010 \
  --source-ranges 0.0.0.0/0 \
  --target-tags gpt-oss-20b

gcloud compute firewall-rules create allow-gptoss-n8n \
  --allow tcp:5678 \
  --source-ranges 0.0.0.0/0 \
  --target-tags gpt-oss-20b
```

## ⚠️ Troubleshooting

### El servicio no responde desde fuera

1. **Verificar que escucha en 0.0.0.0**:
   ```bash
   sudo ss -tulnp | grep [puerto]
   ```
   Debe mostrar `0.0.0.0:[puerto]`, no `127.0.0.1:[puerto]`

2. **Verificar firewall**:
   ```bash
   gcloud compute firewall-rules list --project=mamba-001
   ```

3. **Verificar logs**:
   ```bash
   screen -r [nombre-del-screen]
   ```

### El servicio se detiene al cerrar SSH

Usa `screen` o `tmux` para mantener los servicios corriendo:

```bash
screen -dmS [nombre] bash -c "[comando]"
```

### Puerto ya en uso

```bash
# Ver qué proceso usa el puerto
lsof -ti:5001

# Matar el proceso
kill $(lsof -ti:5001)
```

## ✅ Checklist Final

- [ ] Backend en bounty2 corriendo en puerto 5001
- [ ] Smart MCP en gpt-oss-20b corriendo en puerto 5010
- [ ] N8n corriendo (opcional) en puerto 5678
- [ ] Firewall configurado para todos los puertos
- [ ] Servicios responden desde local
- [ ] Frontend puede conectarse sin errores

