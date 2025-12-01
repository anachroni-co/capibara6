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
 */

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
        // URLs de servicios (usar variables de entorno o defaults)
        const VLLM_URL = process.env.VLLM_URL || 'http://34.175.48.2:8080/v1/chat/completions';
        const OLLAMA_URL = process.env.OLLAMA_URL || 'http://34.175.48.2:11434/api/generate';

        console.log('📡 Intentando vLLM Multi-Model Server...');

        // PRINCIPAL: Intentar con vLLM (OpenAI compatible)
        try {
            const vllmResponse = await fetch(VLLM_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: req.body.model || 'phi4_fast',
                    messages: req.body.messages || [{ role: 'user', content: req.body.prompt || req.body.message }],
                    temperature: req.body.temperature || 0.7,
                    max_tokens: req.body.max_tokens || 200,
                    stream: req.body.stream || false
                }),
                signal: AbortSignal.timeout(30000) // 30 segundos
            });

            if (vllmResponse.ok) {
                console.log('✅ vLLM respondió exitosamente');
                const data = await vllmResponse.json();
                return res.status(200).json({
                    response: data.choices[0].message.content,
                    model: data.model,
                    provider: 'vLLM',
                    tokens: data.usage?.total_tokens
                });
            }
        } catch (vllmError) {
            console.log('⚠️ vLLM no disponible, intentando Ollama fallback...', vllmError.message);
        }

        // FALLBACK: Ollama
        console.log('📡 Usando Ollama como fallback...');
        const ollamaResponse = await fetch(OLLAMA_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: req.body.ollama_model || 'gpt-oss:20b',
                prompt: req.body.prompt || req.body.message || (req.body.messages && req.body.messages[req.body.messages.length - 1].content),
                stream: false,
                options: {
                    temperature: req.body.temperature || 0.7,
                    num_predict: req.body.max_tokens || 200
                }
            }),
            signal: AbortSignal.timeout(30000)
        });

        if (ollamaResponse.ok) {
            console.log('✅ Ollama fallback exitoso');
            const data = await ollamaResponse.json();
            return res.status(200).json({
                response: data.response,
                model: data.model,
                provider: 'Ollama (fallback)',
                done: data.done
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
        console.error('❌ Error en proxy:', error);

        return res.status(500).json({
            error: 'Error al conectar con los servicios de IA',
            details: error.message,
            fallback: true
        });
    }
}

