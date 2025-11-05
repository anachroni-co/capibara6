// Chat page para interactuar con el modelo capibara6 a través del backend MCP

class Capibara6ChatPage {
    constructor() {
        this.backendUrl = typeof CHATBOT_CONFIG !== 'undefined' 
            ? CHATBOT_CONFIG.BACKEND_URL
            : (window.location.hostname === 'localhost' 
                ? 'http://localhost:5000'
                : 'https://www.capibara6.com');
        
        this.messages = [];
        this.chats = [];
        this.currentChatId = null;
        this.isConnected = false;
        this.isProcessing = false;
        this.sidebarCollapsed = false;
        
        // Elementos del DOM
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
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
    }
    
    async init() {
        // Cargar configuración del usuario
        this.loadUserSettings();
        this.loadUserProfile();
        
        // Configurar event listeners
        this.setupEventListeners();
        
        // Verificar conexión con el backend
        await this.checkConnection();
        
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
            const endpoint = typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.ENDPOINTS.MCP_STATUS
                ? this.backendUrl + CHATBOT_CONFIG.ENDPOINTS.MCP_STATUS
                : `${this.backendUrl}/api/mcp/status`;
            const response = await fetch(endpoint);
            const data = await response.json();
            
            if (data.status === 'running') {
                this.isConnected = true;
                this.updateStatus('Conectado', 'success');
            } else {
                this.isConnected = false;
                this.updateStatus('Desconectado', 'error');
                this.showError('El servidor MCP no está disponible. Por favor, verifica que el backend esté corriendo.');
            }
        } catch (error) {
            console.error('Error verificando conexión:', error);
            this.isConnected = false;
            this.updateStatus('Error de conexión', 'error');
            this.showError('No se pudo conectar con el backend. Asegúrate de que el servidor esté corriendo en ' + this.backendUrl);
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
            } else {
                throw new Error('Respuesta inválida del servidor');
            }
            
            // Actualizar lista de chats
            this.updateChatInList();
            
        } catch (error) {
            console.error('Error enviando mensaje:', error);
            this.removeTypingIndicator(typingIndicator);
            this.addMessage(
                'Lo siento, ocurrió un error al procesar tu mensaje. Por favor, intenta de nuevo.',
                'bot',
                true
            );
            this.showError('Error: ' + error.message);
        } finally {
            this.setProcessing(false);
        }
    }
    
    async sendToBackend(message) {
        // Usar el endpoint MCP tools/call para enviar mensajes al modelo
        const endpoint = typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.ENDPOINTS.MCP_TOOLS_CALL
            ? this.backendUrl + CHATBOT_CONFIG.ENDPOINTS.MCP_TOOLS_CALL
            : `${this.backendUrl}/api/mcp/tools/call`;
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: 'analyze_document',
                arguments: {
                    document: message,
                    analysis_type: 'conversational',
                    context: this.getConversationContext()
                }
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Procesar respuesta MCP
        if (data.error) {
            throw new Error(data.error.message || 'Error en la respuesta del servidor');
        }
        
        // Extraer contenido de la respuesta
        if (data.result && data.result.content) {
            return { content: data.result.content };
        } else if (data.result && typeof data.result === 'string') {
            return { content: data.result };
        } else if (data.result && data.result.text) {
            return { content: data.result.text };
        } else {
            // Respuesta genérica si no hay contenido específico
            return { 
                content: 'He recibido tu mensaje. El modelo está procesando tu solicitud. Por favor, ten en cuenta que este es un sistema de demostración y puede requerir configuración adicional del backend para funcionar completamente.'
            };
        }
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
            if (chat.id === this.currentChatId) {
                chatItem.classList.add('active');
            }
            
            chatItem.innerHTML = `
                <div class="chat-item-icon">
                    <i data-lucide="message-circle" style="width: 18px; height: 18px;"></i>
                </div>
                <div class="chat-item-content">
                    <div class="chat-item-title">${chat.title}</div>
                    <div class="chat-item-time">${new Date(chat.timestamp).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })}</div>
                </div>
            `;
            
            chatItem.addEventListener('click', () => {
                this.loadChat(chat.id);
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
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new Capibara6ChatPage();
    });
} else {
    new Capibara6ChatPage();
}
