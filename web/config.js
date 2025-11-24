// Configuración del chatbot capibara6
// Configuración para desarrollo local conectándose a VMs de Google Cloud

// IPs de las VMs (actualizar si cambian)
const VM_IPS = {
    BOUNTY2: '34.12.166.76',      // VM bounty2 - Ollama con modelos
    RAG3: '',                      // VM rag3 - Base de datos RAG (por determinar)
    GPT_OSS_20B: '34.175.136.104' // VM gpt-oss-20b - TTS, MCP, N8n, Bridge
};

// Detectar proxy CORS local automáticamente
const CORS_PROXY_URL = (() => {
    // IPs conocidas del proxy CORS local
    const PROXY_IPS = ['172.22.134.254', 'localhost', '127.0.0.1'];
    const PROXY_PORTS = [8001];
    
    // Usar la IP detectada del proxy
    return 'http://172.22.134.254:8001';
})();

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo local: usar proxy CORS local para evitar problemas CORS
    // En producción: usar dominio de Vercel
    BACKEND_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? CORS_PROXY_URL  // Usar proxy CORS local (resuelve problemas CORS)
        : 'https://www.capibara6.com',
    
    // URLs de servicios específicos para desarrollo local
    SERVICES: {
        // Ollama en bounty2
        OLLAMA_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? `http://${VM_IPS.BOUNTY2}:11434`
            : 'https://www.capibara6.com/api/ollama',
        
        // RAG en rag3 (si está configurado)
        RAG_URL: VM_IPS.RAG3 && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
            ? `http://${VM_IPS.RAG3}:8000`
            : 'https://www.capibara6.com/api/rag',
        
        // TTS en gpt-oss-20b
        TTS_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? `http://${VM_IPS.GPT_OSS_20B}:5002`
            : 'https://www.capibara6.com/api/tts',
        
        // MCP en gpt-oss-20b
        MCP_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? `http://${VM_IPS.GPT_OSS_20B}:5003`
            : 'https://www.capibara6.com/api/mcp',
        
        // N8n en gpt-oss-20b
        N8N_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? `http://${VM_IPS.GPT_OSS_20B}:5678`
            : 'https://www.capibara6.com/api/n8n',
        
        // Bridge en gpt-oss-20b
        BRIDGE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? `http://${VM_IPS.GPT_OSS_20B}:5000`
            : 'https://www.capibara6.com/api/bridge'
    },
    
    // Endpoints
    ENDPOINTS: {
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        HEALTH: '/api/health',
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        MCP_ANALYZE: '/api/mcp/analyze',
        AI_GENERATE: '/api/ai/generate',
        AI_CLASSIFY: '/api/ai/classify',
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        TTS_SPEAK: '/api/tts/speak',
        TTS_VOICES: '/api/tts/voices',
        MODELS: '/api/models'
    }
};

// Log de configuración en desarrollo
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('🔧 Configuración de desarrollo local activada');
    console.log('🔗 Backend URL:', CHATBOT_CONFIG.BACKEND_URL);
    console.log('🔌 Proxy CORS:', CORS_PROXY_URL);
    console.log('📡 Servicios:', CHATBOT_CONFIG.SERVICES);
}
