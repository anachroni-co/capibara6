# 🎨 Integración Completa de UI - Capibara6

## ✅ Funcionalidades Implementadas

He creado un sistema completo de gestión de cuenta que incluye:

### 1. **Redes Sociales** ✅
- Gestión de cuentas de redes sociales (Twitter, LinkedIn, Instagram, GitHub, Facebook, YouTube)
- Importación de datos desde archivos JSON/CSV
- Sincronización automática
- Almacenamiento en localStorage

### 2. **N8n** ✅
- Verificación de estado de N8n
- Configuración de URL del servidor
- Acceso rápido al dashboard
- Gestión de workflows

### 3. **Opciones y Preferencias** ✅
- Idioma y zona horaria
- Configuración de notificaciones
- Privacidad
- Configuración de chat y modelo
- Gestión de almacenamiento
- Exportación de datos

### 4. **Gemelo Digital** ✅
- Ya existente en el HTML
- Integrado con datos de redes sociales

## 📝 Cambios Necesarios en `web/chat.html`

### Paso 1: Actualizar los Tabs

Busca esta sección (línea ~341):
```html
<div class="account-tabs">
    <button class="account-tab active" data-tab="profile">
        <i data-lucide="user" style="width: 18px; height: 18px;"></i>
        Perfil
    </button>
    <button class="account-tab" data-tab="digital-twin">
        <i data-lucide="sparkles" style="width: 18px; height: 18px;"></i>
        Gemelo Digital
    </button>
</div>
```

Reemplázala con:
```html
<div class="account-tabs">
    <button class="account-tab active" data-tab="profile">
        <i data-lucide="user" style="width: 18px; height: 18px;"></i>
        Perfil
    </button>
    <button class="account-tab" data-tab="social">
        <i data-lucide="share-2" style="width: 18px; height: 18px;"></i>
        Redes Sociales
    </button>
    <button class="account-tab" data-tab="digital-twin">
        <i data-lucide="sparkles" style="width: 18px; height: 18px;"></i>
        Gemelo Digital
    </button>
    <button class="account-tab" data-tab="n8n">
        <i data-lucide="workflow" style="width: 18px; height: 18px;"></i>
        N8n
    </button>
    <button class="account-tab" data-tab="preferences">
        <i data-lucide="settings" style="width: 18px; height: 18px;"></i>
        Opciones
    </button>
</div>
```

### Paso 2: Añadir los Nuevos Tabs Content

Añade estos nuevos tabs ANTES del cierre de `</div>` del `modal-body` (antes de la línea 538):

```html
<!-- Tab: Redes Sociales -->
<div class="account-tab-content" id="tab-social">
    <div class="account-section">
        <h3>Gestión de Redes Sociales</h3>
        <p class="section-description">Conecta y guarda tus datos de redes sociales para mejorar tu gemelo digital.</p>
        
        <!-- Lista de redes sociales conectadas -->
        <div class="social-accounts-list" id="social-accounts-list">
            <!-- Se cargará dinámicamente -->
        </div>

        <!-- Formulario para añadir cuenta -->
        <div class="add-social-account">
            <h4>Añadir Nueva Cuenta</h4>
            <div class="form-group">
                <label for="social-platform">Plataforma</label>
                <select id="social-platform" class="form-input">
                    <option value="">Seleccionar plataforma</option>
                    <option value="twitter">Twitter / X</option>
                    <option value="linkedin">LinkedIn</option>
                    <option value="instagram">Instagram</option>
                    <option value="github">GitHub</option>
                    <option value="facebook">Facebook</option>
                    <option value="youtube">YouTube</option>
                </select>
            </div>
            <div class="form-group">
                <label for="social-username">Usuario/Nombre</label>
                <input type="text" id="social-username" class="form-input" placeholder="@usuario o nombre">
            </div>
            <div class="form-group">
                <label for="social-url">URL del Perfil (opcional)</label>
                <input type="url" id="social-url" class="form-input" placeholder="https://...">
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="social-sync-enabled">
                    Sincronizar automáticamente
                </label>
            </div>
            <button class="btn-primary btn-full" id="add-social-account-btn">
                <i data-lucide="plus" style="width: 18px; height: 18px;"></i>
                Añadir Cuenta
            </button>
        </div>

        <!-- Importar datos desde archivo -->
        <div class="import-social-data">
            <h4>Importar Datos</h4>
            <p class="section-description">Importa datos de tus redes sociales desde archivos JSON o CSV.</p>
            <div class="form-group">
                <label for="import-platform">Plataforma</label>
                <select id="import-platform" class="form-input">
                    <option value="">Seleccionar plataforma</option>
                    <option value="twitter">Twitter / X</option>
                    <option value="linkedin">LinkedIn</option>
                    <option value="instagram">Instagram</option>
                    <option value="github">GitHub</option>
                </select>
            </div>
            <div class="form-group">
                <label for="import-file">Archivo</label>
                <input type="file" id="import-file" class="form-input" accept=".json,.csv">
            </div>
            <button class="btn-secondary btn-full" id="import-social-data-btn">
                <i data-lucide="upload" style="width: 18px; height: 18px;"></i>
                Importar Datos
            </button>
        </div>
    </div>
</div>

<!-- Tab: N8n -->
<div class="account-tab-content" id="tab-n8n">
    <div class="account-section">
        <h3>Configuración de N8n</h3>
        <p class="section-description">Gestiona tus workflows y automatizaciones de N8n.</p>
        
        <!-- Estado de N8n -->
        <div class="n8n-status-section">
            <div class="status-card">
                <div class="status-header">
                    <span>Estado de N8n</span>
                    <span class="status-badge" id="n8n-account-status">Verificando...</span>
                </div>
                <div class="status-info" id="n8n-status-info">
                    <p>Cargando información...</p>
                </div>
            </div>
        </div>

        <!-- Configuración de URL -->
        <div class="form-group">
            <label for="n8n-url">URL de N8n</label>
            <input type="url" id="n8n-url" class="form-input" placeholder="http://34.175.136.104:5678">
            <small class="form-hint">URL del servidor N8n</small>
        </div>

        <!-- Workflows activos -->
        <div class="n8n-workflows-section">
            <h4>Workflows Activos</h4>
            <div class="workflows-list" id="n8n-workflows-list">
                <!-- Se cargará dinámicamente -->
            </div>
            <button class="btn-secondary btn-full" id="refresh-n8n-workflows-btn">
                <i data-lucide="refresh-cw" style="width: 18px; height: 18px;"></i>
                Actualizar Workflows
            </button>
        </div>

        <!-- Acciones rápidas -->
        <div class="n8n-actions">
            <h4>Acciones Rápidas</h4>
            <div class="action-buttons-grid">
                <button class="btn-secondary" id="open-n8n-dashboard-btn">
                    <i data-lucide="external-link" style="width: 18px; height: 18px;"></i>
                    Abrir Dashboard
                </button>
                <button class="btn-secondary" id="n8n-templates-btn">
                    <i data-lucide="file-text" style="width: 18px; height: 18px;"></i>
                    Ver Plantillas
                </button>
                <button class="btn-secondary" id="n8n-webhooks-btn">
                    <i data-lucide="webhook" style="width: 18px; height: 18px;"></i>
                    Webhooks
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Tab: Opciones y Preferencias -->
<div class="account-tab-content" id="tab-preferences">
    <div class="account-section">
        <h3>Preferencias Generales</h3>
        
        <!-- Idioma y Región -->
        <div class="settings-section">
            <h4>Idioma y Región</h4>
            <div class="form-group">
                <label for="pref-language">Idioma</label>
                <select id="pref-language" class="form-input">
                    <option value="es">Español</option>
                    <option value="en">English</option>
                    <option value="ca">Català</option>
                    <option value="eu">Euskera</option>
                </select>
            </div>
            <div class="form-group">
                <label for="pref-timezone">Zona Horaria</label>
                <select id="pref-timezone" class="form-input">
                    <option value="Europe/Madrid">Europe/Madrid (GMT+1)</option>
                    <option value="UTC">UTC</option>
                    <option value="America/New_York">America/New_York (GMT-5)</option>
                    <option value="America/Los_Angeles">America/Los_Angeles (GMT-8)</option>
                </select>
            </div>
        </div>

        <!-- Notificaciones -->
        <div class="settings-section">
            <h4>Notificaciones</h4>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-notifications-email">
                    Recibir notificaciones por email
                </label>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-notifications-browser" checked>
                    Notificaciones del navegador
                </label>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-notifications-sound" checked>
                    Sonidos de notificación
                </label>
            </div>
        </div>

        <!-- Privacidad -->
        <div class="settings-section">
            <h4>Privacidad</h4>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-privacy-analytics" checked>
                    Compartir datos de uso anónimos
                </label>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-privacy-personalization" checked>
                    Permitir personalización basada en uso
                </label>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-privacy-gemelo">
                    Compartir datos con gemelo digital
                </label>
            </div>
        </div>

        <!-- Chat y Modelo -->
        <div class="settings-section">
            <h4>Chat y Modelo</h4>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-chat-auto-scroll" checked>
                    Auto-scroll en chat
                </label>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-chat-markdown" checked>
                    Renderizar Markdown
                </label>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-chat-streaming" checked>
                    Respuestas en streaming
                </label>
            </div>
            <div class="form-group">
                <label for="pref-chat-history">Historial de chats a mantener</label>
                <select id="pref-chat-history" class="form-input">
                    <option value="10">10 chats</option>
                    <option value="25" selected>25 chats</option>
                    <option value="50">50 chats</option>
                    <option value="unlimited">Ilimitado</option>
                </select>
            </div>
        </div>

        <!-- Datos y Almacenamiento -->
        <div class="settings-section">
            <h4>Datos y Almacenamiento</h4>
            <div class="storage-info">
                <p>Espacio utilizado: <span id="storage-used">Calculando...</span></p>
                <button class="btn-secondary" id="clear-cache-btn">
                    <i data-lucide="trash-2" style="width: 18px; height: 18px;"></i>
                    Limpiar Caché
                </button>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" id="pref-data-backup" checked>
                    Hacer copia de seguridad automática
                </label>
            </div>
            <div class="form-group">
                <button class="btn-secondary btn-full" id="export-data-btn">
                    <i data-lucide="download" style="width: 18px; height: 18px;"></i>
                    Exportar Mis Datos
                </button>
            </div>
        </div>
    </div>
</div>
```

### Paso 3: Incluir el JavaScript

Añade esta línea ANTES de `chat-page.js` (línea ~600):

```html
<script src="account-management.js"></script>
```

## 🎨 Estilos CSS Necesarios

Añade estos estilos a `web/chat-styles.css`:

```css
/* Tabs de cuenta */
.account-tabs {
    display: flex;
    gap: 8px;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 24px;
    overflow-x: auto;
}

.account-tab {
    padding: 12px 16px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.account-tab:hover {
    color: var(--text-primary);
}

.account-tab.active {
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
}

.account-tab-content {
    display: none;
}

.account-tab-content.active {
    display: block;
}

/* Redes Sociales */
.social-accounts-list {
    margin-bottom: 24px;
}

.social-account-item {
    padding: 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.social-account-header {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
}

.social-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.social-icon.twitter { background: #1DA1F2; }
.social-icon.linkedin { background: #0077B5; }
.social-icon.instagram { background: #E4405F; }
.social-icon.github { background: #181717; }
.social-icon.facebook { background: #1877F2; }
.social-icon.youtube { background: #FF0000; }

.sync-badge {
    padding: 4px 8px;
    background: var(--success-color);
    color: white;
    border-radius: 4px;
    font-size: 12px;
}

/* N8n */
.status-card {
    padding: 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    margin-bottom: 24px;
}

.status-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.status-badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}

.status-badge.success {
    background: var(--success-color);
    color: white;
}

.status-badge.error {
    background: var(--error-color);
    color: white;
}

.action-buttons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
}

/* Preferencias */
.storage-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background: var(--bg-secondary);
    border-radius: 8px;
    margin-bottom: 16px;
}

.empty-state {
    text-align: center;
    padding: 32px;
    color: var(--text-secondary);
}
```

## ✅ Archivos Creados

1. **`web/account-management.js`** - Gestión completa de cuenta, redes sociales, N8n y preferencias

## 🚀 Funcionalidades

### Redes Sociales
- ✅ Añadir cuentas manualmente
- ✅ Importar datos desde archivos JSON/CSV
- ✅ Ver cuentas conectadas
- ✅ Eliminar cuentas
- ✅ Sincronización automática

### N8n
- ✅ Verificar estado del servidor
- ✅ Configurar URL
- ✅ Acceso rápido al dashboard
- ✅ Ver plantillas

### Preferencias
- ✅ Idioma y zona horaria
- ✅ Notificaciones
- ✅ Privacidad
- ✅ Configuración de chat
- ✅ Gestión de almacenamiento
- ✅ Exportar datos

## 📝 Próximos Pasos

1. Añadir los tabs al HTML según las instrucciones
2. Añadir los contenidos de los tabs
3. Incluir `account-management.js` en el HTML
4. Añadir los estilos CSS
5. Probar todas las funcionalidades

¡Todo listo para integrar! 🎉

