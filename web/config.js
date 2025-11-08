// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo: 'http://localhost:5000'
    // En producción: URL de Vercel/Railway con SSL válido
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:5000'
        : 'https://www.capibara6.com',

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
        max_tokens: 100,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 300000 // 5 minutos como recomienda la documentación
    }
};
