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
        const VLLM_URL = process.env.VLLM_URL || 'http://34.175.48.2:8080/v1/chat/completions';
        const OLLAMA_URL = process.env.OLLAMA_URL || 'http://34.175.48.2:11434/api/generate';

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

        console.log('📡 Intentando vLLM y Ollama concurrentemente...');

        // Hacer solicitudes concurrentes con timeouts reducidos
        const [vllmPromise, ollamaPromise] = [
            fetchWithTimeout(VLLM_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(vllmPayload)
            }, 15000), // Reducido a 15 segundos

            fetchWithTimeout(OLLAMA_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(ollamaPayload)
            }, 15000) // Reducido a 15 segundos
        ];

        // Esperar la primera respuesta exitosa
        let vllmResponse = null;
        let ollamaResponse = null;
        let responseCompleted = false;

        // Manejar ambas promesas concurrentemente
        try {
            // Esperar resultados con manejo concurrente
            const vllmResult = vllmPromise.catch(err => {
                console.log('⚠️ vLLM falló:', err.message);
                return null;
            });

            const ollamaResult = ollamaPromise.catch(err => {
                console.log('⚠️ Ollama falló:', err.message);
                return null;
            });

            // Esperar resultados
            [vllmResponse, ollamaResponse] = await Promise.all([vllmResult, ollamaResult]);

            // Procesar la primera respuesta exitosa
            if (vllmResponse && vllmResponse.ok) {
                console.log('✅ vLLM respondió exitosamente');
                const data = await vllmResponse.json();
                const responseData = {
                    response: data.choices[0]?.message?.content || data.response,
                    model: data.model || model,
                    provider: 'vLLM',
                    tokens: data.usage?.total_tokens
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
            }

            if (ollamaResponse && ollamaResponse.ok) {
                console.log('✅ Ollama respondió exitosamente');
                const data = await ollamaResponse.json();
                const responseData = {
                    response: data.response,
                    model: data.model || ollamaPayload.model,
                    provider: 'Ollama',
                    done: data.done
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
            }
        } catch (error) {
            console.error('❌ Error en promesas concurrentes:', error.message);
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

