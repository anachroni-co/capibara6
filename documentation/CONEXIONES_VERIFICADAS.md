# 🔍 Verificación de Conexiones Frontend - Capibara6

## Resultados de la Verificación

Fecha: $(date)

### ✅ Servicios Funcionando

| Servicio | VM | IP | Puerto | Estado |
|----------|----|----|--------|--------|
| **Ollama API** | Bounty2 | 34.12.166.76 | 11434 | ✅ OK (HTTP 200) |

### ⚠️ Servicios con Advertencias

| Servicio | VM | IP | Puerto | Estado | Nota |
|----------|----|----|--------|--------|------|
| **TTS** | gpt-oss-20b | 34.175.136.104 | 5002 | ⚠️ WARNING | Servicio responde pero endpoint `/api/tts/voices` retorna 404. Puede que el endpoint sea diferente. |

### ❌ Servicios No Accesibles

| Servicio | VM | IP | Puerto | Estado | Posible Causa |
|----------|----|----|--------|--------|---------------|
| **Backend Flask** | Bounty2 | 34.12.166.76 | 5001 | ❌ ERROR | Servicio no responde. Verificar si está corriendo. |
| **MCP Server** | gpt-oss-20b | 34.175.136.104 | 5003 | ❌ ERROR | Servicio no responde. Verificar si está corriendo. |
| **MCP Server Alt** | gpt-oss-20b | 34.175.136.104 | 5010 | ❌ ERROR | Servicio no responde. Verificar si está corriendo. |
| **N8n** | gpt-oss-20b | 34.175.136.104 | 5678 | ❌ ERROR | Servicio no responde. Verificar si está corriendo. |
| **Bridge** | gpt-oss-20b | 34.175.136.104 | 5000 | ❌ ERROR | Servicio no responde. Verificar si está corriendo. |

## 🔧 Acciones Recomendadas

### 1. Verificar Servicios en Bounty2

Conecta a Bounty2 y verifica qué servicios están corriendo:

```bash
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
bash scripts/check_services_on_vm.sh
```

**Verificar específicamente:**
- ¿Está corriendo el backend Flask en puerto 5001?
- ¿Qué puertos están escuchando?

```bash
sudo netstat -tuln | grep LISTEN
# o
sudo ss -tuln | grep LISTEN
```

### 2. Verificar Servicios en gpt-oss-20b

Conecta a gpt-oss-20b y verifica qué servicios están corriendo:

```bash
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
bash scripts/check_services_on_vm.sh
```

**Verificar específicamente:**
- ¿Están corriendo los servicios MCP, TTS, N8n y Bridge?
- ¿En qué puertos están escuchando?

### 3. Verificar Firewall Rules

Asegúrate de que las reglas de firewall permiten el acceso:

```bash
# Listar reglas de firewall
gcloud compute firewall-rules list --project=mamba-001

# Ver detalles de una regla específica
gcloud compute firewall-rules describe NOMBRE_REGLA --project=mamba-001
```

**Verificar que existe una regla que permita:**
- Puerto 5001 desde tu IP (para Backend Flask)
- Puertos 5000, 5002, 5003, 5010, 5678 desde tu IP (para servicios en gpt-oss-20b)

### 4. Verificar que los Servicios Escuchan en 0.0.0.0

Los servicios deben escuchar en `0.0.0.0` y no solo en `127.0.0.1` para ser accesibles desde fuera de la VM.

**En cada VM, verifica:**
```bash
# Ver qué está escuchando en cada puerto
sudo lsof -i :5001  # Backend Flask
sudo lsof -i :5003  # MCP
sudo lsof -i :5002  # TTS
sudo lsof -i :5678  # N8n
sudo lsof -i :5000  # Bridge
```

Si muestra `127.0.0.1` o `localhost`, el servicio solo acepta conexiones locales.

### 5. Iniciar Servicios si No Están Corriendo

Si los servicios no están corriendo, inícialos:

**En Bounty2:**
```bash
# Backend Flask (ajustar según tu configuración)
cd /ruta/al/backend
python3 capibara6_integrated_server.py &
# o
python3 server.py &
```

**En gpt-oss-20b:**
```bash
# MCP Server
cd /ruta/al/backend
python3 smart_mcp_server.py &
# o
python3 mcp_server.py &

# TTS (si está separado)
python3 kyutai_tts_server.py &

# N8n (si está en Docker)
docker-compose up -d n8n
# o si está como servicio
sudo systemctl start n8n
```

## 📊 Estadísticas

- **Total de servicios probados**: 7
- **Servicios funcionando**: 1 (14%)
- **Servicios con advertencias**: 1 (14%)
- **Servicios no accesibles**: 5 (72%)

## 🎯 Próximos Pasos

1. ✅ Ollama está funcionando correctamente
2. ⚠️ Verificar endpoint correcto de TTS (puede ser `/api/voices` o similar)
3. ❌ Iniciar Backend Flask en Bounty2 (puerto 5001)
4. ❌ Iniciar servicios en gpt-oss-20b (MCP, N8n, Bridge)
5. ❌ Verificar firewall rules para permitir acceso desde tu IP

## 📝 Notas

- Las IPs probadas son las configuradas en `web/config.js`
- Los timeouts son de 5 segundos
- Se usa HTTP (no HTTPS) para las pruebas
- Los servicios deben estar escuchando en `0.0.0.0` para ser accesibles desde fuera

---

**Para ejecutar la verificación nuevamente:**
```bash
bash scripts/verify_all_services.sh
```

