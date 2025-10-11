# 🔌 Puertos Actuales - Capibara6

## ✅ Configuración Final de Puertos

| Servicio | Puerto | Estado | URL para Vercel |
|----------|--------|--------|-----------------|
| **Gemma Model** | 8080 | ✅ Activo | - |
| **Smart MCP** | **5010** | ✅ Activo | `http://IP_VM:5010/analyze` |
| **Coqui TTS** | **5002** | ⏳ Por iniciar | `http://IP_VM:5002/tts` |

---

## 🌐 Variables de Entorno en Vercel

Configurar estas 2 variables en Vercel:

### 1. Smart MCP URL

```
Name:  SMART_MCP_URL
Value: http://TU_IP_VM:5010/analyze
```

### 2. TTS URL

```
Name:  KYUTAI_TTS_URL
Value: http://TU_IP_VM:5002/tts
```

**Obtener tu IP:**

```bash
# En la VM
curl -s http://checkip.amazonaws.com

# O desde PC
gcloud compute instances describe gemma-3-12b --zone=europe-southwest1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
```

---

## 🔥 Firewall Necesario

Asegúrate de tener estas reglas:

```bash
# Desde tu PC, crear reglas de firewall
gcloud compute firewall-rules create allow-smart-mcp-5010 \
    --allow=tcp:5010 \
    --source-ranges=0.0.0.0/0 \
    --description="Smart MCP Server"

gcloud compute firewall-rules create allow-coqui-tts \
    --allow=tcp:5002 \
    --source-ranges=0.0.0.0/0 \
    --description="Coqui TTS Server"
```

---

## ✅ Verificar Servicios

**En la VM:**

```bash
# Smart MCP (puerto 5010)
curl http://localhost:5010/health

# Coqui TTS (puerto 5002)
curl http://localhost:5002/health
```

---

## 🎯 Estado Actual

```
✅ Smart MCP: ACTIVO en puerto 5010
⏳ Coqui TTS: Pendiente iniciar en puerto 5002
✅ Frontend: Funcional con Web Speech API
```

---

**Confirmo: TTS debe usar puerto 5002. ¿Ya iniciaste Coqui TTS en ese puerto?** 🎙️

