// Configuración global para Capibara6
// Definir endpoints consistentes para evitar discrepancias

// Evitar múltiples declaraciones de la misma variable
if (typeof window.CHATBOT_CONFIG === 'undefined') {
    // Definir la URL base primero para evitar referencias circulares
    const BACKEND_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000'  // Desarrollo
        : window.location.origin;   // Producción (https://www.capibara6.com)

    const CHATBOT_CONFIG = {
        BACKEND_URL: BACKEND_URL,

        // Definir endpoints explícitamente para evitar confusiones
        ENDPOINTS: {
            HEALTH: '/api/health',
            CHAT: '/api/chat',           // Endpoint principal para chat
            COMPLETION: '/api/completion', // Endpoint alternativo (desaconsejado)
            GENERATE: '/api/generate',   // Endpoint para generación
            CLASSIFY: '/api/classify',   // Endpoint para clasificación
            MCP_CONTEXT: '/api/mcp/context',  // Endpoint MCP
            MCP_STATUS: '/api/mcp/status',    // Endpoint estado MCP
        },

        // Servicios adicionales
        SERVICES: {
            ACONTEXT: {
                ENABLED: true,
                BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
                    ? `${BACKEND_URL}/api/acontext`  // Usar gateway local
                    : `${BACKEND_URL}/api/acontext`,  // Usar gateway en producción
                ENDPOINTS: {
                    STATUS: '/status',
                    SESSION_CREATE: '/session/create',
                    SPACE_CREATE: '/space/create',
                    SEARCH: '/search'
                }
            },
            TTS: {
                ENABLED: true,
                ENDPOINT: '/api/tts'
            },
            RAG: {
                ENABLED: true,
                ENDPOINT: '/api/rag'
            }
        }
    };

    // Exportar para uso global
    window.CHATBOT_CONFIG = CHATBOT_CONFIG;
}