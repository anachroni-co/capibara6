// Chat page para interactuar con el modelo capibara6 a través del backend MCP

class Capibara6ChatPage {
    constructor() {
        this.backendUrl = typeof CHATBOT_CONFIG !== 'undefined'
            ? CHATBOT_CONFIG.BACKEND_URL
            : (window.location.hostname === 'localhost'
                ? 'http://localhost:5000'
                : window.location.origin);  // Usar el mismo origen que el frontend
        
        this.messages = [];
        this.chats = [];
        this.currentChatId = null;
        this.isConnected = false;
        this.isProcessing = false;
        this.sidebarCollapsed = false;
        
        // Elementos del DOM
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        // Asegurar autofocus en dispositivos móviles
        this.setupAutoFocus();
        this.chatSendBtn = document.getElementById('chat-send-btn');
        this.statusIndicator = document.getElementById('status-indicator');
        this.statusText = document.getElementById('status-text');
        this.clearChatBtn = document.getElementById('clear-chat-btn');
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebar-toggle');
        this.sidebarToggleMobile = document.getElementById('sidebar-toggle-mobile');
        this.sidebarOverlay = document.getElementById('sidebar-overlay');
        this.newChatBtn = document.getElementById('new-chat-btn');
        this.chatList = document.getElementById('chat-list');
        this.profileMenuBtn = document.getElementById('profile-menu-btn');
        this.profileMenu = document.getElementById('profile-menu');
        this.settingsModal = document.getElementById('settings-modal');
        
        this.init();
        this.setupAutoFocus();
    }
    
    async init() {
        // Cargar configuración del usuario
        this.loadUserSettings();
        this.loadUserProfile();
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Verificar conexión con el backend
        await this.checkConnection();

        // Inicializar servicios integrados
        this.initTTSService();
        this.initMCPService();
        this.initRAGService();
        this.initN8NService();
        this.initModelVisualization();
        this.initEntropyMonitor();
        
        // Cargar chats guardados
        this.loadChats();
        
        // Cargar mensajes del chat actual
        this.loadMessages();
    }
    
    setupEventListeners() {
        // Enviar mensaje
        this.chatSendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize del textarea
        this.chatInput.addEventListener('input', () => {
            this.chatInput.style.height = 'auto';
            this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 200) + 'px';
        });
        
        // Sidebar
        this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        this.sidebarToggleMobile.addEventListener('click', () => this.toggleSidebarMobile());
        this.sidebarOverlay.addEventListener('click', () => this.closeSidebarMobile());
        
        // Nuevo chat
        this.newChatBtn.addEventListener('click', () => this.createNewChat());
        
        // Limpiar chat
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        
        // Perfil
        this.profileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleProfileMenu();
        });
        
        // Cerrar menú de perfil al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!this.profileMenu.contains(e.target) && !this.profileMenuBtn.contains(e.target)) {
                this.profileMenu.classList.remove('active');
            }
        });
        
        // Configuración
        document.getElementById('profile-settings-btn').addEventListener('click', () => {
            this.openSettings();
            this.profileMenu.classList.remove('active');
        });
        
        document.getElementById('settings-modal-close').addEventListener('click', () => {
            this.closeSettings();
        });
        
        document.getElementById('settings-save-btn').addEventListener('click', () => {
            this.saveSettings();
        });
        
        // Temperatura slider
        const tempSlider = document.getElementById('temperature-setting');
        const tempValue = document.getElementById('temperature-value');
        tempSlider.addEventListener('input', (e) => {
            tempValue.textContent = e.target.value;
        });
        
        // Crear proyecto (acción separada)
        document.getElementById('create-project-btn').addEventListener('click', () => {
            this.openCreateProjectModal();
        });
        
        // Modales - Crear Proyecto
        document.getElementById('create-project-modal-close').addEventListener('click', () => {
            this.closeCreateProjectModal();
        });
        
        document.getElementById('create-project-cancel-btn').addEventListener('click', () => {
            this.closeCreateProjectModal();
        });
        
        document.getElementById('create-project-submit-btn').addEventListener('click', () => {
            this.createProject();
        });
        
        // Modales - Seleccionar Proyecto
        document.getElementById('select-project-modal-close').addEventListener('click', () => {
            this.closeSelectProjectModal();
        });
        
        document.getElementById('select-project-cancel-btn').addEventListener('click', () => {
            this.closeSelectProjectModal();
        });
        
        // Modales - Seleccionar Chat para Unir
        document.getElementById('select-chat-merge-modal-close').addEventListener('click', () => {
            this.closeSelectChatMergeModal();
        });
        
        document.getElementById('select-chat-merge-cancel-btn').addEventListener('click', () => {
            this.closeSelectChatMergeModal();
        });
        
        
        // Modal - Cuenta
        document.getElementById('profile-account-btn').addEventListener('click', () => {
            this.openAccountModal();
            this.profileMenu.classList.remove('active');
        });
        
        // Tabs del modal de cuenta
        document.querySelectorAll('.account-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.dataset.tab;
                this.switchAccountTab(tabName);
            });
        });
        
        // Importadores de redes sociales
        document.querySelectorAll('.btn-social-import').forEach(btn => {
            btn.addEventListener('click', () => {
                const platform = btn.dataset.platform;
                const fileInput = document.getElementById(`${platform}-file-input`);
                fileInput.click();
            });
        });
        
        // File inputs para importación
        ['twitter', 'linkedin', 'instagram', 'github'].forEach(platform => {
            const fileInput = document.getElementById(`${platform}-file-input`);
            if (fileInput) {
                fileInput.addEventListener('change', (e) => {
                    this.handleSocialImport(platform, e.target.files[0]);
                });
            }
        });
        
        // Generar gemelo digital
        document.getElementById('generate-twin-btn').addEventListener('click', () => {
            this.generateDigitalTwin();
        });
        
        document.getElementById('account-modal-close').addEventListener('click', () => {
            this.closeAccountModal();
        });
        
        document.getElementById('account-cancel-btn').addEventListener('click', () => {
            this.closeAccountModal();
        });
        
        document.getElementById('account-save-btn').addEventListener('click', () => {
            this.saveAccount();
        });
        
        document.getElementById('change-password-btn').addEventListener('click', () => {
            this.changePassword();
        });
    }
    
    toggleSidebar() {
        this.sidebarCollapsed = !this.sidebarCollapsed;
        if (this.sidebarCollapsed) {
            this.sidebar.classList.add('collapsed');
        } else {
            this.sidebar.classList.remove('collapsed');
        }
        this.saveUserSettings();
    }
    
    toggleSidebarMobile() {
        this.sidebar.classList.toggle('active');
        this.sidebarOverlay.classList.toggle('active');
    }
    
    closeSidebarMobile() {
        this.sidebar.classList.remove('active');
        this.sidebarOverlay.classList.remove('active');
    }
    
    toggleProfileMenu() {
        this.profileMenu.classList.toggle('active');
    }
    
    createNewChat() {
        this.currentChatId = null;
        this.messages = [];
        this.chatMessages.innerHTML = `
            <div class="chat-message bot-message">
                <div class="message-avatar">
                    <div class="avatar-gradient">
                        <i data-lucide="bot" style="width: 24px; height: 24px;"></i>
                    </div>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        <p>¡Hola! Soy capibara6, un modelo de IA híbrido Transformer-Mamba. ¿En qué puedo ayudarte hoy?</p>
                    </div>
                    <div class="message-time">${new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            </div>
        `;
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        this.closeSidebarMobile();
    }
    
    
    async checkConnection() {
        try {
            // Asegurar que tenemos la URL correcta del backend
            const backendUrl = typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.BACKEND_URL
                ? CHATBOT_CONFIG.BACKEND_URL
                : this.backendUrl;

            // Función helper para crear timeout compatible
            const createTimeoutSignal = (ms) => {
                const controller = new AbortController();
                setTimeout(() => controller.abort(), ms);
                return controller.signal;
            };

            // Lista de endpoints a probar (en orden de preferencia, con lógica de CHATBOT_CONFIG)
            const endpointsToTry = [];

            // 1. Endpoint de classify (tu preferencia)
            if (typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.ENDPOINTS?.AI_CLASSIFY) {
                endpointsToTry.push({
                    path: CHATBOT_CONFIG.ENDPOINTS.AI_CLASSIFY,
                    method: 'POST',
                    body: { prompt: 'ping' },
                    description: 'AI Classify'
                });
            } else {
                endpointsToTry.push({
                    path: '/api/ai/classify',
                    method: 'POST',
                    body: { prompt: 'ping' },
                    description: 'AI Classify (fallback)'
                });
            }

            // 2. Endpoint de health (tu fallback)
            if (typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.ENDPOINTS?.HEALTH) {
                endpointsToTry.push({
                    path: CHATBOT_CONFIG.ENDPOINTS.HEALTH,
                    method: 'GET',
                    body: null,
                    description: 'Health (config)'
                });
            } else {
                endpointsToTry.push({
                    path: '/api/health',
                    method: 'GET',
                    body: null,
                    description: 'Health (fallback 1)'
                });
            }

            // 3. Health alternativo y root (del Incoming, para robustez)
            endpointsToTry.push(
                { path: '/health', method: 'GET', body: null, description: 'Health (fallback 2)' },
                { path: '/', method: 'GET', body: null, description: 'Root' }
            );

            // Intentar cada endpoint
            for (const endpoint of endpointsToTry) {
                const fullUrl = `${backendUrl}${endpoint.path}`;
                try {
                    const fetchOptions = {
                        method: endpoint.method,
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'  // ✅ Tu mejora: forzar JSON
                        },
                        signal: createTimeoutSignal(5000)
                    };
                    if (endpoint.body) {
                        fetchOptions.body = JSON.stringify(endpoint.body);
                    }
                    const response = await fetch(fullUrl, fetchOptions);
                    if (response.ok || response.status === 200) {
                        const responseData = await response.json().catch(() => ({}));
                        this.isConnected = true;
                        this.updateStatus('Conectado', 'success');
                        return;
                    }
                } catch (endpointError) {
                    // Silenciar logs redundantes para endpoints fallback
                    continue;
                }
            }

            // Si todos los endpoints fallan
            this.isConnected = false;
            this.updateStatus('Desconectado', 'error');
            this.showError('No se pudo conectar con el backend. Verifica:\n1. Que el servidor esté corriendo\n2. Que el firewall permita conexiones');

        } catch (error) {
            const backendUrl = typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.BACKEND_URL
                ? CHATBOT_CONFIG.BACKEND_URL
                : this.backendUrl;

            if (error.name === 'AbortError' || error.message?.includes('aborted')) {
                this.isConnected = false;
                this.updateStatus('Timeout', 'error');
                this.showError('El backend tardó demasiado en responder. Verifica que el servidor esté activo.');
            } else if (error.name === 'TypeError' && (error.message.includes('Failed to fetch') || error.message.includes('NetworkError'))) {
                this.isConnected = false;
                this.updateStatus('Error de conexión', 'error');
                let errorMsg = `No se pudo conectar con el backend en ${backendUrl}.\n`;
                if (backendUrl.includes('localhost:8001')) {
                    errorMsg += 'Verifica que el proxy esté corriendo y el backend remoto esté activo.';
                } else {
                    errorMsg += 'Posibles causas: servidor no corriendo, firewall, o configuración incorrecta.';
                }
                this.showError(errorMsg);
            } else {
                this.isConnected = false;
                this.updateStatus('Error de conexión', 'error');
                this.showError(`Error de conexión: ${error.message || error}`);
            }
        }
    }
    
    updateStatus(text, type) {
        this.statusText.textContent = text;
        const colors = {
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'connecting': '#6366f1'
        };
        this.statusIndicator.style.background = colors[type] || colors.connecting;
        this.statusIndicator.style.boxShadow = `0 0 8px ${colors[type] || colors.connecting}`;
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isProcessing) return;

        if (!this.isConnected) {
            this.showError('No hay conexión con el servidor. Por favor, verifica tu conexión.');
            return;
        }

        // Crear chat si no existe
        if (!this.currentChatId) {
            this.currentChatId = 'chat_' + Date.now();
            this.saveChats();
        }

        // Agregar mensaje del usuario
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';

        // Deshabilitar input mientras se procesa
        this.setProcessing(true);

        // Mostrar indicador de escritura
        const typingIndicator = this.showTypingIndicator();

        try {
            // Enviar mensaje al backend usando MCP
            const response = await this.sendToBackend(message);

            // Remover indicador de escritura
            this.removeTypingIndicator(typingIndicator);

            // Agregar respuesta del bot
            if (response && response.content) {
                this.addMessage(response.content, 'bot');
                // Mostrar controles TTS cuando hay respuesta del bot
                if (this.showTTSControls) {
                    this.showTTSControls();
                }
            } else {
                throw new Error('Respuesta inválida del servidor');
            }

            // Actualizar lista de chats
            this.updateChatInList();

        } catch (error) {
            this.removeTypingIndicator(typingIndicator);

            // Mensaje de error más descriptivo
            let errorMessage = 'Lo siento, ocurrió un error al procesar tu mensaje.';
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                errorMessage += ' No se pudo conectar con el servidor.';
            } else if (error.message.includes('HTTP error!')) {
                errorMessage += ` El servidor respondió con error: ${error.message}`;
            } else {
                errorMessage += ` Detalles: ${error.message}`;
            }

            this.addMessage(
                errorMessage,
                'bot',
                true
            );
            console.debug('Message sending failed:', error.message); // Solo log debug
        } finally {
            this.setProcessing(false);
        }
    }
    
    async sendToBackend(message) {
        // Determinar endpoint correcto según el entorno - MODIFICADO PARA USAR API CHAT COMPATIBLE
        let endpoint;
        if (this.backendUrl.includes('capibara6.com') || this.backendUrl.includes('vercel.app')) {
            // En producción (Vercel), usar el endpoint de chat compatible
            endpoint = `${this.backendUrl}/api/chat`;
        } else if (typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.ENDPOINTS.AI_GENERATE) {
            // Modificar para usar chat en lugar de ai/generate
            endpoint = this.backendUrl + '/api/chat';
        } else {
            // Fallback para desarrollo - USAR API CHAT
            endpoint = `${this.backendUrl}/api/chat`;
        }

        // Adaptar el formato de la solicitud al esperado por el gateway server
        const chatPayload = {
            message: message,
            model: 'phi4_fast', // Especificar modelo para evitar problemas
            temperature: 0.7,
            max_tokens: 200,
            use_semantic_router: false, // Desactivar temporalmente para estabilidad
            context: this.getConversationContext(),
        };

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(chatPayload)
        });

        // Intentar leer el cuerpo como JSON, pero manejar posibles errores
        let data;
        try {
            data = await response.json();
        } catch (parseError) {
            // Si no es JSON, leer como texto
            const responseText = await response.text();
            data = { error: `Parse error: ${parseError.message}`, raw_response: responseText };
        }

        // Verificar si la respuesta es exitosa
        // En producción con Vercel, los endpoints pueden no tener propiedad 'success'
        // así que verificamos principalmente que no haya un error explícito
        const isErrorResponse = response.status >= 400 ||
            (data.error || data.detail || data.message) ||
            (response.status === 200 && Object.keys(data).length === 0);

        if (isErrorResponse) {
            throw new Error(data.error || data.detail || data.message || `HTTP error! status: ${response.status}, endpoint: ${endpoint}`);
        }

        // Asegurarse de que la estructura de respuesta sea correcta
        // El endpoint ahora devuelve el formato del gateway server
        return {
            content: data.response || data.content || data.choices?.[0]?.message?.content || data,
            modelUsed: data.model || data.modelUsed || 'unknown',
            metadata: {
                tokenCount: data.tokens || data.usage?.total_tokens,
                processingTime: data.latency_ms || data.processing_time || null,
                classification: data.classification || 'general',
            }
        };
    }
    
    getConversationContext() {
        // Obtener los últimos mensajes para contexto
        const recentMessages = this.messages.slice(-10);
        return recentMessages.map(msg => ({
            role: msg.type === 'user' ? 'user' : 'assistant',
            content: msg.text
        }));
    }
    
    addMessage(text, type, isError = false) {
        const message = {
            text: text,
            type: type,
            timestamp: new Date(),
            isError: isError
        };
        
        this.messages.push(message);
        this.saveMessages();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}-message`;
        if (isError) {
            messageDiv.classList.add('error');
        }
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        const avatarGradient = document.createElement('div');
        avatarGradient.className = 'avatar-gradient';
        avatarGradient.innerHTML = type === 'bot' 
            ? '<i data-lucide="bot" style="width: 24px; height: 24px;"></i>'
            : '<i data-lucide="user" style="width: 24px; height: 24px;"></i>';
        avatar.appendChild(avatarGradient);
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        const textP = document.createElement('p');
        textP.textContent = text;
        textDiv.appendChild(textP);
        content.appendChild(textDiv);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = message.timestamp.toLocaleTimeString('es-ES', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        content.appendChild(timeDiv);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Inicializar iconos de Lucide
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        // Scroll al final
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message bot-message';
        messageDiv.appendChild(typingDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        
        return messageDiv;
    }
    
    removeTypingIndicator(typingElement) {
        if (typingElement && typingElement.parentNode) {
            typingElement.remove();
        }
    }
    
    setProcessing(processing) {
        this.isProcessing = processing;
        this.chatInput.disabled = processing;
        this.chatSendBtn.disabled = processing;
        
        if (processing) {
            this.chatSendBtn.innerHTML = '<span>Procesando...</span>';
        } else {
            this.chatSendBtn.innerHTML = '<span>Enviar</span><i data-lucide="send" style="width: 20px; height: 20px;"></i>';
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        // Insertar después del header
        const chatMain = document.querySelector('.chat-main-content');
        chatMain.insertBefore(errorDiv, chatMain.children[1]);
        
        // Remover después de 5 segundos
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    clearChat() {
        if (confirm('¿Estás seguro de que quieres limpiar toda la conversación?')) {
            this.createNewChat();
        }
    }
    
    // Gestión de chats
    loadChats() {
        try {
            const saved = localStorage.getItem('capibara6_chats');
            if (saved) {
                this.chats = JSON.parse(saved);
                this.renderChatList();
            }
        } catch (error) {
            console.warn('Error cargando chats:', error);
        }
    }
    
    saveChats() {
        try {
            if (this.currentChatId) {
                const chatIndex = this.chats.findIndex(c => c.id === this.currentChatId);
                const chatData = {
                    id: this.currentChatId,
                    title: this.messages[0]?.text?.substring(0, 50) || 'Nueva conversación',
                    lastMessage: this.messages[this.messages.length - 1]?.text?.substring(0, 100),
                    timestamp: new Date().toISOString(),
                    messageCount: this.messages.length
                };
                
                if (chatIndex >= 0) {
                    this.chats[chatIndex] = chatData;
                } else {
                    this.chats.unshift(chatData);
                }
                
                // Mantener solo los últimos 20 chats
                this.chats = this.chats.slice(0, 20);
                localStorage.setItem('capibara6_chats', JSON.stringify(this.chats));
                this.renderChatList();
            }
        } catch (error) {
            console.warn('Error guardando chats:', error);
        }
    }
    
    renderChatList() {
        this.chatList.innerHTML = '';
        
        if (this.chats.length === 0) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'empty-chat-list';
            emptyDiv.style.cssText = 'padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.9rem;';
            emptyDiv.textContent = 'No hay conversaciones anteriores';
            this.chatList.appendChild(emptyDiv);
            return;
        }
        
        this.chats.forEach(chat => {
            const chatItem = document.createElement('div');
            chatItem.className = 'chat-item';
            chatItem.dataset.chatId = chat.id;
            if (chat.id === this.currentChatId) {
                chatItem.classList.add('active');
            }
            
            chatItem.innerHTML = `
                <div class="chat-item-icon">
                    <i data-lucide="message-circle" style="width: 18px; height: 18px;"></i>
                </div>
                <div class="chat-item-content">
                    <div class="chat-item-title">${chat.title || 'Chat sin título'}</div>
                    <div class="chat-item-time">${new Date(chat.timestamp || chat.createdAt || Date.now()).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })}</div>
                </div>
                <div class="chat-item-menu">
                    <button class="chat-menu-btn" data-action="add-to-project" title="Añadir a proyecto">
                        <i data-lucide="folder-plus" style="width: 16px; height: 16px;"></i>
                    </button>
                    <button class="chat-menu-btn" data-action="merge" title="Unir con otro chat">
                        <i data-lucide="git-merge" style="width: 16px; height: 16px;"></i>
                    </button>
                    <button class="chat-menu-btn chat-menu-btn-danger" data-action="delete" title="Borrar chat">
                        <i data-lucide="trash-2" style="width: 16px; height: 16px;"></i>
                    </button>
                </div>
            `;
            
            // Click principal para cargar el chat
            chatItem.querySelector('.chat-item-content').addEventListener('click', (e) => {
                e.stopPropagation();
                this.loadChat(chat.id);
            });
            
            // Event listeners para el menú contextual
            const menuBtns = chatItem.querySelectorAll('.chat-menu-btn');
            menuBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const action = btn.dataset.action;
                    const chatId = chatItem.dataset.chatId;
                    
                    if (action === 'add-to-project') {
                        this.addChatToProject(chatId);
                    } else if (action === 'merge') {
                        this.mergeChatWithOther(chatId);
                    } else if (action === 'delete') {
                        this.deleteChat(chatId);
                    }
                });
            });
            
            this.chatList.appendChild(chatItem);
        });
        
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    updateChatInList() {
        this.saveChats();
    }
    
    loadChat(chatId) {
        // Por ahora, solo actualizamos el ID actual
        // En una implementación completa, cargaríamos los mensajes del chat
        this.currentChatId = chatId;
        this.renderChatList();
        this.closeSidebarMobile();
    }
    
    // Configuración
    loadUserSettings() {
        try {
            const settings = localStorage.getItem('capibara6_settings');
            if (settings) {
                const parsed = JSON.parse(settings);
                if (parsed.sidebarCollapsed) {
                    this.sidebarCollapsed = parsed.sidebarCollapsed;
                    if (this.sidebarCollapsed) {
                        this.sidebar.classList.add('collapsed');
                    }
                }
            }
        } catch (error) {
            console.warn('Error cargando configuración:', error);
        }
    }
    
    saveUserSettings() {
        try {
            const settings = {
                sidebarCollapsed: this.sidebarCollapsed
            };
            localStorage.setItem('capibara6_settings', JSON.stringify(settings));
        } catch (error) {
            console.warn('Error guardando configuración:', error);
        }
    }
    
    loadUserProfile() {
        try {
            const profile = localStorage.getItem('capibara6_profile');
            if (profile) {
                const parsed = JSON.parse(profile);
                if (parsed.name) {
                    document.getElementById('user-name').textContent = parsed.name;
                }
                if (parsed.email) {
                    document.getElementById('user-email').textContent = parsed.email;
                }
            }
        } catch (error) {
            console.warn('Error cargando perfil:', error);
        }
    }
    
    openSettings() {
        this.settingsModal.classList.add('active');
    }
    
    closeSettings() {
        this.settingsModal.classList.remove('active');
    }
    
    saveSettings() {
        // Guardar configuración
        const settings = {
            temperature: document.getElementById('temperature-setting').value,
            maxTokens: document.getElementById('max-tokens-setting').value,
            soundNotifications: document.getElementById('sound-notifications').checked,
            autoScroll: document.getElementById('auto-scroll').checked
        };
        
        try {
            localStorage.setItem('capibara6_chat_settings', JSON.stringify(settings));
            this.closeSettings();
            // Mostrar confirmación
            alert('Configuración guardada correctamente');
        } catch (error) {
            console.error('Error guardando configuración:', error);
            alert('Error al guardar la configuración');
        }
    }
    
    saveMessages() {
        try {
            if (this.currentChatId) {
                const chatData = {
                    id: this.currentChatId,
                    messages: this.messages
                };
                localStorage.setItem(`capibara6_chat_${this.currentChatId}`, JSON.stringify(chatData));
            }
        } catch (error) {
            console.warn('Error guardando mensajes:', error);
        }
    }
    
    loadMessages() {
        try {
            if (this.currentChatId) {
                const saved = localStorage.getItem(`capibara6_chat_${this.currentChatId}`);
                if (saved) {
                    const chatData = JSON.parse(saved);
                    this.messages = chatData.messages || [];
                    
                    // Renderizar mensajes
                    this.chatMessages.innerHTML = '';
                    this.messages.forEach(msg => {
                        this.addMessage(msg.text, msg.type, msg.isError);
                    });
                }
            }
        } catch (error) {
            console.warn('Error cargando mensajes:', error);
        }
    }
    
    // ============================================
    // Inicialización de Servicios Integrados
    // ============================================
    
    initTTSService() {
        try {
            if (typeof TTS_CONFIG !== 'undefined') {
                const ttsControls = document.getElementById('tts-controls');
                const ttsPlayBtn = document.getElementById('tts-play-btn');
                const ttsPauseBtn = document.getElementById('tts-pause-btn');
                const ttsStopBtn = document.getElementById('tts-stop-btn');
                const ttsSpeedSlider = document.getElementById('tts-speed');
                const ttsSpeedValue = document.getElementById('tts-speed-value');

                if (ttsControls && ttsPlayBtn) {
                    // Mostrar controles TTS cuando hay un mensaje del bot
                    this.showTTSControls = () => {
                        ttsControls.style.display = 'flex';
                        if (typeof lucide !== 'undefined') {
                            lucide.createIcons();
                        }
                    };

                    // Ocultar controles TTS
                    this.hideTTSControls = () => {
                        ttsControls.style.display = 'none';
                    };

                    // Configurar controles
                    if (ttsPlayBtn) {
                        ttsPlayBtn.addEventListener('click', () => {
                            const lastBotMessage = Array.from(this.chatMessages.querySelectorAll('.bot-message .message-text')).pop();
                            if (lastBotMessage) {
                                const text = lastBotMessage.textContent;
                                if (typeof speakText === 'function') {
                                    speakText(text);
                                    ttsPlayBtn.style.display = 'none';
                                    ttsPauseBtn.style.display = 'flex';
                                    ttsStopBtn.style.display = 'flex';
                                }
                            }
                        });
                    }

                    if (ttsPauseBtn) {
                        ttsPauseBtn.addEventListener('click', () => {
                            if (typeof window.speechSynthesis !== 'undefined') {
                                window.speechSynthesis.pause();
                                ttsPlayBtn.style.display = 'flex';
                                ttsPauseBtn.style.display = 'none';
                            }
                        });
                    }

                    if (ttsStopBtn) {
                        ttsStopBtn.addEventListener('click', () => {
                            if (typeof window.speechSynthesis !== 'undefined') {
                                window.speechSynthesis.cancel();
                                ttsPlayBtn.style.display = 'flex';
                                ttsPauseBtn.style.display = 'none';
                                ttsStopBtn.style.display = 'none';
                            }
                        });
                    }

                    if (ttsSpeedSlider && ttsSpeedValue) {
                        ttsSpeedSlider.addEventListener('input', (e) => {
                            const speed = parseFloat(e.target.value);
                            ttsSpeedValue.textContent = speed.toFixed(1) + 'x';
                            if (typeof TTS_CONFIG !== 'undefined') {
                                TTS_CONFIG.rate = speed;
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.debug('TTS service could not be initialized:', error.message);
        }
    }
    
    initMCPService() {
        try {
            const mcpIndicator = document.getElementById('mcp-indicator');
            const mcpStatusText = document.getElementById('mcp-status-text');

            if (mcpIndicator) {
                // Verificar estado usando checkSmartMCPHealth si está disponible
                if (typeof checkSmartMCPHealth === 'function') {
                    checkSmartMCPHealth().then(isActive => {
                        if (isActive) {
                            mcpIndicator.style.display = 'flex';
                            mcpIndicator.classList.add('active');
                            if (mcpStatusText) {
                                mcpStatusText.textContent = 'MCP Activo';
                            }
                        } else {
                            mcpIndicator.style.display = 'none';
                        }
                    }).catch(() => {
                        mcpIndicator.style.display = 'none';
                    });
                } else if (typeof initMCP === 'function') {
                    // Usar initMCP de mcp-integration.js
                    initMCP().then(() => {
                        if (typeof mcpAvailable !== 'undefined' && mcpAvailable) {
                            mcpIndicator.style.display = 'flex';
                            mcpIndicator.classList.add('active');
                            if (mcpStatusText) {
                                mcpStatusText.textContent = 'MCP Activo';
                            }
                        }
                    }).catch(() => {
                        mcpIndicator.style.display = 'none';
                    });
                }
            }
        } catch (error) {
            console.debug('MCP service could not be initialized:', error.message);
        }
    }
    
    initRAGService() {
        try {
            if (typeof Capibara6API !== 'undefined') {
                const ragPanel = document.getElementById('rag-panel');
                const ragPanelClose = document.getElementById('rag-panel-close');
                const ragSearchBtnSidebar = document.getElementById('rag-search-btn-sidebar');
                const ragSearchBtn = document.getElementById('rag-search-btn');
                const ragSearchInput = document.getElementById('rag-search-input');
                const ragResults = document.getElementById('rag-results');

                if (ragPanel && ragSearchBtnSidebar) {
                    const ragUrl = typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.SERVICE_URLS?.RAG_API
                        ? CHATBOT_CONFIG.SERVICE_URLS.RAG_API
                        : 'http://localhost:8000';

                    this.ragClient = new Capibara6API(ragUrl);

                    // Abrir panel RAG
                    ragSearchBtnSidebar.addEventListener('click', () => {
                        ragPanel.classList.add('open');
                        if (typeof lucide !== 'undefined') {
                            lucide.createIcons();
                        }
                    });

                    // Cerrar panel RAG
                    if (ragPanelClose) {
                        ragPanelClose.addEventListener('click', () => {
                            ragPanel.classList.remove('open');
                        });
                    }

                    // Realizar búsqueda RAG
                    if (ragSearchBtn && ragSearchInput) {
                        const performRAGSearch = async () => {
                            const query = ragSearchInput.value.trim();
                            if (!query) return;

                            const searchType = document.querySelector('input[name="rag-search-type"]:checked')?.value || 'rag';

                            ragResults.innerHTML = '<div class="rag-empty-state"><div class="spinner"></div><p>Buscando...</p></div>';

                            try {
                                let results;
                                if (searchType === 'rag') {
                                    results = await this.ragClient.ragSearch(query, 5, true);
                                } else if (searchType === 'semantic') {
                                    results = await this.ragClient.semanticSearch(query, null, 5);
                                } else {
                                    results = await this.ragClient.searchAll(query, 5);
                                }

                                this.displayRAGResults(results, ragResults, searchType);
                            } catch (error) {
                                ragResults.innerHTML = `<div class="rag-empty-state"><p style="color: var(--danger);">Error: ${error.message}</p></div>`;
                            }
                        };

                        ragSearchBtn.addEventListener('click', performRAGSearch);
                        ragSearchInput.addEventListener('keypress', (e) => {
                            if (e.key === 'Enter') {
                                performRAGSearch();
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.debug('RAG service could not be initialized:', error.message);
        }
    }
    
    displayRAGResults(results, container, searchType) {
        if (!results || (results.results && results.results.length === 0)) {
            container.innerHTML = '<div class="rag-empty-state"><p>No se encontraron resultados</p></div>';
            return;
        }
        
        let html = '';
        
        if (searchType === 'rag' && results.results) {
            // Formato RAG completo
            const allResults = [];
            for (const [collName, collResults] of Object.entries(results.results)) {
                collResults.forEach(r => {
                    allResults.push({ collection: collName, ...r });
                });
            }
            
            allResults.sort((a, b) => (b.similarity || 0) - (a.similarity || 0));
            
            allResults.forEach(result => {
                html += `
                    <div class="rag-result-item">
                        <div class="rag-result-header">
                            <span class="rag-result-type">${result.collection || 'N/A'}</span>
                            <span class="rag-result-similarity">${((result.similarity || 0) * 100).toFixed(1)}%</span>
                        </div>
                        <div class="rag-result-content">${result.document || result.content || 'Sin contenido'}</div>
                        <div class="rag-result-meta">${result.full_data?.created_at ? new Date(result.full_data.created_at).toLocaleDateString() : ''}</div>
                    </div>
                `;
            });
        } else if (results.results && Array.isArray(results.results)) {
            // Formato semántico o all
            results.results.forEach(result => {
                html += `
                    <div class="rag-result-item">
                        <div class="rag-result-header">
                            <span class="rag-result-type">${result.collection || 'N/A'}</span>
                            <span class="rag-result-similarity">${((result.similarity || 0) * 100).toFixed(1)}%</span>
                        </div>
                        <div class="rag-result-content">${result.document || result.content || 'Sin contenido'}</div>
                    </div>
                `;
            });
        }
        
        container.innerHTML = html || '<div class="rag-empty-state"><p>No se encontraron resultados</p></div>';
    }
    
    initN8NService() {
        try {
            if (typeof N8NManager !== 'undefined') {
                const n8nWidget = document.getElementById('n8n-widget');
                const n8nStatus = document.getElementById('n8n-status');
                const n8nWorkflowsList = document.getElementById('n8n-workflows-list');
                const n8nDashboardBtn = document.getElementById('n8n-dashboard-btn');

                if (n8nWidget) {
                    const n8nUrl = typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.SERVICE_URLS?.N8N
                        ? CHATBOT_CONFIG.SERVICE_URLS.N8N
                        : 'http://localhost:5678';

                    this.n8nManager = new N8NManager({
                        baseURL: this.backendUrl,
                        n8nURL: n8nUrl
                    });

                    // Verificar estado N8n
                    this.n8nManager.checkN8NStatus().then(status => {
                        if (status && status.available) {
                            if (n8nStatus) {
                                n8nStatus.innerHTML = `
                                    <span class="status-dot"></span>
                                    <span>N8n Activo</span>
                                `;
                            }
                            this.loadN8NWorkflows();
                        } else {
                            if (n8nStatus) {
                                n8nStatus.innerHTML = `
                                    <span class="status-dot inactive"></span>
                                    <span>N8n No Disponible</span>
                                `;
                            }
                        }
                    }).catch(() => {
                        if (n8nStatus) {
                            n8nStatus.innerHTML = `
                                <span class="status-dot inactive"></span>
                                <span>N8n No Disponible</span>
                            `;
                        }
                    });

                    // Abrir dashboard N8n
                    if (n8nDashboardBtn) {
                        n8nDashboardBtn.addEventListener('click', () => {
                            if (this.n8nManager) {
                                this.n8nManager.openN8N();
                            } else {
                                window.open(n8nUrl, '_blank');
                            }
                        });
                    }
                }
            }
        } catch (error) {
            // Solo log si hay error real
            console.debug('N8n service initialization failed:', error.message);
        }
    }
    
    async loadN8NWorkflows() {
        try {
            if (this.n8nManager && document.getElementById('n8n-workflows-list')) {
                const workflowsList = document.getElementById('n8n-workflows-list');
                
                // Usar getRecommended para obtener plantillas recomendadas
                try {
                    const workflows = await this.n8nManager.getRecommended();
                    
                    if (workflows && workflows.length > 0) {
                        workflowsList.innerHTML = workflows.slice(0, 5).map(wf => `
                            <div class="n8n-workflow-item" title="${wf.description || ''}">
                                <div class="n8n-workflow-name">${wf.name || wf.title || 'Sin nombre'}</div>
                                <div class="n8n-workflow-status active">
                                    <span class="status-dot"></span>
                                    Recomendado
                                </div>
                            </div>
                        `).join('');
                    } else {
                        workflowsList.innerHTML = '<div style="padding: 0.5rem; color: var(--text-muted); font-size: 0.75rem;">No hay workflows disponibles</div>';
                    }
                } catch (error) {
                    workflowsList.innerHTML = '<div style="padding: 0.5rem; color: var(--text-muted); font-size: 0.75rem;">No se pudieron cargar workflows</div>';
                }
            }
        } catch (error) {
            console.warn('⚠️ Error cargando workflows N8n:', error);
        }
    }
    
    initModelVisualization() {
        try {
            if (typeof ModelVisualization !== 'undefined') {
                // La visualización de modelos se puede usar cuando sea necesario
                this.modelViz = new ModelVisualization();
            }
        } catch (error) {
            console.debug('Model visualization could not be initialized:', error.message);
        }
    }

    initEntropyMonitor() {
        try {
            if (typeof EntropyMonitor !== 'undefined') {
                // El monitor de entropía se puede usar cuando sea necesario
                this.entropyMonitor = new EntropyMonitor();
            }
        } catch (error) {
            console.debug('Entropy monitor could not be initialized:', error.message);
        }
    }
    
    // ============================================
    // Gestión de Proyectos y Chats
    // ============================================
    
    openCreateProjectModal() {
        const modal = document.getElementById('create-project-modal');
        modal.classList.add('active');
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    closeCreateProjectModal() {
        const modal = document.getElementById('create-project-modal');
        modal.classList.remove('active');
        // Limpiar formulario
        document.getElementById('project-name').value = '';
        document.getElementById('project-description').value = '';
        document.getElementById('project-include-current-chat').checked = false;
    }
    
    async createProject() {
        const name = document.getElementById('project-name').value.trim();
        const description = document.getElementById('project-description').value.trim();
        const includeCurrent = document.getElementById('project-include-current-chat').checked;
        
        if (!name) {
            this.showError('Por favor, ingresa un nombre para el proyecto');
            return;
        }
        
        try {
            const project = {
                id: 'project_' + Date.now(),
                name: name,
                description: description,
                createdAt: new Date().toISOString(),
                chats: includeCurrent && this.currentChatId ? [this.currentChatId] : []
            };
            
            // Guardar proyecto en localStorage
            const projects = JSON.parse(localStorage.getItem('capibara6_projects') || '[]');
            projects.push(project);
            localStorage.setItem('capibara6_projects', JSON.stringify(projects));
            
            // Si había un chat pendiente para añadir, añadirlo ahora
            if (this.pendingChatForProject) {
                project.chats.push(this.pendingChatForProject);
                localStorage.setItem('capibara6_projects', JSON.stringify(projects));
                this.pendingChatForProject = null;
                this.showSuccess(`Proyecto "${name}" creado y chat añadido exitosamente`);
            } else {
                this.showSuccess(`Proyecto "${name}" creado exitosamente`);
            }
            
            this.closeCreateProjectModal();
            console.log('✅ Proyecto creado:', project);
        } catch (error) {
            console.error('Error creando proyecto:', error);
            this.showError('Error al crear el proyecto');
        }
    }
    
    // ============================================
    // Acciones Contextuales de Chat
    // ============================================
    
    addChatToProject(chatId) {
        const projects = JSON.parse(localStorage.getItem('capibara6_projects') || '[]');
        
        if (projects.length === 0) {
            // Si no hay proyectos, abrir modal para crear uno
            this.openCreateProjectModal();
            // Guardar el chatId para añadirlo después
            this.pendingChatForProject = chatId;
            return;
        }
        
        // Mostrar selector de proyectos
        this.showProjectSelector(chatId);
    }
    
    showProjectSelector(chatId) {
        const projects = JSON.parse(localStorage.getItem('capibara6_projects') || '[]');
        
        if (projects.length === 0) {
            this.showError('No hay proyectos. Crea uno primero.');
            return;
        }
        
        const modal = document.getElementById('select-project-modal');
        const list = document.getElementById('projects-list');
        
        // Guardar chatId para usar después
        this.selectedChatForProject = chatId;
        
        list.innerHTML = projects.map((project, index) => {
            const isInProject = project.chats && project.chats.includes(chatId);
            return `
                <div class="project-item ${isInProject ? 'disabled' : ''}" data-project-index="${index}">
                    <div class="project-item-info">
                        <div class="project-item-name">${project.name}</div>
                        ${project.description ? `<div class="project-item-desc">${project.description}</div>` : ''}
                        ${isInProject ? '<span class="project-item-badge">Ya añadido</span>' : ''}
                    </div>
                    ${!isInProject ? '<i data-lucide="chevron-right" style="width: 20px; height: 20px; color: var(--text-muted);"></i>' : ''}
                </div>
            `;
        }).join('');
        
        // Event listeners
        list.querySelectorAll('.project-item:not(.disabled)').forEach(item => {
            item.addEventListener('click', () => {
                const index = parseInt(item.dataset.projectIndex);
                this.addChatToSelectedProject(chatId, index);
            });
        });
        
        modal.classList.add('active');
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    addChatToSelectedProject(chatId, projectIndex) {
        const projects = JSON.parse(localStorage.getItem('capibara6_projects') || '[]');
        const project = projects[projectIndex];
        
        if (!project.chats) {
            project.chats = [];
        }
        
        if (!project.chats.includes(chatId)) {
            project.chats.push(chatId);
            localStorage.setItem('capibara6_projects', JSON.stringify(projects));
            this.showSuccess(`Chat añadido al proyecto "${project.name}"`);
            this.closeSelectProjectModal();
        } else {
            this.showError('Este chat ya está en el proyecto');
        }
    }
    
    closeSelectProjectModal() {
        const modal = document.getElementById('select-project-modal');
        modal.classList.remove('active');
        this.selectedChatForProject = null;
    }
    
    mergeChatWithOther(chatId) {
        const chats = this.chats.filter(c => c.id !== chatId);
        
        if (chats.length === 0) {
            this.showError('No hay otros chats para unir');
            return;
        }
        
        const modal = document.getElementById('select-chat-merge-modal');
        const list = document.getElementById('chats-merge-list');
        
        // Guardar chatId origen
        this.sourceChatForMerge = chatId;
        
        list.innerHTML = chats.map(chat => `
            <div class="chat-selection-item" data-chat-id="${chat.id}">
                <div class="chat-selection-item-icon">
                    <i data-lucide="message-circle" style="width: 20px; height: 20px;"></i>
                </div>
                <div class="chat-selection-item-info">
                    <div class="chat-selection-item-name">${chat.title || 'Chat sin título'}</div>
                    <div class="chat-selection-item-time">${new Date(chat.timestamp || chat.createdAt || Date.now()).toLocaleDateString('es-ES')}</div>
                </div>
                <i data-lucide="chevron-right" style="width: 20px; height: 20px; color: var(--text-muted);"></i>
            </div>
        `).join('');
        
        // Event listeners
        list.querySelectorAll('.chat-selection-item').forEach(item => {
            item.addEventListener('click', () => {
                const targetChatId = item.dataset.chatId;
                this.performMerge(chatId, targetChatId);
                this.closeSelectChatMergeModal();
            });
        });
        
        modal.classList.add('active');
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    closeSelectChatMergeModal() {
        const modal = document.getElementById('select-chat-merge-modal');
        modal.classList.remove('active');
        this.sourceChatForMerge = null;
    }
    
    async performMerge(sourceChatId, targetChatId) {
        try {
            // Cargar mensajes de ambos chats
            const sourceData = localStorage.getItem(`capibara6_chat_${sourceChatId}`);
            const targetData = localStorage.getItem(`capibara6_chat_${targetChatId}`);
            
            if (!sourceData || !targetData) {
                this.showError('Error al cargar los chats');
                return;
            }
            
            const sourceChat = JSON.parse(sourceData);
            const targetChat = JSON.parse(targetData);
            
            // Combinar mensajes
            const allMessages = [
                ...(sourceChat.messages || []),
                ...(targetChat.messages || [])
            ];
            
            // Ordenar por timestamp
            allMessages.sort((a, b) => new Date(a.timestamp || 0) - new Date(b.timestamp || 0));
            
            // Actualizar chat destino
            targetChat.messages = allMessages;
            targetChat.mergedFrom = targetChat.mergedFrom || [];
            if (!targetChat.mergedFrom.includes(sourceChatId)) {
                targetChat.mergedFrom.push(sourceChatId);
            }
            
            localStorage.setItem(`capibara6_chat_${targetChatId}`, JSON.stringify(targetChat));
            
            // Eliminar chat origen
            localStorage.removeItem(`capibara6_chat_${sourceChatId}`);
            
            this.showSuccess('Chats unidos exitosamente');
            this.loadChats();
            
            // Si el chat actual era el origen, cargar el destino
            if (this.currentChatId === sourceChatId) {
                this.currentChatId = targetChatId;
                this.loadMessages();
            }
        } catch (error) {
            console.error('Error uniendo chats:', error);
            this.showError('Error al unir los chats');
        }
    }
    
    deleteChat(chatId) {
        const chat = this.chats.find(c => c.id === chatId);
        const chatTitle = chat?.title || 'este chat';
        
        if (confirm(`¿Estás seguro de que deseas eliminar "${chatTitle}"?\n\nEsta acción no se puede deshacer.`)) {
            try {
                localStorage.removeItem(`capibara6_chat_${chatId}`);
                
                // Si el chat actual fue eliminado, crear uno nuevo
                if (this.currentChatId === chatId) {
                    this.currentChatId = null;
                    this.messages = [];
                    this.chatMessages.innerHTML = `
                        <div class="chat-message bot-message">
                            <div class="message-avatar">
                                <div class="avatar-gradient">
                                    <i data-lucide="bot" style="width: 24px; height: 24px;"></i>
                                </div>
                            </div>
                            <div class="message-content">
                                <div class="message-text">
                                    <p>¡Hola! Soy capibara6, un modelo de IA híbrido Transformer-Mamba. ¿En qué puedo ayudarte hoy?</p>
                                </div>
                                <div class="message-time">${new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}</div>
                            </div>
                        </div>
                    `;
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }
                
                this.showSuccess('Chat eliminado exitosamente');
                this.loadChats();
            } catch (error) {
                console.error('Error eliminando chat:', error);
                this.showError('Error al eliminar el chat');
            }
        }
    }
    
    // ============================================
    // Gestión de Cuenta
    // ============================================
    
    openAccountModal() {
        const modal = document.getElementById('account-modal');
        
        // Cargar datos del usuario
        const userData = this.loadUserProfile();
        if (userData) {
            document.getElementById('account-name').value = userData.name || 'Usuario';
            document.getElementById('account-email').value = userData.email || 'usuario@example.com';
            document.getElementById('account-company').value = userData.company || '';
        }
        
        modal.classList.add('active');
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
    
    closeAccountModal() {
        const modal = document.getElementById('account-modal');
        modal.classList.remove('active');
    }
    
    async saveAccount() {
        const name = document.getElementById('account-name').value.trim();
        const email = document.getElementById('account-email').value.trim();
        const company = document.getElementById('account-company').value.trim();
        
        if (!name || !email) {
            this.showError('Nombre y email son obligatorios');
            return;
        }
        
        try {
            const userData = {
                name: name,
                email: email,
                company: company,
                updatedAt: new Date().toISOString()
            };
            
            localStorage.setItem('capibara6_user', JSON.stringify(userData));
            
            // Actualizar UI
            document.getElementById('user-name').textContent = name;
            document.getElementById('user-email').textContent = email;
            
            this.closeAccountModal();
            this.showSuccess('Información de cuenta actualizada');
        } catch (error) {
            console.error('Error guardando cuenta:', error);
            this.showError('Error al guardar la información');
        }
    }
    
    changePassword() {
        // TODO: Implementar cambio de contraseña
        this.showError('Funcionalidad de cambio de contraseña próximamente');
    }
    
    // ============================================
    // Gemelo Digital
    // ============================================
    
    switchAccountTab(tabName) {
        // Cambiar tabs activos
        document.querySelectorAll('.account-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabName);
        });
        
        document.querySelectorAll('.account-tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `tab-${tabName}`);
        });
        
        // Mostrar/ocultar botones del footer según la pestaña
        const saveBtn = document.getElementById('account-save-btn');
        const cancelBtn = document.getElementById('account-cancel-btn');
        if (saveBtn && cancelBtn) {
            if (tabName === 'profile') {
                saveBtn.style.display = 'flex';
                cancelBtn.style.display = 'flex';
            } else {
                saveBtn.style.display = 'none';
                cancelBtn.style.display = 'none';
            }
        }
        
        // Inicializar iconos si es necesario
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        // Si se cambia a la pestaña de gemelo digital, cargar estado
        if (tabName === 'digital-twin') {
            this.loadDigitalTwinState();
        }
    }
    
    loadDigitalTwinState() {
        // Cargar estado guardado del gemelo digital
        const twinData = localStorage.getItem('capibara6_digital_twin');
        const importedData = JSON.parse(localStorage.getItem('capibara6_social_imports') || '{}');
        
        // Actualizar estados de importación
        Object.keys(importedData).forEach(platform => {
            this.updateSocialStatus(platform, 'imported');
        });
        
        // Si hay gemelo generado, mostrarlo
        if (twinData) {
            const twin = JSON.parse(twinData);
            this.displayTwinProfile(twin);
        }
        
        // Habilitar botón de generar si hay datos importados
        this.updateGenerateButton();
    }
    
    async handleSocialImport(platform, file) {
        if (!file) return;
        
        try {
            this.showSuccess(`Importando datos de ${platform}...`);
            
            // Leer archivo
            const fileContent = await this.readFileAsText(file);
            
            // Parsear según tipo de archivo
            let data;
            if (file.name.endsWith('.json')) {
                data = JSON.parse(fileContent);
            } else if (file.name.endsWith('.csv')) {
                data = this.parseCSV(fileContent);
            } else {
                throw new Error('Formato de archivo no soportado');
            }
            
            // Guardar datos importados
            const imports = JSON.parse(localStorage.getItem('capibara6_social_imports') || '{}');
            imports[platform] = {
                data: data,
                importedAt: new Date().toISOString(),
                fileName: file.name,
                recordCount: Array.isArray(data) ? data.length : Object.keys(data).length
            };
            localStorage.setItem('capibara6_social_imports', JSON.stringify(imports));
            
            // Actualizar UI
            this.updateSocialStatus(platform, 'imported');
            this.updateGenerateButton();
            
            this.showSuccess(`✅ ${platform} importado exitosamente (${imports[platform].recordCount} registros)`);
            
            // Enviar al backend (simulado por ahora)
            // await this.sendToBackend(platform, data);
            
        } catch (error) {
            console.error(`Error importando ${platform}:`, error);
            this.showError(`Error al importar ${platform}: ${error.message}`);
        }
    }
    
    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = reject;
            reader.readAsText(file);
        });
    }
    
    parseCSV(csvText) {
        // Parseo simple de CSV
        const lines = csvText.split('\n');
        const headers = lines[0].split(',');
        return lines.slice(1).map(line => {
            const values = line.split(',');
            const obj = {};
            headers.forEach((header, i) => {
                obj[header.trim()] = values[i]?.trim() || '';
            });
            return obj;
        }).filter(obj => Object.keys(obj).length > 0);
    }
    
    updateSocialStatus(platform, status) {
        const statusElement = document.getElementById(`${platform}-status`);
        const importBtn = document.querySelector(`[data-platform="${platform}"] .btn-social-import`);
        
        if (statusElement) {
            statusElement.textContent = status === 'imported' ? 'Importado ✓' : 'No importado';
            statusElement.classList.toggle('imported', status === 'imported');
        }
        
        if (importBtn) {
            importBtn.classList.toggle('imported', status === 'imported');
            if (status === 'imported') {
                importBtn.innerHTML = '<i data-lucide="check" style="width: 16px; height: 16px;"></i> Importado';
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }
        }
    }
    
    updateGenerateButton() {
        const imports = JSON.parse(localStorage.getItem('capibara6_social_imports') || '{}');
        const hasImports = Object.keys(imports).length > 0;
        const generateBtn = document.getElementById('generate-twin-btn');
        
        if (generateBtn) {
            generateBtn.disabled = !hasImports;
        }
    }
    
    async generateDigitalTwin() {
        const imports = JSON.parse(localStorage.getItem('capibara6_social_imports') || '{}');
        
        if (Object.keys(imports).length === 0) {
            this.showError('Importa al menos una red social antes de generar el gemelo');
            return;
        }
        
        try {
            // Mostrar progreso
            this.showProgressSection();
            this.updateProgress(0, 'Iniciando generación del gemelo digital...');
            
            // Simular proceso de generación (en producción esto sería una llamada al backend)
            const steps = [
                { progress: 10, message: 'Procesando datos importados...' },
                { progress: 25, message: 'Analizando patrones de escritura...' },
                { progress: 40, message: 'Extrayendo vocabulario característico...' },
                { progress: 55, message: 'Analizando temas frecuentes...' },
                { progress: 70, message: 'Detectando personalidad (Big Five)...' },
                { progress: 85, message: 'Generando perfil del gemelo...' },
                { progress: 100, message: 'Gemelo digital generado exitosamente ✓' }
            ];
            
            for (const step of steps) {
                await this.delay(800);
                this.updateProgress(step.progress, step.message);
            }
            
            // Crear gemelo digital simulado
            const twin = {
                id: 'twin_' + Date.now(),
                name: 'Mi Gemelo Digital',
                createdAt: new Date().toISOString(),
                platforms: Object.keys(imports),
                stats: {
                    messagesAnalyzed: Object.values(imports).reduce((sum, imp) => sum + (imp.recordCount || 0), 0),
                    platformsCount: Object.keys(imports).length
                },
                personality: {
                    openness: Math.random() * 100,
                    conscientiousness: Math.random() * 100,
                    extraversion: Math.random() * 100,
                    agreeableness: Math.random() * 100,
                    neuroticism: Math.random() * 100
                }
            };
            
            // Guardar gemelo
            localStorage.setItem('capibara6_digital_twin', JSON.stringify(twin));
            
            // Actualizar estado
            document.getElementById('twin-status-badge').textContent = 'Activo';
            document.getElementById('twin-status-badge').classList.add('active');
            
            // Mostrar perfil
            this.displayTwinProfile(twin);
            
            this.showSuccess('Gemelo digital generado exitosamente');
            
        } catch (error) {
            console.error('Error generando gemelo:', error);
            this.showError('Error al generar el gemelo digital');
        }
    }
    
    showProgressSection() {
        const progressSection = document.getElementById('twin-progress-section');
        const progressSteps = document.getElementById('twin-progress-steps');
        
        if (progressSection) {
            progressSection.style.display = 'block';
        }
        
        // Limpiar pasos anteriores
        if (progressSteps) {
            progressSteps.innerHTML = '';
        }
    }
    
    updateProgress(percentage, message) {
        const progressBar = document.getElementById('twin-progress-bar');
        const progressPercentage = document.getElementById('twin-progress-percentage');
        const progressSteps = document.getElementById('twin-progress-steps');
        
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
        }
        
        if (progressPercentage) {
            progressPercentage.textContent = `${percentage}%`;
        }
        
        if (progressSteps && message) {
            // Añadir paso actual
            const stepDiv = document.createElement('div');
            stepDiv.className = `progress-step ${percentage === 100 ? 'completed' : percentage > 0 ? 'active' : ''}`;
            stepDiv.innerHTML = `
                <div class="step-icon">${percentage === 100 ? '✓' : '●'}</div>
                <span>${message}</span>
            `;
            progressSteps.appendChild(stepDiv);
            
            // Scroll al último paso
            progressSteps.scrollTop = progressSteps.scrollHeight;
        }
    }
    
    displayTwinProfile(twin) {
        const profileSection = document.getElementById('twin-profile-section');
        if (!profileSection) return;
        
        profileSection.style.display = 'block';
        
        // Actualizar información básica
        document.getElementById('twin-name').textContent = twin.name;
        document.getElementById('twin-created-date').textContent = 
            `Creado el ${new Date(twin.createdAt).toLocaleDateString('es-ES')}`;
        document.getElementById('twin-messages-count').textContent = twin.stats.messagesAnalyzed;
        document.getElementById('twin-platforms-count').textContent = twin.stats.platformsCount;
        
        // Mostrar análisis de personalidad
        const personalityDiv = document.getElementById('twin-personality');
        if (personalityDiv && twin.personality) {
            const traits = [
                { key: 'openness', label: 'Apertura' },
                { key: 'conscientiousness', label: 'Responsabilidad' },
                { key: 'extraversion', label: 'Extroversión' },
                { key: 'agreeableness', label: 'Amabilidad' },
                { key: 'neuroticism', label: 'Neuroticismo' }
            ];
            
            personalityDiv.innerHTML = traits.map(trait => {
                const value = Math.round(twin.personality[trait.key]);
                return `
                    <div class="personality-trait">
                        <div class="trait-name">
                            <span>${trait.label}</span>
                            <span>${value}%</span>
                        </div>
                        <div class="trait-bar-container">
                            <div class="trait-bar" style="width: ${value}%"></div>
                        </div>
                    </div>
                `;
            }).join('');
        }
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    showSuccess(message) {
        // Crear notificación de éxito
        const notification = document.createElement('div');
        notification.className = 'success-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    setupAutoFocus() {
        // Asegurar que el input de chat esté enfocado automáticamente en móviles
        const isMobile = window.innerWidth <= 480 || ("ontouchstart" in window) || (navigator.maxTouchPoints > 0);
        
        if (isMobile) {
            setTimeout(() => {
                if (this.chatInput) {
                    this.chatInput.focus();
                    // Colocar cursor al final del texto si hay contenido
                    if (this.chatInput.value) {
                        this.chatInput.selectionStart = this.chatInput.selectionEnd = this.chatInput.value.length;
                    }
                }
            }, 300); // Pequeño delay para asegurar que el DOM esté completamente cargado
            
            // Escuchar eventos de touch para mantener el foco
            document.addEventListener("touchstart", (e) => {
                if (!e.target.closest(".chat-input, .chat-send-btn, .input-action-btn")) {
                    setTimeout(() => {
                        if (this.chatInput) {
                            this.chatInput.focus();
                        }
                    }, 100);
                }
            }, { passive: true });
        }
    }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new Capibara6ChatPage();
    });
} else {
    new Capibara6ChatPage();
}
