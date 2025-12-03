# Arquitectura de Producción - Capibara6

## Descripción General

Sistema distribuido en 3 VMs que comparten la misma subred de GCloud:

- **models-europe** (34.175.48.2): VM dedicada a modelos de IA y cómputo
- **services** (34.175.255.139): VM dedicada a servicios de backend y coordinación
- **frontend**: VM o servicio web que consume la API

## ⚠️ Guía para Agentes - Servicios por VM

### VM models-europe (esta VM)
**SOLO** debe ejecutar:
- ✅ `multi_model_server.py` (servidor de modelos vLLM con router semántico)
- ✅ 5 modelos de IA especializados con optimizaciones ARM-Axion
- ✅ Soporte para lazy loading de modelos

**NO debe ejecutar**:
- ❌ `mcp_server.py`, `smart_mcp_server.py` (corren en services)
- ❌ `kyutai_tts_server.py`, `coqui_tts_server.py` (corren en services)
- ❌ `capibara6_integrated_server.py` (corre en services)

### VM services
**SOLO** debe ejecutar:
- ✅ `capibara6_integrated_server.py` (backend principal)
- ✅ `mcp_server.py` (Model Context Protocol)
- ✅ `kyutai_tts_server.py` (Text-to-Speech)
- ✅ `smart_mcp_server.py` (alternativa MCP)

**NO debe ejecutar**:
- ❌ `multi_model_server.py` (corre en models-europe)

## Comunicación entre VMs

## Distribución de Servicios

### VM models-europe (34.175.48.2)
**Propósito:** Ejecución de modelos de IA, cómputo intensivo, E2B (por rendimiento)

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| 8082 | vLLM Multi-Model Server | Servidor de 5 modelos ARM-Axion |
| - | E2B Execution | Ejecución más rápida de sandboxes E2B aquí |

### VM services (34.175.255.139) 
**Propósito:** Coordinación de servicios, MCP, integración con frontend

| Puerto | Servicio | Descripción |
|--------|----------|-------------|
| 5000 | Main API Server | Backend principal |
| 5003 | MCP Server | Model Context Protocol |
| 5002 | TTS Server | Text-to-Speech |
| 5010 | Smart MCP | Alternativa ligera |
| 5678 | N8n | Automation workflows |

### Comunicación entre VMs

#### De services a models-europe:
- `http://34.175.48.2:8082/v1/chat/completions` - API de modelos
- `http://34.175.48.2:8082/v1/models` - Listado de modelos
- Para E2B que se ejecuta en models-europe: coordinador en services llama a models-europe

#### De frontend a services:
- `http://34.175.255.139:5000/api/chat` - Endpoint principal de chat
- `http://34.175.255.139:5003/api/mcp/status` - Estado de MCP

## Configuración Correcta

### En VM services:
```bash
# Servidor backend principal
python3 capibara6_integrated_server.py  # Corre en 5000 ó 5001

# Servidor MCP 
python3 mcp_server.py  # Corre en 5003

# Coordinador E2B
# (Este se comunica con models-europe para ejecución)
```

### En VM models-europe (esta VM):
```bash
# Servidor de modelos
python3 multi_model_server.py  # Corre en 8082

# E2B puede ejecutarse aquí para mayor velocidad
```

## Notas Importantes

1. No usar `localhost` o `127.0.0.1` en producción
2. Usar IPs públicas o internas según la configuración de red
3. Asegurar conectividad entre VMs a través del firewall
4. E2B se ejecuta en models-europe por rendimiento pero se coordina desde services
5. El frontend solo se comunica con la VM services