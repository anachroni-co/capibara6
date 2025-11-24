# 📋 Instrucciones Completas para Verificar y Levantar Servicios

## 🎯 Objetivo

Verificar y asegurar que todos los servicios estén corriendo en las VMs y que el frontend pueda conectarse correctamente.

## 🔧 Paso 1: Verificar y Levantar Servicios en gpt-oss-20b

### Conectarse a gpt-oss-20b

```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
```

### Ejecutar Script de Verificación e Inicio

Una vez dentro de gpt-oss-20b:

```bash
# Navegar al proyecto (ajustar ruta según tu configuración)
cd ~/capibara6
# O
cd /ruta/a/tu/proyecto

# Copiar el script si no está
# (o ejecutarlo directamente si ya está en el proyecto)

# Dar permisos de ejecución
chmod +x check_and_start_gpt_oss_20b.sh

# Ejecutar
./check_and_start_gpt_oss_20b.sh
```

Este script:
- ✅ Verifica qué servicios están corriendo
- ✅ Inicia los servicios faltantes en screens separados
- ✅ Verifica que los servicios respondan correctamente
- ✅ Muestra el estado final

### Servicios que Deberían Estar Activos

| Puerto | Servicio | Archivo |
|--------|----------|---------|
| 5000 | Bridge/Main Server | `server.py` o `server_gptoss.py` |
| 5002 | TTS Server | `kyutai_tts_server.py` o `coqui_tts_server.py` |
| 5003 | MCP Server | `smart_mcp_server.py` o `mcp_server.py` |
| 5010 | MCP Server Alt | `smart_mcp_server.py` (puerto alternativo) |
| 5678 | N8n | Docker o servicio systemd |

### Verificar Screens Activos

```bash
# Ver todos los screens
screen -ls

# Entrar a un screen específico
screen -r bridge    # Para ver logs del Bridge
screen -r tts       # Para ver logs del TTS
screen -r mcp       # Para ver logs del MCP

# Salir de un screen (sin detenerlo)
# Presionar: Ctrl+A luego D

# Detener un screen
screen -X -S bridge quit
```

## 🔧 Paso 2: Verificar Servicios en bounty2

### Conectarse a bounty2

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
```

### Verificar Servicios

```bash
# Ver procesos corriendo
ps aux | grep -E "(python|ollama|node)"

# Ver puertos abiertos
sudo netstat -tuln | grep -E "(5001|5000|11434)"
# O
sudo ss -tuln | grep -E "(5001|5000|11434)"

# Probar servicios localmente
curl http://localhost:11434/api/tags  # Ollama
curl http://localhost:5001/api/health  # Backend
```

### Iniciar Backend si No Está Corriendo

```bash
cd backend

# Opción 1: Servidor integrado
python3 capibara6_integrated_server.py

# Opción 2: Servidor básico
python3 server.py

# Opción 3: En screen (para que siga corriendo)
screen -dmS backend python3 capibara6_integrated_server.py

# IMPORTANTE: Asegurar que escucha en 0.0.0.0
# Si el código tiene app.run(host='127.0.0.1'), cambiarlo a:
# app.run(host='0.0.0.0', port=5001)
```

## 🔧 Paso 3: Verificar Servicios en rag3

### Conectarse a rag3

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
```

### Verificar RAG API

```bash
# Ver procesos
ps aux | grep python

# Ver puertos
sudo netstat -tuln | grep 8000

# Probar localmente
curl http://localhost:8000/health
```

## 🌐 Paso 4: Verificar Conexiones desde el Portátil

### Ejecutar Script de Verificación

Desde tu portátil:

```bash
cd /ruta/al/proyecto
chmod +x verify_vm_connections_complete.sh
./verify_vm_connections_complete.sh
```

Este script verifica:
- ✅ Conectividad a todos los puertos
- ✅ Respuesta HTTP de los servicios
- ✅ Estado de cada servicio

### Verificar Manualmente

```bash
# Probar bounty2
curl http://34.12.166.76:11434/api/tags
curl http://34.12.166.76:5001/api/health

# Probar gpt-oss-20b
curl http://34.175.136.104:5000/api/health
curl http://34.175.136.104:5003/api/mcp/status
curl http://34.175.136.104:5678/healthz
```

## 🔗 Paso 5: Verificar Conexiones Internas entre VMs

### Obtener IPs Internas

```bash
# IP interna de bounty2
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# IP interna de rag3
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# IP interna de gpt-oss-20b
gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"
```

### Probar Conexiones Internas

**Desde bounty2:**
```bash
# Probar conexión a rag3
ping [IP_INTERNA_RAG3]
curl http://[IP_INTERNA_RAG3]:8000/health

# Probar conexión a gpt-oss-20b
ping [IP_INTERNA_GPT_OSS_20B]
curl http://[IP_INTERNA_GPT_OSS_20B]:5000/api/health
```

**Desde rag3:**
```bash
# Probar conexión a bounty2
ping [IP_INTERNA_BOUNTY2]
curl http://[IP_INTERNA_BOUNTY2]:5001/api/health
```

**Desde gpt-oss-20b:**
```bash
# Probar conexión a bounty2
ping [IP_INTERNA_BOUNTY2]
curl http://[IP_INTERNA_BOUNTY2]:5001/api/health

# Probar conexión a rag3
ping [IP_INTERNA_RAG3]
curl http://[IP_INTERNA_RAG3]:8000/health
```

## 🔥 Paso 6: Configurar Firewall de Google Cloud

Si los servicios no son accesibles desde tu portátil, configurar el firewall:

```bash
# Obtener tu IP pública
MY_IP=$(curl -s ifconfig.me)
echo "Tu IP: $MY_IP"

# Crear reglas de firewall para bounty2
gcloud compute firewall-rules create allow-bounty2-backend \
  --allow tcp:5001 \
  --source-ranges $MY_IP/32 \
  --target-tags allow-external \
  --project mamba-001 \
  --description "Permitir acceso al backend de bounty2"

gcloud compute firewall-rules create allow-bounty2-ollama \
  --allow tcp:11434 \
  --source-ranges $MY_IP/32 \
  --target-tags allow-external \
  --project mamba-001 \
  --description "Permitir acceso a Ollama en bounty2"

# Crear reglas para gpt-oss-20b
gcloud compute firewall-rules create allow-gptoss-services \
  --allow tcp:5000,tcp:5002,tcp:5003,tcp:5010,tcp:5678 \
  --source-ranges $MY_IP/32 \
  --target-tags allow-external \
  --project mamba-001 \
  --description "Permitir acceso a servicios en gpt-oss-20b"
```

## ✅ Paso 7: Probar Frontend

Una vez que todos los servicios estén corriendo:

1. **Iniciar servidor web local** (si no está corriendo):
```bash
cd web
python3 -m http.server 8000
```

2. **Abrir en navegador**:
```
http://localhost:8000/chat.html
```

3. **Abrir consola del navegador** (F12) y verificar:
   - ✅ Configuración de desarrollo local activada
   - ✅ Backend URL correcta
   - ✅ Sin errores de conexión

4. **Probar página de diagnóstico**:
```
http://localhost:8000/test_backend_connection.html
```

## 🐛 Troubleshooting

### Problema: Servicio no inicia

**Solución**:
- Verificar que Python 3 está instalado
- Verificar dependencias: `pip install -r requirements.txt`
- Ver logs en el screen: `screen -r <nombre>`

### Problema: Puerto ya en uso

**Solución**:
```bash
# Ver qué proceso usa el puerto
sudo lsof -i :5001
# O
sudo netstat -tulnp | grep 5001

# Detener el proceso
kill <PID>
```

### Problema: Servicio escucha solo en localhost

**Solución**:
- Modificar código para usar `0.0.0.0`:
```python
app.run(host='0.0.0.0', port=5001)  # ✅ Correcto
# No: app.run(host='127.0.0.1', port=5001)  # ❌ Incorrecto
```

### Problema: Firewall bloqueando

**Solución**:
- Verificar reglas de firewall existentes
- Crear reglas nuevas para permitir tu IP
- Verificar que las VMs tienen el tag `allow-external`

## 📝 Checklist Final

- [ ] Servicios corriendo en gpt-oss-20b (5000, 5002, 5003, 5010, 5678)
- [ ] Servicios corriendo en bounty2 (11434, 5001)
- [ ] Servicios corriendo en rag3 (8000)
- [ ] Servicios escuchando en 0.0.0.0 (no solo 127.0.0.1)
- [ ] Firewall configurado correctamente
- [ ] Conexiones internas entre VMs funcionando
- [ ] Frontend puede conectarse desde localhost
- [ ] Todos los endpoints responden correctamente

---

**Última actualización**: Noviembre 2025

