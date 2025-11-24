# 🔌 Solución: Proxy CORS Local

## 🔍 Problema Identificado

El frontend está intentando conectarse a `localhost:8001` (un proxy CORS local) que **SÍ existe** pero no tiene todos los endpoints necesarios:

```
✅ GET http://localhost:8001/ → OK (proxy responde)
❌ GET http://localhost:8001/api/health → 404
❌ GET http://localhost:8001/api/mcp/status → 404
❌ GET http://localhost:8001/api/n8n/templates/recommended → 404
```

## 💡 Solución: Proxy CORS Completo

He creado un **proxy CORS completo** que soporta todos los servicios:

### Archivo: `backend/cors_proxy_complete.py`

**Características**:
- ✅ Soporta Backend (bounty2:5001)
- ✅ Soporta MCP (gpt-oss-20b:5010)
- ✅ Soporta RAG (rag3:8000)
- ✅ Soporta N8n (gpt-oss-20b:5678)
- ✅ Maneja preflight OPTIONS correctamente
- ✅ Limpia headers conflictivos
- ✅ CORS configurado para localhost:8000

## 🚀 Iniciar el Proxy CORS

### Opción 1: Comando directo

```bash
# Desde el directorio del proyecto
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/pFYVv

# Iniciar el proxy
python3 backend/cors_proxy_complete.py
```

### Opción 2: En background

```bash
# Iniciar en background
nohup python3 backend/cors_proxy_complete.py > /tmp/cors_proxy.log 2>&1 &

# Ver el proceso
ps aux | grep cors_proxy_complete

# Ver logs
tail -f /tmp/cors_proxy.log
```

### Opción 3: Con screen (Recomendado)

```bash
# Crear sesión de screen
screen -S cors-proxy

# Iniciar el proxy
python3 backend/cors_proxy_complete.py

# Desconectar sin cerrar: Ctrl+A, luego D

# Para volver a conectar
screen -r cors-proxy
```

## 🧪 Verificar que Funciona

### Test 1: Health Check del Proxy

```bash
curl http://localhost:8001/
```

**Respuesta esperada**:
```json
{
  "status": "ok",
  "service": "capibara6-cors-proxy",
  "backend_target": "http://34.12.166.76:5001",
  "timestamp": "2025-11-13T...",
  "endpoints": {
    "backend": "http://34.12.166.76:5001",
    "mcp": "http://34.175.136.104:5010",
    "rag": "http://34.105.131.8:8000",
    "n8n": "http://34.175.136.104:5678"
  }
}
```

### Test 2: Backend Health

```bash
curl http://localhost:8001/api/health
```

### Test 3: MCP Status

```bash
curl http://localhost:8001/api/mcp/status
```

### Test 4: Desde el Frontend

Abre `http://localhost:8000/chat.html` y revisa la consola:

```javascript
// Ya NO deberías ver errores 404
✅ Backend conectado
✅ Smart MCP initialized
✅ RAG initialized
✅ N8n initialized
```

## 📊 Endpoints Soportados

### Backend (bounty2:5001)

| Endpoint Local | Target Remoto | Descripción |
|----------------|---------------|-------------|
| `/api/health` | `34.12.166.76:5001/health` | Health check |
| `/health` | `34.12.166.76:5001/health` | Health check (alternativo) |
| `/api/chat` | `34.12.166.76:5001/api/chat` | Chat con IA |
| `/api/ai/classify` | `34.12.166.76:5001/api/ai/classify` | Clasificación AI |
| `/api/ai/generate` | `34.12.166.76:5001/api/ai/generate` | Generación AI |

### MCP (gpt-oss-20b:5010)

| Endpoint Local | Target Remoto | Descripción |
|----------------|---------------|-------------|
| `/api/mcp/status` | `34.175.136.104:5010/health` | Estado de MCP |
| `/api/mcp/analyze` | `34.175.136.104:5010/api/mcp/analyze` | Análisis con MCP |

### RAG (rag3:8000)

| Endpoint Local | Target Remoto | Descripción |
|----------------|---------------|-------------|
| `/api/rag/health` | `34.105.131.8:8000/health` | Health check RAG |
| `/api/messages` | `34.105.131.8:8000/api/messages` | Mensajes RAG |

### N8n (gpt-oss-20b:5678)

| Endpoint Local | Target Remoto | Descripción |
|----------------|---------------|-------------|
| `/api/n8n/templates/recommended` | Mock local | Templates N8n |

## 🔧 Troubleshooting

### Problema: Puerto 8001 ya está en uso

```bash
# Ver qué proceso usa el puerto
lsof -i :8001
# O en Windows/WSL:
netstat -ano | grep 8001

# Matar el proceso
kill -9 [PID]

# O cambiar el puerto en el archivo
# Editar backend/cors_proxy_complete.py, línea final:
# app.run(host='0.0.0.0', port=8002, debug=False)
```

### Problema: Error "ModuleNotFoundError: No module named 'flask_cors'"

```bash
# Instalar dependencias
pip3 install flask flask-cors requests
```

### Problema: El proxy se detiene al cerrar la terminal

Usa `screen` o `nohup` como se mostró arriba.

### Problema: Timeout en las requests

El proxy tiene timeouts configurados:
- Chat: 300 segundos (5 minutos)
- Otros endpoints: 30 segundos

Si necesitas más tiempo, edita el archivo `backend/cors_proxy_complete.py`.

## 📝 Logs y Monitoreo

### Ver logs del proxy

Si lo iniciaste con `nohup`:
```bash
tail -f /tmp/cors_proxy.log
```

Si lo iniciaste con `screen`:
```bash
screen -r cors-proxy
```

### Logs en la consola del navegador

Con el proxy corriendo, deberías ver:
```
✅ Backend conectado
✅ Smart MCP inicializado
✅ RAG inicializado
✅ N8n inicializado
```

## 🎯 Siguiente Paso

Una vez iniciado el proxy, **recarga el frontend** con:

1. **Hard refresh**: Ctrl+F5
2. **Limpiar caché**: Ctrl+Shift+Del
3. **O abrir en modo incógnito**

## ⚠️ Nota Importante

Este proxy es para **desarrollo local** solamente. Para producción en Vercel, el frontend debe conectarse directamente a las VMs (con CORS configurado en cada servicio).

## 🔄 Alternativa: Sin Proxy

Si prefieres NO usar el proxy local, puedes:

1. Asegurarte de que cada servicio tenga CORS configurado correctamente
2. Actualizar el frontend para conectarse directamente a las IPs públicas

Ver `SOLUCION_SIN_PROXY.md` para esta alternativa.

## 📚 Archivos Relacionados

- `backend/cors_proxy_complete.py` - El proxy completo (NUEVO)
- `backend/cors_proxy_simple.py` - Proxy simple (solo backend)
- `backend/cors_proxy.py` - Proxy antiguo (no usar)
- `DIAGNOSTICO_ESTADO_ACTUAL.md` - Diagnóstico del problema
- `RESUMEN_CONFIGURACION_COMPLETA.md` - Configuración general

## ✅ Checklist

- [ ] Dependencias instaladas (`flask`, `flask-cors`, `requests`)
- [ ] Proxy iniciado en puerto 8001
- [ ] Proxy responde en `http://localhost:8001/`
- [ ] Frontend recargado (Ctrl+F5)
- [ ] No hay errores 404 en la consola
- [ ] Todos los servicios inicializados correctamente

---

**¿Listo para iniciar el proxy?** Ejecuta:

```bash
python3 backend/cors_proxy_complete.py
```

Y recarga el frontend en tu navegador.

