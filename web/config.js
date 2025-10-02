// Configuración del chatbot capibara6

const CHATBOT_CONFIG = {
    // URL del backend
    // En desarrollo: 'http://localhost:5000'
    // En producción: Cambia esto por tu URL de Railway
    BACKEND_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000'
        : 'https://TU-PROYECTO.up.railway.app', // 👈 CAMBIA ESTO después de desplegar en Railway
    
    // Endpoints
    ENDPOINTS: {
        SAVE_CONVERSATION: '/api/save-conversation',
        HEALTH: '/api/health'
    }
};

