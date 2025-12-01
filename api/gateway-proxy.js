/**
 * Vercel Serverless Function - Gateway Proxy
 * Proxy HTTPS para el servicio Gateway en VM services
 * Permite a Vercel conectarse al gateway server que enruta a vLLM/Ollama
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

    // Solo permitir POST para completions
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        // URL base del gateway en la VM services
        const GATEWAY_BASE_URL = process.env.GATEWAY_URL || 'http://34.175.136.104:8080';
        const GATEWAY_CHAT_URL = `${GATEWAY_BASE_URL}/api/chat`;
        
        // Preparar opciones para fetch con timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 45000); // 45 segundos timeout
        
        const fetchOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...req.headers,
                // Asegurar que no se pasen encabezados problemáticos
                'host': undefined,
                'content-length': undefined,
                'connection': undefined,
            },
            signal: controller.signal
        };
        
        // Incluir body
        if (req.body) {
            fetchOptions.body = JSON.stringify(req.body);
        }
        
        try {
            // Hacer la solicitud al gateway
            const gatewayResponse = await fetch(GATEWAY_CHAT_URL, fetchOptions);
            clearTimeout(timeoutId);
            
            // Obtener el cuerpo de la respuesta
            const responseText = await gatewayResponse.text();
            
            // Devolver la respuesta con el mismo status code
            res.status(gatewayResponse.status);
            
            try {
                // Si la respuesta es JSON válida, devolver como JSON
                const jsonData = responseText ? JSON.parse(responseText) : {};
                res.json(jsonData);
            } catch (e) {
                // Si no es JSON, devolver como texto
                res.setHeader('Content-Type', 'text/plain');
                res.send(responseText);
            }
            
        } catch (fetchError) {
            clearTimeout(timeoutId);
            if (fetchError.name === 'AbortError') {
                console.error('❌ Timeout en solicitud al gateway:', GATEWAY_CHAT_URL);
                res.status(408).json({
                    error: 'Tiempo de espera agotado al conectar con el gateway',
                    service: 'gateway'
                });
            } else {
                console.error('❌ Error en solicitud al gateway:', fetchError.message);
                res.status(503).json({
                    error: 'Error al conectar con el gateway de IA',
                    details: fetchError.message,
                    service: 'gateway'
                });
            }
        }
        
    } catch (error) {
        console.error('❌ Error general en gateway proxy:', error);
        res.status(500).json({
            error: 'Error interno en el proxy del gateway',
            details: error.message
        });
    }
}

export const config = {
    api: {
        bodyParser: {
            sizeLimit: '10mb',
        },
    },
};