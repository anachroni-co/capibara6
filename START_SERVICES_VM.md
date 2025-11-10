# 🚀 Guía Rápida: Iniciar Servicios en VM gpt-oss-20b

## 📋 Resumen

En la VM **gpt-oss-20b** (34.175.136.104) deben correr estos servicios:

| Servicio | Puerto | Archivo | Script de inicio |
|----------|--------|---------|------------------|
| **TTS** | 5002 | coqui_tts_server.py | ./start_coqui_tts.sh |
| **MCP** | 5003 | mcp_server.py | (manual) |
| **N8N** | 5678 | (Node.js app) | (ver abajo) |

---

## 🔧 Paso 1: Conectarse a la VM

```bash
# Desde tu máquina local:
./ssh-services.sh

# O directamente:
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

---

## 🎙️ Paso 2: Iniciar TTS (Coqui) - Puerto 5002

```bash
cd ~/capibara6/backend

# Opción 1: Con script (recomendado)
./start_coqui_tts.sh

# Opción 2: En background con screen
screen -S tts
./start_coqui_tts.sh
# Presionar Ctrl+A, luego D para desconectar
```

**Verificar:**
```bash
curl http://localhost:5002/health
```

---

## 🧠 Paso 3: Iniciar MCP - Puerto 5003

```bash
cd ~/capibara6/backend

# Opción 1: Directamente
python3 mcp_server.py

# Opción 2: En background con screen
screen -S mcp
python3 mcp_server.py
# Presionar Ctrl+A, luego D para desconectar

# Opción 3: Con nohup
nohup python3 mcp_server.py > mcp.log 2>&1 &
```

**Verificar:**
```bash
curl http://localhost:5003/health
```

---

## 🔄 Paso 4: Iniciar N8N - Puerto 5678

N8N es una aplicación Node.js separada.

### Si N8N ya está instalado:

```bash
# Verificar si n8n está instalado
which n8n

# Si está instalado, iniciar:
screen -S n8n
n8n start
# Presionar Ctrl+A, luego D para desconectar
```

### Si N8N NO está instalado:

```bash
# Instalar Node.js (si no está instalado)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar N8N globalmente
sudo npm install -g n8n

# Iniciar N8N
screen -S n8n
export N8N_HOST=0.0.0.0
export N8N_PORT=5678
n8n start
# Presionar Ctrl+A, luego D para desconectar
```

**Verificar:**
```bash
curl http://localhost:5678
# O desde navegador: http://34.175.136.104:5678
```

---

## ✅ Paso 5: Verificación Final

```bash
# Verificar todos los servicios
curl http://localhost:5002/health  # TTS
curl http://localhost:5003/health  # MCP
curl http://localhost:5678         # N8N

# Ver puertos en uso
netstat -tulpn | grep -E "5002|5003|5678"

# Ver screens activos
screen -ls
```

---

## 🔥 Firewall (si es necesario)

Si los servicios no son accesibles desde fuera de la VM:

### Google Cloud Firewall:

```bash
# Desde tu máquina local (no desde la VM)
gcloud compute firewall-rules create allow-capibara6-services \
  --project="mamba-001" \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5002,tcp:5003,tcp:5678 \
  --source-ranges=0.0.0.0/0 \
  --description="Allow TTS, MCP, N8N services"
```

### Firewall local (ufw):

```bash
# En la VM gpt-oss-20b
sudo ufw allow 5002/tcp  # TTS
sudo ufw allow 5003/tcp  # MCP
sudo ufw allow 5678/tcp  # N8N
sudo ufw reload
```

---

## 📊 Comandos Útiles

### Ver logs de servicios en screen:

```bash
screen -r tts    # Ver logs de TTS
screen -r mcp    # Ver logs de MCP
screen -r n8n    # Ver logs de N8N
# Presionar Ctrl+A, luego D para salir sin detener
```

### Detener servicios:

```bash
# Si están en screen:
screen -S tts -X quit
screen -S mcp -X quit
screen -S n8n -X quit

# Si están como procesos:
pkill -f coqui_tts_server.py
pkill -f mcp_server.py
pkill -f n8n
```

### Reiniciar servicios:

```bash
# Detener
screen -S tts -X quit
screen -S mcp -X quit

# Iniciar de nuevo
screen -S tts -dm bash -c "cd ~/capibara6/backend && ./start_coqui_tts.sh"
screen -S mcp -dm bash -c "cd ~/capibara6/backend && python3 mcp_server.py"
```

---

## 🔍 Troubleshooting

### Puerto ya en uso:

```bash
# Ver qué proceso usa el puerto
lsof -i :5002
lsof -i :5003
lsof -i :5678

# Matar proceso específico
kill -9 <PID>
```

### Servicio no responde:

```bash
# Ver logs si está en screen
screen -r tts

# Ver logs si está con nohup
tail -f mcp.log
```

### Dependencias faltantes:

```bash
# Para TTS
pip install flask flask-cors TTS

# Para MCP
pip install flask flask-cors requests
```

---

## 📝 Notas

- **TTS**: Primera ejecución puede tardar 30-60 segundos descargando modelo
- **MCP**: Lightweight, inicia rápido
- **N8N**: Interfaz web accesible en http://34.175.136.104:5678
- **Screens**: Útiles para mantener servicios corriendo al desconectar SSH

---

**Última actualización**: 2025-11-10
**VM**: gpt-oss-20b (34.175.136.104)
