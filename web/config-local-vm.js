// Configuración para desarrollo local conectándose a las VMs de Google Cloud
// Este archivo debe ser incluido antes de otros scripts de configuración

// IPs de las VMs (actualizar con las IPs reales obtenidas)
const VM_IPS = {
    // VM bounty2 - Ollama con modelos (europe-west4-a)
    BOUNTY2: '34.12.166.76',  // IP mencionada en documentación - VERIFICAR
    
    // VM rag3 - Base de datos RAG (europe-west2-c)
    RAG3: '[OBTENER_IP]',  // Obtener IP real
    
    // VM gpt-oss-20b - Servicios TTS, MCP, N8n, Bridge (europe-southwest1-b)
    GPT_OSS_20B: '34.175.136.104',  // IP mencionada en documentación - VERIFICAR
};

// Configuración del chatbot para desarrollo local
const CHATBOT_CONFIG_LOCAL = {
    // URL del backend principal (en bounty2)
    BACKEND_URL: `http://${VM_IPS.BOUNTY2}:5001`,
    
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
        
        // TTS endpoints
        TTS_SPEAK: '/api/tts/speak',
        TTS_VOICES: '/api/tts/voices',
        TTS_CLONE: '/api/tts/clone',
    },
    
    // Configuración del modelo
    MODEL_CONFIG: {
        max_tokens: 200,
        temperature: 0.7,
        model_name: 'gpt-oss-20b',
        timeout: 120000 // 2 minutos
    },
    
    // URLs de servicios externos
    SERVICES: {
        // Ollama (en bounty2)
        OLLAMA_URL: `http://${VM_IPS.BOUNTY2}:11434`,
        
        // RAG (en rag3)
        RAG_URL: `http://${VM_IPS.RAG3}:[PUERTO]`,  // Actualizar con puerto real
        
        // Servicios TTS, MCP, etc. (en gpt-oss-20b)
        SERVICES_URL: `http://${VM_IPS.GPT_OSS_20B}:5000`,
        MCP_URL: `http://${VM_IPS.GPT_OSS_20B}:5003`,
        MCP_ALT_URL: `http://${VM_IPS.GPT_OSS_20B}:5010`,
    }
};

// Configuración del modelo para chat-app.js
const MODEL_CONFIG_LOCAL = {
    serverUrl: `${CHATBOT_CONFIG_LOCAL.BACKEND_URL}${CHATBOT_CONFIG_LOCAL.ENDPOINTS.CHAT}`,
    systemPrompt: 'Eres Capibara6, un asistente experto en tecnología, programación e IA. Responde de forma clara, estructurada y en español.',
    defaultParams: {
        n_predict: 200,
        temperature: 0.8,
        top_p: 0.9,
        repeat_penalty: 1.1,
        presence_penalty: 0.0,
        frequency_penalty: 0.0,
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

// Exportar configuración
if (typeof window !== 'undefined') {
    window.CHATBOT_CONFIG_LOCAL = CHATBOT_CONFIG_LOCAL;
    window.MODEL_CONFIG_LOCAL = MODEL_CONFIG_LOCAL;
    window.VM_IPS = VM_IPS;
    
    console.log('🔧 Configuración local para VMs cargada');
    console.log('🔗 Backend URL:', CHATBOT_CONFIG_LOCAL.BACKEND_URL);
    console.log('📡 VM IPs:', VM_IPS);
}

