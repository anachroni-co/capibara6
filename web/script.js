// script.js - Funciones generales para la plataforma Capibara6

document.addEventListener('DOMContentLoaded', function() {
    console.log('Capibara6 plataforma cargada');
    
    // Inicializar animaciones neuronales
    if (typeof initNeuralAnimation === 'function') {
        initNeuralAnimation();
    }
});

// Configuración de endpoints
const API_ENDPOINTS = {
    // Servidor local con CTM y e2b
    // NOTA: Reemplaza [IP_DE_BOUNTY2] con la IP externa real de la VM bounty2
    // Para obtenerla, ejecuta: gcloud compute instances describe bounty2 --zone=europe-west4-a --project=mamba-001
    LOCAL: window.location.hostname === 'localhost' 
        ? 'http://[IP_DE_BOUNTY2]:5001/api'   // VM bounty2 en europe-west4-a en desarrollo
        : 'http://localhost:5001/api',       // Local en producción
    
    // Servicios en la nube (VMs de Google Cloud)
    CLOUD_CHAT: 'http://34.12.166.76:5000/api',  // Capibara6 Main Server (firewall: tcp:5000)
    CLOUD_CONSENSUS: 'http://34.175.136.104:5003/api',  // Smart MCP Server (firewall: tcp:5003)
    CLOUD_TTS: 'http://34.175.136.104:5004/api',  // Servidor TTS (puerto común para TTS)
    CLOUD_MCP: 'http://34.175.136.104:5010/api',  // Smart MCP Server (firewall: tcp:5010)
    
    // Endpoint de Vercel (proxy)
    VERCEL: 'https://your-vercel-deployment.vercel.app/api'
};

// Función para hacer solicitudes API a los servidores backend
async function makeApiRequest(endpoint, data, serviceType = 'local') {
    try {
        let url;
        
        switch(serviceType) {
            case 'local':
                url = `${API_ENDPOINTS.LOCAL}/${endpoint}`;
                break;
            case 'cloud':
                // Por defecto usar el servidor integrado en la nube
                url = `${API_ENDPOINTS.CLOUD_CHAT}/${endpoint}`;
                break;
            case 'consensus':
                url = `${API_ENDPOINTS.CLOUD_CONSENSUS}/${endpoint}`;
                break;
            case 'tts':
                url = `${API_ENDPOINTS.CLOUD_TTS}/${endpoint}`;
                break;
            case 'mcp':
                url = `${API_ENDPOINTS.CLOUD_MCP}/${endpoint}`;
                break;
            case 'vercel':
                url = `${API_ENDPOINTS.VERCEL}/${endpoint}`;
                break;
            default:
                // Por defecto usar servidor local que incluye CTM y e2b
                url = `${API_ENDPOINTS.LOCAL}/${endpoint}`;
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en la solicitud API:', error);
        throw error;
    }
}
