// ============================================
// Configuración Consolidada de Capibara6
// Fusiona: config.js, config-cors-proxy.js, config-dev-vm.js, config-local-vm.js
// ============================================

// IPs de las VMs de Google Cloud - ACTUALIZADO 2025-11-27
// Red VPC: default (10.204.0.0/24) - Zona: europe-southwest1-b
// Todas las VMs están en la misma red VPC para latencia mínima
const VM_IPS = {
    // IP de models-europe (Ollama - Modelos de IA)
    // Modelos: gpt-oss:20b, mistral:latest, phi3:mini
    MODELS_EUROPE_INTERNAL: '10.204.0.9',
    MODELS_EUROPE_EXTERNAL: '34.175.48.2',

    // IP de services (TTS, MCP, N8n, Flask API)
    // Servicios de soporte y gateway
    SERVICES_INTERNAL: '10.204.0.5',
    SERVICES_EXTERNAL: '34.175.136.104',  // IP real de la VM gpt-oss-20b

    // IP de rag-europe (Bridge API + Bases de datos)
    // Milvus, Nebula Graph, PostgreSQL, Redis
    RAG_EUROPE_INTERNAL: '10.204.0.10',
    RAG_EUROPE_EXTERNAL: '34.175.110.120',
};

// Detectar entorno (localhost vs producción)
const isLocalhost = window.location.hostname === 'localhost' ||
                    window.location.hostname === '127.0.0.1' ||
                    window.location.hostname === '' ||
                    window.location.hostname === '34.175.136.104'; // IP de la VM services

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
    // En desarrollo local o VM: usa backend local
    // En producción: URL de Vercel
    BACKEND_URL: isLocalhost
        ? window.location.origin  // Usa el mismo origen (la VM o localhost)
        : 'https://www.capibara6.com',
    
    // URLs de servicios adicionales (solo en desarrollo local)
    SERVICE_URLS: {
        // Detectar si estamos en la VM services
        // Si estamos en la VM, usar rutas proxiadas por NGINX
        // Si estamos en localhost real, usar IPs externas directas

        // vLLM Multi-Model Server (en models-europe) - PRINCIPAL
        // Puerto: 8080 - 5 modelos: phi4_fast, mistral_balanced, qwen_coder, gemma3_multimodal, aya_expanse_multilingual
        VLLM: isLocalhost
            ? (window.location.hostname === '34.175.136.104'
                ? `${window.location.origin}/models`
                : `http://${VM_IPS.MODELS_EUROPE_EXTERNAL}:8080`)
            : null,

        // Ollama API (en models-europe) - ALTERNATIVO
        // Puerto: 11434
        OLLAMA: isLocalhost
            ? `http://${VM_IPS.MODELS_EUROPE_EXTERNAL}:11434`
            : null,

        // Bridge API + RAG (en rag-europe)
        // Puerto: 8000
        RAG_API: isLocalhost
            ? (window.location.hostname === '34.175.136.104'
                ? `${window.location.origin}/rag`
                : `http://${VM_IPS.RAG_EUROPE_EXTERNAL}:8000`)
            : null,

        // Bridge API endpoints específicos
        BRIDGE_API: isLocalhost
            ? (window.location.hostname === '34.175.136.104'
                ? `${window.location.origin}/rag`
                : `http://${VM_IPS.RAG_EUROPE_EXTERNAL}:8000`)
            : null,

        // Nebula Studio (en rag-europe)
        // Puerto: 7001
        NEBULA_STUDIO: isLocalhost
            ? `http://${VM_IPS.RAG_EUROPE_EXTERNAL}:7001`
            : null,

        // TTS (Text-to-Speech) (en services)
        // Puerto: 5001
        TTS: isLocalhost
            ? (window.location.hostname === '34.175.136.104'
                ? `${window.location.origin}/tts`
                : `http://${VM_IPS.SERVICES_EXTERNAL}:5001`)
            : null,

        // MCP (Model Context Protocol) (en services)
        // Puerto: 5003
        MCP: isLocalhost
            ? (window.location.hostname === '34.175.136.104'
                ? `${window.location.origin}/mcp`
                : `http://${VM_IPS.SERVICES_EXTERNAL}:5003`)
            : null,

        // N8n (Workflow Automation) (en services)
        // Puerto: 5678
        N8N: isLocalhost
            ? (window.location.hostname === '34.175.136.104'
                ? `${window.location.origin}/n8n`
                : `http://${VM_IPS.SERVICES_EXTERNAL}:5678`)
            : null,

        // Flask API (en services)
        // Puerto: 5000
        FLASK_API: isLocalhost
            ? `${window.location.origin}/api`
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
            ? `http://${VM_IPS.MODELS_EUROPE_EXTERNAL}:11434/api/generate`
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
    console.log('🌐 Red VPC: default (10.204.0.0/24) - Todas las VMs en la misma zona');
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