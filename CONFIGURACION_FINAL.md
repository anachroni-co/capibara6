# 🎯 Configuración Final - Pasos Exactos

## ✅ Estado Actual

| Servicio | Puerto | Estado | Funciona |
|----------|--------|--------|----------|
| Gemma Model | 8080 | ✅ Activo | ✅ Sí |
| Smart MCP | **5010** | ✅ Activo | ⏳ Falta config |
| Coqui TTS | **5002** | ❌ Inactivo | ❌ Web Speech falla |

---

## 🔥 PASO 1: Abrir Firewall (Desde tu PC)

```bash
# Abrir puerto 5010 (Smart MCP)
gcloud compute firewall-rules create allow-smart-mcp-5010 --allow=tcp:5010 --source-ranges=0.0.0.0/0 --description="Smart MCP Server"

# Abrir puerto 5002 (Coqui TTS)
gcloud compute firewall-rules create allow-coqui-tts --allow=tcp:5002 --source-ranges=0.0.0.0/0 --description="Coqui TTS Server"
```

---

## 🚀 PASO 2: Iniciar Coqui TTS (En la VM)

```bash
cd ~/capibara6/backend
screen -S coqui-tts
./start_coqui_tts_py311.sh
# Espera 5-10 minutos la primera vez
# Ctrl+A, D para salir
```

---

## 🌐 PASO 3: Obtener IP de la VM (En la VM)

```bash
curl -s http://checkip.amazonaws.com
```

**Anota la IP** (ejemplo: `34.175.89.158`)

---

## 🌐 PASO 4: Configurar Variables en Vercel

Ve a: https://vercel.com → tu proyecto → Settings → Environment Variables

### Agregar 2 variables:

#### Variable 1: Smart MCP
```
Name:  SMART_MCP_URL
Value: http://TU_IP_VM:5010/analyze
```

#### Variable 2: TTS
```
Name:  KYUTAI_TTS_URL
Value: http://TU_IP_VM:5002/tts
```

**Environments:** Marcar Production, Preview, Development

**Guardar** y **Re-deploy** el proyecto

---

## ✅ PASO 5: Verificar Todo

**En la VM:**

```bash
# Ver servicios
screen -ls

# Test servicios
curl http://localhost:5010/health  # MCP
curl http://localhost:5002/health  # TTS
```

**En el navegador:**

1. Recarga la página: `Ctrl + Shift + R`
2. Envía un mensaje
3. Haz clic en "Escuchar" 🔊

**Esperado:**
```javascript
✅ Smart MCP conectado  (en lugar de "no disponible")
🔊 Coqui TTS reproduciendo... (en lugar de Web Speech API)
```

---

## 📊 Puertos Confirmados

```
VM Google Cloud
├─ :8080 - Gemma Model  ✅
├─ :5010 - Smart MCP    ✅ (corriendo ahora)
└─ :5002 - Coqui TTS    ⏳ (por iniciar)
```

---

**Sí, TTS es puerto 5002. Inicia Coqui TTS ahí y configura las variables en Vercel.** 🎙️

