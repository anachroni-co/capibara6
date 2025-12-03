// Configuración para el frontend en VM services que coordina E2B en models-europe
const CHATBOT_CONFIG = {
  // Configuración del backend principal que está en esta misma VM (services)
  BACKEND: {
    url: 'http://localhost:5000', // Backend local en services VM
    timeout: 30000
  },

  // Configuración de servicios distribuidos
  SERVICES: {
    // El modelo backend está en models-europe pero accesible a través del backend local
    BACKEND_API: {
      url: 'http://localhost:5000', // Backend local en services actúa como proxy
      enabled: true
    },

    // E2B execution se coordina desde esta VM services pero se ejecuta en models-europe
    E2B: {
      url: 'http://localhost:5003', // Coordinador E2B local en services VM
      enabled: true,
      execute_endpoint: '/api/e2b/execute',
      visualization_endpoint: '/api/e2b/visualization',
      health_endpoint: '/api/e2b/health',
      execution_info: 'E2B tasks executed on models-europe VM for speed, results returned to frontend on services VM'
    },

    // TTS service en services VM
    TTS: {
      url: 'http://localhost:5002',
      enabled: true
    },

    // MCP service en services VM
    MCP: {
      url: 'http://localhost:5003',
      enabled: true
    }
  },

  // Configuración de modelos (accesibles a través del backend local en services)
  MODELS: {
    phi4_fast: {
      name: 'phi4_fast',
      description: 'Modelo rápido para tareas simples',
      domain: 'general'
    },
    mistral_balanced: {
      name: 'mistral_balanced',
      description: 'Modelo equilibrado para tareas técnicas',
      domain: 'technical'
    },
    qwen_coder: {
      name: 'qwen_coder',
      description: 'Modelo especializado en código',
      domain: 'coding'
    },
    gemma3_multimodal: {
      name: 'gemma3_multimodal',
      description: 'Modelo multimodal para análisis complejo',
      domain: 'multimodal_expert'
    },
    aya_expanse_multilingual: {
      name: 'aya_expanse_multilingual',
      description: 'Modelo multilingüe experto',
      domain: 'multilingual_expert'
    }
  },

  // Configuración de seguridad y autenticación
  SECURITY: {
    api_keys_required: false,
    cors_enabled: true,
    allowed_origins: ['*']
  },

  // Información sobre la arquitectura de E2B
  E2B_ARCHITECTURE: {
    execution_vm: 'models-europe',  // Donde se ejecuta para mayor velocidad
    coordination_vm: 'services',     // Donde está el coordinador y el frontend
    file_sharing: 'services VM serves visualization files from models-europe to frontend'
  }
};

// Exportar la configuración
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CHATBOT_CONFIG;
} else if (typeof window !== 'undefined') {
  window.CHATBOT_CONFIG = CHATBOT_CONFIG;
}