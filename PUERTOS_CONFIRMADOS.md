# ✅ Puertos Confirmados y Activos

## 🔌 Configuración Final de Puertos

| Servicio | Puerto | Estado | IP Interna VM |
|----------|--------|--------|---------------|
| **Gemma Model** | 8080 | ✅ Activo | http://10.204.0.4:8080 |
| **Smart MCP** | **5010** | ✅ Activo | http://10.204.0.4:5010 |
| **Coqui TTS** | **5002** | ✅ Activo | http://10.204.0.4:5002 |

---

## ✅ Archivos Actualizados

### Frontend:
- ✅ `web/smart-mcp-integration.js` → Puerto 5010
- ✅ Smart MCP **HABILITADO** (antes estaba deshabilitado)
- ✅ `web/chat.html` → v=6.0 (cache bust)

### Backend Vercel:
- ✅ `api/mcp-analyze.js` → Puerto 5010
- ✅ `api/tts.js` → Puerto 5002

### Backend VM:
- ✅ `backend/coqui_tts_server.py` → Puerto 5002 ✅ Corriendo
- ✅ `backend/smart_mcp_server.py` → Puerto 5010 ✅ Corriendo

---

## 🌐 Variables de Entorno para Vercel

Configura estas 2 variables en Vercel Dashboard:

### 1. Smart MCP URL

```
Name:  SMART_MCP_URL
Value: http://TU_IP_PUBLICA:5010/analyze
```

### 2. TTS URL

```
Name:  KYUTAI_TTS_URL
Value: http://TU_IP_PUBLICA:5002/tts
```

**Obtener IP pública (en la VM):**

```bash
curl -s http://checkip.amazonaws.com
```

---

## 🔥 Firewall Necesario

Asegúrate de tener estas reglas (ejecutar desde tu PC):

```bash
# Puerto 5010 - Smart MCP
gcloud compute firewall-rules create allow-smart-mcp-5010 \
    --allow=tcp:5010 \
    --source-ranges=0.0.0.0/0 \
    --description="Smart MCP Server"

# Puerto 5002 - Coqui TTS
gcloud compute firewall-rules create allow-coqui-tts \
    --allow=tcp:5002 \
    --source-ranges=0.0.0.0/0 \
    --description="Coqui TTS Server"
```

---

## ✅ Verificación

### En la VM:

```bash
# Ver servicios activos
screen -ls

# Test cada servicio
curl http://localhost:5010/health  # Smart MCP
curl http://localhost:5002/health  # Coqui TTS

# Test de síntesis
curl -X POST http://localhost:5002/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola desde Coqui","language":"es"}'
```

### Desde tu PC:

```bash
# Obtener IP
VM_IP=$(gcloud compute instances describe gemma-3-12b --zone=europe-southwest1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

echo "IP de tu VM: $VM_IP"

# Test servicios
curl http://$VM_IP:5010/health
curl http://$VM_IP:5002/health
```

---

## 🎯 Resultado Esperado en el Frontend

Después de configurar las variables y recargar:

```javascript
✅ Smart MCP conectado      (en lugar de "no disponible")
🔊 Coqui TTS reproduciendo... (en lugar de Web Speech API)
✅ Coqui TTS completado
```

---

## 📊 Arquitectura Completa

```
Usuario (Navegador)
    ↓ HTTPS
Vercel
    ├─ /api/completion    → VM:8080 (Gemma)
    ├─ /api/mcp-analyze   → VM:5010 (Smart MCP) ✅
    └─ /api/tts           → VM:5002 (Coqui TTS) ✅
    ↓ HTTP
VM Google Cloud
    ├─ :8080 - Gemma Model  ✅
    ├─ :5010 - Smart MCP    ✅ Corriendo
    └─ :5002 - Coqui TTS    ✅ Corriendo
```

---

## 🎉 Todo Está Corriendo!

- ✅ Smart MCP: Puerto 5010 (activo)
- ✅ Coqui TTS: Puerto 5002 (activo)
- ✅ Frontend: Actualizado
- ✅ Proxies Vercel: Actualizados

**Solo falta:**
1. Configurar 2 variables de entorno en Vercel
2. Abrir puertos 5010 y 5002 en firewall
3. Recargar el navegador

---

**¡Servicios corriendo! Solo configurar las variables en Vercel ahora.** 🚀

