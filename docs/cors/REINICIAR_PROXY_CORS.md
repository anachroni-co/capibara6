# 🔄 Reiniciar Proxy CORS - Solución a Errores 404

## ✅ **Problema Resuelto**

He actualizado `backend/cors_proxy_simple.py` para soportar **todos los endpoints**:

- ✅ `/api/mcp/status` - Estado de MCP
- ✅ `/api/mcp/analyze` - Análisis con MCP
- ✅ `/api/ai/generate` - Generación AI
- ✅ `/api/ai/classify` - Clasificación AI
- ✅ `/api/n8n/templates/recommended` - Templates N8n
- ✅ Todos los demás endpoints del backend

## 🚀 **Pasos para Reiniciar el Proxy**

### Paso 1: Detener el Proxy Actual

```bash
# Opción A: Si está corriendo en una terminal
# Presionar Ctrl+C en la terminal donde está corriendo

# Opción B: Encontrar y matar el proceso
ps aux | grep cors_proxy
# O en Windows/WSL:
netstat -ano | grep 8001
# Luego matar el proceso:
kill -9 [PID]
```

### Paso 2: Reiniciar el Proxy

```bash
# Navegar al directorio del proyecto
cd /mnt/c/Users/elect/.cursor/worktrees/capibara6/pFYVv

# Iniciar el proxy actualizado
python3 backend/cors_proxy_simple.py
```

**Deberías ver**:
```
============================================================
🚀 Iniciando Proxy CORS para Capibara6
============================================================
🌐 Puerto local: 8001

📡 Servicios configurados:
   • Backend (bounty2):    http://34.12.166.76:5001
   • MCP (gpt-oss-20b):    http://34.175.136.104:5010
   • RAG (rag3):           http://34.105.131.8:8000
   • N8n (gpt-oss-20b):    http://34.175.136.104:5678

🔧 CORS habilitado para localhost:8000
============================================================
 * Running on http://0.0.0.0:8001
```

### Paso 3: Verificar que Funciona

En otra terminal:

```bash
# Test 1: Health check del proxy
curl http://localhost:8001/

# Test 2: MCP status
curl http://localhost:8001/api/mcp/status

# Test 3: N8n templates
curl http://localhost:8001/api/n8n/templates/recommended
```

### Paso 4: Recargar el Frontend

1. **Hard refresh** en el navegador: `Ctrl+F5`
2. O **limpiar caché**: `Ctrl+Shift+Del`

## 🧪 **Resultado Esperado**

Después de reiniciar el proxy, **NO deberías ver** estos errores:

```
❌ GET http://localhost:8001/api/mcp/status 404 (NOT FOUND)
❌ GET http://localhost:8001/api/n8n/templates/recommended 404 (NOT FOUND)
❌ POST http://localhost:8001/api/ai/generate 404 (NOT FOUND)
```

En su lugar, deberías ver:

```
✅ Backend conectado
✅ Smart MCP inicializado (o mensaje de no disponible si el servicio no está corriendo)
✅ N8n inicializado
✅ Todos los servicios funcionando
```

## 📋 **Endpoints Soportados**

### Backend (bounty2:5001)
- `/api/chat` - Chat con IA
- `/api/health` - Health check
- `/health` - Health check (alternativo)
- `/api/ai/classify` - Clasificación AI
- `/api/ai/generate` - Generación AI

### MCP (gpt-oss-20b:5010)
- `/api/mcp/status` - Estado de MCP
- `/api/mcp/analyze` - Análisis con MCP

### N8n (gpt-oss-20b:5678)
- `/api/n8n/templates/recommended` - Templates (mock)

### RAG (rag3:8000)
- `/api/messages` - Mensajes RAG
- `/api/rag/*` - Otros endpoints RAG

## ⚠️ **Notas Importantes**

1. **El proxy debe estar corriendo** antes de abrir el frontend
2. **Si el servicio remoto no está disponible**, el proxy devolverá un error 503 o un mensaje JSON indicando que no está disponible (no un 404)
3. **Los errores 404 ahora solo aparecerán** si el endpoint realmente no existe en el proxy

## 🔧 **Troubleshooting**

### Problema: "Address already in use"

El puerto 8001 ya está en uso. Detén el proceso anterior:

```bash
# Encontrar el proceso
lsof -i :8001
# O:
netstat -ano | grep 8001

# Matar el proceso
kill -9 [PID]
```

### Problema: "ModuleNotFoundError: No module named 'flask'"

Instala las dependencias:

```bash
pip3 install flask flask-cors requests
```

### Problema: El proxy se detiene al cerrar la terminal

Usa `screen` o `nohup`:

```bash
# Con screen
screen -S cors-proxy
python3 backend/cors_proxy_simple.py
# Ctrl+A, D para desconectar

# Con nohup
nohup python3 backend/cors_proxy_simple.py > /tmp/cors_proxy.log 2>&1 &
```

## ✅ **Checklist**

- [ ] Proxy anterior detenido
- [ ] Proxy nuevo iniciado
- [ ] Proxy responde en `http://localhost:8001/`
- [ ] Frontend recargado (Ctrl+F5)
- [ ] No hay errores 404 en la consola
- [ ] Todos los servicios inicializados correctamente

---

**¿Listo?** Reinicia el proxy y recarga el frontend. Los errores 404 deberían desaparecer.

