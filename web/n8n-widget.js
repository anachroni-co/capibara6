/**
 * N8N Widget para integración en la UI de Capibara6
 * Widget flotante para acceso rápido a n8n y workflows
 */

class N8NWidget {
    constructor(options = {}) {
        this.position = options.position || 'bottom-right';
        this.n8nManager = options.n8nManager || window.n8nManager;
        this.isOpen = false;
        this.init();
    }

    init() {
        this.createWidget();
        this.attachEventListeners();
        this.checkStatus();

        // Actualizar estado cada 30 segundos
        setInterval(() => this.checkStatus(), 30000);
    }

    createWidget() {
        const widget = document.createElement('div');
        widget.id = 'n8n-widget';
        widget.innerHTML = `
            <style>
                #n8n-widget {
                    position: fixed;
                    ${this.position.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
                    ${this.position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
                    z-index: 1000;
                    font-family: 'Inter', sans-serif;
                }

                .n8n-widget-button {
                    width: 56px;
                    height: 56px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.3s;
                    position: relative;
                }

                .n8n-widget-button:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }

                .n8n-widget-button svg {
                    width: 24px;
                    height: 24px;
                    color: white;
                }

                .n8n-status-indicator {
                    position: absolute;
                    top: 2px;
                    right: 2px;
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    background: #10b981;
                    border: 2px solid white;
                    animation: pulse 2s infinite;
                }

                .n8n-status-indicator.offline {
                    background: #ef4444;
                    animation: none;
                }

                @keyframes pulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.7; transform: scale(0.95); }
                }

                .n8n-widget-panel {
                    position: absolute;
                    bottom: 70px;
                    right: 0;
                    width: 320px;
                    background: #2d2d2d;
                    border-radius: 12px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                    opacity: 0;
                    transform: translateY(10px);
                    pointer-events: none;
                    transition: all 0.3s;
                }

                .n8n-widget-panel.open {
                    opacity: 1;
                    transform: translateY(0);
                    pointer-events: all;
                }

                .n8n-widget-panel-header {
                    padding: 1rem;
                    border-bottom: 1px solid #374151;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .n8n-widget-panel-title {
                    font-weight: 600;
                    color: #e5e7eb;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }

                .n8n-widget-panel-body {
                    padding: 1rem;
                }

                .n8n-quick-actions {
                    display: grid;
                    gap: 0.5rem;
                }

                .n8n-quick-action {
                    padding: 0.75rem;
                    background: #1a1a1a;
                    border: 1px solid #374151;
                    border-radius: 8px;
                    color: #e5e7eb;
                    cursor: pointer;
                    transition: all 0.2s;
                    display: flex;
                    align-items: center;
                    gap: 0.75rem;
                    text-decoration: none;
                }

                .n8n-quick-action:hover {
                    background: #3d3d3d;
                    border-color: #667eea;
                    transform: translateX(2px);
                }

                .n8n-quick-action-icon {
                    width: 32px;
                    height: 32px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 6px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #667eea;
                }

                .n8n-quick-action-text {
                    flex: 1;
                }

                .n8n-quick-action-title {
                    font-size: 0.875rem;
                    font-weight: 600;
                    margin-bottom: 0.125rem;
                }

                .n8n-quick-action-desc {
                    font-size: 0.75rem;
                    color: #9ca3af;
                }

                .n8n-widget-footer {
                    padding: 0.75rem 1rem;
                    border-top: 1px solid #374151;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-size: 0.75rem;
                    color: #9ca3af;
                }

                .n8n-widget-status {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }

                .n8n-widget-status-dot {
                    width: 6px;
                    height: 6px;
                    border-radius: 50%;
                    background: #10b981;
                }

                .n8n-widget-status-dot.offline {
                    background: #ef4444;
                }
            </style>

            <button class="n8n-widget-button" id="n8n-widget-toggle">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
                <span class="n8n-status-indicator" id="n8n-status-indicator"></span>
            </button>

            <div class="n8n-widget-panel" id="n8n-widget-panel">
                <div class="n8n-widget-panel-header">
                    <div class="n8n-widget-panel-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                        </svg>
                        n8n Workflows
                    </div>
                </div>

                <div class="n8n-widget-panel-body">
                    <div class="n8n-quick-actions">
                        <a href="n8n-dashboard.html" class="n8n-quick-action">
                            <div class="n8n-quick-action-icon">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <rect x="3" y="3" width="7" height="7"></rect>
                                    <rect x="14" y="3" width="7" height="7"></rect>
                                    <rect x="14" y="14" width="7" height="7"></rect>
                                    <rect x="3" y="14" width="7" height="7"></rect>
                                </svg>
                            </div>
                            <div class="n8n-quick-action-text">
                                <div class="n8n-quick-action-title">Dashboard</div>
                                <div class="n8n-quick-action-desc">Ver todas las plantillas</div>
                            </div>
                        </a>

                        <div class="n8n-quick-action" id="n8n-open-direct">
                            <div class="n8n-quick-action-icon">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                                    <polyline points="15 3 21 3 21 9"></polyline>
                                    <line x1="10" y1="14" x2="21" y2="3"></line>
                                </svg>
                            </div>
                            <div class="n8n-quick-action-text">
                                <div class="n8n-quick-action-title">Abrir n8n</div>
                                <div class="n8n-quick-action-desc">Ir a la interfaz de n8n</div>
                            </div>
                        </div>

                        <div class="n8n-quick-action" id="n8n-import-template">
                            <div class="n8n-quick-action-icon">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                    <polyline points="7 10 12 15 17 10"></polyline>
                                    <line x1="12" y1="15" x2="12" y2="3"></line>
                                </svg>
                            </div>
                            <div class="n8n-quick-action-text">
                                <div class="n8n-quick-action-title">Importar Rápido</div>
                                <div class="n8n-quick-action-desc">Importar plantilla recomendada</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="n8n-widget-footer">
                    <div class="n8n-widget-status">
                        <span class="n8n-widget-status-dot" id="n8n-widget-status-dot"></span>
                        <span id="n8n-widget-status-text">Verificando...</span>
                    </div>
                    <span id="n8n-widget-templates-count">-</span>
                </div>
            </div>
        `;

        document.body.appendChild(widget);
    }

    attachEventListeners() {
        const toggle = document.getElementById('n8n-widget-toggle');
        const panel = document.getElementById('n8n-widget-panel');

        toggle.addEventListener('click', () => {
            this.isOpen = !this.isOpen;
            panel.classList.toggle('open', this.isOpen);
        });

        // Abrir n8n
        document.getElementById('n8n-open-direct').addEventListener('click', () => {
            this.n8nManager.openN8N();
            this.close();
        });

        // Importar plantilla rápida
        document.getElementById('n8n-import-template').addEventListener('click', async () => {
            try {
                const templates = await this.n8nManager.getTemplatesByPriority(1);
                if (templates.length > 0) {
                    const template = templates[0];
                    const result = await this.n8nManager.importTemplate(template.id);
                    alert(`✓ Plantilla "${template.name}" importada!\n\nAbre n8n para activarla.`);
                    this.n8nManager.openN8N();
                } else {
                    alert('No hay plantillas de prioridad alta disponibles');
                }
            } catch (error) {
                alert(`Error: ${error.message}`);
            }
            this.close();
        });

        // Cerrar al hacer click fuera
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#n8n-widget') && this.isOpen) {
                this.close();
            }
        });
    }

    async checkStatus() {
        try {
            const status = await this.n8nManager.checkN8NStatus();
            const indicator = document.getElementById('n8n-status-indicator');
            const statusDot = document.getElementById('n8n-widget-status-dot');
            const statusText = document.getElementById('n8n-widget-status-text');

            if (status.available) {
                indicator.classList.remove('offline');
                statusDot.classList.remove('offline');
                statusText.textContent = 'Activo';
            } else {
                indicator.classList.add('offline');
                statusDot.classList.add('offline');
                statusText.textContent = 'Offline';
            }

            // Actualizar contador de plantillas
            const stats = await this.n8nManager.getStatistics();
            if (stats) {
                document.getElementById('n8n-widget-templates-count').textContent =
                    `${stats.recommended_templates || 0} plantillas`;
            }
        } catch (error) {
            console.error('Error checking n8n status:', error);
        }
    }

    close() {
        this.isOpen = false;
        document.getElementById('n8n-widget-panel').classList.remove('open');
    }

    open() {
        this.isOpen = true;
        document.getElementById('n8n-widget-panel').classList.add('open');
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
}

// Auto-inicializar si n8nManager está disponible
if (typeof n8nManager !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        window.n8nWidget = new N8NWidget({
            n8nManager: n8nManager,
            position: 'bottom-right'
        });
    });
}
