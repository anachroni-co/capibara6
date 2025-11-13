// Configuración para usar proxy CORS local
// Este archivo debe cargarse ANTES de config.js

// Detectar proxy CORS local automáticamente
const CORS_PROXY_URL = (() => {
    // IPs conocidas del proxy CORS local
    const PROXY_IPS = [
        '172.22.134.254',  // IP detectada
        'localhost',
        '127.0.0.1'
    ];
    
    const PROXY_PORTS = [8001, 5001];
    
    // Intentar detectar proxy automáticamente
    // Por ahora usar la IP detectada
    return 'http://172.22.134.254:8001';
})();

// Configurar para usar proxy
window.CORS_PROXY_URL = CORS_PROXY_URL;

console.log('🔧 Proxy CORS configurado:', CORS_PROXY_URL);

