// Configuración del chatbot capibara6
// 
// Arquitectura de VMs:
// - gpt-oss-20b (34.175.136.104): Servidor principal, MCP, TTS, N8n, Bridge
// - bounty2 (34.12.166.76): Ollama con modelos (gpt-oss-20B, mixtral, phi-mini3)
// - rag3: Base de datos RAG

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo local: Conectar a VM bounty2 (Backend integrado con Ollama)
    // En producción: URL de Vercel
    BACKEND_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://34.12.166.76:5001'  // VM bounty2 - Backend integrado con Ollama
        : 'https://www.capibara6.com',
    
    // Configuración de servicios por VM
    VMS: {
        // VM gpt-oss-20b: Servicios principales
        GPT_OSS_20B: {
            ip: '34.175.136.104',
            services: {
                main: 'http://34.175.136.104:5000',      // Servidor principal
                mcp: 'http://34.175.136.104:5003',        // MCP Server
                mcpAlt: 'http://34.175.136.104:5010',     // MCP Server alternativo
                model: 'http://34.175.136.104:8080'       // Llama Server (gpt-oss-20b)
            }
        },
        // VM bounty2: Ollama con modelos
        BOUNTY2: {
            ip: '34.12.166.76',
            services: {
                ollama: 'http://34.12.166.76:11434',      // Ollama API
                backend: 'http://34.12.166.76:5001'      // Backend Capibara6 integrado
            }
        },
        // VM rag3: Base de datos RAG
        RAG3: {
            ip: '34.105.131.8',
            services: {
                rag: 'http://34.105.131.8:8000',      // RAG Server
                api: 'http://34.105.131.8:8000/api'   // API REST
            }
        }
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
        TTS_SPEAK: '/api/tts/speak',
        TTS_VOICES: '/api/tts/voices',
        // Endpoints RAG
        RAG_SEARCH: '/api/search/rag',
        RAG_SEMANTIC: '/api/search/semantic',
        RAG_MESSAGES: '/api/messages',
        RAG_FILES: '/api/files',
        RAG_USERS: '/api/users'
    }
};
