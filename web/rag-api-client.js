/**
 * Cliente API para Capibara6 RAG System
 * Proporciona funciones para interactuar con el backend API REST
 */

class Capibara6API {
    constructor(baseURL = 'http://localhost:8001') {
        this.baseURL = baseURL;
    }

    /**
     * Realiza una petición HTTP
     * @private
     */
    async _request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    // ==========================================
    // MÉTODOS DE BÚSQUEDA
    // ==========================================

    /**
     * Búsqueda semántica en una colección específica
     * @param {string} query - Texto de búsqueda
     * @param {string} collectionName - Nombre de la colección (opcional)
     * @param {number} nResults - Número de resultados
     * @returns {Promise<Object>} Resultados de la búsqueda
     */
    async semanticSearch(query, collectionName = null, nResults = 5) {
        return this._request('/api/search/semantic', {
            method: 'POST',
            body: JSON.stringify({
                query,
                collection_name: collectionName,
                n_results: nResults
            })
        });
    }

    /**
     * Búsqueda RAG completa (Vector + PostgreSQL + Grafo)
     * @param {string} query - Pregunta en lenguaje natural
     * @param {number} nResults - Resultados por colección
     * @param {boolean} useGraph - Usar exploración de grafo
     * @returns {Promise<Object>} Resultados de RAG
     */
    async ragSearch(query, nResults = 5, useGraph = true) {
        return this._request('/api/search/rag', {
            method: 'POST',
            body: JSON.stringify({
                query,
                n_results: nResults,
                use_graph: useGraph
            })
        });
    }

    /**
     * Búsqueda en todas las colecciones
     * @param {string} query - Texto de búsqueda
     * @param {number} nResults - Resultados por colección
     * @returns {Promise<Object>} Resultados agrupados por colección
     */
    async searchAll(query, nResults = 3) {
        return this._request('/api/search/all', {
            method: 'POST',
            body: JSON.stringify({
                query,
                n_results: nResults
            })
        });
    }

    // ==========================================
    // MÉTODOS DE USUARIOS
    // ==========================================

    /**
     * Listar usuarios
     * @param {number} limit - Límite de resultados
     * @param {number} offset - Offset para paginación
     * @returns {Promise<Object>} Lista de usuarios
     */
    async getUsers(limit = 10, offset = 0) {
        return this._request(`/api/users?limit=${limit}&offset=${offset}`, {
            method: 'GET'
        });
    }

    /**
     * Obtener información de un usuario
     * @param {string} username - Nombre de usuario
     * @returns {Promise<Object>} Información del usuario
     */
    async getUser(username) {
        return this._request(`/api/users/${encodeURIComponent(username)}`, {
            method: 'GET'
        });
    }

    /**
     * Obtener estadísticas de un usuario
     * @param {string} username - Nombre de usuario
     * @returns {Promise<Object>} Estadísticas del usuario
     */
    async getUserStats(username) {
        return this._request(`/api/stats/user/${encodeURIComponent(username)}`, {
            method: 'GET'
        });
    }

    // ==========================================
    // MÉTODOS DE MENSAJES
    // ==========================================

    /**
     * Listar mensajes
     * @param {Object} options - Opciones de filtrado
     * @returns {Promise<Object>} Lista de mensajes
     */
    async getMessages(options = {}) {
        const { userId, sessionId, limit = 50, offset = 0 } = options;

        const params = new URLSearchParams({
            limit: limit.toString(),
            offset: offset.toString()
        });

        if (userId) params.append('user_id', userId);
        if (sessionId) params.append('session_id', sessionId);

        return this._request(`/api/messages?${params.toString()}`, {
            method: 'GET'
        });
    }

    /**
     * Obtener mensajes de una sesión específica
     * @param {string} sessionId - ID de la sesión
     * @returns {Promise<Object>} Mensajes de la sesión
     */
    async getSessionMessages(sessionId) {
        return this._request(`/api/sessions/${encodeURIComponent(sessionId)}`, {
            method: 'GET'
        });
    }

    // ==========================================
    // MÉTODOS DE ARCHIVOS
    // ==========================================

    /**
     * Listar archivos
     * @param {Object} options - Opciones de filtrado
     * @returns {Promise<Object>} Lista de archivos
     */
    async getFiles(options = {}) {
        const { userId, filetype, limit = 50, offset = 0 } = options;

        const params = new URLSearchParams({
            limit: limit.toString(),
            offset: offset.toString()
        });

        if (userId) params.append('user_id', userId);
        if (filetype) params.append('filetype', filetype);

        return this._request(`/api/files?${params.toString()}`, {
            method: 'GET'
        });
    }

    // ==========================================
    // MÉTODOS DE ESTADÍSTICAS
    // ==========================================

    /**
     * Obtener estadísticas generales del sistema
     * @returns {Promise<Object>} Estadísticas del sistema
     */
    async getStats() {
        return this._request('/api/stats', {
            method: 'GET'
        });
    }

    /**
     * Obtener estadísticas de embeddings
     * @returns {Promise<Object>} Estadísticas de embeddings
     */
    async getEmbeddingStats() {
        return this._request('/api/stats/embeddings', {
            method: 'GET'
        });
    }

    // ==========================================
    // HEALTH CHECK
    // ==========================================

    /**
     * Verificar estado del servidor
     * @returns {Promise<Object>} Estado del servidor
     */
    async healthCheck() {
        return this._request('/health', {
            method: 'GET'
        });
    }
}

// Exportar para uso en módulos ES6
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Capibara6API;
}

// Hacer disponible globalmente para uso en navegador
if (typeof window !== 'undefined') {
    window.Capibara6API = Capibara6API;
}
