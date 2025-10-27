/**
 * Vercel Serverless Function
 * Proxy HTTPS para el modelo Gemma en la VM
 * Resuelve el problema de Mixed Content
 */

export default async function handler(req, res) {
    // Solo permitir POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    try {
        // URL del modelo en la VM (HTTP está OK en server-side)
        const MODEL_URL = 'http://34.175.215.109:8080/completion';
        
        // Reenviar la petición a la VM
        const response = await fetch(MODEL_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req.body)
        });

        // Si la VM no está disponible, usar fallback
        if (!response.ok) {
            console.log('⚠️ VM no disponible, usando fallback...');
            return res.status(200).json({
                content: "Lo siento, el modelo de IA no está disponible en este momento. Por favor, intenta más tarde o contacta al administrador.",
                stop: true
            });
        }

        // Si es streaming, manejar como stream
        if (req.body.stream) {
            res.setHeader('Content-Type', 'text/event-stream');
            res.setHeader('Cache-Control', 'no-cache');
            res.setHeader('Connection', 'keep-alive');

            // Pipe the response
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                res.write(chunk);
            }

            res.end();
        } else {
            // Respuesta normal (no streaming)
            const data = await response.json();
            res.status(response.status).json(data);
        }

    } catch (error) {
        console.error('Proxy error:', error);
        
        // Si es error de conexión, usar fallback en lugar de error 500
        if (error.message.includes('fetch failed') || error.message.includes('ECONNREFUSED')) {
            console.log('⚠️ Error de conexión, usando fallback...');
            return res.status(200).json({
                content: "Lo siento, el modelo de IA no está disponible en este momento. Por favor, intenta más tarde o contacta al administrador.",
                stop: true
            });
        }
        
        res.status(500).json({ 
            error: 'Error al conectar con el modelo',
            details: error.message 
        });
    }
}

