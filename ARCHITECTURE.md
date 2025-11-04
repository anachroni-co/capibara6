# Arquitectura de Capibara6

## Visión General

Capibara6 es una aplicación de chat con IA que combina un frontend web moderno con un backend distribuido que ejecuta el modelo GPT-OSS-20B en Google Cloud.

## Componentes Principales

### 1. Frontend Web (`web/`)

**Tecnologías**: HTML5, CSS3, JavaScript ES6+

**Archivos clave**:
- `chat.html` - Interfaz principal del chat
- `chat-app.js` - Lógica del chat y comunicación con API
- `tts-integration.js` - Integración de síntesis de voz
- `smart-mcp-integration.js` - Integración de Smart MCP
- `entropy-auto-inject.js` - Sistema de entropía automática

**Características**:
- Interfaz responsive y moderna
- Integración con Web Speech API
- Sistema de clonación de voces
- Contexto inteligente con MCP
- Monitoreo de entropía en tiempo real

### 2. Backend Flask (`backend/`)

**Tecnologías**: Python 3.11+, Flask, Flask-CORS

**Servidores principales**:

#### Servidor Integrado (`capibara6_integrated_server.py`)
- **Puerto**: 5001
- **Función**: Proxy principal entre frontend y modelo GPT-OSS-20B
- **Endpoints**:
  - `POST /api/chat` - Procesamiento de mensajes
  - `GET /health` - Health check
  - `POST /api/tts/speak` - Proxy a TTS
  - `POST /api/mcp/analyze` - Proxy a MCP

#### Servidor TTS (`coqui_tts_server.py`)
- **Puerto**: 5002
- **Función**: Síntesis de voz con Coqui TTS
- **Características**:
  - Múltiples voces predefinidas
  - Clonación de voz
  - Fallback a Web Speech API

#### Servidor Smart MCP (`smart_mcp_server.py`)
- **Puerto**: 5003
- **Función**: Contexto inteligente para respuestas
- **Características**:
  - Análisis de contexto
  - Triggers inteligentes
  - Mejora de respuestas

### 3. Proxies de Vercel (`api/`)

**Tecnologías**: Node.js, Vercel Functions

**Archivos**:
- `chat.js` - Proxy para `/api/chat`
- `consensus/query.js` - Proxy para consenso
- `tts/speak.js` - Proxy para TTS
- `mcp/analyze.js` - Proxy para MCP

**Función**: Resolver problemas de CORS y Mixed Content entre HTTPS (Vercel) y HTTP (VM)

### 4. Modelo GPT-OSS-20B

**Ubicación**: Google Cloud VM (`gpt-oss-20b`)
- **Zona**: `europe-southwest1-b`
- **Proyecto**: `mamba-001`
- **Servidor**: llama-server en puerto 8080
- **Configuración**: Optimizada para producción

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

### 2. TTS Flow

```
Frontend → Vercel Proxy → VM TTS Server → Coqui TTS → Audio
        ← Frontend ← Vercel Proxy ← VM TTS Server ← Audio
```

### 3. MCP Flow

```
Frontend → Vercel Proxy → VM MCP Server → Análisis → Contexto
        ← Frontend ← Vercel Proxy ← VM MCP Server ← Contexto
```

## Configuración de Red

### Puertos

| Servicio | Puerto | Protocolo | Función |
|----------|--------|-----------|---------|
| Frontend | 8000 | HTTP | Desarrollo local |
| Backend Principal | 5001 | HTTP | Servidor integrado |
| TTS Server | 5002 | HTTP | Síntesis de voz |
| MCP Server | 5003 | HTTP | Contexto inteligente |
| GPT-OSS-20B | 8080 | HTTP | Modelo de IA |

### CORS

- **Orígenes permitidos**: `https://www.capibara6.com`, `http://localhost:8000`
- **Métodos**: GET, POST, OPTIONS
- **Headers**: Content-Type, Authorization

## Despliegue

### 1. Google Cloud VM (Backend)

```bash
# Conectar
gcloud compute ssh --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"

# Ejecutar servicios
python3 capibara6_integrated_server.py &
python3 coqui_tts_server.py &
python3 smart_mcp_server.py &
```

### 2. Vercel (Frontend)

- **Build Command**: `npm run build`
- **Output Directory**: `web`
- **Environment Variables**: Configuradas en Vercel Dashboard

### 3. Dominio

- **Frontend**: `https://www.capibara6.com`
- **API**: `https://www.capibara6.com/api/*`

## Monitoreo

### Logs

- **Backend**: `backend/logs/`
- **VM**: `/var/log/capibara6/`
- **Vercel**: Dashboard de Vercel

### Métricas

- **Throughput**: Tokens por segundo
- **Latencia**: Tiempo de respuesta
- **Uso de memoria**: RAM y VRAM
- **Utilización TPU**: Para fine-tuning

## Seguridad

### Autenticación

- **Frontend**: Sin autenticación (público)
- **Backend**: CORS configurado
- **VM**: SSH con claves

### Datos

- **Mensajes**: No se almacenan permanentemente
- **Voces**: Procesadas localmente
- **Modelo**: Ejecutado en VM privada

## Escalabilidad

### Horizontal

- **Frontend**: CDN de Vercel
- **Backend**: Múltiples instancias de VM
- **Modelo**: Distribución en múltiples GPUs/TPUs

### Vertical

- **VM**: Escalado automático de Google Cloud
- **Modelo**: Optimizaciones de memoria
- **TTS**: Caching de voces

## Troubleshooting

### Problemas Comunes

1. **CORS Error**: Verificar configuración de orígenes
2. **502 Bad Gateway**: Verificar que el backend esté ejecutándose
3. **TTS No Funciona**: Verificar Coqui TTS instalado
4. **MCP No Responde**: Verificar servidor MCP en puerto 5003

### Logs Importantes

- `backend/logs/capibara6.log` - Logs principales
- `backend/logs/errors.log` - Errores del sistema
- Vercel Function Logs - Errores de proxy

## Futuras Mejoras

### Corto Plazo

- [ ] Implementar autenticación de usuarios
- [ ] Mejorar sistema de clonación de voces
- [ ] Optimizar latencia del modelo

### Largo Plazo

- [ ] Implementar fine-tuning automático
- [ ] Añadir más modelos de IA
- [ ] Sistema de plugins
- [ ] API pública

---

**Última actualización**: Enero 2025
**Versión**: 2.0.0
