// Proxy para conectar con la VM models-europe desde Vercel
export default async function handler(req, res) {
    // Configurar CORS más restrictivo
    const allowedOrigin = process.env.NODE_ENV === 'production'
        ? 'https://www.capibara6.com'
        : 'http://localhost:3000';

    res.setHeader('Access-Control-Allow-Origin', allowedOrigin);
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    try {
        const { message, model, temperature, max_tokens, use_semantic_router } = req.body;

        // Preparar payload para conectar con VM models-europe
        const payload = {
            model: model || 'aya_expanse_multilingual',
            messages: [{ role: 'user', content: message || '' }],
            temperature: temperature || 0.7,
            max_tokens: max_tokens || 200,
            use_semantic_router: use_semantic_router || false // Asegurar que se maneje esta propiedad
        };

        // Conectar al gateway server en VM services (IP externa) que enruta a la VM models-europe
        const response = await fetch('http://34.175.48.1:8080/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            timeout: 30000 // 30 segundos de timeout
        });

        const data = await response.json();

        // Verificar si el backend ya devolvió una respuesta simulada
        if (data.status && (data.status.includes('simulated') || data.status.includes('fallback'))) {
            // El backend ya manejó el fallback, devolver la respuesta tal cual
            return res.status(200).json(data);
        }

        return res.status(response.status).json(data);

    } catch (error) {
        console.error('Error en proxy a VM services gateway:', error);

        // En lugar de devolver respuesta simulada, dejar que sea el gateway server quien la maneje
        // Si llegamos aquí es porque no pudimos conectar al gateway server en absoluto
        return res.status(503).json({
            error: 'Service unavailable',
            message: 'No se puede conectar al gateway server'
        });
    }
}
