# 🔍 Resumen de Verificación con gcloud

## ✅ Scripts Creados

He creado varios scripts para verificar servicios usando gcloud:

1. **`verificar_servicios_gpt_oss.sh`** - Verifica servicios en gpt-oss-20b
2. **`check_services_remote.sh`** - Verifica servicios en todas las VMs
3. **`get_vm_info_complete.sh`** - Obtiene información completa de las VMs
4. **`test_gcloud_connection.sh`** - Prueba conexiones básicas

## 🚀 Comandos para Ejecutar Manualmente

### 1. Verificar Servicios en gpt-oss-20b

```bash
./verificar_servicios_gpt_oss.sh
```

O manualmente:

```bash
gcloud compute ssh gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --command="
    echo '📋 Procesos Python:'
    ps aux | grep python | grep -v grep
    echo ''
    echo '🔌 Puertos escuchando:'
    sudo ss -tuln | grep -E ':(500[0-9]|5010|5678)'
    echo ''
    echo '🧪 Probando servicios:'
    curl -s http://localhost:5000/health && echo '✅ Puerto 5000 OK' || echo '❌ Puerto 5000'
    curl -s http://localhost:5002/health && echo '✅ Puerto 5002 OK' || echo '❌ Puerto 5002'
    curl -s http://localhost:5003/health && echo '✅ Puerto 5003 OK' || echo '❌ Puerto 5003'
    curl -s http://localhost:5010/health && echo '✅ Puerto 5010 OK' || echo '❌ Puerto 5010'
    curl -s http://localhost:5678/healthz && echo '✅ Puerto 5678 OK' || echo '❌ Puerto 5678'
  "
```

### 2. Verificar Servicios en bounty2

```bash
gcloud compute ssh bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --command="
    echo '📋 Procesos Python:'
    ps aux | grep python | grep -v grep
    echo ''
    echo '📋 Procesos Ollama:'
    ps aux | grep ollama | grep -v grep
    echo ''
    echo '🔌 Puertos escuchando:'
    sudo ss -tuln | grep -E ':(500[01]|11434)'
    echo ''
    echo '🧪 Probando servicios:'
    curl -s http://localhost:11434/api/tags && echo '✅ Ollama OK' || echo '❌ Ollama'
    curl -s http://localhost:5001/api/health && echo '✅ Backend OK' || echo '❌ Backend'
  "
```

### 3. Verificar Servicios en rag3

```bash
gcloud compute ssh rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --command="
    echo '📋 Procesos Python:'
    ps aux | grep python | grep -v grep
    echo ''
    echo '🔌 Puertos escuchando:'
    sudo ss -tuln | grep 8000
    echo ''
    echo '🧪 Probando RAG API:'
    curl -s http://localhost:8000/health && echo '✅ RAG OK' || echo '❌ RAG'
  "
```

### 4. Obtener IPs de las VMs

```bash
# IP pública de bounty2
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# IP interna de bounty2
gcloud compute instances describe bounty2 \
  --zone=europe-west4-a \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# IP pública de gpt-oss-20b
gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# IP interna de gpt-oss-20b
gcloud compute instances describe gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"

# IP pública de rag3
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# IP interna de rag3
gcloud compute instances describe rag3 \
  --zone=europe-west2-c \
  --project=mamba-001 \
  --format="value(networkInterfaces[0].networkIP)"
```

### 5. Iniciar Servicios en gpt-oss-20b

```bash
gcloud compute ssh gpt-oss-20b \
  --zone=europe-southwest1-b \
  --project=mamba-001 \
  --command="
    cd ~/capibara6/backend || cd /ruta/a/tu/proyecto/backend
    chmod +x check_and_start_gpt_oss_20b.sh
    ./check_and_start_gpt_oss_20b.sh
  "
```

## 📋 Checklist de Verificación

Ejecuta estos comandos en orden:

1. ✅ **Verificar gpt-oss-20b**:
   ```bash
   ./verificar_servicios_gpt_oss.sh
   ```

2. ✅ **Si los servicios no están corriendo, iniciarlos**:
   ```bash
   gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001
   # Una vez dentro:
   cd ~/capibara6
   ./check_and_start_gpt_oss_20b.sh
   ```

3. ✅ **Verificar bounty2**:
   ```bash
   gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="ps aux | grep python; sudo ss -tuln | grep 5001"
   ```

4. ✅ **Verificar desde tu portátil**:
   ```bash
   ./verify_vm_connections_complete.sh
   ```

## 🐛 Si los Comandos No Muestran Salida

Si los comandos de gcloud no muestran salida, puede ser porque:

1. **La salida está siendo redirigida**: Prueba sin redirección:
   ```bash
   gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="hostname"
   ```

2. **Los comandos tardan mucho**: Usa timeout:
   ```bash
   timeout 60 gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="hostname"
   ```

3. **Problemas de autenticación**: Verifica:
   ```bash
   gcloud auth list
   gcloud config get-value project
   ```

## 💡 Recomendación

Ejecuta los comandos manualmente uno por uno para ver la salida completa y diagnosticar cualquier problema.

---

**Última actualización**: Noviembre 2025

