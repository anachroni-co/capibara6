// Configuración del chatbot capibara6 con GPT-OSS-20B

// Detectar si estamos en localhost o en producción
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

// URLs de las VMs de Google Cloud
const VM_MODELS = 'http://34.12.166.76';      // VM de modelos (bounty)
const VM_SERVICES = 'http://34.175.136.104';   // VM de servicios (TTS, MCP, N8N)

const CHATBOT_CONFIG = {
    // URL del backend - cambiar según entorno
    BACKEND_URL: isLocalhost ? 'http://localhost:5001' : VM_MODELS + ':5001',

    // Endpoints
    ENDPOINTS: {
        CHAT: '/api/v1/query',  // Usando el endpoint principal
        CHAT_STREAM: '/api/v1/chat/stream',  // Si está disponible
        SAVE_CONVERSATION: '/api/v1/conversations/save',  // Endpoint actualizado
        HEALTH: '/health',  // Endpoint de salud del backend
        MODELS: '/api/v1/models',
        TTS_SPEAK: '/api/tts/speak',      // Para síntesis de voz
        TTS_VOICES: '/api/tts/voices',    // Para listar voces
        MCP_CONTEXT: '/api/v1/mcp/context',  // Para contexto inteligente
        MCP_STATUS: '/api/v1/mcp/status',  // Endpoint de estado MCP
        E2B_EXECUTE: '/api/v1/e2b/execute'   // Endpoint actualizado para E2B
    },

    // Configuración del modelo GPT-OSS-20B
    MODEL_CONFIG: {
        max_tokens: 100,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 300000 // 5 minutos como recomienda la documentación
    },

    // Configuración de timeouts
    TIMEOUTS: {
        REQUEST: 30000,      // 30 segundos
        CONNECTION: 5000,    // 5 segundos
        RESPONSE: 120000,    // 2 minutos
        MCP_HEALTH: 5000     // 5 segundos para health check MCP
    },

    // Headers para todas las peticiones
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    },

    // Servicios opcionales (configurar si deben usarse o no)
    SERVICES: {
        MCP_ENABLED: false,  // Deshabilitado por defecto ya que no está corriendo en el servidor actual
        TTS_ENABLED: true,
        E2B_ENABLED: true
    },

    // URLs de VMs para servicios externos
    VMS: {
        MODELS: VM_MODELS,          // 34.12.166.76 - VM de modelos (bounty)
        SERVICES: VM_SERVICES       // 34.175.136.104 - VM de servicios
    }
};