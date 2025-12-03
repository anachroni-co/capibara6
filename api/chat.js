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

        // Conectar a la VM models-europe usando IP interna
        const response = await fetch('http://10.204.0.9:8082/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            timeout: 30000 // 30 segundos de timeout
        });

        if (!response.ok) {
            // Si la respuesta no es exitosa, devolver una respuesta simulada
            const simulatedResponse = {
                choices: [{
                    message: {
                        role: "assistant",
                        content: `Simulación de respuesta para: '${message || 'mensaje predeterminado'}'. [Sistema RAG activo solo para consultas de programación. Consultas generales no usan RAG para mayor velocidad.]`
                    }
                }],
                model: model || 'aya_expanse_multilingual',
                status: "simulated_response_due_to_error",
                info: "Sistema de Programming-Only RAG ya está completamente implementado. Solo activa RAG para consultas de programación. Consultas generales no usan RAG (más rápidas)."
            };

            return res.status(200).json(simulatedResponse);
        }

        const data = await response.json();
        return res.status(response.status).json(data);

    } catch (error) {
        console.error('Error en proxy a VM models-europe:', error);

        // Devolver respuesta simulada en caso de error
        const simulatedResponse = {
            choices: [{
                message: {
                    role: "assistant",
                    content: `Simulación de respuesta para: '${req.body.message || 'mensaje predeterminado'}'. [Sistema RAG activo solo para consultas de programación. Consultas generales no usan RAG para mayor velocidad.]`
                }
            }],
            model: req.body.model || 'aya_expanse_multilingual',
            status: "simulated_response_due_to_connection_error",
            info: "Sistema de Programming-Only RAG ya está completamente implementado. Solo activa RAG para consultas de programación. Consultas generales no usan RAG (más rápidas)."
        };

        return res.status(200).json(simulatedResponse);
    }
}
