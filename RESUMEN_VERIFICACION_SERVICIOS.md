# 📋 Resumen de Verificación de Servicios

## ✅ Scripts Creados

He creado scripts para verificar servicios en cada VM:

1. **`verificar_servicios_bounty2.sh`** - Verifica servicios en bounty2
2. **`verificar_servicios_rag3.sh`** - Verifica servicios en rag3  
3. **`verificar_servicios_gpt_oss.sh`** - Verifica servicios en gpt-oss-20b
4. **`verificar_todos_los_servicios.sh`** - Verifica todas las VMs en un solo comando

## 🚀 Ejecutar Verificación

### Opción 1: Verificar Todas las VMs (Recomendado)

```bash
./verificar_todos_los_servicios.sh
```

Este script verificará:
- ✅ Procesos activos (Python, Ollama, Node)
- ✅ Puertos escuchando
- ✅ Servicios HTTP respondiendo
- ✅ IPs de cada VM

### Opción 2: Verificar Individualmente

```bash
# Verificar bounty2
./verificar_servicios_bounty2.sh

# Verificar rag3
./verificar_servicios_rag3.sh

# Verificar gpt-oss-20b
./verificar_servicios_gpt_oss.sh
```

## 📊 Qué Verifica Cada Script

### bounty2 (europe-west4-a)
- ✅ Procesos Python (backend)
- ✅ Procesos Ollama (modelos)
- ✅ Puerto 11434 (Ollama API)
- ✅ Puerto 5001 (Backend Flask)
- ✅ Puerto 5000 (Backend alternativo)
- ✅ Puerto 8000 (HTTP simple)

### rag3 (europe-west2-c)
- ✅ Procesos Python (RAG API)
- ✅ Puerto 8000 (RAG API)
- ✅ Puerto 5432 (PostgreSQL si aplica)
- ✅ Puerto 6379 (Redis si aplica)
- ✅ Servicios Docker (si aplica)

### gpt-oss-20b (europe-southwest1-b)
- ✅ Procesos Python (servicios)
- ✅ Puerto 5000 (Bridge/Main Server)
- ✅ Puerto 5002 (TTS Server)
- ✅ Puerto 5003 (MCP Server)
- ✅ Puerto 5010 (MCP Server alternativo)
- ✅ Puerto 5678 (N8n)

## 🔧 Si los Servicios No Están Corriendo

### En bounty2:

```bash
gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001

# Una vez dentro:
cd ~/capibara6/backend
screen -dmS backend python3 capibara6_integrated_server.py
# O
screen -dmS backend python3 server.py
```

### En rag3:

```bash
gcloud compute ssh rag3 --zone=europe-west2-c --project=mamba-001

# Una vez dentro, iniciar RAG API según tu configuración
```

### En gpt-oss-20b:

```bash
gcloud compute ssh gpt-oss-20b --zone=europe-southwest1-b --project=mamba-001

# Una vez dentro:
cd ~/capibara6
./check_and_start_gpt_oss_20b.sh
```

## 📝 Notas

- Los scripts pueden tardar varios segundos en ejecutarse (conexión SSH)
- Si un servicio no responde, verifica que esté escuchando en `0.0.0.0` y no solo en `127.0.0.1`
- Los scripts muestran tanto puertos abiertos como servicios HTTP respondiendo

## 🆘 Troubleshooting

Si los scripts no muestran salida:
1. Ejecuta manualmente los comandos gcloud uno por uno
2. Verifica tu autenticación: `gcloud auth list`
3. Verifica el proyecto: `gcloud config get-value project`
4. Prueba conectarte manualmente: `gcloud compute ssh bounty2 --zone=europe-west4-a --project=mamba-001`

---

**Última actualización**: Noviembre 2025

