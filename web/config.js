// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // Usar servidor local en lugar del dominio
    BACKEND_URL: 'http://localhost:5001',

    // Endpoints
    ENDPOINTS: {
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',  // Si está disponible
        SAVE_CONVERSATION: '/api/save-conversation',
        HEALTH: '/health',  // Endpoint de salud del backend
        MODELS: '/api/models',
        TTS_SPEAK: '/api/tts/speak',      // Para síntesis de voz
        TTS_VOICES: '/api/tts/voices',    // Para listar voces
        MCP_CONTEXT: '/api/mcp/context',  // Para contexto inteligente
        E2B_EXECUTE: '/api/e2b/execute'   // Para ejecución E2B (si está disponible)
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
        RESPONSE: 120000     // 2 minutos
    },

    // Headers para todas las peticiones
    HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
};