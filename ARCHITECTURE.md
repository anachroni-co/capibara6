# Arquitectura de Capibara6

## Visión General

Capibara6 es una aplicación de chat con IA que combina un frontend web moderno con un backend distribuido que ejecuta el modelo GPT-OSS-20B en Google Cloud. Incluye integración avanzada de Kyutai TTS con optimización de tokens mediante TOON.

## Componentes Principales

### 1. Frontend Web (`web/`)

**Tecnologías**: HTML5, CSS3, JavaScript ES6+

**Archivos clave**:
- `chat.html` - Interfaz principal del chat
- `chat-app.js` - Lógica del chat y comunicación con API
- `tts-integration.js` - Integración de síntesis de voz Kyutai
- `smart-mcp-integration.js` - Integración de Smart MCP
- `entropy-auto-inject.js` - Sistema de entropía automática

**Características**:
- Interfaz responsive y moderna
- Integración con Web Speech API (fallback)
- Sistema de clonación de voces con Kyutai TTS
- Contexto inteligente con MCP
- Monitoreo de entropía en tiempo real
- Soporte para TOON (Token-Oriented Object Notation)

### 2. Backend Flask (`backend/`)

**Tecnologías**: Python 3.11+, Flask, Flask-CORS

**Servidores principales**:

#### Servidor Integrado (`capibara6_integrated_server.py`)
- **Puerto**: 5001
- **Función**: Proxy principal entre frontend y modelo GPT-OSS-20B con Kyutai TTS integrado
- **Endpoints**:
  - `POST /api/chat` - Procesamiento de mensajes
  - `GET /health` - Health check
  - `POST /api/tts/speak` - Servicio Kyutai TTS integrado
  - `POST /api/tts/clone` - Clonación de voz con Kyutai
  - `GET /api/tts/voices` - Lista de voces disponibles
  - `POST /api/tts/preload` - Precarga de modelo Kyutai
  - `GET /api/tts/stats` - Estadísticas de TTS
  - `POST /api/mcp/context` - Análisis de contexto inteligente

#### Servidor Kyutai TTS (`kyutai_tts_server.py`)
- **Puerto**: 5001 (integrado) / 5002 (backup)
- **Función**: Síntesis de voz con Kyutai TTS
- **Características**:
  - Voces de alta calidad con control emocional
  - Clonación de voz avanzada
  - Soporte multilingüe (8+ idiomas)
  - Optimización de recursos
  - Fallback a Web Speech API

#### Servidor Smart MCP (`smart_mcp_server.py`)
- **Puerto**: 5003
- **Función**: Contexto inteligente para respuestas
- **Características**:
  - Análisis de contexto
  - Triggers inteligentes
  - Mejora de respuestas
  - Integración con TOON para eficiencia de tokens

### 3. Proxies de Vercel (`api/`)

**Tecnologías**: Node.js, Vercel Functions

**Archivos**:
- `chat.js` - Proxy para `/api/chat`
- `tts/speak.js` - Proxy para `/api/tts/speak`
- `tts/clone.js` - Proxy para `/api/tts/clone`
- `mcp/analyze.js` - Proxy para MCP

**Función**: Resolver problemas de CORS y Mixed Content entre HTTPS (Vercel) y HTTP (VM) con soporte para TOON.

### 4. Modelo GPT-OSS-20B

**Ubicación**: Google Cloud VM (`gpt-oss-20b`)
- **Zona**: `europe-southwest1-b`
- **Proyecto**: `mamba-001`
- **Servidor**: llama-server en puerto 8080
- **Configuración**: Optimizada para producción con soporte TOON

### 5. Fine-tuning (`fine-tuning/`)

**Tecnologías**: T5X, SeqIO, JAX, Flax

**Estructura**:
```
fine-tuning/
├── configs/           # Configuraciones T5X
├── scripts/           # Scripts de entrenamiento
├── datasets/          # Configuración SeqIO
└── t5x/              # Código T5X existente
```

**Función**: Entrenamiento y fine-tuning del modelo GPT-OSS-20B

## Flujo de Datos

### 1. Chat Flow

```
Usuario → Frontend → Vercel Proxy → VM Backend → GPT-OSS-20B
       ← Frontend ← Vercel Proxy ← VM Backend ← GPT-OSS-20B
```

### 2. TTS Flow (Kyutai TTS)

```
Frontend → Vercel Proxy → VM Backend → Kyutai TTS → Audio
        ← Frontend ← Vercel Proxy ← VM Backend ← Audio
```

### 3. MCP Flow

```
Frontend → Vercel Proxy → VM MCP Server → Análisis → Contexto
        ← Frontend ← Vercel Proxy ← VM MCP Server ← Contexto
```

### 4. TOON Flow (Optimización de Tokens)

```
Frontend → TOON Format → Backend → Modelos IA → TOON Response
        ← JSON Fallback ← Backend ← Modelos IA ← TOON Response
```

## Configuración de Red

### Puertos

| Servicio | Puerto | Protocolo | Función |
|----------|--------|-----------|---------|
| Frontend | 8000 | HTTP | Desarrollo local |
| Backend Principal | 5001 | HTTP | Servidor integrado con Kyutai TTS |
| MCP Server | 5003 | HTTP | Contexto inteligente |
| GPT-OSS-20B | 8080 | HTTP | Modelo de IA |

### CORS

- **Orígenes permitidos**: `https://www.capibara6.com`, `http://localhost:8000`
- **Métodos**: GET, POST, OPTIONS
- **Headers**: Content-Type, Authorization
- **TOON Support**: Application/toon, text/plain

## Despliegue

### 1. Google Cloud VM (Backend)

````
# Conectar
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Ejecutar servicios
python3 capibara6_integrated_server.py &
python3 smart_mcp_server.py &
```

### 2. Vercel (Frontend)

- **Build Command**: `npm run build`
- **Output Directory**: `web`
- **Environment Variables**: Configuradas en Vercel Dashboard
- **TOON Support**: API Functions con soporte para TOON

### 3. Dominio

- **Frontend**: `https://www.capibara6.com`
- **API**: `https://www.capibara6.com/api/*`

## Monitoreo

### Logs

- **Backend**: `backend/logs/`
- **VM**: `/var/log/capibara6/`
- **Vercel**: Dashboard de Vercel

### Métricas

- **Throughput**: Tokens por segundo (con optimización TOON)
- **Latencia**: Tiempo de respuesta (mejorado con Kyutai TTS)
- **Uso de memoria**: RAM y VRAM
- **Utilización TPU**: Para fine-tuning

## Seguridad

### Autenticación

- **Frontend**: Sin autenticación (público)
- **Backend**: CORS configurado
- **VM**: SSH con claves

### Datos

- **Mensajes**: No se almacenan permanentemente
- **Voces**: Procesadas localmente (Kyutai TTS)
- **Modelo**: Ejecutado en VM privada
- **TOON**: Seguro, compatible con JSON existente

## Escalabilidad

### Horizontal

- **Frontend**: CDN de Vercel
- **Backend**: Múltiples instancias de VM
- **Modelo**: Distribución en múltiples GPUs/TPUs

### Vertical

- **VM**: Escalado automático de Google Cloud
- **Modelo**: Optimizaciones de memoria
- **TTS**: Caching de voces de Kyutai
- **TOON**: Reducción de tokens para mayor contexto

## Troubleshooting

### Problemas Comunes

1. **CORS Error**: Verificar configuración de orígenes
2. **502 Bad Gateway**: Verificar que el backend esté ejecutándose
3. **TTS No Funciona**: Verificar Kyutai TTS instalado (reemplaza Coqui)
4. **MCP No Responde**: Verificar servidor MCP en puerto 5003
5. **TOON Errors**: Verificar formato TOON con JSON fallback

### Logs Importantes

- `backend/logs/capibara6.log` - Logs principales
- `backend/logs/errors.log` - Errores del sistema
- Vercel Function Logs - Errores de proxy
- `backend/logs/tts.log` - Logs de Kyutai TTS

## Futuras Mejoras

### Corto Plazo

- [ ] Implementar autenticación de usuarios
- [ ] Mejorar sistema de clonación de voces Kyutai
- [ ] Optimizar latencia del modelo con TOON

### Largo Plazo

- [ ] Implementar fine-tuning automático
- [ ] Añadir más modelos de IA
- [ ] Sistema de plugins
- [ ] API pública con soporte TOON

---

**Última actualización**: Noviembre 2025
**Versión**: 3.0.0
**Integración Kyutai TTS**: Completa
**TOON Support**: Implementado