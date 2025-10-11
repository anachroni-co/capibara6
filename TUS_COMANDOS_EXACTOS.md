# ⚡ TUS COMANDOS EXACTOS - IP: 34.175.104.187

## 🔥 PASO 1: Abrir Firewall (Desde tu PC - Nueva Terminal)

Copia y pega exactamente esto:

```bash
gcloud compute firewall-rules create allow-coqui-tts --allow=tcp:5002 --source-ranges=0.0.0.0/0 --description="Coqui TTS Server puerto 5002"
```

```bash
gcloud compute firewall-rules create allow-smart-mcp-5010 --allow=tcp:5010 --source-ranges=0.0.0.0/0 --description="Smart MCP Server puerto 5010"
```

**Resultado esperado:**
```
Created [https://www.googleapis.com/compute/v1/.../allow-coqui-tts]
Created [https://www.googleapis.com/compute/v1/.../allow-smart-mcp-5010]
```

---

## 🌐 PASO 2: Configurar Variables en Vercel

### Ve a: https://vercel.com/anachroni

1. Click en tu proyecto **capibara6**
2. Click en **Settings** (pestaña superior)
3. Click en **Environment Variables** (menú izquierdo)

### Agregar Variable 1:

Click en **Add New**:

```
Name:  SMART_MCP_URL
Value: http://34.175.104.187:5010/analyze
```

Marcar: ✅ Production ✅ Preview ✅ Development

Click **Save**

### Agregar Variable 2:

Click en **Add New** de nuevo:

```
Name:  KYUTAI_TTS_URL
Value: http://34.175.104.187:5002/tts
```

Marcar: ✅ Production ✅ Preview ✅ Development

Click **Save**

---

## 🔄 PASO 3: Re-deploy en Vercel

1. Ve a **Deployments** (pestaña superior)
2. Click en **...** del deployment más reciente
3. Click en **Redeploy**
4. Confirmar

---

## ✅ PASO 4: Verificar (Desde tu PC)

```bash
# Test TTS directo
curl -X POST http://34.175.104.187:5002/tts -H "Content-Type: application/json" -d "{\"text\":\"Hola\",\"language\":\"es\"}"

# Test MCP directo
curl http://34.175.104.187:5010/health

# Test TTS vía Vercel (después de configurar variable)
curl -X POST https://capibara6-kpdtkkw9k-anachroni.vercel.app/api/tts -H "Content-Type: application/json" -d "{\"text\":\"Hola Vercel\",\"language\":\"es\"}"
```

---

## 🎯 PASO 5: Probar en el Navegador

1. Abre: https://capibara6-kpdtkkw9k-anachroni.vercel.app/chat.html
2. **Hard reload:** `Ctrl + Shift + R`
3. Envía un mensaje
4. Haz clic en **"Escuchar"** 🔊

**Esperado en consola:**

```javascript
✅ Smart MCP conectado          (no más "no disponible")
🔊 Coqui TTS reproduciendo... (no más "Web Speech API")
✅ Coqui TTS completado
```

---

## 📊 Resumen con TU IP

```
VARIABLES EN VERCEL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SMART_MCP_URL    = http://34.175.104.187:5010/analyze
KYUTAI_TTS_URL   = http://34.175.104.187:5002/tts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIREWALL NECESARIO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Puerto 5002: Coqui TTS
Puerto 5010: Smart MCP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**Ejecuta los comandos de firewall desde tu PC y configura las variables en Vercel con exactamente esas URLs.** 🚀

