// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo: 'http://localhost:5002'
    // En producción: URL de Vercel/Railway con SSL válido
    // IP REAL de la VM principal (según conexión actual a gpt-oss-20b)
    // Puerto 5000 confirmado como escuchando en esta VM
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://34.175.136.104:5000'  // Capibara6 Main Server en gpt-oss-20b
        : 'https://www.capibara6.com',   // Servidor en producción

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
