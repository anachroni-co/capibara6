// Chat page para interactuar con el modelo capibara6 a través del backend MCP

class Capibara6ChatPage {
    constructor() {
        this.backendUrl = typeof CHATBOT_CONFIG !== 'undefined' 
            ? CHATBOT_CONFIG.BACKEND_URL
            : (window.location.hostname === 'localhost' 
                ? 'http://localhost:5000'
                : 'https://www.capibara6.com');
        
        this.messages = [];
        this.isConnected = false;
        this.isProcessing = false;
        
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.chatSendBtn = document.getElementById('chat-send-btn');
        this.statusIndicator = document.getElementById('status-indicator');
        this.statusText = document.getElementById('status-text');
        this.clearChatBtn = document.getElementById('clear-chat-btn');
        
        this.init();
    }
    
    async init() {
        // Configurar event listeners
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
        
        // Limpiar chat
        this.clearChatBtn.addEventListener('click', () => this.clearChat());
        
        // Verificar conexión con el backend
        await this.checkConnection();
        
        // Cargar mensajes guardados
        this.loadMessages();
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
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isProcessing) return;
        
        if (!this.isConnected) {
            this.showError('No hay conexión con el servidor. Por favor, verifica tu conexión.');
            return;
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
        // Por ahora, usamos una herramienta de análisis de texto como ejemplo
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
        avatar.innerHTML = type === 'bot' 
            ? '<i data-lucide="bot" style="width: 24px; height: 24px;"></i>'
            : '<i data-lucide="user" style="width: 24px; height: 24px;"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const textP = document.createElement('p');
        textP.textContent = text;
        content.appendChild(textP);
        
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
        const chatMain = document.querySelector('.chat-main');
        chatMain.insertBefore(errorDiv, chatMain.firstChild);
        
        // Remover después de 5 segundos
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    clearChat() {
        if (confirm('¿Estás seguro de que quieres limpiar toda la conversación?')) {
            // Mantener solo el mensaje de bienvenida
            this.messages = [];
            this.chatMessages.innerHTML = `
                <div class="chat-message bot-message">
                    <div class="message-avatar">
                        <i data-lucide="bot" style="width: 24px; height: 24px;"></i>
                    </div>
                    <div class="message-content">
                        <p>¡Hola! Soy capibara6, un modelo de IA híbrido Transformer-Mamba. ¿En qué puedo ayudarte hoy?</p>
                        <div class="message-time">${new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}</div>
                    </div>
                </div>
            `;
            
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            
            this.saveMessages();
        }
    }
    
    saveMessages() {
        try {
            localStorage.setItem('capibara6_chat_messages', JSON.stringify(this.messages));
        } catch (error) {
            console.warn('Error guardando mensajes:', error);
        }
    }
    
    loadMessages() {
        try {
            const saved = localStorage.getItem('capibara6_chat_messages');
            if (saved) {
                const messages = JSON.parse(saved);
                // Restaurar mensajes (excepto el de bienvenida)
                messages.forEach(msg => {
                    if (msg.type !== 'welcome') {
                        this.addMessage(msg.text, msg.type, msg.isError);
                    }
                });
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

