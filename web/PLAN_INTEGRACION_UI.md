# 🎨 Plan de Integración de UI - Servicios Pendientes

## 📊 Resumen Ejecutivo

Se han identificado **7 servicios desarrollados** que tienen código completo pero **NO están integrados** en la UI principal del chat (`chat.html`). Estos servicios tienen interfaces funcionales y diseños modernos que deberían estar disponibles directamente desde el chat.

## 🔴 Servicios Críticos No Integrados

### 1. TTS (Text-to-Speech) - ⚠️ CRÍTICO
- **Archivo**: `tts-integration.js` (398 líneas)
- **Estado**: Código completo pero NO cargado
- **Impacto**: Los usuarios no pueden usar síntesis de voz
- **Solución**: Cargar script + añadir controles UI

### 2. MCP (Model Context Protocol) - ⚠️ CRÍTICO  
- **Archivos**: `smart-mcp-integration.js`, `mcp-integration.js`
- **Estado**: Integración completa pero NO cargada
- **Impacto**: No se usa el contexto inteligente MCP
- **Solución**: Cargar script + añadir indicadores UI

### 3. RAG System - ⚠️ IMPORTANTE
- **Archivos**: `rag-api-client.js`, `rag-demo.html`
- **Estado**: Cliente completo + demo separado
- **Impacto**: No se puede buscar en base de conocimiento
- **Solución**: Integrar búsqueda RAG en chat

### 4. N8n Dashboard - ⚠️ IMPORTANTE
- **Archivos**: `n8n-dashboard.html`, `n8n-manager.js`
- **Estado**: Dashboard completo pero página separada
- **Impacto**: No hay acceso fácil a workflows
- **Solución**: Widget en sidebar + acceso rápido

## 📝 Cambios Específicos Necesarios

### Cambio 1: Añadir Scripts en `chat.html`

**Ubicación**: Después de la línea 211 (`<script src="config.js"></script>`)

```html
<!-- Servicios de integración -->
<script src="tts-integration.js"></script>
<script src="smart-mcp-integration.js"></script>
<script src="rag-api-client.js"></script>
<script src="n8n-manager.js"></script>
<script src="model-visualization.js"></script>
<script src="entropy-monitor.js"></script>
```

### Cambio 2: Añadir Controles TTS en Header

**Ubicación**: En `chat-header-actions` (después de línea 113)

```html
<!-- Controles TTS -->
<div class="tts-controls" id="tts-controls" style="display: none;">
    <button class="btn-icon" id="tts-play-btn" title="Reproducir">
        <i data-lucide="play" style="width: 18px; height: 18px;"></i>
    </button>
    <button class="btn-icon" id="tts-pause-btn" title="Pausar" style="display: none;">
        <i data-lucide="pause" style="width: 18px; height: 18px;"></i>
    </button>
    <input type="range" id="tts-speed" min="0.5" max="2" step="0.1" value="1" 
           title="Velocidad" style="width: 80px; margin: 0 10px;">
</div>
```

### Cambio 3: Añadir Indicador MCP en Header

**Ubicación**: En `chat-status` (después de línea 106)

```html
<!-- Indicador MCP -->
<span class="mcp-indicator" id="mcp-indicator" title="MCP Contexto Inteligente">
    <i data-lucide="brain" style="width: 16px; height: 16px;"></i>
    <span id="mcp-status-text">MCP</span>
</span>
```

### Cambio 4: Añadir Panel Lateral RAG

**Ubicación**: Después del sidebar (antes de línea 94)

```html
<!-- Panel RAG (colapsable) -->
<aside class="rag-panel" id="rag-panel">
    <div class="rag-panel-header">
        <h3>🔍 Búsqueda RAG</h3>
        <button class="btn-icon" id="rag-panel-close">
            <i data-lucide="x" style="width: 18px; height: 18px;"></i>
        </button>
    </div>
    <div class="rag-panel-content">
        <input type="text" id="rag-search-input" placeholder="Buscar en conocimiento...">
        <button id="rag-search-btn">Buscar</button>
        <div id="rag-results"></div>
    </div>
</aside>
```

### Cambio 5: Añadir Widget N8n en Sidebar

**Ubicación**: En sidebar-section (después de línea 51)

```html
<!-- Widget N8n -->
<div class="sidebar-section">
    <div class="sidebar-section-header">
        <span class="section-title">Workflows</span>
        <button class="icon-btn-sm" id="n8n-dashboard-btn" title="Abrir Dashboard">
            <i data-lucide="external-link" style="width: 16px; height: 16px;"></i>
        </button>
    </div>
    <div class="n8n-widget" id="n8n-widget">
        <div class="n8n-status" id="n8n-status">
            <span class="status-dot"></span>
            <span>Cargando...</span>
        </div>
        <div class="n8n-workflows-list" id="n8n-workflows-list">
            <!-- Workflows activos se cargarán aquí -->
        </div>
    </div>
</div>
```

### Cambio 6: Añadir Botón RAG en Input Area

**Ubicación**: En `input-actions` (después de línea 143)

```html
<button class="input-action-btn" id="rag-search-btn-sidebar" title="Buscar en RAG">
    <i data-lucide="search" style="width: 20px; height: 20px;"></i>
</button>
```

## 🎨 Estilos CSS Necesarios

Añadir a `chat-styles.css`:

```css
/* Controles TTS */
.tts-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-right: 1rem;
}

/* Indicador MCP */
.mcp-indicator {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.5rem;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 6px;
    font-size: 0.75rem;
    color: var(--primary);
}

.mcp-indicator.active {
    background: rgba(102, 126, 234, 0.2);
    animation: pulse 2s infinite;
}

/* Panel RAG */
.rag-panel {
    position: fixed;
    right: 0;
    top: 0;
    width: 400px;
    height: 100vh;
    background: var(--bg-card);
    border-left: 1px solid var(--border);
    z-index: 100;
    transform: translateX(100%);
    transition: transform 0.3s;
}

.rag-panel.open {
    transform: translateX(0);
}

/* Widget N8n */
.n8n-widget {
    padding: 0.5rem;
}

.n8n-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    font-size: 0.75rem;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--success);
}

.status-dot.inactive {
    background: var(--danger);
}
```

## 🔧 Inicialización en JavaScript

Añadir en `chat-page.js` después de `init()`:

```javascript
async init() {
    // ... código existente ...
    
    // Inicializar servicios
    this.initTTSService();
    this.initMCPService();
    this.initRAGService();
    this.initN8NService();
}

initTTSService() {
    // Inicializar TTS si está disponible
    if (typeof TTS_CONFIG !== 'undefined') {
        // Configurar event listeners para controles TTS
        document.getElementById('tts-play-btn')?.addEventListener('click', () => {
            // Lógica TTS
        });
    }
}

initMCPService() {
    // Inicializar MCP si está disponible
    if (typeof SmartMCPIntegration !== 'undefined') {
        const mcp = new SmartMCPIntegration({
            serverUrl: CHATBOT_CONFIG.SERVICE_URLS?.MCP
        });
        this.mcpService = mcp;
        this.updateMCPIndicator();
    }
}

initRAGService() {
    // Inicializar RAG si está disponible
    if (typeof Capibara6API !== 'undefined') {
        const ragUrl = CHATBOT_CONFIG.SERVICE_URLS?.RAG_API || 'http://localhost:8000';
        this.ragClient = new Capibara6API(ragUrl);
    }
}

initN8NService() {
    // Inicializar N8n si está disponible
    if (typeof N8NManager !== 'undefined') {
        const n8nUrl = CHATBOT_CONFIG.SERVICE_URLS?.N8N || 'http://localhost:5678';
        this.n8nManager = new N8NManager({ n8nURL: n8nUrl });
        this.loadN8NWorkflows();
    }
}
```

## ✅ Checklist de Implementación

- [ ] Añadir scripts en `chat.html`
- [ ] Añadir controles TTS en header
- [ ] Añadir indicador MCP en header
- [ ] Añadir panel lateral RAG
- [ ] Añadir widget N8n en sidebar
- [ ] Añadir botón RAG en input area
- [ ] Añadir estilos CSS
- [ ] Implementar inicialización en JavaScript
- [ ] Probar funcionalidad TTS
- [ ] Probar funcionalidad MCP
- [ ] Probar funcionalidad RAG
- [ ] Probar funcionalidad N8n

## 📊 Impacto Esperado

Después de la integración:

- ✅ Usuarios podrán usar TTS directamente desde el chat
- ✅ MCP estará activo y visible
- ✅ Búsqueda RAG disponible desde el chat
- ✅ Acceso rápido a workflows N8n
- ✅ UI más completa y funcional
- ✅ Mejor experiencia de usuario

---

**Prioridad**: ALTA
**Tiempo estimado**: 4-6 horas
**Complejidad**: Media

