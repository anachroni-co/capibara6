/**
 * Model Visualization System
 * Gestiona la visualización de modelos activos, métricas y estadísticas
 */

class ModelVisualization {
    constructor() {
        this.currentModel = 'Auto';
        this.currentTier = null;
        this.modelStats = {
            fast: 0,
            balanced: 0,
            complex: 0,
            total: 0
        };
        this.lastResponseMetrics = {
            time: null,
            tokens: null,
            speed: null
        };

        this.init();
    }

    init() {
        // Elementos del DOM
        this.modelBadge = document.getElementById('current-model-badge');
        this.modelName = document.getElementById('current-model-name');
        this.metricsPanel = document.getElementById('model-metrics-panel');
        this.closePanelBtn = document.getElementById('close-metrics-panel');

        // Event listeners
        if (this.modelBadge) {
            this.modelBadge.addEventListener('click', () => this.toggleMetricsPanel());
        }

        if (this.closePanelBtn) {
            this.closePanelBtn.addEventListener('click', () => this.closeMetricsPanel());
        }

        console.log('✅ Model Visualization initialized');
    }

    /**
     * Actualiza el modelo activo en el badge
     * @param {string} modelName - Nombre del modelo (phi3:mini, mistral, gpt-oss:20b)
     * @param {string} tier - Tier del modelo (fast, balanced, complex)
     */
    updateCurrentModel(modelName, tier) {
        this.currentModel = modelName;
        this.currentTier = tier;

        if (this.modelName) {
            // Mostrar nombre corto del modelo
            const shortName = this.getShortModelName(modelName);
            this.modelName.textContent = shortName;
        }

        if (this.modelBadge) {
            // Remover clases de tier previas
            this.modelBadge.classList.remove('tier-fast', 'tier-balanced', 'tier-complex');

            // Añadir clase de tier actual
            if (tier) {
                this.modelBadge.classList.add(`tier-${tier}`);
            }
        }

        // Actualizar panel de métricas
        this.updateMetricsPanel();

        console.log(`📊 Model updated: ${modelName} (${tier})`);
    }

    /**
     * Obtiene nombre corto del modelo para mostrar
     */
    getShortModelName(fullName) {
        const modelMap = {
            'phi3:mini': 'Phi3 Mini',
            'mistral': 'Mistral',
            'gpt-oss:20b': 'GPT-OSS 20B',
            'auto': 'Auto'
        };

        return modelMap[fullName.toLowerCase()] || fullName;
    }

    /**
     * Obtiene nombre completo del tier
     */
    getTierDisplayName(tier) {
        const tierMap = {
            'fast': 'Fast Response',
            'balanced': 'Balanced',
            'complex': 'Complex Reasoning'
        };

        return tierMap[tier] || tier;
    }

    /**
     * Actualiza las métricas de la última respuesta
     * @param {Object} metrics - Objeto con métricas
     */
    updateResponseMetrics(metrics) {
        this.lastResponseMetrics = {
            time: metrics.time || null,
            tokens: metrics.tokens || null,
            speed: metrics.speed || null
        };

        // Actualizar UI del panel de métricas
        const timeEl = document.getElementById('metrics-response-time');
        const tokensEl = document.getElementById('metrics-tokens');
        const speedEl = document.getElementById('metrics-speed');

        if (timeEl) {
            timeEl.textContent = metrics.time ? `${metrics.time.toFixed(2)}s` : '-';
        }

        if (tokensEl) {
            tokensEl.textContent = metrics.tokens || '-';
        }

        if (speedEl) {
            speedEl.textContent = metrics.speed ? `${metrics.speed.toFixed(1)} tok/s` : '-';
        }

        console.log('📈 Response metrics updated:', metrics);
    }

    /**
     * Registra el uso de un modelo para estadísticas
     * @param {string} tier - Tier del modelo usado
     */
    recordModelUsage(tier) {
        if (tier && this.modelStats.hasOwnProperty(tier)) {
            this.modelStats[tier]++;
            this.modelStats.total++;

            // Actualizar gráficos de uso
            this.updateUsageCharts();

            console.log('📊 Model usage recorded:', tier, this.modelStats);
        }
    }

    /**
     * Actualiza los gráficos de uso de modelos
     */
    updateUsageCharts() {
        const total = this.modelStats.total;

        if (total === 0) return;

        const fastPercent = (this.modelStats.fast / total) * 100;
        const balancedPercent = (this.modelStats.balanced / total) * 100;
        const complexPercent = (this.modelStats.complex / total) * 100;

        // Actualizar barras
        this.updateUsageBar('fast', fastPercent);
        this.updateUsageBar('balanced', balancedPercent);
        this.updateUsageBar('complex', complexPercent);
    }

    /**
     * Actualiza una barra individual de uso
     */
    updateUsageBar(tier, percent) {
        const percentEl = document.getElementById(`metrics-${tier}-percent`);
        const barEl = document.getElementById(`metrics-${tier}-bar`);

        if (percentEl) {
            percentEl.textContent = `${percent.toFixed(1)}%`;
        }

        if (barEl) {
            barEl.style.width = `${percent}%`;
        }
    }

    /**
     * Actualiza el panel de métricas completo
     */
    updateMetricsPanel() {
        const currentModelEl = document.getElementById('metrics-current-model');
        const tierEl = document.getElementById('metrics-tier');

        if (currentModelEl) {
            currentModelEl.textContent = this.getShortModelName(this.currentModel);
        }

        if (tierEl && this.currentTier) {
            tierEl.textContent = this.getTierDisplayName(this.currentTier);
        }
    }

    /**
     * Añade badge de modelo a un mensaje
     * @param {HTMLElement} messageElement - Elemento del mensaje
     * @param {string} modelName - Nombre del modelo
     * @param {string} tier - Tier del modelo
     */
    addModelBadgeToMessage(messageElement, modelName, tier) {
        const contentDiv = messageElement.querySelector('.message-content');
        if (!contentDiv) return;

        // Crear badge
        const badge = document.createElement('div');
        badge.className = 'message-model-badge';
        badge.innerHTML = `
            <i data-lucide="cpu" style="width: 12px; height: 12px;"></i>
            <span>${this.getShortModelName(modelName)}</span>
        `;

        // Añadir al final del contenido
        contentDiv.appendChild(badge);

        // Inicializar icono de Lucide
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    /**
     * Abre el panel de métricas
     */
    toggleMetricsPanel() {
        if (this.metricsPanel) {
            this.metricsPanel.classList.toggle('open');

            // Reinicializar iconos de Lucide después de abrir
            if (this.metricsPanel.classList.contains('open')) {
                setTimeout(() => {
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }, 100);
            }
        }
    }

    /**
     * Cierra el panel de métricas
     */
    closeMetricsPanel() {
        if (this.metricsPanel) {
            this.metricsPanel.classList.remove('open');
        }
    }

    /**
     * Resetea las estadísticas
     */
    resetStats() {
        this.modelStats = {
            fast: 0,
            balanced: 0,
            complex: 0,
            total: 0
        };

        this.updateUsageCharts();
        console.log('🔄 Stats reset');
    }

    /**
     * Obtiene estadísticas actuales
     * @returns {Object} Estadísticas
     */
    getStats() {
        return {
            currentModel: this.currentModel,
            currentTier: this.currentTier,
            usage: { ...this.modelStats },
            lastResponse: { ...this.lastResponseMetrics }
        };
    }
}

// Exportar para uso global
window.modelVisualization = new ModelVisualization();

console.log('🎨 Model Visualization System loaded');
