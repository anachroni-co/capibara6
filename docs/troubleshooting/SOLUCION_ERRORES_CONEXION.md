# 🔧 Solución de Errores de Conexión

## ❌ Errores Detectados

### 1. Backend en bounty2 (puerto 5001)
**Error**: `POST http://34.12.166.76:5001/api/ai/classify net::ERR_CONNECTION_REFUSED`

**Causa**: El servicio no está corriendo en el puerto 5001

**Solución**: Iniciar el servidor integrado con Ollama

### 2. Smart MCP Server en gpt-oss-20b (puerto 5010)
**Error**: `GET http://34.175.136.104:5010/health net::ERR_CONNECTION_REFUSED`

**Causa**: El servicio no está corriendo o no está escuchando en 0.0.0.0

**Solución**: Iniciar el Smart MCP Server

### 3. N8n en gpt-oss-20b (puerto 5678)
**Error**: `GET http://34.175.136.104:5678/healthz net::ERR_CONNECTION_TIMED_OUT`

**Causa**: N8n no está corriendo o firewall bloquea el puerto

**Solución**: Verificar e iniciar N8n

## ✅ Soluciones por VM

### VM: bounty2 (34.12.166.76)

#### Iniciar Backend en Puerto 5001

```bash
# Conectarse a la VM
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Ir al directorio del backend
cd ~/capibara6/backend

# Verificar qué servidor usar
ls -la *integrated*.py *server*.py

# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor en screen
screen -dmS capibara6-backend bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5001
    export OLLAMA_BASE_URL=http://localhost:11434
    python3 capibara6_integrated_server_ollama.py || python3 capibara6_integrated_server.py || python3 server_gptoss.py
"

# Verificar que esté corriendo
sleep 3
curl http://localhost:5001/api/health

# Ver logs si es necesario
screen -r capibara6-backend
```

#### Verificar que el servidor escuche en 0.0.0.0

El servidor debe iniciarse con `host='0.0.0.0'` para aceptar conexiones externas.

### VM: gpt-oss-20b (34.175.136.104)

#### Iniciar Smart MCP Server (puerto 5010)

```bash
# Conectarse a la VM
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Ir al directorio del backend
cd ~/capibara6/backend

# Iniciar Smart MCP Server en screen
screen -dmS smart-mcp bash -c "
    cd ~/capibara6/backend
    source venv/bin/activate
    export PORT=5010
    python3 smart_mcp_server.py
"

# Verificar que esté corriendo
sleep 3
curl http://localhost:5010/health

# Ver logs si es necesario
screen -r smart-mcp
```

#### Iniciar N8n (puerto 5678)

```bash
# Verificar si N8n está instalado
which n8n || npm list -g n8n

# Si está instalado, iniciarlo
screen -dmS n8n bash -c "n8n start"

# O si está en Docker
docker ps | grep n8n || docker-compose up -d n8n

# Verificar que esté corriendo
curl http://localhost:5678/healthz
```

## 🔥 Verificar Firewall

Asegúrate de que los puertos estén abiertos:

```bash
# Ver reglas de firewall existentes
gcloud compute firewall-rules list --project=mamba-001 --filter="name~'allow'"

# Crear reglas si no existen
gcloud compute firewall-rules create allow-bounty2-backend \
  --allow tcp:5001 \
  --source-ranges 0.0.0.0/0 \
  --target-tags bounty2 \
  --description "Backend Capibara6 en bounty2"

gcloud compute firewall-rules create allow-gptoss-mcp \
  --allow tcp:5010 \
  --source-ranges 0.0.0.0/0 \
  --target-tags gpt-oss-20b \
  --description "Smart MCP Server en gpt-oss-20b"

gcloud compute firewall-rules create allow-gptoss-n8n \
  --allow tcp:5678 \
  --source-ranges 0.0.0.0/0 \
  --target-tags gpt-oss-20b \
  --description "N8n en gpt-oss-20b"
```

## 📝 Scripts de Inicio Automático

He creado scripts para facilitar el inicio de servicios:

- `scripts/start_bounty2_services.sh` - Inicia servicios en bounty2
- `scripts/check_bounty2_status.sh` - Verifica estado en bounty2

## 🧪 Verificación Final

Después de iniciar los servicios, verifica desde tu PC local:

```bash
# Backend en bounty2
curl http://34.12.166.76:5001/api/health

# Smart MCP en gpt-oss-20b
curl http://34.175.136.104:5010/health

# N8n en gpt-oss-20b
curl http://34.175.136.104:5678/healthz
```

Si todos responden correctamente, el frontend debería funcionar sin errores.
