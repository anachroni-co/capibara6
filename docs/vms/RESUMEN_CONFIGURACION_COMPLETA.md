# 📋 Resumen de Configuración Completa - Capibara6

## 🌐 Arquitectura de VMs en GCloud

### VM 1: bounty2 (Backend + Ollama)
- **IP**: `34.12.166.76`
- **Zona**: europe-west4-a
- **Puerto Backend**: 5001
- **Puerto Ollama**: 11434
- **Servicios**:
  - Backend Flask integrado con CORS
  - Ollama con 3 modelos: `gpt-oss-20B`, `mixtral`, `phi-mini3`
- **SSH**: `gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"`

### VM 2: gpt-oss-20b (Servicios Principales)
- **IP**: `34.175.136.104`
- **Zona**: europe-southwest1-b
- **Puertos**:
  - 5000: Servidor principal
  - 5003: MCP Server
  - 5010: MCP Server alternativo
  - 5678: N8n
  - 8080: Llama Server
- **Servicios**:
  - Smart MCP
  - TTS (Text-to-Speech)
  - N8n (Automatización)
  - Bridge
- **SSH**: `gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"`

### VM 3: rag3 (Base de Datos RAG)
- **IP**: `34.105.131.8`
- **Zona**: europe-west2-c
- **Puerto**: 8000
- **Servicios**:
  - RAG Server (Retrieval-Augmented Generation)
  - API REST para mensajes, archivos y búsqueda
- **SSH**: `gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"`

## 🔧 Configuración del Frontend

### Archivo: `web/config.js`

```javascript
const CHATBOT_CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://34.12.166.76:5001'  // VM bounty2 en desarrollo
        : 'https://www.capibara6.com',
    
    VMS: {
        GPT_OSS_20B: {
            ip: '34.175.136.104',
            services: {
                main: 'http://34.175.136.104:5000',
                mcp: 'http://34.175.136.104:5003',
                mcpAlt: 'http://34.175.136.104:5010',
                model: 'http://34.175.136.104:8080'
            }
        },
        BOUNTY2: {
            ip: '34.12.166.76',
            services: {
                ollama: 'http://34.12.166.76:11434',
                backend: 'http://34.12.166.76:5001'
            }
        },
        RAG3: {
            ip: '34.105.131.8',
            services: {
                rag: 'http://34.105.131.8:8000',
                api: 'http://34.105.131.8:8000/api'
            }
        }
    }
};
```

## 🚀 Iniciar Servicios

### bounty2 (Backend)

```bash
# SSH a la VM
gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"

# Navegar al directorio
cd /path/to/capibara6/backend

# Iniciar backend con screen
screen -S capibara6-backend
python3 capibara6_integrated_server.py
# Ctrl+A, D para desconectar

# Verificar
curl http://localhost:5001/health
```

### gpt-oss-20b (MCP y Servicios)

```bash
# SSH a la VM
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Iniciar Smart MCP
screen -S smart-mcp
cd /path/to/smart-mcp
python3 server.py --port 5010
# Ctrl+A, D

# Iniciar N8n
screen -S n8n
n8n start --port 5678
# Ctrl+A, D

# Verificar servicios
curl http://localhost:5010/health
curl http://localhost:5678
```

### rag3 (RAG Server)

```bash
# SSH a la VM
gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"

# Iniciar RAG Server
screen -S rag-service
cd /path/to/rag/service
python3 app.py --port 8000
# Ctrl+A, D

# Verificar
curl http://localhost:8000/health
```

## 🧪 Verificación de Conexiones

### Desde Local (Scripts)

```bash
# Test de bounty2 (backend)
./scripts/check_bounty2_status.sh

# Test de rag3
./scripts/test_rag3_connection.sh

# Test de MCP en gpt-oss-20b
./scripts/check_mcp_status.sh

# Test completo de todas las VMs
./scripts/test_vm_connectivity.sh
```

### Desde el Navegador (Frontend)

```bash
# Iniciar servidor local
cd web
python3 -m http.server 8000

# Abrir en navegador
# http://localhost:8000/chat.html
```

**En la consola del navegador:**

```javascript
// Verificar configuración
console.log(CHATBOT_CONFIG);

// Test de conexión RAG
await window.ragIntegration.checkConnection();

// Test de guardado de mensaje
await window.ragIntegration.saveMessage('user', 'Test message');
```

## 🔍 Endpoints Principales

### Backend (bounty2:5001)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Estado del servidor |
| `/api/health` | GET | Estado del servidor (alternativo) |
| `/api/ai/classify` | POST | Clasificar tarea con CTM |
| `/api/ai/generate` | POST | Generar texto con Ollama |
| `/api/save-conversation` | POST | Guardar conversación |
| `/api/save-lead` | POST | Guardar lead |

### RAG (rag3:8000)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Estado del servicio |
| `/api/messages` | POST | Guardar mensaje |
| `/api/files` | POST | Guardar archivo |
| `/api/search/semantic` | POST | Búsqueda semántica |
| `/api/search/rag` | POST | Búsqueda RAG |

### MCP (gpt-oss-20b:5010)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Estado del servicio |
| `/api/mcp/analyze` | POST | Analizar con MCP |
| `/api/mcp/status` | GET | Estado de MCP |
| `/api/mcp/tools/call` | POST | Llamar herramienta MCP |

## 🔐 Configuración de Firewall

Asegúrate de que los siguientes puertos estén abiertos en GCloud:

```bash
# bounty2
- Puerto 5001 (Backend)
- Puerto 11434 (Ollama)

# gpt-oss-20b
- Puerto 5000 (Main server)
- Puerto 5003 (MCP)
- Puerto 5010 (MCP Alt)
- Puerto 5678 (N8n)
- Puerto 8080 (Llama)

# rag3
- Puerto 8000 (RAG)
```

## 📝 Archivos Modificados

### Frontend
- `web/config.js`: Configuración centralizada con IPs de las 3 VMs
- `web/chat-page.js`: Método `checkConnection()` mejorado con múltiples fallbacks
- `web/chat-app.js`: Integración con RAG y backend
- `web/rag-integration.js`: Clase para gestionar conexión con RAG
- `web/smart-mcp-integration.js`: Integración con Smart MCP

### Backend
- `backend/capibara6_integrated_server.py`: CORS configurado, endpoints añadidos
- `backend/server.py`: CORS configurado
- `backend/env.example`: URLs actualizadas
- `model_config.json`: Endpoint de Ollama actualizado

### Scripts
- `scripts/test_rag3_connection.sh`: Test de conexión con RAG3
- `scripts/check_bounty2_status.sh`: Verificar estado de bounty2
- `scripts/check_and_restart_bounty2.sh`: Reiniciar servicios en bounty2
- `scripts/reiniciar_backend_con_cors.sh`: Reiniciar backend con CORS
- `scripts/check_mcp_status.sh`: Verificar estado del MCP Server en gpt-oss-20b

### Documentación
- `CONFIGURACION_RAG3.md`: Configuración completa de RAG3
- `SOLUCION_CORS.md`: Solución de problemas CORS
- `SOLUCION_ERROR_TOON_JSON.md`: Solución de errores de parsing TOON/JSON
- `BUGFIXES_APLICADOS.md`: Lista de bugs corregidos

## ✅ Checklist Final

### Backend (bounty2)
- [x] IP obtenida: `34.12.166.76`
- [x] CORS configurado en Flask
- [x] Endpoints `/api/ai/classify` y `/api/ai/generate` funcionando
- [x] Middleware global para OPTIONS requests
- [ ] Servicio corriendo y verificado

### Servicios (gpt-oss-20b)
- [x] IP obtenida: `34.175.136.104`
- [ ] Smart MCP corriendo en puerto 5010 (⚠️ DEBE estar en gpt-oss-20b, NO en bounty2)
- [ ] N8n corriendo en puerto 5678
- [ ] TTS configurado y funcionando

### RAG (rag3)
- [x] IP obtenida: `34.105.131.8`
- [x] Configuración en frontend actualizada
- [x] Integración RAG implementada
- [ ] Servicio RAG corriendo en puerto 8000
- [ ] Test de guardado de mensajes exitoso

### Frontend
- [x] Configuración centralizada en `config.js`
- [x] Método `checkConnection()` mejorado
- [x] Headers `Accept: application/json` añadidos
- [x] Integración RAG implementada
- [x] Bugs de configuración corregidos

## 🚦 Próximos Pasos

1. **Verificar servicios corriendo en las VMs**:
   ```bash
   # bounty2
   gcloud compute ssh --zone "europe-west4-a" "bounty2" --project "mamba-001"
   ps aux | grep capibara6_integrated_server
   
   # gpt-oss-20b
   gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
   ps aux | grep smart-mcp
   
   # rag3
   gcloud compute ssh --zone "europe-west2-c" "rag3" --project "mamba-001"
   ps aux | grep rag
   ```

2. **Ejecutar tests de conexión**:
   ```bash
   ./scripts/test_rag3_connection.sh
   ./scripts/check_bounty2_status.sh
   ```

3. **Probar frontend localmente**:
   ```bash
   cd web
   python3 -m http.server 8000
   # Abrir http://localhost:8000/chat.html
   ```

4. **Verificar en consola del navegador**:
   - Conexión con backend
   - Conexión con RAG
   - Envío de mensajes
   - Guardado en RAG

5. **Configurar firewall si es necesario**:
   ```bash
   gcloud compute firewall-rules list --project=mamba-001
   ```

## 📚 Documentación Adicional

- `ARCHITECTURE.md`: Arquitectura del proyecto
- `API_KEYS_GUIDE.md`: Guía de configuración de API keys
- `REAL_ARCHITECTURE.md`: Arquitectura real descubierta en las VMs
- `VM_CONNECTION_SETUP.md`: Setup de conexión con VMs
- `SOLUCION_CORS.md`: Solución técnica de CORS
- `SOLUCION_ERROR_TOON_JSON.md`: Solución de errores TOON
- `BUGFIXES_APLICADOS.md`: Lista de bugs corregidos

## 🆘 Soporte

Si encuentras problemas:

1. Revisa los logs de cada servicio
2. Verifica que los puertos estén abiertos
3. Confirma que los servicios estén corriendo
4. Revisa la configuración de firewall en GCloud
5. Consulta la documentación específica de cada componente

