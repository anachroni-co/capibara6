// Configuración del chatbot capibara6 con GPT-OSS-20B

const CHATBOT_CONFIG = {
    // URL del backend
    // Conectar directamente con la VM donde está todo el sistema
    BACKEND_URL: window.location.hostname === 'localhost' 
        ? 'http://34.175.215.109:5000'
        : 'http://34.175.215.109:5000',
    
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

