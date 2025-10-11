# ⚡ Comandos para Ejecutar AHORA

## 🎯 Problema Actual

El frontend intenta usar Coqui TTS pero falla → Hace fallback a Web Speech API.

**Causa:** Falta configuración en Vercel y firewall.

---

## 📋 PASO 1: Obtener IP de tu VM (En la VM)

```bash
curl -s http://checkip.amazonaws.com
```

**Anota la IP** (ejemplo: `34.175.89.158`)

---

## 🔥 PASO 2: Abrir Firewall (Desde tu PC)

Abre **otra terminal en tu PC** y ejecuta:

```bash
# Puerto 5002 - Coqui TTS
gcloud compute firewall-rules create allow-coqui-tts --allow=tcp:5002 --source-ranges=0.0.0.0/0 --description="Coqui TTS Server puerto 5002"

# Puerto 5010 - Smart MCP
gcloud compute firewall-rules create allow-smart-mcp-5010 --allow=tcp:5010 --source-ranges=0.0.0.0/0 --description="Smart MCP Server puerto 5010"
```

---

## 🌐 PASO 3: Configurar Variables en Vercel

### 3a. Ir a Vercel

https://vercel.com/anachroni (o tu cuenta)

### 3b. Seleccionar Proyecto

Click en **capibara6**

### 3c. Settings → Environment Variables

1. Click en **Settings** (pestaña arriba)
2. Click en **Environment Variables** (menú izquierda)

### 3d. Agregar Primera Variable

Click en **Add New**:

```
Name:  SMART_MCP_URL
Value: http://TU_IP_VM:5010/analyze
```

Ejemplo: `http://34.175.89.158:5010/analyze`

Marcar: ✅ Production, ✅ Preview, ✅ Development

Click **Save**

### 3e. Agregar Segunda Variable

Click en **Add New** de nuevo:

```
Name:  KYUTAI_TTS_URL
Value: http://TU_IP_VM:5002/tts
```

Ejemplo: `http://34.175.89.158:5002/tts`

Marcar: ✅ Production, ✅ Preview, ✅ Development

Click **Save**

---

## 🔄 PASO 4: Re-deploy en Vercel

Opción A (Automático):
- Vercel re-deployará en el próximo push a GitHub

Opción B (Manual):
1. Ve a **Deployments** (pestaña arriba)
2. Click en **...** del deployment más reciente
3. Click en **Redeploy**
4. Confirmar

---

## ✅ PASO 5: Probar

### 5a. Recarga el navegador

```
Ctrl + Shift + R  (hard reload)
```

### 5b. Envía un mensaje

### 5c. Haz clic en "Escuchar" 🔊

**Esperado:**

```javascript
🔊 Coqui TTS reproduciendo... (tts_models/es/css10/vits)
✅ Coqui TTS completado
```

---

## 🔍 Verificación Desde PC

```bash
# Reemplaza con tu IP
VM_IP="34.175.89.158"

# Test directo a servicios
curl http://$VM_IP:5010/health  # Smart MCP
curl http://$VM_IP:5002/health  # Coqui TTS

# Test TTS completo
curl -X POST http://$VM_IP:5002/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Prueba Coqui","language":"es"}'
```

---

## 📊 Resumen

| Acción | ¿Hecho? |
|--------|---------|
| Servicios corriendo en VM | ✅ Sí |
| Firewall abierto | ⏳ Ejecutar comandos |
| Variables en Vercel | ⏳ Configurar |
| Re-deploy Vercel | ⏳ Después de variables |
| Probar en navegador | ⏳ Después de re-deploy |

---

**Ejecuta los comandos en orden y tendrás Coqui TTS funcionando.** 🎙️✨

