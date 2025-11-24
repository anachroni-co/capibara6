# 🔄 Instrucciones para Verificar y Reiniciar Servicios

## 🎯 Problema Actual

El frontend está intentando conectarse a `http://34.12.166.76:5001/api/health` pero recibe `ERR_CONNECTION_REFUSED`. Esto significa que el Backend Flask en Bounty2 no está corriendo o no está accesible.

## 📋 Pasos para Resolver

### 1. Verificar y Reiniciar Servicios en rag3

Conecta a rag3 y ejecuta el script de verificación:

```bash
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
cd /ruta/al/repositorio  # Ajusta la ruta según donde esté el código
bash scripts/check_and_restart_rag3.sh
```

Este script:
- ✅ Verifica si el RAG API está corriendo en puerto 8000
- ✅ Verifica PostgreSQL y Redis
- ✅ Reinicia el RAG API si no está activo
- ✅ Muestra el estado final de todos los servicios

**Si el script no encuentra el servicio RAG, busca manualmente:**

```bash
# Buscar archivos relacionados con RAG
find . -name "*rag*server*.py" -o -name "*rag*api*.py"

# Iniciar manualmente si encuentras el archivo
screen -S rag-api
python3 [ARCHIVO_ENCONTRADO]
# Ctrl+A, D para salir de screen
```

### 2. Verificar y Reiniciar Servicios en Bounty2 (CRÍTICO)

El Backend Flask en puerto 5001 debe estar corriendo. Conecta a Bounty2:

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
cd /ruta/al/repositorio  # Ajusta la ruta según donde esté el código
bash scripts/check_and_restart_bounty2.sh
```

Este script:
- ✅ Verifica Ollama en puerto 11434
- ✅ Verifica Backend Flask en puerto 5001 (CRÍTICO)
- ✅ Reinicia ambos servicios si no están activos
- ✅ Asegura que escuchan en `0.0.0.0` (no solo `127.0.0.1`)

**Verificación manual rápida:**

```bash
# Ver qué está escuchando en puerto 5001
sudo lsof -i :5001
# o
sudo netstat -tuln | grep 5001

# Si no hay nada, iniciar backend
cd backend
screen -S backend
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5001
python3 capibara6_integrated_server.py
# o
python3 server.py
# Ctrl+A, D para salir
```

**Asegúrate de que el backend escucha en 0.0.0.0:**

El backend debe estar configurado para escuchar en `0.0.0.0:5001` y no solo en `127.0.0.1:5001`. Verifica en el código del servidor:

```python
# Debe ser así:
app.run(host='0.0.0.0', port=5001)

# NO así:
app.run(host='127.0.0.1', port=5001)
```

### 3. Verificar Servicios en gpt-oss-20b

Conecta a gpt-oss-20b y verifica servicios:

```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
cd /ruta/al/repositorio
bash scripts/check_services_on_vm.sh
```

Verifica específicamente:
- TTS (puerto 5002)
- MCP Server (puerto 5003)
- N8n (puerto 5678)
- Bridge (puerto 5000)

### 4. Probar Conexiones Entre VMs

Desde cualquier VM o desde tu portátil, ejecuta:

```bash
bash scripts/test_vm_connections.sh
```

Este script prueba:
- ✅ Conexiones locales en cada VM
- ✅ Conexiones entre VMs (usando IPs internas si está en una VM)
- ✅ Conexiones desde fuera (usando IPs externas)

## 🔍 Verificación Rápida desde tu Portátil

Prueba directamente desde tu portátil:

```bash
# Ollama (debería funcionar)
curl http://34.12.166.76:11434/api/tags

# Backend Flask (el que está fallando)
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

## 🐛 Troubleshooting Específico

### Problema: Backend Flask no responde (puerto 5001)

**Causas posibles:**
1. El servicio no está corriendo
2. El servicio está escuchando solo en `127.0.0.1` en lugar de `0.0.0.0`
3. El puerto está bloqueado por firewall (ya configurado)
4. Hay un error en el código que impide que inicie

**Solución paso a paso:**

```bash
# 1. Conectar a Bounty2
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# 2. Verificar si hay algo en puerto 5001
sudo lsof -i :5001

# 3. Si hay algo, matarlo
sudo kill -9 [PID]

# 4. Ir al directorio del backend
cd /ruta/al/backend

# 5. Verificar que el código escucha en 0.0.0.0
grep -n "app.run\|host=" *.py | grep -v "127.0.0.1"

# 6. Iniciar el backend en screen
screen -S backend
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5001
python3 capibara6_integrated_server.py
# O el archivo que corresponda según tu configuración

# 7. Salir de screen (Ctrl+A, luego D)

# 8. Verificar que está corriendo
curl http://localhost:5001/api/health

# 9. Verificar desde fuera (desde tu portátil)
curl http://34.12.166.76:5001/api/health
```

### Problema: RAG API no responde (puerto 8000)

```bash
# En rag3
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
bash scripts/check_and_restart_rag3.sh

# O manualmente
screen -S rag-api
python3 [ARCHIVO_RAG_SERVER]
# Ctrl+A, D
```

## 📊 Scripts Disponibles

| Script | Descripción | Dónde ejecutar |
|--------|-------------|----------------|
| `scripts/check_and_restart_rag3.sh` | Verifica y reinicia servicios en rag3 | Dentro de rag3 |
| `scripts/check_and_restart_bounty2.sh` | Verifica y reinicia servicios en Bounty2 | Dentro de Bounty2 |
| `scripts/check_services_on_vm.sh` | Verifica servicios en cualquier VM | Dentro de cualquier VM |
| `scripts/test_vm_connections.sh` | Prueba conexiones entre VMs | Cualquier lugar |

## ✅ Checklist de Verificación

- [ ] rag3: RAG API corriendo en puerto 8000
- [ ] Bounty2: Ollama corriendo en puerto 11434
- [ ] Bounty2: Backend Flask corriendo en puerto 5001 (CRÍTICO)
- [ ] gpt-oss-20b: TTS corriendo en puerto 5002
- [ ] gpt-oss-20b: MCP corriendo en puerto 5003
- [ ] gpt-oss-20b: N8n corriendo en puerto 5678
- [ ] gpt-oss-20b: Bridge corriendo en puerto 5000
- [ ] Todos los servicios escuchan en `0.0.0.0` (no solo `127.0.0.1`)
- [ ] Firewall configurado correctamente
- [ ] Conexiones probadas entre VMs

## 🎯 Próximos Pasos Después de Reiniciar

1. Ejecutar `bash scripts/test_vm_connections.sh` para verificar todas las conexiones
2. Probar el frontend nuevamente desde `http://localhost:8000`
3. Verificar los logs si hay errores:
   ```bash
   # En cada VM
   tail -f /tmp/backend.log
   tail -f /tmp/rag_api.log
   ```

---

**Nota importante**: Asegúrate de que todos los servicios están configurados para escuchar en `0.0.0.0` y no solo en `127.0.0.1` para que sean accesibles desde fuera de la VM.

