// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo: 'http://localhost:5001' (puerto correcto según documentación)
    // En producción: IP real del servidor bounty2 puerto 5001
    // Puerto 5001 es el puerto correcto para el backend Flask según documentación
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:5001'  // Puerto correcto para backend Flask (server_gptoss.py) en desarrollo
        : 'http://34.12.166.76:5001',   // Servidor en producción bounty2 puerto 5001

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
            ? 'http://localhost:5001/api/chat'  // Endpoint correcto para desarrollo
            : 'http://34.12.166.76:5001/api/chat',  // Endpoint correcto para producción
        max_tokens: 100,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 300000 // 5 minutos como recomienda la documentación
    }
};
