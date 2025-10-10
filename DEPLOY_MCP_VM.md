# 🚀 Deploy Smart MCP a la VM

Este documento explica cómo deployar el servidor Smart MCP en la misma VM donde corre el modelo Gemma 3-12B.

---

## 📋 Prerequisitos

- ✅ VM de GCP corriendo con el modelo Gemma 3-12B
- ✅ Python 3 instalado en la VM
- ✅ Acceso SSH a la VM
- ✅ Puerto 5003 abierto en el firewall de GCP

---

## 🔧 Opción 1: Deploy Automático (Windows)

Ejecuta desde tu PC:

```cmd
deploy_mcp_to_vm.bat
```

Este script:
1. Crea directorios en la VM
2. Copia archivos del backend
3. Instala dependencias
4. Te da instrucciones para iniciar el servidor

---

## 🔧 Opción 2: Deploy Manual

### Paso 1: Conectar a la VM

```bash
gcloud compute ssh gemma-3-12b --zone=us-east1-b
```

### Paso 2: Crear Directorio

```bash
mkdir -p ~/capibara6/backend
cd ~/capibara6/backend
```

### Paso 3: Copiar Archivos

Desde tu PC local (en otra terminal):

```bash
gcloud compute scp backend/smart_mcp_server.py gemma-3-12b:~/capibara6/backend/ --zone=us-east1-b
gcloud compute scp backend/requirements.txt gemma-3-12b:~/capibara6/backend/ --zone=us-east1-b
```

### Paso 4: Instalar Dependencias en la VM

En la VM:

```bash
cd ~/capibara6/backend
python3 -m pip install --user flask flask-cors
```

### Paso 5: Iniciar Smart MCP con Screen

```bash
screen -S smart-mcp
python3 smart_mcp_server.py
```

**Desconectar del screen:** `Ctrl+A` luego `D`

**Reconectar:** `screen -r smart-mcp`

---

## 🔥 Opción 3: Configurar como Servicio Systemd (Recomendado)

### Crear archivo de servicio

```bash
sudo nano /etc/systemd/system/smart-mcp.service
```

Pegar:

```ini
[Unit]
Description=Smart MCP Server for Capibara6
After=network.target

[Service]
Type=simple
User=gmarco
WorkingDirectory=/home/gmarco/capibara6/backend
Environment="PATH=/home/gmarco/.local/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 smart_mcp_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Activar el servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable smart-mcp
sudo systemctl start smart-mcp
sudo systemctl status smart-mcp
```

### Ver logs

```bash
sudo journalctl -u smart-mcp -f
```

---

## 🌐 Configurar Firewall en GCP

Abrir puerto 5003:

```bash
gcloud compute firewall-rules create allow-smart-mcp \
    --allow=tcp:5003 \
    --source-ranges=0.0.0.0/0 \
    --description="Permitir acceso al Smart MCP Server"
```

---

## ✅ Verificar Funcionamiento

### Desde la VM:

```bash
curl http://localhost:5003/health
```

### Desde tu PC:

```bash
curl http://34.175.104.187:5003/health
```

Deberías recibir:

```json
{
  "service": "capibara6-mcp",
  "status": "healthy",
  "contexts_available": 3,
  "tools_available": 3,
  "timestamp": "2025-10-10T..."
}
```

---

## 🎯 Servicios Corriendo en la VM

Una vez completado, tendrás:

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **Gemma 3-12B** | 8080 | Modelo de lenguaje |
| **Smart MCP** | 5003 | Contexto verificado |

---

## 📊 URLs Finales

- **Modelo:** `http://34.175.104.187:8080`
- **Smart MCP:** `http://34.175.104.187:5003`
- **Web (Vercel):** `https://capibara6.vercel.app`

---

## 🐛 Troubleshooting

### Smart MCP no responde:

```bash
# Ver si el proceso está corriendo
ps aux | grep smart_mcp

# Ver logs
sudo journalctl -u smart-mcp -n 50

# Reiniciar servicio
sudo systemctl restart smart-mcp
```

### Firewall bloqueando:

```bash
# Verificar reglas
gcloud compute firewall-rules list | grep 5003

# Abrir puerto manualmente
sudo ufw allow 5003
```

---

## 📝 Notas

- El Smart MCP se reiniciará automáticamente si falla
- Los logs se guardan en el journal de systemd
- El servicio se inicia automáticamente al reiniciar la VM
- CORS está configurado para aceptar desde Vercel y localhost

---

**¡Listo! El Smart MCP estará corriendo en la VM junto al modelo.** 🎉

