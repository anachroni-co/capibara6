# 🔥 Resumen de Configuración de Firewalls - Capibara6

## 📋 Puertos Abiertos por VM

### VM: **bounty2** (34.12.166.76)
**Puertos abiertos** (según configuración anterior):
- ✅ **5000, 5001** - Backend Capibara6
- ✅ **11434** - Ollama API
- ✅ **22** - SSH

### VM: **gpt-oss-20b** (34.175.136.104)
**Puertos abiertos** (según firewall):
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
**Puertos abiertos** (según firewall):
- ✅ **5000** - Capibara6 Integrated Server
- ✅ **5001** - Kyutai TTS Server
- ✅ **8080** - llama.cpp Server / CapibaraGPT-v2 GUI
- ✅ **11434** - Ollama API
- ✅ **443** - HTTPS
- ✅ **22** - SSH
- ✅ **7001** - Nebula Graph Studio

**Puertos NO abiertos**:
- ❌ **8000** - RAG API (necesita regla de firewall o usar puerto 5000)

## 🔧 Configuración Actualizada

### TTS
- **gpt-oss-20b**: Puerto **5001** (Kyutai TTS Server) ✅
- **rag3**: Puerto **5001** (Kyutai TTS Server) ✅

### MCP
- **gpt-oss-20b**: Puerto **5003** (Smart MCP Server) ✅
- **Backend principal**: A través de bounty2:5001 (integrado) ✅

### RAG API
- **rag3**: Usar puerto **5000** (Capibara6 Integrated Server) hasta que se abra 8000
- O añadir regla de firewall para puerto 8000

### N8n
- **gpt-oss-20b**: Puerto **5678** NO está abierto
- **Solución**: Añadir regla de firewall o verificar si está en otro puerto

## 📝 Acciones Recomendadas

1. ✅ **TTS**: Actualizado a puerto 5001 en `web/config.js`
2. ✅ **MCP**: Ya configurado para puerto 5003
3. ⚠️ **RAG API**: Actualizado a puerto 5000 (temporal, hasta abrir 8000)
4. ⚠️ **N8n**: Verificar puerto o añadir regla de firewall para 5678
5. ⚠️ **Obtener IP de rag3**: Necesario para completar configuración

## 🎯 Próximos Pasos

1. Obtener IP externa de rag3
2. Verificar qué servicios están realmente corriendo en cada puerto
3. Añadir reglas de firewall si es necesario:
   - Puerto 8000 en rag3 para RAG API
   - Puerto 5678 en gpt-oss-20b para N8n

