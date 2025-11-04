# ✅ Verificación de Servicios - Checklist Completo

## 🔍 Comandos de Verificación

### En la VM (donde estás ahora):

```bash
# 1. Ver qué está corriendo en screen
screen -ls

# Deberías ver algo como:
# 5001.coqui-tts    o    5001.tts-fallback
# 5003.smart-mcp

# 2. Verificar TTS (puerto 5001)
curl http://localhost:5001/health

# Respuesta esperada:
# {"service": "coqui-tts", "status": "healthy", ...}
# o
# {"service": "tts-fallback-server", "status": "healthy", ...}

# 3. Verificar Smart MCP (puerto 5003)
curl http://localhost:5003/health

# Respuesta esperada:
# {"service": "capibara6-mcp", "status": "healthy", ...}

# 4. Test de síntesis TTS
curl -X POST http://localhost:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola, soy Capibara6","language":"es"}'

# Debería devolver JSON con audioContent en base64
```

---

## 🌐 Obtener IP de la VM

```bash
# Desde la VM, obtener IP pública
curl -s http://checkip.amazonaws.com

# O desde tu PC
gcloud compute instances describe gemma-3-12b \
  --zone=europe-southwest1-b \
  --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
```

**Anota esta IP**, la necesitarás para Vercel.

---

## 🔧 Configurar Vercel

### Paso 1: Ir a Vercel Dashboard

1. Ve a: https://vercel.com/anachroni
2. Selecciona el proyecto **capibara6**
3. Ve a **Settings** (pestaña superior)
4. Click en **Environment Variables** (menú lateral)

### Paso 2: Agregar Variable

Click en **Add New**:

- **Name:** `KYUTAI_TTS_URL`
- **Value:** `http://TU_IP_VM:5001/tts`  
  _(Reemplaza TU_IP_VM con la IP que obtuviste)_
- **Environment:** Marcar las 3 casillas:
  - ✅ Production
  - ✅ Preview
  - ✅ Development

Click en **Save**

### Paso 3: Re-deploy

1. Ve a **Deployments** (pestaña superior)
2. Click en los **...** del último deployment
3. Click en **Redeploy**
4. Confirmar

**O simplemente esperar:** Vercel re-deployará automáticamente en el próximo push a GitHub.

---

## 🧪 Testing End-to-End

### Desde tu PC:

```bash
# Obtener IP de VM
VM_IP=$(gcloud compute instances describe gemma-3-12b --zone=europe-southwest1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

echo "Tu VM IP: $VM_IP"

# 1. Test directo a TTS en VM
curl -X POST http://$VM_IP:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Prueba desde PC","language":"es"}'

# 2. Test directo a MCP en VM
curl http://$VM_IP:5003/health

# 3. Test Gemma Model
curl http://$VM_IP:8080/health

# 4. Test proxy Vercel (después de configurar variable)
curl -X POST https://capibara6-kpdtkkw9k-anachroni.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Prueba desde Vercel","language":"es"}'
```

---

## 🌐 Testing en el Navegador

1. Abre: https://capibara6-kpdtkkw9k-anachroni.vercel.app/chat.html
2. **Hard reload:** `Ctrl + Shift + R`
3. Envía un mensaje
4. Haz clic en **"Escuchar"** 🔊

### En la consola del navegador verás:

#### Si Coqui TTS está corriendo:
```
🎙️ Texto limpio para TTS (150 chars): "Hola..."
🔊 Coqui DSM TTS reproduciendo... (tts_models/es/css10/vits)
✅ Coqui TTS completado
```

#### Si usa fallback:
```
⚠️ Kyutai no disponible, usando Web Speech API
🎤 Usando voz: Microsoft Helena
🔊 Web Speech API iniciado
✅ Web Speech API completado
```

---

## 📊 Checklist de Servicios

### En la VM:

- [ ] Gemma Model corriendo (puerto 8080)
- [ ] Smart MCP corriendo (puerto 5003)  
- [ ] TTS corriendo (puerto 5001) - Coqui o Fallback
- [ ] Firewall abierto (puertos 8080, 5001, 5003)

### En Vercel:

- [ ] Deploy exitoso (sin errores)
- [ ] Variable `KYUTAI_TTS_URL` configurada
- [ ] Frontend cargando correctamente

### En el Navegador:

- [ ] Chat funciona
- [ ] Botón "Escuchar" aparece
- [ ] TTS reproduce audio

---

## 🐛 Si Algo No Funciona

### TTS no reproduce:

```bash
# Ver logs en la VM
screen -r coqui-tts
# o
screen -r tts-fallback
```

### Error de conexión desde Vercel:

```bash
# Verificar firewall
gcloud compute firewall-rules list | grep 5001

# Si no existe, crear
gcloud compute firewall-rules create allow-kyutai-tts \
    --allow=tcp:5001 \
    --source-ranges=0.0.0.0/0
```

### Smart MCP no responde:

```bash
# En la VM
screen -r smart-mcp

# Si no está corriendo
screen -S smart-mcp
cd ~/capibara6/backend
./start_smart_mcp.sh
```

---

## 🎯 Arquitectura Completa Activa

```
Usuario (Navegador)
    ↓ HTTPS
Vercel
    ├─ Frontend (HTML/JS/CSS)
    ├─ /api/completion    → VM:8080 (Gemma)
    ├─ /api/mcp-analyze   → VM:5003 (Smart MCP)
    └─ /api/tts           → VM:5001 (TTS)
    ↓ HTTP
VM Google Cloud (IP: TU_IP)
    ├─ :8080 - Gemma Model ✅
    ├─ :5003 - Smart MCP   ✅
    └─ :5001 - Coqui TTS   ✅
```

---

## 📝 Próximos Pasos

1. **Obtener IP de VM** y anotarla
2. **Configurar en Vercel:** Variable `KYUTAI_TTS_URL`
3. **Re-deploy** en Vercel (o esperar auto-deploy)
4. **Probar** el botón "Escuchar" en el chat

---

**¿Qué servicio TTS iniciaste? ¿Coqui o Fallback?** 🎙️

**¿Quieres que te ayude a configurar la variable en Vercel ahora?** 🚀

