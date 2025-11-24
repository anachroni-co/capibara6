# 📋 Comandos Manuales para Verificar Servicios

## ⚠️ Importante

Los scripts automáticos pueden quedarse bloqueados. **Ejecuta estos comandos manualmente uno por uno** para ver la salida completa.

## 🔍 Verificación Paso a Paso

### Paso 1: Verificar Acceso Básico

```bash
# Verificar que puedes listar VMs
gcloud compute instances list --project=mamba-001
```

Si esto funciona, continúa. Si no, verifica tu autenticación:
```bash
gcloud auth list
gcloud config set project mamba-001
```

### Paso 2: Verificar bounty2

**Comando 1: Ver procesos Python**
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="ps aux | grep python | grep -v grep"
```

**Comando 2: Ver procesos Ollama**
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="ps aux | grep ollama | grep -v grep"
```

**Comando 3: Ver puertos abiertos**
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="sudo ss -tuln | grep -E ':(5001|11434)'"
```

**Comando 4: Probar Ollama**
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="curl -s http://localhost:11434/api/tags | head -5"
```

**Comando 5: Probar Backend**
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001 --command="curl -s http://localhost:5001/api/health"
```

### Paso 3: Verificar rag3

**Comando 1: Ver procesos**
```bash
gcloud compute ssh rag3 --zone=europe-west2-c --project=mamba-001 --command="ps aux | grep python | grep -v grep"
```

**Comando 2: Ver puertos**
```bash
gcloud compute ssh rag3 --zone=europe-west2-c --project=mamba-001 --command="sudo ss -tuln | grep 8000"
```

**Comando 3: Probar RAG API**
```bash
gcloud compute ssh rag3 --zone=europe-west2-c --project=mamba-001 --command="curl -s http://localhost:8000/health"
```

### Paso 4: Verificar gpt-oss-20b

**Comando 1: Ver procesos Python**
```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="ps aux | grep python | grep -v grep"
```

**Comando 2: Ver puertos**
```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="sudo ss -tuln | grep -E ':(500[0-9]|5010|5678)'"
```

**Comando 3: Probar servicios**
```bash
# Bridge (5000)
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="curl -s http://localhost:5000/api/health || echo 'Puerto 5000 no responde'"

# TTS (5002)
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="curl -s http://localhost:5002/health || echo 'Puerto 5002 no responde'"

# MCP (5003)
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="curl -s http://localhost:5003/health || echo 'Puerto 5003 no responde'"

# N8n (5678)
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001 --command="curl -s http://localhost:5678/healthz || echo 'Puerto 5678 no responde'"
```

## 🚀 Alternativa: Conectarse Interactivamente

Si los comandos remotos tardan mucho, conéctate directamente:

### bounty2
```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001

# Una vez dentro:
ps aux | grep python
ps aux | grep ollama
sudo ss -tuln | grep -E ':(5001|11434)'
curl http://localhost:11434/api/tags
curl http://localhost:5001/api/health
```

### rag3
```bash
gcloud compute ssh rag3 --zone=europe-west2-c --project=mamba-001

# Una vez dentro:
ps aux | grep python
sudo ss -tuln | grep 8000
curl http://localhost:8000/health
```

### gpt-oss-20b
```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001

# Una vez dentro:
ps aux | grep python
sudo ss -tuln | grep -E ':(500[0-9]|5010|5678)'
curl http://localhost:5000/api/health
curl http://localhost:5003/health
curl http://localhost:5678/healthz
```

## 📊 Resumen de Qué Buscar

### bounty2 debe tener:
- ✅ Proceso Ollama corriendo
- ✅ Puerto 11434 abierto
- ✅ Proceso Python (backend) corriendo
- ✅ Puerto 5001 abierto (o 5000)

### rag3 debe tener:
- ✅ Proceso Python (RAG API) corriendo
- ✅ Puerto 8000 abierto

### gpt-oss-20b debe tener:
- ✅ Proceso Python (Bridge) en puerto 5000
- ✅ Proceso Python (TTS) en puerto 5002
- ✅ Proceso Python (MCP) en puerto 5003 o 5010
- ✅ N8n en puerto 5678 (Docker o servicio)

## 🐛 Si los Comandos se Bloquean

1. **Presiona Ctrl+C** para cancelar
2. **Mata procesos bloqueados**:
```bash
pkill -f "gcloud.*ssh"
```
3. **Usa conexión interactiva** en lugar de comandos remotos

---

**Última actualización**: Noviembre 2025

