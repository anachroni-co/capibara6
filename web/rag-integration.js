/**
 * Integración RAG para Capibara6
 * Conecta el frontend con el servicio RAG para guardar y buscar datos del usuario
 */

class RAGIntegration {
    constructor() {
        // Configuración del servicio RAG
        // Usar configuración centralizada si está disponible
        if (typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.VMS?.RAG3?.services?.rag) {
            this.ragBaseURL = CHATBOT_CONFIG.VMS.RAG3.services.rag;
        } else {
            // Fallback para desarrollo local
            this.ragBaseURL = window.location.hostname === 'localhost'
                ? 'http://34.105.131.8:8000'  // IP de rag3
                : 'https://www.capibara6.com/api/rag';
        }
        
        // Usar API client si está disponible
        this.apiClient = typeof Capibara6API !== 'undefined' 
            ? new Capibara6API(this.ragBaseURL)
            : null;
        
        // ID de usuario actual (obtener de localStorage o generar)
        this.userId = this.getOrCreateUserId();
        this.sessionId = this.getOrCreateSessionId();
        
        console.log('🔗 RAG Integration inicializada');
        console.log(`   Usuario: ${this.userId}`);
        console.log(`   Sesión: ${this.sessionId}`);
    }
    
    /**
     * Obtener o crear ID de usuario
     */
    getOrCreateUserId() {
        let userId = localStorage.getItem('capibara6_user_id');
        if (!userId) {
            userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('capibara6_user_id', userId);
        }
        return userId;
    }
    
    /**
     * Obtener o crear ID de sesión
     */
    getOrCreateSessionId() {
        let sessionId = localStorage.getItem('capibara6_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('capibara6_session_id', sessionId);
        }
        return sessionId;
    }
    
    /**
     * Guardar mensaje en RAG
     */
    async saveMessage(role, content, metadata = {}) {
        try {
            if (!this.apiClient) {
                console.warn('⚠️ RAG API Client no disponible');
                return false;
            }
            
            // Guardar usando el endpoint de mensajes del servicio RAG
            const messageData = {
                session_id: this.sessionId,
                content: content,
                message_role: role, // 'user' o 'assistant'
                metadata: {
                    ...metadata,
                    user_id: this.userId,
                    timestamp: new Date().toISOString()
                }
            };
            
            // Usar fetch directamente si el API client no tiene método saveMessage
            const response = await fetch(`${this.ragBaseURL}/api/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(messageData)
            });
            
            if (response.ok) {
                console.log('✅ Mensaje guardado en RAG');
                return true;
            } else {
                console.warn('⚠️ Error guardando en RAG:', response.statusText);
                return false;
            }
        } catch (error) {
            console.warn('⚠️ Error conectando con RAG:', error);
            return false;
        }
    }
    
    /**
     * Guardar archivo en RAG
     */
    async saveFile(file, metadata = {}) {
        try {
            if (!this.apiClient) {
                console.warn('⚠️ RAG API Client no disponible');
                return false;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('user_id', this.userId);
            formData.append('session_id', this.sessionId);
            formData.append('metadata', JSON.stringify(metadata));
            
            const response = await fetch(`${this.ragBaseURL}/api/files`, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                console.log('✅ Archivo guardado en RAG');
                return await response.json();
            } else {
                console.warn('⚠️ Error guardando archivo en RAG:', response.statusText);
                return null;
            }
        } catch (error) {
            console.warn('⚠️ Error guardando archivo en RAG:', error);
            return null;
        }
    }
    
    /**
     * Buscar en historial usando RAG
     */
    async searchHistory(query, nResults = 5) {
        try {
            if (!this.apiClient) {
                console.warn('⚠️ RAG API Client no disponible');
                return [];
            }
            
            // Buscar en colección de mensajes de chat
            const results = await this.apiClient.semanticSearch(
                query,
                'chat_messages',
                nResults
            );
            
            return results.results || [];
        } catch (error) {
            console.warn('⚠️ Error buscando en RAG:', error);
            return [];
        }
    }
    
    /**
     * Obtener historial de mensajes de la sesión actual
     */
    async getSessionHistory() {
        try {
            if (!this.apiClient) {
                return [];
            }
            
            const messages = await this.apiClient.getSessionMessages(this.sessionId);
            return messages.messages || [];
        } catch (error) {
            console.warn('⚠️ Error obteniendo historial:', error);
            return [];
        }
    }
    
    /**
     * Verificar conexión con RAG
     */
    async checkConnection() {
        try {
            const response = await fetch(`${this.ragBaseURL}/health`);
            if (response.ok) {
                const data = await response.json();
                console.log('✅ RAG Service conectado:', data);
                return true;
            }
            return false;
        } catch (error) {
            console.warn('⚠️ RAG Service no disponible:', error);
            return false;
        }
    }
}

// Crear instancia global
if (typeof window !== 'undefined') {
    window.ragIntegration = new RAGIntegration();
}

