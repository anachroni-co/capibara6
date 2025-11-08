// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
<<<<<<< HEAD
    // Usar dominio correcto con SSL válido y www
    BACKEND_URL: 'https://www.capibara6.com',
    
    // Endpoints
    ENDPOINTS: {
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        SAVE_CONVERSATION: '/api/save-conversation',
        HEALTH: '/api/health',
        MODELS: '/api/models'
    },
    
    // Configuración del modelo GPT-OSS-20B
    MODEL_CONFIG: {
        max_tokens: 100,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 300000 // 5 minutos como recomienda la documentación
=======
    // En desarrollo: 'http://localhost:5000'
    // En producción: URL de Railway
    BACKEND_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000'
        : 'https://www.capibara6.com',
    // Endpoints
    ENDPOINTS: {
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        HEALTH: '/api/health',
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call'
>>>>>>> 0d79365 (add web files)
    }
};

