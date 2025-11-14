// ============================================
// Configuración Consolidada de Capibara6
// Fusiona: config.js, config-cors-proxy.js, config-dev-vm.js, config-local-vm.js
// ============================================

// IPs de las VMs de Google Cloud
// Actualizar según vm_config.json o ejecutando: scripts/get_vm_info.py
const VM_IPS = {
    // IP externa de Bounty2 (Ollama + Backend)
    // Zona: europe-west4-a
    BOUNTY2_EXTERNAL: '34.12.166.76',
    
    // IP externa de gpt-oss-20b (TTS, MCP, N8n, Bridge)
    // Zona: europe-southwest1-b
    GPTOSS_EXTERNAL: '34.175.136.104',
    
    // IP externa de rag3 (RAG API)
    // Zona: europe-west2-c
    // TODO: Actualizar con IP real cuando esté disponible
    RAG3_EXTERNAL: '',
};

// Detectar entorno (localhost vs producción)
const isLocalhost = window.location.hostname === 'localhost' || 
                    window.location.hostname === '127.0.0.1' ||
                    window.location.hostname === '';

// Detectar proxy CORS local automáticamente
// El proxy CORS resuelve problemas de CORS entre localhost y las VMs remotas
const CORS_PROXY_URL = (() => {
    if (!isLocalhost) return null;
    
    // IPs conocidas del proxy CORS local
    const PROXY_IPS = [
        '172.22.134.254',  // IP detectada en WSL/Docker
        'localhost',
        '127.0.0.1'
    ];
    
    const PROXY_PORTS = [8001, 5001];
    
    // Por defecto usar localhost:8001 (proxy CORS local)
    // Si el proxy está en otra IP, actualizar aquí
    return 'http://localhost:8001';
})();

// ============================================
// Configuración Principal del Chatbot
// ============================================
const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo local: usa proxy CORS local que conecta a Bounty2:5001
    // En producción: URL de Vercel
    BACKEND_URL: isLocalhost
        ? (CORS_PROXY_URL || 'http://localhost:8001')  // Proxy CORS local
        : 'https://www.capibara6.com',
    
    // URLs de servicios adicionales (solo en desarrollo local)
    SERVICE_URLS: {
        // Ollama API (en Bounty2)
        // Puerto: 11434
        OLLAMA: isLocalhost
            ? `http://${VM_IPS.BOUNTY2_EXTERNAL}:11434`
            : null,
        
        // RAG API (en rag3)
        // Puerto: 8000
        RAG_API: isLocalhost && VM_IPS.RAG3_EXTERNAL
            ? `http://${VM_IPS.RAG3_EXTERNAL}:8000`
            : null,
        
        // TTS (Text-to-Speech) (en gpt-oss-20b)
        // Puerto: 5002
        TTS: isLocalhost
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5002`
            : null,
        
        // MCP (Model Context Protocol) (en gpt-oss-20b)
        // Puerto: 5003 (alternativa: 5010)
        MCP: isLocalhost
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5003`
            : null,
        
        // N8n (Workflow Automation) (en gpt-oss-20b)
        // Puerto: 5678
        N8N: isLocalhost
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5678`
            : null,
        
        // Servidor principal de Capibara6 (en gpt-oss-20b)
        // Puerto: 5000
        SERVER: isLocalhost
            ? `http://${VM_IPS.GPTOSS_EXTERNAL}:5000`
            : null,
    },
    
    // Endpoints de la API
    ENDPOINTS: {
        // Chat
        CHAT: '/api/chat',
        CHAT_STREAM: '/api/chat/stream',
        
        // Conversaciones y leads
        SAVE_CONVERSATION: '/api/save-conversation',
        SAVE_LEAD: '/api/save-lead',
        
        // Sistema
        HEALTH: '/api/health',
        MODELS: '/api/models',
        
        // MCP (Model Context Protocol)
        MCP_STATUS: '/api/mcp/status',
        MCP_TOOLS_CALL: '/api/mcp/tools/call',
        MCP_ANALYZE: '/api/mcp/analyze',
        
        // AI
        AI_GENERATE: '/api/ai/generate',
        AI_CLASSIFY: '/api/ai/classify',
        
        // TTS (Text-to-Speech)
        TTS_SPEAK: '/api/tts/speak',
        TTS_VOICES: '/api/tts/voices',
        TTS_CLONE: '/api/tts/clone',
    },
    
    // Configuración del modelo
    MODEL_CONFIG: {
        max_tokens: 200,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 120000, // 2 minutos
    }
};

// ============================================
// Configuración del Modelo para chat-app.js
// Compatible con la configuración de chat-app.js
// ============================================
const MODEL_CONFIG = {
    // URL del servidor del modelo
    serverUrl: typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.BACKEND_URL
        ? `${CHATBOT_CONFIG.BACKEND_URL}${CHATBOT_CONFIG.ENDPOINTS.CHAT}`
        : (isLocalhost
            ? `http://${VM_IPS.BOUNTY2_EXTERNAL}:5001/api/chat`
            : 'https://www.capibara6.com/api/chat'),
    
    // Prompt del sistema
    systemPrompt: 'Eres Capibara6, un asistente experto en tecnología, programación e IA. Responde de forma clara, estructurada y en español.',
    
    // Parámetros por defecto del modelo
    defaultParams: {
        n_predict: 200,          // Tokens máximos a generar
        temperature: 0.8,        // Creatividad (0.0-1.0)
        top_p: 0.9,              // Nucleus sampling
        repeat_penalty: 1.1,     // Penalización por repetición
        presence_penalty: 0.0,   // Penalización por presencia
        frequency_penalty: 0.0,  // Penalización por frecuencia
        stop: [
            "Usuario:",
            "Capibara6:",
            "<end_of_turn>",
            "<|end_of_turn|>",
            "<|im_end|>",
            "\n\n"
        ]
    }
};

// ============================================
// Exponer variables globales
// ============================================
if (typeof window !== 'undefined') {
    // Exponer configuración principal
    window.CHATBOT_CONFIG = CHATBOT_CONFIG;
    window.MODEL_CONFIG = MODEL_CONFIG;
    window.VM_IPS = VM_IPS;
    
    // Exponer proxy CORS si está disponible
    if (CORS_PROXY_URL) {
        window.CORS_PROXY_URL = CORS_PROXY_URL;
    }
    
    // Exponer detección de entorno
    window.isLocalhost = isLocalhost;
}

// ============================================
// Logs de configuración (solo en desarrollo)
// ============================================
if (isLocalhost) {
    console.log('🔧 Configuración de desarrollo local activada');
    console.log('🔗 Backend URL:', CHATBOT_CONFIG.BACKEND_URL);
    
    if (CORS_PROXY_URL) {
        console.log('🔧 Proxy CORS configurado:', CORS_PROXY_URL);
    }
    
    console.log('📡 Servicios disponibles:', CHATBOT_CONFIG.SERVICE_URLS);
    console.log('🖥️  VM IPs:', VM_IPS);
    
    // Advertencias
    if (!VM_IPS.RAG3_EXTERNAL) {
        console.warn('⚠️  RAG3_EXTERNAL no configurado. El servicio RAG no estará disponible.');
    }
} else {
    console.log('🌐 Configuración de producción activada');
    console.log('🔗 Backend URL:', CHATBOT_CONFIG.BACKEND_URL);
}

// ============================================
// Funciones de utilidad
// ============================================

/**
 * Obtener URL completa de un endpoint
 * @param {string} endpoint - Nombre del endpoint (ej: 'CHAT')
 * @returns {string} URL completa
 */
function getEndpointUrl(endpoint) {
    const endpointPath = CHATBOT_CONFIG.ENDPOINTS[endpoint];
    if (!endpointPath) {
        console.error(`Endpoint no encontrado: ${endpoint}`);
        return null;
    }
    return `${CHATBOT_CONFIG.BACKEND_URL}${endpointPath}`;
}

/**
 * Obtener URL de un servicio
 * @param {string} service - Nombre del servicio (ej: 'TTS', 'MCP')
 * @returns {string|null} URL del servicio o null si no está disponible
 */
function getServiceUrl(service) {
    return CHATBOT_CONFIG.SERVICE_URLS[service] || null;
}

/**
 * Verificar si un servicio está disponible
 * @param {string} service - Nombre del servicio
 * @returns {boolean} true si el servicio está disponible
 */
function isServiceAvailable(service) {
    return CHATBOT_CONFIG.SERVICE_URLS[service] !== null && 
           CHATBOT_CONFIG.SERVICE_URLS[service] !== undefined;
}

// Exponer funciones de utilidad
if (typeof window !== 'undefined') {
    window.getEndpointUrl = getEndpointUrl;
    window.getServiceUrl = getServiceUrl;
    window.isServiceAvailable = isServiceAvailable;
}