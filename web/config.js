// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo: 'http://localhost:5002'
    // En producción: URL de Vercel/Railway con SSL válido
    // IP REAL de la VM bounty2 donde está corriendo el backend de modelos
    // Puerto 5000 confirmado como escuchando (capibara6 Backend en 127.0.0.1:5000 y 10.164.0.9:5000)
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://34.12.166.76:5000'  // capibara6 Backend de modelos en bounty2 (puerto: 5000)
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
