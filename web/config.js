// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // Usar dominio correcto con SSL válido
    BACKEND_URL: 'https://capibara6.com',
    
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
    }
};

