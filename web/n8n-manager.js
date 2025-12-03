/**
 * N8N Manager para Capibara6
 * Gestiona la integración con n8n desde el frontend
 */

class N8NManager {
    constructor(config = {}) {
        // Usar URLs de la VM services para producción
        // Para acceso desde frontend (Vercel), usar IP externa
        this.baseURL = config.baseURL || 'http://34.175.255.139:5000';  // IP externa VM services
        this.n8nURL = config.n8nURL || 'http://34.175.255.139:5678';    // Puerto de n8n en VM services (externa)
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N getCatalog fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N getRecommended fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N searchTemplates fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N getTemplateDetails fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N downloadTemplate fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N importTemplate fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N openTemplateInN8N fallido - opcional:', error.message);
            }
            throw error;
        }
    }

    /**
     * Verifica si n8n está disponible
     */
    async checkN8NStatus() {
        try {
            // Usar fetch con timeout para evitar bloqueos
            // n8n usa endpoint /health para health check
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 segundos timeout

            const response = await fetch(`${this.n8nURL}/health`, {
                method: 'GET',
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            // n8n puede devolver diferentes tipos de respuesta
            let data;
            try {
                data = await response.json();
            } catch (parseError) {
                // Si no es JSON, tratar como texto y crear objeto de salud
                data = { status: 'ok', message: 'n8n is running' };
            }

            return {
                available: response.ok,
                url: this.n8nURL,
                status: response.status,
                data: data
            };
        } catch (error) {
            // No mostrar error si n8n no está disponible (es opcional)
            // Solo registrar en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N health check fallido - opcional:', error.message);
            }
            return { available: false, error: error.message, url: this.n8nURL };
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N exportTemplateAsFile fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N getStatistics fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N getTemplatesByCategory fallido - opcional:', error.message);
            }
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
            // Solo logear si estamos en modo desarrollo
            if (window.location.hostname === 'localhost' || window.DEBUG_MODE) {
                console.debug('N8N getTemplatesByPriority fallido - opcional:', error.message);
            }
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
    baseURL: window.API_BASE_URL || 'http://34.175.255.139:5000',  // IP externa VM services
    n8nURL: window.N8N_URL || 'http://34.175.255.139:5678'        // Puerto de n8n en VM services (externa)
});

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { N8NManager, n8nManager };
}
