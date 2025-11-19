# 🚀 Inicio Rápido - Capibara6

## ⚡ Opción 1: Modo Demo (Sin VMs - Para probar ahora)

**El chat funcionará inmediatamente con respuestas simuladas:**

```bash
# 1. Asegúrate de que .env tiene USE_DEMO_MODE=true
cd ~/capibara6/backend
cat .env | grep USE_DEMO_MODE
# Debe mostrar: USE_DEMO_MODE=true

# 2. Inicia el servidor
python3 server_gptoss.py
```

**En otra terminal:**
```bash
# 3. Inicia el frontend
cd ~/capibara6/web
python3 -m http.server 8000
```

**4. Abre en tu navegador:**
```
http://localhost:8000/chat.html
```

✅ **Todo funcionará**: UI, botones de envío, subida de archivos
⚠️ **Las respuestas serán simuladas** (texto fijo de demo)

---

## 🌐 Opción 2: Modo Producción (Con VMs de Google Cloud)

### Requisitos previos:

1. **VMs encendidas** en Google Cloud
2. **Puertos abiertos** en firewall:
   - 8080 (GPT-OSS)
   - 5001 (Backend API)
   - 5002 (TTS)
   - 5003 (MCP)
   - 5678 (N8N)
3. **Servicios corriendo** en las VMs

### Configuración:

```bash
cd ~/capibara6/backend

# Cambiar a modo producción
nano .env
# Cambia: USE_DEMO_MODE=false
# Y verifica que las IPs sean correctas
```

### Verificar conectividad:

```bash
# Probar VM de modelos
curl http://34.12.166.76:8080/health

# Probar VM de servicios
curl http://34.175.136.104:5002/health
```

Si ambos responden, inicia el servidor:

```bash
python3 server_gptoss.py
```

---

## 🔧 Solución de Problemas

### Las VMs no responden:

**Verifica en Google Cloud Console:**
1. Ve a: https://console.cloud.google.com/compute/instances
2. Verifica que las VMs estén **encendidas** (verde)
3. Verifica las **IPs externas** (pueden cambiar si se reinician)

**Abre los puertos en firewall:**
```bash
# Crear reglas de firewall (ejecutar desde gcloud CLI o Cloud Shell)
gcloud compute firewall-rules create allow-capibara6 \
  --allow tcp:5001,tcp:8080,tcp:5002,tcp:5003,tcp:5678 \
  --source-ranges 0.0.0.0/0 \
  --description "Allow Capibara6 services"
```

**Conéctate por SSH para verificar servicios:**
```bash
# SSH a VM de modelos
gcloud compute ssh bounty --zone=YOUR_ZONE

# Dentro de la VM, verifica qué está corriendo:
ps aux | grep -E "python|server"
netstat -tulpn | grep LISTEN
```

### El chat no carga:

1. **Limpia cache del navegador**: `Ctrl + Shift + Del`
2. **Hard refresh**: `Ctrl + Shift + R`
3. **Verifica consola del navegador**: F12 > Console

### Backend no inicia:

```bash
# Verifica dependencias
cd ~/capibara6/backend
pip install flask flask-cors requests python-dotenv

# Verifica puerto disponible
lsof -i :5001
# Si está ocupado, mata el proceso o cambia PORT en .env
```

---

## 📋 Archivos de configuración disponibles

En `backend/`:
- `.env` - Configuración actual (se crea al inicio)
- `.env.example` - Plantilla base
- `.env.local` - Para desarrollo local
- `.env.production` - Para producción con VMs

**Cambiar entre configuraciones:**
```bash
cd ~/capibara6/backend

# Para desarrollo local/demo:
cp .env.local .env

# Para producción:
cp .env.production .env
# Luego edita USE_DEMO_MODE=false
```

---

## ✅ Checklist de verificación

Antes de reportar un problema, verifica:

- [ ] El servidor backend está corriendo (puerto 5001)
- [ ] El servidor web está corriendo (puerto 8000)
- [ ] El navegador puede acceder a localhost:8000
- [ ] La consola del navegador (F12) no muestra errores
- [ ] El archivo .env existe en backend/
- [ ] Si usas VMs, están encendidas y accesibles

---

## 🆘 Soporte

**Email**: marco@anachroni.co
**Repositorio**: https://github.com/anachroni-co/capibara6
