/**
 * Vercel Serverless Function - Chat Completions
 * Proxy HTTPS para vLLM Multi-Model Server con fallback a Ollama
 *
 * Arquitectura:
 * - PRINCIPAL: vLLM Multi-Model Server (models-europe:8080)
 *   - 5 modelos: phi4_fast, mistral_balanced, qwen_coder, gemma3_multimodal, aya_expanse
 *   - Sistema de consenso y routing inteligente
 * - FALLBACK: Ollama (models-europe:11434)
 *   - 4 modelos: gpt-oss:20b, mistral:latest, phi3:mini, smollm2:135m
 *
 * Actualizado: 2025-12-01
 * Mejoras: Timeout reducido, conexión concurrente, manejo de caché
 */

// Simple cache en memoria para respuestas (limitado por la naturaleza serverless de Vercel)
const RESPONSE_CACHE = new Map();
const CACHE_TTL = 300000; // 5 minutos en ms

// Función para generar clave de caché
function generateCacheKey(prompt, model, temperature) {
    return `${prompt}-${model || 'default'}-${temperature || 0.7}`;
}

// Función para limpiar entradas de caché expiradas
function cleanupCache() {
    const now = Date.now();
    for (const [key, { timestamp }] of RESPONSE_CACHE.entries()) {
        if (now - timestamp > CACHE_TTL) {
            RESPONSE_CACHE.delete(key);
        }
    }
}

// Función auxiliar para hacer fetch con timeout
async function fetchWithTimeout(url, options, timeoutMs) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        throw error;
    }
}

export default async function handler(req, res) {
    // CORS headers (se aplican siempre)
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    // Handle preflight (OPTIONS) immediately
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    // Solo permitir POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        // Extraer parámetros
        const prompt = req.body.prompt || req.body.message || (req.body.messages && req.body.messages[req.body.messages.length - 1].content);
        const model = req.body.model || 'phi4_fast';
        const temperature = req.body.temperature || 0.7;
        const max_tokens = req.body.max_tokens || 200;

        // Verificar cache antes de hacer peticiones
        if (prompt) {
            const cacheKey = generateCacheKey(prompt, model, temperature);
            cleanupCache(); // Limpiar entradas expiradas

            const cachedResponse = RESPONSE_CACHE.get(cacheKey);
            if (cachedResponse && Date.now() - cachedResponse.timestamp < CACHE_TTL) {
                console.log('✅ Respuesta desde caché');
                return res.status(200).json(cachedResponse.data);
            }
        }

        // URLs de servicios (usar variables de entorno o defaults)
        // Usar el gateway server en VM services como intermediario
        const GATEWAY_URL = process.env.GATEWAY_URL || 'http://34.175.136.104:8080';
        const CHAT_URL = `${GATEWAY_URL}/api/chat`;

        // Preparar payloads para ambas solicitudes
        const vllmPayload = {
            model: model,
            messages: req.body.messages || [{ role: 'user', content: prompt }],
            temperature: temperature,
            max_tokens: max_tokens,
            stream: req.body.stream || false
        };

        const ollamaPayload = {
            model: req.body.ollama_model || 'gpt-oss:20b',
            prompt: prompt,
            stream: false,
            options: {
                temperature: temperature,
                num_predict: max_tokens
            }
        };

        console.log('📡 Enviando solicitud al gateway server...');

        // Preparar payload para el gateway
        const gatewayPayload = {
            message: prompt,
            model: model,
            use_semantic_router: true,
            temperature: temperature,
            max_tokens: max_tokens
        };

        // Si hay mensajes anteriores en la conversación, incluirlos también
        if (req.body.messages && req.body.messages.length > 0) {
            // El gateway manejará el contexto si tiene semantic routing
            gatewayPayload.messages = req.body.messages;
        }

        // Hacer solicitud al gateway server
        try {
            const gatewayResponse = await fetchWithTimeout(CHAT_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(gatewayPayload)
            }, 25000); // Timeout más largo para procesamiento completo

            if (gatewayResponse.ok) {
                console.log('✅ Gateway respondió exitosamente');
                const data = await gatewayResponse.json();

                // Adaptar la respuesta del gateway a la estructura esperada
                const responseData = {
                    response: data.response,
                    model: data.model || model,
                    provider: 'gateway',
                    tokens: data.tokens,
                    routing_info: data.routing_info
                };

                // Almacenar en caché si hay prompt
                if (prompt) {
                    const cacheKey = generateCacheKey(prompt, model, temperature);
                    RESPONSE_CACHE.set(cacheKey, {
                        data: responseData,
                        timestamp: Date.now()
                    });
                }

                return res.status(200).json(responseData);
            } else {
                console.log(`❌ Gateway respondió con status: ${gatewayResponse.status}`);
                const errorText = await gatewayResponse.text();
                console.error('Error del gateway:', errorText);

                return res.status(503).json({
                    error: 'Servicio de IA no disponible a través del gateway',
                    gateway_status: gatewayResponse.status,
                    details: errorText
                });
            }
        } catch (error) {
            console.error('❌ Error conectando con el gateway:', error.message);

            return res.status(503).json({
                error: 'Error al conectar con el gateway de IA',
                details: error.message
            });
        }

        // Si ambos fallan, mensaje de error
        console.log('❌ Todos los servicios fallaron');
        return res.status(503).json({
            error: 'Servicios de IA temporalmente no disponibles',
            message: 'Tanto vLLM como Ollama no están respondiendo. Por favor, intenta más tarde.',
            fallback: true
        });

    } catch (error) {
        console.error('❌ Error general en proxy:', error);
        return res.status(500).json({
            error: 'Error al conectar con los servicios de IA',
            details: error.message,
            fallback: true
        });
    }
}

