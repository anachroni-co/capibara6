# 🔄 Cambio de Puerto: 5001 → 5002

## ✅ Cambio Realizado

He cambiado todos los servicios TTS del puerto **5001** al puerto **5002** para evitar conflictos.

---

## 📦 Archivos Actualizados

| Archivo | Cambio |
|---------|--------|
| `backend/coqui_tts_server.py` | Puerto 5001 → 5002 |
| `backend/kyutai_tts_server_simple.py` | Puerto 5001 → 5002 |
| `backend/start_coqui_tts.sh` | Menciones de puerto |
| `backend/start_coqui_tts_py311.sh` | Puerto + auto-kill |
| `deploy_services_to_vm.sh` | Firewall + mensajes |
| `api/tts.js` | URL por defecto |

---

## 🚀 Para Ti (en la VM ahora)

### Opción A: Re-copiar archivos actualizados

**Desde tu PC (otra terminal):**

```bash
# Re-copiar servidores con puerto 5002
gcloud compute scp backend/coqui_tts_server.py gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b

gcloud compute scp backend/kyutai_tts_server_simple.py gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b

gcloud compute scp backend/start_coqui_tts_py311.sh gemma-3-12b:~/capibara6/backend/ --zone=europe-southwest1-b
```

**En la VM (donde estás):**

```bash
cd ~/capibara6/backend

# Dar permisos
chmod +x start_coqui_tts_py311.sh

# Iniciar Coqui TTS (puerto 5002, auto-mata proceso anterior)
screen -S coqui-tts
./start_coqui_tts_py311.sh
# Ctrl+A, D
```

### Opción B: Pull desde Git

```bash
cd ~/capibara6

# Pull últimos cambios
git pull

# Iniciar servicio
cd backend
screen -S coqui-tts
./start_coqui_tts_py311.sh
```

---

## 🔥 Crear Regla de Firewall (Puerto 5002)

**Desde tu PC:**

```bash
gcloud compute firewall-rules create allow-coqui-tts \
    --allow=tcp:5002 \
    --source-ranges=0.0.0.0/0 \
    --description="Coqui TTS Server"
```

**Verificar:**

```bash
gcloud compute firewall-rules list | grep 5002
```

---

## 📊 Puertos Actualizados

| Servicio | Puerto Anterior | Puerto Nuevo |
|----------|----------------|--------------|
| Gemma Model | 8080 | 8080 (sin cambio) |
| Smart MCP | 5003 | 5003 (sin cambio) |
| **Coqui TTS** | ~~5001~~ | **5002** ✨ |

---

## ✅ Verificar que Funciona

**En la VM:**

```bash
# Verificar TTS en nuevo puerto
curl http://localhost:5002/health

# Respuesta esperada:
{
  "service": "coqui-tts",
  "status": "healthy"
}

# Test de síntesis
curl -X POST http://localhost:5002/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola mundo","language":"es"}'
```

**Desde tu PC:**

```bash
VM_IP="TU_IP_AQUI"  # Reemplaza con tu IP

curl http://$VM_IP:5002/health
```

---

## 🌐 Actualizar Variable en Vercel

Ve a: https://vercel.com → Settings → Environment Variables

**Actualizar o crear:**

```
Name:  KYUTAI_TTS_URL
Value: http://TU_IP_VM:5002/tts  ← Nuevo puerto 5002
```

**IMPORTANTE:** Cambiar de `5001` a `5002`

---

## 🎯 Resultado Final

```
VM Google Cloud
├─ :8080 - Gemma Model  ✅
├─ :5003 - Smart MCP    ✅
└─ :5002 - Coqui TTS    ✨ Nuevo puerto
```

**Sin conflictos, puerto 5001 libre.** ✅

---

**Sigue los pasos de arriba para actualizar todo al puerto 5002.** 🚀

