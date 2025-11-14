// Configuración de desarrollo para conectar al backend en VMs
// Este archivo sobreescribe la configuración predeterminada para entorno local
// Cuando trabajamos localmente, nos conectamos a la VM remota

const CHATBOT_CONFIG = {
    // URL del backend en la VM de Capibara6 (usado cuando estamos en localhost)
    BACKEND_URL: 'http://34.175.136.104:5001',  // IP de la VM de Capibara6 en puerto 5001

    // Endpoints
    ENDPOINTS: {
        // Chat endpoints
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        
        // Endpoints específicos de MCP
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        MCP_ANALYZE: '/api/mcp/analyze',
        
        // Conversaciones y leads
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        
        // Sistema
        HEALTH: '/api/health',
        MODELS: '/api/models',
        
        // TTS endpoints (si están disponibles)
        TTS_SPEAK: '/api/tts/speak',
        TTS_VOICES: '/api/tts/voices'
    },

    // Configuración del modelo
    MODEL_CONFIG: {
        max_tokens: 200,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 120000 // 2 minutos
    }
};

console.log('🔧 Configuración de conexión a VM cargada');
console.log('🔗 Backend URL:', CHATBOT_CONFIG.BACKEND_URL);
console.log('📡 Conectando a la VM remota desde entorno local');