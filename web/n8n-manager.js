/**
 * N8N Manager para Capibara6
 * Gestiona la integración con n8n desde el frontend
 */

class N8NManager {
    constructor(config = {}) {
        this.baseURL = config.baseURL || 'http://localhost:5000';
        this.n8nURL = config.n8nURL || 'http://localhost:5678';
        this.cache = {
            templates: null,
            recommended: null,
            lastUpdate: null
        };
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutos
    }

    /**
     * Obtiene el catálogo completo de plantillas
     */
    async getCatalog() {
        if (this._isCacheValid('templates')) {
            return this.cache.templates;
        }

        try {
            const response = await fetch(`${this.baseURL}/api/n8n/templates`);
            const data = await response.json();

            if (data.status === 'success') {
                this.cache.templates = data.catalog;
                this.cache.lastUpdate = Date.now();
                return data.catalog;
            }

            throw new Error(data.error || 'Error obteniendo catálogo');
        } catch (error) {
            console.error('Error getCatalog:', error);
            throw error;
        }
    }

    /**
     * Obtiene plantillas recomendadas
     */
    async getRecommended() {
        if (this._isCacheValid('recommended')) {
            return this.cache.recommended;
        }

        try {
            const response = await fetch(`${this.baseURL}/api/n8n/templates/recommended`);
            const data = await response.json();

            if (data.status === 'success') {
                this.cache.recommended = data.templates;
                this.cache.lastUpdate = Date.now();
                return data.templates;
            }

            throw new Error(data.error || 'Error obteniendo recomendadas');
        } catch (error) {
            console.error('Error getRecommended:', error);
            throw error;
        }
    }

    /**
     * Busca plantillas por término
     */
    async searchTemplates(query) {
        try {
            const response = await fetch(
                `${this.baseURL}/api/n8n/templates/search?q=${encodeURIComponent(query)}`
            );
            const data = await response.json();

            if (data.status === 'success') {
                return data.results;
            }

            throw new Error(data.error || 'Error en búsqueda');
        } catch (error) {
            console.error('Error searchTemplates:', error);
            throw error;
        }
    }

    /**
     * Obtiene detalles de una plantilla
     */
    async getTemplateDetails(templateId) {
        try {
            const response = await fetch(`${this.baseURL}/api/n8n/templates/${templateId}`);
            const data = await response.json();

            if (data.status === 'success') {
                return data.template;
            }

            throw new Error(data.error || 'Plantilla no encontrada');
        } catch (error) {
            console.error('Error getTemplateDetails:', error);
            throw error;
        }
    }

    /**
     * Descarga el JSON de una plantilla
     */
    async downloadTemplate(templateId) {
        try {
            const response = await fetch(`${this.baseURL}/api/n8n/templates/${templateId}/download`);
            const data = await response.json();

            if (data.status === 'success') {
                return data.workflow;
            }

            throw new Error(data.error || 'Error descargando plantilla');
        } catch (error) {
            console.error('Error downloadTemplate:', error);
            throw error;
        }
    }

    /**
     * Importa una plantilla directamente a n8n
     */
    async importTemplate(templateId) {
        try {
            const response = await fetch(
                `${this.baseURL}/api/n8n/templates/${templateId}/import`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        n8n_url: this.n8nURL
                    })
                }
            );
            const data = await response.json();

            if (data.success) {
                return data;
            }

            throw new Error(data.error || 'Error importando plantilla');
        } catch (error) {
            console.error('Error importTemplate:', error);
            throw error;
        }
    }

    /**
     * Abre n8n en nueva ventana
     */
    openN8N() {
        window.open(this.n8nURL, '_blank');
    }

    /**
     * Abre una plantilla específica en n8n (después de importar)
     */
    async openTemplateInN8N(templateId) {
        try {
            const result = await this.importTemplate(templateId);
            if (result.workflow_id) {
                window.open(`${this.n8nURL}/workflow/${result.workflow_id}`, '_blank');
            }
            return result;
        } catch (error) {
            console.error('Error openTemplateInN8N:', error);
            throw error;
        }
    }

    /**
     * Verifica si n8n está disponible
     */
    async checkN8NStatus() {
        try {
            // Si estamos usando una URL de producción (Vercel), usar el endpoint proxy
            let healthCheckUrl;
            if (this.n8nURL.includes('capibara6.com')) {
                healthCheckUrl = `${this.n8nURL}/n8n/healthz`;
            } else {
                healthCheckUrl = `${this.n8nURL}/healthz`;
            }

            const response = await fetch(healthCheckUrl, {
                method: 'GET',
                mode: 'no-cors' // Para evitar CORS en health check
            });
            return { available: true, url: this.n8nURL };
        } catch (error) {
            return { available: false, error: error.message };
        }
    }

    /**
     * Exporta una plantilla como archivo JSON
     */
    async exportTemplateAsFile(templateId, filename) {
        try {
            const workflow = await this.downloadTemplate(templateId);
            const blob = new Blob([JSON.stringify(workflow, null, 2)], {
                type: 'application/json'
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename || `${templateId}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            return true;
        } catch (error) {
            console.error('Error exportTemplateAsFile:', error);
            throw error;
        }
    }

    /**
     * Obtiene estadísticas del catálogo
     */
    async getStatistics() {
        try {
            const catalog = await this.getCatalog();
            return catalog.statistics || {
                total_templates: 0,
                custom_templates: 0,
                recommended_templates: 0
            };
        } catch (error) {
            console.error('Error getStatistics:', error);
            return null;
        }
    }

    /**
     * Filtra plantillas por categoría
     */
    async getTemplatesByCategory(categoryId) {
        try {
            const catalog = await this.getCatalog();
            const category = catalog.categories?.find(cat => cat.id === categoryId);
            return category?.templates || [];
        } catch (error) {
            console.error('Error getTemplatesByCategory:', error);
            return [];
        }
    }

    /**
     * Filtra plantillas por prioridad
     */
    async getTemplatesByPriority(priority) {
        try {
            const recommended = await this.getRecommended();
            return recommended.filter(
                t => t.capibara6_integration?.priority === priority
            );
        } catch (error) {
            console.error('Error getTemplatesByPriority:', error);
            return [];
        }
    }

    /**
     * Verifica si el caché es válido
     */
    _isCacheValid(key) {
        if (!this.cache[key] || !this.cache.lastUpdate) {
            return false;
        }
        return (Date.now() - this.cache.lastUpdate) < this.cacheTimeout;
    }

    /**
     * Limpia el caché
     */
    clearCache() {
        this.cache = {
            templates: null,
            recommended: null,
            lastUpdate: null
        };
    }
}

// Instancia global
const n8nManager = new N8NManager({
    baseURL: window.API_BASE_URL || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000'
        : 'https://www.capibara6.com/api'),
    n8nURL: window.N8N_URL || (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5678'
        : 'https://www.capibara6.com')
});

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { N8NManager, n8nManager };
}
