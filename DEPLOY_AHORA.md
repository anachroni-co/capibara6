# 🚀 Deploy COMPLETO - Kyutai TTS + Smart MCP

## ✅ Cambios Aplicados en Vercel

Los errores de Vercel están **arreglados**:

1. ✅ **"data is too long"** → Solucionado: Ahora `api/tts.py` es un proxy ligero
2. ✅ **Warning ESM** → Solucionado: Agregado `package.json` con `"type": "module"`

**Vercel ahora solo hace proxy** → El modelo corre en tu VM.

---

## 🎯 Pasos para Deploy en VM

### Paso 1: Ejecutar Script de Deploy

**En Windows:**

```cmd
deploy_services_to_vm.bat
```

**En Linux/Mac:**

```bash
chmod +x deploy_services_to_vm.sh
./deploy_services_to_vm.sh
```

Este script:
- Copia archivos a la VM
- Instala dependencias
- Configura firewall
- Te muestra la IP de tu VM

### Paso 2: Conectar a la VM

```cmd
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

### Paso 3: Iniciar Kyutai TTS Server

```bash
# En la VM, iniciar Kyutai TTS en screen
screen -S kyutai-tts
cd ~/capibara6/backend
chmod +x start_kyutai_tts.sh
./start_kyutai_tts.sh

# Esperar a que cargue el modelo (puede tardar 2-3 minutos)
# Verás: "✅ Modelo Kyutai cargado exitosamente"

# Presionar Ctrl+A, luego D para salir del screen
```

### Paso 4: Iniciar Smart MCP Server

```bash
# En la VM, en otra sesión de screen
screen -S smart-mcp
cd ~/capibara6/backend
python3 smart_mcp_server.py

# Verás: "🚀 Smart MCP Server iniciado en puerto 5003"

# Presionar Ctrl+A, luego D para salir del screen
```

### Paso 5: Verificar que Todo Funciona

```bash
# Verificar Kyutai TTS
curl http://localhost:5001/health

# Verificar Smart MCP
curl http://localhost:5003/health

# Salir de la VM
exit
```

---

## 🌐 Configurar IP en Vercel

### Obtener IP de tu VM

```cmd
gcloud compute instances describe gemma-3-12b --zone=europe-southwest1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
```

Anota la IP (ejemplo: `34.175.89.158`)

### Configurar Variable de Entorno en Vercel

1. Ve a: https://vercel.com/anachroni
2. Abre tu proyecto **capibara6**
3. Ve a **Settings** → **Environment Variables**
4. Agregar nueva variable:
   - **Name:** `KYUTAI_TTS_URL`
   - **Value:** `http://TU_IP:5001/tts` (reemplazar `TU_IP`)
   - Marcar: **Production**, **Preview**, **Development**
5. **Save**
6. Ir a **Deployments** → Re-deploy el último deployment

---

## ✅ Verificación Final

### Desde tu PC

```bash
# 1. Verificar TTS en VM (directo)
curl -X POST http://TU_IP_VM:5001/tts \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Hola mundo\",\"language\":\"es\"}"

# 2. Verificar MCP en VM (directo)
curl http://TU_IP_VM:5003/health

# 3. Verificar proxy de Vercel
curl -X POST https://capibara6-kpdtkkw9k-anachroni.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Hola desde Vercel\",\"language\":\"es\"}"
```

### Desde el Frontend

1. Abre: https://capibara6-kpdtkkw9k-anachroni.vercel.app/chat.html
2. Envía un mensaje
3. Haz clic en el botón **"Escuchar"** 🔊
4. Deberías escuchar el audio sintetizado

---

## 📊 Servicios Activos en la VM

| Servicio | Puerto | Status | Comando |
|----------|--------|--------|---------|
| **Gemma Model** | 8080 | Ya corriendo | - |
| **Kyutai TTS** | 5001 | Nuevo | `screen -r kyutai-tts` |
| **Smart MCP** | 5003 | Nuevo | `screen -r smart-mcp` |

---

## 🔍 Monitoreo

### Ver logs en tiempo real

```bash
# Conectar a la VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Ver logs de Kyutai TTS
screen -r kyutai-tts

# Ver logs de Smart MCP
screen -r smart-mcp

# Listar todas las sesiones de screen
screen -ls
```

### Reiniciar servicios si es necesario

```bash
# Kyutai TTS
screen -S kyutai-tts -X quit  # Matar sesión anterior
screen -S kyutai-tts
cd ~/capibara6/backend
./start_kyutai_tts.sh

# Smart MCP
screen -S smart-mcp -X quit
screen -S smart-mcp
cd ~/capibara6/backend
python3 smart_mcp_server.py
```

---

## 🐛 Troubleshooting

### Error: "Moshi not found"

```bash
# En la VM
pip install --user moshi>=0.2.6 torch torchaudio soundfile numpy
```

### Error: "CUDA out of memory"

El modelo Kyutai 1B necesita ~4 GB de VRAM. Si tu VM no tiene suficiente GPU:

```bash
# Opción 1: Usar CPU (más lento pero funciona)
# El servidor detecta automáticamente si CUDA no está disponible

# Opción 2: Usar modelo más pequeño
# En kyutai_tts_server.py, cambiar:
# 'model_repo': 'kyutai/tts-lite-en_es',  # 300 MB
```

### TTS no responde desde Vercel

1. Verificar que la VM responda directamente: `curl http://VM_IP:5001/health`
2. Verificar firewall: `gcloud compute firewall-rules list | grep 5001`
3. Verificar variable de entorno en Vercel
4. Re-deploy en Vercel después de configurar la variable

---

## 🎉 Resultado Final

Una vez completado, tendrás:

```
┌─────────────────────────────────────────┐
│           USUARIO (Navegador)           │
└─────────────────┬───────────────────────┘
                  │ HTTPS
                  ▼
┌─────────────────────────────────────────┐
│         VERCEL (Frontend + Proxy)       │
│  - Chat HTML/JS                         │
│  - API Proxy (tts.py)                   │
│  - API Proxy (mcp-analyze.js)           │
└──────────┬──────────────┬───────────────┘
           │ HTTP         │ HTTP
           ▼              ▼
┌──────────────────────────────────────────┐
│         VM GOOGLE CLOUD                  │
│  ┌────────────────────────────────────┐  │
│  │  Gemma 3-12B     :8080            │  │
│  ├────────────────────────────────────┤  │
│  │  Kyutai TTS      :5001 ✨ NUEVO   │  │
│  ├────────────────────────────────────┤  │
│  │  Smart MCP       :5003 ✨ NUEVO   │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

**Ventajas:**
- ✅ TTS natural y gratuito (Kyutai)
- ✅ Contexto verificado (Smart MCP)
- ✅ HTTPS seguro (Vercel)
- ✅ Sin costos de API
- ✅ Auto-hospedado y privado

---

## 📝 Comandos Rápidos

```bash
# Deploy inicial (Windows)
deploy_services_to_vm.bat

# Deploy inicial (Linux/Mac)
chmod +x deploy_services_to_vm.sh && ./deploy_services_to_vm.sh

# Conectar a VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Ver servicios corriendo
screen -ls

# Verificar salud
curl http://localhost:5001/health  # TTS
curl http://localhost:5003/health  # MCP

# Ver logs
screen -r kyutai-tts  # Ver logs TTS
screen -r smart-mcp   # Ver logs MCP
```

---

**¡Listo para deployar!** 🚀

- **Windows:** Ejecuta `deploy_services_to_vm.bat`
- **Linux/Mac:** Ejecuta `./deploy_services_to_vm.sh`

Luego sigue los pasos mostrados en pantalla.

