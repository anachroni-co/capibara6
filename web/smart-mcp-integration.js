/**
 * Smart MCP Integration v2.0
 * Basado en principios reales de MCP y RAG selectivo
 * Solo agrega contexto cuando es REALMENTE necesario
 */

const SMART_MCP_CONFIG = {
    // Usar el backend integrado de bounty2 que incluye MCP
    // En desarrollo local: usar proxy CORS local (puerto 8001) que conecta a bounty2:5001
    // En producción: usar Vercel que hace proxy al backend
    serverUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8001/api/mcp/tools/call'  // Proxy CORS local → bounty2:5001
        : 'https://www.capibara6.com/api/mcp/tools/call',   // Servidor en producción
    healthUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8001/api/mcp/status'  // Health check a través del proxy
        : 'https://www.capibara6.com/api/mcp/status',
    enabled: true,  // ✅ HABILITADO - Smart MCP integrado en backend de bounty2
    timeout: 5000, // 5 segundos máximo para desarrollo
    fallbackOnError: true
};

/**
 * Analiza la consulta y solo agrega contexto si es necesario
 */
async function smartMCPAnalyze(userQuery) {
    // Si está deshabilitado, devolver la query original
    if (!SMART_MCP_CONFIG.enabled) {
        return {
            needsContext: false,
            prompt: userQuery,
            lightweight: true
        };
    }

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), SMART_MCP_CONFIG.timeout);

        // Usar la URL configurada (ya incluye el proxy en desarrollo local)
        const serverUrl = SMART_MCP_CONFIG.serverUrl || 
            (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
                ? 'http://localhost:8001/api/mcp/tools/call'
                : 'https://www.capibara6.com/api/mcp/tools/call');

        const response = await fetch(serverUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                name: 'analyze_document',
                arguments: {
                    query: userQuery
                }
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`MCP server error: ${response.status}`);
        }

        const data = await response.json();
        
        // Log para debugging (solo si hay contexto agregado)
        if (data.needs_context) {
            console.log('🎯 Smart MCP: Contexto agregado', {
                contextsAdded: data.contexts_added,
                original: userQuery,
                augmented: data.augmented_prompt.substring(0, 100) + '...'
            });
        }

        return {
            needsContext: data.needs_context,
            prompt: data.augmented_prompt,
            contextsAdded: data.contexts_added,
            lightweight: data.lightweight
        };

    } catch (error) {
        if (error.name === 'AbortError') {
            console.warn('⏱️ Smart MCP timeout, usando query original');
        } else {
            console.error('❌ Smart MCP error:', error.message);
        }

        // Fallback: devolver query original
        if (SMART_MCP_CONFIG.fallbackOnError) {
            return {
                needsContext: false,
                prompt: userQuery,
                lightweight: true,
                error: error.message
            };
        }

        throw error;
    }
}

/**
 * Verifica el estado del servidor MCP
 */
async function checkSmartMCPHealth() {
    try {
        // Usar la URL de health configurada (a través del proxy en desarrollo local)
        const healthUrl = SMART_MCP_CONFIG.healthUrl || 
            (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
                ? 'http://localhost:8001/api/mcp/status'
                : 'https://www.capibara6.com/api/mcp/status');
        
        console.log(`🔍 Verificando Smart MCP en: ${healthUrl}`);
        
        const response = await fetch(healthUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            signal: AbortSignal.timeout(3000)  // 3 segundos de timeout
        });

        console.log(`📡 Respuesta MCP: status=${response.status}, ok=${response.ok}`);

        if (response.ok) {
            const data = await response.json();
            console.log('📦 Datos MCP:', data);
            
            // Verificar que la respuesta tenga datos válidos
            // El backend integrado puede devolver diferentes formatos
            if (data && (
                data.status === 'healthy' || 
                data.status === 'running' ||
                data.status === 'ok' ||
                data.service || 
                data.approach ||
                data.connector ||
                data.mcp_available === true
            )) {
                console.log('✅ Smart MCP ACTIVO:', data.service || data.approach || data.connector || data.status || 'healthy');
                return true;
            }
        }
        
        console.log('⚠️ Smart MCP respondió pero con formato inesperado');
        return false;
    } catch (error) {
        console.log('ℹ️ Smart MCP no disponible (se usará modo directo)');
        console.log('🔍 Error:', error.message);
        return false;
    }
}

/**
 * Toggle para habilitar/deshabilitar MCP desde la UI
 */
function toggleSmartMCP(enabled) {
    SMART_MCP_CONFIG.enabled = enabled;
    console.log(`🔄 Smart MCP ${enabled ? 'activado' : 'desactivado'}`);
    
    // Actualizar indicador en UI si existe
    const mcpIndicator = document.querySelector('.mcp-indicator');
    if (mcpIndicator) {
        mcpIndicator.classList.toggle('active', enabled);
        mcpIndicator.title = enabled 
            ? 'Smart MCP: Activo (contexto selectivo)' 
            : 'Smart MCP: Desactivado';
    }
}

// Exportar funciones globalmente
window.smartMCPAnalyze = smartMCPAnalyze;
window.checkSmartMCPHealth = checkSmartMCPHealth;
window.toggleSmartMCP = toggleSmartMCP;

// Verificar estado al cargar
document.addEventListener('DOMContentLoaded', () => {
    checkSmartMCPHealth().then(isActive => {
        SMART_MCP_CONFIG.enabled = isActive;
        
        // Actualizar indicador visual
        const mcpIndicator = document.querySelector('.mcp-indicator');
        if (mcpIndicator) {
            mcpIndicator.classList.toggle('active', isActive);
            mcpIndicator.title = isActive 
                ? 'Smart MCP v2.0: Activo (RAG selectivo)' 
                : 'Smart MCP: No disponible';
        }
    });
});

console.log('🚀 Smart MCP Integration v2.0 cargado');
console.log('📊 Enfoque: Selective RAG - Solo contexto cuando es necesario');

