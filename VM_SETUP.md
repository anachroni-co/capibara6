# 🌐 Configuración de VMs de Google Cloud - Capibara6

## 📋 Información de las VMs

### VM 1: Modelos (bounty2)
- **Nombre**: bounty2
- **IP Externa**: 34.12.166.76
- **Zona**: europe-west4-a
- **Proyecto**: mamba-001
- **Servicios**:
  - Puerto 8080: GPT-OSS-20B (Modelo de lenguaje)
  - Puerto 5001: Backend API Flask

**Conectarse:**
```bash
./ssh-bounty2.sh
# O directamente:
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### VM 2: Servicios (gpt-oss-20b)
- **Nombre**: gpt-oss-20b
- **IP Externa**: 34.175.136.104
- **Zona**: europe-southwest1-b
- **Proyecto**: mamba-001
- **Servicios**:
  - Puerto 5002: TTS (Text-to-Speech)
  - Puerto 5003: MCP (Model Context Protocol)
  - Puerto 5678: N8N (Automatización)

**Conectarse:**
```bash
./ssh-services.sh
# O directamente:
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

---

## 🚀 Scripts de Gestión

### Verificar estado de VMs:
```bash
./check-vms.sh
```

Este script:
- ✅ Lista el estado de ambas VMs
- ✅ Prueba conectividad a cada servicio
- ✅ Muestra qué servicios están accesibles
- ✅ Da recomendaciones si algo falla

---

## 🔧 Configuración Inicial

### 1. Verificar que las VMs estén encendidas:

```bash
gcloud compute instances list --project "mamba-001"
```

Si alguna está apagada (STATUS: TERMINATED):
```bash
# Encender VM de modelos
gcloud compute instances start bounty2 --zone="europe-west4-a" --project="mamba-001"

# Encender VM de servicios
gcloud compute instances start gpt-oss-20b --zone="europe-southwest1-b" --project="mamba-001"
```

### 2. Configurar reglas de firewall:

```bash
# Crear regla para VM de modelos (bounty2)
gcloud compute firewall-rules create allow-capibara6-models \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5001,tcp:8080 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-models \
  --description="Allow Capibara6 model services"

# Crear regla para VM de servicios (gpt-oss-20b)
gcloud compute firewall-rules create allow-capibara6-services \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5002,tcp:5003,tcp:5678 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=capibara6-services \
  --description="Allow Capibara6 auxiliary services"

# Aplicar tags a las instancias
gcloud compute instances add-tags bounty2 \
  --zone="europe-west4-a" \
  --project="mamba-001" \
  --tags=capibara6-models

gcloud compute instances add-tags gpt-oss-20b \
  --zone="europe-southwest1-b" \
  --project="mamba-001" \
  --tags=capibara6-services
```

### 3. Verificar reglas existentes:

```bash
gcloud compute firewall-rules list --project="mamba-001" | grep -E "capibara|5001|5002|5003|8080|5678"
```

---

## 🔍 Verificación de Servicios

### En VM de Modelos (bounty2):

```bash
# Conectarse
./ssh-bounty2.sh

# Una vez dentro, verificar servicios
ps aux | grep -E "python|llama|server"
netstat -tulpn | grep -E "8080|5001"
sudo systemctl status gpt-oss  # O el nombre del servicio
```

**Iniciar servicios si no están corriendo:**
```bash
# Ejemplo genérico - ajustar según tu configuración:
cd ~/gpt-oss-20b  # O el directorio correcto
./start_server.sh

# O si es un servicio systemd:
sudo systemctl start gpt-oss
sudo systemctl enable gpt-oss  # Para auto-inicio
```

### En VM de Servicios (gpt-oss-20b):

```bash
# Conectarse
./ssh-services.sh

# Verificar servicios
ps aux | grep -E "tts|mcp|n8n"
netstat -tulpn | grep -E "5002|5003|5678"

# Verificar estado de servicios
sudo systemctl status tts-service
sudo systemctl status mcp-service
sudo systemctl status n8n
```

---

## 🐛 Troubleshooting

### Problema: "Connection refused" al hacer curl

**Posibles causas:**
1. VM apagada
2. Servicio no está corriendo
3. Firewall bloqueando

**Soluciones:**

```bash
# 1. Verificar que VM esté encendida
gcloud compute instances describe bounty2 --zone="europe-west4-a" --project="mamba-001" | grep status

# 2. Conectarse y verificar servicios
./ssh-bounty2.sh
ps aux | grep server
sudo systemctl status nombre-del-servicio

# 3. Verificar firewall
gcloud compute firewall-rules list --project="mamba-001"
# Verificar que existan reglas para los puertos necesarios
```

### Problema: "404 Not Found" al hacer curl

**Causa:** El servicio está corriendo pero el endpoint no existe o la ruta es incorrecta.

**Solución:**
```bash
# Conectarse a la VM
./ssh-services.sh

# Revisar logs del servicio
sudo journalctl -u nombre-del-servicio -n 50

# Verificar qué endpoints están disponibles
curl http://localhost:5002/  # Puede mostrar rutas disponibles
```

### Problema: IP externa cambió

Las IPs externas de GCP pueden cambiar si la VM se detiene. Para verificar:

```bash
# Ver IPs actuales
gcloud compute instances list --project="mamba-001" --format="table(name,zone,networkInterfaces[0].accessConfigs[0].natIP)"
```

Si cambiaron, actualizar en:
- `backend/.env`
- `web/config.js`

---

## 📊 Monitoreo

### Ver logs en tiempo real:

**VM de modelos:**
```bash
./ssh-bounty2.sh
sudo journalctl -u gpt-oss -f
# O si es un proceso manual:
tail -f ~/logs/gpt-oss.log
```

**VM de servicios:**
```bash
./ssh-services.sh
sudo journalctl -u tts-service -f
sudo journalctl -u mcp-service -f
sudo journalctl -u n8n -f
```

### Uso de recursos:

```bash
# CPU y RAM
top
htop  # Si está instalado

# Disco
df -h

# Red
netstat -an | grep ESTABLISHED | wc -l
```

---

## 💰 Gestión de Costos

### Detener VMs cuando no se usan:

```bash
# Detener VM de modelos
gcloud compute instances stop bounty2 --zone="europe-west4-a" --project="mamba-001"

# Detener VM de servicios
gcloud compute instances stop gpt-oss-20b --zone="europe-southwest1-b" --project="mamba-001"
```

### Reiniciar VMs:

```bash
# Reiniciar VM de modelos
gcloud compute instances start bounty2 --zone="europe-west4-a" --project="mamba-001"

# Reiniciar VM de servicios
gcloud compute instances start gpt-oss-20b --zone="europe-southwest1-b" --project="mamba-001"
```

**Nota:** Al detener/iniciar, la IP externa puede cambiar a menos que tengas una IP estática configurada.

---

## 🔒 Seguridad

### Restringir acceso por IP (Recomendado para producción):

En lugar de `--source-ranges=0.0.0.0/0`, usa tu IP específica:

```bash
# Obtener tu IP pública
curl ifconfig.me

# Actualizar regla de firewall
gcloud compute firewall-rules update allow-capibara6-models \
  --project="mamba-001" \
  --source-ranges=TU_IP/32
```

### Usar túnel SSH para desarrollo:

```bash
# Túnel para acceder a servicios como si fueran locales
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001" \
  --ssh-flag="-L 8080:localhost:8080" \
  --ssh-flag="-L 5001:localhost:5001"

# Ahora puedes acceder localmente:
curl http://localhost:8080/health
```

---

## 📚 Recursos Útiles

- **Console GCP**: https://console.cloud.google.com/compute/instances?project=mamba-001
- **Documentación gcloud**: https://cloud.google.com/sdk/gcloud/reference/compute
- **Logs y Monitoring**: https://console.cloud.google.com/logs?project=mamba-001

---

## ✅ Checklist de Configuración

- [ ] VMs encendidas (STATUS: RUNNING)
- [ ] Reglas de firewall creadas para puertos necesarios
- [ ] Tags aplicados a las instancias
- [ ] Servicios corriendo en ambas VMs
- [ ] Conectividad verificada con `./check-vms.sh`
- [ ] IPs externas actualizadas en `.env` y `config.js`
- [ ] Backend local funciona en modo demo
- [ ] Backend local funciona conectado a VMs

---

**Última actualización**: 2025-11-10
**Proyecto GCP**: mamba-001
**Mantenedor**: marco@anachroni.co
