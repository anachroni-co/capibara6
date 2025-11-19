# 🔥 Configuración Final de Firewalls - Capibara6

## 📋 Resumen de Puertos por VM

### VM: **bounty2** (34.12.166.76)
**Puertos abiertos externamente**:
- ✅ **5000** - Capibara6 Integrated Server
- ✅ **5002** - Coqui TTS Server
- ✅ **8080** - Gemma Model Server / CapibaraGPT-v2 GUI
- ✅ **7001** - Nebula Graph Studio
- ✅ **80** - HTTP
- ✅ **22** - SSH

**Puertos NO abiertos externamente**:
- ❌ **5001** - Backend Flask (usar 5000 en su lugar)
- ❌ **11434** - Ollama API (solo acceso interno 10.0.0.0/8)

**Puertos internos/TPU**:
- 🔒 **8470** - TPU interno (solo 10.0.0.0/8)
- 🔒 **9230** - TPU healthcheck (rangos Google)
- 🔒 **12355** - TPU coordination (solo 10.128.0.0/20)

### VM: **gpt-oss-20b** (34.175.136.104)
**Puertos abiertos externamente**:
- ✅ **5000** - Capibara6 Main Server
- ✅ **5001** - Kyutai TTS Server
- ✅ **5003** - Smart MCP Server
- ✅ **8080** - Gemma Model Server / CapibaraGPT-v2 GUI
- ✅ **80** - HTTP
- ✅ **443** - HTTPS
- ✅ **22** - SSH
- ✅ **7001** - Nebula Graph Studio

**Puertos NO abiertos**:
- ❌ **5002** - TTS (usar 5001 en su lugar)
- ❌ **5010** - MCP alternativo (usar 5003 en su lugar)
- ❌ **5678** - N8n (necesita regla de firewall)

### VM: **rag3** (IP a obtener)
**Puertos abiertos externamente**:
- ✅ **5000** - Capibara6 Integrated Server
- ✅ **5001** - Kyutai TTS Server
- ✅ **8080** - llama.cpp Server / CapibaraGPT-v2 GUI
- ✅ **11434** - Ollama API
- ✅ **443** - HTTPS
- ✅ **22** - SSH
- ✅ **7001** - Nebula Graph Studio

**Puertos NO abiertos**:
- ❌ **8000** - RAG API (usar 5000 en su lugar o añadir regla)

## 🔧 Configuración Actualizada

### Backend Principal
- **bounty2**: Puerto **5000** ✅ (actualizado de 5001)
- Proxy CORS: `http://localhost:8001` → `http://34.12.166.76:5000`

### Ollama
- **NO accesible externamente** desde el frontend
- Solo accesible internamente (10.0.0.0/8) o a través del backend integrado
- El backend en puerto 5000 puede acceder a Ollama internamente

### TTS
- **bounty2**: Puerto **5002** (Coqui TTS Server) ✅
- **gpt-oss-20b**: Puerto **5001** (Kyutai TTS Server) ✅

### MCP
- **gpt-oss-20b**: Puerto **5003** (Smart MCP Server) ✅
- **Backend integrado**: A través de bounty2:5000 (integrado) ✅

### RAG API
- **rag3**: Puerto **5000** (temporal, hasta abrir 8000) ⚠️

### N8n
- **gpt-oss-20b**: Puerto **5678** NO está abierto ⚠️
- Necesita regla de firewall o verificar puerto alternativo

## ✅ Cambios Realizados

1. ✅ **backend/cors_proxy_simple.py**: Actualizado a puerto 5000
2. ✅ **web/config.js**: 
   - Ollama marcado como no accesible externamente
   - RAG API actualizado a puerto 5000
   - TTS en gpt-oss-20b actualizado a puerto 5001
3. ✅ **web/smart-mcp-integration.js**: Comentarios actualizados

## 📝 Próximos Pasos

1. ⚠️ **Verificar que el backend está corriendo en puerto 5000** en bounty2
2. ⚠️ **Añadir regla de firewall para N8n** (puerto 5678) en gpt-oss-20b
3. ⚠️ **Añadir regla de firewall para RAG API** (puerto 8000) en rag3, o confirmar que usa 5000
4. ⚠️ **Obtener IP externa de rag3** y actualizar configuración

## 🎯 Notas Importantes

- **Ollama NO es accesible directamente** desde el frontend. Debe usarse a través del backend integrado.
- El **backend principal** debe estar en **puerto 5000**, no 5001.
- **TTS** usa diferentes puertos según la VM: 5002 en bounty2, 5001 en gpt-oss-20b.

