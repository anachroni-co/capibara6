/**
 * Proxy de MCP para evitar problemas de CORS
 * Utiliza endpoints proxy en el backend Flask para evitar problemas de CORS
 */

class MCPCORSProxy {
    constructor() {
        // IP del servidor backend
        this.backendUrl = 'http://34.12.166.76:5000';
    }

    /**
     * Proxy para la llamada MCP - Usando endpoint proxy en el backend Flask
     */
    async callMCPTask(taskData) {
        try {
            // Usar endpoint proxy en el servidor proxy local para evitar CORS
            // El proxy local redirige la solicitud al backend real
            const response = await fetch('http://localhost:8001/api/mcp/tools/call-proxy', {  // Endpoint proxy en servidor local en puerto 8001
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });

            if (!response.ok) {
                throw new Error(`MCP Tools Call Proxy failed: ${response.status} - ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error en conexión MCP a través del proxy:', error);
            // Si falla con el proxy, intentar directamente como fallback
            try {
                // Intentar con endpoint directo como último recurso
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 segundos timeout

                const directResponse = await fetch('http://34.12.166.76:5000/api/mcp/tools/call', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(taskData),
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!directResponse.ok) {
                    throw new Error(`Direct MCP call failed: ${directResponse.status}`);
                }

                return await directResponse.json();
            } catch (directError) {
                console.error('Error también en conexión directa:', directError);
                throw error; // Lanzar el error original
            }
        }
    }

    /**
     * Proxy para el status MCP - Usando endpoint proxy en el backend Flask
     */
    async getMCPStatus() {
        try {
            // Usar endpoint genérico de proxy en el backend
            const response = await fetch('/api/proxy', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    target_url: 'http://34.12.166.76:5000/api/mcp/status',
                    method: 'GET'
                })
            });

            if (!response.ok) {
                throw new Error(`MCP Status Proxy failed: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error obteniendo estado MCP a través del proxy:', error);
            // Intentar directamente como fallback
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 segundos timeout

                const directResponse = await fetch('http://34.12.166.76:5000/api/mcp/status', {
                    method: 'GET',
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!directResponse.ok) {
                    throw new Error(`Direct MCP status failed: ${directResponse.status}`);
                }

                return await directResponse.json();
            } catch (directError) {
                console.error('Error también en estado MCP directo:', directError);
                throw error; // Lanzar el error original
            }
        }
    }
}

// Exportar globalmente
window.MCPCORSProxy = MCPCORSProxy;