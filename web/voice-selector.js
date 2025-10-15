/**
 * Voice Selector & Cloning Module
 * Permite seleccionar voces predefinidas y clonar voces personalizadas
 */

const VOICE_CONFIG = {
    isLocal: true,  // Siempre usar la VM
    baseUrl: window.location.protocol === 'https:'
        ? 'https://34.175.215.109'  // Producción: HTTPS
        : 'http://34.175.215.109:5000',  // Desarrollo: HTTP
    selectedVoice: 'sofia',  // Voz por defecto
    customVoices: {}
};

/**
 * Inicializar selector de voces
 */
async function initVoiceSelector() {
    console.log('🎤 Inicializando selector de voces...');
    
    try {
        // Cargar voces disponibles
        await loadAvailableVoices();
        
        // Crear UI del selector
        createVoiceSelectorUI();
        
        // Event listeners
        setupVoiceEvents();
        
        console.log('✅ Selector de voces inicializado');
    } catch (error) {
        console.error('❌ Error al inicializar selector de voces:', error);
    }
}

/**
 * Cargar voces disponibles desde el servidor
 */
async function loadAvailableVoices() {
    try {
        const endpoint = VOICE_CONFIG.isLocal 
            ? `${VOICE_CONFIG.baseUrl}/voices`
            : '/api/tts-voices';
        const response = await fetch(endpoint);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log('📋 Voces disponibles:', data.voices);
        
        // Actualizar voces custom
        if (data.voices.custom) {
            VOICE_CONFIG.customVoices = data.voices.custom;
        }
        
        return data.voices;
        
    } catch (error) {
        console.warn('⚠️ No se pudieron cargar las voces:', error.message);
        return null;
    }
}

/**
 * Crear UI del selector de voces
 */
function createVoiceSelectorUI() {
    // Buscar contenedor del chat (puede ser .chat-container o #chat-area)
    const chatArea = document.querySelector('#chat-area') || document.querySelector('.chat-container');
    if (!chatArea) {
        console.warn('⚠️ No se encontró #chat-area o .chat-container');
        return;
    }
    
    // Crear panel de voces
    const voicePanel = document.createElement('div');
    voicePanel.className = 'voice-selector-panel';
    voicePanel.innerHTML = `
        <div class="voice-selector-header">
            <h3>🎤 Seleccionar Voz</h3>
            <button id="toggle-voice-panel" class="btn-icon" title="Mostrar/Ocultar">
                <i data-lucide="chevron-up"></i>
            </button>
        </div>
        
        <div class="voice-selector-content" style="display: block;">
            <!-- Estado del TTS -->
            <div id="tts-status-banner" class="tts-status-banner" style="display: none;">
                <i data-lucide="alert-circle"></i>
                <span>Usando voz del navegador. Para voces personalizadas, activa Coqui TTS en el servidor.</span>
            </div>
            
            <!-- Voces predefinidas -->
            <div class="voice-section">
                <h4>Voces Predefinidas</h4>
                <div class="voice-options">
                    <label class="voice-option">
                        <input type="radio" name="voice" value="sofia" checked>
                        <div class="voice-card">
                            <div class="voice-icon">👩</div>
                            <div class="voice-info">
                                <strong>Sofía</strong>
                                <span>Femenina • Profesional</span>
                            </div>
                            <button class="btn-test-voice" data-voice="sofia" title="Probar voz">
                                <i data-lucide="play"></i>
                            </button>
                        </div>
                    </label>
                    
                    <label class="voice-option">
                        <input type="radio" name="voice" value="ana">
                        <div class="voice-card">
                            <div class="voice-icon">👧</div>
                            <div class="voice-info">
                                <strong>Ana</strong>
                                <span>Femenina • Amigable</span>
                            </div>
                            <button class="btn-test-voice" data-voice="ana" title="Probar voz">
                                <i data-lucide="play"></i>
                            </button>
                        </div>
                    </label>
                    
                    <label class="voice-option">
                        <input type="radio" name="voice" value="carlos">
                        <div class="voice-card">
                            <div class="voice-icon">👨</div>
                            <div class="voice-info">
                                <strong>Carlos</strong>
                                <span>Masculina • Clara</span>
                            </div>
                            <button class="btn-test-voice" data-voice="carlos" title="Probar voz">
                                <i data-lucide="play"></i>
                            </button>
                        </div>
                    </label>
                </div>
            </div>
            
            <!-- Clonación de voz -->
            <div class="voice-section">
                <h4>🎭 Clonar Voz Personalizada</h4>
                <div class="voice-clone-area">
                    <div class="upload-area" id="voice-upload-area">
                        <i data-lucide="upload" class="upload-icon"></i>
                        <p>Arrastra un audio o haz clic para seleccionar</p>
                        <span class="upload-hint">WAV, MP3 (5-10 seg recomendado)</span>
                        <input type="file" id="voice-file-input" accept="audio/*" style="display: none;">
                    </div>
                    
                    <div id="voice-clone-status" style="display: none;">
                        <div class="clone-progress">
                            <span id="clone-message">Procesando...</span>
                            <div class="progress-bar">
                                <div class="progress-fill"></div>
                            </div>
                        </div>
                    </div>
                    
                    <div id="custom-voices-list" style="display: none;">
                        <h5>Voces Clonadas</h5>
                        <div id="custom-voices-container"></div>
                    </div>
                </div>
            </div>
            
            <div class="voice-selector-footer">
                <span class="voice-info-text">
                    <i data-lucide="info"></i>
                    La voz seleccionada se usará para el botón 🔊
                </span>
            </div>
        </div>
    `;
    
    // Insertar antes del contenedor de mensajes
    const messagesContainer = chatArea.querySelector('#messages-container') || chatArea.querySelector('.chat-messages');
    if (messagesContainer) {
        chatArea.insertBefore(voicePanel, messagesContainer);
        console.log('✅ Selector de voz insertado en la UI');
    } else {
        // Si no hay contenedor de mensajes, agregar al final del chat-area
        chatArea.appendChild(voicePanel);
        console.log('✅ Selector de voz agregado al final del chat-area');
    }
    
    // Reinicializar iconos de Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

/**
 * Setup event listeners
 */
function setupVoiceEvents() {
    // Toggle panel
    const toggleBtn = document.getElementById('toggle-voice-panel');
    const content = document.querySelector('.voice-selector-content');
    
    if (toggleBtn && content) {
        toggleBtn.addEventListener('click', () => {
            const isHidden = content.style.display === 'none';
            content.style.display = isHidden ? 'block' : 'none';
            
            const icon = toggleBtn.querySelector('[data-lucide]');
            if (icon) {
                icon.setAttribute('data-lucide', isHidden ? 'chevron-up' : 'chevron-down');
                lucide.createIcons();
            }
        });
    }
    
    // Verificar si Coqui TTS está disponible
    checkTTSAvailability();
    
    // Selección de voz
    const voiceRadios = document.querySelectorAll('input[name="voice"]');
    voiceRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            VOICE_CONFIG.selectedVoice = e.target.value;
            console.log('🎤 Voz seleccionada:', VOICE_CONFIG.selectedVoice);
        });
    });
    
    // Botones de test de voz
    const testButtons = document.querySelectorAll('.btn-test-voice');
    testButtons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const voiceId = btn.dataset.voice;
            await testVoice(voiceId);
        });
    });
    
    // Upload área
    const uploadArea = document.getElementById('voice-upload-area');
    const fileInput = document.getElementById('voice-file-input');
    
    if (uploadArea && fileInput) {
        // Click en área abre selector
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        // Drag & drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', async (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('audio/')) {
                await cloneVoice(file);
            } else {
                alert('Por favor, sube un archivo de audio');
            }
        });
        
        // File input change
        fileInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (file) {
                await cloneVoice(file);
            }
        });
    }
}

/**
 * Probar una voz con texto de ejemplo
 */
async function testVoice(voiceId) {
    console.log(`🔊 Probando voz: ${voiceId}`);
    
    try {
        const testText = '¡Hola! Esta es una demostración de mi voz.';
        
        // Usar la función de TTS pero con la voz específica
        if (typeof speakText === 'function') {
            await speakText(testText, null, voiceId);
        } else {
            console.error('❌ speakText no disponible');
        }
        
    } catch (error) {
        console.error('❌ Error al probar voz:', error);
    }
}

/**
 * Clonar una voz desde archivo
 */
async function cloneVoice(audioFile) {
    console.log('🎭 Clonando voz desde:', audioFile.name);
    
    // Mostrar status
    const statusDiv = document.getElementById('voice-clone-status');
    const messageSpan = document.getElementById('clone-message');
    
    if (statusDiv) statusDiv.style.display = 'block';
    if (messageSpan) messageSpan.textContent = 'Procesando audio...';
    
    try {
        // Crear FormData
        const formData = new FormData();
        formData.append('audio', audioFile);
        formData.append('name', 'Mi Voz Personalizada');
        
        // Enviar al servidor
        const endpoint = VOICE_CONFIG.isLocal 
            ? `${VOICE_CONFIG.baseUrl}/clone`
            : `/api/tts-clone`;
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            console.log('✅ Voz clonada:', data.voice_id);
            
            // Actualizar mensaje
            if (messageSpan) {
                messageSpan.textContent = `✅ Voz "${data.name}" clonada exitosamente`;
            }
            
            // Agregar a voces custom
            VOICE_CONFIG.customVoices[data.voice_id] = {
                name: data.name
            };
            
            // Actualizar UI
            await updateCustomVoicesList();
            
            // Auto-seleccionar la nueva voz
            VOICE_CONFIG.selectedVoice = data.voice_id;
            
            // Ocultar status después de 3 seg
            setTimeout(() => {
                if (statusDiv) statusDiv.style.display = 'none';
            }, 3000);
            
        } else {
            throw new Error(data.error || 'Error desconocido');
        }
        
    } catch (error) {
        console.error('❌ Error al clonar voz:', error);
        
        if (messageSpan) {
            messageSpan.textContent = `❌ Error: ${error.message}`;
        }
        
        setTimeout(() => {
            if (statusDiv) statusDiv.style.display = 'none';
        }, 3000);
    }
}

/**
 * Actualizar lista de voces clonadas
 */
async function updateCustomVoicesList() {
    const container = document.getElementById('custom-voices-container');
    const listDiv = document.getElementById('custom-voices-list');
    
    if (!container || !listDiv) return;
    
    // Si hay voces custom, mostrar lista
    const customCount = Object.keys(VOICE_CONFIG.customVoices).length;
    
    if (customCount > 0) {
        listDiv.style.display = 'block';
        
        container.innerHTML = Object.entries(VOICE_CONFIG.customVoices).map(([id, info]) => `
            <label class="voice-option">
                <input type="radio" name="voice" value="${id}">
                <div class="voice-card">
                    <div class="voice-icon">🎭</div>
                    <div class="voice-info">
                        <strong>${info.name}</strong>
                        <span>Voz personalizada</span>
                    </div>
                    <button class="btn-test-voice" data-voice="${id}" title="Probar voz">
                        <i data-lucide="play"></i>
                    </button>
                </div>
            </label>
        `).join('');
        
        // Re-setup event listeners para las nuevas voces
        setupVoiceEvents();
        
        // Reinicializar iconos
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
    } else {
        listDiv.style.display = 'none';
    }
}

/**
 * Obtener voz seleccionada
 */
function getSelectedVoice() {
    return VOICE_CONFIG.selectedVoice;
}

/**
 * Verificar si Coqui TTS está disponible
 */
async function checkTTSAvailability() {
    try {
        const endpoint = VOICE_CONFIG.isLocal 
            ? `${VOICE_CONFIG.baseUrl}/health`
            : '/api/tts';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: 'test', language: 'es' })
        });
        
        const banner = document.getElementById('tts-status-banner');
        
        if (!response.ok || response.status === 503) {
            // TTS no disponible, mostrar banner
            if (banner) {
                banner.style.display = 'flex';
            }
            console.warn('⚠️ Coqui TTS no disponible, usando Web Speech API');
        } else {
            // TTS disponible, ocultar banner
            if (banner) {
                banner.style.display = 'none';
            }
            console.log('✅ Coqui TTS disponible');
        }
    } catch (error) {
        // Error al conectar, mostrar banner
        const banner = document.getElementById('tts-status-banner');
        if (banner) {
            banner.style.display = 'flex';
        }
        console.warn('⚠️ No se pudo verificar Coqui TTS:', error.message);
    }
}

// Exportar funciones
window.initVoiceSelector = initVoiceSelector;
window.getSelectedVoice = getSelectedVoice;
window.testVoice = testVoice;

console.log('🎤 Voice Selector Module cargado');
console.log('✅ Funciones disponibles: initVoiceSelector, getSelectedVoice, testVoice');

