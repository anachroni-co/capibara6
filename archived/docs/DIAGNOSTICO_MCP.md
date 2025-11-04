# 🔍 Diagnóstico: Smart MCP No Se Activa

## 📋 Síntomas

El frontend muestra: `ℹ️ Smart MCP no disponible (se usará modo directo)`

---

## ✅ Paso 1: Verificar Servicios en la VM

### Conectar a la VM

```bash
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b
```

### Ejecutar Script de Verificación

```bash
cd ~/capibara6/backend
chmod +x verificar_servicios.sh
./verificar_servicios.sh
```

**Resultado esperado:**
```
✓ Gemma 3-12B (puerto 8080)... ACTIVO
✓ Smart MCP (puerto 5010)... ACTIVO
✓ Coqui TTS (puerto 5002)... ACTIVO
```

### Si Smart MCP NO está activo:

```bash
# Ver si hay un screen corriendo
screen -ls

# Si NO hay screen "smart-mcp", iniciarlo:
screen -S smart-mcp
cd ~/capibara6/backend
./start_smart_mcp.sh

# Esperar a ver: "Running on http://0.0.0.0:5010"
# Presionar Ctrl+A, D para salir
```

### Verificar manualmente:

```bash
curl http://localhost:5010/health
```

**Debe responder:**
```json
{"status":"healthy","service":"mcp","port":5010}
```

---

## ✅ Paso 2: Verificar Firewall Google Cloud

### Desde tu PC Local

```bash
# Verificar que el firewall permita el puerto 5010
gcloud compute firewall-rules list --filter="name:mcp"
```

**Debe mostrar:**
```
allow-smart-mcp-5010  ...  tcp:5010  ...
```

### Si NO existe:

```bash
gcloud compute firewall-rules create allow-smart-mcp-5010 \
    --allow=tcp:5010 \
    --source-ranges=0.0.0.0/0 \
    --description="Smart MCP Server"
```

---

## ✅ Paso 3: Verificar Variables de Vercel

### Ve a Vercel Dashboard

1. https://vercel.com
2. Tu proyecto → **Settings** → **Environment Variables**

### Verifica que existan:

| Nombre | Valor |
|--------|-------|
| `SMART_MCP_URL` | `http://34.175.104.187:5010/analyze` |
| `KYUTAI_TTS_URL` | `http://34.175.104.187:5002/tts` |

**⚠️ IMPORTANTE:** Marcar los 3 checkboxes:
- ✅ Production
- ✅ Preview
- ✅ Development

### Si hiciste cambios:

**Re-deploy** el proyecto en Vercel para aplicar las variables.

---

## ✅ Paso 4: Probar Conexión Directa

### Desde tu PC, probar la VM:

```bash
curl http://34.175.104.187:5010/health
```

**Debe responder:**
```json
{"status":"healthy","service":"mcp","port":5010}
```

### Si NO responde:

1. El servicio no está corriendo → volver al Paso 1
2. El firewall está bloqueando → volver al Paso 2

---

## ✅ Paso 5: Probar Proxy de Vercel

### Desde el navegador (consola):

```javascript
fetch('https://www.capibara6.com/api/mcp-health')
  .then(r => r.json())
  .then(d => console.log('MCP Health:', d))
```

**Resultado esperado:**
```javascript
MCP Health: {status: "healthy", service: "mcp", port: 5010}
```

### Si devuelve error 503:

- El proxy de Vercel no puede alcanzar la VM
- Verificar que la IP en `SMART_MCP_URL` sea correcta
- Verificar firewall

---

## ✅ Paso 6: Verificar Frontend

### Abrir Consola del Navegador

1. Ir a: https://www.capibara6.com/chat.html
2. Presionar F12 → Consola
3. Buscar estos logs:

```javascript
🔍 Verificando Smart MCP en: /api/mcp-health
📡 Respuesta MCP: status=200, ok=true
📦 Datos MCP: {status: "healthy", service: "mcp", port: 5010}
✅ Smart MCP ACTIVO: mcp
```

### Si ves:

```javascript
ℹ️ Smart MCP no disponible (se usará modo directo)
🔍 Error: [mensaje de error]
```

**Solución:** El error te dirá exactamente qué falló:
- `Failed to fetch` → Problema de red/firewall
- `timeout` → El servicio tarda mucho/no responde
- `503` → El proxy no puede alcanzar la VM

---

## 🎯 Checklist Completo

Marca cada paso:

- [ ] 1. Smart MCP corriendo en VM (puerto 5010)
- [ ] 2. Health check responde: `curl http://localhost:5010/health`
- [ ] 3. Firewall abierto: `allow-smart-mcp-5010`
- [ ] 4. Variables en Vercel configuradas
- [ ] 5. Re-deploy en Vercel realizado
- [ ] 6. Conexión externa funciona: `curl http://34.175.104.187:5010/health`
- [ ] 7. Proxy funciona: `https://www.capibara6.com/api/mcp-health`
- [ ] 8. Frontend detecta MCP activo

---

## 💡 Logs Útiles

### En la VM:

```bash
# Ver logs del MCP
screen -r smart-mcp

# Ver últimas líneas
tail -f ~/capibara6/backend/mcp.log  # Si existe

# Ver proceso
ps aux | grep smart_mcp
```

### En Vercel:

1. Dashboard → Tu proyecto → **Deployments**
2. Click en el último deploy → **Functions**
3. Click en `api/mcp-health.js` → **Logs**

---

## 🚨 Solución Rápida

Si todo falla, reinicia el servicio MCP:

```bash
# Conectar a VM
gcloud compute ssh gemma-3-12b --zone=europe-southwest1-b

# Matar proceso MCP anterior
pkill -f smart_mcp_server

# Limpiar screens
screen -ls | grep smart-mcp | awk '{print $1}' | xargs -I {} screen -X -S {} quit

# Reiniciar limpio
screen -S smart-mcp
cd ~/capibara6/backend
./start_smart_mcp.sh

# Ctrl+A, D
# Verificar
curl http://localhost:5010/health
```

**¡Ahora recarga la página del chat y debería funcionar!** 🎉

