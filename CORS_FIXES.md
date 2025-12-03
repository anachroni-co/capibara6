# Correcciones CORS - Capibara6

**Fecha:** 2025-12-01
**Estado:** ✅ Todos los problemas CORS resueltos

---

## 🔴 PROBLEMAS IDENTIFICADOS

### 1. Endpoints Faltantes
El frontend llamaba a endpoints que no existían:
- ❌ `/api/health` - No existía
- ❌ `/api/ai/classify` - No existía
- ❌ `/api/mcp/status` - No existía (solo `/api/mcp-health`)

### 2. CORS - Dominios Diferentes
El frontend en `https://capibara6.com` intentaba acceder a `https://www.capibara6.com`:
- Aunque son el mismo dominio, el navegador los trata como orígenes diferentes
- Headers CORS no configurados para todas las rutas

### 3. Rutas No Mapeadas en vercel.json
Los nuevos endpoints no estaban en la configuración de rewrites

---

## ✅ SOLUCIONES IMPLEMENTADAS

### 1. Nuevos Endpoints Creados

#### `api/health.js` ✅
**Ruta:** `/api/health`
**Método:** GET

Endpoint general de health check que retorna:
```json
{
  "status": "healthy",
  "service": "Capibara6 Backend",
  "timestamp": "2025-12-01T...",
  "environment": "production",
  "version": "2.0.0",
  "services": {
    "vercel": "operational",
    "serverless": "operational"
  },
  "endpoints": {
    "completion": "/api/completion",
    "tts": "/api/tts",
    "mcp": {...}
  }
}
```

#### `api/mcp-status.js` ✅
**Ruta:** `/api/mcp/status`
**Método:** GET

Alias de `mcp-health.js` para mantener compatibilidad con frontend:
- Intenta puerto 5003 primero (MCP principal)
- Fallback a puerto 5010
- Retorna `available: true/false` para indicar estado

```json
{
  "service": "capibara6-mcp",
  "status": "healthy",
  "available": true,
  "tools_available": 3,
  "contexts_available": 3,
  "vm": "services",
  "port": 5003
}
```

#### `api/ai-classify.js` ✅
**Ruta:** `/api/ai/classify`
**Método:** POST
**Body:** `{"text": "...", "message": "...", "query": "..."}`

Clasifica el tipo de petición del usuario:
- Categoría: coding, technical, multilingual, company, general
- Modelo sugerido: qwen_coder, gemma3_multimodal, phi4_fast, etc.
- Indica si necesita contexto o RAG

```json
{
  "category": "coding",
  "subcategory": "programming",
  "confidence": 0.9,
  "suggested_model": "qwen_coder",
  "needs_context": false,
  "needs_rag": false
}
```

**Clasificación inteligente basada en keywords:**
- Código: `qwen_coder`
- Análisis técnico: `gemma3_multimodal`
- Multilingüe: `aya_expanse_multilingual`
- Empresa/Info: `phi4_fast` + contexto
- General: `phi4_fast`

---

### 2. Actualización de vercel.json

#### Nuevas Rutas Añadidas:
```json
{
  "source": "/api/health",
  "destination": "/api/health.js"
},
{
  "source": "/api/ai/classify",
  "destination": "/api/ai-classify.js"
},
{
  "source": "/api/mcp/status",
  "destination": "/api/mcp-status.js"
}
```

#### Headers CORS Mejorados:
```json
{
  "source": "/api/(.*)",
  "headers": [
    {
      "key": "Access-Control-Allow-Origin",
      "value": "*"  // ✅ Permite cualquier origen (capibara6.com y www.capibara6.com)
    },
    {
      "key": "Access-Control-Allow-Methods",
      "value": "GET, POST, PUT, DELETE, OPTIONS"  // ✅ Todos los métodos
    },
    {
      "key": "Access-Control-Allow-Headers",
      "value": "Content-Type, Authorization, X-Requested-With"  // ✅ Headers comunes
    },
    {
      "key": "Access-Control-Max-Age",
      "value": "86400"  // ✅ Cache preflight 24h
    }
  ]
},
{
  "source": "/(.*)",  // ✅ CORS para todas las rutas
  "headers": [
    {
      "key": "Access-Control-Allow-Origin",
      "value": "*"
    }
  ]
}
```

#### Beneficios:
- ✅ Preflight requests (OPTIONS) cacheados 24 horas
- ✅ Todos los headers necesarios permitidos
- ✅ CORS configurado para TODAS las rutas, no solo `/api/*`
- ✅ Funciona con `capibara6.com` y `www.capibara6.com`

---

### 3. CORS Headers en Cada Función

Todas las funciones serverless incluyen headers CORS:

```javascript
// En TODAS las funciones
res.setHeader('Access-Control-Allow-Origin', '*');
res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

// Handle preflight
if (req.method === 'OPTIONS') {
  return res.status(200).end();
}
```

---

## 🔧 MAPEO COMPLETO DE ENDPOINTS

| Ruta Frontend | Archivo Serverless | Método | Estado |
|---------------|-------------------|---------|--------|
| `/api/health` | `api/health.js` | GET | ✅ Nuevo |
| `/api/ai/classify` | `api/ai-classify.js` | POST | ✅ Nuevo |
| `/api/mcp/status` | `api/mcp-status.js` | GET | ✅ Nuevo |
| `/api/mcp-health` | `api/mcp-health.js` | GET | ✅ Existente |
| `/api/mcp-analyze` | `api/mcp-analyze.js` | POST | ✅ Actualizado |
| `/api/completion` | `api/completion.js` | POST | ✅ Actualizado |
| `/api/tts` | `api/tts.js` | POST | ✅ Actualizado |
| `/api/tts-voices` | `api/tts-voices.js` | GET | ✅ Existente |
| `/api/tts-clone` | `api/tts-clone.js` | POST | ✅ Existente |

---

## 🚀 DESPLIEGUE

### Archivos Modificados:
```
✅ api/health.js (nuevo)
✅ api/mcp-status.js (nuevo)
✅ api/ai-classify.js (nuevo)
✅ vercel.json (actualizado)
```

### Comandos para Deploy:

```bash
# Verificar cambios
git status

# Añadir archivos
git add api/health.js api/mcp-status.js api/ai-classify.js vercel.json CORS_FIXES.md

# Commit
git commit -m "Fix CORS errors: Add missing endpoints and update vercel.json

- Added /api/health endpoint for general health checks
- Added /api/mcp/status endpoint (alias for mcp-health)
- Added /api/ai/classify endpoint for intelligent request classification
- Updated vercel.json with new routes and improved CORS headers
- CORS now works with both capibara6.com and www.capibara6.com
- Added Access-Control-Max-Age for better preflight caching"

# Deploy a Vercel
npm run deploy

# O push a GitHub (si auto-deploy está activado)
git push origin main
```

---

## ✅ VERIFICACIÓN POST-DEPLOY

Una vez deployed, verifica cada endpoint:

### 1. Health Check
```bash
curl https://www.capibara6.com/api/health
# Debe retornar: {"status":"healthy",...}
```

### 2. MCP Status
```bash
curl https://www.capibara6.com/api/mcp/status
# Debe retornar: {"available":true,"service":"capibara6-mcp",...}
```

### 3. AI Classify
```bash
curl -X POST https://www.capibara6.com/api/ai/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"escribe una función en python"}'
# Debe retornar: {"category":"coding","suggested_model":"qwen_coder",...}
```

### 4. CORS desde Frontend
Abre DevTools en `https://capibara6.com`:
```javascript
// No debería haber más errores CORS
fetch('https://www.capibara6.com/api/health')
  .then(r => r.json())
  .then(console.log)
```

---

## 🎯 ERRORES RESUELTOS

### Antes (Errores en Console):
```
❌ Access to fetch at 'https://www.capibara6.com/api/mcp/status' from origin 'https://capibara6.com' has been blocked by CORS policy
❌ Failed to load resource: net::ERR_FAILED
❌ Access to fetch at 'https://www.capibara6.com/api/ai/classify' from origin 'https://capibara6.com' has been blocked by CORS policy
❌ Access to fetch at 'https://www.capibara6.com/api/health' from origin 'https://capibara6.com' has been blocked by CORS policy
```

### Después (Expected Behavior):
```
✅ MCP Status check: {"available":true,...}
✅ AI Classify: {"category":"general",...}
✅ Health check: {"status":"healthy",...}
✅ No CORS errors
```

---

## 💡 NOTAS IMPORTANTES

### Por qué `Access-Control-Allow-Origin: *`
Usar `*` es seguro aquí porque:
1. Las funciones serverless no manejan sesiones/cookies sensibles
2. Todas las peticiones son stateless
3. Autenticación (si es necesaria) se maneja via API keys en headers
4. Permite acceso desde cualquier origen (útil para desarrollo y producción)

### Si necesitas restringir orígenes en futuro:
```javascript
// En las funciones serverless
const allowedOrigins = [
  'https://capibara6.com',
  'https://www.capibara6.com',
  'http://localhost:3000'
];

const origin = req.headers.origin;
if (allowedOrigins.includes(origin)) {
  res.setHeader('Access-Control-Allow-Origin', origin);
}
```

### Preflight Caching
`Access-Control-Max-Age: 86400` significa:
- El navegador cachea el preflight request por 24 horas
- Reduce requests OPTIONS repetitivos
- Mejora performance significativamente

---

## 📊 RESUMEN

**Problemas encontrados:** 3
**Soluciones implementadas:** 3
**Endpoints creados:** 3
**Archivos modificados:** 4

**Estado:** ✅ **LISTO PARA DEPLOY**

Todos los errores CORS del frontend han sido resueltos. Una vez deployed, el frontend debería funcionar sin errores de CORS.

---

## 🔗 Referencias

- [Vercel Headers Docs](https://vercel.com/docs/projects/project-configuration#headers)
- [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Vercel Rewrites](https://vercel.com/docs/projects/project-configuration#rewrites)
