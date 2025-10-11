# 🎯 Comandos Finales - Activar Todo el Sistema

## ✅ Ya Instalaste Todo en la VM

Ahora solo quedan 3 pasos para activar todo:

---

## 📋 Paso 1: Obtener IP de tu VM

**En la VM (donde estás):**

```bash
curl -s http://checkip.amazonaws.com
```

**O desde tu PC:**

```bash
gcloud compute instances describe gemma-3-12b --zone=europe-southwest1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
```

**Anota esta IP** (ejemplo: `34.175.89.158`)

---

## 🔍 Paso 2: Verificar Servicios

**En la VM:**

```bash
# Ver sesiones de screen activas
screen -ls

# Verificar cada servicio
curl http://localhost:5001/health  # TTS
curl http://localhost:5003/health  # MCP
curl http://localhost:8080/health  # Gemma (si está corriendo)

# Test de TTS completo
curl -X POST http://localhost:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola soy Capibara6","language":"es"}'

# Debería devolver JSON con audioContent
```

**Resultados esperados:**

```json
// TTS Health
{
  "service": "coqui-tts",  // o "tts-fallback-server"
  "status": "healthy"
}

// MCP Health
{
  "service": "capibara6-mcp",
  "status": "healthy",
  "contexts_available": 3
}
```

---

## 🌐 Paso 3: Configurar Vercel

### 3a. Ir a Vercel Dashboard

https://vercel.com/anachroni (o tu cuenta)

### 3b. Abrir Proyecto

Click en **capibara6**

### 3c. Settings → Environment Variables

1. Click en **Settings** (pestaña superior)
2. Click en **Environment Variables** (menú izquierdo)
3. Click en **Add New**

### 3d. Agregar Variable

```
Name:  KYUTAI_TTS_URL
Value: http://TU_IP_VM:5001/tts
```

**Ejemplo:** `http://34.175.89.158:5001/tts`

**Environments:** Marcar las 3:
- ✅ Production
- ✅ Preview  
- ✅ Development

Click en **Save**

### 3e. Re-deploy

Opción A (Automático):
- Vercel re-deployará solo en el próximo git push

Opción B (Manual):
1. Ve a **Deployments**
2. Click en **...** del último deployment
3. Click en **Redeploy**

---

## 🧪 Paso 4: Testing Final

### Desde tu PC:

```bash
# Reemplaza VM_IP con tu IP
VM_IP="34.175.89.158"  # Tu IP aquí

# Test 1: TTS directo a VM
curl -X POST http://$VM_IP:5001/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Prueba directa","language":"es"}' | jq

# Test 2: TTS a través de Vercel (después de configurar variable)
curl -X POST https://capibara6-kpdtkkw9k-anachroni.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Prueba Vercel","language":"es"}' | jq

# Test 3: MCP
curl http://$VM_IP:5003/health | jq
```

### En el Navegador:

1. **Abrir:** https://capibara6-kpdtkkw9k-anachroni.vercel.app/chat.html
2. **Hard reload:** `Ctrl + Shift + R`
3. **Enviar mensaje:** "Hola, ¿cómo estás?"
4. **Click en "Escuchar"** 🔊

**Esperado en consola:**

```javascript
🔊 Coqui DSM TTS reproduciendo... (tts_models/es/css10/vits)
✅ Coqui TTS completado
```

---

## 📊 Servicios Activos

Deberías tener corriendo:

| Servicio | Puerto | Comando para verificar |
|----------|--------|------------------------|
| **Gemma Model** | 8080 | `curl localhost:8080/health` |
| **Smart MCP** | 5003 | `curl localhost:5003/health` |
| **Coqui TTS** | 5001 | `curl localhost:5001/health` |

Ver sesiones: `screen -ls`

---

## 🔄 Reconectar a Servicios

```bash
# Ver logs de TTS
screen -r coqui-tts

# Ver logs de MCP
screen -r smart-mcp

# Salir sin cerrar: Ctrl+A, luego D
```

---

## 🎉 Si Todo Funciona

Verás en el chat:

1. ✅ Mensajes generados por Gemma
2. ✅ Contexto verificado por Smart MCP  
3. ✅ Audio sintetizado por Coqui TTS
4. ✅ Todo servido via HTTPS desde Vercel

---

## 🐛 Si Algo Falla

### TTS no responde:

```bash
# Ver logs
screen -r coqui-tts

# Reiniciar
screen -S coqui-tts -X quit
screen -S coqui-tts
./start_coqui_tts_py311.sh
```

### MCP no responde:

```bash
screen -r smart-mcp

# Reiniciar
screen -S smart-mcp -X quit
screen -S smart-mcp
./start_smart_mcp.sh
```

---

## 📝 Comandos Rápidos de Referencia

```bash
# Ver servicios
screen -ls

# Ver logs de un servicio
screen -r NOMBRE

# Salir de screen (sin cerrar)
Ctrl+A, luego D

# Matar una sesión
screen -S NOMBRE -X quit

# Ver puertos en uso
sudo lsof -i -P -n | grep LISTEN
```

---

**¡Todo debería estar funcionando! Ejecuta los comandos de verificación arriba.** ✅🚀

