// Ejemplo de configuración con IPs reales para desarrollo local
// ESTE ES UN ARCHIVO DE EJEMPLO - NO SE USA DIRECTAMENTE EN LA APP

// Suponiendo que la IP pública de bounty2 es: 34.175.215.109 (SOLO EJEMPLO)
// Y que el servidor capibara6_integrated_server está corriendo en el puerto 5001

const EXAMPLE_CHATBOT_CONFIG = {
    // URL del backend - USAR SOLO PARA PRUEBAS LOCALES
    BACKEND_URL: 'http://34.175.215.109:5001',  // IP REAL de bounty2 con puerto real del servidor

    // Endpoints (no cambian)
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

    // Configuración del modelo
    MODEL_CONFIG: {
        max_tokens: 100,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 300000 // 5 minutos
    }
};

console.log('⚠️  ESTE ES SOLO UN EJEMPLO');
console.log('⚠️  No uses este archivo directamente en la aplicación');
console.log('⚠️  Debes obtener la IP REAL de bounty2 y el PUERTO REAL del servidor');