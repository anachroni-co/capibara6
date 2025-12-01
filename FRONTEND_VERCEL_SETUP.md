# Configuración del Frontend para Vercel - Capibara6

## 🎯 Objetivo
Este documento describe cómo configurar el frontend de Capibara6 para que funcione correctamente con Vercel como proxy a las VMs de backend.

## 🏗️ Arquitectura Actual

### VMs (Google Cloud)
- **models-europe** (34.175.48.2): vLLM, Ollama, modelos IA
- **services** (34.175.136.104): TTS, MCP, N8N, servicios adicionales
- **rag-europe** (34.175.110.120): Bridge API, Milvus, Nebula, PostgreSQL, Redis

### Vercel (Proxy)
- **Frontend**: `https://www.capibara6.com`
- **API Serverless Functions**: Actúan como proxy a las VMs
- **Endpoints**: `/api/completion`, `/api/tts`, `/api/mcp-*`, etc.

## 🔄 Flujo de Comunicación

### Desarrollo (localhost)
```
Frontend (localhost:3000) 
    └──→ Backend Local (localhost:5001/5002/5003)
```

### Producción (Vercel)
```
Frontend (www.capibara6.com)
    └──→ Vercel API Functions (www.capibara6.com/api/*)
        └──→ VMs Backend (34.175.48.2, 34.175.136.104, etc.)
```

## 📁 Archivos Actualizados

### 1. `frontend/src/config.js`
- Configura URLs dinámicas según entorno (localhost vs producción)
- Usa endpoints de Vercel en producción
- Actualiza IPs correctas de las VMs

### 2. `frontend/src/chat-app.js`
- Usa endpoint `/api/completion` de Vercel en producción
- Mantiene `http://localhost:5001/api/chat` para desarrollo

### 3. `frontend/src/clients/api-client.js`
- Detecta automáticamente entorno (localhost vs producción)
- Usa endpoints adecuados según el entorno
- `/api/completion` en producción, `/api/chat` en desarrollo

## 🛠️ Configuración de Vercel

### Variables de Entorno (Vercel Dashboard)
```bash
# vLLM Principal
VLLM_URL=http://34.175.48.2:8080/v1/chat/completions

# Ollama Fallback
OLLAMA_URL=http://34.175.48.2:11434/api/generate

# TTS Service
TTS_URL=http://34.175.136.104:5002/speak

# MCP Service
MCP_HEALTH_URL=http://34.175.136.104:5003/api/mcp/health
MCP_AUGMENT_URL=http://34.175.136.104:5003/api/mcp/augment

# Seguridad
INTER_VM_API_KEY=TaKnyUy9Yqhxme6PmbUXHTX3rjq_3XF1HPMQQXW-29w
```

### vercel.json
- Ya configurado con rewrites y headers CORS
- Endpoints disponibles: `/api/completion`, `/api/tts`, `/api/health`, `/api/mcp-*`, etc.

## 📱 Endpoints Usados por el Frontend

### Producción (Vercel)
- `https://www.capibara6.com/api/completion` → vLLM/Ollama
- `https://www.capibara6.com/api/tts` → TTS Service
- `https://www.capibara6.com/api/mcp-health` → MCP Health
- `https://www.capibara6.com/api/mcp-analyze` → MCP Analysis
- `https://www.capibara6.com/api/health` → Health Check
- `https://www.capibara6.com/api/ai/classify` → Task Classification

### Desarrollo (Localhost)
- `http://localhost:5001/api/chat` → Backend Local
- `http://localhost:5002/` → TTS Local
- `http://localhost:5003/` → MCP Local

## 🧪 Pruebas Post-Deploy

### 1. Health Check
```bash
curl https://www.capibara6.com/api/health
```

### 2. Completions
```bash
curl -X POST https://www.capibara6.com/api/completion \
  -H "Content-Type: application/json" \
  -d '{"message":"Hola","model":"phi4_fast"}'
```

### 3. TTS
```bash
curl -X POST https://www.capibara6.com/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hola mundo","language":"es"}'
```

### 4. MCP
```bash
curl https://www.capibara6.com/api/mcp-health
```

## ⚠️ Problemas Comunes y Soluciones

### 1. Error 400 en `/api/ai/classify`
- Verificar que el endpoint exista en `api/ai-classify.js`
- Confirmar que el vercel.json tiene el rewrite correcto

### 2. Conexiones CORS
- Headers CORS ya configurados en vercel.json
- Permiten acceso desde `capibara6.com` y `www.capibara6.com`

### 3. Fallo de conexión a servicios backend
- Verificar que las IPs de las VMs sean accesibles
- Confirmar que los puertos estén abiertos en el firewall

## 🚀 Deploy

```bash
# Asegurar cambios
git add frontend/src/config.js frontend/src/chat-app.js frontend/src/clients/api-client.js
git commit -m "feat: actualizar configuración para Vercel proxy"
git push origin main

# El deploy se hará automáticamente si está conectado a GitHub
# O manualmente con:
# vercel --prod
```

## 📋 Checklist Pre-Deploy

- [x] Configuración dinámica localhost/producción implementada
- [x] IPs correctas de VMs utilizadas
- [x] Endpoints de Vercel configurados correctamente
- [x] CORS configurado en vercel.json
- [x] Variables de entorno en Vercel Dashboard actualizadas
- [x] Pruebas de conectividad verificadas
- [x] Documentación actualizada

## 📞 Soporte

Si hay problemas con la configuración:
1. Verificar logs de Vercel: Dashboard → Deployments → Logs
2. Probar endpoints directamente con curl
3. Confirmar estado de servicios en las VMs