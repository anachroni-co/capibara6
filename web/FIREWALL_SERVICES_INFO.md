# 🚀 Conexión del Frontend a las VMs Reales - SERVICIOS ACTUALES

## 📊 Servicios Disponibles en VM (IP: 34.175.215.109)

Según el análisis del firewall proporcionado, estos son los servicios reales disponibles:

### 🔑 Puertos Abiertos en Firewall

| Puerto | Servicio | Descripción | Estado |
|--------|----------|-------------|---------|
| **5000** | `tcp:5000` | Capibara6 Main Server | ✅ Disponible |
| **5003** | `tcp:5003` | Smart MCP Server | ✅ Disponible |
| **5010** | `tcp:5010` | Smart MCP Server (alternativo) | ✅ Disponible |
| **8080** | `tcp:8080` | Llama Server (modelo gpt-oss-20b) | ✅ Disponible |

### 🏗️ Arquitectura de Servicios Real

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                 │
│                       (Local/Web)                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTPS/HTTP
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CAPIBARA6 VM REAL                            │
│                       34.175.215.109                           │
├─────────────────────────────────────────────────────────────────┤
│  MAIN SERVER (puerto 5000)                                     │
│  ├─ Chat endpoints                                              │
│  ├─ Save conversation/lead                                      │
│  ├─ System health                                               │
│  └─ MCP integration                                             │
│                                                                 │
│  SMART MCP SERVER (puerto 5003)                                │
│  ├─ MCP status                                                  │
│  ├─ MCP tools/list                                              │
│  ├─ MCP tools/call                                              │
│  └─ Context analysis                                            │
│                                                                 │
│  SMART MCP SERVER (puerto 5010)                                │
│  ├─ MCP analyze                                                 │
│  └─ Advanced features                                           │
│                                                                 │
│  LLAMA SERVER (puerto 8080)                                    │
│  ├─ Model: gpt-oss-20b                                          │
│  ├─ Endpoints: /completion, /health                             │
│  └─ High-performance                                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🌐 Configuración de Conexión Actualizada

### Servidores Disponibles

#### 1. Capibara6 Main Server (Recomendado para frontend)
- **IP**: `34.175.215.109`
- **Puerto**: `5000`
- **Endpoints**:
  - `POST /api/chat` - Chat principal
  - `POST /api/save-conversation` - Guardar conversaciones
  - `POST /api/save-lead` - Guardar leads
  - `GET /api/health` - Verificación de salud
  - `POST /api/mcp/tools/call` - Integración MCP

#### 2. Smart MCP Server (Para contexto y herramientas)
- **IP**: `34.175.215.109`
- **Puerto**: `5003`
- **Endpoints**:
  - `GET /api/mcp/status` - Estado del MCP
  - `POST /api/mcp/tools/call` - Llamadas a herramientas MCP
  - `GET /api/mcp/tools/list` - Listado de herramientas

#### 3. Smart MCP Server (Puerto Alternativo)
- **IP**: `34.175.215.109`
- **Puerto**: `5010`
- **Endpoints**:
  - `POST /api/mcp/analyze` - Análisis inteligente

#### 4. Llama Server (Modelo gpt-oss-20b)
- **IP**: `34.175.215.109`
- **Puerto**: `8080`
- **Endpoints**:
  - `POST /completion` - Generación de texto
  - `GET /health` - Estado del modelo

## 🔧 Configuración del Frontend con IPs Reales

### Recomendaciones de Uso

#### Para desarrollo local:
- **Chat principal**: `http://34.175.215.109:5000`
- **MCP Services**: `http://34.175.215.109:5003`
- **Llama Server**: `http://34.175.215.109:8080`

#### Ejemplos de conexión:

```javascript
// Configuración para desarrollo local
const DEV_CONFIG = {
    // Servidor principal para chat
    CHAT_SERVER: 'http://34.175.215.109:5000',  // Capibara6 Main Server
    
    // Servicios de contexto MCP
    MCP_SERVER_5003: 'http://34.175.215.109:5003',  // Smart MCP
    MCP_SERVER_5010: 'http://34.175.215.109:5010',  // Smart MCP (alternativo)
    
    // Servidor del modelo
    MODEL_SERVER: 'http://34.175.215.109:8080',   // gpt-oss-20b
};
```

## 🔍 Verificación de Servicios

### Comandos para verificar disponibilidad:

```bash
# Verificar servidor principal
curl -X POST http://34.175.215.109:5000/api/health

# Verificar MCP en puerto 5003
curl -X GET http://34.175.215.109:5003/api/mcp/status

# Verificar MCP en puerto 5010
curl -X POST http://34.175.215.109:5010/api/mcp/analyze -H 'Content-Type: application/json' -d '{"query":"test"}'

# Verificar servidor de modelo
curl -X GET http://34.175.215.109:8080/health
```

## 📞 Soporte

- **IP Principal**: `34.175.215.109`
- **Puerto Principal**: `5000` - Capibara6 Main Server
- **Puerto MCP**: `5003` - Smart MCP Server
- **Puerto Modelo**: `8080` - gpt-oss-20b

¡Tu frontend está ahora configurado con las IPs y puertos reales de la VM!