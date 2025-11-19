# 🏗️ Arquitectura Capibara6 - Referencia Rápida

## 📍 VMs de Google Cloud

### VM 1: bounty2 (Modelos) - europe-west4-a
**IP**: 34.12.166.76

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **Ollama** | 11434 | Servidor de modelos LLM |
| **Backend Flask** | 5001 | API de chat (server_gptoss.py) |

**Conectar**: `./ssh-bounty2.sh`

**Modelos disponibles en Ollama**:
- gpt-oss:20b (20.9B parámetros) ← Principal
- mistral
- phi3

---

### VM 2: gpt-oss-20b (Servicios) - europe-southwest1-b
**IP**: 34.175.136.104

| Servicio | Puerto | Archivo | Descripción |
|----------|--------|---------|-------------|
| **TTS** | 5002 | coqui_tts_server.py | Text-to-Speech (Coqui) |
| **MCP** | 5003 | mcp_server.py | Model Context Protocol |
| **N8N** | 5678 | (Node.js) | Automatización de workflows |

**Conectar**: `./ssh-services.sh`

---

## 🔧 Frontend (Local o VM)

| Archivo | URL | Descripción |
|---------|-----|-------------|
| chat.html | http://localhost:8000/chat.html | Chat principal |
| index.html | http://localhost:8000/ | Landing page |

**Iniciar frontend local**:
```bash
cd web
python3 -m http.server 8000
```

---

## 🔄 Flujo de Datos

```
[Frontend] → [Backend Flask:5001] → [Ollama:11434] → [Modelo gpt-oss:20b]
    ↓
[Servicios Opcionales]
    ├─ TTS:5002 (texto a voz)
    ├─ MCP:5003 (contexto)
    └─ N8N:5678 (automatización)
```

---

## 🚀 Inicio Rápido

### En VM bounty2 (Modelos):

```bash
# 1. Verificar Ollama
curl http://localhost:11434/api/tags

# 2. Iniciar backend
cd ~/capibara6/backend
python3 server_gptoss.py
```

### En VM gpt-oss-20b (Servicios):

```bash
# 1. Iniciar TTS
cd ~/capibara6/backend
./start_coqui_tts.sh

# 2. Iniciar MCP
python3 mcp_server.py

# 3. Iniciar N8N (si está instalado)
n8n start
```

### En máquina local:

```bash
# Iniciar frontend
cd web
python3 -m http.server 8000

# Abrir: http://localhost:8000/chat.html
```

---

## 🧪 Verificación de Servicios

### VM bounty2:
```bash
curl http://34.12.166.76:11434/api/tags    # Ollama
curl http://34.12.166.76:5001/api/health   # Backend
```

### VM gpt-oss-20b:
```bash
curl http://34.175.136.104:5002/health  # TTS
curl http://34.175.136.104:5003/health  # MCP
curl http://34.175.136.104:5678         # N8N
```

---

## 📦 Configuración (.env)

### Backend (.env en bounty2):
```env
PORT=5001
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:20b
OLLAMA_TIMEOUT=120

SERVICES_VM_URL=http://34.175.136.104
TTS_URL=http://34.175.136.104:5002
MCP_URL=http://34.175.136.104:5003
N8N_URL=http://34.175.136.104:5678
```

### Frontend (config.js):
```javascript
const VM_MODELS = 'http://34.12.166.76';
const VM_SERVICES = 'http://34.175.136.104';

BACKEND_URL: 'http://34.12.166.76:5001'  // o localhost:5001 local
```

---

## 🔥 Puertos que deben estar abiertos

### VM bounty2:
- 11434 (Ollama)
- 5001 (Backend)

### VM gpt-oss-20b:
- 5002 (TTS)
- 5003 (MCP)
- 5678 (N8N)

### Verificar firewall:
```bash
# Google Cloud
gcloud compute firewall-rules list --project="mamba-001"

# Local (en cada VM)
sudo ufw status
```

---

## 📝 Archivos Clave

### Backend:
- `backend/server_gptoss.py` - Servidor principal de chat
- `backend/.env` - Configuración
- `backend/coqui_tts_server.py` - TTS
- `backend/mcp_server.py` - MCP

### Frontend:
- `web/chat.html` - UI del chat
- `web/chat-app.js` - Lógica del chat
- `web/config.js` - Configuración de URLs

### Scripts:
- `ssh-bounty2.sh` - SSH a VM de modelos
- `ssh-services.sh` - SSH a VM de servicios
- `backend/start_coqui_tts.sh` - Iniciar TTS
- `backend/start_smart_mcp.sh` - Iniciar MCP alternativo

---

## 🆘 Troubleshooting

### Backend no conecta a Ollama:
```bash
# Verificar que Ollama esté en 0.0.0.0:11434 (no solo 127.0.0.1)
sudo systemctl status ollama
netstat -tulpn | grep 11434
```

### Frontend devuelve vacío:
- Verificar que backend esté corriendo en puerto 5001
- Ver logs: `tail -f backend.log` en bounty2
- Verificar CORS en server_gptoss.py

### Servicios no responden:
```bash
# Ver procesos
ps aux | grep -E "coqui|mcp|n8n"

# Ver puertos
netstat -tulpn | grep -E "5002|5003|5678"

# Revisar logs en screens
screen -ls
screen -r tts
```

---

**Última actualización**: 2025-11-10
**Proyecto**: Capibara6 v2.0
**Contacto**: marco@anachroni.co
