// Configuración del chatbot capibara6
// Para desarrollo local, actualiza las IPs en este archivo según VM_SETUP_GUIDE.md

// IPs de las VMs (actualizar según vm_config.json o ejecutando scripts/get_vm_info.py)
const VM_IPS = {
    // IP externa de Bounty2 (Ollama + Backend)
    BOUNTY2_EXTERNAL: '34.12.166.76',  // ACTUALIZAR con IP real
    // IP externa de gpt-oss-20b (TTS, MCP, N8n, Bridge)
    GPTOSS_EXTERNAL: '34.175.136.104',  // ACTUALIZAR con IP real
    // IP externa de rag3 (RAG API)
    RAG3_EXTERNAL: '',  // ACTUALIZAR con IP real
};

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo local: usa el proxy CORS local en puerto 8001 que conecta a Bounty2
    // El proxy resuelve problemas de CORS entre localhost:8000 y la VM remota
    // En producción: URL de Vercel
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:8001'  // Proxy CORS local que conecta a Bounty2:5001
        : 'https://www.capibara6.com',
    
    // URLs de servicios adicionales (para desarrollo local)
    SERVICE_URLS: {
        // Ollama API (en Bounty2)
        OLLAMA: window.location.hostname === 'localhost'
            ? `http://${VM_IPS.BOUNTY2_EXTERNAL}:11434`
            : null,
        
        // RAG API (en rag3)
        RAG_API: window.location.hostname === 'localhost' && VM_IPS.RAG3_EXTERNAL
            ? `http://${VM_IPS.RAG3_EXTERNAL}:8000`
            : null,
        
        // TTS (en gpt-oss-20b)
        TTS: window.location.hostname === 'localhost'
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5002`
            : null,
        
        // MCP (en gpt-oss-20b)
        MCP: window.location.hostname === 'localhost'
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5003`
            : null,
        
        // N8n (en gpt-oss-20b)
        N8N: window.location.hostname === 'localhost'
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5678`
            : null,
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
        TTS_CLONE: '/api/tts/clone',
        MODELS: '/api/models'
    },
    
    // Configuración del modelo
    MODEL_CONFIG: {
        max_tokens: 200,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 120000 // 2 minutos
    }
};

// Log de configuración en desarrollo
if (window.location.hostname === 'localhost') {
    console.log('🔧 Configuración de desarrollo local activada');
    console.log('🔗 Backend URL:', CHATBOT_CONFIG.BACKEND_URL);
    console.log('📡 Servicios disponibles:', CHATBOT_CONFIG.SERVICE_URLS);
}
