# ⚡ SOLO FALTA ESTO - 2 Pasos Simples

## ✅ Lo Que Ya Funciona

- ✅ **Chat** funcionando perfectamente
- ✅ **Gemma Model** generando respuestas
- ✅ **Audio/TTS** funcionando con Web Speech API
- ✅ **Servicios en VM** activos:
  - Smart MCP en puerto 5010 ✅
  - Coqui TTS en puerto 5002 ✅

---

## ⚠️ Lo Que Falta (Solo 2 Pasos)

```
❌ GET https://www.capibara6.com/api/mcp-health 503 (Service Unavailable)
```

El frontend **intenta** conectar pero **no puede** porque:

1. Firewall no abierto (puertos 5010 y 5002)
2. Variables no configuradas en Vercel

---

## 🔥 PASO 1: Abrir Firewall (2 comandos)

**Desde tu PC (PowerShell o CMD nueva terminal):**

```bash
gcloud compute firewall-rules create allow-smart-mcp-5010 --allow=tcp:5010 --source-ranges=0.0.0.0/0 --description="Smart MCP Server"
```

```bash
gcloud compute firewall-rules create allow-coqui-tts --allow=tcp:5002 --source-ranges=0.0.0.0/0 --description="Coqui TTS Server"
```

**Resultado esperado:**
```
Created [https://www.googleapis.com/.../allow-smart-mcp-5010]
Created [https://www.googleapis.com/.../allow-coqui-tts]
```

---

## 🌐 PASO 2: Configurar Variables en Vercel

### 2a. Ir a Vercel

https://vercel.com/anachroni

### 2b. Abrir tu proyecto

Click en **capibara6**

### 2c. Settings → Environment Variables

1. Click en **Settings** (pestaña arriba)
2. Click en **Environment Variables** (menú izquierda)
3. Click en **Add New**

### 2d. Agregar Primera Variable

```
Name:  SMART_MCP_URL
Value: http://34.175.104.187:5010/analyze
```

Marcar: ✅ Production ✅ Preview ✅ Development

Click **Save**

### 2e. Agregar Segunda Variable

Click en **Add New** de nuevo:

```
Name:  KYUTAI_TTS_URL
Value: http://34.175.104.187:5002/tts
```

Marcar: ✅ Production ✅ Preview ✅ Development

Click **Save**

### 2f. Re-deploy

1. Ve a **Deployments** (pestaña arriba)
2. Click en **...** del último deployment
3. Click en **Redeploy**

---

## 🎉 Resultado Después

Recarga el navegador (`Ctrl + Shift + R`) y verás:

### ANTES:
```javascript
ℹ️ Smart MCP no disponible (se usará modo directo)
⚠️ Coqui TTS no disponible, usando Web Speech API
```

### DESPUÉS:
```javascript
✅ Smart MCP activo: Selective RAG
🔊 Coqui TTS reproduciendo... (tts_models/es/css10/vits)
✅ Coqui TTS completado
```

---

## 📊 Checklist

- [ ] Ejecutar 2 comandos de firewall (desde PC)
- [ ] Configurar 2 variables en Vercel
- [ ] Re-deploy en Vercel
- [ ] Recargar navegador con Ctrl+Shift+R
- [ ] Probar botón "Escuchar" 🔊

---

## ✅ Todo lo Demás Ya Está Listo

- ✅ Código actualizado y pusheado
- ✅ Servicios corriendo en VM
- ✅ Frontend optimizado
- ✅ Proxies configurados
- ✅ Documentación completa (20+ archivos)

**Solo ejecuta esos 2 comandos de firewall y configura las 2 variables.** 🚀

---

**¡Estás a 5 minutos de tener el sistema completo funcionando!** 🎉

