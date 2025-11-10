/**
 * Proxy de MCP para evitar problemas de CORS
 * Redirige las llamadas MCP a través del backend local para evitar CORS
 */

class MCPCORSProxy {
    constructor(localBackendUrl) {
        this.localBackendUrl = localBackendUrl || 'http://localhost:8080/proxy/mcp';
    }

    /**
     * Proxy para la llamada MCP
     */
    async callMCPTask(taskData) {
        try {
            // Usar el backend local como proxy para evitar CORS
            const response = await fetch(`${window.location.origin}/api/mcp-proxy`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    target: 'http://34.12.166.76:5000/api/mcp/tools/call',  // URL remota real
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: taskData
                })
            });

            if (!response.ok) {
                throw new Error(`Proxy response failed: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error en MCP proxy:', error);
            throw error;
        }
    }

    /**
     * Proxy para el status MCP
     */
    async getMCPStatus() {
        try {
            const response = await fetch(`${window.location.origin}/api/mcp-proxy`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    target: 'http://34.12.166.76:5000/api/mcp/status',  // URL remota real
                    method: 'GET'
                })
            });

            if (!response.ok) {
                throw new Error(`MCP Status proxy failed: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error en MCP Status proxy:', error);
            throw error;
        }
    }
}

// Exportar globalmente
window.MCPCORSProxy = MCPCORSProxy;