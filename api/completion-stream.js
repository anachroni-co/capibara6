/**
 * Vercel Serverless Function - Chat Completions con Streaming
 * Proxy HTTPS para vLLM Multi-Model Server con streaming y contexto
 */

export const config = {
  api: {
    responseLimit: false,
    bodyParser: {
      sizeLimit: '10mb',
    },
  },
};

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

  // Configurar para streaming
  res.writeHead(200, {
    'Content-Type': 'text/plain; charset=utf-8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Transfer-Encoding': 'chunked',
  });

  try {
    // URLs de servicios (usar variables de entorno o defaults)
    const VLLM_URL = process.env.VLLM_URL || 'http://34.175.48.2:8080/v1/chat/completions';
    const OLLAMA_URL = process.env.OLLAMA_URL || 'http://34.175.48.2:11434/api/generate';

    // Extraer parámetros
    const prompt = req.body.prompt || req.body.message || (req.body.messages && req.body.messages[req.body.messages.length - 1]?.content);
    const model = req.body.model || 'phi4_fast';
    const temperature = req.body.temperature || 0.7;
    const max_tokens = req.body.max_tokens || 200;
    
    // Preparar mensajes con contexto más completo
    const messages = req.body.messages && req.body.messages.length > 0 
      ? [...req.body.messages] 
      : [{ role: 'user', content: prompt }];

    // Payload para vLLM con streaming
    const vllmPayload = {
      model: model,
      messages: messages,
      temperature: temperature,
      max_tokens: max_tokens,
      stream: true, // Activar streaming
    };

    // Hacer solicitud a vLLM con streaming
    const vllmResponse = await fetch(VLLM_URL, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(vllmPayload),
      signal: AbortSignal.timeout(30000) // 30 segundos
    });

    if (vllmResponse.ok && vllmResponse.body) {
      // Procesar el stream
      const reader = vllmResponse.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      // Enviar inicio de stream
      res.write('data: {"type": "start"}\n\n');

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          
          // Procesar líneas completas
          const lines = buffer.split(/\r?\n/);
          buffer = lines.pop() || ''; // Mantener la última línea incompleta

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6); // Quitar 'data: '
              if (data === '[DONE]') {
                break;
              }
              
              try {
                const parsed = JSON.parse(data);
                const content = parsed.choices?.[0]?.delta?.content;
                
                if (content) {
                  // Enviar el contenido al cliente
                  res.write(`data: ${JSON.stringify({ type: 'content', content })}\n\n`);
                  res.flush ? res.flush() : void 0; // Forzar envío si está disponible
                }
                
                // Enviar done si terminó
                if (parsed.choices?.[0]?.finish_reason) {
                  res.write(`data: ${JSON.stringify({ type: 'done', finish_reason: parsed.choices[0].finish_reason })}\n\n`);
                }
              } catch (e) {
                // Si no es JSON, puede ser un error, continuar
                console.error('Error parsing stream data:', e);
              }
            }
          }
        }
      } finally {
        reader.releaseLock();
      }

      // Enviar finalización
      res.write(`data: ${JSON.stringify({ type: 'complete' })}\n\n`);
      res.end();
    } else {
      // Si vLLM no funciona, intentar Ollama
      const ollamaPayload = {
        model: req.body.ollama_model || 'gpt-oss:20b',
        prompt: prompt,
        stream: true,
        options: {
          temperature: temperature,
          num_predict: max_tokens
        }
      };

      const ollamaResponse = await fetch(OLLAMA_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ollamaPayload),
        signal: AbortSignal.timeout(30000)
      });

      if (ollamaResponse.ok) {
        // Procesar stream de Ollama
        const reader = ollamaResponse.body.getReader();
        const decoder = new TextDecoder();

        res.write('data: {"type": "start"}\n\n');

        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            // Procesar respuesta de Ollama
            const lines = chunk.split('\n');
            for (const line of lines) {
              if (line.trim()) {
                try {
                  const parsed = JSON.parse(line);
                  if (parsed.response) {
                    res.write(`data: ${JSON.stringify({ type: 'content', content: parsed.response })}\n\n`);
                  }
                  if (parsed.done) {
                    res.write(`data: ${JSON.stringify({ type: 'done' })}\n\n`);
                  }
                } catch (e) {
                  // Ignorar líneas que no son JSON
                }
              }
            }
          }
        } finally {
          reader.releaseLock();
        }

        res.write(`data: ${JSON.stringify({ type: 'complete' })}\n\n`);
        res.end();
      } else {
        res.write(`data: ${JSON.stringify({ error: 'Servicios no disponibles' })}\n\n`);
        res.end();
      }
    }
  } catch (error) {
    console.error('❌ Error en proxy streaming:', error);
    res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
    res.end();
  }
}