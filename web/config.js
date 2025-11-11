// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo: usar proxy local para evitar problemas CORS con backend remoto
    // En producción: IP real del servidor bounty2 puerto 5001
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:8001'  // Proxy local para evitar problemas CORS
        : 'http://34.12.166.76:5001',       // Servidor en producción bounty2 puerto 5001

    // Endpoints
    ENDPOINTS: {
        // Chat endpoints
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',

        // Conversaciones y leads
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',

        // Sistema
        HEALTH: '/api/health',
        MODELS: '/api/models',

        // MCP endpoints
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call'
    },

    // Configuración del modelo GPT-OSS-20B
    MODEL_CONFIG: {
        serverUrl: window.location.hostname === 'localhost'
            ? 'http://localhost:8001/api/chat'  // Usar proxy local para evitar problemas CORS
            : 'http://34.12.166.76:5001/api/chat',  // Endpoint correcto para producción
        max_tokens: 100,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 300000 // 5 minutos como recomienda la documentación
    }
};
