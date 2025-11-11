// Configuración del chatbot capibara6

const CHATBOT_CONFIG = {
    // URL del backend
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
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        AI_GENERATE: '/api/ai/generate',
        AI_CLASSIFY: '/api/ai/classify'
    }
};
