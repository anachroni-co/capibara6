// ============================================
// INTEGRACIÓN DE CONSENSO - CAPIBARA6
// ============================================

// Configuración del sistema de consenso
const CONSENSUS_CONFIG = {
    // NOTA: Reemplaza [IP_DE_BOUNTY2] con la IP externa real de la VM bounty2
    // Para obtenerla, ejecuta: gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001
    serverUrl: window.location.hostname === 'localhost'
        ? 'http://34.175.215.109:5003/api/mcp/tools/call'  // Smart MCP Server (firewall: tcp:5003)
        : 'http://localhost:5001/api/mcp/tools/call',      // Local en producción
    fallbackUrl: 'http://34.175.89.158:8080/completion',
    enabled: true,
    defaultTemplate: 'general',
    selectedModels: ['capibara6', 'oss-120b']
};

// Estado del consenso
let availableModels = [];
let availableTemplates = [];
let selectedTemplate = 'general';
let selectedModels = ['capibara6', 'oss-120b'];
let consensusEnabled = true;

// ============================================
// FUNCIONES DE CONSENSO
// ============================================

async function loadConsensusConfig() {
    try {
        // Cargar modelos disponibles (usando endpoints MCP en lugar de consensus)
        // IP REAL de la VM (según firewall actualizado)
        // Puerto 5003 está abierto para Smart MCP Server según firewall
        const serverBaseUrl = window.location.hostname === 'localhost'
            ? 'http://34.175.215.109:5003'  // Smart MCP Server (firewall: tcp:5003)
            : 'http://localhost:5001';
            
        const modelsResponse = await fetch(`${serverBaseUrl}/api/mcp/tools/list`);
        if (modelsResponse.ok) {
            const modelsData = await modelsResponse.json();
            availableModels = modelsData.result ? Object.keys(modelsData.result) : ['gpt-oss-20b', 'phi', 'mixtral'];
        } else {
            // Fallback si el endpoint MCP no está disponible
            availableModels = ['gpt-oss-20b', 'phi', 'mixtral'];
        }
        
        // Cargar plantillas disponibles
        const templatesResponse = await fetch(`${serverBaseUrl}/api/mcp/prompts/list`);
        if (templatesResponse.ok) {
            const templatesData = await templatesResponse.json();
            availableTemplates = templatesData.result ? Object.keys(templatesData.result) : ['analyze-compliance', 'optimize-performance', 'multimodal-analysis'];
        } else {
            // Fallback si el endpoint MCP no está disponible
            availableTemplates = ['analyze-compliance', 'optimize-performance', 'multimodal-analysis'];
        }
        
        // Cargar estado del MCP
        const configResponse = await fetch(`${serverBaseUrl}/api/mcp/status`);
        if (configResponse.ok) {
            const configData = await configResponse.json();
            consensusEnabled = configData.enabled;
        }
        
        console.log('Configuración del consenso cargada:', {
            models: availableModels,
            templates: availableTemplates,
            enabled: consensusEnabled
        });
        
        // Actualizar interfaz
        updateConsensusUI();
        
    } catch (error) {
        console.warn('No se pudo cargar la configuración del consenso, usando fallback:', error);
        // Usar configuración por defecto
        availableModels = ['capibara6'];
        availableTemplates = ['general'];
        consensusEnabled = false;
    }
}

async function queryWithConsensus(prompt, template = 'general') {
    if (!consensusEnabled || availableModels.length === 0) {
        // Fallback al modelo original
        return await queryOriginalModel(prompt);
    }
    
    try {
        const response = await fetch(CONSENSUS_CONFIG.serverUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                template: template,
                models: selectedModels
            })
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error(`Error del servidor: ${response.status}`);
        }
        
    } catch (error) {
        console.warn('Error en consenso, usando fallback:', error);
        return await queryOriginalModel(prompt);
    }
}

async function queryOriginalModel(prompt) {
    // Función original de consulta al modelo
    const conversationHistory = buildConversationHistory(prompt);
    
    const response = await fetch(CONSENSUS_CONFIG.fallbackUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: conversationHistory,
            n_predict: 100,
            temperature: 0.6,
            top_p: 0.85,
            repeat_penalty: 1.3,
            stream: true
        })
    });
    
    if (!response.ok) {
        throw new Error(`Error del servidor: ${response.status}`);
    }
    
    return await response.json();
}

function buildConversationHistory(prompt) {
    const systemPrompt = 'Responde en el mismo idioma de la pregunta. Si piden código, usa bloques markdown: ```lenguaje';
    let conversationHistory = '';
    
    if (systemPrompt) {
        conversationHistory += `<bos><start_of_turn>system\n${systemPrompt}<end_of_turn>\n`;
    }
    
    // Agregar historial de conversación
    if (typeof currentChatId !== 'undefined' && currentChatId && typeof chats !== 'undefined' && chats[currentChatId]) {
        const chat = chats[currentChatId];
        for (const message of chat.messages) {
            if (message.role === 'user') {
                conversationHistory += `<start_of_turn>user\n${message.content}<end_of_turn>\n`;
            } else if (message.role === 'assistant') {
                conversationHistory += `<start_of_turn>model\n${message.content}<end_of_turn>\n`;
            }
        }
    }
    
    // Agregar el prompt actual
    conversationHistory += `<start_of_turn>user\n${prompt}<end_of_turn>\n<start_of_turn>model\n`;
    
    return conversationHistory;
}

// ============================================
// INTERFAZ DE USUARIO
// ============================================

function updateConsensusUI() {
    // Actualizar contador de consenso
    if (typeof updateConsensusCount === 'function') {
        updateConsensusCount(availableModels.length);
    }
    
    // Actualizar información del consenso
    if (typeof showConsensusInfo === 'function') {
        updateConsensusInfo();
    }
}

function updateConsensusInfo() {
    const consensusCount = document.getElementById('consensus-count');
    if (consensusCount) {
        const modelNames = availableModels.map(id => {
            const config = getModelConfig(id);
            return config ? config.name : id;
        }).join(', ');
        
        consensusCount.title = `🟡 MODO BETA - Capibara6 Consensus
Modelos activos: ${availableModels.length}
Modelos: ${modelNames}
Plantilla actual: ${selectedTemplate}
Consenso: ${consensusEnabled ? 'Habilitado' : 'Deshabilitado'}`;
    }
}

function getModelConfig(modelId) {
    const modelConfigs = {
        'capibara6': {
            name: 'Capibara6',
            hardware: 'GPU',
            base_model: 'Gemma3-12B'
        },
        'oss-120b': {
            name: 'OSS-120B',
            hardware: 'TPU-v5e-64',
            base_model: 'Open Source Supervised 120B'
        }
    };
    
    return modelConfigs[modelId];
}

// ============================================
// SELECTOR DE PLANTILLAS
// ============================================

function createTemplateSelector() {
    const templateSelector = document.createElement('div');
    templateSelector.className = 'template-selector';
    templateSelector.innerHTML = `
        <div class="template-header">
            <i data-lucide="layout-template"></i>
            <span>Plantilla de Prompt</span>
        </div>
        <select id="template-select" class="template-select">
            <option value="general">General</option>
            <option value="coding">Programación</option>
            <option value="analysis">Análisis</option>
            <option value="creative">Creativo</option>
            <option value="technical">Técnico</option>
        </select>
    `;
    
    // Agregar al sidebar
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.appendChild(templateSelector);
        
        // Event listener para cambio de plantilla
        const select = document.getElementById('template-select');
        if (select) {
            select.addEventListener('change', (e) => {
                selectedTemplate = e.target.value;
                console.log('Plantilla cambiada a:', selectedTemplate);
            });
        }
    }
}

// ============================================
// SELECTOR DE MODELOS
// ============================================

function createModelSelector() {
    const modelSelector = document.createElement('div');
    modelSelector.className = 'model-selector';
    modelSelector.innerHTML = `
        <div class="model-header">
            <i data-lucide="cpu"></i>
            <span>Modelos Activos</span>
        </div>
        <div class="model-checkboxes">
            <label class="model-checkbox">
                <input type="checkbox" id="model-capibara6" checked>
                <span>Capibara6 (GPU)</span>
            </label>
            <label class="model-checkbox">
                <input type="checkbox" id="model-oss-120b" checked>
                <span>OSS-120B (TPU)</span>
            </label>
        </div>
    `;
    
    // Agregar al sidebar
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.appendChild(modelSelector);
        
        // Event listeners para cambio de modelos
        const checkboxes = modelSelector.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateSelectedModels);
        });
    }
}

function updateSelectedModels() {
    selectedModels = [];
    
    const capibara6Checkbox = document.getElementById('model-capibara6');
    const oss120bCheckbox = document.getElementById('model-oss-120b');
    
    if (capibara6Checkbox && capibara6Checkbox.checked) {
        selectedModels.push('capibara6');
    }
    
    if (oss120bCheckbox && oss120bCheckbox.checked) {
        selectedModels.push('oss-120b');
    }
    
    console.log('Modelos seleccionados:', selectedModels);
}

// ============================================
// INICIALIZACIÓN
// ============================================

function initConsensus() {
    // Cargar configuración
    loadConsensusConfig();
    
    // Crear selectores de interfaz
    createTemplateSelector();
    createModelSelector();
    
    // Inicializar iconos
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Auto-inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initConsensus);
} else {
    initConsensus();
}

// Exportar funciones para uso global
window.loadConsensusConfig = loadConsensusConfig;
window.queryWithConsensus = queryWithConsensus;
window.updateConsensusUI = updateConsensusUI;
window.initConsensus = initConsensus;
