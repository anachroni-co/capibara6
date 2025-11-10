// Chat page para interactuar con el modelo capibara6 a través del backend MCP

class Capibara6ChatPage {
    constructor() {
        // IP REAL de la VM principal (según firewall actualizado)
        // Puerto 5000 está abierto para Capibara6 Main Server según firewall
        this.backendUrl = typeof CHATBOT_CONFIG !== 'undefined' 
            ? CHATBOT_CONFIG.BACKEND_URL
            : (window.location.hostname === 'localhost' 
                ? 'http://34.12.166.76:5000'  // Capibara6 Main Server (firewall: tcp:5000)
                : 'https://www.capibara6.com'); // Servidor en producción
        
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
        this.loadUserSettings();
        this.loadUserProfile();
        this.setupEventListeners();
        await this.checkConnection();
        this.loadChats();
        this.loadMessages();
    }
    
    setupEventListeners() {
        this.chatSendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.chatInput.addEventListener('input', () => {
            this.chatInput.style.height = 'auto';
            this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 200) + 'px';
        });
        
        this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        this.sidebarToggleMobile.addEventListener('click', () => this.toggleSidebarMobile());
        this.sidebarOverlay.addEventListener('click', () => this.closeSidebarMobile());
        this.newChatBtn.addEventListener('click', () => this.createNewChat());
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        
        this.profileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleProfileMenu();
        });
        
        document.addEventListener('click', (e) => {
            if (!this.profileMenu.contains(e.target) && !this.profileMenuBtn.contains(e.target)) {
                this.profileMenu.classList.remove('active');
            }
        });
        
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
        
        const tempSlider = document.getElementById('temperature-setting');
        const tempValue = document.getElementById('temperature-value');
        tempSlider.addEventListener('input', (e) => {
            tempValue.textContent = e.target.value;
        });

        // n8n Automation Panel
        const n8nAutomationBtn = document.getElementById('n8n-automation-btn');
        const n8nPanel = document.getElementById('n8n-automation-panel');
        const closeN8nPanel = document.getElementById('close-n8n-panel');

        if (n8nAutomationBtn && n8nPanel) {
            n8nAutomationBtn.addEventListener('click', () => {
                n8nPanel.classList.toggle('active');
            });
        }

        if (closeN8nPanel && n8nPanel) {
            closeN8nPanel.addEventListener('click', () => {
                n8nPanel.classList.remove('active');
            });
        }

        // n8n Actions
        const n8nOpenEditor = document.getElementById('n8n-open-editor');
        if (n8nOpenEditor) {
            n8nOpenEditor.addEventListener('click', () => {
                const n8nURL = window.CONFIG?.N8N_URL || 'http://localhost:5678';
                window.open(n8nURL, '_blank');
            });
        }
    }
    
    toggleSidebar() {
        this.sidebarCollapsed = !this.sidebarCollapsed;
        this.sidebar.classList.toggle('collapsed', this.sidebarCollapsed);
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
        if (typeof lucide !== 'undefined') lucide.createIcons();
        this.closeSidebarMobile();
    }
    
    async checkConnection() {
        try {
            // Usar endpoint de salud general
            const endpoint = `${this.backendUrl}/api/health`;
            const response = await fetch(endpoint, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            
            // Verificar que es un objeto con propiedades esperadas
            if (data && typeof data === 'object') {
                this.isConnected = true;
                this.updateStatus('Conectado', 'success');
            } else {
                this.isConnected = false;
                this.updateStatus('Desconectado', 'error');
                this.showError('El servidor no está disponible.');
            }
        } catch (error) {
            console.error('Error verificando conexión:', error);
            // Simplificar manejo del error - no usar proxy que no está implementado
            this.isConnected = false;
            this.updateStatus('Error de conexión', 'error');
            this.showError('No se pudo conectar con el backend en ' + this.backendUrl);
        }
    }
    
    updateStatus(text, type) {
        this.statusText.textContent = text;
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            connecting: '#6366f1'
        };
        const color = colors[type] || colors.connecting;
        this.statusIndicator.style.background = color;
        this.statusIndicator.style.boxShadow = `0 0 8px ${color}`;
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isProcessing) return;
        if (!this.isConnected) {
            this.showError('No hay conexión con el servidor.');
            return;
        }
        
        if (!this.currentChatId) {
            this.currentChatId = 'chat_' + Date.now();
            this.saveChats();
        }
        
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';
        this.setProcessing(true);
        
        const typingIndicator = this.showTypingIndicator();
        
        try {
            const response = await this.sendToBackend(message);
            this.removeTypingIndicator(typingIndicator);
            
            if (response && response.content) {
                this.addMessage(response.content, 'bot');
            } else {
                throw new Error('Respuesta inválida del servidor');
            }
            
            this.updateChatInList();
            
        } catch (error) {
            console.error('Error enviando mensaje:', error);
            this.removeTypingIndicator(typingIndicator);
            this.addMessage('Lo siento, ocurrió un error al procesar tu mensaje.', 'bot', true);
            this.showError('Error: ' + error.message);
        } finally {
            this.setProcessing(false);
        }
    }
    
    async sendToBackend(message) {
        // Intentar usar el endpoint directo primero, si falla por CORS usar proxy
        const endpoint = `${this.backendUrl}/api/mcp/tools/call`;
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: 'analyze_document',  // Usar herramienta disponible en MCP
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
            
            return response;
        } catch (error) {
            console.warn('Error de conexión directa, intentando alternativa...', error);
            // Si falla la conexión directa, usar fetch con modo 'no-cors' como último recurso
            // aunque no permita leer respuesta completa
            console.warn('Intentando conexión con modo no-cors...');
            try {
                const fallback_response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: 'analyze_document',
                        arguments: {
                            document: message,
                            analysis_type: 'conversational',
                            context: this.getConversationContext()
                        }
                    }),
                    mode: 'no-cors'  // Evitar verificación CORS (no permitirá leer respuesta completa)
                });
                
                // En modo 'no-cors', la respuesta no se puede leer completamente
                // así que simplemente devolvemos un indicador de que la solicitud fue enviada
                return {
                    ok: true,
                    json: async () => ({ message: "Solicitud MCP enviada", success: true }),
                    status: 200
                };
            } catch (fallback_error) {
                console.error('Error también en conexión no-cors:', fallback_error);
                throw new Error(`Error de conexión con el servidor: ${error.message}`);
            }
        }
    }
    
    getConversationContext() {
        const recentMessages = this.messages.slice(-10);
        return recentMessages.map(msg => ({
            role: msg.type === 'user' ? 'user' : 'assistant',
            content: msg.text
        }));
    }

    normalizeMessageContent(content) {
        if (typeof content === 'string') return content;
        if (Array.isArray(content)) {
            return content.map(c => this.normalizeMessageContent(c)).join('\n').trim();
        }
        if (content && typeof content === 'object') {
            if (typeof content.text === 'string') return content.text;
            if (content.text !== undefined) return this.normalizeMessageContent(content.text);
            return JSON.stringify(content);
        }
        if (content == null) return '';
        return String(content);
    }
    
    addMessage(text, type, isError = false) {
        const normalizedText = this.normalizeMessageContent(text);
        const message = {
            text: normalizedText,
            type,
            timestamp: new Date(),
            isError
        };
        
        this.messages.push(message);
        this.saveMessages();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}-message${isError ? ' error' : ''}`;
        
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
        textP.textContent = normalizedText;
        textDiv.appendChild(textP);
        content.appendChild(textDiv);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = message.timestamp.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
        content.appendChild(timeDiv);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        if (typeof lucide !== 'undefined') lucide.createIcons();
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>`;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message bot-message';
        messageDiv.appendChild(typingDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        
        return messageDiv;
    }
    
    removeTypingIndicator(el) {
        if (el && el.parentNode) el.remove();
    }
    
    setProcessing(state) {
        this.isProcessing = state;
        this.chatInput.disabled = state;
        this.chatSendBtn.disabled = state;
        this.chatSendBtn.innerHTML = state 
            ? '<span>Procesando...</span>' 
            : '<span>Enviar</span><i data-lucide="send" style="width: 20px; height: 20px;"></i>';
        if (!state && typeof lucide !== 'undefined') lucide.createIcons();
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        const chatMain = document.querySelector('.chat-main-content');
        chatMain.insertBefore(errorDiv, chatMain.children[1]);
        setTimeout(() => errorDiv.remove(), 5000);
    }
    
    clearChat() {
        if (confirm('¿Seguro que quieres limpiar toda la conversación?')) {
            this.createNewChat();
        }
    }
    
    // --- Gestión de chats ---
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
            if (!this.currentChatId) return;
            
            const chatIndex = this.chats.findIndex(c => c.id === this.currentChatId);
            const firstMessage = this.messages[0];
            const lastMessage = this.messages[this.messages.length - 1];
            const firstText = firstMessage ? this.normalizeMessageContent(firstMessage) : '';
            const lastText = lastMessage ? this.normalizeMessageContent(lastMessage) : '';
            
            const safeSubstring = (val, len) => typeof val === 'string' ? val.substring(0, len) : '';
            
            const chatData = {
                id: this.currentChatId,
                title: safeSubstring(firstText, 50) || 'Nueva conversación',
                lastMessage: safeSubstring(lastText, 100),
                timestamp: new Date().toISOString(),
                messageCount: this.messages.length
            };
            
            if (chatIndex >= 0) this.chats[chatIndex] = chatData;
            else this.chats.unshift(chatData);
            
            this.chats = this.chats.slice(0, 20);
            localStorage.setItem('capibara6_chats', JSON.stringify(this.chats));
            this.renderChatList();
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
            if (chat.id === this.currentChatId) chatItem.classList.add('active');
            
            chatItem.innerHTML = `
                <div class="chat-item-icon">
                    <i data-lucide="message-circle" style="width: 18px; height: 18px;"></i>
                </div>
                <div class="chat-item-content">
                    <div class="chat-item-title">${chat.title}</div>
                    <div class="chat-item-time">${new Date(chat.timestamp).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })}</div>
                </div>`;
            
            chatItem.addEventListener('click', () => this.loadChat(chat.id));
            this.chatList.appendChild(chatItem);
        });
        if (typeof lucide !== 'undefined') lucide.createIcons();
    }
    
    updateChatInList() {
        this.saveChats();
    }
    
    loadChat(chatId) {
        this.currentChatId = chatId;
        this.renderChatList();
        this.closeSidebarMobile();
    }
    
    // --- Configuración ---
    loadUserSettings() {
        try {
            const settings = localStorage.getItem('capibara6_settings');
            if (settings) {
                const parsed = JSON.parse(settings);
                if (parsed.sidebarCollapsed) {
                    this.sidebarCollapsed = true;
                    this.sidebar.classList.add('collapsed');
                }
            }
        } catch (error) {
            console.warn('Error cargando configuración:', error);
        }
    }
    
    saveUserSettings() {
        try {
            localStorage.setItem('capibara6_settings', JSON.stringify({
                sidebarCollapsed: this.sidebarCollapsed
            }));
        } catch (error) {
            console.warn('Error guardando configuración:', error);
        }
    }
    
    loadUserProfile() {
        try {
            const profile = localStorage.getItem('capibara6_profile');
            if (profile) {
                const parsed = JSON.parse(profile);
                if (parsed.name) document.getElementById('user-name').textContent = parsed.name;
                if (parsed.email) document.getElementById('user-email').textContent = parsed.email;
            }
        } catch (error) {
            console.warn('Error cargando perfil:', error);
        }
    }
    
    openSettings() { this.settingsModal.classList.add('active'); }
    closeSettings() { this.settingsModal.classList.remove('active'); }
    
    saveSettings() {
        const settings = {
            temperature: document.getElementById('temperature-setting').value,
            maxTokens: document.getElementById('max-tokens-setting').value,
            soundNotifications: document.getElementById('sound-notifications').checked,
            autoScroll: document.getElementById('auto-scroll').checked
        };
        localStorage.setItem('capibara6_model_settings', JSON.stringify(settings));
        this.closeSettings();
    }
    
    loadMessages() {
        try {
            const saved = localStorage.getItem(`capibara6_messages_${this.currentChatId}`);
            if (saved) this.messages = JSON.parse(saved);
        } catch (error) {
            console.warn('Error cargando mensajes:', error);
        }
    }
    
    saveMessages() {
        try {
            if (!this.currentChatId) return;
            localStorage.setItem(`capibara6_messages_${this.currentChatId}`, JSON.stringify(this.messages));
        } catch (error) {
            console.warn('Error guardando mensajes:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.capibara6ChatPage = new Capibara6ChatPage();
});
