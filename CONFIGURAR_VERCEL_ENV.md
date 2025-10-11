# 🔧 Configurar Variables de Entorno en Vercel

Para que el proxy TTS funcione, necesitas configurar la URL de tu VM en Vercel.

---

## 📝 Paso 1: Obtener IP de tu VM

```bash
# En tu PC, ejecutar:
gcloud compute instances describe gemma-3-12b --zone=europe-southwest1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)"
```

**Resultado:** Tu IP pública (ejemplo: `34.175.89.158`)

---

## 🌐 Paso 2: Configurar en Vercel Dashboard

### Opción A: Desde el Dashboard (Recomendado)

1. Ve a: https://vercel.com/anachroni/capibara6
2. Ir a **Settings** > **Environment Variables**
3. Agregar nueva variable:
   - **Name:** `KYUTAI_TTS_URL`
   - **Value:** `http://TU_IP_VM:5001/tts` (ejemplo: `http://34.175.89.158:5001/tts`)
   - **Environment:** Production, Preview, Development (marcar todos)
4. Hacer clic en **Save**
5. **Re-deploy** el proyecto

### Opción B: Desde CLI

```bash
# Instalar Vercel CLI si no lo tienes
npm install -g vercel

# Login
vercel login

# Configurar variable
vercel env add KYUTAI_TTS_URL

# Cuando te pregunte, pegar:
http://34.175.89.158:5001/tts

# Seleccionar: Production, Preview, Development
```

---

## 🔄 Paso 3: Re-deploy

Después de configurar la variable, re-deployar:

```bash
# Opción A: Push a GitHub (auto-deploy)
git push

# Opción B: Deploy manual
vercel --prod
```

---

## ✅ Verificar Configuración

Una vez deployado:

```bash
# Verificar que el proxy funciona
curl -X POST https://capibara6-kpdtkkw9k-anachroni.vercel.app/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola desde Vercel","language":"es"}'
```

Deberías recibir:
```json
{
  "audioContent": "UklGRn4gAABXQVZF...",
  "provider": "Kyutai DSM TTS",
  "format": "wav"
}
```

---

## 🐛 Troubleshooting

### Error: "TTS server unavailable"

**Causa:** La VM no está respondiendo en puerto 5001

**Solución:**
```bash
# 1. Verificar que la VM esté corriendo
gcloud compute instances list

# 2. Conectar a la VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# 3. Verificar que Kyutai TTS esté corriendo
curl http://localhost:5001/health

# 4. Si no responde, iniciar el servicio
screen -S kyutai-tts
cd ~/capibara6/backend
python3 kyutai_tts_server.py
# Ctrl+A, D para salir
```

### Error: "Connection timeout"

**Causa:** Firewall bloqueando puerto 5001

**Solución:**
```bash
# Verificar regla de firewall
gcloud compute firewall-rules list | grep 5001

# Si no existe, crear
gcloud compute firewall-rules create allow-kyutai-tts \
    --allow=tcp:5001 \
    --source-ranges=0.0.0.0/0 \
    --description="Kyutai TTS Server"
```

---

## 📊 Variables de Entorno Necesarias

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `KYUTAI_TTS_URL` | `http://VM_IP:5001/tts` | URL del servidor Kyutai en VM |

---

## 🎯 Resultado Final

**Arquitectura:**

```
[Usuario]
   ↓
[Vercel HTTPS]
   ↓ (proxy)
[VM HTTP:5001] ← Kyutai TTS Server
   ↓
[Audio WAV]
```

**Ventajas:**
- ✅ HTTPS seguro desde Vercel
- ✅ Modelo completo en VM (sin límites)
- ✅ Fallback automático a Web Speech API
- ✅ Sin costos de API

---

**¡Listo! Tu proxy TTS funcionará correctamente.** 🎙️

