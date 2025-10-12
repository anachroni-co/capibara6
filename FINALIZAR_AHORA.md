# ⚡ Finalizar Sistema en 3 Pasos (15 minutos)

## 🎯 Objetivo

Activar Smart MCP y actualizar Coqui TTS a XTTS v2 para tener el sistema 100% operacional.

---

## ✅ Paso 1: Verificar y Activar Smart MCP (5 min)

### 1.1. Conectar a la VM

```bash
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

### 1.2. Ejecutar Script de Diagnóstico

```bash
cd ~/capibara6/backend
chmod +x verificar_servicios.sh
./verificar_servicios.sh
```

### 1.3. Ver Resultado

**Si Smart MCP está ✓ ACTIVO:**
```
✓ Smart MCP (puerto 5010)... ACTIVO
```
→ **¡Perfecto! Pasa al Paso 2.**

**Si Smart MCP está ✗ NO RESPONDE:**
```bash
# Iniciar Smart MCP
screen -S smart-mcp
cd ~/capibara6/backend
./start_smart_mcp.sh
```

Espera a ver:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5010
```

Presiona: **Ctrl+A, luego D** (para salir del screen)

### 1.4. Verificar que Funciona

```bash
curl http://localhost:5010/health
```

**Debe responder:**
```json
{"status":"healthy","service":"mcp","port":5010}
```

✅ **Smart MCP activado!**

---

## ✅ Paso 2: Actualizar a Coqui XTTS v2 (10 min)

### 2.1. Ver Screens Activos

```bash
screen -ls
```

Busca el screen del TTS actual (puede ser `coqui-tts`, `tts`, o similar).

### 2.2. Detener TTS Actual

```bash
# Conectar al screen (usa el nombre que viste en screen -ls)
screen -r coqui-tts

# Detener el servidor: Ctrl+C
# Salir del screen: Ctrl+D
```

### 2.3. Iniciar XTTS v2

```bash
cd ~/capibara6/backend
screen -S coqui-xtts
./start_coqui_tts_py311.sh
```

**Primera vez:** Verás que descarga el modelo (~2 GB):
```
Downloading: 100%|████████| 2.1G/2.1G [05:23<00:00, 6.5MB/s]
```

Espera a ver:
```
🎙️  COQUI TTS SERVER - Capibara6
📦 Modelo: XTTS v2 (Máxima Calidad)
✅ Modelo cargado exitosamente
* Running on all addresses (0.0.0.0)
* Running on http://0.0.0.0:5002
```

Presiona: **Ctrl+A, luego D** (para salir del screen)

### 2.4. Verificar que Funciona

```bash
curl http://localhost:5002/health
```

**Debe responder:**
```json
{"status":"healthy","model":"xtts_v2","service":"coqui-tts"}
```

✅ **Coqui XTTS v2 activado!**

---

## ✅ Paso 3: Verificar en el Chat (2 min)

### 3.1. Abrir el Chat

```
https://www.capibara6.com/chat.html
```

### 3.2. Forzar Recarga del Cache

Presiona: **Ctrl+Shift+R** (Windows/Linux) o **Cmd+Shift+R** (Mac)

### 3.3. Abrir Consola del Navegador

Presiona: **F12** → pestaña **Console**

### 3.4. Verificar Logs

Busca estos mensajes:

```javascript
🔍 Verificando Smart MCP en: /api/mcp-health
📡 Respuesta MCP: status=200, ok=true
📦 Datos MCP: {status: "healthy", service: "mcp", port: 5010}
✅ Smart MCP ACTIVO: mcp  ← ¡ESTO ES LO IMPORTANTE!
```

Y también:

```javascript
🔊 TTS Integration cargado
✅ Funciones disponibles: speakText, stopSpeaking
```

### 3.5. Probar el Sistema

1. **Escribe una pregunta:**
   ```
   ¿Qué ventajas tiene usar Google TPU para entrenar modelos?
   ```

2. **Verifica:**
   - ✅ La respuesta se genera (streaming)
   - ✅ Aparecen las estadísticas (tokens, tiempo, entropía)
   - ✅ Hay un botón 🔊 en la respuesta

3. **Prueba el audio:**
   - Click en el botón 🔊
   - **Debe sonar con voz natural de alta calidad** (Coqui XTTS v2)

---

## 🎉 ¡Sistema 100% Operacional!

Si todo funciona, tendrás:

### ✅ Frontend
- Chat responsive
- 7 plantillas de perfil
- Rating system + entropía
- TTS con Coqui XTTS v2

### ✅ Backend
- 🧠 Gemma 3-12B (puerto 8080)
- 🔍 Smart MCP (puerto 5010) ← **Activado**
- 🎙️ Coqui XTTS v2 (puerto 5002) ← **Actualizado**

### ✅ Infraestructura
- Proxies HTTPS en Vercel
- Firewall configurado
- Variables de entorno OK

---

## 🔧 Comandos Útiles (Para Después)

### Ver Servicios Corriendo

```bash
# Conectar a VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Ver screens activos
screen -ls

# Conectar a un screen específico
screen -r nombre-del-screen

# Salir de un screen (sin cerrarlo): Ctrl+A, D
```

### Verificar Health de Servicios

```bash
curl http://localhost:8080/health  # Gemma
curl http://localhost:5010/health  # Smart MCP
curl http://localhost:5002/health  # Coqui TTS
```

### Reiniciar un Servicio

```bash
# 1. Conectar al screen
screen -r nombre-del-servicio

# 2. Detener con Ctrl+C

# 3. Reiniciar el script
./start_[servicio].sh

# 4. Salir: Ctrl+A, D
```

---

## 📊 Resumen Visual

```
┌─────────────────────────────────────────────────┐
│         Frontend (Vercel HTTPS)                 │
│         www.capibara6.com/chat.html             │
└────────────────┬────────────────────────────────┘
                 │ HTTPS Proxies
┌────────────────▼────────────────────────────────┐
│         Backend (VM: 34.175.104.187)            │
│  ┌──────────────────────────────────────────┐   │
│  │ 🧠 Gemma 3-12B (8080)    [ACTIVO]       │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ 🔍 Smart MCP (5010)      [ACTIVAR ✅]    │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ 🎙️ XTTS v2 (5002)        [ACTUALIZAR 🔄]│   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**⏱️ Tiempo estimado: 15 minutos**

**🎯 Resultado: Sistema completo y operacional**

---

## 💡 Tips Finales

1. **Los screens persisten:** Aunque cierres la terminal SSH, los servicios siguen corriendo.

2. **Primer inicio de XTTS v2:** Tarda 10-15 min (descarga modelo). Después tarda ~30 seg.

3. **Verificar logs en tiempo real:** Usa `screen -r nombre` para ver qué está pasando.

4. **Si algo falla:** Revisa `DIAGNOSTICO_MCP.md` o `verificar_servicios.sh`.

5. **Próxima vez que reinicies la VM:** Tendrás que iniciar los servicios de nuevo (los screens no persisten entre reinicios de VM).

---

**¡Adelante! 🚀 En 15 minutos tendrás todo funcionando perfectamente. ✨**

