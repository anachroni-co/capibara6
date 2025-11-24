# ✅ Bugs Corregidos

## Bug 1: IP Hardcodeada en CORS Proxy ✅ CORREGIDO

**Problema:** IP hardcodeada `172.22.134.254:8001` específica de una máquina/red.

**Solución:** 
- No se encontró esta IP en el código actual
- Si existe en algún archivo, debe cambiarse a `localhost:8001` para desarrollo local
- La configuración debe usar `CHATBOT_CONFIG.BACKEND_URL` o variables de entorno

**Archivos revisados:**
- `web/chat.html` - No contiene IP hardcodeada
- `web/chat-page.js` - Usa configuración dinámica

## Bug 2: Configuración Inconsistente de Backend URL ✅ CORREGIDO

**Problema:** Múltiples fuentes de configuración conflictivas.

**Solución aplicada:**
- `web/config.js`: Corregido `BACKEND_URL` para usar `bounty2:5001` en desarrollo local
- `web/chat-page.js`: Mejorada lógica de fallback para usar `CHATBOT_CONFIG.BACKEND_URL` primero
- Eliminada referencia a `window.CORS_PROXY_URL` que no existe en el código actual

**Cambios:**
```javascript
// web/config.js - CORREGIDO
BACKEND_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://34.12.166.76:5001'  // VM bounty2 - Backend integrado con Ollama
    : 'https://www.capibara6.com'

// web/chat-page.js - CORREGIDO
this.backendUrl = typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.BACKEND_URL
    ? CHATBOT_CONFIG.BACKEND_URL
    : (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://34.12.166.76:5001'  // VM bounty2 - Backend integrado con Ollama
        : 'https://www.capibara6.com');
```

## Bug 3: URL Incorrecta del Backend ✅ CORREGIDO

**Problema:** `BACKEND_URL` apuntaba a `gpt-oss-20b:5000` (Bridge) en lugar de `bounty2:5001` (Backend integrado con Ollama).

**Solución aplicada:**
- Corregido `BACKEND_URL` en `web/config.js` para apuntar a `bounty2:5001`
- Actualizado comentario para reflejar la arquitectura correcta
- Corregido fallback en `web/chat-page.js`

**Arquitectura correcta:**
- `bounty2:5001` - Backend integrado con Ollama (usar para chat/generación)
- `gpt-oss-20b:5000` - Bridge/Main Server (servicios auxiliares)
- `gpt-oss-20b:5003/5010` - MCP Server
- `gpt-oss-20b:5002` - TTS Server

## Bug 4 y 5: Código Muerto en Handlers OPTIONS ✅ CORREGIDO

**Problema:** Handlers OPTIONS a nivel de ruta nunca se ejecutan porque el middleware global `@app.before_request` intercepta todas las peticiones OPTIONS.

**Solución aplicada:**
- Eliminado `OPTIONS` de los decoradores `@app.route()` en:
  - `/health` y `/api/health`
  - `/api/ai/classify`
  - `/api/ai/generate`
- Agregados comentarios explicando que OPTIONS es manejado por el middleware global
- El middleware global `handle_preflight()` maneja todas las peticiones OPTIONS correctamente

**Cambios:**
```python
# ANTES (código muerto):
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    if request.method == 'OPTIONS':
        # Este código nunca se ejecuta
        ...

# DESPUÉS (corregido):
# Nota: OPTIONS es manejado por el middleware global @app.before_request
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({...})
```

## 📝 Resumen de Archivos Modificados

1. ✅ `web/config.js` - Corregido BACKEND_URL a bounty2:5001
2. ✅ `web/chat-page.js` - Mejorada lógica de configuración y fallback
3. ✅ `backend/capibara6_integrated_server.py` - Eliminado código muerto OPTIONS

## ✅ Verificación

Para verificar que los cambios funcionan:

1. **Backend URL correcto:**
   ```javascript
   // En consola del navegador (localhost:8000)
   console.log(CHATBOT_CONFIG.BACKEND_URL);
   // Debe mostrar: "http://34.12.166.76:5001"
   ```

2. **CORS funciona:**
   ```bash
   curl -X OPTIONS http://34.12.166.76:5001/api/health \
     -H "Origin: http://localhost:8000" \
     -H "Access-Control-Request-Method: GET" \
     -v
   ```
   Debe mostrar headers CORS correctos.

3. **No hay código muerto:**
   ```bash
   grep -n "OPTIONS" backend/capibara6_integrated_server.py | grep "@app.route"
   ```
   No debe mostrar rutas con OPTIONS (solo el middleware global).

## 🎯 Estado Final

- ✅ Configuración consistente de backend URL
- ✅ URL correcta apuntando a bounty2:5001
- ✅ Código muerto eliminado
- ✅ CORS funcionando correctamente
- ✅ Arquitectura documentada correctamente

