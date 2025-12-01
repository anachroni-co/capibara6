/**
 * Vercel Serverless Function - N8N Proxy
 * Proxy HTTPS para el servicio N8N en VM services
 *
 * Arquitectura:
 * - N8N corriendo en VM services (34.175.136.104:5678)
 * - Proxy que permite acceso desde frontend con CORS resuelto
 */

export default async function handler(req, res) {
    // CORS headers (se aplican siempre)
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');

    // Handle preflight (OPTIONS) immediately
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    try {
        // URL de N8N en la VM services
        const N8N_BASE_URL = process.env.N8N_URL || 'http://34.175.136.104:5678';
        
        // Obtener el path de la solicitud y construir URL completa
        const { path = '' } = req.query;
        const n8nPath = Array.isArray(path) ? path.join('/') : path;
        const n8nUrl = `${N8N_BASE_URL}/${n8nPath}`;
        
        // Obtener el cuerpo de la solicitud si existe
        const body = req.body ? JSON.stringify(req.body) : null;
        
        // Preparar opciones para fetch
        const fetchOptions = {
            method: req.method,
            headers: {
                'Content-Type': 'application/json',
                ...req.headers,
            }
        };
        
        // Solo incluir body si hay datos
        if (body) {
            fetchOptions.body = body;
        }
        
        // Hacer la solicitud a N8N
        const n8nResponse = await fetch(n8nUrl, fetchOptions);
        
        // Obtener el cuerpo de la respuesta
        const responseText = await n8nResponse.text();
        
        // Devolver la respuesta con el mismo status code
        res.status(n8nResponse.status).json({
            status: n8nResponse.status,
            statusText: n8nResponse.statusText,
            body: responseText ? JSON.parse(responseText) : null
        });
        
    } catch (error) {
        console.error('❌ Error en N8N proxy:', error);
        res.status(500).json({
            error: 'Error al conectar con el servicio N8N',
            details: error.message
        });
    }
}

export const config = {
    api: {
        // Permite recibir cuerpos grandes para workflows de N8N
        bodyParser: {
            sizeLimit: '10mb',
        },
    },
};