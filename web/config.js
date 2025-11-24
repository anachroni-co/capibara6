// Configuración del chatbot capibara6
// Para desarrollo local, usa el proxy CORS local (puerto 8001) para el backend principal
// El proxy CORS debe estar corriendo en tu portátil: python3 backend/cors_proxy_simple.py

// IPs de las VMs (para servicios que no pasan por el proxy principal)
const VM_IPS = {
    // IP externa de Bounty2 (Ollama + Backend)
    BOUNTY2_EXTERNAL: '34.12.166.76',  // Para Ollama directamente
    // IP externa de gpt-oss-20b (TTS, MCP, N8n, Bridge)
    GPTOSS_EXTERNAL: '34.175.136.104',
    // IP externa de rag3 (RAG API)
    RAG3_EXTERNAL: '',  // ACTUALIZAR con IP real cuando esté disponible
};

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo local: usar proxy CORS local (puerto 8001) para evitar problemas CORS
    // En producción: URL de Vercel
    BACKEND_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:8001'  // Proxy CORS local (debe estar corriendo en el portátil)
        : 'https://www.capibara6.com',
    
    // URLs de servicios adicionales (para desarrollo local)
    // NOTA: Estos servicios pueden necesitar proxies también si hay problemas CORS
    SERVICE_URLS: {
        // Ollama API (en Bounty2) - NO accesible externamente según firewall
        // Solo accesible internamente (10.0.0.0/8) o a través del backend integrado
        // Usar el backend en puerto 5000 que puede acceder a Ollama internamente
        OLLAMA: null,  // No accesible directamente, usar backend integrado
        
        // RAG API (en rag3) - Usar puerto 5000 (Capibara6 Integrated Server) ya que 8000 no está abierto en firewall
        // NOTA: Si RAG API está en otro puerto, actualizar aquí
        RAG_API: window.location.hostname === 'localhost' && VM_IPS.RAG3_EXTERNAL
            ? `http://${VM_IPS.RAG3_EXTERNAL}:5000`  // Puerto 5000 abierto según firewall
            : null,
        
        // TTS (en gpt-oss-20b) - Puerto 5001 según firewall (Kyutai TTS Server)
        TTS: window.location.hostname === 'localhost'
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5001`
            : null,
        
        // MCP (en gpt-oss-20b) - Puede necesitar proxy si hay CORS
        MCP: window.location.hostname === 'localhost'
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5003`
            : null,
        
        // N8n (en gpt-oss-20b) - Puede necesitar proxy si hay CORS
        N8N: window.location.hostname === 'localhost'
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5678`
            : null,
    },
    
    // Endpoints disponibles en el servidor integrado
    ENDPOINTS: {
        // Chat principal
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        
        // Health check (el servidor integrado usa /health, no /api/health)
        HEALTH: '/health',
        
        // AI endpoints
        AI_GENERATE: '/api/ai/generate',
        // NOTA: /api/ai/classify NO existe en el servidor integrado
        
        // MCP endpoints
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        MCP_ANALYZE: '/api/mcp/analyze',
        
        // TTS endpoints
        TTS_SPEAK: '/api/tts/speak',
        TTS_VOICES: '/api/tts/voices',
        TTS_CLONE: '/api/tts/clone',
        
        // Otros endpoints
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
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
