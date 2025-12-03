// Configuración automática para desarrollo local
// Generado el 2025-12-02 06:32:26
// IPs de las VMs de Google Cloud

const VM_CONFIG = {
    // VM bounty2 - Ollama con modelos
    BOUNTY2_IP: 'N/A',
    OLLAMA_URL: 'http://N/A:11434',
    BACKEND_API_URL: 'http://N/A:5001',
    
    // VM rag3 - Base de datos RAG
    RAG3_IP: 'N/A',
    RAG_API_URL: 'http://N/A:8000',
    
    // VM gpt-oss-20b - Servicios TTS, MCP, N8n, Bridge
    GPT_OSS_IP: 'N/A',
    TTS_URL: 'http://N/A:5002',
    MCP_URL: 'http://N/A:5003',
    N8N_URL: 'http://N/A:5678',
    BRIDGE_URL: 'http://N/A:5000',
};

// Configuración del chatbot para desarrollo local
const CHATBOT_CONFIG = {
    BACKEND_URL: window.location.hostname === 'localhost'
        ? VM_CONFIG.BACKEND_API_URL  // Usar VM bounty2 cuando está en localhost
        : 'https://www.capibara6.com',
    
    ENDPOINTS: {
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        HEALTH: '/api/health',
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        MCP_ANALYZE: '/api/mcp/analyze',
        TTS_SPEAK: '/api/tts/speak',
        TTS_VOICES: '/api/tts/voices',
        MODELS: '/api/models',
    },
    
    MODEL_CONFIG: {
        max_tokens: 200,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 120000
    }
};

console.log('🔧 Configuración de VMs cargada');
console.log('🔗 Backend URL:', CHATBOT_CONFIG.BACKEND_URL);
