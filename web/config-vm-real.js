// Configuración de desarrollo para conectar al backend en VMs reales
// Basado en los comandos de gcloud proporcionados
// VM "gpt-oss-20b" en europe-southwest1-b -> modelo GPT-OSS-20B
// VM "bounty2" en europe-west4-a -> posiblemente backend de servicios

// NOTA: Las IPs reales deben obtenerse ejecutando:
// gcloud compute instances describe --zone "europe-southwest1-b" "gpt-oss-20b" --project "mamba-001"
// gcloud compute instances describe --zone "europe-west4-a" "bounty2" --project "mamba-001"

// Configuración provisional - DEBE ACTUALIZARSE CON LAS IPs REALES
const CHATBOT_CONFIG = {
    // URL del backend en la VM de Capibara6 (esto podría ser bounty2 o una nueva IP)
    // Por defecto uso la IP mencionada en la documentación, pero podría ser diferente
    BACKEND_URL: 'http://34.175.215.109:5001',  // IP de la VM de Capibara6 en puerto 5001 (debe verificarse)

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

console.log('🔧 Configuración de conexión a VMs reales cargada');
console.log('🔗 Backend URL:', CHATBOT_CONFIG.BACKEND_URL);
console.log('📡 Verifica que esta IP corresponda a la VM correcta');