/**
 * Account Management - Gestión completa de cuenta, redes sociales, N8n y preferencias
 * Integración con el modal de cuenta de Capibara6
 */

class AccountManager {
    constructor(backendUrl) {
        this.backendUrl = backendUrl || (typeof CHATBOT_CONFIG !== 'undefined' ? CHATBOT_CONFIG.BACKEND_URL : 'http://localhost:8001');
        this.init();
    }

    init() {
        this.setupTabSwitching();
        this.setupSocialAccounts();
        this.setupN8nIntegration();
        this.setupPreferences();
        this.loadAllData();
    }

    // ============================================
    // Tab Switching
    // ============================================
    
    setupTabSwitching() {
        const tabs = document.querySelectorAll('.account-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetTab = tab.getAttribute('data-tab');
                this.switchTab(targetTab);
            });
        });
    }

    switchTab(tabName) {
        // Desactivar todos los tabs
        document.querySelectorAll('.account-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.account-tab-content').forEach(c => c.classList.remove('active'));

        // Activar el tab seleccionado
        const tabButton = document.querySelector(`.account-tab[data-tab="${tabName}"]`);
        const tabContent = document.getElementById(`tab-${tabName}`);
        
        if (tabButton) tabButton.classList.add('active');
        if (tabContent) tabContent.classList.add('active');

        // Cargar datos específicos del tab
        if (tabName === 'social') this.loadSocialAccounts();
        if (tabName === 'n8n') this.loadN8nStatus();
        if (tabName === 'preferences') this.loadPreferences();
    }

    // ============================================
    // Redes Sociales
    // ============================================

    setupSocialAccounts() {
        // Añadir cuenta
        const addBtn = document.getElementById('add-social-account-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.addSocialAccount());
        }

        // Importar datos
        const importBtn = document.getElementById('import-social-data-btn');
        if (importBtn) {
            importBtn.addEventListener('click', () => this.importSocialData());
        }
    }

    loadSocialAccounts() {
        const accounts = this.getSocialAccounts();
        const container = document.getElementById('social-accounts-list');
        if (!container) return;

        if (accounts.length === 0) {
            container.innerHTML = '<p class="empty-state">No hay cuentas de redes sociales conectadas.</p>';
            return;
        }

        container.innerHTML = accounts.map(account => `
            <div class="social-account-item" data-platform="${account.platform}">
                <div class="social-account-header">
                    <div class="social-icon ${account.platform}">
                        <i data-lucide="${this.getPlatformIcon(account.platform)}" style="width: 20px; height: 20px;"></i>
                    </div>
                    <div class="social-account-info">
                        <h5>${this.getPlatformName(account.platform)}</h5>
                        <span>${account.username || account.url || 'Sin información'}</span>
                    </div>
                    <div class="social-account-actions">
                        <button class="icon-btn-sm" onclick="accountManager.removeSocialAccount('${account.id}')" title="Eliminar">
                            <i data-lucide="trash-2" style="width: 16px; height: 16px;"></i>
                        </button>
                    </div>
                </div>
                ${account.syncEnabled ? '<span class="sync-badge">Sincronizado</span>' : ''}
            </div>
        `).join('');

        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }

    async addSocialAccount() {
        const platform = document.getElementById('social-platform').value;
        const username = document.getElementById('social-username').value.trim();
        const url = document.getElementById('social-url').value.trim();
        const syncEnabled = document.getElementById('social-sync-enabled').checked;

        if (!platform) {
            this.showError('Selecciona una plataforma');
            return;
        }

        const account = {
            id: `social_${Date.now()}`,
            platform,
            username,
            url,
            syncEnabled,
            createdAt: new Date().toISOString()
        };

        const accounts = this.getSocialAccounts();
        accounts.push(account);
        this.saveSocialAccounts(accounts);

        // Limpiar formulario
        document.getElementById('social-platform').value = '';
        document.getElementById('social-username').value = '';
        document.getElementById('social-url').value = '';
        document.getElementById('social-sync-enabled').checked = false;

        this.loadSocialAccounts();
        this.showSuccess('Cuenta añadida correctamente');
    }

    removeSocialAccount(accountId) {
        const accounts = this.getSocialAccounts();
        const filtered = accounts.filter(a => a.id !== accountId);
        this.saveSocialAccounts(filtered);
        this.loadSocialAccounts();
        this.showSuccess('Cuenta eliminada');
    }

    async importSocialData() {
        const platform = document.getElementById('import-platform').value;
        const fileInput = document.getElementById('import-file');
        const file = fileInput.files[0];

        if (!platform || !file) {
            this.showError('Selecciona plataforma y archivo');
            return;
        }

        try {
            const text = await file.text();
            const data = file.name.endsWith('.json') ? JSON.parse(text) : this.parseCSV(text);

            // Guardar datos importados
            const importedData = this.getImportedSocialData();
            importedData[platform] = {
                data,
                importedAt: new Date().toISOString(),
                fileName: file.name
            };
            this.saveImportedSocialData(importedData);

            this.showSuccess(`Datos de ${this.getPlatformName(platform)} importados correctamente`);
            fileInput.value = '';
        } catch (error) {
            console.error('Error importing data:', error);
            this.showError('Error al importar datos: ' + error.message);
        }
    }

    parseCSV(text) {
        // Implementación básica de CSV parser
        const lines = text.split('\n');
        const headers = lines[0].split(',');
        return lines.slice(1).map(line => {
            const values = line.split(',');
            const obj = {};
            headers.forEach((header, i) => {
                obj[header.trim()] = values[i]?.trim() || '';
            });
            return obj;
        });
    }

    getSocialAccounts() {
        const stored = localStorage.getItem('capibara6_social_accounts');
        return stored ? JSON.parse(stored) : [];
    }

    saveSocialAccounts(accounts) {
        localStorage.setItem('capibara6_social_accounts', JSON.stringify(accounts));
    }

    getImportedSocialData() {
        const stored = localStorage.getItem('capibara6_imported_social_data');
        return stored ? JSON.parse(stored) : {};
    }

    saveImportedSocialData(data) {
        localStorage.setItem('capibara6_imported_social_data', JSON.stringify(data));
    }

    getPlatformIcon(platform) {
        const icons = {
            twitter: 'twitter',
            linkedin: 'linkedin',
            instagram: 'instagram',
            github: 'github',
            facebook: 'facebook',
            youtube: 'youtube'
        };
        return icons[platform] || 'share-2';
    }

    getPlatformName(platform) {
        const names = {
            twitter: 'Twitter / X',
            linkedin: 'LinkedIn',
            instagram: 'Instagram',
            github: 'GitHub',
            facebook: 'Facebook',
            youtube: 'YouTube'
        };
        return names[platform] || platform;
    }

    // ============================================
    // N8n Integration
    // ============================================

    setupN8nIntegration() {
        const refreshBtn = document.getElementById('refresh-n8n-workflows-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadN8nWorkflows());
        }

        const dashboardBtn = document.getElementById('open-n8n-dashboard-btn');
        if (dashboardBtn) {
            dashboardBtn.addEventListener('click', () => this.openN8nDashboard());
        }

        const templatesBtn = document.getElementById('n8n-templates-btn');
        if (templatesBtn) {
            templatesBtn.addEventListener('click', () => this.openN8nTemplates());
        }
    }

    async loadN8nStatus() {
        const n8nUrl = this.getN8nUrl();
        const statusEl = document.getElementById('n8n-account-status');
        const infoEl = document.getElementById('n8n-status-info');

        if (!statusEl || !infoEl) return;

        try {
            const response = await fetch(`${n8nUrl}/healthz`, { method: 'GET' });
            if (response.ok) {
                statusEl.textContent = 'Activo';
                statusEl.className = 'status-badge success';
                infoEl.innerHTML = `<p>N8n está funcionando correctamente en <a href="${n8nUrl}" target="_blank">${n8nUrl}</a></p>`;
            } else {
                throw new Error('N8n no disponible');
            }
        } catch (error) {
            statusEl.textContent = 'No disponible';
            statusEl.className = 'status-badge error';
            infoEl.innerHTML = `<p>No se pudo conectar con N8n. Verifica la URL: ${n8nUrl}</p>`;
        }

        // Cargar workflows
        await this.loadN8nWorkflows();
    }

    async loadN8nWorkflows() {
        const container = document.getElementById('n8n-workflows-list');
        if (!container) return;

        container.innerHTML = '<p>Cargando workflows...</p>';

        try {
            const n8nUrl = this.getN8nUrl();
            // Nota: Esto requeriría autenticación en producción
            container.innerHTML = '<p>Para ver workflows, abre el dashboard de N8n directamente.</p>';
        } catch (error) {
            container.innerHTML = '<p class="error">Error al cargar workflows</p>';
        }
    }

    openN8nDashboard() {
        const n8nUrl = this.getN8nUrl();
        window.open(n8nUrl, '_blank');
    }

    openN8nTemplates() {
        window.open('/n8n-dashboard.html', '_blank');
    }

    getN8nUrl() {
        const input = document.getElementById('n8n-url');
        if (input && input.value) {
            this.saveN8nUrl(input.value);
            return input.value;
        }
        const saved = localStorage.getItem('capibara6_n8n_url');
        // En producción, usar endpoint proxy de Vercel, de lo contrario usar URL de servicio directo
        if (typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.BACKEND_URL && !CHATBOT_CONFIG.BACKEND_URL.includes('localhost')) {
            // En producción, usar un proxy de Vercel para N8N
            return 'https://www.capibara6.com/n8n';
        } else {
            return saved || (typeof CHATBOT_CONFIG !== 'undefined' && CHATBOT_CONFIG.SERVICE_URLS?.N8N) || 'http://34.175.136.104:5678';
        }
    }

    saveN8nUrl(url) {
        localStorage.setItem('capibara6_n8n_url', url);
    }

    // ============================================
    // Preferencias
    // ============================================

    setupPreferences() {
        // Idioma
        const languageSelect = document.getElementById('pref-language');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.savePreference('language', e.target.value);
            });
        }

        // Timezone
        const timezoneSelect = document.getElementById('pref-timezone');
        if (timezoneSelect) {
            timezoneSelect.addEventListener('change', (e) => {
                this.savePreference('timezone', e.target.value);
            });
        }

        // Checkboxes
        const checkboxes = [
            'pref-notifications-email',
            'pref-notifications-browser',
            'pref-notifications-sound',
            'pref-privacy-analytics',
            'pref-privacy-personalization',
            'pref-privacy-gemelo',
            'pref-chat-auto-scroll',
            'pref-chat-markdown',
            'pref-chat-streaming',
            'pref-data-backup'
        ];

        checkboxes.forEach(id => {
            const checkbox = document.getElementById(id);
            if (checkbox) {
                checkbox.addEventListener('change', (e) => {
                    const key = id.replace('pref-', '');
                    this.savePreference(key, e.target.checked);
                });
            }
        });

        // Historial de chats
        const historySelect = document.getElementById('pref-chat-history');
        if (historySelect) {
            historySelect.addEventListener('change', (e) => {
                this.savePreference('chatHistory', e.target.value);
            });
        }

        // Limpiar caché
        const clearCacheBtn = document.getElementById('clear-cache-btn');
        if (clearCacheBtn) {
            clearCacheBtn.addEventListener('click', () => this.clearCache());
        }

        // Exportar datos
        const exportBtn = document.getElementById('export-data-btn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportData());
        }

        // Calcular almacenamiento
        this.calculateStorage();
    }

    loadPreferences() {
        const prefs = this.getPreferences();

        // Idioma
        const languageSelect = document.getElementById('pref-language');
        if (languageSelect && prefs.language) {
            languageSelect.value = prefs.language;
        }

        // Timezone
        const timezoneSelect = document.getElementById('pref-timezone');
        if (timezoneSelect && prefs.timezone) {
            timezoneSelect.value = prefs.timezone;
        }

        // Checkboxes
        Object.keys(prefs).forEach(key => {
            const checkbox = document.getElementById(`pref-${key}`);
            if (checkbox && typeof prefs[key] === 'boolean') {
                checkbox.checked = prefs[key];
            }
        });

        // Historial
        const historySelect = document.getElementById('pref-chat-history');
        if (historySelect && prefs.chatHistory) {
            historySelect.value = prefs.chatHistory;
        }

        // N8n URL
        const n8nUrlInput = document.getElementById('n8n-url');
        if (n8nUrlInput) {
            n8nUrlInput.value = this.getN8nUrl();
        }
    }

    getPreferences() {
        const stored = localStorage.getItem('capibara6_preferences');
        return stored ? JSON.parse(stored) : {
            language: 'es',
            timezone: 'Europe/Madrid',
            notificationsBrowser: true,
            notificationsSound: true,
            privacyAnalytics: true,
            privacyPersonalization: true,
            chatAutoScroll: true,
            chatMarkdown: true,
            chatStreaming: true,
            dataBackup: true,
            chatHistory: '25'
        };
    }

    savePreference(key, value) {
        const prefs = this.getPreferences();
        prefs[key] = value;
        localStorage.setItem('capibara6_preferences', JSON.stringify(prefs));
    }

    calculateStorage() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                total += localStorage[key].length + key.length;
            }
        }
        const mb = (total / 1024 / 1024).toFixed(2);
        const storageEl = document.getElementById('storage-used');
        if (storageEl) {
            storageEl.textContent = `${mb} MB`;
        }
    }

    clearCache() {
        if (confirm('¿Estás seguro de que quieres limpiar la caché? Esto eliminará datos temporales pero no tus conversaciones.')) {
            // Limpiar solo datos temporales, no conversaciones ni configuración
            const keysToKeep = [
                'capibara6_chats',
                'capibara6_user',
                'capibara6_settings',
                'capibara6_preferences',
                'capibara6_social_accounts',
                'capibara6_imported_social_data'
            ];
            
            const allKeys = Object.keys(localStorage);
            allKeys.forEach(key => {
                if (!keysToKeep.includes(key)) {
                    localStorage.removeItem(key);
                }
            });

            this.calculateStorage();
            this.showSuccess('Caché limpiada correctamente');
        }
    }

    exportData() {
        const data = {
            user: JSON.parse(localStorage.getItem('capibara6_user') || '{}'),
            chats: JSON.parse(localStorage.getItem('capibara6_chats') || '[]'),
            settings: JSON.parse(localStorage.getItem('capibara6_settings') || '{}'),
            preferences: this.getPreferences(),
            socialAccounts: this.getSocialAccounts(),
            importedSocialData: this.getImportedSocialData(),
            exportedAt: new Date().toISOString()
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `capibara6-export-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);

        this.showSuccess('Datos exportados correctamente');
    }

    // ============================================
    // Utilidades
    // ============================================

    loadAllData() {
        this.loadSocialAccounts();
        this.loadPreferences();
    }

    showSuccess(message) {
        // Usar el sistema de notificaciones existente si está disponible
        if (window.chatPage && typeof window.chatPage.showSuccess === 'function') {
            window.chatPage.showSuccess(message);
        } else {
            alert(message);
        }
    }

    showError(message) {
        if (window.chatPage && typeof window.chatPage.showError === 'function') {
            window.chatPage.showError(message);
        } else {
            alert(message);
        }
    }
}

// Inicializar cuando el DOM esté listo
let accountManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        accountManager = new AccountManager();
        window.accountManager = accountManager;
    });
} else {
    accountManager = new AccountManager();
    window.accountManager = accountManager;
}

