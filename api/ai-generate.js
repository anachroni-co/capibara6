/**
 * Vercel Serverless Function - AI Generate
 * Endpoint principal para generación de respuestas de IA
 *
 * Este es el endpoint que el frontend llama para chat completions
 * Usa vLLM como principal y Ollama como fallback
 *
 * Actualizado: 2025-12-01
 */

export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const {
      message,
      prompt,
      text,
      model,
      temperature = 0.7,
      max_tokens = 500,
      stream = false
    } = req.body;

    const userMessage = message || prompt || text || '';

    if (!userMessage) {
      return res.status(400).json({
        error: 'Message, prompt or text is required'
      });
    }

    // URLs de servicios
    const VLLM_URL = process.env.VLLM_URL || 'http://34.175.48.2:8080/v1/chat/completions';
    const OLLAMA_URL = process.env.OLLAMA_URL || 'http://34.175.48.2:11434/api/generate';

    console.log(`📨 Mensaje recibido: ${userMessage.substring(0, 50)}...`);
    console.log(`🎯 Modelo solicitado: ${model || 'auto'}`);

    // PRINCIPAL: Intentar con vLLM Multi-Model Server
    try {
      console.log('📡 Intentando vLLM Multi-Model Server...');

      const vllmResponse = await fetch(VLLM_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: model || 'phi4_fast',
          messages: [
            {
              role: 'system',
              content: 'Eres Capibara6, un asistente de IA experto y útil de Anachroni s.coop. Respondes en español de forma clara y concisa.'
            },
            {
              role: 'user',
              content: userMessage
            }
          ],
          temperature: temperature,
          max_tokens: max_tokens,
          stream: false
        }),
        signal: AbortSignal.timeout(30000)
      });

      if (vllmResponse.ok) {
        const data = await vllmResponse.json();
        console.log('✅ vLLM respondió exitosamente');

        return res.status(200).json({
          response: data.choices[0].message.content,
          content: data.choices[0].message.content,
          model: data.model || model || 'phi4_fast',
          provider: 'vLLM Multi-Model',
          tokens: data.usage?.total_tokens,
          finish_reason: data.choices[0].finish_reason
        });
      }
    } catch (vllmError) {
      console.log('⚠️ vLLM no disponible:', vllmError.message);
      console.log('📡 Cambiando a Ollama fallback...');
    }

    // FALLBACK: Ollama
    console.log('📡 Usando Ollama como fallback...');
    const ollamaResponse = await fetch(OLLAMA_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-oss:20b',
        prompt: `Eres Capibara6, un asistente de IA de Anachroni s.coop. Responde en español de forma clara.\n\nUsuario: ${userMessage}\n\nAsistente:`,
        stream: false,
        options: {
          temperature: temperature,
          num_predict: max_tokens
        }
      }),
      signal: AbortSignal.timeout(30000)
    });

    if (ollamaResponse.ok) {
      const data = await ollamaResponse.json();
      console.log('✅ Ollama fallback exitoso');

      return res.status(200).json({
        response: data.response,
        content: data.response,
        model: 'gpt-oss:20b',
        provider: 'Ollama (fallback)',
        done: data.done
      });
    }

    // Si ambos fallan
    throw new Error('Todos los servicios de IA no están disponibles');

  } catch (error) {
    console.error('❌ Error en AI Generate:', error);

    return res.status(503).json({
      error: 'Servicios de IA temporalmente no disponibles',
      message: 'Por favor, intenta de nuevo en unos momentos.',
      details: error.message,
      fallback: true
    });
  }
}
