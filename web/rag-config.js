/**
 * Configuración del sistema RAG Ingestion
 * Para integración con la VM rag-europe (10.204.0.10:8000)
 */

const RAG_CONFIG = {
    // URL base del servicio RAG
    BASE_URL: 'http://10.204.0.10:8000/api/v1',
    
    // Límites
    MAX_FILE_SIZE: 104857600, // 100MB en bytes (versión beta/demo)
    MAX_BATCH_SIZE: 10,       // Máximo archivos por batch
    TIMEOUT_MS: 300000,       // Timeout de 5 minutos por archivo
    
    // Tipos de archivos permitidos
    ALLOWED_EXTENSIONS: {
        text: ['.txt', '.json', '.xml', '.csv', '.md'],
        documents: ['.pdf', '.doc', '.docx', '.xls', '.xlsx'],
        archives: ['.zip', '.rar', '.7z', '.tar', '.gz']
    },
    
    // ENDPOINTS
    ENDPOINTS: {
        INGEST_TEXT: '/ingest/text',
        INGEST_FILE: '/ingest/file',
        INGEST_STATS: '/ingest/stats',
        INGEST_JOB_STATUS: '/ingest/job', // + '/{job_id}',
        INGEST_CANCEL: '/ingest/cancel', // + '/{job_id}',
        HEALTH: '/health'
    },
    
    // Tipos de fuentes
    SOURCE_TYPES: {
        TEXT: 'text',
        DATABASE: 'database',
        DOCUMENT: 'document',
        ARCHIVE: 'archive',
        CODE: 'code',
        WEB: 'web',
        CUSTOM: 'custom'
    }
};

/**
 * Cliente de Ingestión de RAG
 */
class Capibara6RAGClient {
    constructor(config = {}) {
        this.config = { ...RAG_CONFIG, ...config };
        this.baseUrl = this.config.BASE_URL;
    }
    
    /**
     * Ingestar texto directamente
     */
    async ingestText(text, options = {}) {
        const {
            sourceType = 'text',
            sourceName = 'manual_input',
            metadata = {}
        } = options;
        
        try {
            const response = await fetch(`${this.baseUrl}${this.config.ENDPOINTS.INGEST_TEXT}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text,
                    source_type: sourceType,
                    source_name: sourceName,
                    metadata: {
                        ...metadata,
                        client: 'capibara6-frontend',
                        timestamp: new Date().toISOString()
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${await response.text()}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error en ingestText:', error);
            throw error;
        }
    }
    
    /**
     * Ingestar archivo
     */
    async ingestFile(file, options = {}) {
        const {
            sourceType = 'document',
            sourceName = file.name,
            metadata = {}
        } = options;
        
        try {
            const formData = new FormData();
            formData.append('file', file, file.name);
            formData.append('source_type', sourceType);
            formData.append('source_name', sourceName);
            formData.append('metadata', JSON.stringify({
                ...metadata,
                original_filename: file.name,
                size: file.size,
                client: 'capibara6-frontend',
                timestamp: new Date().toISOString()
            }));
            
            const response = await fetch(`${this.baseUrl}${this.config.ENDPOINTS.INGEST_FILE}`, {
                method: 'POST',
                body: formData // El navegador establece automáticamente el Content-Type con boundary
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${await response.text()}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error en ingestFile:', error);
            throw error;
        }
    }
    
    /**
     * Obtener estadísticas del sistema
     */
    async getStats() {
        try {
            const response = await fetch(`${this.baseUrl}${this.config.ENDPOINTS.INGEST_STATS}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${await response.text()}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error en getStats:', error);
            throw error;
        }
    }
    
    /**
     * Verificar estado de un job
     */
    async getJobStatus(jobId) {
        try {
            const response = await fetch(`${this.baseUrl}${this.config.ENDPOINTS.INGEST_JOB_STATUS}/${jobId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${await response.text()}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`Error en getJobStatus (${jobId}):`, error);
            throw error;
        }
    }
    
    /**
     * Esperar a que un job termine
     */
    async waitForJob(jobId, maxAttempts = 30, intervalMs = 2000) {
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            try {
                const status = await this.getJobStatus(jobId);
                
                if (status.status === 'completed' || status.status === 'failed') {
                    return status;
                }
                
                // Esperar antes de la próxima verificación
                await new Promise(resolve => setTimeout(resolve, intervalMs));
            } catch (error) {
                console.error(`Error verificando job ${jobId}:`, error);
                // Continuar esperando incluso si hay un error temporal
                await new Promise(resolve => setTimeout(resolve, intervalMs));
            }
        }
        
        throw new Error(`Job ${jobId} no terminó después de ${maxAttempts} intentos`);
    }
    
    /**
     * Cancelar un job
     */
    async cancelJob(jobId) {
        try {
            const response = await fetch(`${this.baseUrl}${this.config.ENDPOINTS.INGEST_CANCEL}/${jobId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${await response.text()}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`Error cancelando job ${jobId}:`, error);
            throw error;
        }
    }
    
    /**
     * Verificar si el servicio RAG está disponible
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseUrl}${this.config.ENDPOINTS.HEALTH}`);
            return response.ok;
        } catch (error) {
            console.error('Error en checkHealth:', error);
            return false;
        }
    }
}

// Exportar para uso global o como módulo
if (typeof window !== 'undefined') {
    window.Capibara6RAGClient = Capibara6RAGClient;
    window.RAG_CONFIG = RAG_CONFIG;
}

// Para uso con módulos ES6 si se necesita
export { Capibara6RAGClient, RAG_CONFIG };