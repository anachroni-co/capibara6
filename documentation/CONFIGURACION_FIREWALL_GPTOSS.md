# 🔥 Configuración de Firewall - VM gpt-oss-20b

## ✅ Puertos Abiertos según Firewall

| Puerto | Servicio | Regla de Firewall | Estado |
|--------|----------|-------------------|--------|
| **5000** | Capibara6 Main Server | `allow-capibara6-main`, `allow-capibara6-port5000` | ✅ ABIERTO |
| **5001** | Kyutai TTS Server | `allow-kyutai-tts` | ✅ ABIERTO |
| **5003** | Smart MCP Server | `allow-smart-mcp` | ✅ ABIERTO |
| **8080** | Gemma Model Server / CapibaraGPT-v2 GUI | `allow-gemma-model`, `allow-capibara-gui` | ✅ ABIERTO |
| **80** | HTTP | `allow-http-llama` | ✅ ABIERTO |
| **443** | HTTPS | `allow-capibara6-https` | ✅ ABIERTO |
| **22** | SSH | `allow-ssh` | ✅ ABIERTO |
| **7001** | Nebula Graph Studio | `allow-nebula-studio` | ✅ ABIERTO |

## ❌ Puertos NO Abiertos (según firewall)

- **5002** - TTS (NO hay regla, usar 5001 en su lugar)
- **5010** - MCP alternativo (NO hay regla, usar 5003 en su lugar)
- **5678** - N8n (NO hay regla, necesita añadirse o usar otro puerto)

## 🔧 Correcciones Necesarias

### 1. TTS: Cambiar de puerto 5002 → 5001
El firewall tiene abierto el puerto **5001** para Kyutai TTS Server, no el 5002.

### 2. MCP: Usar puerto 5003 (ya correcto)
El puerto **5003** está abierto para Smart MCP Server según la regla `allow-smart-mcp`.

### 3. N8n: Verificar puerto o añadir regla
El puerto **5678** no está abierto. Necesita:
- Añadir regla de firewall, O
- Usar otro puerto que esté abierto, O
- Verificar si N8n está corriendo en otro puerto

### 4. Servidor Principal: Puerto 5000 (correcto)
El puerto **5000** está abierto para Capibara6 Main Server.

## 📝 Cambios a Realizar

1. Actualizar `web/config.js` para usar puerto 5001 para TTS
2. Confirmar que MCP usa puerto 5003 (ya está correcto)
3. Verificar configuración de N8n

