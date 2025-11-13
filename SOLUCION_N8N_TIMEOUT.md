# 🔧 Solución al Timeout de N8N

## ❌ Problema

```
http://34.175.136.104:5678/healthz net::ERR_CONNECTION_TIMED_OUT
```

El frontend no puede conectarse a N8N en la VM `gpt-oss-20b` (puerto 5678).

## 🔍 Causas Posibles

1. **Firewall de GCP bloqueando el puerto 5678**
2. **N8N no está corriendo en la VM**
3. **N8N no está escuchando en `0.0.0.0` (solo en localhost)**

## ✅ Soluciones

### 1. Verificar y Configurar Firewall

Ejecuta el script para configurar el firewall:

```bash
chmod +x configurar_firewall_n8n.sh
./configurar_firewall_n8n.sh
```

O manualmente:

```bash
# Crear regla de firewall
gcloud compute firewall-rules create allow-n8n-5678 \
    --project=mamba-001 \
    --allow tcp:5678 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow N8N access on port 5678" \
    --target-tags n8n-server

# Añadir tag a la VM
gcloud compute instances add-tags gpt-oss-20b \
    --zone=europe-southwest1-b \
    --project=mamba-001 \
    --tags n8n-server
```

### 2. Verificar que N8N está Corriendo

```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="
    # Verificar proceso
    ps aux | grep -i n8n | grep -v grep
    
    # Verificar puerto
    sudo netstat -tlnp | grep 5678 || sudo ss -tlnp | grep 5678
    
    # Verificar servicio systemd
    sudo systemctl status n8n.service
"
```

### 3. Iniciar N8N si No Está Corriendo

```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="
    # Iniciar servicio
    sudo systemctl start n8n.service
    
    # Habilitar inicio automático
    sudo systemctl enable n8n.service
    
    # Verificar estado
    sudo systemctl status n8n.service
"
```

### 4. Verificar Configuración de N8N

Asegúrate de que N8N esté configurado para escuchar en `0.0.0.0`:

```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="
    # Verificar variables de entorno del servicio
    sudo systemctl show n8n.service | grep N8N_HOST
    
    # Ver archivo de servicio
    sudo cat /etc/systemd/system/n8n.service | grep N8N_HOST
"
```

Debería mostrar `N8N_HOST=0.0.0.0`. Si no, edita el servicio:

```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="
    sudo systemctl edit n8n.service
    # Añadir:
    # [Service]
    # Environment='N8N_HOST=0.0.0.0'
    # Environment='N8N_PORT=5678'
    
    sudo systemctl daemon-reload
    sudo systemctl restart n8n.service
"
```

### 5. Probar Conexión

```bash
# Desde local
curl -v http://34.175.136.104:5678/healthz

# Desde la VM (debería funcionar)
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="curl http://localhost:5678/healthz"
```

## 🔄 Script de Verificación Completa

Ejecuta el script de verificación:

```bash
chmod +x verificar_n8n_y_firewall.sh
./verificar_n8n_y_firewall.sh
```

## 📝 Endpoint `/api/ai/generate`

También se ha añadido el endpoint `/api/ai/generate` al proxy CORS local para que funcione correctamente desde el frontend.

## ✅ Checklist

- [ ] Firewall de GCP configurado para puerto 5678
- [ ] Tag `n8n-server` añadido a la VM `gpt-oss-20b`
- [ ] N8N corriendo en la VM
- [ ] N8N escuchando en `0.0.0.0:5678`
- [ ] Conexión desde local funciona (`curl http://34.175.136.104:5678/healthz`)
- [ ] Frontend puede conectarse a N8N

---

**Última actualización**: Noviembre 2025

